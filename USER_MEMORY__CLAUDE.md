# Recommended user memory for forge (`~/.claude/CLAUDE.md`)

Generic working rules that fit forge's lifecycle. **Optional:** copy the sections you want into your own `~/.claude/CLAUDE.md` (user memory, applies to every project). forge's setup asks before adding anything; it never writes this file without your consent. Project `CLAUDE.md` / `AGENTS.md` win on conflict.

---

# Global working rules

**In all interactions and commit messages, be extremely concise. Sacrifice grammar for the sake of concision.**

Applies to every project. Repo `CLAUDE.md` wins on conflict.
Guardrails below are not situational — apply every time, unprompted.

## 1. Claude Code specifics

- **Load the matching skill first.** Before working an area that has one, invoke it. Area skill overrides generic skill. Don't work from memory when a skill exists.
- **Plan before code.** Anything beyond a trivial edit: approach first, wait for go-ahead. Use plan mode for multi-file work.
- **No subagents for fix/validation.** Read, code, verify inline. Subagents start cold, re-derive context already here, burn tokens. Only on explicit ask.
- **Use file tools, not shell.** Read/Grep/Glob over `cat`/`grep`/`sed`. Batch independent calls in one block.
- **Don't re-read a file to verify an edit.** Edit errors if it failed.
- **Report honestly.** Test failed → say so, paste output. Step skipped → say so. Done and verified → state it plainly, no hedging.

## 2. How to answer me

| Do | Don't |
|---|---|
| Lead with the answer, then the why | "Great question — let me look into…" |
| Table when comparing 3+ things | Paragraph listing them |
| "TC013 fails: `.x` no longer in FE" | "There appear to be some issues" |
| Paste the actual error line | "The test failed" |
| State the assumption and carry on | Stop and ask what you could assume |
| One root cause per edit, verify, next | Bundle 3 fixes into one change |
| Probe first (`console.log`, `page.evaluate`), confirm, then fix | Guess-patch and re-run hoping |
| Say "I couldn't verify X" | Present a guess as fact |

A follow-up question from me ≠ you got it wrong. Answer it; don't re-audit what you already said.
Long answer is fine when the content needs it. Padding is not.

## 3. Git

**Never commit.** No `git commit`, `git push`, `git add`. Don't stage. Finish → summarise → hand back. "Commit this" = present the diff, I run it.

**No `--no-verify`.** Never skip hooks.

**No AI attribution.** Drop the trailer block — no `Co-Authored-By: Claude…`, no `Claude-Session:`, no `🤖 Generated with…`, in commits or PR bodies. Subject + body, nothing appended.

## 4. Code quality — generic

- Match surrounding code: naming, idiom, comment density. Don't import a foreign style.
- Smallest change that fixes the stated root cause. No drive-by refactors.
- No silent catch. `catch(() => {})` is banned. Rethrow, or throw richer: `catch(e) { throw new Error('step X failed: ' + e.message) }`.
- No hardcoded env URLs, credentials, or absolute paths in committed code.
- Delete dead code rather than commenting it out.

## 5. TypeScript

Apply to new code. Don't retrofit an existing codebase without asking.

- **Declare return types** on top-level module functions. Exception: components returning JSX.
- **`unknown` over `any`.** Narrow with type guards. No `as` casts or `!` to silence the compiler — that's hiding a bug, same as relaxing an assertion.
- **Avoid `enum`** — union type or `as const` object. Enums are nominally typed, numeric ones emit reverse mappings, not erasable syntax. Leave existing enums alone unless asked.
- **`satisfies`** to check an object literal without killing inference. Not `:`, which widens.
- **Let inference work.** Annotate boundaries (params, return types, config). Don't annotate what TS already knows.
- **Discriminated unions** over optional-flag bags. Illegal states unrepresentable.
- **`import type` / `export type`** for type-only imports.
- **Generics only for a real input→output relationship.** Not for its own sake.

**tsconfig baseline:** `strict` · `noUncheckedIndexedAccess` · `noImplicitOverride` · `skipLibCheck` · `esModuleInterop` · `isolatedModules` · `verbatimModuleSyntax` · `moduleDetection: force` · `target: es2022`.

Flag when a repo undercuts this — e.g. `noImplicitAny: false` alongside `strict: true` cancels part of strict.

## 6. Test automation — hard rules

1. **No fake passes** — never relax an assertion to hide a real failure. `expect(true).toBe(true)` is not a test.
2. **No skips** — no `.skip`, no `.only`. Fails with a specific actionable error, or it isn't there.
3. **No `waitForTimeout` / `sleep`** — `locator.waitFor({ state })`, `expect.poll`, or a network-settled helper.
4. **Fail fast** — fail on first problem. No stacked retries or long polls papering over a slow env. Retries are for network flakes only; a locator miss gets 0 retries and a fixed selector.
5. **No label/text selectors** — copy changes, they rot. Priority: stable CSS class → `data-testid` → exact `aria-label` → `id` → role+exact name. Never body-text regex to detect page state.
6. **Selectors live in the POM**, never inline in specs. Verify against the FE repo before writing one.
7. **No speculative popup handlers** — only when the flow is known to trigger that popup.
8. **No unrelated files** in a test repo.

Before editing a shared/public method: list every caller first, run the full affected suite after.

## 7. Where output goes

Test repos hold test code and test data. Design/analysis/planning docs go to the project's designated docs location — forge uses `forge-docs:` in the project `CLAUDE.md` (default `docs/forge/`). When in doubt, not in the test repo.

Per-project output locations (design docs, review artifacts) belong in **your own** copy of this section, e.g.:

| Output | Path |
|---|---|
| Design / analysis / status docs | `<your docs folder>/designs/` |
| MR/PR review artifacts | `<your docs folder>/designs/pr-reviews/` |

Naming: designs `<YYYY-MM-DD>-<slug>.md` · reviews `<YYYY-MM-DD>-mr<iid>-<slug>-review.md`. Re-review appends a dated section; never overwrite.
