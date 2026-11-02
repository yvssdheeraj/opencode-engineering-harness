---
name: security-review
description: Perform a focused application or change-level security review covering trust boundaries, access control, input handling, data exposure, secrets, dependencies, and abuse cases.
---

# Focused Security Review Skill

1. Identify assets, actors, trust boundaries, entry points, and privileged operations.
2. Trace input from untrusted source to parsing, business logic, storage, and output.
3. Verify authentication, authorization, ownership/tenant boundaries, and least privilege.
4. Inspect secret handling, logs, telemetry, error messages, and sensitive data lifecycle.
5. Check relevant injection, path traversal, SSRF, XSS, CSRF, deserialization, and resource-exhaustion risks.
6. Check dependency, build, container, CI, and infrastructure risks if touched.
7. Consider abuse cases and rate limiting.
8. Separate confirmed vulnerabilities from hardening recommendations and assumptions.
9. Report severity, exploit scenario, impact, evidence, and remediation.
10. Do not claim a complete security audit from a focused diff review.
