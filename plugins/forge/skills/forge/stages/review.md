# Stage: review

`/forge review <spec|design|arch|test|code> [target]`. Output: `tasks/NN_<slug>/reviews/YYYY-MM-DD_<type>_review.md` from `templates/review.md`. Target outside a task (path, branch, PR) → `<root>/reviews/YYYY-MM-DD_<type>_<slug>_review.md`.

## Target

| Given | Read |
|---|---|
| task# / none | active task's spec, design, ledger (incl. check evidence), changed files |
| path | that file/dir |
| branch | `git diff <base>...<branch>` |
| PR # | `gh pr view` + `gh pr diff` (if `gh` missing, ask for diff) |

## Check against — every row of the chosen type

| Type | Checks |
|---|---|
| spec | validator clean (`scripts/spec_check.py`); objective has success + failure criteria; evidence dated/sourced, assumptions marked, no invented numbers (CT5); **every fact that drives scope, a requirement or a decision re-run by the reviewer** (command or code read; result in the review file's `## Facts re-run`), conclusions drawn from facts checked against the code (`rules/readiness.md` RD4); MVP slice is the smallest that tests the value; non-goals explicit; every AC measurable; KPIs have baseline/target/how measured (standard, deep); telemetry has no PII |
| design | problem has evidence; facts that drive a decision re-run by the reviewer (as for spec); Solving exactly is precise; every R# testable; scope has explicit outs; UC# ↔ R# mapped; open questions resolved or owned; `rules/diagrams.md` DG2 design set present, problem understandable from diagram + `Read:` alone |
| arch | approach choice justified vs alternatives; `rules/diagrams.md` DG2 architect set present, DG3 captions, DG7 diagram ↔ text agree; data model + migrations reversible; APIs meet `rules/api-standards.md` API1–API5 incl. every error case; `rules/security-checklist.md` items answered; flags have kill switch + removal; failure modes + observability; consistent with `understanding.md`; domain pack items |
| test | every R#/UC# covered; negative/edge/authz cases; levels per TS10; `rules/test-standards.md` TS1–TS11; tests actually run (evidence) |
| code | three perspectives below |

## Code review — three perspectives

| Perspective | Checks | Evidence first |
|---|---|---|
| **static** | lint / type / format / security / dependency check results (`rules/quality.md`); `rules/code-standards.md`; matching `rules/profiles/*.md` items; idioms, maintainability, correctness | tool output in ledger; reasoning only where tools are silent or not run |
| **functional** | every spec AC has a passing test that would fail without the change (QG7); authz + tenant boundaries; edge + error cases; regressions; user journey; UI matches `U*` rules + approved screenshots, implementation screenshots linked (`rules/ux.md` UX4, when `ui: true`); ledger `✅` rows have `Verified by` (G5); no scope creep (G8) | spec, tests, ledger |
| **architecture** | contracts + compatibility; modularity, coupling; failure handling, retries, idempotency; performance; data integrity + migrations (`rules/profiles/database.md`); security on changed surface (`rules/security-checklist.md`); rollout + rollback; matches design + evolution path | design, code |

Depth by path: fast / standard → one pass, one section per perspective. Deep → three separate passes.

**Independent reviewers** (deep path, or any path with `forge-review: independent` in project `CLAUDE.md`; relaxes G9 for review only). **Document review** (spec, design, arch, test — incl. the RD6 review before an approval): spawn one fresh-context reviewer per document type, given only `templates/reviewer-brief.md` (document variant) — target doc, the docs it builds on, `understanding.md`, project `CLAUDE.md`, the "Check against" row and `rules/readiness.md`; never your own conclusions or readiness results. **Code review:** spawn three fresh-context reviewers in parallel, one per perspective, each given only `templates/reviewer-brief.md` filled in — diff command, spec, design, ledger, rules paths; never your own conclusions. Merge their tables: same `file:line` + same issue → one finding (keep highest severity, note "raised by n reviewers"); re-number F1…; verify each merged finding yourself before it counts (drop ones the code disproves, say so). Record in the review file which findings came from which reviewer.

## Steps

1. Read target fully. Verify each candidate finding against the code/doc before reporting — no speculative or fabricated findings.
2. Findings table (`templates/review.md`): ID, perspective, severity, where (`file:line` or §), evidence, ref (R/AC/§), impact, fix, verify. **critical / high = blocker**; medium = fix or accept with reason; low = optional. Rank by severity.
3. Verdict: `approve` (no open blockers, mediums fixed or accepted) or `changes needed`.
4. **Fix loop** (code review): each blocker → smallest fix (G8) → rerun the affected checks + tests (`rules/quality.md`) → append re-review with status. Max 3 rounds (`forge-fix-rounds: <n>` overrides); Log `[rework]` per round. Still open → `⛔ blocked` with evidence, ask user. Fix that changes design or spec scope → stop, reopen that approval (CT8).
5. **Approve on code review** → write readiness report from `templates/readiness.md` → `tasks/NN_<slug>/YYYY-MM-DD_readiness.md`; spec status `verified` only if every AC has passing evidence.
6. Summarize in chat: verdict + top 3 findings + readiness state + file links.

## Re-review

Same file exists → append `## Re-review YYYY-MM-DD` with per-finding status (fixed / open / won't fix) + new findings. Never edit earlier sections.

## Independent reviewer

Outside `forge-review: independent`, fresh-context subagent review only when user asks (G9). Give it the target + rules files, not your conclusions.
