# forge product stages — Slice 1 plan

Status: impl-plan · ✅ executed 2026-11-18 (approved 2026-11-18) · results `evals/results/2026-11-18-slice1.md` · 1 open finding (F1)
Design: `docs/2026-11-18-forge-product-design.md` (v3, approved 2026-11-18) · Target version: forge 0.2.0
Slice 1 = contract, validator, spec template, `discover` + `spec` stages, router paths + next-step, G1 scaling, design-stage spec link, review `spec`. Demos D1 + D3.

Skill dir below = `plugins/forge/skills/forge/` (S/).

## Rules for this plan

- One step = one reviewable deliverable with its own Verify. Steps run in order; tick `[x]` only with Verify output recorded (G5).
- `bash scripts/check.sh` must PASS after every step from 03 on.
- Agent never commits (G2). Hand back diff summary after each step.
- SKILL.md < 150 lines throughout.

## Steps

| # | Step | Verify | Result |
|---|---|---|---|
| 00 | Baseline demo runs (current forge) | D1 + D3 baseline numbers recorded | ✅ |
| 01 | Validator tests first (red) | tests fail: module missing | ✅ 26 tests red |
| 02 | Validator `check` (green) | all tests pass | ✅ green |
| 03 | `rules/contract.md` | check.sh refs resolve; sections match validator | ✅ |
| 04 | `templates/spec.md` | template passes validator as fixture after fill | ✅ |
| 05 | G1 scaled + paths + router next-step | SKILL.md < 150; check.sh PASS | ✅ 91 lines |
| 06 | `stages/discover.md` | check.sh PASS; read-through vs design §6 | ✅ |
| 07 | `stages/spec.md` | check.sh PASS; read-through vs design §5.2 | ✅ |
| 08 | design stage spec link + review type `spec` | check.sh PASS | ✅ |
| 09 | Index template, README, check.sh, version, CHANGELOG | check.sh PASS incl. tests | ✅ PASS |
| 10 | Demos D1 + D3 (new forge) + compare | pass criteria design §8 met; results recorded | ⚠️ D1+D3 criteria met; D3 Q 3 vs 2 (F1) |

### 00 — Baseline (before any skill change)

- [x] Write scenarios: `evals/scenarios/D1-idea-to-mvp.md` (solo founder, tutoring booking, fictional), `evals/scenarios/D3-dont-build.md` (feature request contradicted by supplied evidence). Each: context, user turns, pass criteria (design §8), anti-behaviours.
- [x] User runs each in fresh session with currently installed forge (`/forge:forge new …`) in a scratch repo outside forge-kit.
- [x] Record per run in `evals/results/2026-11-18-baseline.md`: questions asked, docs created, human interventions, elapsed minutes, notes.
- Verify: results file has 2 rows with all 4 numbers (observed, not estimated).

### 01 — Validator tests first

Files: `tests/spec_check/test_spec_check.py` (unittest), `tests/spec_check/fixtures/`:

| Fixture | Expect |
|---|---|
| `valid_fast.md`, `valid_standard.md` | exit 0 |
| `legacy_no_contract.md` | exit 0 + notice "legacy, skipped" |
| `missing_front_matter_field.md` (no `revision`) | exit 1, names field |
| `bad_id.md` (`SPEC-07`, `spec-7`) | exit 1 |
| `id_folder_mismatch/07_x/…_spec.md` with `SPEC-8` | exit 1 |
| `bad_status.md` (`in_progress`) | exit 1 |
| `missing_section_standard.md` (no KPIs) | exit 1, names section |
| `ac_without_r.md`, `r_without_ac.md` | exit 1, names IDs |
| `empty_section.md` (heading, no text) | exit 1; `n/a — reason` accepted |
| `approved_no_approval.md` | exit 1 |

- Verify: `python3 -m unittest discover tests/spec_check` → errors (module not found). Paste output.

### 02 — Validator `check`

File: `S/scripts/spec_check.py` — python3 stdlib only.

```text
python3 spec_check.py check <spec.md> [--path fast|standard|deep]
exit 0 ok · 1 errors · 2 warnings only
```
- Front matter: flat `key: value`, lists `[a, b]`; required `contract, id, revision, status, source_rev`.
- Path: `--path` or task row in `tasks/index.md` next to the spec's task folder; default `standard`.
- Required sections per path = design §5.2 table (headings matched case-insensitively).
- `R<n>` / `AC<n>` parsed from tables or bullets; each AC cites ≥1 existing R; each R has ≥1 AC.
- `approved` and later: `## Approvals` line present (`YYYY-MM-DD <name> rev <n>`).
- Output: one line per problem `ERROR <section|field>: <what> → <fix>`.
- Verify: `python3 -m unittest discover tests/spec_check -v` → all pass. Paste summary.

### 03 — `S/rules/contract.md`

