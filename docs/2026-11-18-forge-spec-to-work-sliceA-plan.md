# forge spec → work — Slice A plan

Status: impl-plan · ✅ executed 2026-11-18 · results `evals/results/2026-11-18-sliceA.md` · Slice B built (planner, rules, stage, tests); real publish demo pending user login + scratch repos
Design: `docs/2026-11-18-forge-spec-to-work-design.md` (approved 2026-11-18) · Target: forge 0.3.0
Slice A = entry resolution + normalization, minimum-sufficient design sections, work items + ledger columns, `spec_check.py plan` + `gaps`, develop entry by item/batch. No tracker writes (Slice B).

S/ = `plugins/forge/skills/forge/`. Rules: one step = one verifiable deliverable; tick only with Verify output (G5); `bash scripts/check.sh` PASS after every step; agent never commits (G2).

| # | Step | Verify | Result |
|---|---|---|---|
| 01 | Tests first: `plan` + `gaps` fixtures (red) | new tests fail, existing 28 pass | ✅ 15 red |
| 02 | `spec_check.py gaps` + `source` field | gaps tests green | ✅ |
| 03 | `spec_check.py plan` (+ `--json`) | plan tests green | ✅ |
| 04 | Contract + templates: `source` (CT2), work-item front matter, ledger columns, design template sections | template-derived fixture passes `plan`; check.sh PASS | ✅ |
| 05 | Stages: design (resolve + normalize + sections + spike), impl-plan (items, split rules, run `plan`), develop (item / issue / batch entry, `--rev` re-check), SKILL route | SKILL < 150; check.sh PASS | ✅ SKILL 94 lines |
| 06 | Compatibility test: 01 spec template → check → plan | test green | ✅ 44 tests |
| 07 | Demos E1–E3 headless + README, CHANGELOG 0.3.0 | criteria below met; results recorded | ✅ E1, E2 (after fix A1), E3 |

### 01 — Tests first (`tests/spec_check/test_plan.py`, `test_gaps.py`)

Plan fixtures (task dir with spec + `impl-tasks/NN_*.md` + ledger):

| Fixture | Expect |
|---|---|
| fast: 1 item covering all R/AC | exit 0, 1 batch |
| standard: 4 items, diamond deps (db → api, telemetry → frontend) | exit 0, critical path TASK1→TASK2→TASK4, batches [1],[2,3],[4] |
| uncovered AC | exit 1, names AC |
| unknown dep / cycle | exit 1, prints cycle |
| duplicate items (same refs + files) | exit 1 |
| bad item id / id ≠ file NN / bad type / bad layer | exit 1 |
| `--json` | valid JSON: items, deps, batches, critical path, spec rev |

Gaps fixtures: external doc with no AC / vague R ("fast", "user-friendly") / no non-goals → exit 0, lists gaps; never writes the file.

### 02 — `gaps` + `source`

`spec_check.py gaps <doc>`: missing required sections (per `path`, default standard), R without AC, vague-word requirements (`fast`, `easy`, `user-friendly`, `scalable`, `robust`, `intuitive` without a number), missing success/failure criteria. Report only, exit 0. `source` optional front-matter (`native` default | `external:<path>@<rev>`).

### 03 — `plan`

`spec_check.py plan <task dir> [--json]`: reads spec R/AC + item front matter (`id`, `type` story|enabler|spike|bug|task, `refs`, `depends_on`, `layer` db|backend|frontend|integration|telemetry|test|mixed); checks coverage, ids, deps, cycles, duplicates; prints batches (topological levels) + critical path (longest dependency chain by item count); `--json` manifest incl. spec id/rev, design rev if present.

### 04 — Contract + templates

- `rules/contract.md`: CT2 optional `source`; CT1 adds item front matter fields + types; CT12 plan rules (coverage, no cycles, split only when independently verifiable).
- `templates/impl-task.md`: front matter + Outcome, Scope / Non-scope, Acceptance criteria, Blockers.
- `templates/ledger.md`: `| ID | Item | Type | Depends | Status | Verified by | Issue | Updated |`.
- `templates/design.md`: header pin; sections Current vs proposed, Affected components + reuse, Evolution path (now/later, scaling triggers, capacity/cost).

### 05 — Stages + router

- `stages/design.md` §Resolve: SPEC id / path / issue / external doc / text per design §3; normalization → new task, spec `status: proposed`, `gaps` output in `## Open gaps` → spec approval point. Section table per design §4. Spike rule.
- `stages/architect.md`: Evolution path required on deep.
- `stages/impl-plan.md`: item rules (design §5), run `plan`, show batches + critical path; approval only on deep.
- `stages/develop.md`: entry `develop SPEC-n.TASKk | #issue | batch`; before each item `check --rev N` (stale → stop); batch = items whose deps are ✅.
- `SKILL.md` §3: route `design <SPEC-n|path|#issue|text>`, `develop <item|#issue|batch>`.

### 06 — Compatibility

Test: fill `templates/spec.md` (01) + two items from `templates/impl-task.md` → `check --require-approved` → `plan` exit 0.

### 07 — Demos (headless, fresh session, `--plugin-dir` 0.3.0 snapshot)

| # | Case | Pass when |
|---|---|---|
| E1 | Small change on fixture repo (fast) | one item = spec `## Fix` with `file:line` + before/after + failing test; no design doc, no impl-plan |
| E2 | Approved standard spec with a DB change (fixture repo) | design has current vs proposed with `file:line`, migration + rollback, evolution path; items split db/backend/frontend only where verifiable; plan check: full coverage, batches, critical path |
| E3 | Ambiguous external PRD | normalized spec `proposed` with `## Open gaps`; no invented R/AC; stops at spec approval |

Record questions, docs, turns, secs in `evals/results/2026-11-18-sliceA.md`. README + CHANGELOG 0.3.0 + plugin.json.
