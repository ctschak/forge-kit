# Test standards

Defaults. Project rules win where stricter.

| ID | Rule |
|---|---|
| TS1 | A failing test fails with a specific, actionable message. Fix the cause; the assertion stays (`rules/guardrails.md` G5). |
| TS2 | Every test runs: no `.skip`, `.only`, `xit`, commented-out tests. |
| TS3 | Wait on state, not time: `waitFor({state})`, `expect.poll`, network-settled helpers. No `sleep` / `waitForTimeout`. |
| TS4 | Fail fast. Retries only for network flakes; locator/assert misses get zero retries. |
| TS5 | Selectors: stable CSS class → `data-testid` → exact `aria-label` → `id` → role + exact name. No copy-text / body regex. |
| TS6 | Selectors live in page objects / helpers, not specs. Verify against FE source. |
| TS7 | One behaviour per test; name says the behaviour (`rejects_duplicate_phone`). |
| TS8 | Deterministic data: factories/fixtures, unique per run, cleaned up. No shared mutable state between tests. |
| TS9 | Every requirement `R#` / use case `UC#` maps to ≥1 test; negative + edge cases included. |
| TS10 | Pyramid: logic → unit; boundaries (DB, API, queue) → integration; critical user journeys → e2e. |
| TS11 | Test repos hold test code + test data only. |
