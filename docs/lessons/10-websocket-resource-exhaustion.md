# 10. A rate limit that only guarded the front door

**Book chapters:** Ch. 4.6 (Review: security checklist), Ch. 5
**Area:** real-time messaging (`chat-service` and `notification-service`)

## What happened
The WebSocket endpoint had a rate limit: 30 connections per minute. But it applied only **at
connect time**. After the handshake, every incoming message triggered an authorization call to
another service, a database write, and a fan-out to subscribers, all unthrottled. One client
could open a single connection and flood all three.

## The fix
Per-client limits **inside** the read loop (60 messages/min, 30 subscriptions/min), checked
*before* authorization, with a structured `rate_limited` error frame. Streams (SSE) also got
registration limits and a cap on concurrent streams per tenant. Each fix has its own test,
including a real WebSocket flood of 70 messages.

## Takeaway
Ask "what does each request cost, and who can make it?" for every expensive operation, not just
for the entry point. Agents add the obvious limit; the engineer checks where the cost actually is.
