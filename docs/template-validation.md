# Template Validation and Project Readiness

## Automated validation (`scripts/validate_harness.py`)

Run the zero-dependency validator to check configuration syntax, OpenCode V2 permission ordering, read-only reviewer contracts, skill frontmatter and template sections, all 323 rule IDs in `.opencode/rules/RULE-CATALOG.md`, and cross-file references:

```sh
# Validate the blueprint template itself (used in CI)
python3 scripts/validate_harness.py --mode template

# Run the automated unit test suite
python3 -m unittest discover -s tests -v

# Check project readiness after adopting the harness into a target repository
python3 scripts/validate_harness.py --mode project
```

`--mode project` runs every template integrity check and additionally verifies that `AGENTS.md` `TODO` placeholders have been populated, checks for conflicting duplicate OpenCode config files, and checks whether the `opencode` CLI is installed.

## Structure and traceability checklist

- [ ] Every path referenced from `AGENTS.md` exists.
- [ ] `opencode.jsonc` references all seven always-on common rule files.
- [ ] Every ID range in `.opencode/rules/RULE-CATALOG.md` appears in its authoritative detailed rule file.
- [ ] Rule IDs are unique within their prefix and are not reused for a different standard.
- [ ] Conditional rules are not injected into every agent by default; the routing map explains when to read them.
- [ ] Technology skills have valid `name` / folder-name matches and useful trigger descriptions.

## OpenCode configuration and permissions

- [ ] `opencode.jsonc` parses under the installed OpenCode version and schema.
- [ ] Agent IDs match filenames and referenced subagent permission resources.
- [ ] `developer` is the intended default primary agent.
- [ ] Read-only agents deny `edit` (which covers `edit`, `write`, and `patch` in OpenCode V2), arbitrary `shell` (allowing only read-only `git status *`/`git diff *`/`git log *`/`git show *`), and recursive `subagent` actions using the syntax supported by OpenCode V2.
- [ ] Shell approvals and web/external access match the team's risk tolerance.
- [ ] Permission syntax has been checked against the installed OpenCode release; do not mix V1 and V2 configuration formats.

## Repository readiness

- [ ] Root `AGENTS.md` project facts and exact commands are populated.
- [ ] Existing `.opencode/commands/`, plugin configuration, and user instructions are preserved.
- [ ] Feature-specific requirements remain in feature or task artifacts.

## Runtime pilot

- [ ] Start a fresh OpenCode session so changed instructions are loaded.
- [ ] Confirm the default `developer` agent is selectable.
- [ ] Confirm specialist agents can be invoked by their configured names.
- [ ] Verify reviewer agents cannot edit/write files or execute non-read-only shell commands.
- [ ] Verify the developer selects only relevant detailed rules and technology skills.
- [ ] Run one low-risk feature or bug fix through implementation, review, and verification.
- [ ] Confirm final reports distinguish executed checks from passed checks and skipped checks.
- [ ] Add executable CI enforcement for repeatable quality gates; prompt rules alone are not enforcement.
