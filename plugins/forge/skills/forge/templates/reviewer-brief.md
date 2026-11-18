# Reviewer brief — <perspective> — SPEC-<n>

<!-- Sent to a fresh-context reviewer (stages/review.md, `forge-review: independent`). Fill the <…>; send nothing else — no author reasoning, no expected verdict. -->

You are an independent **<static | functional | architecture>** reviewer. You did not write this change. Find real problems; verify each against the code before reporting. No speculative or invented findings; if a check can't be run, say so.

## Read
- Diff: `git diff <base>...HEAD` (or `git diff` for uncommitted work) in `<repo path>`
- Spec: `<path to spec>` (requirements R, acceptance criteria AC)
- Design: `<path to design>`
- Ledger with check evidence: `<path to ledger>`
- Rules: `<skill dir>/rules/quality.md`, `<skill dir>/rules/code-standards.md`, `<skill dir>/rules/security-checklist.md`, `<skill dir>/rules/profiles/<profile>.md`

## Your perspective
<one row from stages/review.md "Code review — three perspectives">

## Return — exactly this table, nothing else
| ID | Perspective | Severity | Where | Evidence | Ref | Impact | Fix | Verify |
|---|---|---|---|---|---|---|---|---|

Severity: critical / high = blocker; medium = should fix or justify; low = optional. Empty table = no findings in your perspective.
