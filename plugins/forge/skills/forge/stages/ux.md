# Stage: ux

HTML prototype + real screenshots + spec `## UX` for a spec that changes what users see or do (`ui: true`). Rules: `rules/ux.md` (UX1–UX5) · contract CT14. Runs inside the spec stage, before its approval point; one approval covers both.

Files (task folder, N = spec revision):
- `ux/rev-N/index.html` — self-contained prototype, opens from disk.
- `ux/rev-N/screens/<screen>-<viewport>-<state>.png` — actual browser screenshots of the prototype.
- Project once: DESIGN.md (or equivalent); none → `<docs root>/ux/ux-standards.md` from `templates/ux-standards.md`.

## Steps

1. **Read the shipped UI first** (UX2 — match it, don't restyle): tokens / theme file, font + where it loads, icon set, layout shell, component styles on the screens being changed. Record paths + commit in an HTML comment at the top of the prototype.
2. **Standards**: DESIGN.md / `ux-standards.md` missing → create from step 1 (users + devices, foundations, breakpoints from existing CSS, states, copy, accessibility, evidence).
3. **Prototype** `ux/rev-N/index.html`:
   - Tokens, font, icons, component styles from step 1; light + dark if the app has both.
   - Demo data in the domain's language; no real customer data (UX5).
   - Controls bar outside the product UI: state · role · theme · viewport; same switches as URL params.
   - Every screen and state listed in `## UX` reachable; primary interactions clickable; out-of-scope clicks show a toast naming the spec that owns them.
4. **Screenshots**: open each screen × state × viewport (+ dark) in a headless browser via the URL params, save to `screens/`, look at each image, fix layout defects, check console errors. No browser available → say so, give the capture command, leave image links out (never a path to a file that doesn't exist).
5. **`## UX` in the spec** (`templates/spec.md`): prototype link · screens `S*` with images · states · exact copy · UX rules `U<n>` each citing ≥ 1 `R`. Add front matter `ui: true`.
6. Back to spec stage step 5 (validate — CT14 checks the links and `U*` citations) → approval point shows prototype path + screenshots.

## Later

- Feedback that changes scope → spec revision +1 (CT8) → new `ux/rev-N+1/`; never overwrite an approved revision's files.
- Design cites `SPEC-n.U*` and `S*`; test captures implementation screenshots under `ux/verification/rev-N/` (UX4); review checks UI vs `U*`.
