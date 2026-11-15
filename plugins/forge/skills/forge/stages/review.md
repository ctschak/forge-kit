# Stage: review

`/forge review <design|arch|test|code> [target]`. Output: `tasks/NN_<slug>/reviews/YYYY-MM-DD_<type>_review.md` from `templates/review.md`. Target outside a task (path, branch, PR) → `<root>/reviews/YYYY-MM-DD_<type>_<slug>_review.md`.

## Target

| Given | Read |
|---|---|
| task# / none | active task's design, ledger, changed files |
| path | that file/dir |
| branch | `git diff <base>...<branch>` |
| PR # | `gh pr view` + `gh pr diff` (if `gh` missing, ask for diff) |

## Check against — every row of the chosen type

| Type | Checks |
|---|---|
| design | problem has evidence; Solving exactly is precise; every R# testable; scope has explicit outs; UC# ↔ R# mapped; open questions resolved or owned; `rules/diagrams.md` DG2 design set present, problem understandable from diagram + `Read:` alone |
| arch | approach choice justified vs alternatives; `rules/diagrams.md` DG2 architect set present, DG3 captions, DG7 diagram ↔ text agree; data model + migrations reversible; APIs meet `rules/api-standards.md` API1–API5 incl. every error case; `rules/security-checklist.md` items answered; flags have kill switch + removal; failure modes + observability; consistent with `understanding.md`; domain pack items |
| test | every R#/UC# covered; negative/edge/authz cases; levels per TS10; `rules/test-standards.md` TS1–TS11; tests actually run (evidence) |
| code | correctness vs design + step files; `rules/code-standards.md`; security checklist on changed surface; tests present + green; ledger `✅` rows all have `Verified by` (flag any without, G5); no scope creep (G8) |

## Steps

1. Read target fully. Verify each candidate finding against the code/doc before reporting — no speculative findings.
2. Findings table: severity (high = wrong/unsafe/data loss; med = will cause rework; low = polish), location (`file:line` or §), issue, fix. Rank by severity.
3. Verdict: `approve` (no high, meds accepted) or `changes needed`.
4. Summarize in chat: verdict + top 3 findings + file link.

## Re-review

Same file exists → append `## Re-review YYYY-MM-DD` with per-finding status (fixed / open / won't fix) + new findings. Never edit earlier sections.

## Independent reviewer

Fresh-context subagent review only when user asks (G9). Give it the target + rules files, not your conclusions.
