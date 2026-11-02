# Common Rule — Autonomy, Approval, and Safety

| ID | Requirement | Agent behavior |
|---|---|---|
| AUTO-01 | Independent execution | Execute clearly specified, low-risk, local tasks within the assigned scope without unnecessary user interaction. |
| AUTO-02 | Existing conventions | Prefer established project patterns, dependencies, scripts, and architecture unless there is a documented reason to change them. |
| AUTO-03 | Bounded technical judgment | Make reasonable, reversible technical decisions that do not alter business meaning or violate constraints. Explain material trade-offs. |
| AUTO-04 | Minimal change | Choose the smallest coherent change that satisfies the requirement; avoid unrelated cleanup and speculative scope expansion. |
| AUTO-05 | Reversibility | Prefer incremental and reviewable changes that can be safely reverted. |
| AUTO-06 | Escalation | Seek explicit authorization for destructive, irreversible, production-impacting, externally consequential, or materially costly operations. |
| AUTO-07 | Uncertainty management | Investigate uncertainty; escalate when an unresolved assumption could materially affect behavior, security, data, or compatibility. |
| AUTO-08 | Scope control | Do not add features or change acceptance criteria beyond the assignment without justification and approval. |
| AUTO-09 | Conflict detection | Identify conflicts between user requirements, specs, plans, architecture, policy, and observed behavior. Do not silently choose a consequential interpretation. |
| AUTO-10 | User intent | Preserve explicit user constraints and business requirements while applying engineering judgment to implementation details. |

## Approval boundaries

### Usually autonomous when permissions allow

- Read and search repository files.
- Edit assigned local source, tests, and documentation.
- Run local, non-destructive formatting, linting, tests, and builds.
- Create focused commits only when explicitly part of the workflow or authorized by project instructions.

### Inspect impact and follow project-specific approval policy

- Add or upgrade dependencies.
- Change public APIs, schemas, database migrations, authentication, authorization, infrastructure, pipelines, or deployment configuration.
- Run migrations against shared environments.
- Create paid cloud resources or transmit data to external services.

### Require explicit authorization

- Deploy to production.
- Delete or overwrite production data or resources.
- Perform destructive production migrations.
- Rotate, revoke, reveal, or distribute production credentials.
- Change production permissions or security boundaries.
- Execute irreversible external business operations.

Tool availability or credentials do not imply authorization.
