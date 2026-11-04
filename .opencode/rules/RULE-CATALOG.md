# Complete Rule Catalogue

This index maps every numbered requirement discussed for the agent framework to its authoritative rule file. A rule ID is stable and should not be silently reused for a different requirement.

## Common agent operating rules

| ID range | Area | File |
|---|---|---|
| COM-01–COM-10 | Communication and tone | `common/communication.md` |
| CTX-01–CTX-12 | Context and token efficiency | `common/context-management.md` |
| DEL-01–DEL-15 | Delegation and orchestration | `common/delegation.md` |
| TOOL-01–TOOL-10 | Tool discipline | `common/tool-use.md` |
| AUTO-01–AUTO-10 | Autonomy and safety | `common/autonomy-and-safety.md` |
| COL-01–COL-10 | Collaboration and ownership | `common/collaboration.md` |
| EVID-01–EVID-10 | Evidence and reporting | `common/evidence-and-reporting.md` |

## Engineering requirements

| ID range | Area | File |
|---|---|---|
| ARCH-01–ARCH-15 | Architecture and design | `engineering/architecture.md` |
| CODE-01–CODE-15 | Coding standards and clean code | `engineering/coding-standards.md` |
| TEST-01–TEST-18 | Testing strategy, TDD, BDD | `engineering/testing.md` |
| SEC-01–SEC-17 | Security engineering | `engineering/security.md` |
| PERF-01–PERF-12 | Performance and scalability | `engineering/performance.md` |
| REL-01–REL-12 | Reliability and resilience | `engineering/reliability.md` |
| API-01–API-14 | API and integration design | `engineering/api-and-integration.md` |
| DATA-01–DATA-13 | Database and data management | `engineering/data-management.md` |
| OBS-01–OBS-10 | Observability | `engineering/observability.md` |
| FE-01–FE-18 | Frontend engineering | `engineering/frontend.md` |
| UX-01–UX-10 | Accessibility, UX, product quality | `engineering/accessibility-and-ux.md` |
| INFRA-01–INFRA-20 | Infrastructure and cloud | `engineering/infrastructure.md` |
| CICD-01–CICD-20 | CI/CD and release engineering | `engineering/cicd.md` |
| DOC-01–DOC-10 | Documentation and knowledge management | `engineering/documentation.md` |
| GIT-01–GIT-10 | Git hygiene and review | `engineering/git-and-review.md` |
| XENG-01–XENG-15 | Cross-cutting methods and practices | `engineering/cross-cutting-practices.md` |

## Workflow controls

| ID range | Area | File |
|---|---|---|
| QG-01–QG-17 | Quality gates / definition of done | `workflow/quality-gates.md` |
| SKILLSEL | Technology and domain skill selection | `workflow/skill-selection.md` |
| Task workflow | Before/during/after implementation | `workflow/task-execution.md` |

## Applicability

- These are a standards catalogue, not a command to apply every rule to every task.
- Agents must select all applicable rules based on the affected components and risk.
- If a rule is not applicable, the agent should not invent work to satisfy it.
- Critical or high-risk controls should be enforced by executable checks or review where possible, not only by prompt instructions.
