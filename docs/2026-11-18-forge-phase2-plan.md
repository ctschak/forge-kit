# forge Phase 2 plan — PRD, release, independent review, changed-code coverage

Status: impl-plan · ✅ executed 2026-11-18 · results `evals/results/2026-11-18-phase2.md`
Designs: `docs/2026-11-18-forge-product-design.md` (v3 §5, §6: `prd`, `release`, `check --prd`, `trace`) · `docs/2026-11-18-forge-adaptive-sdlc-design.md` (§6, §9 Phase 2). Target: forge 0.5.0.
Order (agreed 2026-11-18): prd → release → independent review → changed-code coverage. Unblocks Leadly prompt 04.

S/ = `plugins/forge/skills/forge/`. Rules: one verifiable deliverable per step; tick only with Verify output (G5); `bash scripts/check.sh` PASS after every step; agent never commits (G2).

## Where things live (product repo, forge docs root)

```
<root>/PRD.md                 ← living master: released behavior only, FEAT-n sections
<root>/releases/vX.Y.Z.md     ← one per release: specs shipped, evidence, rollout, outcome hooks
<root>/tasks/NN_*/…           ← unchanged (spec, design, ledger, reviews, readiness)
```

| # | Step | Verify | Result |
|---|---|---|---|
| 01 | Tests first: `spec_check.py prd`, `release`, `trace` (red) | new tests fail; existing 69 pass | ✅ 21 red |
| 02 | Implement `prd`, `release`, `trace` | tests green | ✅ 67 green |
| 03 | `S/templates/prd.md`, `S/templates/release.md`; contract CT13 (PRD + release rules), CT6 release row | template-filled fixtures pass `prd` / `release` | ✅ +2 template tests (69) |
| 04 | `S/stages/prd.md` (baseline + update) | check.sh PASS | ✅ |
| 05 | `S/stages/release.md` (+ briefs on request, media rules) | check.sh PASS | ✅ |
| 06 | Independent review: `S/templates/reviewer-brief.md`, review stage deep path wiring | check.sh PASS | ✅ |
| 07 | Tests first + `S/scripts/changed_coverage.py` (lcov + Cobertura + `git diff`) | coverage tests green | ✅ 5 red → green |
| 08 | Router + layout: route `prd`, `release`; docs layout; QG6 points to script; SKILL < 150 | check.sh PASS | ✅ SKILL 104 lines |
| 09 | Demos P1, Q10, Q8 | criteria below; results recorded | ✅ P1, Q10, Q8 |
| 10 | README, CHANGELOG 0.5.0, plugin.json, CLAUDE.md | check.sh PASS | ✅ |

### 01–02 — validator commands

`spec_check.py prd <PRD.md>`
- front matter: `contract: 1`, `type: prd`, `revision`, `status` (proposed / approved), `source_rev`, optional `baseline: <tag>`.
- `## FEAT-n <name>` sections: IDs unique, plain numbers; each has `Evidence:` line with level `verified-prod` · `exercised-local` · `code-only` · `docs-only` · `not-exercised`; baseline requirements `FEAT-n.R<k>` unique.
- `Changed by:` / `Added by:` lines cite only specs whose status is `released` (resolved from `<root>/tasks/*/_spec.md`) → planned or verified-but-unreleased work in the PRD = error (CT13).
- `## Open decisions` allowed (Q / DEC items); no future tense requirement wording check (out of scope).

`spec_check.py release <releases/vX.Y.Z.md>`
- front matter `type: release`, `version` (semver), `status` (planned / released), `date`.
- `## Specs` lists `SPEC-n @ rev N`; each spec exists, rev matches, status `verified` (planned) or `released` (released); readiness report exists for each.
- released → every listed spec status `released` + `released_in: vX.Y.Z`; PRD has a `FEAT` citing it.

`spec_check.py trace <root> [--json]`
- per spec: R → AC → work items (refs) → ledger `Verified by` → release → PRD FEAT; prints gaps (R without item, AC without evidence, verified spec in no release, released spec missing in PRD). Exit 0 always (report), `--strict` → exit 1 on gaps.

