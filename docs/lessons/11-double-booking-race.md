# 11. The double booking: a race condition

**Book chapters:** Ch. 4.6 (Test), Ch. 5
**Area:** idempotency in a money-handling path (`user-service`)

## What happened
Booking requests carry an idempotency key so a retried request doesn't create a second booking.
The check was **GET, then insert**: two concurrent requests with the same key could both see
"no key yet," both create a job, and both lock funds in escrow. A duplicate funded booking.

A second defect: if the client disconnected at the wrong moment, the request's context was
canceled and the idempotency key was never written.

## How the fix was proven
- The race was reproduced first: a concurrency test **failed 25 out of 25 runs** before the fix
  and **0 out of 25** after it.
- The dropped-key bug got a deterministic reproduction that failed before and passed after.

The fix claims the key atomically with Redis `SET NX` and a pending marker, returns the winner's
result (or an explicit 409) to concurrent losers, and writes the key on a context that survives
client disconnects.

## Takeaway
"Check, then act" on shared state is a race. And a race isn't fixed until a test that reproduces
it fails before the fix and passes after, many times in a row.
