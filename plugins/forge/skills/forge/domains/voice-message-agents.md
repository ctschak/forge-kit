# Domain: AI voice & message agents

Consult in design, architect, review when task touches WhatsApp/SMS/voice bots, AI receptionists, auto-replies, conversational journeys.

| Area | Check | Common failure |
|---|---|---|
| Channels | per channel: provider, inbound webhook, outbound API, limits | one code path assuming WhatsApp rules everywhere |
| WhatsApp rules | 24h session window; templates pre-approved for outside window; template categories | free-form message outside window → rejected |
| Consent | opt-in captured, opt-out keywords (STOP) honoured, per-channel | messaging opted-out users |
| Webhooks | signature verified, dedupe by message id, ack fast, process async | duplicate replies on provider retry |
| Ordering | per-conversation sequential processing (queue key = conversation) | replies out of order |
| Conversation state | explicit state machine / journey step persisted; resumable after restart | bot forgets where user was |
| Human handoff | trigger rules, agent assignment, bot paused while human active, return-to-bot | bot and agent reply at once |
| LLM pipeline | system prompt versioned, tools/function calls typed, guard on output | prompt edits untracked, hallucinated prices |
| Grounding | answers from KB/catalog/CRM data; "don't know" path | invents policies |
| Latency (voice) | budget: STT + LLM + TTS ≤ ~800ms to first audio; streaming each stage | dead air, users hang up |
| Turn-taking (voice) | VAD, barge-in cancels TTS, endpointing tuned | bot talks over caller |
| Telephony | SIP/provider, call recording consent, DTMF fallback, transfer to human | no escape to human |
| Failure paths | LLM/STT/provider down → fallback message, retry policy, alert | silent drop |
| Cost | tokens/minutes per conversation tracked; caps per tenant | runaway bills |
| Rate limits | provider throughput tiers, backoff, queue | bans / quality rating drop |
| Media | images/audio/docs: size/type limits, storage, virus scan, expiry of provider URLs | broken media links |
| Evals | test set of real (redacted) conversations; regression run on prompt change | prompt tweak breaks known flows |
| Observability | transcript + tool calls + latency per turn, correlation id | can't debug a bad reply |
| Privacy | PII redaction in logs/transcripts, retention policy | phone numbers in plain logs |
