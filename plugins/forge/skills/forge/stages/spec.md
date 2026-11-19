# Stage: spec

Write the one product document engineering builds from. File: `tasks/NN_<slug>/YYYY-MM-DD_<slug>_spec.md` from `templates/spec.md`. Contract: `rules/contract.md` (CT1–CT14). Approval point on every path (G1).

Read first: discover output in the same spec (standard, deep); request + code for fast; `understanding.md`; specs/FEATs it depends on or changes (link, don't copy — CT9).

## Steps

1. **Fill sections for the path** (CT3). Write only what a builder or reviewer needs; `n/a — <why>` beats filler.
   - **Fast defect:** reproduce or locate root cause, cite `file:line`; add `## Fix` with before → after code and the failing test that proves the bug.
2. **Requirements + criteria** (CT4): `R1…` testable behavior; `AC1…` measurable (number + unit, or observable yes/no), each citing its R. Include edge/error cases that matter to users.
3. **KPIs + telemetry** (standard, deep): primary KPI + guardrail; baseline (value or `not measured`), target `(assumption)`, how measured; events needed to compute them. No PII in event properties.
4. **Priorities** (standard, deep): Now = MVP slice, aim 2–3 days of build, with what was cut and why; Next = path to production-ready (aim ≤ 2 weeks) or the constraint that prevents it; Later.
4a. **UX** (`rules/ux.md` UX1): material UI change → front matter `ui: true`, run `stages/ux.md` now (prototype + screenshots + `## UX`); the approval below covers both. Small UI change → reuse components, screenshots at test. No UI → skip.
5. **Validate**: `python3 <skill dir>/scripts/spec_check.py check <spec>`. Fix every error; ask the user only when the fix needs their decision.
6. **Approval point.** Show ≤ 15 lines: objective + success/failure, MVP slice, non-goals, R/AC counts, KPIs, open assumptions, prototype path + screenshots (if `ui: true`), `validator: OK`. Ask to approve rev N.
   - Approved → `## Approvals` line `YYYY-MM-DD <name> rev N` (CT7), status `approved`, index row updated, re-run validator.
   - Changes → revise, re-validate, ask again.
7. **Continue** (SKILL.md §5): fast → develop; standard/deep → design. Print the one-line next step and start it.

## Later changes

- Engineering asks a question → answer in `## Clarifications` (dated). Answer changes scope → CT8: revision+1, status `proposed`, `## Changes` line, re-approve; tell engineering the design's pinned rev is stale.

## Done when

- Validator exit 0; status `approved` with matching approval line; index updated; next step started.
