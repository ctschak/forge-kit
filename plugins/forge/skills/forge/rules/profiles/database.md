# Profile: Database

Loaded when detection returns `database` (migrations, SQL, ORM schema). Destructive operations need approval (`rules/guardrails.md` G6).

| ID | Check |
|---|---|
| DB1 | Migration validity: applies on a fresh DB and on a copy of current schema; ordered after existing migrations; idempotent where the tool expects it. |
| DB2 | Compatibility: expand → migrate → contract. Old code keeps working after the migration; column/table drops only in a later release. |
| DB3 | Rollback: down migration, or a stated reason it's safe to leave (additive nullable column) and the forward-recovery plan (`stages/design.md`). |
| DB4 | Constraints: NOT NULL, FK, UNIQUE, CHECK express the business rules the spec states; uniqueness enforced in DB, not only code. |
| DB5 | Transactions: multi-row writes atomic; isolation / locking chosen for contended rows; no long transactions around network calls. |
| DB6 | Indexes + queries: new query paths have an index or a stated reason; `EXPLAIN` for queries on large tables; no N+1 in loops. |
| DB7 | Tenancy + data safety: tenant key on every new table + query; backfills batched and resumable; PII columns minimized (SEC7). |
| DB8 | Destructive DDL/DML (drop, truncate, rewrite, mass update/delete) → never on shared/prod DBs without explicit approval + backup step. |
