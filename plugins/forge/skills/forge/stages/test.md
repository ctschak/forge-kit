# Stage: test

Input: spec `## Acceptance criteria` (if spec exists) + design §Test coverage, implemented code. Apply `rules/test-standards.md`.

## Steps

1. **Plan** — refine design §Test coverage into a table: test name, level (unit/integration/e2e), covers (R#/UC#), data needed. Include negative, edge, authz (other tenant / missing role), idempotency/retry cases where relevant. Every R#/UC# — and every spec `AC` — ≥1 test (TS9). Approval point only on deep path; else continue.
2. **Locate conventions** — existing test dirs, helpers, factories, page objects. New selectors go in page objects (TS6).
3. **Implement** missing tests.
4. **Run** — targeted, then the affected suite. Paste summary (pass/fail counts, failing names + first error line).
5. **Failures** — real bug → back to develop (new ledger row or reopen step). Test bug → fix test, assertion stays honest (TS1, G5).
6. **Record** — ledger Log line: suite, command, result. Design `Status:` + index updated.

## Done when

- Every R#/UC# (spec: every `AC`) mapped to a passing test, or listed as uncovered with reason user accepted.
- Spec exists and every AC has test evidence in ledger `Verified by` → spec status `verified`.
- Suite run result pasted; no skips/only added (TS2).
- Next = `review test` (deep) / `review code`.
