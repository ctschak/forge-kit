# Stage: onboard

Project-level. Output: `<root>/understanding.md` + `<root>/health.md`. Templates: `templates/understanding.md`, `templates/health.md`.

## Steps

1. **Tell user** plan in 2 lines: deep read, then two docs, then AI-readiness, then stop. Read-only on code.
2. **Read in depth** — every row below covered before writing. Record `git rev-parse HEAD`.

| Area | Look at |
|---|---|
| Structure | top-level tree, workspaces/monorepo, module boundaries |
| Stack | manifests (`package.json`, `pyproject`, `go.mod`, `pom.xml`…), lockfiles, runtime versions |
| Entry points | servers, CLIs, workers, cron, serverless handlers, FE routes |
| Data model | schemas, migrations, ORM models, indexes |
| Integrations | 3rd-party SDK clients, webhooks in/out, queues |
| Auth | authn flow, session/token, authz checks, tenancy |
| Config/env | `.env.example`, config loaders, secrets handling |
| Build/deploy | scripts, Dockerfiles, CI, IaC, hosting |
| Tests | frameworks, dirs, how run, what's covered vs not |
| Conventions | naming, layering, error handling, logging |
| Existing docs | README, docs/, ADRs, CLAUDE.md |

3. **Ask** only what code can't answer: business purpose, users, current pain, roadmap, known incidents. Questions per SKILL.md §6.1 (batched, with defaults); "skip" accepted.
4. **Write `understanding.md`** — every template section filled or omitted; module map with real paths; main flows with entry `file:line`.
5. **Write `health.md`** — every finding has severity (high/med/low), `file:line`, why it matters, direction. Rank by severity. Cover: gaps, risks (security per `rules/security-checklist.md`, data loss, scale, single points of failure), tech debt, test coverage per area.
6. **Run** `stages/ai-readiness.md` → fills `## AI-assisted development` in `health.md`.
7. **Stop.** Summarize top 5 findings in chat (≤ 10 lines) + links to both docs. Ask user which direction: fix a finding (`/forge new`), start a feature, or refine docs.

## Done when

- Both docs exist, SHA recorded, every health row has severity + location.
- No code changed (G1, G8).

## Refresh (`/forge onboard` with existing docs)

Diff from recorded SHA (`git diff --stat <sha>..HEAD`), re-read changed areas, update affected sections, new SHA, append `Refreshed YYYY-MM-DD` line. Health: mark resolved rows `✅ resolved YYYY-MM-DD`, add new ones.
