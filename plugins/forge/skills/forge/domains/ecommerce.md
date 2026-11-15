# Domain: Ecommerce

Consult in design, architect, review when task touches catalog, cart, checkout, payments, orders, fulfilment.

| Area | Check | Common failure |
|---|---|---|
| Catalog | product vs variant (SKU) model; options; media; SEO slugs | price on product, not variant |
| Pricing | money as integer minor units + currency; price lists, tax-inclusive flag | float rounding errors |
| Inventory | stock per SKU per location; reservation on checkout, release on timeout | overselling under concurrency |
| Cart | guest + logged-in merge; recalculated server-side on every change | client-trusted prices |
| Promotions | rule engine (conditions, stacking, limits per user/code); applied server-side | coupon reused beyond limit |
| Tax | by jurisdiction/HSN/GST; invoice numbering sequential + gapless where required | wrong tax on interstate |
| Checkout | address validation, shipping rates, order total locked before payment | total changes after pay |
| Payments | `rules/api-standards.md` API5: idempotency, PSP tokens, webhooks, state machine | double charge on retry |
| Order state | explicit machine: placed → paid → packed → shipped → delivered / cancelled / returned | ad-hoc status strings |
| Fulfilment | split shipments, carrier integration, tracking webhooks | one order = one shipment assumption |
| Returns/refunds | RMA flow, partial refunds, restock rules | refund without restock |
| Notifications | order/shipping emails + WhatsApp/SMS; templated; idempotent | duplicate "order confirmed" |
| Search | indexed (title, attributes), facets, typo tolerance, sync on update | stale results after price change |
| Performance | CDN for media, cache catalog, p95 checkout latency budget | slow PDP kills conversion |
| Peak traffic | load test for sale events; queue for order intake; rate limits | outage on sale day |
| Fraud | velocity checks, COD limits, address/phone risk | COD abuse |
| Customer accounts | auth, addresses, order history, GDPR/DPDP export + delete | — |
| Analytics | events: view, add-to-cart, checkout-start, purchase; attribution | funnel blind spots |
| Admin | role-based admin, audit log for price/stock edits | untracked price changes |
