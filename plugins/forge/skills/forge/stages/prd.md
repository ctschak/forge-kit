# Stage: prd

One living PRD of **released** behavior: `<root>/PRD.md` from `templates/prd.md`. Rules: `rules/contract.md` CT13, CT5. Planned work never goes here — it lives in specs until released.

## Baseline (existing product, no PRD yet)

Read first: `understanding.md` (no file + code exists → run `stages/onboard.md` first), product docs, supplied evidence (reports, screenshots, analytics exports), the code paths behind each capability.

1. **Inventory capabilities** from code + docs: routes / screens / jobs / integrations / roles. One `## FEAT-n` per user-meaningful capability (not per file).
2. **Evidence level per FEAT** — the strongest evidence you actually have:

| Level | Means |
|---|---|
| verified-prod | seen working in production (data, logs, user confirmation with date) |
| exercised-local | ran locally / demo / test env — say "demo data", "simulated webhook" etc. |
| code-only | implemented in code (`file:line`), not exercised |
| docs-only | described in docs/marketing, not found or not checked in code |
| not-exercised | code path exists but known not run (e.g. payments never sent) |

   Never write "works", "used" or "popular" without that evidence. Implemented ≠ used ≠ working.
3. **Requirements as they are today**: `FEAT-n.R<k>` bullets, business rules, permissions, limits — current behavior, including awkward behavior (describe, don't fix).
4. **Reconcile contradictions** (docs vs code vs report, e.g. plan count) → state each side + source under Known gaps; ask only if it changes the baseline.
5. **Findings from supplied reports** → Known gaps: `observed in <report, date, commit> — needs current verification`; verify against current code when cheap and say which.
6. **Open questions** from reports/users → `## Open decisions` (Q1…), preserved verbatim; no answers invented.
7. **KPIs + telemetry today**: what is actually measured / logged now; missing = `not measured`.
8. Validate: `python3 <skill dir>/scripts/spec_check.py prd <root>/PRD.md`.
9. **Approval point.** Show ≤ 15 lines: features + evidence mix, biggest gaps, open decisions. Approved → `status: approved`, `## Changes` line `YYYY-MM-DD rev 1: baseline`, then propose `git tag product-baseline-YYYY-MM-DD` (user runs, G2).

## Update

Only the release stage changes `PRD.md` (CT13). Corrections to the baseline itself (wrong evidence level, missed capability) → revision +1 with a `## Changes` line and re-approval.

## Done when

- `prd` check exit 0; every FEAT has an evidence level with a source; status `approved`; tag proposed.
