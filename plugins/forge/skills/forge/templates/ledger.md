# Ledger — NN <task>

Rule: `✅ done` only with `Verified by` filled (command + result). Statuses: `⬜ not started` · `🔄 in progress` · `✅ done` · `⛔ blocked`.

Status = evidence state. When a tracker is used it owns live status (assignee, open/closed); `Issue` holds the verified URL.

| ID | Item | Type | Depends | Status | Verified by | Issue | Updated |
|---|---|---|---|---|---|---|---|
| SPEC-<n>.TASK1 | <item-slug> | story | — | ⬜ not started | — | — | — |

Checks: <from quality_detect: lint `cmd` · type `cmd` · test `cmd` · not available: …>

Next: SPEC-<n>.TASK1 — <what to do first>
Batches: <from `spec_check.py plan`> · Critical path: <…>
Blockers: none

## Log
<!-- tags: [approval] user approved/denied · [intervention] user had to unblock or correct · [rework] item reopened / review round · check <name>: <cmd> → exit n, counts -->
- YYYY-MM-DD — impl-plan created
