# Eval scenarios

Run with `evals/harness/` (see `evals/README.md`). Simulated user answers **only** from the scenario's facts; anything else → "I don't know". Record turns, questions, docs, secs per run in `evals/results/<date>-<slice>.md`.

| # | Variant (`setup.sh`) | User turns | Pass criteria |
|---|---|---|---|
| D1 idea → MVP | `empty` | `D1-idea-to-mvp.md` opening prompt (prefix `/forge:forge new`) → answers from its fact sheet → approve | `D1-idea-to-mvp.md` P1–P6 |
| D3 don't build | `shelftrack` | `/forge:forge new Our biggest customer asked for AI demand forecasting in ShelfTrack. Let's build it next sprint — please plan it. (Our numbers are in docs/evidence.md.)` → facts from `D3-dont-build.md` | `D3-dont-build.md` P1–P5 |
| E1 fast bug | `projapp` | `/forge:forge Bug: GET projects page 1 shows nothing for orgs with fewer than 20 projects (list_projects). Please fix.` | `results/2026-11-18-sliceA.md` E1 |
| E2 standard spec → plan | `projapp` | `/forge:forge design SPEC-1` → `Approve.` | sliceA E2 (incl. migration rollback) |
| E3 vague external PRD | `projapp-prd-input` | `/forge:forge design docs/prd-export.md` | sliceA E3 (gaps listed, nothing invented) |
| Q1 fast UI fix | `webapp` | `/forge:forge The header cart badge shows '0' when the cart is empty, and big counts overflow the icon. Hide the badge at 0 and show '99+' above 99 (src/cart-badge.ts).` → `Approve.` | `results/2026-11-18-phase1-sdlc.md` Q1 |
| Q2 feature to readiness (+ Q4 unsupported tooling) | `projapp` | `/forge:forge SPEC-1` → `Approve.` | phase1-sdlc Q2, Q4 |
| Q3 failing check | `webapp-lint` | Q1 prompt → `Approve.` → (if lint blocked as pre-existing) `Add the console.log removal to this fix. Don't install anything.` | phase1-sdlc Q3 |
| Q5 approval denial | `projapp` | `/forge:forge SPEC-1` → `No, I don't approve this design. We can't take a schema migration this sprint.` | phase1-sdlc Q5 |
| Q6 interrupt + resume | `projapp` | `/forge:forge SPEC-1` → `interrupt_after.py <run> <plugin> "Approve." SPEC-1.TASK1` → fresh session `/forge:forge` | phase1-sdlc Q6 (TASK1 not redone) |
| Q7 uncertain integration | `projapp` | `/forge:forge new Notify org admins by email when a project is archived, using our email provider's API. We don't know their rate limits or whether our current plan allows transactional email.` → `1. Postmark. 2. Your default. 3. Your default. I agree: build after the spike.` → `Approve rev 1. Continue until impl-plan.` → `Approve the design. I can't check Postmark right now — put the spike in the plan as the first work item and plan the rest behind it.` | phase1-sdlc Q7 (spike item first) |
| P1 baseline PRD | Q2's finished run dir + `fixtures/inputs/projapp-journey-report.md` at `docs/reports/2026-11-10-journeys.md`, committed, fresh session | `/forge:forge prd` → `Approve rev 1.` | `results/2026-11-18-phase2.md` P1 (unreleased SPEC-1 not in PRD) |
| Q10 release → PRD | P1 run (same session) | `/forge:forge release` → `1. Yes, merged. 2. Deployed to prod on <date> by me. 3. Migration 002 applied before the code, full rollout, no flag. The app does attach a handler to projapp.events. v0.1.0 is fine.` | phase2 Q10 (`trace --strict` 0 gaps) |
| Q8 deep migration, independent review | `projapp-independent` | `/forge:forge new Project names must be unique per org. Production already has duplicate names (we don't know how many). Make it safe to roll out.` → `Approve SPEC-2 rev 1. Defaults are fine; production is SQLite.` → `Approve the design and architecture.` → `Approve the plan. No linter for now.` (budget ≥ 6: `FORGE_EVAL_BUDGET=6`) | phase2 Q8 |

Baselines for overhead: same scenario against an older version — `snapshot.sh <dir> <git-ref>`.
