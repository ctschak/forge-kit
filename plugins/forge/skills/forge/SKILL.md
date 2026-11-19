---
name: forge
description: Use when turning an idea, feature request, bug or existing product into shipped, verified software — evaluating whether to build, writing a spec, MVP scoping, designing, architecting, planning, building, testing or reviewing work in a project; onboarding onto an unfamiliar codebase; auditing AI-assisted-dev setup; or continuing work tracked in docs/forge.
argument-hint: "[<request> | new <desc> | discover | spec | design | architect | impl-plan | develop | test | review <spec|design|arch|test|code> [target] | onboard | ai-readiness] [task#]"
---

# forge

Product + engineering delivery: idea → validated spec → verified code, fast and safe. Forge owns the process: works out the next step from the docs, runs it, and stops only where a decision or approval is needed. State lives in docs so any session resumes.

## 1. Always

- Load `rules/guardrails.md` and `rules/doc-style.md` first, every run. Guardrails are hard.
- Precedence: user/project `CLAUDE.md` > forge rules, except guardrails (only G2, G9 relaxable).
- Least process that keeps quality: no extra docs, questions or ceremonies the path doesn't need.

## 2. Resolve docs root

1. Project `CLAUDE.md` has line `forge-docs: <path>` → use it; expand `~`; relative = from repo root.
2. Else → `docs/forge/` in repo root. Create it on first write; say so in one line ("Docs in `docs/forge/` — say if you want another path"). Other path chosen later → move docs, offer `forge-docs:` line in project `CLAUDE.md`.

Layout under root:
```
understanding.md · health.md
PRD.md                                            ← released behavior only (CT13)
releases/vX.Y.Z.md                                ← what shipped, when, evidence
tasks/index.md
tasks/NN_<slug>/YYYY-MM-DD_<slug>_spec.md        ← product: SPEC-<NN>, rules/contract.md
tasks/NN_<slug>/YYYY-MM-DD_<slug>_design.md      ← engineering (standard, deep)
tasks/NN_<slug>/ux/rev-N/index.html, screens/*.png  ← optional code-first UX
tasks/NN_<slug>/impl-tasks/ledger.md, NN_<step>.md
tasks/NN_<slug>/reviews/YYYY-MM-DD_<type>_review.md
```

## 3. Route

| Args | Load |
|---|---|
| `onboard` | `stages/onboard.md` |
| `ai-readiness` | `stages/ai-readiness.md` |
| `new <desc>` or free-text request for new work | §4 |
| `discover` · `spec` | `stages/<name>.md` on active task |
| `design [SPEC-n \| path \| #issue \| text]` | `stages/design.md` (resolves input, normalizes external docs) |
| `develop [SPEC-n.TASKk \| #issue \| batch]` | `stages/develop.md` |
| `architect` · `impl-plan` · `test` | `stages/<name>.md` on active task |
| `publish` | `stages/publish.md` (tracker issues) |
| `prd` | `stages/prd.md` (baseline PRD for an existing product) |
| `release` | `stages/release.md` (verified specs → release doc → PRD) |
| `review <type> [target]` | `stages/review.md` |
| `SPEC-n` · `#issue` | that task → §5 next step |
| `status` | one line per open task: path, step, readiness state (`templates/readiness.md`) |
| none | §5 next step |

Modifiers on any of the above: `until <step>` → stop after that step · `only <step>` → run just that step.

Experts may name any stage or path explicitly — that overrides the inferred step.

`[task#]` given → that task is active. None given + exactly one open task → that one; several → one line each (task, path, step, next), user picks.

No tasks yet: repo has code, no `understanding.md`, request needs code knowledge → `stages/onboard.md` first. Empty repo, no request → ask what to build.

## 4. New task + paths

1. Pick the path from the request and evidence; state it in one line with the reason. User may override. Escalate or simplify later with a one-line reason.

| Path | When | Steps | Approval points (G1) |
|---|---|---|---|
| fast | clear, reversible, low-risk (defect, small tweak) | spec (fast) → develop → test → review code | spec |
| standard | feature; new product idea with a small, reversible MVP | discover (lite; skip if problem + user clear) → spec → design → impl-plan → develop → test → review code | spec · design |
| deep | hard to undo or wide blast radius: data migration, security/auth, money, cross-system contracts. Not for demand uncertainty — discover's "test first" handles that | discover → spec → design → architect → review design+arch → impl-plan → develop → test → review test+code → staged rollout | spec · design+arch · plan · rollout |

Old sizes still accepted: Fix = fast, Change = standard, Build = deep.

2. NN = highest existing `tasks/NN_*` number + 1 (01 if none), zero-padded. Never reuse a number — check `index.md` rows too. Spec ID = `SPEC-<NN as integer>`.
3. Create `tasks/NN_<kebab-slug>/`, spec from `templates/spec.md`, row in `tasks/index.md` (create from `templates/tasks-index.md` if missing; set `Started`).
4. Start first step: `discover` (standard, deep) or `spec` (fast).

Aims, not promises: fast in hours; standard MVP slice usable in 2–3 days, production-ready ≤ 2 weeks when scoped so. Doesn't fit → cut scope or report blocker; never skip quality. Spike only when a specific question blocks a decision: question + time box + resulting decision.

## 5. Next step (resume and hand-off)

1. Read `tasks/index.md` → active task; spec `status`; design `Status:` line; `impl-tasks/ledger.md` `Next:` + `Blockers:`. Docs, not chat memory.
2. Next step = first unfinished step of the task's path (§4). Spec `dropped` → task closed.
3. Print one line: `SPEC-7 Lesson reminders · standard · spec approved → next: design (starting)`.
4. Run it, then the next, through the path: spec → design → plan → develop → test (quality gate, `rules/quality.md`) → review code (3 perspectives + fix loop) → readiness report. Stop only for: approval point, decision-changing ambiguity, irreversible/external action, missing authority, blocker, `until`.
   - Approval denied → Log `[approval] denied: <reason>`, stop, offer alternatives (revise, smaller scope, drop); build nothing.
   - Project `CLAUDE.md` `forge-approvals: combined` + spec approved → standard path asks design + plan approval together (one stop).
5. Load only that stage file + the files it needs. For customer-facing work, load `rules/ux.md`: code-first HTML prototypes and embedded browser screenshots before spec approval when materially useful; no external design tool or extra approval gate required.

If `understanding.md` commit SHA is ≥ 30 commits behind `HEAD` (`git rev-list --count <sha>..HEAD`), offer `onboard` refresh first.

## 6. Every stage

1. **Questions only when the answer changes the decision.** Batch related ones (≤ 3 per message), offer a recommended default for each. Otherwise state `(assumption)` and continue; list assumptions at the next approval point. Anchor in specifics (a real scenario, a file, a number).
2. **Write** the stage's output into its file, per `rules/doc-style.md`. Resume = continue from the docs; never regenerate an artifact that exists and is still valid.
3. **Approval** only at the path's approval points (§4) and before irreversible/external actions (G1). Changes requested → revise, ask again.
4. **Record.** Update spec `status` / design `Status:` line, ledger (if any), `tasks/index.md` row (step, status, date). Append one `Log` line (tags `[approval]` `[intervention]` `[rework]` for metrics).
5. **Continue.** Print the §5 line and start the next step; user can redirect or stop.

## 7. Domain packs

Task touches the domain → discover + spec + design + architect + review consult:
- CRM, leads, contacts, pipelines → `domains/crm.md`
- WhatsApp/SMS/voice bots, AI receptionists, conversational agents → `domains/voice-message-agents.md`
- Catalog, cart, checkout, orders, payments → `domains/ecommerce.md`