Fixtures cover: valid baseline PRD, missing evidence level, duplicate FEAT, PRD citing a `verified` (unreleased) spec, release with rev mismatch, release missing readiness, trace gaps.

### 03 — templates + contract
- `templates/prd.md`: front matter; Product (one paragraph), Users + roles, Journeys (diagram per `rules/diagrams.md` if useful), `## FEAT-n` sections (behavior, rules, permissions, evidence level, source `file:line`), KPI + telemetry inventory (what exists today), Known gaps + risks, Open decisions, Changes (dated, rev).
- `templates/release.md`: front matter; Specs; Readiness summary (link per spec); Rollout + rollback; Customer-facing notes; Outcome hooks (KPI, baseline, check date → Phase 3 `outcome`); Briefs (links); Assets table (name, version, location, approval, checksum).
- CT13: PRD = released behavior only; update only at release; FEAT IDs never reused; baseline tag proposed, user runs (G2).

### 04 — `stages/prd.md`
- **Baseline** (existing product, no PRD): read `understanding.md` (run onboard first if missing and code exists), docs, code, supplied evidence (reports, screenshots); every capability → FEAT with evidence level; never "used / working" without evidence; findings from reports = `observed — needs current verification`; open questions preserved as Q items; plan/pricing contradictions listed, not resolved by guess. Status `proposed` → **approval point** → `approved` + propose `git tag product-baseline-YYYY-MM-DD` (user runs).
- **Update** only via `release` stage.
- Validator `prd` clean before approval.

### 05 — `stages/release.md`
- Input: verified specs + readiness reports. Never claims deployed/merged without evidence; asks for the rollout facts.
- Steps: pick specs → `release` check (planned) → user confirms rollout done (authority, evidence) → specs `released` + `released_in` → PRD FEAT sections added/changed (`Added by` / `Changed by`), revision+1 → `prd` + `release` + `trace` checks → propose tag `product-vX.Y.Z` (user runs).
- Briefs on request (positioning, onboarding, landing page, marketing / video scripts): Markdown under `<root>/releases/vX.Y.Z/briefs/`, built from PRD + spec facts only; rendered media only to user-designated storage, permissions untouched, asset table; no rendering claim without a tool.

### 06 — independent review
- `templates/reviewer-brief.md`: what a fresh reviewer gets — perspective, diff command, spec + design + ledger paths, rules files, finding format; explicitly **not** the author's conclusions.
- `stages/review.md`: deep path + `forge-review: independent` → three subagents (static, functional, architecture) via the brief; merge findings (dedupe same file:line + same issue), then normal verdict + fix loop. Without the setting: three passes inline.

### 07 — `changed_coverage.py`
`changed_coverage.py --report <lcov.info | coverage.xml> [--base <ref>] [--repo <dir>] [--json]` → changed executable lines covered / total / %, per file, uncovered line list. Tests: lcov fixture, Cobertura fixture, no changed lines, file not in report (= uncovered), new file. Parses `git diff -U0 <base>` in a temp git repo fixture.

### 09 — demos

| # | Case | Pass when |
|---|---|---|
| P1 | Baseline PRD for an existing product (projapp + a supplied journey report with demo-only evidence) | FEATs with evidence levels; report findings marked needing verification; no future features as present; `prd` clean; stops at approval; tag proposed, not run |
| Q10 | Product spec → release-ready → release (projapp SPEC-1 from approved baseline) | release doc; SPEC-1 `released`; PRD FEAT added with `Added by: SPEC-1`; `trace` no gaps; tag proposed |
| Q8 | High-risk migration, deep path (projapp: names unique per org, existing duplicates) with `forge-review: independent` | expand/contract + dedupe backfill + rollback; destructive step gated on approval; 3 independent reviewer contexts; findings merged; readiness |

Results → `evals/results/2026-11-18-phase2.md` (turns, secs, docs, subagents used).
