# forge evals

Behavioural regression demos for the forge skill: realistic scenarios run in fresh headless Claude Code sessions, scored against written pass criteria. Unit tests for the scripts live in `tests/` (run by `scripts/check.sh`); these evals check how the skill *behaves*.

```
evals/
  scenarios/   index.md (all scenarios: variant, user turns, criteria) · D1, D3 fact sheets
  fixtures/    projapp (Python + sqlite, approved SPEC-1, planted pagination bug) · webapp (TS, project lint script) · shelftrack (evidence only) · inputs/ (external PRD, journey report)
  harness/     setup.sh · snapshot.sh · turn.sh · interrupt_after.py
  results/     one file per run date / slice
```

## Run one scenario

```bash
W=$(mktemp -d)                                         # keep runs outside the repo
bash evals/harness/snapshot.sh $W/v                    # forge under test (working tree; add a git ref for a baseline)
bash evals/harness/setup.sh projapp $W/run             # fixture variant from scenarios/index.md
bash evals/harness/turn.sh $W/run $W/v/forge "/forge:forge SPEC-1"
bash evals/harness/turn.sh $W/run $W/v/forge "Approve."   # next turn resumes the same session
```

Each turn appends to `<run>/.log.md` (`secs`, `cost`, reply). Count questions, docs (`git status docs`), turns and seconds; re-validate artifacts with `plugins/forge/skills/forge/scripts/spec_check.py` before scoring.

## Notes

- Isolation: `--setting-sources project` loads only the plugin under test (your user `~/.claude/CLAUDE.md` still loads — same for every run). `--allowedTools` lets the agent run `python3`, `npm`, `node`, `npx` without prompts; everything else is denied, as a cautious user would.
- Cost: most turns $0.3–1.5; the independent-review scenario (Q8) ≈ $9 total — set `FORGE_EVAL_BUDGET=6`.
- Fixtures need no network. The webapp's `typecheck` script needs `npm install` (tsc) — without it, forge must report typecheck as `not run`.
