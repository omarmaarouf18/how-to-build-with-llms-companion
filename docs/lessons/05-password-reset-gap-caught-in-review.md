# 05. The password-reset gap that review caught

**Book chapters:** Ch. 4.6 (Design, Review) — this is the real version of the book's password-reset example
**Area:** authentication. The full record: [docs/adr/0026-two-phase-password-reset.md](../adr/0026-two-phase-password-reset.md)

## What happened
ADR-0026 split password reset into two phases: verify the emailed code, then set the new
password. The design was careful: rate limiting before any comparison, identical errors for
"unknown email" / "wrong code" / "expired code," and race-safe one-time code consumption.

But phase 2 was authorized only by **the email address plus a server-side "verified" flag**.
Nothing proved that the caller in phase 2 was the same party who entered the correct code in
phase 1. Anyone who knew the target's email could complete the reset during the verified window.

## How it was caught
In review. The ADR's own "residual risk" paragraph had judged the design acceptable; review found
that paragraph understated a real gap.

## The fix
An amendment, written the same day, keeps the original text for history and supersedes it:
- On successful verification, the server mints a random 32-byte **possession token**, stores only
  its SHA-256 digest (in the same atomic update that consumes the code), and returns the raw
  token exactly once.
- Phase 2 requires that token, compared in constant time, with its own 10-minute expiry, and
  clears it on success (single use).
- Every failure mode returns the same generic error.

## Takeaway
A design document can be thorough and still wrong. The "residual risk accepted" paragraph is
exactly where a reviewer should push hardest. And keep the original decision visible when you
amend it: the history of *why* is part of the documentation.
