#!/usr/bin/env python3
"""Validate OpenCode Engineering Harness configuration, contracts, and project readiness.

Modes:
  --mode template (default): Validates the blueprint repository itself (CI gate).
  --mode project           : Runs all template checks plus adopter readiness checks
                             (AGENTS.md TODO placeholders, Spec Kit constitution, CLIs).
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import fnmatch
import json
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any

EXPECTED_SCHEMA = "https://opencode.ai/config.json"
EXPECTED_COMMON_RULES = [
    ".opencode/rules/common/communication.md",
    ".opencode/rules/common/context-management.md",
    ".opencode/rules/common/delegation.md",
    ".opencode/rules/common/tool-use.md",
    ".opencode/rules/common/autonomy-and-safety.md",
    ".opencode/rules/common/collaboration.md",
    ".opencode/rules/common/evidence-and-reporting.md",
]
VALID_V2_ROOT_KEYS = {
    "$schema",
    "shell",
    "model",
    "default_agent",
    "update",
    "share",
    "enterprise",
    "username",
    "timezone",
    "permissions",
    "policies",
    "agents",
    "snapshots",
    "watcher",
    "formatter",
    "lsp",
    "media",
    "tool_output",
    "mcp",
    "compaction",
    "skills",
    "commands",
    "instructions",
    "references",
    "websearch",
    "plugins",
    "worktree",
    "warming",
    "providers",
    "experimental",
    "logLevel",
    "server",
}
DEPRECATED_V1_ROOT_KEYS = {
    "permission",
    "tools",
    "agent",
    "mode",
    "command",
    "reference",
    "snapshot",
    "plugin",
    "autoshare",
    "autoupdate",
    "disabled_providers",
    "enabled_providers",
    "small_model",
    "subagent_depth",
    "provider",
    "layout",
    "attachment",
}
VALID_V2_AGENT_KEYS = {
    "description",
    "mode",
    "model",
    "permissions",
    "steps",
    "hidden",
    "color",
    "disabled",
    "request",
    "system",
}
DEPRECATED_V1_AGENT_KEYS = {
    "permission",
    "tools",
    "prompt",
    "maxSteps",
    "disable",
    "temperature",
    "top_p",
}
VALID_V2_PERMISSION_ACTIONS = {
    "*",
    "read",
    "edit",
    "glob",
    "grep",
    "shell",
    "subagent",
    "skill",
    "question",
    "webfetch",
    "websearch",
    "experimental_image_generate",
    "external_directory",
    "opencode_list_mcp_resources",
    "opencode_read_mcp_resource",
    "execute",
    "browser",
}
DEPRECATED_V1_PERMISSION_ACTIONS = {
    "write",
    "patch",
    "bash",
    "task",
    "doom_loop",
    "lsp",
    "todowrite",
}
MCP_ACTION_PATTERN = re.compile(r"^[a-z0-9]+_[a-z0-9_]+$")
VALID_EFFECTS = {"allow", "ask", "deny"}
VALID_AGENT_MODES = {"primary", "subagent", "all"}
STARTER_TECH_SKILLS = {"postgresql", "spring-boot", "react-typescript", "terraform"}
REQUIRED_TECH_SKILL_HEADINGS = [
    "## Supported scope",
    "## When to load",
    "## Before implementation",
    "## Implementation standards",
    "## Testing and verification",
    "## Completion checklist",
    "## References",
]
REQUIRED_IGNORE_PATTERNS = [
    ".env",
    ".env.*",
    "!.env.example",
    "*.pem",
    "*.key",
    ".aws/",
    ".ssh/",
    "secrets/",
    "*credentials*",
]
MAX_ALWAYS_ON_ESTIMATED_TOKENS = 7000
SKILL_ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclasses.dataclass
class CheckFinding:
    level: str  # "PASS", "WARN", "FAIL"
    category: str
    message: str


def strip_jsonc(text: str) -> str:
    """Remove // and /* */ comments and trailing commas outside JSON string literals."""
    result: list[str] = []
    i = 0
    n = len(text)
    in_string = False
    while i < n:
        ch = text[i]
        if in_string:
            result.append(ch)
            if ch == "\\" and i + 1 < n:
                i += 1
                result.append(text[i])
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
        elif ch == "/" and i + 1 < n and text[i + 1] == "/":
            i += 2
            while i < n and text[i] not in "\r\n":
                i += 1
        elif ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
        else:
            result.append(ch)
            i += 1

    without_comments = "".join(result)
    cleaned: list[str] = []
    i = 0
    n = len(without_comments)
    in_string = False
    while i < n:
        ch = without_comments[i]
        if in_string:
            cleaned.append(ch)
            if ch == "\\" and i + 1 < n:
                i += 1
                cleaned.append(without_comments[i])
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            cleaned.append(ch)
            i += 1
            continue

        if ch == ",":
            j = i + 1
            while j < n and without_comments[j] in " \t\r\n":
                j += 1
            if j < n and without_comments[j] in "}]":
                i += 1
                continue

        cleaned.append(ch)
        i += 1

    return "".join(cleaned)


