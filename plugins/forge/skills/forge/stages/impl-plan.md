# Stage: impl-plan

Input: approved design. Output: `tasks/NN_<slug>/impl-tasks/` — one file per step from `templates/impl-task.md` + `ledger.md` from `templates/ledger.md`.

## Steps

1. Split design into ordered steps. One step = one deliverable a reviewer could accept or reject on its own, with its own verification. Typical order: data/migration → domain logic → API → UI → wiring/flags → cleanup.
2. Name files `NN_<kebab-slug>.md`, NN in execution order, zero-padded.
3. Each step file fills every template field:
   - Design ref (§ + R#/UC#)
   - Files (exact paths; verify existing paths in repo)
   - Steps (numbered actions)
   - Code: before/after for changes, snippet for new — signatures + the non-obvious parts, not whole files
   - Verify: exact command + expected result
   - Done when
4. Every R# covered by ≥1 step; list any R# with no step → fix before approval.
5. Create `ledger.md`: one row per step, all `⬜ not started`; `Next:` = step 01.
6. Show user the step list (table: #, step, verify) → approval.

## Done when

- Every R# mapped to a step; every step has a runnable Verify.
- Ledger created; index stage = `impl-plan ✅`; next = develop.
