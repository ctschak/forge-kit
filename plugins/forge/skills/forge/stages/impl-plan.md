# Stage: impl-plan

Input: approved design (fast: approved spec). Output: `tasks/NN_<slug>/impl-tasks/` — one work item per file from `templates/impl-task.md` + `ledger.md` from `templates/ledger.md`. Rules: `rules/contract.md` CT12.

## Steps

1. **Split into work items.** One item = one measurable engineering outcome a reviewer can accept or reject, with its own Verify and its tests inside Done when.
   - Fast path → one item.
   - Separate db / backend / frontend / integration / telemetry only when each part is independently verifiable and leaves the system working (e.g. migration expand step before code that uses it). Coupled changes stay one item; say why in one line.
   - Separate integration / e2e item only when it proves something per-item tests can't.
   - Type each item: `story` (user-visible value) · `enabler` (technical prerequisite) · `spike` (question + time box + decision) · `bug` · `task`.
   - No trivial items (rename, config line) — fold them into the item that needs them.
   - Item with a migration: Verify covers forward and the design's rollback (down step run, or reason it's safe to leave).
2. **Files:** `NN_<kebab-slug>.md`, NN in execution order, zero-padded; front matter `id: SPEC-n.TASK<NN>`, `type`, `refs` (R/AC + design §), `depends_on`, `layer`. Fill every template field: Outcome, Scope / non-scope, Acceptance criteria, Files (verify paths exist), Steps, Code (signatures + non-obvious parts), Verify (exact command + expected), Done when, Blockers.
3. **Check:** `python3 <skill dir>/scripts/spec_check.py plan <task dir>` → fix every error (uncovered R/AC, unknown dep, cycle, duplicate, bad id). Stale design pin → back to design.
4. **Ledger:** one row per item, all `⬜ not started`; `Next:` = first item of batch 1; `Batches:` + `Critical path:` from the check.
5. **Show** table (ID, item, type, depends, verify) + batches + critical path. Approval point only on deep path; otherwise continue to develop (SKILL.md §5).
6. **Publish (optional):** project has `forge-tracker:` other than `local`, or user asks → `stages/publish.md`.

## Done when

- `plan` check exit 0; every item has a runnable Verify.
- Ledger created; index step = `impl-plan ✅`; next = develop (or publish, then develop).
