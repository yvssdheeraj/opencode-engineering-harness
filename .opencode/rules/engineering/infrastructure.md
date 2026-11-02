# Engineering Rule — Infrastructure, Cloud, and Platform Engineering (INFRA)

Apply these standards when modifying infrastructure, cloud resources, networking, containers, platform configuration, or deployment environments.

| ID | Requirement | Agent must enforce |
|---|---|---|
| INFRA-01 | Infrastructure as Code | Define managed infrastructure declaratively and keep definitions in version control. |
| INFRA-02 | Environment consistency | Keep environment configuration structurally consistent while separating environment-specific values and secrets. |
| INFRA-03 | Reproducibility | Make infrastructure reproducible from reviewed definitions, pinned inputs, and documented state/backend assumptions. |
| INFRA-04 | Least-privilege identity | Apply least privilege to IAM roles, workload identities, service accounts, and human access. |
| INFRA-05 | Secret handling | Keep secrets out of source, plans, state outputs, logs, container images, and public configuration; use approved secret stores. |
| INFRA-06 | Network security | Apply segmentation, private connectivity, ingress/egress restrictions, and exposure limits appropriate to the service. |
| INFRA-07 | Resource sizing and limits | Set appropriate CPU, memory, storage, request, concurrency, and autoscaling limits. |
| INFRA-08 | Availability design | Design redundancy and failure domains according to availability requirements and acceptable cost. |
| INFRA-09 | Backup and restoration | Define backup frequency, retention, protection, and tested restore procedures for critical resources. |
| INFRA-10 | Infrastructure validation | Run syntax, formatting, policy, and plan/preview validation before applying infrastructure changes. |
| INFRA-11 | Change review | Review planned create/update/replace/destroy actions and their dependencies before execution. |
| INFRA-12 | State management | Store IaC state securely with access control, locking, encryption, and backup as supported by the tool. |
| INFRA-13 | Drift detection | Detect and reconcile unintended differences between declared and deployed infrastructure. |
| INFRA-14 | Cost awareness | Assess resource cost, idle resources, data transfer, scaling behavior, and environment lifetime. |
| INFRA-15 | Infrastructure monitoring | Monitor capacity, availability, saturation, errors, and key platform dependencies. |
| INFRA-16 | Disaster recovery | Establish recovery/failover approach and test it in proportion to criticality and RTO/RPO needs. |
| INFRA-17 | Container security | Use trusted/minimal images, pin appropriate image references, scan vulnerabilities, avoid root where feasible, and minimize capabilities. |
| INFRA-18 | Configuration separation | Separate application configuration, platform settings, and secrets; avoid environment-specific values embedded in images or code. |
| INFRA-19 | Policy as Code | Apply automated policy checks for security, compliance, resource constraints, and approved platform patterns when appropriate. |
| INFRA-20 | Safe infrastructure rollout | Use reviewed plans, dependency-aware rollout, health validation, and recovery procedures; never apply destructive changes without authorization. |

## Infrastructure change checklist

- Inspect plan/preview and state/backend.
- Identify resource replacement or destruction.
- Check permissions, network exposure, secrets, data persistence, and costs.
- Confirm backup/recovery and rollout order where applicable.
- Do not execute production applies or destructive operations without explicit authorization.
