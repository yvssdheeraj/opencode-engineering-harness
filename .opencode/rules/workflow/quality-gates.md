# Workflow Rule — Quality Gates and Definition of Done (QG)

Quality gates are conditional on the change. The developer must identify which apply and why any material gate is not applicable. CI should enforce repeatable checks; agent prose alone is not enforcement.

| ID | Gate | Completion evidence |
|---|---|---|
| QG-01 | Requirements | Applicable acceptance criteria addressed; unresolved ambiguity disclosed. |
| QG-02 | Architecture | Design is consistent with project architecture or justified deviations/ADRs are recorded. |
| QG-03 | Implementation | Scoped behavior is implemented; no unexplained stubs, fake success, or unrelated changes. |
| QG-04 | Tests | Relevant unit, integration, contract, E2E, regression, and acceptance checks executed as applicable; results recorded. |
| QG-05 | Static quality | Applicable formatting, lint, type-check, and static-analysis checks pass. |
| QG-06 | Build | Relevant application/package build succeeds. |
| QG-07 | Security | Relevant trust-boundary, authorization, input, data, secrets, and dependency risks are assessed; unacceptable findings are resolved or escalated. |
| QG-08 | Data | Data integrity, migrations, compatibility, and recovery are reviewed where persistence changes. |
| QG-09 | Infrastructure | IaC validation/plan, permissions, destructive actions, and operational impact are reviewed where infrastructure changes. |
| QG-10 | Delivery | CI/CD, artifact, deployment, and rollback impact is assessed where delivery behavior changes; production action remains separately authorized. |
| QG-11 | Observability | New operationally important behavior is diagnosable where relevant. |
| QG-12 | Accessibility and UX | Relevant semantics, keyboard access, user states, and accessibility checks are addressed for UI changes. |
| QG-13 | Documentation | Relevant README, API docs, ADRs, configuration, runbooks, and feature artifacts are updated. |
| QG-14 | Git hygiene | Final diff is inspected and unrelated user changes are preserved. |
| QG-15 | Independent review | Appropriate specialist reviews are completed for the risk profile; material findings are resolved or explicitly accepted by an authorized owner. |
| QG-16 | Spec Kit convergence | Convergence is executed and its exact reported status is recorded; generated gaps are addressed or disclosed. |
| QG-17 | Final report | Changed files, commands/results, skipped checks, limitations, blockers, and risks are reported honestly. |

A green unit-test suite is not proof of integration, security, performance, accessibility, deployment, or operational correctness. Do not claim a gate passed without evidence.
