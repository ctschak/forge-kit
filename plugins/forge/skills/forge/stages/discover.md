# Stage: discover

Decide **whether and what** to build before anyone specs it. Output goes into the task's spec file (`templates/spec.md`, status `proposed`): `## Objective`, `## Users and value`, `## Evidence and assumptions`, and a recommendation. Rules: `rules/contract.md` CT5, CT6.

Read first: the request; supplied files (briefs, feedback, data); `understanding.md` if present; code when the request touches existing behavior; matching `domains/*.md` (SKILL.md §7).

## Steps

1. **Sort what's known** — every claim is one of:

| Kind | Mark | Example |
|---|---|---|
| verified | source + date, or `file:line` | "38% of tickets are scanning (evidence.md, 2026-11-01)" |
| assumption | `(assumption)` + how to test | "tutors lose ~2 lessons/month (assumption: founder's own count)" |
| proposed | it's the idea under discussion | "reminders cut no-shows" |

   Existing behavior: check the code, cite `file:line`. Implemented ≠ used ≠ working — say which you have evidence for.

2. **Fill gaps that change the recommendation** (SKILL.md §6.1): first real users, the pain and how often, today's workaround, what success looks like, constraints (time, people, money). Batch ≤ 3 questions with a default each; otherwise assume and mark.

3. **Market check — only when it changes the decision** (new product, pricing, crowded space): segments, alternatives incl. status quo, competitors, willingness to pay, distribution, risks. Dated sources; no source → hypothesis. Never invent market size, rates or validation (CT5).

4. **Riskiest assumption → cheapest test.** Before an expensive build, prefer: talk to N users, manual/concierge service, spreadsheet or no-code prototype, fake door with disclosure, pilot with one customer. State what result would change the plan.

5. **Recommend one** and write it into the spec:

| Verdict | When | Spec result |
|---|---|---|
| build | problem + user clear, value plausible, smallest slice fits | Objective (success + failure criteria), Users and value, Evidence and assumptions filled → spec stage |
| test first | value or demand unproven, test is much cheaper than build | spec scope = the experiment + decision rule → spec stage |
| don't build | evidence against, or better problem found | status `dropped`, `## Decision`: why (cite evidence), cheaper next test, revisit trigger. Better problem → mention it in one line as a possible new task (a statement, not a question); never switch scope silently |

   Include: target persona, job to be done, value vs workaround, MVP idea (much smaller than the request), non-goals. Numbers carry unit + assumption + how measured.

6. **Show ≤ 15 lines**: verdict, why (top 3 facts), MVP idea, what's out, riskiest assumption + test, then `Assumed:` lines (statements the user can correct — not questions). End with exactly one ask: agree with the verdict, or override.

## Done when

- Verdict recorded in spec; every number labelled verified or `(assumption)`.
- build / test first → next = spec (starts automatically). Don't build → user agreed, status `dropped`, index row `✅ closed — dropped`.
