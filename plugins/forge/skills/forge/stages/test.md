# Stage: test

Input: spec `## Acceptance criteria` (if spec exists) + design §Test coverage, implemented code. Apply `rules/test-standards.md` and the quality gate `rules/quality.md` (QG1–QG8).

## Steps

1. **Plan** — refine design §Test coverage into a table: test name, level (unit/integration/e2e), covers (R#/UC#), data needed. Include negative, edge, authz (other tenant / missing role), idempotency/retry cases where relevant. Every R#/UC# — and every spec `AC` — ≥1 test (TS9). Approval point only on deep path; else continue.
2. **Locate conventions** — existing test dirs, helpers, factories, page objects. New selectors go in page objects (TS6).
3. **Implement** missing tests.
4. **Quality gate** — `python3 <skill dir>/scripts/quality_detect.py <repo>` → load matching `rules/profiles/*.md`; write detected checks to ledger `Checks:` line. Run relevant checks (QG1): lint / type / format for changed languages, the tests covering changed code, broader regression on deep path or shared-module change. Coverage per QG6.
4a. **Visual/interaction verification** — when UI changed, apply `rules/ux.md`: use existing browser tools to exercise applicable UX flows and responsive states, capture implementation screenshots, compare with approved visual intent, link evidence in the ledger, and report meaningful deviations or missing checks. No additional framework required for minor changes.
5. **Record evidence** (QG2, QG3) — one ledger Log line per check: `check <name>: <command> → exit <n>, <counts>`; unrun → `not run: <reason>`. Paste summary (pass/fail counts, failing names + first error line).
6. **Failures** — real bug → back to develop (reopen item, Log `[rework]`). Test bug → fix test, assertion stays honest (TS1, G5). Lint/type failure on changed code → finding for review's fix loop (QG8).
7. **Record** — design `Status:` + index updated.

## Done when

- Every R#/UC# (spec: every `AC`) mapped to a passing test, or listed as uncovered with reason user accepted.
- Spec exists and every AC has test evidence in ledger `Verified by` → spec status `verified`.
- Suite run result pasted; no skips/only added (TS2).
- Every detected check either has evidence or `not run: <reason>` (QG3).
- Next = `review test` (deep) / `review code`.
