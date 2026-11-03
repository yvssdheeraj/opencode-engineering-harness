# Adoption Steps

## A. Inspect before installing

1. Run `opencode --version`, `specify version`, and `python3 --version`.
   - This blueprint uses **OpenCode V2** configuration syntax (`permissions` array, `shell`, `subagent`) and is tested with **Spec Kit (`specify-cli`) `>= 1.2.x`**.
   - Do not mix OpenCode V1 (`permission` map, `bash`, `task`) and OpenCode V2 permission formats.
2. Inspect `git status`; commit or back up existing work.
3. Inspect whether `.specify/`, `specs/`, `.opencode/commands/`, `.opencode/plugin/`, `opencode.json`/`opencode.jsonc`, and `AGENTS.md` already exist.
4. Do not run an initializer with `--force` until you understand what it will merge or replace.

## B. Install or add Spec Kit's OpenCode integration

- New project: `specify init <project-name> --integration opencode`
- Existing initialized Spec Kit project: `specify integration install opencode`
- Use `specify version` to verify the CLI. Check the official integration guide if your project already has another integration or commands.

Spec Kit commands are run in the OpenCode chat, not in the terminal. The OpenCode integration uses dotted commands such as `/speckit.specify`.

## C. Merge this blueprint

1. Copy `.opencode/agents/`, `.opencode/rules/`, and `.opencode/skills/` into the repo, merging rather than replacing any existing definitions.
2. Merge `opencode.jsonc` fields into the repository's existing OpenCode config. Do not maintain duplicate conflicting config files.
3. Merge root `AGENTS.md` guidance into the existing one. Preserve repository-specific facts and generated instructions.
4. Leave Spec Kit's `.opencode/commands/` and `.opencode/plugin/` intact.
5. Inspect effective permissions. `opencode.jsonc` relies on OpenCode V2's built-in defaults (`read`, `glob`, `grep`, `skill`, and `.env` approval prompts) and sets `shell`, `external_directory`, `websearch`, and `webfetch` to `"ask"` so OpenCode prompts the developer and stores **"Allow always"** command prefixes per project. `explorer` and `*-reviewer` agents deny `edit`, `subagent`, and non-Git `shell` commands.

## D. Tailor the project

1. Run `/speckit.constitution` using `docs/templates/constitution-input.md` as input guidance.
2. Run `/init` or manually fill the project-specific section in `AGENTS.md` with verified architecture, commands, versions, and conventions.
3. Remove example technology skills in `.opencode/skills/` that do not apply to the repo, install relevant stack skills from `skills.sh` (`npx skills add <owner/repo> --skill <name> -a opencode`), and vet their `SKILL.md` descriptions/instructions per `docs/adding-skills.md` (or author custom skills using `docs/templates/technology-skill-template.md`).
4. Add exact test/build/lint commands to the project docs and CI. To reduce approval prompts during TDD while keeping destructive commands gated, either use OpenCode V2's **Allow always** prompt option (which saves project-scoped command-prefix approvals) or append narrowly scoped non-destructive command rules after `{ "action": "shell", "resource": "*", "effect": "ask" }` in `opencode.jsonc`:

   ```jsonc
   { "action": "shell", "resource": "*", "effect": "ask" },
   { "action": "shell", "resource": "git status *", "effect": "allow" },
   { "action": "shell", "resource": "git diff *", "effect": "allow" },
   { "action": "shell", "resource": "git log *", "effect": "allow" },
   { "action": "shell", "resource": "git show *", "effect": "allow" },
   { "action": "shell", "resource": "pytest *", "effect": "allow" },
   { "action": "shell", "resource": "npm test *", "effect": "allow" },
   { "action": "shell", "resource": "git push *", "effect": "deny" },
   { "action": "shell", "resource": "rm -rf *", "effect": "deny" }
   ```

5. Review the quality-gate rules with the team. Some checks may be conditional or handled by CI rather than the agent.

## E. Validate the setup

1. Run the automated readiness doctor to verify configuration syntax, permission contracts, rule catalogue integrity, and resolved `AGENTS.md` placeholders:

   ```sh
   python3 scripts/validate_harness.py --mode project
   ```

2. Start a fresh OpenCode session so changed instructions are loaded.
3. Confirm the `developer` primary agent is selectable/default.
4. Confirm the named read-only subagents appear in the agent list.
5. Ask `developer` to inspect repository structure and identify applicable rules/skills without editing.
6. Ask `explorer` to locate a known symbol; verify it cannot edit or run non-Git shell commands.
7. Ask `code-reviewer` to inspect a harmless existing diff or small sample; verify no edits are made.
8. Run `/speckit.constitution` and one small feature through the Spec Kit workflow.
9. Inspect `git diff` and OpenCode config after setup.

## F. Roll out gradually

- Begin with one small feature and a single primary writer.
- Track false-positive rule enforcement, missed checks, agent context usage, test escape defects, and review value.
- Refine skill descriptions so they trigger on the right tasks.
- Add CI enforcement for repeatable checks. Prompt instructions alone are not enforcement.
- Add write-capable specialist workers only when file ownership and integration boundaries are well-defined.
