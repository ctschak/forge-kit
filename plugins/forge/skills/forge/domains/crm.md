# Domain: CRM

Consult in design, architect, review when task touches leads, contacts, accounts, pipelines, assignment, activities.

| Area | Check | Common failure |
|---|---|---|
| Entity model | lead vs contact vs account vs deal separated; lead→contact conversion defined | one "customer" table doing everything |
| Identity | canonical phone (E.164) + email normalized; unique per tenant | `+91 98…` and `98…` = two leads |
| Dedupe | match rules (phone, email, fuzzy name), merge strategy, survivor fields | merge loses activity history |
| Ownership | owner, team, assignment rules (round-robin, territory, load) | unassigned leads rot silently |
| Pipeline | stages configurable per tenant; stage history kept | stage overwritten, no funnel analytics |
| Activity timeline | every touch (call, msg, note, status) appended, immutable, actor + time | edits rewrite history |
| SLA | first-response + follow-up timers, escalation | no alert when lead untouched |
| Multi-tenancy | `tenant_id` on every row + every query; indexes lead with tenant | cross-tenant leak via search/export |
| Permissions | role matrix: admin / manager / agent; agent sees only assigned | agent sees all chats/leads |
| Import/export | CSV mapping, validation report, dry run, idempotent re-import; export audited | partial import, duplicates on retry |
| Sources/attribution | source, campaign, UTM, ad id captured at creation, never overwritten | attribution lost on update |
| Consent | opt-in per channel, timestamp, source; opt-out honoured everywhere | messaging opted-out contacts |
| Custom fields | typed, validated, per-tenant schema; indexed if filtered | JSON blob unsearchable |
| Search/filter | indexed fields, pagination, saved views | full-table scans at 100k leads |
| Notifications | in-app/push/email on assignment, mention, SLA breach; dedupe | notification storms |
| Reporting | funnel, conversion by source/owner, response times; from events not current state | reports wrong after stage edits |
| Audit | role change, export, delete, merge logged | no trail for deleted leads |
| Data retention | soft delete + purge policy; GDPR/DPDP erase request flow | "deleted" data still exported |
