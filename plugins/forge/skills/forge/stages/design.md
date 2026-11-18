# Stage: design

Owns design doc sections **Problem → Use cases** (legacy Fix: also Detailed design before/after + Test coverage). File: `tasks/NN_<slug>/YYYY-MM-DD_<slug>_design.md` from `templates/design.md`.

Read first: `understanding.md` (if present), matching `domains/*.md` (see SKILL.md §7), `rules/diagrams.md`.

## Spec exists (contract repo)

Task has an approved spec (`rules/contract.md`) → it owns Problem → Use cases. Then:
1. Run `python3 <skill dir>/scripts/spec_check.py check <spec> --require-approved`. Errors → back to spec stage; don't design around them.
2. Design header: `Spec: SPEC-n @ rev N` (pins revision; later checks add `--rev N` → stale if spec changed).
3. Problem → Use cases sections = one line each linking the spec; cite `SPEC-n.R*` / `AC*`, never restate them (CT9).
4. Write only engineering content: current behavior in code (`file:line`), diagrams (DG2 design set may reuse spec journeys), then architect sections per path.
5. Need a product answer → ask; record it in spec `## Clarifications` (scope change → CT8).

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
3. Approval → develop.

## Write

- Requirements numbered R1…; each testable.
- Use cases UC1… in table.
- Diagrams per `rules/diagrams.md` DG2 (design column): current-state flow in Problem with `❌` at the break; actor flow in Use cases if ≥ 3 actors. Each with `**Read:**` caption (DG3).
- Concise per `rules/doc-style.md`.

## Done when

- Every R# testable; every UC# maps to ≥1 R#.
- DG2 diagrams present (or `n/a — <why>`), each captioned.
- Open questions listed (or none).
- Approval point per path (SKILL.md §4) → `Status: design · ✅`, index updated, next step started (architect for deep, impl-plan for standard).
