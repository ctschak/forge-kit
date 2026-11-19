# <Product> — UX standards

Revision 1 · <date> · Code at `<sha>` · Status: proposed

Shared rules every UX spec (`tasks/NN_<slug>/*_ux.md`) links to instead of repeating. A UX spec may tighten a rule, never loosen it without a dated line in its `## Changes`.

## UX spec IDs
Screens `S*`, rules `U*`, usability tasks `T*`; cite as `SPEC-n.U3`. Every `U` cites ≥ 1 spec `R`.

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

## Mockups
One self-contained HTML mockup per UX spec: `tasks/NN_<slug>/ux/<slug>-mockup.html` (rules: forge `stages/ux.md` step 4).

## UX evidence
Per screen in the ledger: screenshots mobile + desktop, light + dark, each required state; axe-core 0 serious/critical; usability results in `tasks/NN_<slug>/reviews/YYYY-MM-DD_usability_review.md`.

## Usability protocol
Moderated, 30 min, think-aloud, 3–5 participants; same script before/after where a current UI exists; record success, time, first click, errors; demo data only.

## Changes
