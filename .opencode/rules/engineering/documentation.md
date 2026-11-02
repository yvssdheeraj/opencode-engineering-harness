# Engineering Rule — Documentation and Knowledge Management (DOC)

Documentation should describe actual behavior and help users, developers, operators, and future agents work safely.

| ID | Requirement | Agent must enforce |
|---|---|---|
| DOC-01 | README accuracy | Keep purpose, prerequisites, setup, execution, testing, and contribution instructions accurate. |
| DOC-02 | Architecture documentation | Document material system boundaries, components, dependencies, data flows, and deployment structure. |
| DOC-03 | API documentation | Update API contracts, schemas, examples, and compatibility information when APIs change. |
| DOC-04 | Architecture Decision Records | Record consequential architecture decisions, context, alternatives, trade-offs, and consequences in ADRs. |
| DOC-05 | Operational documentation | Update deployment, monitoring, troubleshooting, backup, recovery, and runbook material when operational behavior changes. |
| DOC-06 | Configuration documentation | Document configuration options, required variables, defaults, and environment behavior without exposing secrets. |
| DOC-07 | Testing documentation | Document how to run relevant tests and any required local services, fixtures, or environment setup. |
| DOC-08 | Artifact synchronization | Update affected specifications, diagrams, examples, and task artifacts when implementation or design changes make them stale. |
| DOC-09 | Documentation freshness | Remove or correct instructions that no longer match actual behavior; do not leave misleading examples. |
| DOC-10 | Developer onboarding | Ensure a new developer can understand the project and reproduce the basic setup using documented steps. |

## Documentation as code

- Store important technical docs near the code or in the repository's established documentation location.
- Prefer examples that are executable or verified where practical.
- Keep documentation changes scoped to the behavior or workflow that changed.
