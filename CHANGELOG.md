# Changelog

## 0.7.1 — 2026-11-25

From the Leadly dogfood (dependency bump): RD3 checked only the tests the spec named, so an untested consumer of the changed behaviour (a second webhook using the raw body) slipped past spec, design and review; two plan items that both rewrite the lockfile were batched in parallel.

- `rules/readiness.md` RD3: consumers first — for a change to shared behaviour, search the code for every consumer and list each with its test; a cited test must assert the claimed behaviour (read it, not just the line).
- `spec_check.py plan`: error when two items in one batch both `Modify:`/`Create:` the same file → sequence with `depends_on` (+2 tests). `stages/impl-plan.md` step 3 names the check.

## 0.7.0 — 2026-11-24

Readiness before every approval point (from the Leadly dogfood: a spec deferred work to an unowned item past a CI deadline, missed a related debt item, claimed test coverage without evidence).

- `rules/readiness.md` RD1–RD6: related records (debt, backlog, tracker), deferrals checked against the deferred item's live state and the driving deadline, coverage claims with `file:line`, no placeholders, consistency, and `stages/review.md` run on the document. Results go in the approval message.
- Spec step 6, design (fast and standard/deep "Done when"), impl-plan step 5 cite RD1–RD6 before their approval point.
- impl-plan step 5: with `forge-approvals: combined` the standard path stops after impl-plan for one approval of design + plan.

## 0.6.0 — 2026-11-18

Code-first UX: merges PR #1 (`rules/ux.md`) with the Leadly dogfood UX stage (SPEC-8–11).

- `rules/ux.md` UX1–UX5: when UX applies, prototype + real browser screenshots before spec approval, PRD/release screenshots of the real product only, implementation screenshots at test. Adds `ui: true`, prototype controls (state · role · theme · viewport + URL params), project standards (DESIGN.md, else `ux/ux-standards.md`).
- `stages/ux.md` (procedure) + `templates/ux-standards.md`; spec gets `## UX` (`templates/spec.md`): prototype link, screens `S*`, states, copy, rules `U<n>` → R. No separate UX document. Artifacts: `ux/rev-N/index.html`, `ux/rev-N/screens/*.png`.
- Contract CT2 optional `ui`, CT3 `UX` row, CT14: `spec_check.py check` with `ui: true` → `## UX` present, prototype file exists, every image path exists, every `U` cites an existing R (+9 tests).
- Spec step 4a, design step 3, review functional perspective, test 4a, prd 7a, release 5a cite `rules/ux.md`.
- Figma not required: Starter-plan limits (3 pages, 1 variable mode, MCP call cap) blocked a 4-spec set; HTML prototypes need no account.
- Migration (pre-release local layout): `_ux.md` + `ux/<slug>-mockup.html` → fold UX spec into `## UX`, move mockup to `ux/rev-N/index.html`.

## 0.5.0 — 2026-11-18

Phase 2 (plan `docs/2026-11-18-forge-phase2-plan.md`).

- `prd` stage + `templates/prd.md`: baseline PRD of released behavior for an existing product; `FEAT-n` with evidence levels (verified-prod / exercised-local / code-only / docs-only / not-exercised); report findings marked for re-verification; open questions preserved; baseline tag proposed.
- `release` stage + `templates/release.md`: verified specs → release doc (planned → released only on user-confirmed rollout) → specs `released` + `released_in` → PRD FEAT `Added by` / `Changed by`; outcome hooks; briefs on request with media/permission rules; tag proposed.
- Contract CT13 (PRD + releases), CT2 `released_in`.
- `spec_check.py prd`, `release`, `trace [--json] [--strict]` (+23 tests).
- Independent review: `forge-review: independent` on deep path → three fresh-context reviewers from `templates/reviewer-brief.md`, findings merged + attributed + re-verified.
- `scripts/changed_coverage.py` (lcov / Cobertura + `git diff`, +5 tests); QG6 points to it.
- Evals P1 (baseline PRD), Q10 (release → PRD), Q8 (deep migration, independent review): `evals/results/2026-11-18-phase2.md`.

## 0.4.0 — 2026-11-18

Adaptive SDLC + quality, Phase 1 (prompt 03; design `docs/2026-11-18-forge-adaptive-sdlc-design.md`).

- Entry: `/forge:forge SPEC-n` / `#issue` continues to the next approval point; `until <step>`, `only <step>`, `status`; approval denial logged and stops; `forge-approvals: combined` (standard path).
- `rules/quality.md` (QG1–QG8): relevant checks, evidence format, unrun checks reported, never weaken gates, missing-tool proposals with versions from project runtime + official docs, coverage policy (80% changed lines default when measurable), tests prove behavior.
- Profiles `rules/profiles/`: js-ts, java, python, database — loaded only when detected.
- `scripts/quality_detect.py` (+10 tests): project scripts / CI / tool config / defaults → checks with availability; never runs or installs.
- test stage runs the quality gate; review `code` = static · functional · architecture perspectives, finding format with evidence, fix loop (max 3 rounds) → readiness report (`templates/readiness.md`: implemented / reviewed / verified / release-ready / released).
- Ledger: `Checks:` line, Log tags `[approval]` `[intervention]` `[rework]`; contract CT2 optional `fixes: [SPEC-n]` (escaped defects).
- Evals Q1–Q7 vs 0.3.0: `evals/results/2026-11-18-phase1-sdlc.md` (same turns, +2–5% time, +1 doc).

