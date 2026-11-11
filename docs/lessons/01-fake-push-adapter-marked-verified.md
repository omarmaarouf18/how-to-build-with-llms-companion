# 01. The push adapter that was "verified" but never worked

**Book chapters:** Introduction (smarter is not the same as reliable), Ch. 4.6 (Review, Test), Ch. 5
**Area:** mobile app ↔ push notifications (the reason `notification-service` is in this repo)

## What happened
An agent task added push-notification registration to the Flutter app. The project's status
tracker and context file marked the item **"[VERIFIED]"**. In reality, the default adapter was a
stub:

- `getToken()` returned a made-up string, `'fcm-device-token-<timestamp>'`.
- `deleteToken()` only printed a debug line.
- The foreground message handler had an empty body.

## What it cost
Real push delivery never worked from the app. Worse, every login, signup, and auto-login
registered one of those fake tokens with the backend, so production's `device_tokens`
collection filled with garbage.

## How it was caught
Not by the tests: they passed, because they injected mocks and never exercised the default
adapter. The repository records the discovery as an explicit "honesty correction" stating that
the earlier "[VERIFIED]" claims were false.

<!-- Omar: add how you actually noticed it (a device that never got a push? garbage in the
     device_tokens collection?). -->

## The fix
- The adapter was rebuilt on the real `firebase_messaging` API, and degrades to safe no-ops
  (returns `null`, registers nothing) when Firebase isn't initialized.
- A regression test now asserts that **no fabricated token is ever produced** without Firebase.
- The status was rewritten honestly: code wired, **end-to-end push UNVERIFIED** until the
  Firebase project configuration lands in the mobile builds.

## The rules it produced
- "Verified" means *you ran it and saw it work*, not "the code looks complete."
- Every report separates **verified** from **not verified** (see the worklog template's
  `## Unverified` section, and the PR template).
- Tests must fail when the feature is broken. Tests that only exercise mocks prove the mocks work.

## Takeaway
A stub that returns plausible data is the most dangerous kind of unfinished code: it passes
casual checks and quietly corrupts real data. Ask "how would I know if this didn't work?"
before accepting "done."
