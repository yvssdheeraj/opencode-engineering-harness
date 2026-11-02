# Engineering Rule — Database and Data Management (DATA)

Select storage and consistency techniques according to domain requirements, data volume, access patterns, and operational constraints.

| ID | Requirement | Agent must enforce |
|---|---|---|
| DATA-01 | Data modeling | Model entities, relationships, identifiers, types, ownership, and lifecycle in a way that reflects domain needs and access patterns. |
| DATA-02 | Data integrity | Enforce invariants using suitable constraints, validation, transactions, and domain rules; do not rely only on UI validation. |
| DATA-03 | Versioned migrations | Track schema changes in version control using the project's migration mechanism; do not make undocumented manual production changes. |
| DATA-04 | Backward compatibility | Consider old and new application versions, producers, consumers, and rolling deployment order when changing schemas. |
| DATA-05 | Transaction management | Use transactions and suitable isolation for operations that require consistency; keep transaction scope bounded. |
| DATA-06 | Query efficiency | Inspect query patterns and avoid N+1 access, accidental full scans, unnecessary joins, and over-fetching. |
| DATA-07 | Indexing | Add or change indexes based on query patterns and evidence; consider write overhead, size, selectivity, and migration impact. |
| DATA-08 | Connection management | Use controlled pooling, timeouts, lifecycle management, and capacity settings. |
| DATA-09 | Data lifecycle | Define retention, archival, deletion, and legal/business lifecycle behavior where applicable. |
| DATA-10 | Data privacy | Classify and protect personal, sensitive, regulated, and tenant-specific data. Minimize unnecessary collection and exposure. |
| DATA-11 | Backup and restore | Provide appropriate backups and test restoration for data whose loss would matter. |
| DATA-12 | Test and seed data | Use reproducible, safe seed/fixture data; do not embed production secrets or personal data. |
| DATA-13 | Migration verification | Test forward migrations and relevant rollback/forward-recovery procedures; inspect destructive operations and data transformations before execution. |

## Migration safety

- Identify table/column changes, data backfills, locks, runtime duration, storage impact, and deployment ordering.
- Prefer expand-and-contract patterns when old and new application versions must coexist.
- Do not run migrations against shared or production environments without appropriate authorization.
- Treat rollback as a designed recovery strategy; a down migration is not always safe after new writes occur.
