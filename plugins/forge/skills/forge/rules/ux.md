# Code-first UX (default; no external design provider required)

The goal is fast product validation, not another design ceremony. Use this rule for customer-facing work and PRD baselines. Load only when useful.

## UX1 — Choose automatically

- No visible UI change: skip, with one-line reason if relevant.
- Small UI change: use existing components and browser validation; an implementation screenshot is sufficient if a separate mockup adds no value.
- New screen, material workflow change, or new product: generate an interactive HTML prototype before spec approval. One representative prototype per coherent journey, not per requirement.
- New screen / material workflow / new product → spec front matter `ui: true`; the validator then checks `## UX` (`rules/contract.md` CT14). Small or no UI change → omit `ui`.
- A user can request a prototype or screenshots at any time. Figma and other tools are optional inputs only, never required.

## UX2 — Generate and share

Inspect existing UI, brand, design tokens, component library, screenshots and responsive behavior first. Reuse them; do not silently redesign the entire application or introduce a new framework. For greenfield work, define minimal reusable tokens and conventions. Record durable design rules in project DESIGN.md (or the existing equivalent); none → `<docs root>/ux/ux-standards.md` from `templates/ux-standards.md`. Keep it concise; specs reference it, never duplicate it.

Save artifacts next to the spec, under `ux/rev-N/`:
- `index.html`: locally openable, self-contained HTML/CSS/JS prototype, with representative synthetic data and functional interactions needed to demonstrate the journey. Prototype controls bar outside the product UI (state · role · theme · viewport) with the same switches as URL params (`?state=…&role=…&theme=…&view=…`) so screenshots and review links are reproducible. No production API calls, credentials, real customer data, trackers, external CDNs or deployment. If a prototype genuinely requires a local server, include exact run instructions.
- `screens/<screen>-<viewport>-<state>.png`: actual browser screenshots of the prototype, not AI illustrations or placeholder image paths. Use desktop and mobile for responsive screens and additional key states when relevant.
- Only if needed, a concise README for run instructions or interaction details not obvious in the prototype.

Use available browser automation (prefer existing Playwright setup) to open the HTML, exercise key interactions, capture actual screenshots, check console errors, basic keyboard/accessibility and responsive layout. Never claim checks or screenshots succeeded without evidence. If browser tooling is unavailable, deliver the HTML, say screenshots are blocked, provide exact capture instructions, and request user input only when visual validation is material to approval. Do not install tooling or publish artifacts without applicable authorization.

In the spec, add `## UX` (`templates/spec.md`): link to the HTML; screens `S*`; states that apply (loading, empty, error, no permission); exact copy that carries meaning; UX rules `U<n>` each citing ≥ 1 `R`; inline Markdown images with paths relative to the spec. Caption each image with the screen/state, viewport, source (prototype, not shipped), and relevant R/AC IDs. Example:

```markdown
[Open interactive HTML prototype](ux/rev-1/index.html)

![Proposed onboarding — desktop, connection pending](ux/rev-1/screens/onboarding-desktop-pending.png)

Prototype · rev 1 · R1, AC1 · 1440×900
```

Share the document path, HTML path and screenshots in the existing spec approval summary; offer a local browser preview when available. Treat feedback as spec clarifications or scope changes under CT8. No extra mandatory approval gate. Preserve revision-specific artifacts; do not overwrite an approved visual baseline. Scope-changing feedback increments the spec revision and invalidates affected design/plan work. Keep assets in the project docs root, not the Forge Kit marketplace itself; respect privacy and project storage rules.

## UX3 — Baseline PRD and release

Embed actual screenshots of existing behavior in the relevant PRD FEAT section, using relative Markdown paths and concise captions with source environment, date, evidence and viewport. Store captures under `ux/baseline/` or `releases/vX.Y.Z/ux/` relative to the docs root. Use safe local/demo accounts and synthetic or redacted data. A prototype is never evidence of released behavior. If current screens cannot be exercised, state why and omit the image rather than fabricate it. When explicitly useful, a separate baseline HTML demo may be linked and labelled illustrative; it is not proof of current functionality.

Planned screenshots live only in the associated spec; the living PRD can link to a spec as a separate roadmap reference only if explicitly requested and clearly labelled, never as a released FEAT. At confirmed release, link verified implementation screenshots in the updated PRD FEAT and retain the spec prototype history.

## UX4 — Engineering and verification

Design reads the approved spec revision's UX references and DESIGN.md. Treat screenshots as visual intent and R/AC as behavior authority; discrepancies require clarification, not guesses. Reuse application components and production architecture rather than copying prototype HTML blindly. Check relevant loading, empty, error, success, permission, keyboard and responsive states. Build only approved scope.

During test, capture actual implementation screenshots using equivalent viewports/states, store under task `ux/verification/rev-N/`, and link from the existing ledger/readiness evidence. Compare to approved visuals with functional checks and accessibility checks; avoid pixel-perfect requirements unless specified. Record meaningful deviations and resolve blockers or obtain explicit acceptance. No new test framework for trivial changes when existing browser tools suffice.

## UX5 — Guardrails

HTML and images are optional contract artifacts, not mandatory new documents. Use narrow representative coverage and reuse approved artifacts. Never expose secrets, private customer data or confidential screenshots; never upload to an external design provider by default. Follow existing hard guardrails, approval rules and Git restrictions. Report missing browser access, unavailable screens, and unverified behavior explicitly.
