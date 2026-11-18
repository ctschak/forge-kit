# Profile: JavaScript / TypeScript

Loaded when detection returns `js-ts`. Existing project tools and scripts win (`rules/quality.md` QG4, QG5).

| Kind | Prefer existing | Default if absent (propose, QG5) |
|---|---|---|
| lint | `npm run lint` / ESLint config | ESLint flat config + `typescript-eslint` recommended |
| type | `npm run typecheck` | `tsc --noEmit` with `strict` |
| format | Prettier / Biome config | Prettier `--check` (only if team wants a formatter) |
| test | Jest / Vitest / `node --test` / framework runner | runner already in deps; else `node --test` for libraries |
| browser | existing Playwright / Cypress | Playwright only for critical user journeys (TS10) |

Review focus (static + functional perspectives):

| ID | Check |
|---|---|
| JS1 | Async: every promise awaited or handled; no floating promises; errors wrapped with context (CS4); no `async` in `forEach`. |
| JS2 | Boundaries: external input (HTTP, env, storage, `JSON.parse`) validated at the edge (schema or guard); typed as `unknown` until narrowed — no `any`, no `as` to silence errors (CS3). |
| JS3 | Contracts: exported functions/components declare return types; API request/response types shared or generated, not duplicated by hand. |
| JS4 | Resources: listeners, timers, subscriptions, AbortControllers cleaned up (UI unmount, request cancel). |
| JS5 | UI: loading / empty / error states present; accessible names, labels, keyboard reach for changed controls; no layout shift on state change. |
| JS6 | Dependencies: new package justified (size, maintenance, licence); lockfile updated; no duplicate of an existing dep. |
| JS7 | Security: no `innerHTML` / `dangerouslySetInnerHTML` with untrusted data; secrets never in client bundle (SEC5, SEC6). |