def parse_jsonc(text: str) -> Any:
    return json.loads(strip_jsonc(text))


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def parse_frontmatter(markdown_text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter used in OpenCode agent and skill Markdown files."""
    if not markdown_text.startswith("---\n") and not markdown_text.startswith("---\r\n"):
        raise ValueError("Missing opening YAML frontmatter delimiter '---'")

    lines = markdown_text.splitlines()
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("Missing closing YAML frontmatter delimiter '---'")

    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :])
    data: dict[str, Any] = {}
    i = 0
    while i < len(fm_lines):
        raw_line = fm_lines[i]
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            raise ValueError(f"Unexpected indentation in frontmatter line: {raw_line!r}")
        if ":" not in raw_line:
            raise ValueError(f"Invalid frontmatter entry: {raw_line!r}")

        key, rest = raw_line.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if rest:
            data[key] = _unquote(rest)
            i += 1
            continue

        items: list[dict[str, str]] = []
        nested_map: dict[str, str] = {}
        i += 1
        while i < len(fm_lines):
            sub_raw = fm_lines[i]
            sub_stripped = sub_raw.strip()
            if not sub_stripped or sub_stripped.startswith("#"):
                i += 1
                continue
            if not (sub_raw.startswith(" ") or sub_raw.startswith("\t")):
                break

            if sub_stripped.startswith("- "):
                item: dict[str, str] = {}
                first_kv = sub_stripped[2:].strip()
                if ":" not in first_kv:
                    raise ValueError(f"Unsupported list item in frontmatter: {sub_raw!r}")
                ik, iv = first_kv.split(":", 1)
                item[ik.strip()] = _unquote(iv)
                item_indent = len(sub_raw) - len(sub_raw.lstrip())
                i += 1
                while i < len(fm_lines):
                    cont_raw = fm_lines[i]
                    cont_stripped = cont_raw.strip()
                    if not cont_stripped or cont_stripped.startswith("#"):
                        i += 1
                        continue
                    cont_indent = len(cont_raw) - len(cont_raw.lstrip())
                    if cont_indent <= item_indent or cont_stripped.startswith("- "):
                        break
                    if ":" not in cont_stripped:
                        raise ValueError(f"Invalid mapping line in list item: {cont_raw!r}")
                    ck, cv = cont_stripped.split(":", 1)
                    item[ck.strip()] = _unquote(cv)
                    i += 1
                items.append(item)
            elif ":" in sub_stripped:
                nk, nv = sub_stripped.split(":", 1)
                nested_map[nk.strip()] = _unquote(nv)
                i += 1
            else:
                raise ValueError(f"Unsupported nested structure in frontmatter: {sub_raw!r}")

        data[key] = items if items else nested_map

    return data, body


def wildcard_match(pattern: str, value: str, *, is_shell: bool = False) -> bool:
    """Match OpenCode V2 wildcard pattern ('*' matches any chars including '/', '?' matches 1 char)."""
    if is_shell and pattern.endswith(" *") and value == pattern[:-2]:
        return True
    regex_parts = ["^"]
    for ch in pattern:
        if ch == "*":
            regex_parts.append(".*")
        elif ch == "?":
            regex_parts.append(".")
        else:
            regex_parts.append(re.escape(ch))
    regex_parts.append("$")
    return re.match("".join(regex_parts), value) is not None


def resolve_permission(
    rules: list[dict[str, str]],
    action: str,
    resource: str,
    *,
    default: str = "ask",
) -> str:
    """Evaluate OpenCode V2 permission rules in order; last matching rule wins."""
    effect = default
    is_shell = action == "shell"
    for rule in rules:
        rule_action = rule.get("action", "")
        rule_resource = rule.get("resource", "")
        rule_effect = rule.get("effect", "")
        if wildcard_match(rule_action, action) and wildcard_match(
            rule_resource, resource, is_shell=is_shell
        ):
            effect = rule_effect
    return effect


def is_valid_v2_action(action: str) -> bool:
    if action in DEPRECATED_V1_PERMISSION_ACTIONS:
        return False
    if action in VALID_V2_PERMISSION_ACTIONS:
        return True
    return bool(MCP_ACTION_PATTERN.match(action))


def validate_permission_list(
    rules: Any, source_label: str, findings: list[CheckFinding]
) -> list[dict[str, str]]:
    if not isinstance(rules, list) or not rules:
        findings.append(
            CheckFinding("FAIL", "permissions", f"{source_label} must define a non-empty permissions list.")
        )
        return []
    valid_rules: list[dict[str, str]] = []
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            findings.append(
                CheckFinding("FAIL", "permissions", f"{source_label} rule #{idx + 1} must be an object.")
            )
            continue
        action = rule.get("action")
        resource = rule.get("resource")
        effect = rule.get("effect")
        if (
            not isinstance(action, str)
            or not action
            or not isinstance(resource, str)
            or not resource
            or effect not in VALID_EFFECTS
        ):
            findings.append(
                CheckFinding(
                    "FAIL",
                    "permissions",
                    f"{source_label} rule #{idx + 1} must have string action/resource and effect in {sorted(VALID_EFFECTS)}.",
                )
            )
            continue
        if action in DEPRECATED_V1_PERMISSION_ACTIONS:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "permissions",
                    f"{source_label} rule #{idx + 1} uses legacy/redundant V1 action {action!r}; in OpenCode V2 'edit' covers edit/write/patch, 'shell' covers bash, and 'subagent' covers task.",
                )
            )
            continue
        if not is_valid_v2_action(action):
            findings.append(
                CheckFinding(
                    "FAIL",
                    "permissions",
                    f"{source_label} rule #{idx + 1} uses unsupported OpenCode V2 permission action {action!r}.",
                )
            )
            continue
        valid_rules.append({"action": action, "resource": resource, "effect": effect})
    return valid_rules


def check_opencode_config(root: pathlib.Path, findings: list[CheckFinding]) -> dict[str, Any] | None:
    config_path = root / "opencode.jsonc"
    if not config_path.is_file():
        findings.append(CheckFinding("FAIL", "config", "Missing root opencode.jsonc file."))
        return None

    try:
        config = parse_jsonc(config_path.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(CheckFinding("FAIL", "config", f"Failed to parse opencode.jsonc: {exc}"))
        return None

    if not isinstance(config, dict):
        findings.append(CheckFinding("FAIL", "config", "opencode.jsonc root must be a JSON object."))
        return None

    if config.get("$schema") != EXPECTED_SCHEMA:
        findings.append(
            CheckFinding(
                "FAIL",
                "config",
                f"opencode.jsonc $schema must be {EXPECTED_SCHEMA!r}, found {config.get('$schema')!r}.",
            )
        )

    legacy_keys = sorted(DEPRECATED_V1_ROOT_KEYS.intersection(config.keys()))
    if legacy_keys:
        findings.append(
            CheckFinding(
                "FAIL",
                "config",
                f"opencode.jsonc contains deprecated OpenCode V1 keys: {legacy_keys}. Use V2 'permissions' and 'agents'.",
            )
        )

    unknown_root_keys = sorted(set(config.keys()) - VALID_V2_ROOT_KEYS - DEPRECATED_V1_ROOT_KEYS)
    if unknown_root_keys:
        findings.append(
            CheckFinding(
                "FAIL",
                "config",
                f"opencode.jsonc contains unknown root keys not in OpenCode V2 schema: {unknown_root_keys}.",
            )
        )

    default_agent = config.get("default_agent")
    if default_agent != "developer":
        findings.append(
            CheckFinding(
                "FAIL",
                "config",
                f"opencode.jsonc default_agent must be 'developer', found {default_agent!r}.",
            )
        )

    instructions = config.get("instructions")
    if not isinstance(instructions, list):
        findings.append(CheckFinding("FAIL", "config", "opencode.jsonc 'instructions' must be a list."))
    else:
        missing_common = [p for p in EXPECTED_COMMON_RULES if p not in instructions]
        if missing_common:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "config",
                    f"opencode.jsonc is missing always-on common rules: {missing_common}.",
                )
            )
        for rel_path in instructions:
            if not isinstance(rel_path, str) or not (root / rel_path).is_file():
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "config",
                        f"opencode.jsonc instruction file does not exist: {rel_path!r}.",
                    )
                )

    rules = validate_permission_list(config.get("permissions"), "opencode.jsonc", findings)
    if rules:
        for safe_sample in ("src/index.ts", "README.md", ".env.example", ".env.sample", ".env.template"):
            eff = resolve_permission(rules, "read", safe_sample)
            if eff != "allow":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc must allow reading safe workspace file {safe_sample!r} (resolved to {eff!r}).",
                    )
                )

        for env_sample in (".env", ".env.local", ".env.production", "services/api/.env"):
            eff = resolve_permission(rules, "read", env_sample)
            if eff not in ("ask", "deny"):
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc allows unrestricted read of {env_sample!r} (resolved to {eff!r}); must be 'ask' or 'deny'.",
                    )
                )

        for secret_sample in (
            "tls/private.key",
            "certs/server.pem",
            "certs/ bundle.p12",
            "certs/client.pfx",
            "id_rsa",
            "id_ed25519",
            ".aws/credentials",
            ".ssh/id_rsa",
            "secrets/prod.json",
            "config/service-credentials.json",
        ):
            eff = resolve_permission(rules, "read", secret_sample)
            if eff != "deny":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc must deny reading sensitive secret/key path {secret_sample!r} (resolved to {eff!r}).",
                    )
                )

        ext_eff = resolve_permission(rules, "external_directory", "../outside-project/*")
        if ext_eff not in ("ask", "deny"):
            findings.append(
                CheckFinding(
                    "FAIL",
                    "security",
                    f"opencode.jsonc must guard external_directory with 'ask' or 'deny' (resolved to {ext_eff!r}).",
                )
            )

        for shell_cmd in ("rm -rf /", "git push origin main", "curl https://example.com"):
            sh_eff = resolve_permission(rules, "shell", shell_cmd)
            if sh_eff not in ("ask", "deny"):
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc must not pre-allow arbitrary shell command {shell_cmd!r} (resolved to {sh_eff!r}).",
                    )
                )

        for git_cmd in ("git status", "git status --short", "git diff", "git log -n 5", "git show HEAD"):
            git_eff = resolve_permission(rules, "shell", git_cmd)
            if git_eff != "allow":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "permissions",
                        f"opencode.jsonc should allow read-only Git command {git_cmd!r} (resolved to {git_eff!r}).",
                    )
                )

        if resolve_permission(rules, "grep", "DEFAULT_TIMEOUT") != "allow":
            findings.append(
                CheckFinding(
                    "FAIL",
                    "permissions",
                    "opencode.jsonc must allow normal code grep queries such as 'DEFAULT_TIMEOUT'.",
                )
            )
        for dump_pattern in (".*", ".+", "^.*", "^.+"):
            dump_eff = resolve_permission(rules, "grep", dump_pattern)
            if dump_eff not in ("ask", "deny"):
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc must guard catch-all grep dump pattern {dump_pattern!r} with 'ask' or 'deny' (resolved to {dump_eff!r}).",
                    )
                )
        for key_pattern in ("-----BEGIN RSA PRIVATE KEY-----", "PRIVATE KEY"):
            key_eff = resolve_permission(rules, "grep", key_pattern)
            if key_eff != "deny":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "security",
                        f"opencode.jsonc must deny grep private-key pattern {key_pattern!r} (resolved to {key_eff!r}).",
                    )
                )

    ignore_path = root / ".ignore"
    if not ignore_path.is_file():
        findings.append(
            CheckFinding(
                "FAIL",
                "security",
                "Missing root .ignore file to prevent ripgrep (rg --hidden) from indexing secret files during directory searches.",
            )
        )
    else:
        ignore_lines = {
            line.strip()
            for line in ignore_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
        missing_ignore = [pat for pat in REQUIRED_IGNORE_PATTERNS if pat not in ignore_lines]
        if missing_ignore:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "security",
                    f".ignore is missing required ripgrep secret-protection patterns: {missing_ignore}.",
                )
            )

    if not any(f.level == "FAIL" and f.category in ("config", "security", "permissions") for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "config",
                "opencode.jsonc syntax, V2 schema keys, common instructions, and secret/permission boundaries verified.",
            )
        )
    return config


def check_agents(root: pathlib.Path, findings: list[CheckFinding]) -> set[str]:
    agents_dir = root / ".opencode" / "agents"
    if not agents_dir.is_dir():
        findings.append(CheckFinding("FAIL", "agents", "Missing .opencode/agents directory."))
        return set()

    agent_files = sorted(agents_dir.glob("*.md"))
    if not agent_files:
        findings.append(CheckFinding("FAIL", "agents", "No agent Markdown files found in .opencode/agents/."))
        return set()

    agent_ids = {p.stem for p in agent_files}
    expected_subagents = {
        "explorer",
        "architecture-reviewer",
        "code-reviewer",
        "security-reviewer",
        "test-reviewer",
        "infra-reviewer",
    }
    missing_agents = sorted((expected_subagents | {"developer"}) - agent_ids)
    if missing_agents:
        findings.append(
            CheckFinding("FAIL", "agents", f"Missing required agent definitions: {missing_agents}.")
        )

    for agent_path in agent_files:
        agent_id = agent_path.stem
        rel_label = str(agent_path.relative_to(root))
        try:
            fm, body = parse_frontmatter(agent_path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(CheckFinding("FAIL", "agents", f"{rel_label} invalid frontmatter: {exc}"))
            continue

        legacy_keys = sorted(DEPRECATED_V1_AGENT_KEYS.intersection(fm.keys()))
        if legacy_keys:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "agents",
                    f"{rel_label} uses deprecated OpenCode V1 frontmatter keys: {legacy_keys}.",
                )
            )

        unknown_agent_keys = sorted(set(fm.keys()) - VALID_V2_AGENT_KEYS - DEPRECATED_V1_AGENT_KEYS)
        if unknown_agent_keys:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "agents",
                    f"{rel_label} uses unknown OpenCode V2 frontmatter keys: {unknown_agent_keys}.",
                )
            )

        description = fm.get("description")
        if not isinstance(description, str) or not description.strip():
            findings.append(CheckFinding("FAIL", "agents", f"{rel_label} is missing a non-empty description."))

        mode = fm.get("mode")
        if mode not in VALID_AGENT_MODES:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "agents",
                    f"{rel_label} has invalid mode {mode!r}; expected one of {sorted(VALID_AGENT_MODES)}.",
                )
            )

        if not body.strip():
            findings.append(CheckFinding("FAIL", "agents", f"{rel_label} has an empty prompt body."))

        rules = validate_permission_list(fm.get("permissions"), rel_label, findings)
        if not rules:
            continue

        if agent_id == "developer":
            if mode != "primary":
                findings.append(
                    CheckFinding("FAIL", "agents", f"{rel_label} must have mode 'primary', found {mode!r}.")
                )
            if resolve_permission(rules, "edit", "src/main.py") != "allow":
                findings.append(CheckFinding("FAIL", "agents", "developer.md must allow 'edit' on workspace files."))
            if resolve_permission(rules, "shell", "npm test") != "ask":
                findings.append(CheckFinding("FAIL", "agents", "developer.md must keep arbitrary 'shell' on 'ask'."))
            if resolve_permission(rules, "subagent", "unlisted-agent") != "deny":
                findings.append(
                    CheckFinding("FAIL", "agents", "developer.md must deny unlisted subagents by default.")
                )
            for rule in rules:
                if rule["action"] == "subagent" and rule["effect"] == "allow":
                    target_subagent = rule["resource"]
                    if target_subagent not in agent_ids:
                        findings.append(
                            CheckFinding(
                                "FAIL",
                                "agents",
                                f"developer.md allows non-existent subagent {target_subagent!r}.",
                            )
                        )
            for req_sub in sorted(expected_subagents):
                if resolve_permission(rules, "subagent", req_sub) != "allow":
                    findings.append(
                        CheckFinding(
                            "FAIL",
                            "agents",
                            f"developer.md must allow specialist subagent {req_sub!r}.",
                        )
                    )
        else:
            if mode != "subagent":
                findings.append(
                    CheckFinding("FAIL", "agents", f"{rel_label} must have mode 'subagent', found {mode!r}.")
                )
            eff = resolve_permission(rules, "edit", "src/app.py")
            if eff != "deny":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "agents",
                        f"Read-only subagent {rel_label} must deny 'edit' (which governs edit/write/patch in V2; resolved to {eff!r}).",
                    )
                )
            if resolve_permission(rules, "subagent", "explorer") != "deny":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "agents",
                        f"Read-only subagent {rel_label} must deny recursive subagent delegation.",
                    )
                )
            for forbidden_cmd in ("rm -rf /", "git commit -m x", "git push", "git status-malicious"):
                eff = resolve_permission(rules, "shell", forbidden_cmd)
                if eff != "deny":
                    findings.append(
                        CheckFinding(
                            "FAIL",
                            "agents",
                            f"Read-only subagent {rel_label} must deny shell command {forbidden_cmd!r} (resolved to {eff!r}).",
                        )
                    )
            for allowed_git_cmd in ("git status", "git status --short", "git diff", "git log -n 3", "git show HEAD"):
                eff = resolve_permission(rules, "shell", allowed_git_cmd)
                if eff != "allow":
                    findings.append(
                        CheckFinding(
                            "FAIL",
                            "agents",
                            f"Read-only subagent {rel_label} must allow read-only Git command {allowed_git_cmd!r} (resolved to {eff!r}).",
                        )
                    )

    if not any(f.level == "FAIL" and f.category == "agents" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "agents",
                f"All {len(agent_files)} agent definitions and single-writer/read-only permission contracts verified.",
            )
        )
    return agent_ids


def check_skills(root: pathlib.Path, findings: list[CheckFinding]) -> set[str]:
    skills_dir = root / ".opencode" / "skills"
    if not skills_dir.is_dir():
        findings.append(CheckFinding("FAIL", "skills", "Missing .opencode/skills directory."))
        return set()

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        findings.append(CheckFinding("FAIL", "skills", "No SKILL.md files found under .opencode/skills/*/."))
        return set()

    skill_ids: set[str] = set()
    for skill_path in skill_files:
        folder_name = skill_path.parent.name
        rel_label = str(skill_path.relative_to(root))
        skill_ids.add(folder_name)

        if not SKILL_ID_PATTERN.match(folder_name) or len(folder_name) > 64:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "skills",
                    f"{rel_label} directory name {folder_name!r} must be lowercase kebab-case (1-64 chars).",
                )
            )

        try:
            fm, body = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(CheckFinding("FAIL", "skills", f"{rel_label} invalid frontmatter: {exc}"))
            continue

        name = fm.get("name")
        if name != folder_name:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "skills",
                    f"{rel_label} frontmatter name {name!r} does not match directory name {folder_name!r}.",
                )
            )

        description = fm.get("description")
        if not isinstance(description, str) or len(description.strip()) < 15:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "skills",
                    f"{rel_label} must provide a specific non-empty frontmatter description.",
                )
            )

        if folder_name in STARTER_TECH_SKILLS:
            for heading in REQUIRED_TECH_SKILL_HEADINGS:
                if heading not in body:
                    findings.append(
                        CheckFinding(
                            "FAIL",
                            "skills",
                            f"Starter technology skill {rel_label} is missing template section {heading!r}.",
                        )
                    )
            if not re.search(r"^- Last reviewed:\s*\d{4}-\d{2}\b", body, re.MULTILINE):
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "skills",
                        f"Starter technology skill {rel_label} is missing '- Last reviewed: YYYY-MM' metadata in Supported scope.",
                    )
                )

    if not any(f.level == "FAIL" and f.category == "skills" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "skills",
                f"All {len(skill_files)} skills have valid frontmatter, matching IDs, and required template sections.",
            )
        )
    return skill_ids


def check_rule_catalog(root: pathlib.Path, findings: list[CheckFinding]) -> int:
    catalog_path = root / ".opencode" / "rules" / "RULE-CATALOG.md"
    if not catalog_path.is_file():
        findings.append(CheckFinding("FAIL", "rules", "Missing .opencode/rules/RULE-CATALOG.md."))
        return 0

    catalog_text = catalog_path.read_text(encoding="utf-8")
    row_pattern = re.compile(r"^\| ([^|]+?) \| ([^|]+?) \| `([^`]+)` \|$", re.MULTILINE)
    range_pattern = re.compile(r"^([A-Z]+)-(\d+)–\1-(\d+)$")

    rows = row_pattern.findall(catalog_text)
    if not rows:
        findings.append(CheckFinding("FAIL", "rules", "No catalogue rows found in RULE-CATALOG.md."))
        return 0

    all_rule_ids: list[str] = []
    catalog_files: set[pathlib.Path] = set()
    rules_root = root / ".opencode" / "rules"

    for id_col, _area, rel_file in rows:
        id_col = id_col.strip()
        target_path = (rules_root / rel_file).resolve()
        catalog_files.add(target_path)
        if not target_path.is_file():
            findings.append(
                CheckFinding(
                    "FAIL",
                    "rules",
                    f"RULE-CATALOG.md references missing file '.opencode/rules/{rel_file}'.",
                )
            )
            continue

        m = range_pattern.match(id_col)
        if not m:
            continue

        prefix, start_s, end_s = m.group(1), m.group(2), m.group(3)
        start_num, end_num = int(start_s), int(end_s)
        expected_ids = [f"{prefix}-{num:02d}" for num in range(start_num, end_num + 1)]
        file_text = target_path.read_text(encoding="utf-8")
        found_ids = re.findall(r"^\| (" + re.escape(prefix) + r"-\d+) \|", file_text, re.MULTILINE)
        if found_ids != expected_ids:
            missing = sorted(set(expected_ids) - set(found_ids))
            extra = sorted(set(found_ids) - set(expected_ids))
            findings.append(
                CheckFinding(
                    "FAIL",
                    "rules",
                    f".opencode/rules/{rel_file} rule IDs do not match catalogue range {id_col} (missing={missing}, extra={extra}, order_match={found_ids == expected_ids}).",
                )
            )
        all_rule_ids.extend(found_ids)

    duplicates = sorted(k for k, count in collections.Counter(all_rule_ids).items() if count > 1)
    if duplicates:
        findings.append(CheckFinding("FAIL", "rules", f"Duplicate rule IDs found: {duplicates}."))

    actual_rule_files = {
        p.resolve()
        for p in rules_root.rglob("*.md")
        if p.name != "RULE-CATALOG.md"
    }
    unindexed = sorted(str(p.relative_to(root)) for p in (actual_rule_files - catalog_files))
    if unindexed:
        findings.append(
            CheckFinding("FAIL", "rules", f"Rule files not indexed in RULE-CATALOG.md: {unindexed}.")
        )

    if not any(f.level == "FAIL" and f.category == "rules" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "rules",
                f"RULE-CATALOG.md verified across {len(actual_rule_files)} rule files and {len(all_rule_ids)} numbered rule IDs.",
            )
        )
    return len(all_rule_ids)


def check_references(
    root: pathlib.Path,
    skill_ids: set[str],
    agent_ids: set[str],
    findings: list[CheckFinding],
) -> None:
    md_files: list[pathlib.Path] = []
    for base in (root / "AGENTS.md", root / "README.md"):
        if base.is_file():
            md_files.append(base)
    for folder in (root / ".opencode", root / "docs"):
        if folder.is_dir():
            md_files.extend(sorted(folder.rglob("*.md")))

    path_token_re = re.compile(
        r"`((?:\.opencode|docs|scripts|tests|\.github|common|engineering|workflow)/[A-Za-z0-9_./-]+)`"
    )
    OptionalExternalOrGenerated = {
        ".opencode/commands/",
        ".opencode/plugin/",
        ".opencode/cache/",
        ".opencode/tmp/",
        ".opencode/agents/implementation-worker.md",
        ".opencode/agents/reviewer.md",
        ".opencode/agents/explainer.md",
        ".opencode/skills/git-release/SKILL.md",
    }

    for md_path in md_files:
        rel_md = str(md_path.relative_to(root))
        text = md_path.read_text(encoding="utf-8")
        for match in path_token_re.finditer(text):
            token = match.group(1)
            if token in OptionalExternalOrGenerated or "*" in token or "<" in token or ">" in token:
                continue
            if token.startswith(("common/", "engineering/", "workflow/")):
                candidate = root / ".opencode" / "rules" / token
            else:
                candidate = root / token

            if token.endswith("/"):
                exists = candidate.is_dir()
            else:
                exists = candidate.exists()

            if not exists:
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "references",
                        f"{rel_md} references non-existent path {token!r}.",
                    )
                )

    skill_sel_path = root / ".opencode" / "rules" / "workflow" / "skill-selection.md"
    if skill_sel_path.is_file():
        sel_text = skill_sel_path.read_text(encoding="utf-8")
        if re.search(r"\bdatabase skill\b", sel_text):
            findings.append(
                CheckFinding(
                    "FAIL",
                    "references",
                    ".opencode/rules/workflow/skill-selection.md still contains ambiguous 'database skill' prose instead of backticked 'database-engineering'.",
                )
            )
        examples_section = sel_text.split("## Loading", 1)[0].split("Examples:", 1)[-1]
        for token in re.findall(r"`([a-z0-9-]+)`", examples_section):
            if token not in skill_ids:
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "references",
                        f".opencode/rules/workflow/skill-selection.md example references unknown skill {token!r}.",
                    )
                )

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme_text = readme_path.read_text(encoding="utf-8")
        v1_doc_links = re.findall(r"https://opencode\.ai/docs/[A-Za-z0-9_/-]*", readme_text)
        if v1_doc_links:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "references",
                    f"README.md links to OpenCode V1 docs instead of V2 docs (/v2/docs/...): {v1_doc_links}.",
                )
            )

    agents_md_path = root / "AGENTS.md"
    if agents_md_path.is_file():
        agents_md_text = agents_md_path.read_text(encoding="utf-8")
        if "Grant write access only through a separate, explicit, bounded remediation assignment" in agents_md_text:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "references",
                    "AGENTS.md contains contradictory guidance claiming review/explorer agents can be granted write access via prompt assignment.",
                )
            )
        for cited_agent in (
            "developer",
            "explorer",
            "architecture-reviewer",
            "security-reviewer",
            "test-reviewer",
            "infra-reviewer",
            "code-reviewer",
        ):
            if cited_agent not in agent_ids:
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "references",
                        f"AGENTS.md references agent {cited_agent!r} that is missing from .opencode/agents/.",
                    )
                )

    if not any(f.level == "FAIL" and f.category == "references" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "references",
                "All internal file paths, skill IDs, agent IDs, and OpenCode V2 documentation links verified.",
            )
        )


def check_templates(root: pathlib.Path, findings: list[CheckFinding]) -> None:
    worker_template = root / "docs" / "templates" / "implementation-worker-agent.md"
    if not worker_template.is_file():
        findings.append(
            CheckFinding("FAIL", "templates", "Missing docs/templates/implementation-worker-agent.md.")
        )
        return

    text = worker_template.read_text(encoding="utf-8")
    fenced_match = re.search(r"```markdown\n(---\n.*?)\n```", text, re.DOTALL)
    if not fenced_match:
        findings.append(
            CheckFinding(
                "FAIL",
                "templates",
                "docs/templates/implementation-worker-agent.md is missing a fenced ```markdown agent profile.",
            )
        )
        return

    rel_label = "docs/templates/implementation-worker-agent.md"
    try:
        fm, body = parse_frontmatter(fenced_match.group(1))
    except Exception as exc:
        findings.append(CheckFinding("FAIL", "templates", f"{rel_label} invalid frontmatter: {exc}"))
        return

    legacy_keys = sorted(DEPRECATED_V1_AGENT_KEYS.intersection(fm.keys()))
    if legacy_keys:
        findings.append(
            CheckFinding("FAIL", "templates", f"{rel_label} uses deprecated V1 frontmatter keys: {legacy_keys}.")
        )
    if fm.get("mode") != "subagent":
        findings.append(
            CheckFinding(
                "FAIL",
                "templates",
                f"{rel_label} must declare mode 'subagent', found {fm.get('mode')!r}.",
            )
        )
    if not body.strip():
        findings.append(CheckFinding("FAIL", "templates", f"{rel_label} has an empty prompt body."))

    rules = validate_permission_list(fm.get("permissions"), rel_label, findings)
    if rules:
        for allowed_path in ("src/module-a/index.ts", "tests/module-a/index.test.ts"):
            eff = resolve_permission(rules, "edit", allowed_path)
            if eff != "allow":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "templates",
                        f"{rel_label} must allow 'edit' on owned path {allowed_path!r} (resolved to {eff!r}).",
                    )
                )
        for denied_path in (
            "src/module-b/index.ts",
            "package-lock.json",
            "AGENTS.md",
            "opencode.jsonc",
            "specs/001-feature/spec.md",
            "db/migrations/001_init.sql",
        ):
            eff = resolve_permission(rules, "edit", denied_path)
            if eff != "deny":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "templates",
                        f"{rel_label} must deny 'edit' on out-of-scope/shared path {denied_path!r} (resolved to {eff!r}).",
                    )
                )
        if resolve_permission(rules, "subagent", "explorer") != "deny":
            findings.append(
                CheckFinding("FAIL", "templates", f"{rel_label} must deny recursive subagent launches.")
            )
        if resolve_permission(rules, "shell", "rm -rf /") != "deny":
            findings.append(
                CheckFinding("FAIL", "templates", f"{rel_label} must deny arbitrary shell commands.")
            )
        if resolve_permission(rules, "shell", "git status --short") != "allow":
            findings.append(
                CheckFinding("FAIL", "templates", f"{rel_label} must allow read-only 'git status *'.")
            )

    if not any(f.level == "FAIL" and f.category == "templates" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "templates",
                "docs/templates/implementation-worker-agent.md V2 frontmatter and path-scoped write boundaries verified.",
            )
        )


def check_rule_routing(
    root: pathlib.Path,
    skill_ids: set[str],
    agent_ids: set[str],
    findings: list[CheckFinding],
) -> dict[str, Any] | None:
    routing_path = root / ".opencode" / "rules" / "rule-routing.json"
    if not routing_path.is_file():
        findings.append(
            CheckFinding("FAIL", "routing", "Missing .opencode/rules/rule-routing.json manifest.")
        )
        return None

    try:
        manifest = json.loads(routing_path.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(CheckFinding("FAIL", "routing", f"Invalid JSON in rule-routing.json: {exc}"))
        return None

    if not isinstance(manifest, dict):
        findings.append(CheckFinding("FAIL", "routing", "rule-routing.json root must be an object."))
        return None

    workflow_rules = manifest.get("always_on_workflow_rules")
    if not isinstance(workflow_rules, list) or not workflow_rules:
        findings.append(
            CheckFinding("FAIL", "routing", "rule-routing.json must define 'always_on_workflow_rules'.")
        )
    else:
        for wf_path in workflow_rules:
            if not isinstance(wf_path, str) or not (root / wf_path).is_file():
                findings.append(
                    CheckFinding("FAIL", "routing", f"rule-routing.json workflow rule missing: {wf_path!r}.")
                )

    domains = manifest.get("domains")
    if not isinstance(domains, dict) or not domains:
        findings.append(CheckFinding("FAIL", "routing", "rule-routing.json must define non-empty 'domains'."))
        return None

    valid_qg_ids = {f"QG-{i:02d}" for i in range(1, 18)}
    referenced_eng_rules: set[str] = set()

    for domain_name, spec in domains.items():
        if not isinstance(spec, dict):
            findings.append(CheckFinding("FAIL", "routing", f"Domain {domain_name!r} entry must be an object."))
            continue
        rules = spec.get("rules", [])
        if not isinstance(rules, list) or not rules:
            findings.append(CheckFinding("FAIL", "routing", f"Domain {domain_name!r} must list at least one rule."))
        else:
            for r_rel in rules:
                referenced_eng_rules.add(r_rel)
                if not (root / ".opencode" / "rules" / r_rel).is_file():
                    findings.append(
                        CheckFinding(
                            "FAIL",
                            "routing",
                            f"Domain {domain_name!r} references missing rule '.opencode/rules/{r_rel}'.",
                        )
                    )
        for sk in spec.get("skills", []):
            if sk not in skill_ids:
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "routing",
                        f"Domain {domain_name!r} references unknown skill {sk!r}.",
                    )
                )
        for qg in spec.get("quality_gates", []):
            if qg not in valid_qg_ids:
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "routing",
                        f"Domain {domain_name!r} references invalid quality gate ID {qg!r}.",
                    )
                )
        for rev in spec.get("reviewers", []):
            if rev not in agent_ids or rev == "developer":
                findings.append(
                    CheckFinding(
                        "FAIL",
                        "routing",
                        f"Domain {domain_name!r} references invalid specialist reviewer {rev!r}.",
                    )
                )

    eng_dir = root / ".opencode" / "rules" / "engineering"
    if eng_dir.is_dir():
        actual_eng_rules = {f"engineering/{p.name}" for p in eng_dir.glob("*.md")}
        unrouted = sorted(actual_eng_rules - referenced_eng_rules)
        if unrouted:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "routing",
                    f"Engineering rule files not reachable from any domain in rule-routing.json: {unrouted}.",
                )
            )

    if not any(f.level == "FAIL" and f.category == "routing" for f in findings):
        findings.append(
            CheckFinding(
                "PASS",
                "routing",
                f"rule-routing.json verified across {len(domains)} domains and all 16 engineering rule files.",
            )
        )
    return manifest


def check_context_budget(root: pathlib.Path, findings: list[CheckFinding]) -> None:
    always_on_paths = [root / "AGENTS.md"] + [root / p for p in EXPECTED_COMMON_RULES]
    total_chars = 0
    total_lines = 0
    for p in always_on_paths:
        if p.is_file():
            content = p.read_text(encoding="utf-8")
            total_chars += len(content)
            total_lines += len(content.splitlines())

    estimated_tokens = (total_chars + 3) // 4
    if estimated_tokens > MAX_ALWAYS_ON_ESTIMATED_TOKENS:
        findings.append(
            CheckFinding(
                "FAIL",
                "context-budget",
                f"Always-on context (AGENTS.md + 7 common rules) is ~{estimated_tokens} tokens, exceeding budget of {MAX_ALWAYS_ON_ESTIMATED_TOKENS}.",
            )
        )
    else:
        findings.append(
            CheckFinding(
                "PASS",
                "context-budget",
                f"Always-on context footprint is {total_lines} lines / ~{estimated_tokens} tokens (within {MAX_ALWAYS_ON_ESTIMATED_TOKENS}-token budget).",
            )
        )


def _match_path_glob(file_path: str, pattern: str) -> bool:
    norm_path = file_path.strip("/").replace("\\", "/")
    norm_pat = pattern.strip("/").replace("\\", "/")
    if fnmatch.fnmatch(norm_path, norm_pat):
        return True
    if norm_pat.startswith("**/") and fnmatch.fnmatch(norm_path, norm_pat[3:]):
        return True
    if "/**/" in norm_pat:
        collapsed = norm_pat.replace("/**/", "/")
        if fnmatch.fnmatch(norm_path, collapsed):
            return True
    return False


def compute_preflight(
    root: pathlib.Path,
    *,
    domains: list[str] | None = None,
    files: list[str] | None = None,
    stack: str = "<detect from manifests>",
) -> dict[str, Any]:
    routing_path = root / ".opencode" / "rules" / "rule-routing.json"
    manifest = json.loads(routing_path.read_text(encoding="utf-8"))
    domain_map: dict[str, Any] = manifest["domains"]

    matched_domains: list[str] = []
    for d in domains or []:
        d_clean = d.strip().lower()
        if not d_clean:
            continue
        if d_clean not in domain_map:
            raise ValueError(
                f"Unknown domain {d_clean!r}. Valid domains: {', '.join(sorted(domain_map.keys()))}"
            )
        if d_clean not in matched_domains:
            matched_domains.append(d_clean)

    for fpath in files or []:
        for d_name, spec in domain_map.items():
            for pat in spec.get("path_globs", []):
                if _match_path_glob(fpath, pat) and d_name not in matched_domains:
                    matched_domains.append(d_name)

    if not matched_domains:
        matched_domains.append("application-code")

    rules: list[str] = []
    skills: list[str] = []
    quality_gates: list[str] = []
    reviewers: list[str] = []

    for d_name in matched_domains:
        spec = domain_map[d_name]
        for r in spec.get("rules", []):
            full_r = f".opencode/rules/{r}"
            if full_r not in rules:
                rules.append(full_r)
        for s in spec.get("skills", []):
            if s not in skills:
                skills.append(s)
        for qg in spec.get("quality_gates", []):
            if qg not in quality_gates:
                quality_gates.append(qg)
        for rev in spec.get("reviewers", []):
            if rev not in reviewers:
                reviewers.append(rev)

    quality_gates.sort(key=lambda x: int(x.split("-")[1]))

    block_lines = [
        "RULE & SKILL PREFLIGHT",
        f"Detected stack & versions: {stack}",
        f"Task domains: {', '.join(matched_domains)}",
        f"Required engineering rules loaded: {', '.join(rules) if rules else 'none'}",
        f"Skills loaded: {', '.join(skills) if skills else 'none'}",
        f"Applicable quality gates: {', '.join(quality_gates) if quality_gates else 'none'}",
        f"Recommended specialist reviewers: {', '.join(reviewers) if reviewers else 'none'}",
    ]
    return {
        "stack": stack,
        "domains": matched_domains,
        "files": files or [],
        "always_on_workflow_rules": manifest.get("always_on_workflow_rules", []),
        "engineering_rules": rules,
        "skills": skills,
        "quality_gates": quality_gates,
        "reviewers": reviewers,
        "formatted": "\n".join(block_lines),
    }
    agents_md = root / "AGENTS.md"
    if agents_md.is_file():
        lines = agents_md.read_text(encoding="utf-8").splitlines()
        todo_lines = [line.strip() for line in lines if re.search(r":\s*TODO\b", line)]
        if todo_lines:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "readiness",
                    f"AGENTS.md still has {len(todo_lines)} unresolved project-specific TODO placeholder(s): {todo_lines}",
                )
            )
        else:
            findings.append(
                CheckFinding("PASS", "readiness", "AGENTS.md project-specific facts are populated (no TODOs).")
            )

    constitution = root / ".specify" / "memory" / "constitution.md"
    if constitution.is_file():
        findings.append(CheckFinding("PASS", "readiness", "Found .specify/memory/constitution.md."))
    else:
        findings.append(
            CheckFinding(
                "WARN",
                "readiness",
                "Missing .specify/memory/constitution.md (run '/speckit.constitution' after initializing Spec Kit).",
            )
        )

    commands_dir = root / ".opencode" / "commands"
    if commands_dir.is_dir() and any(commands_dir.iterdir()):
        findings.append(CheckFinding("PASS", "readiness", "Found Spec Kit commands in .opencode/commands/."))
    else:
        findings.append(
            CheckFinding(
                "WARN",
                "readiness",
                "No Spec Kit command files found in .opencode/commands/ (run 'specify init . --integration opencode' or 'specify integration install opencode').",
            )
        )

def _parse_semver(text: str) -> tuple[int, int, int] | None:
    m = re.search(r"\b(\d+)\.(\d+)\.(\d+)\b", text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def check_project_readiness(root: pathlib.Path, findings: list[CheckFinding]) -> None:
    agents_md = root / "AGENTS.md"
    if agents_md.is_file():
        lines = agents_md.read_text(encoding="utf-8").splitlines()
        todo_lines = [line.strip() for line in lines if re.search(r":\s*TODO\b", line)]
        if todo_lines:
            findings.append(
                CheckFinding(
                    "FAIL",
                    "readiness",
                    f"AGENTS.md still has {len(todo_lines)} unresolved project-specific TODO placeholder(s): {todo_lines}",
                )
            )
        else:
            findings.append(
                CheckFinding("PASS", "readiness", "AGENTS.md project-specific facts are populated (no TODOs).")
            )

    constitution = root / ".specify" / "memory" / "constitution.md"
    if constitution.is_file():
        findings.append(CheckFinding("PASS", "readiness", "Found .specify/memory/constitution.md."))
    else:
        findings.append(
            CheckFinding(
                "WARN",
                "readiness",
                "Missing .specify/memory/constitution.md (run '/speckit.constitution' after initializing Spec Kit).",
            )
        )

    commands_dir = root / ".opencode" / "commands"
    if commands_dir.is_dir() and any(commands_dir.iterdir()):
        findings.append(CheckFinding("PASS", "readiness", "Found Spec Kit commands in .opencode/commands/."))
    else:
        findings.append(
            CheckFinding(
                "WARN",
                "readiness",
                "No Spec Kit command files found in .opencode/commands/ (run 'specify init . --integration opencode' or 'specify integration install opencode').",
            )
        )

    opencode_bin = shutil.which("opencode")
    if not opencode_bin:
        findings.append(
            CheckFinding("WARN", "readiness", "CLI tool 'opencode' is not installed or not on PATH.")
        )
    else:
        try:
            proc = subprocess.run(
                [opencode_bin, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            out = (proc.stdout or proc.stderr or "").strip()
            ver = _parse_semver(out)
            if ver is not None and ver[0] < 2:
                findings.append(
                    CheckFinding(
                        "WARN",
                        "readiness",
                        f"CLI tool 'opencode' at {opencode_bin} reported V1 version {ver[0]}.{ver[1]}.{ver[2]}; this harness targets OpenCode V2.",
                    )
                )
            else:
                ver_label = f"{ver[0]}.{ver[1]}.{ver[2]}" if ver else (out.splitlines()[0] if out else "unknown")
                findings.append(
                    CheckFinding("PASS", "readiness", f"CLI tool 'opencode' found at {opencode_bin} (version: {ver_label}).")
                )
        except Exception as exc:
            findings.append(
                CheckFinding("WARN", "readiness", f"CLI tool 'opencode' at {opencode_bin} failed version check: {exc}")
            )

    specify_bin = shutil.which("specify")
    if not specify_bin:
        findings.append(
            CheckFinding("WARN", "readiness", "CLI tool 'specify' is not installed or not on PATH.")
        )
    else:
        try:
            proc = subprocess.run(
                [specify_bin, "version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            out = (proc.stdout or proc.stderr or "").strip()
            ver = _parse_semver(out)
            if ver is not None and (ver[0], ver[1]) < (1, 2):
                findings.append(
                    CheckFinding(
                        "WARN",
                        "readiness",
                        f"CLI tool 'specify' at {specify_bin} reported version {ver[0]}.{ver[1]}.{ver[2]}; Spec Kit >= 1.2.0 is recommended for '/speckit.converge'.",
                    )
                )
            else:
                ver_label = f"{ver[0]}.{ver[1]}.{ver[2]}" if ver else "detected"
                findings.append(
                    CheckFinding("PASS", "readiness", f"CLI tool 'specify' found at {specify_bin} (version: {ver_label}).")
                )
        except Exception as exc:
            findings.append(
                CheckFinding("WARN", "readiness", f"CLI tool 'specify' at {specify_bin} failed version check: {exc}")
            )


def validate_repository(root: pathlib.Path, *, mode: str = "template") -> list[CheckFinding]:
    if mode not in ("template", "project"):
        raise ValueError(f"Unsupported validation mode: {mode!r}")

    findings: list[CheckFinding] = []
    check_opencode_config(root, findings)
    agent_ids = check_agents(root, findings)
    skill_ids = check_skills(root, findings)
    check_templates(root, findings)
    check_rule_catalog(root, findings)
    check_rule_routing(root, skill_ids, agent_ids, findings)
    check_context_budget(root, findings)
    check_references(root, skill_ids, agent_ids, findings)
    if mode == "project":
        check_project_readiness(root, findings)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the OpenCode Engineering Harness (--mode template or --mode project)."
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parent.parent,
        help="Repository root directory to validate.",
    )
    parser.add_argument(
        "--mode",
        choices=("template", "project"),
        default="template",
        help="Validation mode: 'template' for the blueprint repo CI; 'project' for adopted project readiness.",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Compute a deterministic Rule & Skill Preflight manifest from .opencode/rules/rule-routing.json.",
    )
    parser.add_argument(
        "--domains",
        type=str,
        default="",
        help="Comma-separated domain names for --preflight (for example: api,database,security).",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="Changed or affected file paths for --preflight domain inference.",
    )
    parser.add_argument(
        "--stack",
        type=str,
        default="<detect from manifests>",
        help="Detected stack summary to include in --preflight output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON output.",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.preflight:
        domain_list = [d.strip() for d in args.domains.split(",") if d.strip()]
        try:
            preflight = compute_preflight(
                root,
                domains=domain_list,
                files=args.files,
                stack=args.stack,
            )
        except Exception as exc:
            print(f"Preflight error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(preflight, indent=2))
        else:
            print(preflight["formatted"])
        return 0

    findings = validate_repository(root, mode=args.mode)
    failures = [f for f in findings if f.level == "FAIL"]
    warnings = [f for f in findings if f.level == "WARN"]

    if args.json:
        payload = {
            "mode": args.mode,
            "root": str(root),
            "status": "FAIL" if failures else "PASS",
            "counts": {
                "pass": sum(1 for f in findings if f.level == "PASS"),
                "warn": len(warnings),
                "fail": len(failures),
            },
            "findings": [dataclasses.asdict(f) for f in findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"OpenCode Engineering Harness — Validation ({args.mode} mode)")
        print("=" * 60)
        for item in findings:
            print(f"[{item.level}] ({item.category}) {item.message}")
        print("-" * 60)
        overall = "READY / PASSED" if not failures else "NOT READY / FAILED"
        print(
            f"Overall: {overall} "
            f"({sum(1 for f in findings if f.level == 'PASS')} pass, {len(warnings)} warn, {len(failures)} fail)"
        )

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
