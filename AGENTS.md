# Repository Agent Instructions

This file is the repository-wide entry point for every OpenCode agent.

## First principles

- Treat actual repository state and current project documentation as authoritative; detect stack and versions rather than assuming them.
- Feature artifacts define feature intent; the Spec Kit constitution defines durable project-specific engineering principles.
- The primary `developer` agent owns feature implementation, integration, final verification, convergence, and reporting.
- Exploration and review agents (`explorer` and `*-reviewer`) are strictly read-only at the permission layer. Prompt instructions cannot override their `edit`/`write` denials; if bounded parallel implementation is ever required, define a dedicated path-scoped worker agent (`docs/templates/implementation-worker-agent.md`) with explicit file ownership.
- Preserve user changes and Spec Kit-generated files.

## Always-on instructions

`opencode.jsonc` loads the common operating contract for every agent:

- `.opencode/rules/common/communication.md`
- `.opencode/rules/common/context-management.md`
- `.opencode/rules/common/delegation.md`
- `.opencode/rules/common/tool-use.md`
- `.opencode/rules/common/autonomy-and-safety.md`
- `.opencode/rules/common/collaboration.md`
- `.opencode/rules/common/evidence-and-reporting.md`

## Detailed rule-loading protocol

Before meaningful work, read `.opencode/rules/workflow/task-execution.md`, `.opencode/rules/workflow/skill-selection.md`, and `.opencode/rules/workflow/quality-gates.md`. For Spec Kit work, also read `.opencode/rules/workflow/speckit-lifecycle.md`.

Then read the applicable domain rules. If a task crosses domains, load the union of relevant files.

| Task touches | Required detailed rules |
|---|---|
| Any application code | `engineering/coding-standards.md`, `engineering/testing.md`, `engineering/architecture.md` as appropriate |
| Architecture, module boundaries, refactoring | `engineering/architecture.md`, `engineering/coding-standards.md`, `engineering/cross-cutting-practices.md` |
| API, services, events, messaging | `engineering/api-and-integration.md`, `engineering/reliability.md`, `engineering/security.md`, `engineering/observability.md` as relevant |
| Authentication, authorization, PII, secrets, trust boundaries | `engineering/security.md`; select `security-review` skill |
| Database, persistence, schema, migration, cache | `engineering/data-management.md`, `engineering/performance.md`, `engineering/reliability.md`, `engineering/security.md` as relevant |
| Frontend, UI, mobile, client application | `engineering/frontend.md`, `engineering/accessibility-and-ux.md`, `engineering/testing.md`, `engineering/security.md` as relevant |
| Performance/scale-sensitive behavior | `engineering/performance.md`, `engineering/observability.md`, `engineering/reliability.md` |
| Reliability, distributed systems, background jobs | `engineering/reliability.md`, `engineering/api-and-integration.md`, `engineering/observability.md`, `engineering/testing.md` |
| Infrastructure, cloud, containers, IaC | `engineering/infrastructure.md`, `engineering/security.md`, `engineering/reliability.md`, `engineering/observability.md` |
| CI/CD, build, release, deployment | `engineering/cicd.md`, `engineering/security.md`, `engineering/infrastructure.md`, `engineering/observability.md` |
| Logs, metrics, tracing, alerts | `engineering/observability.md`, `engineering/reliability.md`, `engineering/security.md` |
| Accessibility, user workflows, localization | `engineering/accessibility-and-ux.md`, `engineering/frontend.md` |
| Documentation, ADRs, runbooks | `engineering/documentation.md`; `engineering/architecture.md` for ADRs |
| Git, commits, diffs, review | `engineering/git-and-review.md` |
| Cross-cutting architecture/method choice | `engineering/cross-cutting-practices.md` as applicable |

The complete numbered index is `.opencode/rules/RULE-CATALOG.md`.

## Skill selection

1. Inspect manifests, lockfiles, source, build files, tests, CI, containers, and IaC to detect technologies and versions.
2. Select skills based on both detected technology and the files/behavior affected by the task.
3. Load full `SKILL.md` instructions through the OpenCode skill mechanism when available; read the file directly if needed.
4. Skills guide implementation but do not enforce tests. Run the project's actual formatters, tests, linters, scanners, and build commands.
5. Do not load unrelated skills. If an applicable skill is missing, follow repository conventions, verify version-specific guidance, and propose a focused skill.

## Subagent delegation and mandatory review gates
The primary `developer` agent is the single write-owner by default; `explorer` and all `*-reviewer` agents are strictly read-only and advisory. Use `.opencode/rules/common/delegation.md` and `docs/templates/delegation-contract.md` when delegating bounded tasks:

- **Discovery (`explorer`):** Delegate bounded codebase fact-finding during `/speckit.specify`, `/speckit.plan`, or `/speckit.analyze` to avoid flooding primary context.
- **Architecture review (`architecture-reviewer`):** Delegate before accepting `/speckit.plan` on cross-cutting features or module-boundary changes, and optionally after implementation.
- **Security review (`security-reviewer`):** Delegate during `/speckit.plan` and after `/speckit.implement` whenever work touches authentication, authorization, PII, secrets, or trust boundaries.
- **Test review (`test-reviewer`):** Delegate during `/speckit.tasks` or after `/speckit.implement` for complex workflows, safety-critical logic, or high regression risk.
- **Infrastructure review (`infra-reviewer`):** Delegate before and after preparing IaC, container, CI/CD, or deployment changes.
- **Code review (`code-reviewer`):** Delegate after a coherent implementation diff exists and relevant tests pass, and repeat after material fixes before final convergence.
- **When NOT to delegate:** Never delegate one-line changes, trivial renames, typo fixes, or tightly coupled edits where delegation overhead exceeds the work.

## Spec Kit integration

- Spec Kit owns specification, plan, task, analysis, implementation orchestration, and convergence artifacts/commands.
- Keep the primary `developer` selected for `/speckit.*` command unless project-specific integration guidance says otherwise.
- Use specialists for bounded discovery or review; do not let several agents edit the same Spec Kit artifact concurrently.
- Preserve Spec Kit-generated `.opencode/commands/` and integration event/plugin configuration.
- Do not shadow or recreate existing `/speckit.*` commands.
- Use the installed command syntax shown by the current integration; these commands are invoked in OpenCode chat, not assumed shell commands.
- Do not mark tasks complete or claim convergence without actual implementation and evidence.

## Project-specific facts to maintain

Replace these placeholders after inspecting the real repository:

- Project purpose: TODO
- Architecture and module boundaries: TODO
- Languages/frameworks and versions: TODO
- Build/test/lint/security commands: TODO
- Local run commands: TODO
- CI checks and release flow: TODO
- Datastores and external integrations: TODO (no secrets)
- Compatibility, security, and operational constraints: TODO
