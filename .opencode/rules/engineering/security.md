# Engineering Rule — Application and Product Security (SEC)

Security is a default engineering concern, not a late-stage optional review. Select controls based on assets, threats, data sensitivity, exposure, and risk. Use applicable OWASP guidance and relevant compliance requirements.

| ID | Requirement | Agent must enforce |
|---|---|---|
| SEC-01 | Secure by design | Consider assets, trust boundaries, attack surfaces, abuse cases, and security requirements during specification and design. |
| SEC-02 | Input validation | Validate untrusted data at trust boundaries using explicit schemas, bounds, allowlists, and domain constraints. |
| SEC-03 | Output encoding | Encode output appropriately for its destination context; avoid unsafe HTML, template, shell, and serialization behavior. |
| SEC-04 | Authentication | Use established, secure authentication mechanisms; avoid custom cryptography or homegrown authentication flows. |
| SEC-05 | Authorization | Enforce authorization at trusted server/service boundaries for every protected operation and relevant object/tenant. UI hiding alone is not authorization. |
| SEC-06 | Least privilege | Grant users, services, agents, pipelines, and infrastructure only the permissions required. |
| SEC-07 | Secrets management | Do not hardcode secrets. Use approved secret stores, protected environment injection, rotation processes, and secret scanning. |
| SEC-08 | Sensitive data protection | Protect sensitive data in transit and at rest according to its classification, threat model, and applicable requirements. |
| SEC-09 | Injection prevention | Use parameterized queries and safe APIs; prevent SQL, command, LDAP, template, path, and other injection classes relevant to the stack. |
| SEC-10 | Dependency security | Evaluate dependencies for known vulnerabilities, provenance, maintenance, license, and necessity; use approved scanning. |
| SEC-11 | Session and token security | Protect token/session generation, storage, scope, expiry, renewal, revocation, and transport. Avoid leaking tokens in URLs or logs. |
| SEC-12 | Safe error handling | Do not expose stack traces, secrets, internal topology, sensitive records, or implementation details to untrusted clients. |
| SEC-13 | Security audit logging | Log relevant authentication, authorization, administrative, and security events while excluding secrets and unnecessary sensitive values. |
| SEC-14 | Threat modeling | For high-risk or cross-boundary changes, identify assets, entry points, trust boundaries, threats, mitigations, and residual risks. |
| SEC-15 | Secure defaults and fail-closed behavior | Default to deny for access decisions; fail safely when authorization, validation, or security configuration cannot be established. |
| SEC-16 | Privacy and data minimization | Collect, retain, process, and expose only data needed for the stated purpose; honor retention, deletion, and consent requirements. |
| SEC-17 | Security testing | Test relevant access controls, abuse cases, input handling, data exposure, dependency/configuration weaknesses, and security failure paths. |

## Minimum security review questions

- Who can call this operation, and how is that checked?
- Can a caller access another user's or tenant's object by changing an identifier?
- Which inputs are untrusted, and where are they validated/encoded?
- Could data, tokens, secrets, or personal information appear in logs, errors, URLs, telemetry, or test artifacts?
- What happens when an authorization provider, secret store, or dependency fails?
- Are new dependencies, permissions, ports, endpoints, or pipeline capabilities introduced?
