# forge-kit

Claude Code plugin marketplace. First plugin: **forge** — one skill that runs software work like a senior architect: understand → question → document approach → build in verified steps → review. Resumable across sessions via docs.

## Install

```
/plugin marketplace add ctschak/forge-kit      # or a local path to this repo
/plugin install forge@forge-kit
```

## Commands

| Command | Does |
|---|---|
| `/forge` | Existing code, no docs → onboard. Open tasks → list, resume chosen one. Empty repo → ask what to build. |
| `/forge new <desc>` | Size task (Fix / Change / Build), create task folder, start first stage |
| `/forge <stage> [task#]` | `design` · `architect` · `impl-plan` · `develop` · `test` · `review` |
| `/forge review <design\|arch\|test\|code> [target]` | Review task#, path, branch or PR |
| `/forge onboard` | Re-run codebase understanding + health |
| `/forge ai-readiness` | Audit missing AI-assisted-dev elements |

## Sizing

| Size | Stages |
|---|---|
| Fix | design (lite) → develop → test → review(code) |
| Change | design → impl-plan → develop → test → review(code) |
| Build | design → architect → review(design+arch) → impl-plan → develop → test → review(test+code) |

## Docs layout (in each project)

Default root `docs/forge/`. Override: add to project `CLAUDE.md`:

```
forge-docs: ~/path/outside/repo
```

```
<root>/
  understanding.md          ← how the system works (onboard)
  health.md                 ← gaps, risks, debt, coverage, AI-readiness
  tasks/
    index.md                ← all tasks + status
    01_<slug>/
      YYYY-MM-DD_<slug>_design.md
      impl-tasks/ledger.md, 01_<step>.md, 02_<step>.md …
      reviews/YYYY-MM-DD_<type>_review.md
```

## Reuse rules in your project

`plugins/forge/skills/forge/rules/` is the single source for guardrails, doc style, API, code, test and security standards. Point your project `CLAUDE.md` at them, or copy what fits. Project/user `CLAUDE.md` overrides forge defaults except hard guardrails.

## Layout

```
.claude-plugin/marketplace.json
plugins/forge/
  .claude-plugin/plugin.json
  skills/forge/  SKILL.md · rules/ · stages/ · domains/ · templates/
docs/specs/ · docs/plans/     ← design + build plan for forge itself
scripts/check.sh              ← structural checks
```

## License

MIT