## 0.3.0 — 2026-11-18

Spec → executable work (prompt 02; design `docs/2026-11-18-forge-spec-to-work-design.md`).

- design resolves any input to one contract spec: `SPEC-n`, path, issue, external PRD (normalized: `source: external:…`, `## Imported`, `## Open gaps`, nothing invented) or text. Minimum-sufficient sections by path; current vs proposed with `file:line`; reuse; evolution path with scaling triggers; migrations state forward + rollback + deploy order; spike only when feasibility blocks a decision.
- Work items (CT12): front matter `id SPEC-n.TASKk`, `type`, `refs`, `depends_on`, `layer`; split rules; fast path = spec `## Fix`.
- `spec_check.py gaps` (report-only) and `plan` (coverage, unknown deps, cycles, duplicates, batches, critical path, `--json` manifest).
- Ledger columns `ID · Item · Type · Depends · Status · Verified by · Issue · Updated`; tracker owns live status.
- develop entry by item / issue / batch; stale spec revision check before each item.
- Tracker publishing: `rules/trackers.md` (TR1–TR7, `forge-tracker:` preference, GitHub `gh`, GitLab `glab`, Jira/Linear via connectors), `stages/publish.md`, `scripts/tracker_sync.py` (marker-based idempotent planner + ledger writer). Preview + approval before every external write; never close/delete.
- Tests: `tests/spec_check` 44, `tests/tracker_sync` 13, run by `scripts/check.sh`. Evals E1–E3: `evals/results/2026-11-18-sliceA.md`.

## 0.2.1 — 2026-11-18

- discover ends with one ask (agree / override verdict); assumptions shown as `Assumed:` statements, not questions (eval F1: D3 questions 3 → 1).
- Path `deep` = hard to undo / wide blast radius; demand uncertainty stays `standard` via discover "test first"; new idea with small reversible MVP = `standard` (eval F4).

## 0.2.0 — 2026-11-18

Product stages inside forge (design: `docs/2026-11-18-forge-product-design.md`, Slice 1).

- New stages `discover` (build / test first / don't build, evidence labelled) and `spec` (one validated product doc per task).
- `rules/contract.md` (CT1–CT11) + `scripts/spec_check.py` validator (python3 stdlib) + 28 tests in `tests/spec_check/`, run by `scripts/check.sh`.
- Router owns the process: works out the next step from docs, prints `task · path · done → next`, runs it; stops only at approvals, decision-changing ambiguity, irreversible actions.
- Questions only when they change the decision, batched with defaults (was: one per message, every row).
- Docs root defaults to `docs/forge/` without asking.
- design stage links an approved spec (`Spec: SPEC-n @ rev N`) instead of restating Problem → Use cases; develop/test move spec status to implemented/verified; review type `spec`.
- **Breaking:** sizes Fix/Change/Build → paths fast/standard/deep (old names accepted as aliases). `tasks/index.md` template columns `Path`, `Step`, `Started`, `First slice`, `Released`.
- **Breaking (governance):** G1 approvals scaled by path (approved 2026-11-18) instead of before every stage; irreversible/external actions still always need approval.
- `evals/`: scenarios D1 (idea → MVP), D3 (don't build) + baseline/slice-1 results.

## 0.1.2 — 2026-11-15

- `rules/diagrams.md` (DG1–DG7): diagram type per question, required set per size, `**Read:**` plain-language caption, new/changed markers, diagram ↔ text consistency.
- design stage: current-state flow (Problem), actor flow (≥ 3 actors). architect stage: component, sequence per main UC, ER, state, before/after.
- `templates/design.md`: diagram + caption slots. review design/arch checks diagrams. DS7 → points to `rules/diagrams.md`.

## 0.1.1 — 2026-11-15

- Docs-root prompt: one question; offer `forge-docs:` line only when a non-default path is chosen (dogfood: Leadly asked two questions + offered a CLAUDE.md for the default).
- README: command is `/forge:forge` (plugin skill namespace).

## 0.1.0 — unreleased

- Repo scaffold: marketplace + `forge` plugin manifests, README, maintainer CLAUDE.md, `scripts/check.sh` (incl. `claude plugin validate`).
- `SKILL.md` router: docs-root resolution, routing, sizing (Fix/Change/Build), task numbering, resume.
- `rules/`: guardrails G1–G9, doc style, API standards (REST, errors, payments example), code, test, security checklist.
- `stages/`: onboard, ai-readiness, design, architect, impl-plan, develop, test, review.
- `templates/`: design, impl-task, ledger, review, understanding, health, tasks-index.
- `domains/`: CRM, voice/message agents, ecommerce.
- Pending before release: dogfood on Leadly (plan Tasks 5–7, 9).
