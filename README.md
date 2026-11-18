# forge-kit

Claude Code plugin marketplace. First plugin: **forge** — one skill that takes work from idea to verified software: decide whether to build → validated spec → design → build in verified steps → review. Forge works out the next step from the docs and runs it, stopping only for decisions and approvals. Resumable across sessions.

## Install

```
/plugin marketplace add ctschak/forge-kit      # or a local path to this repo
/plugin install forge@forge-kit
```

## Use

Just describe the work, or run `/forge:forge` to continue where you left off.

| Command | Does |
|---|---|
| `/forge:forge` | Continue: shows `task · path · done → next` and runs the next step. Existing code, no docs → onboard first. |
| `/forge:forge <request>` or `new <desc>` | Pick a path, create the task, start discover (or spec for fast) |
| `/forge:forge <step> [task#]` | Expert override: `discover` · `spec` · `design` · `architect` · `impl-plan` · `develop` · `test` |
| `/forge:forge review <spec\|design\|arch\|test\|code> [target]` | Review task#, path, branch or PR |
| `/forge:forge onboard` · `ai-readiness` | Codebase understanding + health · AI-assisted-dev audit |

## Paths

| Path | When | Steps | Approvals |
|---|---|---|---|
| fast | clear, reversible, low-risk | spec → develop → test → review | spec |
| standard | feature | discover → spec → design → impl-plan → develop → test → review | spec · design |
| deep | uncertain, irreversible, security / cross-system | discover → spec → design → architect → reviews → impl-plan → develop → test → review → rollout | spec · design+arch · plan · rollout |

Old sizes Fix / Change / Build still work (= fast / standard / deep).

## Spec contract

Each task has one spec (`SPEC-<n>` = task number) that engineering builds from without restating it: objective with success/failure criteria, scope, non-goals, requirements `R`, measurable acceptance criteria `AC`, plus users, KPIs, telemetry and priorities on standard/deep. Status: proposed → approved → implemented → verified → released, or dropped ("don't build"). Rules: `plugins/forge/skills/forge/rules/contract.md`. Validator:

```
python3 plugins/forge/skills/forge/scripts/spec_check.py check <spec.md> [--require-approved] [--rev N]
```

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
      YYYY-MM-DD_<slug>_spec.md      ← SPEC-<n>
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
docs/                         ← designs + build plans for forge itself
evals/                        ← demo scenarios + results
tests/spec_check/             ← validator tests
scripts/check.sh              ← structural checks + validator tests
```

## License

MIT