IDs (§5.1), front matter (§5.2), sections by path, statuses + who moves them (§5.3), change/clarification rules, compatibility (`contract: 1`, legacy skip), ownership (§5.5), validator commands. IDs `CT1…` for citation. Cites `rules/doc-style.md`, not restating.
- Verify: `bash scripts/check.sh` PASS; section list in contract == validator's table (manual diff, note result).

### 04 — `S/templates/spec.md`

Front matter block + every section of §5.2 with 1-line `<!-- fill -->` hint and path marker (`fast+`, `standard+`, `deep`). Includes `## Approvals`, `## Clarifications`, `## Changes`.
- Verify: fill template minimally into `tests/spec_check/fixtures/from_template.md` → validator exit 0 (add to tests).

### 05 — G1 scaled, paths, router

- `S/rules/guardrails.md` G1 → "Approval at path approval points (SKILL.md §4) and before any irreversible/external action; never write code before the spec (fast: scope) is approved." Red-flag line kept.
- `S/SKILL.md`:
  - §4 sizes → paths fast/standard/deep table (design §3) + alias line `Fix=fast, Change=standard, Build=deep`.
  - §3 / §5 → next-step rule (design §4): read docs → one-line status → run next step → stop only at approval / consequential ambiguity / irreversible / missing authority.
  - §6.1 → questions rule: ask only decision-changing questions, batch them, else `(assumption)` and continue.
  - Route `discover`, `spec`; `new <desc>` starts at discover (standard/deep) or spec (fast).
  - Task folder: spec file `YYYY-MM-DD_<slug>_spec.md`; `SPEC-<n>` = folder number.
- Verify: `wc -l S/SKILL.md` < 150; `bash scripts/check.sh` PASS.

### 06 — `S/stages/discover.md`

Inputs: idea / product / feedback / brief; code + `understanding.md` if present. Steps: classify evidence (verified · assumption · proposed); research only when it changes the decision (dated sources, hypotheses labelled, no invented sizes); cheap experiment before build. Output = spec sections Objective, Persona · job · value, Evidence & assumptions, recommendation `build | test first | don't build` (→ `dropped`). Done when recommendation stated + user agrees or overrides.
- Verify: check.sh PASS; every design §6 discover item present (checklist in step notes).

### 07 — `S/stages/spec.md`

Write/complete spec per path (`rules/contract.md`); now/next/later; MVP slice (aim 2–3 days) + ≤ 2-week path or stated constraint; numbers with units + assumption + how measured; run validator; fix list → user; approval → status `approved`, `## Approvals` line, index updated → next step starts automatically (design or develop for fast).
- Verify: check.sh PASS; read-through vs design §5.2 + §5.6.

### 08 — Design link + review `spec`

- `S/stages/design.md`: "Spec exists → run validator; errors → back to spec stage; write `Spec: SPEC-n @ rev N` + cite `SPEC-n.R*`; skip Problem → Use cases." Fast path unchanged otherwise.
- `S/stages/review.md` + `S/templates/review.md`: type `spec` — evidence dated/real, MVP smallest, AC + KPIs measurable, non-goals explicit, no invented numbers, validator clean.
- Verify: check.sh PASS.

### 09 — Wiring + release prep

- `S/templates/tasks-index.md`: `Size` → `Path`; add `Started`, `First slice`, `Released`.
- `scripts/check.sh`: expected files += `rules/contract.md`, `stages/discover.md`, `stages/spec.md`, `templates/spec.md`, `scripts/spec_check.py`; run `python3 -m unittest discover tests/spec_check`.
- `README.md`: paths, product stages, contract one-liner. `plugin.json` → 0.2.0; `CHANGELOG.md` 0.2.0 entry incl. breaking notes (paths aliases, G1).
- Verify: `bash scripts/check.sh` → PASS (paste).

### 10 — Demos with new forge

- Ran headless with `--plugin-dir` snapshot of 0.2.0, same setup as 00.
- Record `evals/results/2026-11-18-slice1.md` same 4 numbers + pass/fail per criterion; compare with baseline.
- Verify: D1 + D3 pass criteria met; questions + docs ≤ baseline. Fail → fix one root cause per edit, re-run (G8).

## Not in Slice 1

`prd`, `release`, `outcome` stages, `trace`, `--prd`, `--json`, D2 fixture repo → Slice 2/3.

## Execution notes (2026-11-18)

- Validator: exit codes simplified to 0/1 (legacy = 0 + notice); flags `--require-approved`, `--rev N` added for handoff/stale checks; front matter gains required `path` (CT2). Tests: 28.
- Extra small edits needed for consistency: develop/test stages (fast path from spec `## Fix`, spec status implemented/verified, test-plan approval only on deep), architect/design template/onboard wording, marketplace description, `CLAUDE.md` pointers. Docs-root question removed (default `docs/forge/`).
- Step 10 fix attempt for F1: `stages/discover.md` step 5 (better-problem offer = statement). Question count unchanged; left open.
