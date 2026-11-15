# forge — design

Status: draft v2 for approval · 2026-11-14

## 1. Intent

One Claude Code skill, `forge`: carries any software work from vague idea → reviewed, tested code, like a senior full-stack architect. Understand first, question hard, write approach down, build in small verified steps, review. Survives multi-session work: new session resumes from docs, not chat memory.

Shared broadly: Claude Code plugin in own repo, installable into any project.

## 2. Goals

- **Questions before output** — every stage grills before producing.
- **Approach before build** — each stage writes decision, waits for approval.
- **Resumable** — ledger/status updated every step; `/forge` resumes.
- **One skill, many jobs** — single entry; stages load on demand.
- **Sized work** — small tasks skip unneeded stages.
- **Onboarding** — existing codebase → understanding doc + health doc.
- **AI-readiness** — find missing elements for AI-assisted dev.
- **Review** — design, architecture, test plan, code.
- **Reusable rules + guardrails** — one source, leveraged by every stage and by projects.
- **Domain depth** — CRM, AI voice/message agents, ecommerce.

## 3. Non-goals

- Separate subagents per role. Same Claude, stage playbooks.
- PM tool (tickets, estimates, assignment).
- Stack/framework lock-in.
- Dependency on other plugins.

## 4. Anti-goals

- Code/docs before approval.
- Long prose docs; walls of text.
- Resume that needs user to re-explain.
- Fake progress: ledger says done, verification never ran.
- Bloated SKILL.md loading every stage every run.

## 5. Packaging

Repo: `~/Documents/icloud-archive-folder-back-up/Documents/Projects/18_Agent_Skills/repos/forge-kit`

```
forge-kit/
  .claude-plugin/marketplace.json
  plugins/forge/
    .claude-plugin/plugin.json
    skills/forge/
      SKILL.md                  ← entry: routing, resume, sizing, points to rules
      rules/                    ← single source of truth, reusable
        guardrails.md           ← hard rules (never break)
        doc-style.md            ← concise, no grammar, tables, code-first
        api-standards.md        ← REST patterns, authn/z, errors, payments
        code-standards.md
        test-standards.md
        security-checklist.md
      stages/
        onboard.md
        ai-readiness.md
        design.md
        architect.md
        impl-plan.md
        develop.md
        test.md
        review.md
      domains/
        crm.md
        voice-message-agents.md
        ecommerce.md
      templates/
        design.md
        impl-task.md
        ledger.md
        review.md
        understanding.md
        health.md
        tasks-index.md
  docs/specs/                   ← this file
  CLAUDE.md                     ← maintainer rules
  README.md                     ← install, usage, how projects reuse rules/
  CHANGELOG.md
  LICENSE
```

SKILL.md target < 150 lines; everything else loads only on its branch.

## 6. Invocation

| Command | Behaviour |
|---|---|
| `/forge` | No `understanding.md` + existing code → onboard. Empty repo → ask what to build. Else → show tasks index, resume chosen task at ledger's next step. |
| `/forge new <desc>` | Size task, create task folder, start first stage. |
| `/forge <stage> [task#]` | Run stage explicitly: `design`, `architect`, `impl-plan`, `develop`, `test`, `review`. |
| `/forge review <design\|arch\|test\|code> [target]` | Review; target = task#, path, branch, or PR. |
| `/forge onboard` / `/forge ai-readiness` | Re-run project-level stages. |

## 7. Doc locations + naming

- Root default: `docs/forge/` in project repo.
- Override: project `CLAUDE.md` line `forge-docs: <path>` (outside-repo once project matures).
- Neither + first write → ask once, offer to add line.

```
<root>/
  understanding.md
  health.md
  tasks/
    index.md                                  ← all tasks: #, name, size, stage, status
    01_lead-dedupe/
      2026-11-14_lead-dedupe_design.md
      impl-tasks/
        ledger.md
        01_add-dedupe-index.md
        02_merge-service.md
        03_api-endpoint.md
      reviews/
        2026-11-15_design_review.md
        2026-11-20_code_review.md
    02_whatsapp-voice-handoff/
      ...
```

Naming rules:
- Task folder: `NN_<kebab-slug>` — 2-digit, next free number, never reused.
- Design file: `YYYY-MM-DD_<slug>_design.md`.
- Impl step: `NN_<kebab-slug>.md`, numbered in execution order.
- Review: `YYYY-MM-DD_<type>_review.md`; re-review appends dated section, never overwrites.

## 8. Resume model

- `tasks/index.md` → which tasks exist, stage, status.
- Design doc header `Status:` line → stage progress.
- `impl-tasks/ledger.md` → per-step progress.
- Every step completion updates ledger + index. New session: read index → ledger → only the file needed.

