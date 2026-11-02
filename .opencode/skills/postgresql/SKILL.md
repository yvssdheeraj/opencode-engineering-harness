---
name: postgresql
description: Use when the affected system uses PostgreSQL and the task changes schemas, SQL, indexes, transactions, migrations, roles, or database performance.
---

# PostgreSQL Skill — Starter Guidance

- Detect the supported PostgreSQL server version, extensions, migration tool, and client/ORM versions.
- Prefer constraints for durable invariants; understand NULL semantics, uniqueness, foreign keys, and check constraints.
- Review transaction isolation, locks, long-running transactions, and migration locking impact.
- Use EXPLAIN (and EXPLAIN ANALYZE only when safe) to evaluate query plans with representative data.
- Add indexes for measured query patterns and account for write/storage cost.
- Use parameterized queries; never concatenate untrusted input into SQL.
- Consider JSONB, partitioning, full-text search, and advanced features only when requirements justify them.
- Use backward-compatible migration patterns for production data.
- Avoid running destructive operations against shared or production databases without explicit authorization.
