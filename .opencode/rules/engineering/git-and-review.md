# Engineering Rule — Git, Change Hygiene, and Code Review (GIT)

Protect user work and keep each change understandable, attributable, and reviewable.

| ID | Requirement | Agent must enforce |
|---|---|---|
| GIT-01 | Version control | Keep relevant source, tests, configuration, documentation, and IaC in the project's version control system. |
| GIT-02 | Focused changes | Keep each change scoped to the assigned task and make independent changes separable where useful. |
| GIT-03 | Meaningful commits | Use descriptive commit messages and the repository's convention when commits are authorized or requested. |
| GIT-04 | No unrelated changes | Avoid unrelated formatting, renames, dependency churn, and cleanup that obscure the task. |
| GIT-05 | Preserve user changes | Inspect Git status before and after work; never overwrite, reset, clean, or discard unrelated user modifications. |
| GIT-06 | Final diff review | Inspect the final diff for unintended changes, secrets, generated noise, missing files, and accidental deletions. |
| GIT-07 | Regression awareness | Assess affected callers, integrations, schemas, behavior, and public contracts before finalizing. |
| GIT-08 | Dependency review | Justify new dependencies; check necessity, maintenance, security, license, size, transitive impact, and version policy. |
| GIT-09 | Independent review | Use independent review proportional to risk; reviewers should inspect actual diffs and requirements, not only the developer's summary. |
| GIT-10 | Traceability | Keep implementation, commits, tests, and review findings traceable to the feature, task, or requirement. |

## Git safety

- Do not run destructive reset/clean/checkout/restore operations against user changes without explicit authorization.
- Do not rewrite shared history or force-push unless explicitly authorized and consistent with repository policy.
- Do not commit secrets, local state, generated outputs, or build artifacts unless the project explicitly requires them.
