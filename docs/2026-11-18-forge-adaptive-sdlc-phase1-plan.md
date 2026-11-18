# forge adaptive SDLC — Phase 1 plan

Status: impl-plan · ✅ executed 2026-11-18 · results `evals/results/2026-11-18-phase1-sdlc.md` · D2 (eslint/tsc in fixture) not met: npm registry unreachable
Design: `docs/2026-11-18-forge-adaptive-sdlc-design.md` (approved 2026-11-18) · Target: forge 0.4.0
Phase 1 = entry overrides, quality rules + profiles, tool detection, quality gate, 3-perspective review + remediation, readiness report, metrics. Demos Q1–Q7.

S/ = `plugins/forge/skills/forge/`. Rules: one verifiable deliverable per step; tick only with Verify output (G5); `bash scripts/check.sh` PASS after every step; agent never commits (G2).

| # | Step | Verify | Result |
|---|---|---|---|
| 01 | Tests first: `quality_detect` fixtures (red) | new tests fail; existing 57 pass | ✅ 10 red |
| 02 | `S/scripts/quality_detect.py` | detect tests green | ✅ 10 green |
| 03 | `S/rules/quality.md` (QG1…) + `S/rules/profiles/{js-ts,java,python,database}.md` | check.sh refs resolve | ✅ |
| 04 | Quality gate in `S/stages/test.md`; ledger template: `Checks:` header, Log tags | check.sh PASS | ✅ |
| 05 | `S/stages/review.md` 3 perspectives + finding format + remediation loop; `S/templates/review.md` | check.sh PASS | ✅ |
| 06 | `S/templates/readiness.md`; `fixes:` optional field (CT2) + validator test | tests green | ✅ +2 tests (46) |
| 07 | `S/SKILL.md`: `SPEC/#issue` entry, `until` / `only` / `status`, `forge-approvals: combined`; SKILL < 150 | check.sh PASS | ✅ SKILL 100 lines |
| 08 | Fixtures: `webapp` (TS UI, eslint + tsc installed in fixture), `projapp` (no tools), planted lint failure, external-API spike case | fixture checks run as expected | ⚠️ eslint/tsc not installable (network); project lint script used |
| 09 | Demos Q1–Q7 on 0.4.0 + Q1/Q2 on 0.3.0 for overhead | criteria met; results recorded | ✅ Q1–Q7 (Q4 via Q2); overhead +2–5% secs, +1 doc |
| 10 | README, CHANGELOG 0.4.0, plugin.json, CLAUDE.md pointers | check.sh PASS | ✅ |

### 01–02 — `quality_detect.py <repo> [--json]`

| Fixture | Expect |
|---|---|
| TS: `package.json` scripts `lint`, `typecheck`, `test`; `eslint.config.js`; `tsconfig.json` | profiles [js-ts]; checks `npm run lint` / `npm run typecheck` / `npm test` source `script` |
| TS without scripts but with `tsconfig.json` | `npx tsc --noEmit` source `default`, available per `node_modules/.bin/tsc` |
| Python: `pyproject.toml` `[tool.ruff]`, `[tool.pytest.ini_options]` | profiles [python]; `ruff check .`, `pytest` source `config`; available = on PATH |
| Python bare (`*.py`, unittest tests) | profiles [python]; `python3 -m unittest discover tests` source `default` available yes; ruff/mypy `available: no` + `suggest` |
| Java Maven `pom.xml` with checkstyle plugin | profiles [java]; `mvn -q verify` source `config` |
| `db/migrations/*.sql` | profile database added |
| CI `.github/workflows/*.yml` / `.gitlab-ci.yml` with `run:` / `script:` commands | checks with source `ci` |
| empty repo | no profiles, no checks, exit 0 |

Output: `{languages, profiles, checks: [{name, kind lint|type|format|test|security|build, command, source script|ci|config|default, available yes|no|unknown, suggest?}]}`. Never runs the checks itself.

### 03 — rules
- `quality.md`: QG1 run relevant checks only (changed languages; deep/shared modules → broader regression) · QG2 evidence `command → exit, counts` in ledger · QG3 unrun = `not run: <reason>`, never omitted · QG4 never weaken/disable existing gates; no legacy cleanup (G8) · QG5 tooling absent → propose minimal config, versions chosen from project runtime + official docs at that time, install only with approval · QG6 coverage: project policy, else 80% changed lines when measurable, else `not measured` · QG7 tests prove behavior (AC), not coverage.
- Profiles: per design §4, each ≤ 40 lines: tools (prefer existing), checks, language risks to review, DB: migration rules (forward, rollback, order, destructive = G6 approval).

### 04 — quality gate (`test.md`)
Detect → run relevant checks + affected tests → evidence per check in ledger → failures become findings for review/fix loop. Ledger template: `Checks:` line (detected list) and Log tags `[approval]` `[intervention]` `[rework]`.

### 05 — review
Types unchanged; `code` review runs perspectives static · functional · architecture (fast/standard: one pass, three sections; deep: three passes). Finding row per design §6. Remediation: blockers → fix → rerun affected → append re-review; max 3 rounds (`forge-fix-rounds:`), then `⛔ blocked`. Scope/design change → stop, reopen approval.

### 06 — readiness + `fixes:`
`templates/readiness.md`: states table (implemented / reviewed / verified / release-ready), per-AC evidence, checks run / not run, coverage, open findings, risks, rollout + rollback, metrics (elapsed, approvals, interventions, rework), next action. Written by review on approve → `tasks/NN_<slug>/YYYY-MM-DD_readiness.md`. CT2 optional `fixes: [SPEC-n]` (escaped defect link).

### 07 — router
`/forge:forge SPEC-n` / `#issue` → resolve task → §5 next step. `until <step>` stop after; `only <step>` single step; `status` one line per open task with readiness state. `forge-approvals: combined` → standard path: spec already approved by product + design approval asked together with plan summary (one approval).

### 08 — fixtures (scratchpad, not committed)
- `webapp`: tiny TS (no framework) page module + unit tests via `node --test`; `npm i -D typescript eslint @eslint/js typescript-eslint` inside fixture (versions = whatever npm resolves today, recorded); scripts lint/typecheck/test.
- planted lint error variant (Q3); approved fast spec for a UI text/state bug (Q1).
- `projapp` reused (Q2 feature, Q4 tool-less, Q5 denial, Q6 interrupt).
- Q7: spec "send archive notifications via an email provider (unknown API limits)".

### 09 — demos (headless, fresh sessions, simulated user)

| # | Pass when |
|---|---|
| Q1 fast UI fix (webapp) | fast path; eslint/tsc/test run with evidence; combined 3-perspective review; readiness report |
| Q2 feature (projapp SPEC-1) | design → plan → develop → test gate → review → readiness; states distinguished; unrun tools reported |
| Q3 failing check (webapp planted lint) | finding → fix → rerun green ≤ 3 rounds; evidence |
| Q4 unsupported tooling (projapp) | ruff/pytest/mypy `not run: tool missing` + proposal; nothing installed |
| Q5 approval denial (projapp design) | denial logged `[approval]`; nothing built; alternatives offered |
| Q6 interrupt + resume (projapp) | stop after item 1 → fresh session continues at item 2; item 1 not redone |
| Q7 uncertain integration | spike item (question, time box, decision) before dependent items |

Overhead: Q1 + Q2 also on 0.3.0 snapshot → turns, questions, secs, docs. Results → `evals/results/2026-11-18-phase1-sdlc.md`.
