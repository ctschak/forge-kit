# Stage: design

Owns design doc sections **Problem → Use cases** (Fix size: also Detailed design before/after + Test coverage). File: `tasks/NN_<slug>/YYYY-MM-DD_<slug>_design.md` from `templates/design.md`.

Read first: `understanding.md` (if present), matching `domains/*.md` (see SKILL.md §7).

## Grill — cover every row before writing

| Section | Get from user / code |
|---|---|
| Problem | the last real occurrence; who hit it; evidence (ticket, log, `file:line`, metric) |
| Solving exactly | the one outcome that means done; what would make it a failure even if it "works" |
| Requirements | functional R#; non-functional: latency, volume, availability, compliance, cost |
| Scope | explicitly out: what user might assume is included |
| Use cases | actors, triggers, happy path, top 3 edge/failure paths |
| Constraints | stack, deadlines, dependencies, team, existing contracts that can't break |

One question per message. Guess when you can and let user correct: "I'm guessing X because Y — right?"

## Fix size (lite)

1. Reproduce or locate root cause; cite `file:line`.
2. Write Problem, Solving exactly, Detailed design with **before vs after** code, Test coverage (failing test that proves the bug).
3. Approval → develop.

## Write

- Requirements numbered R1…; each testable.
- Use cases UC1… in table.
- Concise per `rules/doc-style.md`.

## Done when

- Every R# testable; every UC# maps to ≥1 R#.
- Open questions listed (or none).
- User approved → `Status: design · ✅`, index updated, next stage named (architect for Build, impl-plan for Change, develop for Fix).
