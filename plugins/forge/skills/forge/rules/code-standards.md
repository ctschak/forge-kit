# Code standards

Defaults. Project `CLAUDE.md` / linters / existing code win.

| ID | Rule |
|---|---|
| CS1 | Match surrounding code: naming, idiom, structure, comment density. |
| CS2 | Smallest change that fixes the root cause (see `rules/guardrails.md` G8). |
| CS3 | Types declared at boundaries (params, returns, config, API contracts). Typed langs: `unknown` + narrowing over `any`; no casts to silence the compiler. |
| CS4 | Errors: rethrow or wrap with context (`step X failed: <cause>`). Empty catch = bug. |
| CS5 | Config/env/URLs/credentials from config, never hardcoded. |
| CS6 | Delete dead code; no commented-out blocks. |
| CS7 | Validate input at the boundary; trust internal types after. |
| CS8 | Side effects (DB, network, queue) behind a seam that tests can replace. |
| CS9 | Idempotent handlers for retries: webhooks, queue consumers, payment ops. |
| CS10 | Log with request/correlation id; never log secrets or full PII. |
| CS11 | New behaviour behind a feature flag when the design says so; flag removal tracked. |
