---
name: forge
description: Use when starting, resuming, evaluating, designing, architecting, planning, building, testing or reviewing software work in a project — kicking off a feature or fix, onboarding onto an unfamiliar codebase, auditing AI-assisted-dev setup, or continuing work tracked in docs/forge.
argument-hint: "[new <desc> | design | architect | impl-plan | develop | test | review <design|arch|test|code> [target] | onboard | ai-readiness] [task#]"
---

# forge

Senior-architect workflow: understand → question → write approach → approval → build in verified steps → review. State lives in docs so any session resumes.

## 1. Always

- Load `rules/guardrails.md` and `rules/doc-style.md` first, every run. Guardrails are hard.
- Precedence: user/project `CLAUDE.md` > forge rules, except guardrails (only G2, G9 relaxable).

## 2. Resolve docs root

1. Project `CLAUDE.md` has line `forge-docs: <path>` → use it; expand `~`; relative = from repo root.
2. Else → `docs/forge/` in repo root.
3. Root dir missing → say which path, confirm before creating.
4. No project `CLAUDE.md` or no `forge-docs:` line, first write → ask once: default `docs/forge/` or another path; offer to add the `forge-docs:` line.

Layout under root:
```
understanding.md · health.md
tasks/index.md
tasks/NN_<slug>/YYYY-MM-DD_<slug>_design.md
tasks/NN_<slug>/impl-tasks/ledger.md, NN_<step>.md
tasks/NN_<slug>/reviews/YYYY-MM-DD_<type>_review.md
```

## 3. Route

| Args | Load |
|---|---|
| `onboard` | `stages/onboard.md` |
| `ai-readiness` | `stages/ai-readiness.md` |
| `new <desc>` | §4 then first stage of size |
| `design` · `architect` · `impl-plan` · `develop` · `test` | `stages/<name>.md` on active task |
| `review <type> [target]` | `stages/review.md` |
| none | decision below |

No args — first match wins:
1. Repo has code, no `understanding.md` → `stages/onboard.md`.
2. Repo empty → ask what to build → §4.
3. `tasks/index.md` has rows not `✅` → list them (#, task, stage, status), ask which to resume — never pick for the user — → §5.
4. All done / no tasks → show index summary, ask: new task, review, or refresh onboard.

`[task#]` given → that task is active. None given + exactly one open task → that one; several → ask.

## 4. New task

1. Ask enough to size it, then propose size:

| Size | Signal | Stages |
|---|---|---|
| Fix | defect, known area | design (lite) → develop → test → review code |
| Change | small feature, ≤ few files, no new contract | design → impl-plan → develop → test → review code |
| Build | new feature/system/integration/API/data model | design → architect → review design+arch → impl-plan → develop → test → review test+code |

2. User confirms or overrides size.
3. NN = highest existing `tasks/NN_*` number + 1 (01 if none), zero-padded. Never reuse a number, even if a folder was deleted — check `index.md` rows too.
4. Create `tasks/NN_<kebab-slug>/`, design file from `templates/design.md`, add row to `tasks/index.md` (create from `templates/tasks-index.md` if missing).
5. Start first stage.

## 5. Resume

1. Read `tasks/index.md` → active task row.
2. Read design file `Status:` line.
3. `impl-tasks/ledger.md` exists → read `Next:` + `Blockers:`.
4. Load only the stage file for the current stage + the files that stage needs.
5. Tell user in ≤ 3 lines: task, stage, next step. Continue on confirmation.

If `understanding.md` commit SHA is ≥ 30 commits behind `HEAD` (`git rev-list --count <sha>..HEAD`), offer `onboard` refresh first.

## 6. Every stage

1. **Questions first.** One question per message. Anchor in specifics (a real scenario, a file, a failure). Play back understanding in short chunks; mark guesses `(assumption)`. User says "skip" → proceed on stated defaults, list them.
2. **Write** the stage's output into its file, per `rules/doc-style.md`.
3. **Approval.** Ask user to approve. Changes requested → revise, ask again. Next stage starts only after approval (G1).
4. **Record.** Update design `Status:` line, ledger (if any), `tasks/index.md` row (stage, status, date). Append one `Log` line.
5. **Hand off.** Name the next stage per size; user can jump or stop.

## 7. Domain packs

Task touches the domain → design + architect + review consult:
- CRM, leads, contacts, pipelines → `domains/crm.md`
- WhatsApp/SMS/voice bots, AI receptionists, conversational agents → `domains/voice-message-agents.md`
- Catalog, cart, checkout, orders, payments → `domains/ecommerce.md`
