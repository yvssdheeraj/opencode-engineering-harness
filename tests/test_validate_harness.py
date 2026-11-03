import json
import pathlib
import shutil
import tempfile
import unittest

from scripts import validate_harness


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


class ValidateHarnessTests(unittest.TestCase):
    def _copy_repo_to_temp(self) -> pathlib.Path:
        tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="harness-test-"))
        self.addCleanup(lambda: shutil.rmtree(tmp_dir, ignore_errors=True))
        for item in ("opencode.jsonc", "AGENTS.md", "README.md", ".opencode", "docs", "scripts"):
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


if __name__ == "__main__":
    unittest.main()
