import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from scripts import validate_harness


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


class ValidateHarnessTests(unittest.TestCase):
    def _copy_repo_to_temp(self) -> pathlib.Path:
        tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="harness-test-"))
        self.addCleanup(lambda: shutil.rmtree(tmp_dir, ignore_errors=True))
        for item in ("opencode.jsonc", ".ignore", "AGENTS.md", "README.md", ".opencode", "docs", "scripts"):
            src = REPO_ROOT / item
            dst = tmp_dir / item
            if src.is_dir():
                shutil.copytree(src, dst)
            elif src.is_file():
                shutil.copy2(src, dst)
        return tmp_dir

    def test_template_mode_passes_on_repository(self) -> None:
        findings = validate_harness.validate_repository(REPO_ROOT, mode="template")
        failures = [f for f in findings if f.level == "FAIL"]
        self.assertEqual(failures, [], f"Expected zero failures in template mode, got: {failures}")

    def test_jsonc_parser_handles_comments_and_trailing_commas(self) -> None:
        sample = """
        {
          // Line comment with https://opencode.ai/config.json inside
          "$schema": "https://opencode.ai/config.json",
          /* Block comment */
          "list": [
            "a",
            "b",
          ],
        }
        """
        parsed = validate_harness.parse_jsonc(sample)
        self.assertEqual(parsed["$schema"], "https://opencode.ai/config.json")
        self.assertEqual(parsed["list"], ["a", "b"])

    def test_detects_clobbered_env_and_secret_read_permissions(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        cfg_path = tmp_root / "opencode.jsonc"
        cfg = validate_harness.parse_jsonc(cfg_path.read_text(encoding="utf-8"))
        # Append a broad allow at the end so last-match-wins clobbers .env and key protections
        cfg["permissions"].append({"action": "read", "resource": "*", "effect": "allow"})
        cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        failures = [f for f in findings if f.level == "FAIL" and f.category == "security"]
        self.assertTrue(
            any(".env" in f.message for f in failures),
            f"Expected .env security failure when read:* allow is last, got: {failures}",
        )
        self.assertTrue(
            any("private.key" in f.message or "id_rsa" in f.message for f in failures),
            f"Expected key/secret security failure when read:* allow is last, got: {failures}",
        )

    def test_detects_reviewer_granted_write_or_shell_access(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        reviewer_path = tmp_root / ".opencode" / "agents" / "code-reviewer.md"
        text = reviewer_path.read_text(encoding="utf-8")
        mutated = text.replace("  - action: edit\n    resource: \"*\"\n    effect: deny", "  - action: edit\n    resource: \"*\"\n    effect: allow")
        reviewer_path.write_text(mutated, encoding="utf-8")

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        failures = [f for f in findings if f.level == "FAIL" and f.category == "agents"]
        self.assertTrue(
            any("code-reviewer.md" in f.message and "edit" in f.message for f in failures),
            f"Expected failure when code-reviewer allows edit, got: {failures}",
        )

    def test_detects_rule_catalog_id_mismatch(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        sec_rule_path = tmp_root / ".opencode" / "rules" / "engineering" / "security.md"
        text = sec_rule_path.read_text(encoding="utf-8")
        sec_rule_path.write_text(text.replace("| SEC-17 |", "| SEC-99 |"), encoding="utf-8")

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        failures = [f for f in findings if f.level == "FAIL" and f.category == "rules"]
        self.assertTrue(
            any("security.md" in f.message for f in failures),
            f"Expected rule catalogue mismatch failure, got: {failures}",
        )

    def test_detects_skill_name_mismatch_and_broken_reference(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        skill_path = tmp_root / ".opencode" / "skills" / "tdd" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace("name: tdd", "name: wrong-name"),
            encoding="utf-8",
        )
        agents_md = tmp_root / "AGENTS.md"
        agents_md.write_text(
            agents_md.read_text(encoding="utf-8") + "\nSee `.opencode/rules/engineering/non-existent.md`.\n",
            encoding="utf-8",
        )

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        skill_failures = [f for f in findings if f.level == "FAIL" and f.category == "skills"]
        ref_failures = [f for f in findings if f.level == "FAIL" and f.category == "references"]
        self.assertTrue(any("wrong-name" in f.message for f in skill_failures))
        self.assertTrue(any("non-existent.md" in f.message for f in ref_failures))

    def test_project_mode_flags_unresolved_agents_md_todos(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        findings = validate_harness.validate_repository(tmp_root, mode="project")
        readiness_failures = [f for f in findings if f.level == "FAIL" and f.category == "readiness"]
        self.assertTrue(
            any("TODO" in f.message for f in readiness_failures),
            f"Expected project mode to fail on unresolved AGENTS.md TODOs, got: {readiness_failures}",
        )

        # Resolve TODOs and verify readiness failure disappears
        agents_md = tmp_root / "AGENTS.md"
        agents_md.write_text(
            agents_md.read_text(encoding="utf-8").replace(": TODO", ": Configured"),
            encoding="utf-8",
        )
        findings_after = validate_harness.validate_repository(tmp_root, mode="project")
        readiness_failures_after = [
            f for f in findings_after if f.level == "FAIL" and f.category == "readiness"
        ]
        self.assertEqual(readiness_failures_after, [])

    def test_detects_legacy_v1_permission_actions_and_missing_ignore(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        # Inject legacy V1 'write' action into explorer.md and delete .ignore
        explorer_path = tmp_root / ".opencode" / "agents" / "explorer.md"
        explorer_path.write_text(
            explorer_path.read_text(encoding="utf-8").replace(
                "  - action: edit\n    resource: \"*\"\n    effect: deny",
                "  - action: edit\n    resource: \"*\"\n    effect: deny\n  - action: write\n    resource: \"*\"\n    effect: deny",
            ),
            encoding="utf-8",
        )
        (tmp_root / ".ignore").unlink()

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        perm_failures = [f for f in findings if f.level == "FAIL" and f.category == "permissions"]
        sec_failures = [f for f in findings if f.level == "FAIL" and f.category == "security"]
        self.assertTrue(
            any("write" in f.message for f in perm_failures),
            f"Expected V1 action 'write' to be rejected, got: {perm_failures}",
        )
        self.assertTrue(
            any(".ignore" in f.message for f in sec_failures),
            f"Expected missing .ignore to fail security validation, got: {sec_failures}",
        )

    def test_validates_implementation_worker_template_scope_boundaries(self) -> None:
        tmp_root = self._copy_repo_to_temp()
        worker_tpl = tmp_root / "docs" / "templates" / "implementation-worker-agent.md"
        # Break the worker boundary by appending edit: * -> allow at the end
        worker_tpl.write_text(
            worker_tpl.read_text(encoding="utf-8").replace(
                "  - action: edit\n    resource: \"tests/module-a/**\"\n    effect: allow",
                "  - action: edit\n    resource: \"tests/module-a/**\"\n    effect: allow\n  - action: edit\n    resource: \"*\"\n    effect: allow",
            ),
            encoding="utf-8",
        )

        findings = validate_harness.validate_repository(tmp_root, mode="template")
        tpl_failures = [f for f in findings if f.level == "FAIL" and f.category == "templates"]
        self.assertTrue(
            any("package-lock.json" in f.message or "module-b" in f.message for f in tpl_failures),
            f"Expected worker template scope escape to fail, got: {tpl_failures}",
        )

    def test_deterministic_preflight_resolves_domains_and_file_globs(self) -> None:
        result = validate_harness.compute_preflight(
            REPO_ROOT,
            domains=["api"],
            files=["db/migrations/V1__users.sql", "src/auth/jwt.ts"],
            stack="Spring Boot 3.3, PostgreSQL 16",
        )
        self.assertEqual(result["domains"], ["api", "database", "application-code", "security"])
        self.assertIn(".opencode/rules/engineering/security.md", result["engineering_rules"])
        self.assertIn(".opencode/rules/engineering/data-management.md", result["engineering_rules"])
        self.assertIn(".opencode/rules/engineering/api-and-integration.md", result["engineering_rules"])
        self.assertIn("database-engineering", result["skills"])
        self.assertIn("security-review", result["skills"])
        self.assertIn("security-reviewer", result["reviewers"])
        self.assertIn("QG-07", result["quality_gates"])
        self.assertIn("QG-08", result["quality_gates"])

    def test_ripgrep_ignore_blocks_secret_files_under_opencode_v2_flags(self) -> None:
        rg_bin = shutil.which("rg")
        if not rg_bin:
            self.skipTest("ripgrep (rg) binary not installed")

        tmp_root = self._copy_repo_to_temp()
        marker = "SUPER_SECRET_CANARY_TOKEN_98765"
        (tmp_root / ".env").write_text(f"API_KEY={marker}\n", encoding="utf-8")
        (tmp_root / ".env.production").write_text(f"PROD_KEY={marker}\n", encoding="utf-8")
        (tmp_root / ".env.example").write_text(f"EXAMPLE_KEY={marker}\n", encoding="utf-8")
        (tmp_root / "server.pem").write_text(f"-----BEGIN PRIVATE KEY-----\n{marker}\n", encoding="utf-8")
        (tmp_root / "private.key").write_text(f"{marker}\n", encoding="utf-8")
        (tmp_root / "service-credentials.json").write_text(f'{{"secret": "{marker}"}}\n', encoding="utf-8")
        secrets_dir = tmp_root / "secrets"
        secrets_dir.mkdir(exist_ok=True)
        (secrets_dir / "db.txt").write_text(f"{marker}\n", encoding="utf-8")
        aws_dir = tmp_root / ".aws"
        aws_dir.mkdir(exist_ok=True)
        (aws_dir / "credentials").write_text(f"aws_secret_access_key = {marker}\n", encoding="utf-8")

        # Execute ripgrep with the exact flags used by OpenCode V2 packages/core/src/ripgrep.ts
        proc = subprocess.run(
            [
                rg_bin,
                "--no-config",
                "--files-with-matches",
                "--hidden",
                "--no-messages",
                "--glob=!**/.git/**",
                "--",
                marker,
                ".",
            ],
            cwd=tmp_root,
            capture_output=True,
            text=True,
            check=False,
        )
        matched_files = {
            line.strip().removeprefix("./")
            for line in proc.stdout.splitlines()
            if line.strip()
        }
        self.assertEqual(
            matched_files,
            {".env.example"},
            f"Expected .ignore to block all secret files except .env.example under rg --no-config --hidden; got: {matched_files}",
        )


if __name__ == "__main__":
    unittest.main()
