# <Title>

Status: <stage> · <⬜|🔄|✅|⛔> · YYYY-MM-DD
Size: <Fix|Change|Build> · Task: NN · Owner: <name>

<!-- Fix size keeps: Problem, Solving exactly, Detailed design (before/after), Test coverage. Omit the rest. -->
<!-- design stage owns Problem → Use cases. architect stage owns Approaches → Feature flags. -->

## Problem
<!-- what's broken/missing · who hurts · evidence (ticket, log, metric, file:line) -->

## Solving exactly
<!-- 1–3 bullets: precise outcome. Anything else is out of scope. -->

## Requirements
| ID | Type | Requirement |
|---|---|---|
| R1 | functional | |
| R2 | non-functional | <!-- latency, scale, availability, compliance --> |

## Scope
- In:
- Out:

## Use cases
| ID | Actor | Action | Result |
|---|---|---|---|
| UC1 | | | |

## Approaches
| | A: <name> | B: <name> |
|---|---|---|
| How | | |
| Pros | | |
| Cons | | |
| Effort / risk | | |

**Recommendation:** <A|B> — <one line why>.

## High-level design
```mermaid
flowchart LR
  Client --> API --> Service --> DB
```
- Components:
- Data flow:

## Detailed design
### <Component>
<!-- defect: before vs after. new impl: snippet. -->
```<lang>
// before — path/file.ext:42
```
```<lang>
// after
```

## Data model
<!-- tables/fields/indexes/migrations; omit if none -->

## API design
<!-- one block per endpoint, every row of rules/api-standards.md API1 -->

## Security
<!-- relevant SEC# items from rules/security-checklist.md with answer -->

## Feature flags
| Flag | Default | Rollout | Kill switch | Removal |
|---|---|---|---|---|

## Test coverage
| Test | Level | Covers |
|---|---|---|
| | unit / integration / e2e | R1, UC1 |

## Open questions
-
