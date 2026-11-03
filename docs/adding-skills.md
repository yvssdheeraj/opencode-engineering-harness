# Adding and Managing Skills (`skills.sh` + Custom Skills)

In this harness:

1. **Stack-neutral engineering standards live in `.opencode/rules/`** (architecture, clean code, TDD/BDD testing, API design, database management, security, reliability, observability, CI/CD, and infrastructure), while **specialist roles live in `.opencode/agents/`** (`developer`, `explorer`, and `*-reviewer`).
2. **Technology and framework playbooks live in `.opencode/skills/`** (sourced from [skills.sh](https://skills.sh) or custom-authored using `docs/templates/technology-skill-template.md`), such as `react-typescript`, `spring-boot`, `postgresql`, `terraform`, Next.js, FastAPI, Go, etc.

## Installing community skills from `skills.sh`

When adopting this blueprint into a project, install technology skills for your actual stack from `skills.sh` into `.opencode/skills/`:

```sh
npx skills add <owner/repo> --skill <skill-name> -a opencode
```

### Vetting checklist for `skills.sh` skills (Mandatory)

Community skills are written by external authors for generic environments. Before committing an installed skill from `skills.sh`, review its `SKILL.md` (and any bundled files):

1. **Tighten the frontmatter `description`:** Many community skills use overly broad descriptions (for example, *"Use for all backend development"*), which causes OpenCode to load them on every prompt and waste context tokens. Edit `description` so it names the exact library/framework and task types.
2. **Verify `name` and folder match:** Ensure `.opencode/skills/<name>/SKILL.md` has a lowercase kebab-case `name` matching its directory name.
3. **Remove conflicting workflow commands:** Strip or ignore instructions inside third-party skills that tell the agent to auto-commit, bypass TDD, run unapproved `npx`/`curl` installers, or introduce competing libraries not used by your repo.
4. **Check bundled scripts for safety:** If the downloaded skill includes `scripts/` or executable files, inspect them before allowing the agent to run them.
5. **Remove unused starter skills:** Delete starter technology skills in `.opencode/skills/` that do not exist in your repository so they never clutter skill discovery.

## Skill design checklist (when authoring or tailoring a skill)

- One skill should cover one language/framework/platform/domain with a clear trigger.
- Use lowercase kebab-case for directory and `name`, matching exactly.
- Keep the description specific so the agent knows when to load it.
- State supported versions and tell the agent to inspect the actual project version first.
- Include implementation patterns, common anti-patterns, testing guidance, security/performance caveats, and verification commands.
- Prefer official documentation; avoid copying large documentation sections into the skill.
- Do not duplicate stack-neutral principles already covered by `.opencode/rules/`.
- Do not treat skill text as a substitute for tests, linters, scanners, or CI.

## Example skill selection

| Task | Technology skills to load | Engineering rules to read |
|---|---|---|
| Spring Boot endpoint with PostgreSQL | `spring-boot`, `postgresql` | `engineering/api-and-integration.md`, `engineering/testing.md`, `engineering/data-management.md`, `engineering/security.md` |
| React form | `react-typescript` | `engineering/frontend.md`, `engineering/accessibility-and-ux.md`, `engineering/testing.md` |
| Terraform network module | `terraform` | `engineering/infrastructure.md`, `engineering/security.md`, `engineering/reliability.md` |
| PostgreSQL migration | `postgresql` | `engineering/data-management.md`, `engineering/reliability.md`, `engineering/performance.md` |
| CI pipeline | CI provider skill (if installed) | `engineering/cicd.md`, `engineering/security.md`, `engineering/infrastructure.md` |

## Example: add a language/framework skill

1. Copy `docs/templates/technology-skill-template.md` to `.opencode/skills/<technology-name>/SKILL.md`.
2. Replace the name and description; ensure the folder and frontmatter name match.
3. Add verified guidance for the actual version used in your projects.
4. Add exact commands only after testing them in a representative repository.
5. Add one trigger example and one non-trigger example to reduce accidental loading.
6. Ask the developer agent to explain why it selected the skill for representative tasks.
7. Review and refine the description based on false-positive/false-negative selection.