**ledger.md**
```
| # | Step | Status | Verified by | Updated |
|---|---|---|---|---|
| 01 | add-dedupe-index | ✅ done | migration up/down ran, test X green | 2026-11-16 |
| 02 | merge-service | 🔄 in progress | — | 2026-11-17 |
| 03 | api-endpoint | ⬜ not started | — | — |

Next: 02 — finish merge conflict rules (see 02_merge-service.md §Steps 3)
Blockers: none
Log:
- 2026-11-17 — 02 started; open Q: keep oldest owner?
```
Status values: `⬜ not started` · `🔄 in progress` · `✅ done` · `⛔ blocked`. `done` requires "Verified by" filled.

## 9. Sizing

| Size | Example | Stages |
|---|---|---|
| Fix | defect | design (lite: problem, root cause, before/after, tests) → develop → test → review(code) |
| Change | small feature | design → impl-plan → develop → test → review(code) |
| Build | feature / system / integration | design → architect → review(design+arch) → impl-plan → develop → test → review(test plan+code) |

forge proposes; user overrides.

## 10. Rules + guardrails (`rules/`)

Single source; stages point here, never restate. README explains projects can copy/reference these from their own `CLAUDE.md`. Project/user `CLAUDE.md` overrides non-hard rules.

**guardrails.md (hard — always apply):**
1. No code/doc output for a stage before its questions + approval.
2. No commit/push/stage unless project rules allow.
3. No `--no-verify`, no skipped hooks.
4. No secrets, tokens, real customer data in docs, code, examples.
5. No fake pass: never relax assertion, skip test, or mark ledger done without verification evidence.
6. No silent catch; no destructive commands (drop, reset --hard, rm -rf) without explicit approval.
7. Report honestly: failure → paste output; unverified → say so.
8. Stay in scope: smallest change per root cause; no drive-by refactors.
9. No subagents unless user asks.

**doc-style.md:** concise, skip grammar, bullets/tables over prose, table for 3+ comparisons, code over description, every section earns its place, `file:line` refs.

**api-standards.md:** see §12.

**code-standards.md:** match surrounding code; declared types at boundaries; no dead code; config not hardcoded.

**test-standards.md:** no skips/only, no sleeps (wait on state), fail fast, stable selectors in POM, one assertion intent per test, deterministic data.

**security-checklist.md:** authn, authz/tenant isolation, input validation, output encoding, secrets mgmt, PII handling/logging, rate limits, CSRF/CORS, webhook signature verification, dependency risk, audit log.

## 11. Stages

### onboard (project-level)
- Trigger: `/forge` with no `understanding.md` + non-empty codebase, or `/forge onboard`.
- Deep read: structure, modules, entry points, data model, integrations, auth, config/env, build/deploy, tests, conventions.
- Asks only what code can't answer (business context, users, roadmap, pain).
- `understanding.md`: overview, main flows, module map w/ paths, data model, integrations, key decisions, conventions, git SHA.
- `health.md`: gaps, risks, tech debt, test coverage — severity, `file:line`, why, direction.
- Runs ai-readiness. Stops; user picks direction.
- Later `/forge`: many commits since SHA → offer refresh.

### ai-readiness
Finds **missing** elements for AI-assisted dev:

| Element | Checks |
|---|---|
| `CLAUDE.md`/`AGENTS.md` | exists, accurate, lean; stack, commands, conventions, no-go areas |
| Project skills | repeated workflows that deserve a skill |
| Guardrails | git, test, secrets, protected paths |
| Rules/conventions | written where agent reads them |
| Hooks | lint/format/typecheck/test; block dangerous cmds |
| Permissions | settings allowlist/denylist |
| Feedback loops | one-command typecheck/lint/unit test |
| MCP/tools | needed integrations configured |
| Agent-facing docs | understanding doc, glossary, ADRs reachable |

Output: `## AI-assisted development` in `health.md`, ranked by impact. Drafts fixes only after approval.

