# Stage: ai-readiness

Finds what's **missing** for AI-assisted development in this project. Output: `## AI-assisted development` section in `<root>/health.md` (create `health.md` from `templates/health.md` if run standalone).

## Checklist — assess every row

| Element | Look at | Present when |
|---|---|---|
| `CLAUDE.md` / `AGENTS.md` | repo root, nested dirs | exists, matches code, < ~200 lines, states stack, run/test/build commands, conventions, no-go areas |
| Project skills | `.claude/skills/`, plugins | repeated workflows (deploy, migration, release, test-writing, data fix) have a skill |
| Guardrails | CLAUDE.md, hooks, settings | git policy, test rules (no skips/fake passes), secrets handling, protected paths written down |
| Rules / conventions | CLAUDE.md, linked docs | coding standards, architecture boundaries, naming reachable by pointer |
| Hooks | `.claude/settings*.json` `hooks` | format/lint/typecheck on edit; dangerous commands blocked |
| Permissions | `.claude/settings.json` | safe commands allowlisted; destructive denied |
| Feedback loops | package scripts, Makefile | typecheck, lint, unit tests each runnable by one command, fast |
| MCP / tools | `.mcp.json`, settings | integrations the work needs (DB, browser, tracker) configured |
| Agent-facing docs | docs/, ADRs, glossary | architecture/understanding doc, glossary, decisions reachable from CLAUDE.md |
| Secrets hygiene | `.gitignore`, `.env*` | `.env` ignored, `.env.example` present, no secrets committed |

## Steps

1. Assess each row: `present` / `weak` / `missing` + evidence (path).
2. Rank gaps by impact on agent output quality: high (agent will make wrong changes), med (slower / more prompting), low (polish).
3. Write rows into the health section table, with a concrete recommended addition per gap (e.g. "CLAUDE.md: add `pnpm test:unit` command + 'never edit generated/`").
4. Offer drafts for top gaps (CLAUDE.md, skill stub, hook config, settings allowlist). Write them only after approval (G1).

## Done when

Every checklist row assessed with evidence; every non-`present` row has a recommendation.
