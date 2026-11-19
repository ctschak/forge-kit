# <Product> — UX standards

Revision 1 · <date> · Code at `<sha>` · Status: proposed

Default when the project has no DESIGN.md (`rules/ux.md` UX2). Every spec `## UX` links here instead of repeating. A spec may tighten a rule, never loosen it without a dated line in its `## Changes`.

## IDs
Screens `S*`, rules `U*`, usability tasks `T*`; cite as `SPEC-n.U3`. Every `U` cites ≥ 1 spec `R` (CT14).

## Users and context
| Persona | Device (assumption until tested) | Context |
|---|---|---|

## Foundations (existing — reuse)
<!-- theme/preset, token file + names, font + loading, icon set, radius, shadows, dark mode mechanism, breakpoints from existing CSS, touch target ≥ 44 px, no horizontal scroll at 360 px -->

## States (every data view)
| State | Rule |
|---|---|
| Loading | skeleton shaped like content; never blank on refresh |
| Empty (nothing set up) | why + one action that fixes it |
| Zero (set up, no data) | say so + one way to widen |
| Error | what failed + Retry; other panels keep working |
| Partial / stale | timestamp + reason |
| No permission | hide entry; direct URL → redirect + message |

## Copy
<!-- voice, case, domain words, money/date/number formats, error pattern, no promised third-party durations -->

## Accessibility (WCAG 2.2 AA)
Contrast 4.5:1 / 3:1 both themes · full keyboard path, visible focus · labels + linked errors · live regions for async status · text equivalents for charts · reduced motion respected · canvas/drag UIs need a list alternative.

## Prototypes
One self-contained HTML prototype per spec revision: `tasks/NN_<slug>/ux/rev-N/index.html`, screenshots in `ux/rev-N/screens/` (forge `stages/ux.md`).

## UX evidence
Per screen in the ledger: implementation screenshots under `ux/verification/rev-N/`, mobile + desktop, light + dark, each required state; axe-core 0 serious/critical; usability results in `tasks/NN_<slug>/reviews/YYYY-MM-DD_usability_review.md`.

## Usability protocol
Moderated, 30 min, think-aloud, 3–5 participants; same script before/after where a current UI exists; record success, time, first click, errors; demo data only.

## Changes
