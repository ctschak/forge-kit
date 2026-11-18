# Quality gate

Applies in test + review stages. Project tools, CI and `CLAUDE.md` policy win; these are defaults. Detection: `scripts/quality_detect.py <repo>`. Language/DB specifics: `rules/profiles/<profile>.md` — load only the profiles detection returns.

| ID | Rule |
|---|---|
| QG1 | **Relevant checks.** Run lint / type / format for changed languages and the tests covering changed code. Deep path or change to a shared module (used by ≥ 3 callers, public API, schema) → also the broader regression suite. |
| QG2 | **Evidence.** Each check run → ledger line `check <name>: <command> → exit <n>, <counts>` (e.g. `12 passed, 0 failed`). Paste the first failing line on failure (G7). |
| QG3 | **Unrun is reported.** Detected but not run → `not run: <reason>` (tool missing, deps not installed, needs CI/service). Never omitted, never claimed. |
| QG4 | **Never weaken gates.** No disabling rules, raising thresholds, `--no-verify`, skips (G3, G5). Fix only findings on changed lines/behavior; pre-existing issues → `health.md`, not this task (G8). |
| QG5 | **Missing tooling.** Propose the smallest config the project needs (one tool per kind), versions chosen from the project's runtime and the tool's official docs at that moment — never from memory. Install only with approval; don't add a tool that duplicates an existing one. |
| QG6 | **Coverage.** Project policy wins. Else, when coverage tooling exists: changed-line coverage target 80% (`forge-coverage: <n>` overrides). Below target → review finding (medium), not a reason to test trivial lines. Measure with `scripts/changed_coverage.py --report <lcov|cobertura> --base <ref> --target <n>`. No tooling → `not measured`. |
| QG7 | **Tests prove behavior.** Every spec AC has a test that fails if the behavior breaks; add unit / integration / e2e by risk (TS10). Never write tests only to raise coverage. |
| QG8 | **Failures are findings.** Failed check on changed code → review finding (static perspective) → fix loop (`stages/review.md`). Flaky (passes on rerun without change) → note it, don't hide it. |
