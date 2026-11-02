# Template Validation Notes

## Structure and traceability

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
- [ ] Read-only agents deny `edit`/`write`, arbitrary `shell` (allowing only read-only `git status`/`git diff`/`git log`/`git show`), and recursive `subagent` actions using the syntax supported by the installed OpenCode version.
- [ ] Shell approvals and web/external access match the team's risk tolerance.
- [ ] Permission syntax has been checked against the installed OpenCode release; do not mix V1 and V2 configuration formats.

## Repository and Spec Kit integration

- [ ] Root `AGENTS.md` project facts and exact commands are populated.
- [ ] Spec Kit `/speckit.*` commands are installed and remain intact.
- [ ] Existing `.opencode/commands/`, event/plugin configuration, and user instructions are preserved.
- [ ] The project constitution is concise and does not duplicate the full detailed rule catalogue.
- [ ] Feature-specific requirements remain in feature artifacts.

## Runtime pilot

- [ ] Start a fresh OpenCode session so changed instructions are loaded.
- [ ] Confirm the default `developer` agent is selectable.
- [ ] Confirm specialist agents can be invoked by their configured names.
- [ ] Verify reviewer agents cannot edit/write files or execute non-read-only shell commands.
- [ ] Verify the developer selects only relevant detailed rules and technology skills.
- [ ] Run one low-risk Spec Kit feature through implementation, review, verification, and convergence.
- [ ] Confirm final reports distinguish executed checks from passed checks and skipped checks.
- [ ] Add executable CI enforcement for repeatable quality gates; prompt rules alone are not enforcement.
