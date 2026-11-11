# CLAUDE.md — instructions for agents working in this repository

<!-- This is a trimmed version of the instruction file used in production
     (reference/CLAUDE.production.md). Every rule below exists because of a
     real problem; the lesson behind it is linked. HTML comments like this one
     are stripped before the file reaches the model, so they cost no tokens. -->

## What this repo is
A companion slice of a production system: one Go service (`services/notification-service`),
the shared packages it uses (`shared/infra`), docs, and reference material. `reference/` is
read-only history. Never edit files there.

## Commands
- Gate before every commit: `make check` (gofmt, vet, build, test, secret scan).
- Tests: `make test`. Mongo/Redis tests skip if unreachable; start them with `make up`.
- Never run `go test` against a shared database you didn't start for this task.

## Lane rule
- Every task states its allowed paths (its lane). Editing anything outside the lane means:
  stop and ask. Never fix, refactor, or "helpfully" extend out of lane.
- Hot paths, only with explicit ownership in the task: `shared/infra/**`, any `go.mod`/`go.sum`,
  `infrastructure/**`, `.github/**`, `Makefile`.
- Stop conditions: a decision you'd have to guess, an out-of-lane change, a failing gate you
  can't fix inside your lane. Write the question in the task's worklog and stop. Do not guess.

## Git
- Work on a branch, never on `main`. One commit per logical change, after `make check` passes.
- Never push, never force-push, never rebase shared branches, never use `--no-verify`.
  The owner reviews, merges, and pushes.

## Honesty rules (see docs/lessons/01, 02, 03)
- Never mark anything "verified" that you did not verify by running it. Write what you
  checked AND what you did not check.
- Paste command output exactly as captured. Never write "illustrative" or reconstructed
  output. If you didn't capture it, say so.
- Never write a full 40-character commit SHA you didn't just get from `git rev-parse`.

## Worklog
- Each task keeps `docs/worklog/<TASK-ID>.md` using the template in `docs/worklog/README.md`:
  decisions, commits, verification, unverified items, out-of-lane findings, open questions.

## Final report of every task
- `git log --oneline main..HEAD` and `git diff --stat main..HEAD`, literal output.
- Each verification command and its literal output.
- Anything claimed but not verified, with the reason.
