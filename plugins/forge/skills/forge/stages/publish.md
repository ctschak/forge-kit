# Stage: publish

Turn a checked plan into tracker issues, idempotently. Rules: `rules/trackers.md` (TR1–TR7). Input: task with `impl-tasks/` that passes `spec_check.py plan`. Output: issues + ledger `Issue` column.

## Steps

1. **Provider** (TR1, TR3): read `forge-tracker:`; missing → detect + ask once + persist. `local` or tool unavailable → stop: ledger + `plan --json` are the task list; say how to enable.
2. **Manifest:** `python3 <skill dir>/scripts/spec_check.py plan <task dir> --json > <scratch>/plan.json`. Errors → back to impl-plan.
3. **Existing:** list issues whose body has `forge:SPEC-n` (any state) with the TR3 command → map to `<scratch>/issues.json`.
4. **Plan actions:** `python3 <skill dir>/scripts/tracker_sync.py plan --manifest plan.json --existing issues.json [--native-deps]`.
5. **Preview** (TR2) — one table, then ask approval:

| Target | Create | Update | Skip | Conflict | Orphan |
|---|---|---|---|---|---|
| `<provider> <project/repo>` | n | n | n | n | n |

   plus each create/update title + depends-on. Conflicts (marker found twice) and orphans (item removed from spec) are listed with a proposed human action; forge doesn't resolve them itself.
6. **Apply** in planner order (deps first, parent last). For each action:
   - create / update → write body to a temp file; replace every `{{SPEC-n.TASKk}}` with that item's issue ref (created earlier in this run, or from the planner) → provider command.
   - orphan → comment with the planner's text only if the user approved it.
   - Re-read the issue (TR5) → `python3 <skill dir>/scripts/tracker_sync.py ledger <ledger.md> --set ID=URL`.
   - Failure → record, continue with the rest.
7. **Report:** created / updated / skipped / failed counts + URLs; failed → "rerun publish to resume". Log line in ledger.

## Revised spec

Spec revision changed after publish → re-run impl-plan (items may change) → publish again: planner marks `update` for changed items, `create` for new ones, `orphan` for removed ones. Preview shows the impact; nothing is closed.

## Done when

- Every approved action applied and read back, or reported failed.
- Ledger `Issue` filled for every published item; rerun shows only `skip`.
