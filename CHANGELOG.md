# Changelog

## 0.1.2 — 2026-11-15

- `rules/diagrams.md` (DG1–DG7): diagram type per question, required set per size, `**Read:**` plain-language caption, new/changed markers, diagram ↔ text consistency.
- design stage: current-state flow (Problem), actor flow (≥ 3 actors). architect stage: component, sequence per main UC, ER, state, before/after.
- `templates/design.md`: diagram + caption slots. review design/arch checks diagrams. DS7 → points to `rules/diagrams.md`.

## 0.1.1 — 2026-11-15

- Docs-root prompt: one question; offer `forge-docs:` line only when a non-default path is chosen (dogfood: Leadly asked two questions + offered a CLAUDE.md for the default).
- README: command is `/forge:forge` (plugin skill namespace).

## 0.1.0 — unreleased

- Repo scaffold: marketplace + `forge` plugin manifests, README, maintainer CLAUDE.md, `scripts/check.sh` (incl. `claude plugin validate`).
- `SKILL.md` router: docs-root resolution, routing, sizing (Fix/Change/Build), task numbering, resume.
- `rules/`: guardrails G1–G9, doc style, API standards (REST, errors, payments example), code, test, security checklist.
- `stages/`: onboard, ai-readiness, design, architect, impl-plan, develop, test, review.
- `templates/`: design, impl-task, ledger, review, understanding, health, tasks-index.
- `domains/`: CRM, voice/message agents, ecommerce.
- Pending before release: dogfood on Leadly (plan Tasks 5–7, 9).
