---
name: postgresql
description: Use when the affected system uses PostgreSQL and the task changes schemas, SQL, indexes, transactions, migrations, roles, or database performance.
---

# PostgreSQL Skill — Starter Guidance

## Supported scope

- Technology and version range: PostgreSQL 14–18+ (inspect the repository's actual server version, Docker/Compose manifests, or cloud database config before using version-specific SQL features).
- Last reviewed: 2026-11
- Runtime/build tooling: SQL migrations (Flyway, Liquibase, Alembic, Prisma, Drizzle, Goose, sqitch, or raw SQL) and application query layers.
- Framework modules covered: relational schema design, DDL migrations, indexing, query plans, transactions/locking, and role/permission boundaries.
- Out-of-scope / unsupported versions: EOL PostgreSQL (< 14) without explicit legacy support requirements; non-PostgreSQL engines and application-specific ORM mapping idioms (load the application framework skill separately).

## When to load

Load when the affected system uses PostgreSQL and the task changes schemas, SQL queries, indexes, constraints, transactions, migrations, database roles, or persistence performance. Do not load for in-memory or non-PostgreSQL stores.

## Before implementation

- Detect the supported PostgreSQL server version, installed extensions (`pgcrypto`, `citext`, `pg_trgm`, `postgis`, etc.), migration tool, and client/ORM versions.
- Inspect existing schema naming conventions, primary-key strategy, timestamp columns (`timestamptz` vs `timestamp`), and migration file ordering.
- Check whether migrations run automatically on startup or in a separate deployment step.

## Implementation standards

- Prefer database constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY`, exclusion constraints) for durable data invariants; account for PostgreSQL `NULL` semantics in unique constraints (`NULLS NOT DISTINCT` requires PostgreSQL 15+).
- Use backward-compatible expand-and-contract migrations for live tables; avoid long-held `ACCESS EXCLUSIVE` locks during online deployments (for example, consider `CREATE INDEX CONCURRENTLY` outside a transaction block, or adding `NOT VALID` constraints before validating).
- Review transaction isolation (`READ COMMITTED` default vs `REPEATABLE READ` / `SERIALIZABLE`), lock ordering, statement timeouts, and idle-in-transaction timeouts.
- Use parameterized queries exclusively; never concatenate untrusted input into SQL strings or dynamic PL/pgSQL.
- Add indexes (`B-tree`, `GIN`, `GiST`, partial, or covering `INCLUDE` indexes) for measured query predicates and sort orders while accounting for write amplification and storage overhead.
- Use `JSONB`, partitioning, or full-text search only when access patterns and query predicates justify them over normalized columns.

## Testing and verification

- Run forward migrations against a disposable local/containerized PostgreSQL instance and verify schema state and application compatibility.
- Use `EXPLAIN` (and `EXPLAIN (ANALYZE, BUFFERS)` only in non-production or safe transaction-rolled-back environments) to verify query plans:
  - Do not assume every `Seq Scan` is a defect; small lookup tables naturally use sequential scans. Flag a `Seq Scan` when `Rows Removed by Filter` is high relative to returned rows or shared buffer reads grow linearly with table size on a hot path.
  - Verify that new indexes actually appear as `Index Scan`, `Index Only Scan`, or `Bitmap Index Scan` under realistic row counts and parameter types.
- Test constraint violations, concurrent update races, null/boundary values, and rollback/forward-fix behavior.

## Completion checklist

- [ ] Implementation follows the actual PostgreSQL version and migration tool conventions.
- [ ] Migrations and repository/integration tests executed and verified.
- [ ] Lock impact, backward compatibility, and rollback/recovery strategy reviewed.
- [ ] No hardcoded credentials or destructive shared-environment operations executed without authorization.

## References

- PostgreSQL official documentation: https://www.postgresql.org/docs/current/
- PostgreSQL `ALTER TABLE` and concurrency notes: https://www.postgresql.org/docs/current/sql-altertable.html
- PostgreSQL `EXPLAIN` usage: https://www.postgresql.org/docs/current/using-explain.html
