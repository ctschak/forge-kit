---
contract: 1
id: SPEC-1
revision: 1
status: approved
path: standard
source_rev: 0aa4982
---

# Archive projects

## Objective
Let org admins archive finished projects so active lists stay short. Success: ≥ 30% of orgs with > 20 projects archive at least one within 30 days (assumption). Failure: support requests about "lost projects" > 2/week.

## Scope
- Archive and restore a project
- Project list hides archived by default; filter to show them

## Non-goals
- Deleting projects
- Bulk archive

## Users and value
Org admin with many old projects; job: find active work fast; value vs today: no way to hide old projects.

## Journeys and rules
- Admin archives project → disappears from default list → visible with `include_archived`.
- Restore returns it to the default list.
- Rule: only same-org access; archiving an archived project is a no-op.

## Requirements
| ID | Requirement |
|---|---|
| R1 | Admin can archive a project; archived time is stored |
| R2 | Default project list excludes archived projects |
| R3 | List can include archived projects on request |
| R4 | Admin can restore an archived project |

## Acceptance criteria
| ID | Criterion | Verifies |
|---|---|---|
| AC1 | Archiving sets an archived timestamp; second archive leaves it unchanged | R1 |
| AC2 | Default list for an org returns 0 archived projects | R2 |
| AC3 | List with include_archived returns archived and active | R3 |
| AC4 | Restore clears the archived timestamp and project reappears in default list | R4 |
| AC5 | Archive/restore of another org's project fails with not-found | R1, R4 |

## Constraints
Python 3.9 stdlib + sqlite3; existing migrations in `db/migrations`.

## Dependencies
n/a — none

## KPIs
| KPI | Baseline | Target | How measured |
|---|---|---|---|
| Orgs archiving ≥ 1 project in 30 days | not measured | 30% (assumption) | `project_archived` events |

## Telemetry
- `project_archived` — on archive — org_id, project_id
- `project_restored` — on restore — org_id, project_id

## Priorities
Now: archive, restore, list filter (1–2 days). Next: UI toggle. Later: bulk archive.

## Approvals
- 2026-11-18 Owner rev 1
