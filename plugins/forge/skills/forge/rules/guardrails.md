# Guardrails (hard)

Apply every run, every stage. Project/user `CLAUDE.md` may relax **only G2 and G9**. Violating the letter = violating the spirit.

| ID | Do | Never |
|---|---|---|
| G1 | Ask questions → write approach → get explicit approval, then produce the stage output | Write code, docs or files for a stage before its approval |
| G2 | Leave changes unstaged; hand back a diff summary | `git add`, `commit`, `push`, `tag` — unless project rules allow |
| G3 | Let hooks run; fix what they flag | `--no-verify`, disabling hooks, bypassing CI |
| G4 | Use placeholders (`sk_test_xxx`, `user@example.com`, `+10000000000`) | Real secrets, tokens, customer data, PII in docs, code, examples, logs |
| G5 | Mark done only with evidence: command run + result recorded | Relax an assertion, skip/`.only` a test, mark ledger `✅` without `Verified by` |
| G6 | Ask before destructive ops; rethrow or enrich errors | `drop`, `truncate`, `reset --hard`, `rm -rf`, force-push, migrations on shared DBs without approval; silent `catch` |
| G7 | Report exactly: failure → paste output; unverified → say "not verified" | Claim success you did not observe |
| G8 | Smallest change per root cause; one root cause per edit | Drive-by refactors, scope creep, bundled unrelated fixes |
| G9 | Work inline | Spawn subagents — unless user asks (e.g. fresh-context reviewer) |

## Red flags — stop, re-read the table

- "Approach is obvious, I'll just write it" → G1
- "Test is flaky, skip it for now" → G5
- "I'll commit so the work isn't lost" → G2
- "Probably passes, ledger ✅" → G5, G7
- "While I'm here, let me clean this up" → G8
