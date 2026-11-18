---
id: SPEC-<n>.TASK<NN>
type: <story|enabler|spike|bug|task>
refs: [R<n>, AC<n>]
depends_on: []
layer: <db|backend|frontend|integration|telemetry|test|mixed>
---

# NN <item-name>

Design ref: §<section> · Spec: SPEC-<n> @ rev <N>

## Outcome
<!-- one measurable engineering result -->

## Scope
<!-- in · non-scope -->

## Acceptance criteria
<!-- this item's checks; cite spec AC it contributes to -->

## Files
- Modify: `path/file.ext` (fn/area)
- Create: `path/new.ext`
- Test: `path/file.test.ext`

## Steps
1.
2.

## Code
```<lang>
// before — path/file.ext:42   (defect / change)
```
```<lang>
// after / new snippet
```

## Verify
```bash
<command>
```
Expected: <exact output / test names green>

## Done when
- [ ] Tests for this item written and green
- [ ] Verify command passes
- [ ] Ledger row updated with `Verified by`

## Blockers
<!-- none, or what + who unblocks -->

## Deviations
<!-- filled during develop if implementation differs from design -->
