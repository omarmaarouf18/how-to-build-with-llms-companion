# 13. A public repository to afford CI

**Book chapters:** Ch. 3.6 (cost levers), Ch. 4.1 (CI), Ch. 4.2 (secrets in history)
**Area:** cost vs. security trade-off

## The situation
The production repository was made **public** for a practical reason: the project ran a very
high number of CI builds, and GitHub Actions minutes on standard runners are free for public
repositories.

## What that trades away
- **Secrets in history.** Staging credentials committed early on were replaced with
  placeholders later (commit message: "SEC-01a: replace real secrets in staging env example with
  placeholders"), but history keeps them forever. The owner verified they were not used in
  production, and the secret-scanning config documents that decision.
- **Security logic is readable by anyone**: rate limits, admin-access controls, verification flows.
  Good security doesn't rely on secrecy, but it does give an attacker a map.
- **Business logic and decisions** are visible to competitors, with the ADRs explaining why.

## The alternatives considered
- Keep the repository private and cut CI cost instead: scope CI to what changed (the local gate
  already does this with `scripts/changed-scope.sh`), cancel superseded runs, cache, and run the
  full end-to-end suite only on merges to `main`.
- A self-hosted runner for a private repository (never for a public one: a pull request from a
  fork could run code on your machine). Check the current pricing for self-hosted runners.
- Split: keep the sensitive services private, publish the rest. The project already separates
  deployment artifacts into a private repository (ADR-0010).

## Takeaway
Cost decisions are engineering decisions, and they have security consequences. Make them on
purpose, write them down, and rotate any secret that history still holds.

<!-- Omar: add how you decided, and whether you'd decide the same today. -->
