# Book map: which file goes with which chapter

| Chapter | Topic | Look at |
|---|---|---|
| Introduction | Smarter is not the same as reliable | [lessons/01](docs/lessons/01-fake-push-adapter-marked-verified.md), [lessons/02](docs/lessons/02-fabricated-commit-shas.md) |
| 1.6 | Sampling: never trust one run, verify | [lessons/02](docs/lessons/02-fabricated-commit-shas.md), [lessons/03](docs/lessons/03-illustrative-output.md) |
| 1.17 | Anatomy of a harness: hooks, permissions, sub-agents | [reference/githooks/](reference/githooks/), [reference/scripts/agent-worktree.sh](reference/scripts/agent-worktree.sh) |
| 2.4 | Permissions and undo | [CLAUDE.md](CLAUDE.md) (Git section), [reference/docs/WORKFLOW.md](reference/docs/WORKFLOW.md) §5 "How the push block works" |
| 2.5 | CLAUDE.md and AGENTS.md | [CLAUDE.md](CLAUDE.md), [AGENTS.md](AGENTS.md), [reference/CLAUDE.production.md](reference/CLAUDE.production.md) |
| 2.9 | Hooks: rules that can't be ignored | [reference/githooks/pre-commit](reference/githooks/pre-commit), [reference/githooks/pre-push](reference/githooks/pre-push) |
| 3 | Choosing models, cost | [lessons/12](docs/lessons/12-cheap-model-on-a-big-job.md), [lessons/13](docs/lessons/13-public-repo-vs-ci-minutes.md), [reference/scripts/changed-scope.sh](reference/scripts/changed-scope.sh) |
| 4.1 | Day zero: skeleton, one command per job, environments, CI | [Makefile](Makefile), [.env.example](.env.example), [.github/workflows/ci.yml](.github/workflows/ci.yml), [infrastructure/](infrastructure/), [lessons/07](docs/lessons/07-databases-exposed-to-the-internet.md), [lessons/08](docs/lessons/08-ci-credentials-gotchas.md) |
| 4.2 | Git: branches, small commits, worktrees, secrets in history | [reference/docs/WORKFLOW.md](reference/docs/WORKFLOW.md), [reference/scripts/](reference/scripts/), [lessons/04](docs/lessons/04-dangling-loose-object.md), [lessons/13](docs/lessons/13-public-repo-vs-ci-minutes.md) |
| 4.3 | GitHub: PRs, protected main, CI | [.github/pull_request_template.md](.github/pull_request_template.md), [reference/workflows/](reference/workflows/), [reference/docs/RELEASE-GATE.md](reference/docs/RELEASE-GATE.md) |
| 4.4 | Documentation the agent works from | [docs/adr/](docs/adr/README.md), [docs/worklog/](docs/worklog/README.md), [lessons/09](docs/lessons/09-doc-drift-false-claim.md) |
| 4.5 | An agent-friendly codebase | [services/notification-service/](services/notification-service/), [shared/infra/](shared/infra/), [lessons/14](docs/lessons/14-mongo-crash-under-tests.md) |
| 4.6 | Requirements → spec → design → tasks → implement → review → test | [docs/adr/0026](docs/adr/0026-two-phase-password-reset.md), [lessons/05](docs/lessons/05-password-reset-gap-caught-in-review.md), [docs/worklog/PUSH-FCM.md](docs/worklog/PUSH-FCM.md), [lessons/06](docs/lessons/06-production-image-without-time-zones.md) |
| 5 | Quality: reading, testing, securing AI code | [lessons/01](docs/lessons/01-fake-push-adapter-marked-verified.md), [lessons/06](docs/lessons/06-production-image-without-time-zones.md), [lessons/10](docs/lessons/10-websocket-resource-exhaustion.md), [lessons/11](docs/lessons/11-double-booking-race.md) |
| 6 | A real project, end to end | This whole repository |

Every piece is explained in [docs/WHY.md](docs/WHY.md).
