# Repository Agent Instructions

This file is the repository-wide entry point for every OpenCode agent.

## First principles

- Treat actual repository state and current project documentation as authoritative; detect stack and versions rather than assuming them.
- If feature artifacts (spec, plan, tasks) or project principles exist, treat them as the source of feature intent.
- The primary `developer` agent owns feature implementation, integration, final verification, and reporting.
- Exploration and review agents (`explorer` and `*-reviewer`) are strictly read-only at the permission layer. Prompt instructions cannot override their `edit`/`write` denials; if bounded parallel implementation is ever required, define a dedicated path-scoped worker agent (`docs/templates/implementation-worker-agent.md`) with explicit file ownership.
- Preserve user changes and generated integration files.

## Always-on instructions

`opencode.jsonc` auto-loads the common operating contract for every agent (communication, context, delegation, tool-use, autonomy, collaboration, evidence).

## Detailed rule-loading protocol

Before meaningful work, read `.opencode/rules/workflow/task-execution.md`, `.opencode/rules/workflow/skill-selection.md`, and `.opencode/rules/workflow/quality-gates.md`.

Then read the applicable domain rules from the routing table below. If a task crosses domains, load the union of relevant files.

| Task touches | Required detailed rules |
|---|---|
| Any application code | `engineering/coding-standards.md`, `engineering/testing.md`, `engineering/architecture.md` as appropriate |
| Architecture, module boundaries, refactoring | `engineering/architecture.md`, `engineering/coding-standards.md`, `engineering/cross-cutting-practices.md` |
| API, services, events, messaging | `engineering/api-and-integration.md`, `engineering/reliability.md`, `engineering/security.md`, `engineering/observability.md` as relevant |
| Authentication, authorization, PII, secrets, trust boundaries | `engineering/security.md`; delegate to `security-reviewer` |
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

- **Discovery (`explorer`):** Delegate bounded codebase fact-finding to avoid flooding primary context.
- **Architecture review (`architecture-reviewer`):** Delegate for cross-cutting features or module-boundary changes, before accepting the plan and optionally after implementation.
- **Security review (`security-reviewer`):** Delegate whenever work touches authentication, authorization, PII, secrets, or trust boundaries.
- **Test review (`test-reviewer`):** Delegate for complex workflows, safety-critical logic, or high regression risk.
- **Infrastructure review (`infra-reviewer`):** Delegate before and after preparing IaC, container, CI/CD, or deployment changes.
- **Code review (`code-reviewer`):** Delegate after a coherent implementation diff exists and relevant tests pass, and repeat after material fixes.
- **When NOT to delegate:** Never delegate one-line changes, trivial renames, typo fixes, or tightly coupled edits where delegation overhead exceeds the work.

## External integrations (optional)

- If feature artifacts (spec, plan, tasks) or generated command integrations (for example `.opencode/commands/`, `.specify/`, `specs/`) exist, treat them as read-only inputs unless the owning workflow explicitly says to update them.
- Do not shadow or recreate existing slash commands.
- Preserve generated integration configuration.
- Do not mark tasks complete without actual implementation and evidence.

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