### design → `NN_<slug>/YYYY-MM-DD_<slug>_design.md`
Template sections (omit what size doesn't need):
```
# <title>
Status: <stage> · <state> · <date>
## Problem          ← what's broken/missing, who hurts, evidence
## Solving exactly   ← 1–3 bullets: the precise outcome
## Requirements      ← functional / non-functional, numbered (R1, R2…)
## Scope             ← in / out
## Use cases         ← UC1: actor → action → result
## Approaches        ← A/B/(C): table pros/cons → recommendation
## High-level design ← components, flow diagram (mermaid), data flow
## Detailed design   ← per component; code examples:
##                      defect → before vs after
##                      new impl → code snippet
## API design        ← if any (§12)
## Security          ← from security-checklist, task-specific
## Feature flags     ← flag name, default, rollout, kill-switch, cleanup
## Test coverage     ← levels, cases mapped to R#/UC#
## Open questions
```
Design stage owns Problem → Use cases. Domain packs consulted.

### architect (Build size)
Owns Approaches → Feature flags in same design doc: system shape, data model, contracts, integrations, scalability, failure modes, observability, migration/rollout. Reads `understanding.md`; stays consistent with existing conventions.

### impl-plan → `impl-tasks/`
- Splits approved design into ordered steps; each step file:
```
# NN <step>
Design ref: §Detailed design / R2
Goal:
Files: path/a.ts, path/b.ts
Steps: 1… 2… 3…
Code: before/after or snippet
Verify: command + expected result
Done when:
```
- Creates `ledger.md` all `⬜`. Updates `tasks/index.md`.

### develop
- Execute ledger in order: step → verify → update ledger (`Verified by`) → next.
- Deviations from design → note in step file + ask if material.
- Updates `understanding.md` when system structure changes.

### test
- Test plan from design §Test coverage; implement per test-standards; run; record results in ledger.

### review → `reviews/YYYY-MM-DD_<type>_review.md`
| Type | Reviews against |
|---|---|
| design | problem clarity, requirements testable, scope, use cases, approach choice justified |
| arch | scalability, failure modes, data model, security, flags, consistency w/ understanding.md, domain pack |
| test | coverage vs R#/UC#, levels, negative/edge cases, test-standards |
| code | correctness, design conformance, security-checklist, code-standards, tests present + green |

Findings: `| # | Severity | Where (file:line / §) | Issue | Fix |`, ranked. Verdict: approve / changes needed. Re-review appends dated section. Optional fresh-context reviewer subagent only when user asks.

## 12. API standards (`rules/api-standards.md`)

Every API in a design must document:

| Item | Content |
|---|---|
| Endpoint | `METHOD /v1/<plural-resource>/{id}/<sub>` |
| Authn | scheme (Bearer JWT / OAuth2 / API key / session cookie), where validated |
| Authz | role/scope required, tenant/ownership check |
| Headers | `Authorization`, `Content-Type`, `Idempotency-Key`, `X-Request-Id`, custom |
| Cookies | name, `HttpOnly`/`Secure`/`SameSite`, purpose (if any) |
| Path params | name, type, validation |
| Query params | filter, sort, `limit`/`cursor` pagination, defaults, max |
| Request body | schema + example |
| Response | status + schema + example |
| Errors | each case: status, code, example body |
| Rate limit | limit + `429` behaviour |

REST patterns: plural nouns, no verbs in path; GET/POST/PUT/PATCH/DELETE semantics; 201 + `Location` on create; 204 on empty; cursor pagination; versioned path `/v1`; consistent error body (RFC 9457 `application/problem+json`): `{type, title, status, detail, code, errors[]}`.

Status codes: 400 validation · 401 unauthenticated · 403 forbidden · 404 not found / not owned · 409 conflict · 422 business rule · 429 rate limit · 5xx server.

Payments: `Idempotency-Key` required on create; amounts integer minor units + ISO currency; no card data stored (PSP token only); webhook signature verified + replay window; state machine (`pending → authorized → captured | failed | refunded`). Example payload set lives in `api-standards.md`.

## 13. Domain packs

- **crm:** lead/contact/account model, dedupe, ownership/assignment, pipeline, activity timeline, multi-tenancy, permissions, imports, audit.
- **voice-message-agents:** channels (WhatsApp/SMS/voice), latency budgets, STT/TTS/LLM pipeline, barge-in, human handoff, conversation state, consent/opt-in, template approval, cost/conversation, evals.
- **ecommerce:** catalog/variants, inventory, cart/checkout, payments+idempotency, orders/fulfilment, returns, tax, promotions, search, peak traffic.

## 14. Calls made by me (check)

- Name `forge`; repo `forge-kit` hosting plugin `forge`; path `18_Agent_Skills/repos/`.
- Naming: folder `NN_<slug>`, design `YYYY-MM-DD_<slug>_design.md` (your `xxxxxx_xx_design.md` read as date_slug).
- `ledger.md` inside `impl-tasks/` (per your layout); stage progress via design doc `Status:` line + `tasks/index.md`.
- Added `tasks/index.md` so `/forge` can resume across multiple tasks.
- Architect kept as stage but writes into same design doc (no separate arch file).
- Reviews in `reviews/` under task folder; re-review appends.
- AI-readiness = section in `health.md`.
- One question per message during grilling; "skip" proceeds on defaults.
- forge standalone; owns process while running even if superpowers installed.
- License MIT.

## 15. Left to builder

- Exact SKILL.md wording + description triggers.
- Template detail beyond section lists.
- Domain checklist and payment example detail.
- Evals (skill-creator) v1 or later.

## 16. Build order

1. Repo scaffold, manifests, README, CLAUDE.md, LICENSE.
2. `rules/` (guardrails first) + SKILL.md + templates.
3. onboard + ai-readiness → dogfood on Leadly.
4. design, architect, impl-plan stages.
5. develop, test, review stages.
6. Domain packs.
7. Dogfood one Build-size task end-to-end on Leadly; fix; v0.1.0.
