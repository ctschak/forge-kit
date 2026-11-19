# Product ↔ engineering contract (`contract: 1`)

One small contract between product stages (discover, spec) and engineering stages (design onward). Validated by `scripts/spec_check.py`. Style per `rules/doc-style.md`.

| ID | Rule |
|---|---|
| CT1 | **IDs.** Spec = initiative = task: `SPEC-<n>`, n = task folder number (`07_<slug>` → `SPEC-7`). Inside: `SPEC-7.R3` requirement · `SPEC-7.AC2` acceptance criterion · `SPEC-7.TASK2` work item (= impl step 02). Released features in `PRD.md`: `FEAT-<n>`. Plain numbers, never reused. |
| CT2 | **Front matter** (required): `contract: 1` · `id` · `revision` (integer, +1 per approved-scope change) · `status` · `path` (fast / standard / deep) · `source_rev` (git commit the spec was written against). Optional: `depends_on: [SPEC-3]` · `changes: [FEAT-4]` · `source: native | external:<path>@<rev>` (normalized external doc) · `fixes: [SPEC-n]` (this spec fixes a defect in a released spec — escaped-defect metric) · `released_in: vX.Y.Z` (set by release stage). Unknown fields ignored. |
| CT3 | **Sections by path** (exact `##` headings; nothing to say → `n/a — <why>`, never empty). Table below. |
| CT4 | **R ↔ AC.** Requirements numbered `R1…`; criteria `AC1…`, each cites ≥ 1 existing R; every R has ≥ 1 AC. AC measurable: number + unit, or observable yes/no. |
| CT5 | **Numbers.** Unit + assumption + how measured. Unknown → `(assumption)` or `not measured`. Never invented market sizes, rates or results. |
| CT6 | **Status** `proposed → approved → implemented → verified → released`, or `dropped` (don't build). Who moves it: table below. |
| CT7 | **Approval** = line in `## Approvals`: `YYYY-MM-DD <name> rev <n>`. Must match current `revision` while status ≥ approved. |
| CT8 | **Scope change after approval** → `revision`+1, status `proposed`, dated line in `## Changes`, re-approve. Clarification without scope change → dated line in `## Clarifications`. |
| CT9 | **Link, don't copy.** Spec cites `FEAT-*`, research files, other specs. Design cites `SPEC-n.R*` / `AC*` and pins `Spec: SPEC-n @ rev N`. PRD cites specs on release. |
| CT10 | **Ownership.** Product: intent, spec, AC, KPIs, released behavior (`PRD.md`), release decision. Engineering: design decisions, plan, code, test evidence. Tracker (when used): live issue status. |
| CT11 | **Compatibility.** No `contract:` field = legacy doc → validator skips with notice. Newer optional fields ignored. Breaking change → `contract: 2` + migration note in CHANGELOG. |
| CT12 | **Work items** (`impl-tasks/NN_<slug>.md`, `templates/impl-task.md`). Front matter: `id: SPEC-n.TASK<NN>` · `type` story / enabler / spike / bug / task · `refs: [R2, AC3, "design §…"]` · `depends_on: [SPEC-n.TASK1]` · `layer` db / backend / frontend / integration / telemetry / test / mixed. One measurable outcome per item; tests inside its Done when. Split by layer only when each part is independently verifiable and leaves the system working; otherwise one item, reason stated. Fast path = one item: the spec's `## Fix` (no impl-plan); write `impl-tasks/01_<slug>.md` only when publishing to a tracker. `plan` check: every R and AC covered, deps known, no cycles, no duplicates. |
| CT13 | **PRD + releases.** `PRD.md` (`templates/prd.md`) = released behavior only: `## FEAT-n` sections, each with `Evidence:` level verified-prod / exercised-local / code-only / docs-only / not-exercised, baseline requirements `FEAT-n.R<k>`; may cite only `released` specs (`Added by` / `Changed by`). Updated only by the release stage (revision +1). `releases/vX.Y.Z.md` (`templates/release.md`) lists `SPEC-n @ rev N`; `planned` needs verified specs + readiness reports; `released` needs user-confirmed rollout, specs `released` + `released_in`, PRD citing them. Baseline / release tags proposed, user runs (G2). |

**Optional UX artifacts (CT14).** For relevant UI specs, follow `rules/ux.md`: optional `## UX` contains revision-specific HTML prototype links and embedded screenshots with R/AC references. Prototype evidence is never released behavior. PRD FEAT screenshots must represent the actual existing/released product and carry evidence context. This is an additive convention, not a breaking contract/schema change; no artifacts are required for non-UI tasks.

## CT3 — sections

| `##` heading | fast | standard | deep |
|---|---|---|---|
| Objective (incl. success + failure criteria) | ✓ | ✓ | ✓ |
| Scope | ✓ | ✓ | ✓ |
| Non-goals | ✓ | ✓ | ✓ |
| Requirements | ✓ | ✓ | ✓ |
| Acceptance criteria | ✓ | ✓ | ✓ |
| Users and value (persona, job, value) | | ✓ | ✓ |
| Journeys and rules (user journeys, business rules) | | ✓ | ✓ |
| Constraints | if any | ✓ | ✓ |
| Dependencies | if any | ✓ | ✓ |
| KPIs (baseline, target, how measured) | | ✓ | ✓ |
| Telemetry (events needed) | | ✓ | ✓ |
| Priorities (now / next / later, MVP slice) | | ✓ | ✓ |
| Evidence and assumptions (dated sources) | | if any | ✓ |
| Rollout (incl. rollback) | | if risky | ✓ |
| Approvals · Clarifications · Changes | as needed | as needed | as needed |

`dropped` spec needs only `## Objective` + `## Decision` (why, evidence, cheaper next test, revisit trigger).

## CT6 — status moves

| Move | By | Requires |
|---|---|---|
| → approved | user, at spec stage | validator clean; CT7 line |
| → dropped | user, at discover/spec | `## Decision` |
| approved → proposed | anyone | CT8 |
| → implemented | develop stage | all impl steps ✅ in ledger |
| → verified | test/review stage | every AC has test evidence in ledger `Verified by` |
| → released | release stage | user-confirmed rollout; release doc lists spec; PRD FEAT cites it (CT13) |

## Validator

```
python3 <skill dir>/scripts/spec_check.py check <spec.md>                       # spec stage, before approval
python3 <skill dir>/scripts/spec_check.py check <spec.md> --require-approved --rev N   # design stage, before start
python3 <skill dir>/scripts/spec_check.py gaps <doc.md> [--path P]     # normalizing an external doc: report only
python3 <skill dir>/scripts/spec_check.py plan <task dir> [--json]     # impl-plan: coverage, deps, batches, critical path
python3 <skill dir>/scripts/spec_check.py prd <root>/PRD.md            # prd + release stages
python3 <skill dir>/scripts/spec_check.py release <root>/releases/vX.Y.Z.md
python3 <skill dir>/scripts/spec_check.py trace <root> [--json] [--strict]
```
`<skill dir>` = base directory of this skill. Exit 0 = ok or legacy; 1 = errors (one line each, with fix).
