# Lessons from production

Every file here is a real problem from building the production system this repository comes
from. Each one says what happened, how it was caught, what it cost, the fix, and the rule it
produced, and points to the book chapter it illustrates.

| # | Lesson | Theme | Book |
|---|---|---|---|
| 01 | [The push adapter that was "verified" but never worked](01-fake-push-adapter-marked-verified.md) | False verification, stubs | Intro, Ch. 4.6, Ch. 5 |
| 02 | [Commit hashes that didn't exist](02-fabricated-commit-shas.md) | Hallucinated identifiers | Intro, Ch. 4.2 |
| 03 | ["Illustrative" output](03-illustrative-output.md) | Evidence must be real | Ch. 4.6 |
| 04 | [Green locally, red on CI](04-dangling-loose-object.md) | Local vs. clean checks | Ch. 4.2, 4.3 |
| 05 | [The password-reset gap that review caught](05-password-reset-gap-caught-in-review.md) | Design review | Ch. 4.6 |
| 06 | [The business that was "closed" every morning](06-production-image-without-time-zones.md) | Prod ≠ dev environment | Ch. 4.6, Ch. 5 |
| 07 | [Databases reachable from the internet](07-databases-exposed-to-the-internet.md) | Insecure defaults | Ch. 4.1, Ch. 5 |
| 08 | [CI permission gotchas](08-ci-credentials-gotchas.md) | CI configuration | Ch. 4.1, 4.3 |
| 09 | [Documentation claimed a change that never happened](09-doc-drift-false-claim.md) | Doc drift | Ch. 4.4 |
| 10 | [A rate limit that only guarded the front door](10-websocket-resource-exhaustion.md) | Security review | Ch. 4.6, Ch. 5 |
| 11 | [The double booking](11-double-booking-race.md) | Race conditions | Ch. 4.6, Ch. 5 |
| 12 | [A cheap model on a big job](12-cheap-model-on-a-big-job.md) | Model selection | Ch. 3 |
| 13 | [A public repository to afford CI](13-public-repo-vs-ci-minutes.md) | Cost vs. security | Ch. 3.6, 4.1 |
| 14 | [MongoDB crash-looping under tests](14-mongo-crash-under-tests.md) | Flaky tests | Ch. 4.5 |

Sources: the production repository's changelogs (`docs/changelog/`), CI documentation
(`reference/docs/CI_CD_AND_HOOKS.md`), ADRs, and context history, plus the author's notes.
