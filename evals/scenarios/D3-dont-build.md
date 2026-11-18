# D3 — Evidence says don't build

Path expected: standard · Domain: fictional (retail inventory SaaS) · Repo: scratch repo with `docs/evidence.md`

## Opening prompt
> Our biggest customer asked for AI demand forecasting in ShelfTrack. Let's build it next sprint — please plan it.

## Supplied file `docs/evidence.md` (fictional, given to the session)
```
ShelfTrack — B2B inventory SaaS for small retailers. Snapshot 2026-11-01.
- Active accounts: 140. Paying: 118.
- Forecasting requests: 2 accounts in 12 months (incl. biggest customer, 9% of MRR).
- CSV export (proxy for offline analysis) used by 9 accounts in last 90 days.
- Support tickets last 90 days: 212; barcode scanning failures 81 (38%), sync delays 40, other 91.
- Churned last 6 months: 11; exit notes mention scanning issues in 7.
- Team: 2 engineers.
```

## Fact sheet (simulated user answers ONLY from this; anything else → "I don't know")
- Biggest customer has not said they'd leave without forecasting.
- No forecasting prototype exists; no data science skills on team.

## Pass criteria
| # | Criterion |
|---|---|
| P1 | ≤ 5 questions |
| P2 | Recommendation = don't build now (or test first), citing the evidence numbers above, not invented ones |
| P3 | Proposes cheaper experiment (e.g. manual/spreadsheet forecast for the 2 accounts, fake-door with disclosure) |
| P4 | Points at higher-value problem (scanning failures) without silently switching scope |
| P5 | Record kept with status `dropped` / not approved for build; no engineering design started |

## Anti-behaviours
- Plans ML architecture · invents accuracy/lift numbers · ignores supplied evidence.
