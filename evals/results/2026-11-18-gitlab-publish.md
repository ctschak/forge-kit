# Real GitLab publish — forge 0.5.0

Date: 2026-11-18 · Runner: headless `claude -p`, `--plugin-dir plugins/forge` (0.5.0), `--allowedTools` python3 / glab / git remote. Input: E2 run (projapp, SPEC-1 rev 1, 2 work items, plan check OK), no `forge-tracker:` line. Target: private scratch project `gitlab.com/chakra.cisco/forge-tracker-demo` (glab 1.114). Closes sliceA finding A5 for GitLab.

| Turn | Input | Secs | Cost | Result |
|---|---|---|---|---|
| 1 | `/forge:forge publish 01` | 64 | 0.46 | ✅ detected GitLab remote + glab auth; preview 3 creates (TASK1, TASK2, parent last), 0 existing; one ask: provider (persist `forge-tracker: gitlab`) + label creation; nothing written |
| 2 | `yes` | 54 | 0.78 | ✅ 3 issues created (#1, #2, #3 parent), all read back; `{{SPEC-1.TASK1}}` → `#1` in TASK2 body; ledger `Issue` filled; planner rerun → skip 3; scratch files removed; foreign untracked files left alone |
| 3 | fresh session, `/forge:forge publish 01` | 73 | 0.52 | ✅ no question (preference persisted); 0 create / 0 update / 3 skip; no GitLab writes; issue count still 3 |

Independent check: `glab issue list --all` → 3 issues, markers `<!-- forge:SPEC-1[.TASKk] rev=1 -->`, labels as previewed.

## Findings

| # | Finding | Action |
|---|---|---|
| G1 | Parent (spec) issue URL has no ledger row — recorded only in a log line | backlog: ledger header `Tracker: <url>` line for the parent |
| G2 | GitLab returns `/-/work_items/N` URLs for issues; flat issues only, no task hierarchy | backlog: opt-in `forge-tracker: gitlab:workitems` (child tasks via `glab work-items create --type task` + GraphQL parent link; `work-items` is experimental in glab 1.114) |
| G3 | Revised-spec update path (rev 2 → `update`) not exercised live | covered by tracker_sync unit tests; run on next real spec revision |
| G4 | GitHub publish still not run: `gh` 2.105 installed + logged in, but the fine-grained token had no grant for the private target repo (404, `metadata=read`); repo creation not permitted | skipped by user 2026-11-18; rerun with a token scoped to a private scratch repo (Issues: read/write) |
