# Readiness — before every approval point

Run before asking for approval of a spec, a design, an implementation plan, or a combined design + plan. List each check with its evidence in the approval message (`Readiness: RD1 ✓ … RD6 ✓`). A check that changes scope or a recommendation goes into the document, not only the message. Project specifics (where the debt register is, which tracker project, naming conventions) come from `understanding.md` and the project `CLAUDE.md`.

| ID | Check | Evidence |
|---|---|---|
| RD1 | **Related records.** Search the project's debt/health records, backlog, work items and tracker (`rules/trackers.md` find command, read-only) for anything touching the same files, packages or modules. Each hit is in scope, or a named non-goal with its reason. | hits listed with ids |
| RD2 | **Deferrals hold up.** Anything left to another item (non-goal, "owned by …", Next/Later) → read that item's live state: owner, status, due date, its own blockers. Compare with the deadline that drives this task. Can't meet it → recommend doing the work here. The recommendation states the facts it rests on. | item id + state + deadline |
| RD3 | **Coverage claims are real.** Every AC or design statement that relies on existing tests names them (`file:line`). A behaviour with no test → name the target (endpoint, function) and the test to add; it fails first if the behaviour changes. | `file:line` per claim |
| RD4 | **No placeholders.** Every number comes from a source (file count, command output with date); every name follows the project's conventions (branch, ids, labels). No unfilled template markers, to-be-decided values or empty baseline cells. | sources cited |
| RD5 | **Consistent.** Requirements, scope, non-goals, ACs and the design don't contradict each other; every R has an AC; every design task maps to an R or AC. | — |
| RD6 | **Reviewed.** `stages/review.md` run on the document (`review spec`; `review design` + `review test` for a design or plan); findings fixed or answered; review file path in the approval message. | review file path |
