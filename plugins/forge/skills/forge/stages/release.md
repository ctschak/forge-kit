# Stage: release

Record what actually shipped and fold it into the PRD. File: `<root>/releases/vX.Y.Z.md` from `templates/release.md`. Rules: `rules/contract.md` CT13, G1, G2. Forge never deploys, merges or tags; it records what the user confirms.

Input: specs with status `verified` + their readiness reports (`stages/review.md`).

## Steps

1. **Pick specs**: list verified specs with readiness state; user chooses which ship together. Version: next semver from `releases/` (patch for fixes, minor for features) — user may override.
2. **Plan**: write the release doc with `status: planned`; run `python3 <skill dir>/scripts/spec_check.py release <file>`; fix errors (stale rev → back to that spec).
3. **Rollout facts** (approval point): ask the user what happened — merged? deployed where, when, by whom? flags / staged rollout? Record only what they confirm; nothing confirmed → stop at `planned`.
4. **Mark released**: each spec `status: released`, `released_in: vX.Y.Z`; release doc `status: released`, rollout + rollback section filled.
5. **Update PRD**: per spec, add or change `## FEAT-n` sections with `Added by: SPEC-n` / `Changed by: SPEC-n`, behavior as now released (from spec R/AC + readiness evidence), evidence level from rollout facts; PRD `revision` +1, `## Changes` line.
5a. **UX evidence:** for released UI changes, link actual verified implementation screenshots in the affected PRD FEAT sections per `rules/ux.md`; retain prototype screenshots in the spec, never as released evidence. Label the capture environment and evidence level; omit unavailable images with reason.
6. **Check**: `spec_check.py release <file>`, `spec_check.py prd <root>/PRD.md`, `spec_check.py trace <root> --strict` → fix gaps.
7. **Outcome hooks**: copy each spec's KPIs (baseline, target) into the release doc with a check date matched to usage frequency — input for the product `outcome` stage.
8. **Tag**: propose `git tag product-vX.Y.Z` (user runs, G2).

## Briefs (only on request)

Positioning, onboarding guide, landing-page copy, marketing or video script — one Markdown file per audience under `<root>/releases/vX.Y.Z/briefs/`, built only from PRD + released spec facts (no invented numbers, CT5).
- Rendered media (images, video) goes only to the storage the user names; permissions untouched; record each in the release doc `## Assets` (version, location, approval, checksum).
- No rendering tool available → deliver scripts / storyboards only; never claim media was produced.

## Done when

- Release doc `released`, all three checks exit 0 (`trace` with no gaps), PRD revision bumped, tag proposed.
- Not confirmed by the user → stays `planned`; say what's missing.
