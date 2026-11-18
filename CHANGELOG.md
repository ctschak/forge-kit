# Changelog

## 0.2.0 — 2026-11-18

Product stages inside forge (design: `docs/2026-11-18-forge-product-design.md`, Slice 1).

- New stages `discover` (build / test first / don't build, evidence labelled) and `spec` (one validated product doc per task).
- `rules/contract.md` (CT1–CT11) + `scripts/spec_check.py` validator (python3 stdlib) + 28 tests in `tests/spec_check/`, run by `scripts/check.sh`.
- Router owns the process: works out the next step from docs, prints `task · path · done → next`, runs it; stops only at approvals, decision-changing ambiguity, irreversible actions.
- Questions only when they change the decision, batched with defaults (was: one per message, every row).
- Docs root defaults to `docs/forge/` without asking.
- design stage links an approved spec (`Spec: SPEC-n @ rev N`) instead of restating Problem → Use cases; develop/test move spec status to implemented/verified; review type `spec`.
- **Breaking:** sizes Fix/Change/Build → paths fast/standard/deep (old names accepted as aliases). `tasks/index.md` template columns `Path`, `Step`, `Started`, `First slice`, `Released`.
- **Breaking (governance):** G1 approvals scaled by path (approved 2026-11-18) instead of before every stage; irreversible/external actions still always need approval.
- `evals/`: scenarios D1 (idea → MVP), D3 (don't build) + baseline/slice-1 results.

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
