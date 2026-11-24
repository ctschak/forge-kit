# Stage: design

Owns design doc sections **Problem → Use cases** (legacy Fix: also Detailed design before/after + Test coverage). File: `tasks/NN_<slug>/YYYY-MM-DD_<slug>_design.md` from `templates/design.md`.

Read first: `understanding.md` (if present), matching `domains/*.md` (see SKILL.md §7), `rules/diagrams.md`.

## Resolve input — always one contract spec, never a second requirements doc

| Input (`design <x>`) | Do |
|---|---|
| `SPEC-n` or spec path | that task's spec |
| issue `#n` / URL | read via tracker (`rules/trackers.md`); body has `forge:SPEC-n.TASKk` marker → that task; else treat as external requirement |
| external PRD / doc path | **normalize**: new task (SKILL.md §4); spec from `templates/spec.md` with `source: external:<path>@<rev or date>`, sections mapped from the doc, unmapped text kept under `## Imported`; run `spec_check.py gaps` → `## Open gaps` with a proposed decision per gap; status `proposed` → spec approval point. Never invent R, AC or numbers to fill gaps |
| supplied text | fast-path spec stub (Objective, Scope, Non-goals, R, AC) → spec approval point |

Path: take the spec's `path`; re-pick (SKILL.md §4) only with a one-line reason from code evidence.

## Spec exists (contract repo)

Task has an approved spec (`rules/contract.md`) → it owns Problem → Use cases. Then:
1. Run `python3 <skill dir>/scripts/spec_check.py check <spec> --require-approved`. Errors → back to spec stage; don't design around them.
2. Design header: `Spec: SPEC-n @ rev N` (pins revision; later checks add `--rev N` → stale if spec changed).
3. Problem → Use cases sections = one line each linking the spec; cite `SPEC-n.R*` / `AC*`, never restate them (CT9). `ui: true` → read `## UX`, the prototype and DESIGN.md / `ux-standards.md` (`rules/ux.md` UX4); UI parts cite `SPEC-n.U*` and screens `S*`. Prototype = visual intent, not architecture; conflicts with the spec → clarify, don't guess.
4. Inspect the real code, contracts, tests, conventions; write **minimum sufficient** engineering content — sections by path below, omit the rest.
5. Material gaps → list each with a proposed decision; product answers go to spec `## Clarifications` (scope change → CT8).

| Section | fast | standard | deep |
|---|---|---|---|
| Current vs proposed (`file:line`), gaps + proposed decisions | in spec `## Fix` | ✓ | ✓ |
| Affected components + reuse | — | ✓ | ✓ |
| Approaches (alternatives + chosen trade-off) | — | if a real choice | ✓ |
| Before/after code or API example | ✓ | where it helps | ✓ |
| Data model · permissions · failure modes · compatibility · observability | — | if touched | ✓ |
| Migration: every schema/contract change states (1) forward step, (2) **rollback** — down step, or why leaving it is safe (e.g. additive nullable column), (3) order vs code deploy (expand → migrate → contract) | — | if data/contract changes | ✓ |
| Evolution path: now vs later, scaling triggers (metric + threshold → action), capacity/cost (assumptions labelled) | — | short | ✓ |

**Spike** only when unknown feasibility blocks a decision: work item `type: spike` with question, time box, decision it unblocks. Design waits only on blocking spikes.

No spec (legacy task) → sections below as before.

## Grill — cover every row before writing

| Section | Get from user / code |
|---|---|
| Problem | the last real occurrence; who hit it; evidence (ticket, log, `file:line`, metric) |
| Solving exactly | the one outcome that means done; what would make it a failure even if it "works" |
| Requirements | functional R#; non-functional: latency, volume, availability, compliance, cost |
| Scope | explicitly out: what user might assume is included |
| Use cases | actors, triggers, happy path, top 3 edge/failure paths |
| Constraints | stack, deadlines, dependencies, team, existing contracts that can't break |

Questions per SKILL.md §6.1: only decision-changing, batched, with defaults. Guess when you can: "I'm guessing X because Y — right?"

## Fast path / legacy Fix (lite)

1. Reproduce or locate root cause; cite `file:line`.
2. Write Problem, Solving exactly, Detailed design with **before vs after** code, Test coverage (failing test that proves the bug).
3. `rules/readiness.md` RD1–RD6 → approval → develop.

## Write

- Requirements numbered R1…; each testable.
- Use cases UC1… in table.
- Diagrams per `rules/diagrams.md` DG2 (design column): current-state flow in Problem with `❌` at the break; actor flow in Use cases if ≥ 3 actors. Each with `**Read:**` caption (DG3).
- Concise per `rules/doc-style.md`.

## Done when

- Every R# testable; every UC# maps to ≥1 R#.
- DG2 diagrams present (or `n/a — <why>`), each captioned.
- Open questions listed (or none).
- `rules/readiness.md` RD1–RD6 run (RD6 = `review design` + `review test`); with `forge-approvals: combined` they run after impl-plan, over design + plan together.
- Approval point per path (SKILL.md §4) → `Status: design · ✅`, index updated, next step started (architect for deep, impl-plan for standard).
