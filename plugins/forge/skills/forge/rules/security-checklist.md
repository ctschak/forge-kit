# Security checklist

Design §Security answers each relevant item for this task; review (arch, code) checks them.

| ID | Check |
|---|---|
| SEC1 | Authn: every entry point authenticated? Which scheme, where enforced? |
| SEC2 | Authz: role/scope checked server-side? Tenant + ownership enforced on every read/write (incl. list, search, export)? |
| SEC3 | Input: validated at boundary (type, length, format, enum)? File uploads type/size-checked? |
| SEC4 | Injection: parameterized queries; no string-built SQL/shell/templates from input? |
| SEC5 | Output: encoded for context (HTML, URL, JSON); no internals in errors? |
| SEC6 | Secrets: from secret store/env; none in code, logs, docs, client bundles? |
| SEC7 | PII: minimized, masked in logs, retention defined, consent captured where required? |
| SEC8 | Abuse: rate limits, lockouts, idempotency, replay protection? |
| SEC9 | Browser: CSRF protection for cookie auth; CORS allowlist; cookies `HttpOnly` `Secure` `SameSite`? |
| SEC10 | Webhooks/callbacks: signature verified, timestamp window, event dedupe? |
| SEC11 | Dependencies: new packages vetted (maintained, licence, known CVEs)? |
| SEC12 | Audit: security-relevant actions (login, role change, export, payment, delete) logged with actor + time? |
