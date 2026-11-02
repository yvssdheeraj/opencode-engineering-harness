---
name: database-engineering
description: Use when designing schemas, queries, indexes, transactions, migrations, persistence models, or data lifecycle behavior.
---

# Database Engineering Skill

- Inspect current database engine, version, schema conventions, migration tooling, and access patterns.
- Model constraints and invariants explicitly.
- Prefer version-controlled, reviewable migrations; assess compatibility with live data and old application versions.
- Check transaction boundaries, locking, isolation, and idempotency.
- Use query plans and realistic data volumes before optimizing indexes or queries.
- Avoid N+1 behavior and unbounded reads.
- Protect PII and secrets; use synthetic test data.
- Define recovery/rollback or forward-fix strategy for risky migrations.
- Add appropriate repository/integration tests and verify migrations in a disposable test environment where possible.
