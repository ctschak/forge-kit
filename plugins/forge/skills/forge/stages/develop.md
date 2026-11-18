# Stage: develop

Input: approved design + `impl-tasks/` (standard, deep) or spec `## Fix` / design Detailed design (fast). Apply `rules/code-standards.md`.

## Loop — per ledger step

1. Read ledger `Next:` → step file. Set row `🔄 in progress`, date.
2. Read the files the step lists; confirm design still fits the code. Material mismatch → stop, note in step `## Deviations`, ask user.
3. Write the test first where the step has testable behaviour; run it; see it fail for the right reason.
4. Implement — smallest change for the step (G8).
5. Run the step's **Verify** command. Paste the result summary.
   - Pass → row `✅ done`, `Verified by` = `<command> → <result>`.
   - Fail → fix and re-run; still failing → row `⛔ blocked`, `Blockers:` = pasted error, ask user.
6. Update `Next:`, append Log line, update `tasks/index.md` date.
7. Hand back diff summary for the step (files + one line each). Git per G2.
8. Next step — or pause if user asked to go step-by-step.

A row reaches `✅` only with `Verified by` filled from a command actually run this session (G5, G7).

## Fast path (no ledger)

Apply spec `## Fix` (or design) before/after → run failing test → passes → run related suite → record result in design `Status:` + index.

## Also

- System structure changed (new module, entity, integration, flow) → update `understanding.md` sections + SHA note.
- New debt or risk spotted → add row to `health.md`, don't fix it in this task (G8).

## Done when

All ledger rows `✅` with evidence; spec status `implemented` (if spec exists); index stage = `develop ✅`; next = test (starts automatically).
