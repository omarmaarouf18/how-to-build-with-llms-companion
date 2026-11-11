# Why every piece of this repository exists

This file walks through the repository and explains each piece: what it is, why it's there,
and which problem it prevents. Where a rule came from a real incident, the lesson is linked.

---

## The agent instruction files

### `CLAUDE.md`
The file Claude Code loads into the context at the start of every session (Ch. 2.5). It's short
on purpose: commands, the lane rule, Git rules, honesty rules, the worklog, and the final report.
It's a trimmed version of the production file in `reference/CLAUDE.production.md`, which is worth
reading in full: almost every paragraph there was written after something went wrong.

The production rules worth noticing:

- **The lane rule.** Every task states which paths it may touch. Anything outside the lane means
  *stop and ask*. This single rule prevents the most common agent failure: the "helpful" refactor
  of something nobody asked to change.
- **Hot paths.** Shared code, dependency files, infrastructure, CI, and the Makefile can be touched
  only by a task that explicitly owns them, and only one running task at a time. With several agents
  in parallel, this is what keeps them from colliding in the files everyone depends on.
- **Stop conditions.** A decision that would have to be guessed, an out-of-lane change, a gate that
  can't be fixed in-lane: write the question down and stop. Guessing is how agents create work for you.
- **Honesty rules.** No "verified" without running it; literal output only; no invented commit
  hashes. See lessons [01](lessons/01-fake-push-adapter-marked-verified.md),
  [02](lessons/02-fabricated-commit-shas.md), [03](lessons/03-illustrative-output.md).

### `AGENTS.md`
A one-line pointer: "Follow CLAUDE.md verbatim." In production, every other agent's instruction file
(for example `GEMINI.md`) is a pointer like this, never a copy, because copies drift apart (Ch. 4.4).

---

## The code

### `services/notification-service/`
A real production service, unchanged. It delivers notifications to users in real time over
Server-Sent Events, sends push notifications through Firebase Cloud Messaging, stores notification
history in MongoDB, and uses Redis pub/sub so several instances can share one stream of events
(see [ADR-0005](adr/0005-realtime-hub-horizontal-scaling.md)).

Things to look at:
- `internal/config/config.go`: configuration comes **only** from environment variables, and missing
  required values stop the service at startup instead of failing later (Ch. 4.1).
- `internal/fcm/`: if Firebase isn't configured, push is disabled cleanly and the status is logged,
  rather than pretending to work (the opposite of lesson [01](lessons/01-fake-push-adapter-marked-verified.md)).
- The tests: about 25 test files, including regression tests named after the issue they reproduce
  (`q18_test.go`, `q27_repro_test.go`, `safe_error_regression_test.go`). A bug isn't fixed until a test
  that failed before passes after.
- `Dockerfile`: a multi-stage build (dev, build, prod). The prod stage is a small Alpine image that runs
  as a non-root user. Read lesson [06](lessons/06-production-image-without-time-zones.md) for what a
  minimal image can silently leave out.

### `shared/infra/`
The shared Go packages notification-service imports: `jwtutil` (token validation), `ratelimit`
(Redis-backed limits), `redact` (keeps secrets and personal data out of logs), `resilience` (circuit
breakers and retries), `tlsutil` (mTLS between services), `handlerutil`, and `testutil` (per-run
database and key names so parallel test runs never collide, see lesson [14](lessons/14-mongo-crash-under-tests.md)).

In production this folder is a **hot path**: one change here affects every service, so only a task
that explicitly owns it may touch it.

---

## The machinery

### `Makefile`
"One command per job" (Ch. 4.1): `make setup`, `make check`, `make up`. Humans, agents, and CI run
the same commands. `make check` is the gate before every commit.

The production Makefile (`reference/Makefile.production`) goes further: `make commit` refuses to
commit unless a passing `make check` stamped **exactly** the tree being committed, and the pre-commit
hook blocks raw `git commit`. That turns "run the tests before committing" from advice into a fact.

### `.github/workflows/ci.yml`
Format, build, vet, and test for each module, with real MongoDB and Redis as service containers, plus
a gitleaks secret scan. `concurrency: cancel-in-progress` stops paying for runs that a newer push
already replaced (Ch. 3.6). The production pipeline (`reference/workflows/`) adds pinned security
tools (gosec, govulncheck), compose validation, script regression tests, a release gate with
end-to-end tests, and image publishing.

### `.github/pull_request_template.md`
Every PR states what and why, the literal test output, what was **and wasn't** verified, risks, and a
checklist that starts with "I read every line of this diff" (Ch. 4.3).

### `.gitleaks.toml`
Secret-scanning rules. It keeps every default rule and relaxes only the noisy generic rule inside
test files, which contain fake key-shaped values on purpose. Specific rules (cloud keys, private keys)
still fire everywhere.

### `.env.example`
Every variable the stack needs, with placeholders. The real `.env` is in `.gitignore` (Ch. 4.1).

### `infrastructure/`
- `docker-compose.yml`: MongoDB, Redis, and the service. Every published port is bound to `127.0.0.1`
  (lesson [07](lessons/07-databases-exposed-to-the-internet.md)); Mongo has the raised file limit
  (lesson [14](lessons/14-mongo-crash-under-tests.md)).
- `certs/generate-certs.sh`: throwaway local certificates for the mTLS the services use between
  themselves. Generated files are git-ignored.

---

## The documentation

### `docs/adr/`
Selected architecture decision records from production. See [adr/README.md](adr/README.md) for why
each one was chosen. ADR-0026 is the real version of the book's password-reset example, including
the amendment written after review found a gap (lesson [05](lessons/05-password-reset-gap-caught-in-review.md)).

### `docs/worklog/`
The per-task worklog template and one real worklog (`PUSH-FCM.md`). On a task branch, agents never
edit the shared status files; they write one worklog per task, including what they did **not**
verify and their open questions, and the owner folds it into the shared docs at merge time. This
avoids merge conflicts between parallel agents and keeps an honest record of every task (Ch. 4.4, 4.6).

### `docs/lessons/`
The real problems. Start with [lessons/README.md](lessons/README.md).

---

## `reference/`
Production files kept for reading. They are **not wired** to this repository: they reference
services, branches, and scripts that aren't here. See [reference/README.md](../reference/README.md).
