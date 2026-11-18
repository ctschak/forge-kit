# Stage: architect

Owns design doc sections **Approaches → Feature flags** in the same design file. Input: approved Problem → Use cases.

Read first: `understanding.md` (conventions, existing modules, data model), matching `domains/*.md`, `rules/diagrams.md`.

## Grill

- Scale: volumes now / 12 months, peak patterns.
- Consistency: what must be transactional vs eventually consistent.
- Failure: what happens when each dependency is down/slow.
- Rollout: big-bang vs flagged vs migration window; rollback path.
- Ops: who gets paged, what dashboards/alerts.

## Write — every applicable section

| Section | Must contain |
|---|---|
| Approaches | ≥2 when a real choice exists; table (how, pros, cons, effort/risk); **one recommendation + why** |
| High-level design | component diagram (new/changed marked, DG4); sequence diagram per main UC with failure `alt`; components; data flow |
| Detailed design | per component: responsibility, interfaces/signatures, code snippet (new) or before/after (change); before/after flow (Change); state diagram if entity has lifecycle |
| Data model | ER diagram; tables/fields/types/indexes, migrations (forward + rollback), backfill |
| API design | every endpoint satisfies `rules/api-standards.md` API1 table; REST per API2; errors per API3/API4; payments per API5 |
| Security | each relevant `rules/security-checklist.md` item answered for this design |
| Feature flags | name, default, rollout steps, kill switch, removal task |
| Failure modes | dependency down/slow, retries, idempotency, timeouts, partial failure |
| Observability | logs (with request id), metrics, alerts |
| Test coverage | levels per `rules/test-standards.md` TS10; each R#/UC# mapped |

Diagrams: required set per `rules/diagrams.md` DG2 (architect column); every one captioned (DG3) and matching the text (DG7).

Stay consistent with existing conventions; any deviation states why.

## Done when

- Recommendation made; every API row filled incl. every error case.
- DG2 diagrams present (or `n/a — <why>`), captioned, consistent with text.
- Security + flags + test coverage present.
- User approved → `Status: architect · ✅`; next = `review design` + `review arch` (deep).
