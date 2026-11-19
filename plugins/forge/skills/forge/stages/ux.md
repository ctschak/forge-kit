# Stage: ux

UX spec + clickable HTML mockup for every spec that changes what users see or do (`ui: true`, `rules/contract.md` CT14). Runs inside the spec stage, before its approval point; approved together with the spec (one approval line covers both).

Files (task folder):
- `YYYY-MM-DD_<slug>_ux.md` from `templates/ux.md` — screens, states, copy, rules `U*`, usability script.
- `ux/<slug>-mockup.html` — the visual reference. UX spec text wins on conflict.
- Project once: `<docs root>/ux/ux-standards.md` from `templates/ux-standards.md` (shared rules; UX specs link, never repeat).

Not for: pure backend/infra/security specs → `ui: false` (or omit).

## Steps

1. **Read the shipped UI first** (match it; don't restyle): token file (CSS variables / theme), font + where it loads, icon set, layout shell (sidebar/topbar), existing component styles on the screens being changed. Record paths + commit in the mockup header comment.
2. **Standards**: create `ux/ux-standards.md` if missing (users + devices, foundations from step 1, breakpoints from existing CSS, states table, copy, accessibility WCAG 2.2 AA, evidence, usability protocol).
3. **UX spec** (`templates/ux.md`): tasks `T*` → screens `S*` (ASCII sketch only while drafting) → states per screen → interactions → copy that matters (exact strings) → accessibility → rules `U*`, each citing ≥ 1 spec `R*` → usability script with pass bars `(assumption)`.
4. **Mockup** — one self-contained `.html`, opens from disk, no build:
   - Tokens, font, icons and component styles copied from step 1, light + dark if the app has both.
   - Real-looking demo data in the domain's language; no real customer data.
   - Mockup controls bar (outside the product UI): state · role · theme · viewport. Mobile via container queries so it works on any screen.
   - Same switches as URL params (`?state=…&role=…&theme=…&view=…`) for review links and evidence.
   - Every screen and state in the UX spec reachable; primary interactions clickable; out-of-scope clicks show a toast naming the spec that owns them.
   - External assets only from the app's own CDNs/fonts; pinned versions.
5. **Self-check + screenshots**: render each screen and state × viewport (+ dark for the main screen) in a headless browser, look at the images, fix defects. Save PNGs to `ux/screens/<screen-or-state>.png` and embed each under its screen / in the States section of the UX spec, replacing ASCII sketches (no duplicate grids); spec embeds the main screen only. Report what was checked; say if no browser was available.
6. **Link**: spec gets `ui: true` and an R "UI implements `<ux file>` and `ux/<mockup>`" with an AC for UX evidence (CT14). UX spec header pins `Spec: SPEC-n @ rev N`.
7. Back to spec stage step 5 (validate) → approval point shows the mockup path and how to open it.

## Later

- Scope change in UX → UX spec revision line + spec CT8 if requirements change.
- Design stage cites `SPEC-n.U*` and mockup screens; review/test attach evidence per `ux-standards.md`.
