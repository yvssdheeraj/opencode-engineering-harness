# Engineering Rule — CI/CD and Release Engineering (CICD)

Pipelines are production software and must be secure, reproducible, observable, and maintainable.

| ID | Requirement | Agent must enforce |
|---|---|---|
| CICD-01 | Automated builds | Build from version-controlled source using documented, repeatable pipeline steps. |
| CICD-02 | Automated tests | Run the applicable unit, integration, contract, and acceptance tests in CI. |
| CICD-03 | Code quality | Run the project's formatters, linters, type checks, and relevant static analysis. |
| CICD-04 | Security scanning | Include relevant SAST, dependency, secret, container, IaC, and configuration scanning. |
| CICD-05 | Reproducible build inputs | Control toolchain, dependency, base image, and build inputs sufficiently to make artifacts predictable. |
| CICD-06 | Artifact management | Version, store, retain, and access-control build artifacts and metadata appropriately. |
| CICD-07 | Environment promotion | Promote the same validated artifact across environments rather than rebuilding materially different artifacts for each environment. |
| CICD-08 | Deployment automation | Automate repeatable deployment steps and avoid undocumented manual procedures. |
| CICD-09 | Post-deployment verification | Run appropriate smoke tests, health checks, and deployment validation after rollout. |
| CICD-10 | Rollback/forward recovery | Define a tested rollback or forward-recovery plan appropriate to application, schema, and infrastructure changes. |
| CICD-11 | Migration coordination | Coordinate database migration ordering and compatibility with application release and rollback strategies. |
| CICD-12 | Branch and review protection | Protect important branches with required checks, review policy, and restricted bypass permissions. |
| CICD-13 | Pipeline security | Restrict job permissions, isolate untrusted contributions, protect secrets, and avoid unsafe privileged execution. |
| CICD-14 | Failure visibility | Preserve logs, test reports, artifacts, and actionable failure details for diagnosis. |
| CICD-15 | Release documentation | Maintain appropriate release notes, change history, migration notes, and operational notices. |
| CICD-16 | Deployment strategy | Choose rolling, canary, blue/green, recreate, or other strategies according to system architecture and risk. |
| CICD-17 | Feature flags | Use feature flags when they provide useful separation between deploying code and enabling behavior; manage ownership and flag removal. |
| CICD-18 | Pipeline maintainability | Keep pipelines modular, reusable, readable, and documented without hiding critical behavior in opaque templates. |
| CICD-19 | Dependency integrity | Pin or constrain build inputs appropriately and verify package, action, plugin, and image provenance where supported. |
| CICD-20 | Software supply-chain security | Use SBOMs, artifact provenance, signing, attestations, and verification where required by project risk or policy. |

## CI/CD implementation guidance

- Fail the pipeline on failed mandatory checks; do not make required quality gates informational-only without an approved reason.
- Separate validation, packaging, promotion, and deployment responsibilities.
- Do not expose deployment credentials to untrusted pull-request code.
- Do not deploy to production unless the user or approved workflow explicitly authorizes it.
