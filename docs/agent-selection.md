# Agent Selection and Delegation Guide

## Core idea

External workflows (for example Spec Kit) define the development lifecycle; OpenCode agents define who performs or reviews a bounded part of that lifecycle. Do not map every workflow stage to a separate agent. Keep one primary developer selected so feature work and implementation have a single owner.

## Recommended selection matrix

| Work/stage | Primary | Delegate when useful | Why |
|---|---|---|---|
| Understand an existing repo | developer | explorer | Discover modules, entry points, tests, conventions, and existing capabilities without flooding the primary context. |
| Specify behavior | developer + product owner | explorer only for fact-finding | The spec owns requirements. A stakeholder resolves business decisions; agents should not invent them. |
| Clarify | developer + stakeholder | usually none | Keep ambiguity and answers in one authoritative feature artifact. |
| Plan a cross-cutting feature | developer | explorer; architecture-reviewer | Verify existing architecture and challenge design before tasks are fixed. |
| Create checklists/tasks | developer | test-reviewer or security-reviewer for critique | Primary owns the plan/task artifacts and dependency order. |
| Analyze artifacts | developer | explorer only for targeted fact-finding | Resolve contradictions in the source artifacts; don't let reviewers rewrite them. |
| Implement | developer | initially avoid parallel writers | Single writer avoids overlapping file edits and integration confusion. Add a path-scoped worker (`docs/templates/implementation-worker-agent.md`) only after boundaries are stable. |
| Review implementation | developer | code-reviewer | Independent read-only review catches issues the implementer may miss. |
| Security-sensitive change | developer | security-reviewer | Specialized threat/abuse-case review. |
| Test strategy / critical flows | developer | test-reviewer | Challenge acceptance coverage, edge cases, and test-layer choice. |
| IaC/CI/CD/deployment changes | developer | infra-reviewer | Review state, permissions, destructive diffs, rollback, and operations. |
| Converge/finalize | developer | reviewers for unresolved risk | Primary closes generated gaps, reruns checks, and owns the report. |

## When not to delegate

- A one-line change with clear scope.
- A trivial local rename or typo correction.
- Work where the subagent would need the entire conversation to be useful.
- Tightly coupled changes to the same files.
- A task where delegate/setup/review overhead exceeds the work.

## Delegation request template

```text
Objective:
Feature/task ID:
Relevant acceptance criteria:
Context and constraints:
Files/symbols to inspect:
Scope / out of scope:
Permission boundary: read-only unless explicitly stated
Expected response:
- findings with file/symbol references
- evidence examined
- risks/assumptions
- recommended next step
Do not modify files or delegate further.
```

## Reviewer timing

- Architecture reviewer: before implementation for broad architecture changes; optionally after implementation to verify that the design was followed.
- Test reviewer: before or after implementation for complex workflows, safety-critical logic, or high regression risk.
- Security reviewer: during planning for security-sensitive designs and after implementation for affected trust boundaries.
- Code reviewer: after a coherent diff exists, preferably after relevant tests pass; repeat after material fixes.
- Infra reviewer: before applying IaC/deployment changes and after changes are prepared, never as permission to deploy.

Reviewers are advisory and read-only. The primary developer decides which findings are valid, makes changes, and re-runs relevant checks.
