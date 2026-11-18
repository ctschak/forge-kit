# forge-kit — maintainer rules

Repo holds Claude Code plugins. `forge` skill lives at `plugins/forge/skills/forge/`.

## Editing the skill

- `SKILL.md` = router only. < 150 lines. Detail that only some branches need → `stages/`, `domains/`, `templates/`, `rules/`.
- One meaning, one place. Rules live in `rules/`; stages cite by file + ID (e.g. `rules/guardrails.md` G5), never restate.
- Write per `rules/doc-style.md`: concise, tables/bullets, code over prose. Positive instruction first; "never" only for hard guardrails.
- Paths referenced inside skill files use `rules/x.md` form so `scripts/check.sh` can verify them.

## Before calling a change done

1. `bash scripts/check.sh` → PASS.
2. Dogfood changed stage in a real project, fresh session.
3. Bump `plugins/forge/.claude-plugin/plugin.json` version + `CHANGELOG.md` entry.

## Design + plan

- Spec: `docs/specs/2026-11-14-forge-design.md` (v0.1) · product stages: `docs/2026-11-18-forge-product-design.md`
- Build plan + progress: `docs/plans/2026-11-14-forge-v0.1-plan.md` · `docs/2026-11-18-forge-product-slice1-plan.md` (checkboxes)
- Demo scenarios + results: `evals/`. Validator tests: `tests/spec_check/` (run by `scripts/check.sh`).

## Git

Agent does not commit, stage or push. Hand back a diff summary; maintainer commits.
