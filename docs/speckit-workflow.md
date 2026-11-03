# How OpenCode Agents Fit into the Spec Kit Ecosystem

## Responsibility split

| Concern | Owner |
|---|---|
| User intent, requirements, acceptance criteria | User/product owner, recorded through Spec Kit artifacts |
| Durable engineering principles | Project team, captured by `/speckit.constitution` |
| Spec, plan, tasks, checklists, analysis, convergence | Spec Kit commands/artifacts |
| Shared behavior, permissions, and role boundaries | OpenCode configuration and agent files |
| Detailed stack/domain practices | OpenCode `SKILL.md` files, loaded on demand |
| Actual quality enforcement | Tests, linters, type checkers, scanners, CI, reviewers, deployment controls |

Spec Kit is not an agent directory; OpenCode is not a requirements tracker. Keep the two responsibilities distinct.

## Recommended full feature cycle

1. **Constitution:** Run `/speckit.constitution` once for the project. Put short, durable, verifiable principles in the constitution. Keep detailed rules in `.opencode/rules/`.
2. **Specify:** Run `/speckit.specify` with the feature intent. Focus on what users/business need, not premature framework decisions.
3. **Clarify:** Run `/speckit.clarify` when material ambiguity exists. Record decisions in the feature artifacts.
4. **Plan:** Run `/speckit.plan`. The primary developer detects the existing stack, reads relevant architecture/security/reliability rules, loads technical skills, and may ask `explorer` to map existing code. For cross-cutting changes, use `architecture-reviewer` before accepting the plan.
5. **Checklist:** Run `/speckit.checklist` for risk-appropriate requirement-quality checklists. Consider security, accessibility, performance, operability, data migration, and failure behavior where relevant.
6. **Tasks:** Run `/speckit.tasks`. Ensure tasks are ordered, scoped, traceable, and testable. Include migration, documentation, observability, and CI work when needed.
7. **Analyze:** Run `/speckit.analyze`. Fix inconsistencies at their source before implementation.
8. **Implement:** Run `/speckit.implement`. The primary developer remains the single write owner by default. It loads relevant skills, applies TDD where practical, updates tests/docs, and reports task evidence.
9. **Converge:** Run `/speckit.converge`. If it adds missing tasks, implement them and run converge again until it reports `Converged`.
10. **Independent review:** Use code/security/test/architecture/infra reviewers according to risk. Resolve findings and re-run affected tests.
11. **Final report:** Summarize tasks, modified files, exact verification, review findings, what was not run, and remaining risk.

The clarify, checklist, and analyze gates are especially valuable for meaningful or risky work; do not turn them into unnecessary ceremony for trivial changes. Check the installed Spec Kit version for the exact command set and invocation syntax.

## Example: customer registration API

- `specify`: customer can register with required details and defined behavior for duplicate email.
- `clarify`: define email uniqueness, verification, password policy, and error disclosure.
- `plan`: identify existing auth module, service, persistence, migrations, API style, and deployment constraints; explorer can inspect the current code.
- `checklist`: authentication/authorization, input validation, privacy, audit/telemetry, migration safety, failure behavior.
- `tasks`: schema/migration, domain/service behavior, API endpoint, tests, documentation, metrics/logging as applicable.
- `analyze`: fix missing dependencies or contradictions.
- `implement`: developer reads the applicable `.opencode/rules/engineering/*.md` files (`api-and-integration.md`, `testing.md`, `data-management.md`, `security.md`) and loads the detected framework/database skills (for example `spring-boot`, `postgresql`). It does not load unrelated frontend/IaC skills.
- `review`: security-reviewer checks auth, hashing, sensitive data, enumeration; test-reviewer checks edge cases; code-reviewer checks final diff.
- `converge`: close gaps against spec and tasks.

## Preserve generated files

Spec Kit's OpenCode integration installs command markdown files under `.opencode/commands/` and may add an event plugin reference to OpenCode configuration. Do not overwrite these during template adoption. If you update/reinstall the Spec Kit integration, inspect the diff and preserve custom configuration.

## Large features and parallelism

Start single-writer. If the plan has genuinely independent workstreams, define file ownership and interfaces in `tasks.md` first. Then consider a separate implementation worker with explicit write permissions scoped to its files. Integrate and test in the primary developer. Do not let multiple agents edit the same files or feature artifacts concurrently.
