# API standards

Apply to every API in a design. Project conventions (from `understanding.md`) win where they already differ — note the deviation.

## API1 — Required per endpoint

| Item | Content |
|---|---|
| Endpoint | `METHOD /v1/<plural-resource>/{id}/<sub-resource>` |
| Purpose | one line |
| Authn | scheme: Bearer JWT / OAuth2 (scopes) / API key / session cookie; where validated |
| Authz | role/scope required; tenant + ownership check (which field, where) |
| Headers | `Authorization`, `Content-Type`, `Idempotency-Key`, `X-Request-Id`, custom |
| Cookies | name, `HttpOnly` · `Secure` · `SameSite`, purpose — or "none" |
| Path params | name, type, validation |
| Query params | filters, `sort`, `limit` (default/max), `cursor` |
| Request body | schema table + JSON example |
| Response | status + schema + JSON example |
| Errors | every case: status, `code`, when, example body |
| Rate limit | limit/window, `429` + `Retry-After` |
| Idempotency | safe/idempotent? key required? replay behaviour |

## API2 — REST patterns

- Plural nouns, kebab-case: `/v1/lead-sources`. No verbs in path; state change = sub-resource or field (`POST /v1/orders/{id}/cancellation`).
- `GET` read · `POST` create/action · `PUT` full replace · `PATCH` partial · `DELETE` remove.
- Create → `201` + `Location` header + body. No body → `204`.
- Pagination: cursor — `?limit=50&cursor=<opaque>` → `{ data: [], next_cursor }`.
- Filtering `?status=open&created_after=2026-01-01`; sorting `?sort=-created_at`.
- Versioning in path `/v1`; breaking change → `/v2`.
- JSON `snake_case`; timestamps ISO-8601 UTC; IDs opaque strings.
- Never leak existence across tenants: not-owned → `404`, not `403`.

## API3 — Status codes

| Code | When |
|---|---|
| 400 | malformed / validation failed |
| 401 | missing/invalid credentials |
| 403 | authenticated, lacks permission |
| 404 | not found or not owned |
| 409 | conflict: duplicate, version mismatch, idempotency key reused with different body |
| 422 | valid shape, business rule rejects (e.g. payment declined) |
| 429 | rate limited |
| 500/502/503 | server / upstream / unavailable — no internals in body |

## API4 — Error body (RFC 9457, `application/problem+json`)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation failed",
  "status": 400,
  "code": "VALIDATION_FAILED",
  "detail": "phone must be E.164",
  "request_id": "req_123",
  "errors": [{ "field": "phone", "code": "FORMAT", "message": "must be E.164" }]
}
```

## API5 — Payments

- `Idempotency-Key` required on every create/capture/refund; same key + same body → original response; same key + different body → `409`.
- Amounts: integer minor units + ISO-4217 currency (`amount_minor: 49900, currency: "INR"`). No floats.
- Store PSP tokens only — never PAN/CVV.
- Webhooks: verify signature (HMAC over raw body), reject outside 5-min timestamp window, dedupe by event id, respond `2xx` fast, process async.
- State machine: `pending → authorized → captured | failed`; `captured → refunded | partially_refunded`. Transitions server-side only.

### Worked example — `POST /v1/payments`

```http
POST /v1/payments
Authorization: Bearer <jwt>            # scope: payments:write
Content-Type: application/json
Idempotency-Key: 6f1c2a9e-0b7d-4e7a-9a51-2d4c8c1f0e11
X-Request-Id: req_123

{ "order_id": "ord_123", "amount_minor": 49900, "currency": "INR",
  "method": { "type": "card", "token": "tok_test_xxx" } }
```

`201 Created` · `Location: /v1/payments/pay_123`
```json
{ "id": "pay_123", "order_id": "ord_123", "status": "authorized",
  "amount_minor": 49900, "currency": "INR", "created_at": "2026-11-14T10:00:00Z" }
```

| Status | code | When |
|---|---|---|
| 400 | `VALIDATION_FAILED` | missing amount, bad currency |
| 401 | `UNAUTHENTICATED` | no/expired token |
| 403 | `FORBIDDEN` | token lacks `payments:write` |
| 404 | `ORDER_NOT_FOUND` | order missing or other tenant's |
| 409 | `IDEMPOTENCY_CONFLICT` | key reused, body differs |
| 409 | `ORDER_ALREADY_PAID` | order has captured payment |
| 422 | `PAYMENT_DECLINED` | PSP declined; `detail` = safe reason |
| 429 | `RATE_LIMITED` | over limit |
| 502 | `PSP_UNAVAILABLE` | PSP timeout — client retries with same key |

Webhook in:
```http
POST /v1/webhooks/psp
X-Signature: t=1731578400,v1=<hex-hmac-sha256>

{ "id": "evt_123", "type": "payment.captured", "data": { "payment_id": "pay_123" } }
```
Verify: HMAC-SHA256(secret, `t + "." + raw_body`) == `v1` (constant-time compare) · `|now - t| ≤ 300s` · `evt_123` not seen → enqueue → `200`.
