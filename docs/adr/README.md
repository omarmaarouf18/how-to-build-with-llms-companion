# Architecture decision records (selected)

Six of the 28 ADRs from the production repository, copied unchanged. Commit hashes inside them
refer to the production repository, not this one.

An ADR records **one** decision: the context, the decision, and its consequences (Ch. 4.4). The
production repo writes one whenever a decision is expensive to reverse, and agents read them
before "improving" something that was decided on purpose.

| ADR | Why it's here |
|---|---|
| [0005 Realtime hub horizontal scaling](0005-realtime-hub-horizontal-scaling.md) | The design behind notification-service's hub: an audit found in-memory hubs silently lost notifications once the service ran on 2+ instances; Redis pub/sub fixed it |
| [0010 Separate repos for deployment artifacts](0010-separate-repos-for-deployment-artifacts.md) | Why deployment lives in a separate, private repository: a release-pipeline security decision |
| [0012 Single source of truth for the production .env](0012-single-source-of-truth-for-production-env.md) | Born from a production incident (a silently reverted OTP dispatcher and a database auth mismatch): where production configuration must live |
| [0015 Strict CD pre-flight validation](0015-strict-cd-preflight-validation.md) | The follow-up safeguard: validate the environment before deploying, and roll back automatically if health checks fail |
| [0016 Tiered rate limits](0016-tiered-rate-limits-for-ux-over-uniform-security-floor.md) | A trade-off between security and user experience, decided explicitly instead of by accident |
| [0026 Two-phase password reset](0026-two-phase-password-reset.md) | The real version of the book's password-reset example, including the amendment written after review found a gap (see lesson 05) |

Notice the shape they share: status, date, related commit, the audit finding or incident that
triggered them, and consequences that admit the costs. ADR-0026 also shows how to **amend** a
decision: the original text stays for history, and the amendment says what it supersedes.
