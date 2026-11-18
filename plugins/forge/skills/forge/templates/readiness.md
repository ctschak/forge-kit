# Readiness — SPEC-<n> <title>

Date: YYYY-MM-DD · Path: <fast|standard|deep> · Spec rev <N> · Design pinned rev <N>
Recommendation: <ready for human review / merge | not ready — <blocker>>

<!-- Never claim merged / deployed / released without evidence. Rollout needs explicit authority. -->

## State
| State | Status | Evidence |
|---|---|---|
| implemented | ✅ / ❌ | ledger: all items ✅ with `Verified by` |
| reviewed | ✅ / ❌ | review file verdict, open blockers: n |
| verified | ✅ / ❌ | every AC has passing test evidence |
| release-ready | ✅ / ❌ | rollout, rollback, flags, migrations, observability checked below |
| released | ⬜ | after authorized rollout (product `release`) |

## Acceptance criteria
| AC | Test | Result |
|---|---|---|
| AC1 | `path::test name` | pass (command, date) / not covered — why |

## Checks
| Check | Command | Result |
|---|---|---|
| lint | | exit 0 · n issues / not run: <reason> |

Coverage: <changed-line % vs target / not measured: reason>

## Open findings + risks
<!-- accepted mediums, unrun checks, uncovered requirements, residual risks -->

## Rollout + rollback
<!-- flag / staged steps, migration order, rollback trigger + action; n/a — why -->

## Metrics (observed)
| Started | First slice | Elapsed | Approvals | Interventions | Rework rounds |
|---|---|---|---|---|---|

## Next action
<!-- one line: who does what -->
