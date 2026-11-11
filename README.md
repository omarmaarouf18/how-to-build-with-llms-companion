# How to Build with LLMs — Companion Repository

This is the companion repository for the book **How to Build with LLMs: An Engineer's Guide to AI Agent Workflows** by Omar Maarouf.

Everything the book teaches was applied for real in a production system: a multi-service SaaS platform (Go microservices, a Flutter app, MongoDB, Redis, Docker, GitHub Actions) built with AI coding agents, by one engineer, over several months and about 1,800 commits. This repository is a slice of that system, published so you can see the ideas as working files instead of only as prose:

- **A real service** you can build, test, and run: `services/notification-service` (real-time notifications over Server-Sent Events, push notifications through Firebase Cloud Messaging, notification history in MongoDB, fan-out across instances through Redis).
- **The shared infrastructure** that service depends on: `shared/infra` (JWT validation, rate limiting, log redaction, resilience, mTLS helpers).
- **The documentation system** the agents worked from: the instruction file, architecture decision records, the per-task worklog template, and a real worklog.
- **The guardrails** that kept agents in line: git hooks, stamped commits, the parallel-agent worktree workflow, CI, and the release gate, as they were used in production (`reference/`).
- **The lessons**: real problems that happened while building it, from an agent claiming work was "verified" when it wasn't, to a production image that silently lost its time zone database. Each one tells you what happened, how it was caught, what it cost, and the rule that was added so it never happened again (`docs/lessons/`).

Nothing here is a polished demo built for the book. It is what the work actually looked like.

## Where to start

| If you want to... | Read |
|---|---|
| See which file goes with which chapter | [BOOK_MAP.md](BOOK_MAP.md) |
| Understand why each piece of this repo exists | [docs/WHY.md](docs/WHY.md) |
| Read the real problems and what they taught | [docs/lessons/](docs/lessons/README.md) |
| See the instruction file the agents followed in production | [reference/CLAUDE.production.md](reference/CLAUDE.production.md) |
| See how parallel agents were run safely | [reference/docs/WORKFLOW.md](reference/docs/WORKFLOW.md) |
| Run the service | [Quick start](#quick-start) below |

## Repository layout

```text
.
├── CLAUDE.md, AGENTS.md         Instructions for agents working in THIS repo
├── Makefile                     One command per job: setup, up, check, test...
├── .github/                     CI (format, build, vet, test, secret scan) and PR template
├── services/notification-service/   The real service (unchanged production code)
├── shared/infra/                The shared Go packages it depends on
├── infrastructure/              Local Docker Compose stack and dev certificates
├── docs/
│   ├── WHY.md                   Why every piece of this repo exists
│   ├── adr/                     Selected architecture decision records
│   ├── worklog/                 The per-task worklog template, plus a real worklog
│   └── lessons/                 Real problems, how they were caught, the rules they produced
└── reference/                   Production files kept for reading, NOT wired to this repo
```

## Quick start

Requirements: Go 1.26, Docker with Compose, OpenSSL, and optionally [gitleaks](https://github.com/gitleaks/gitleaks).

```bash
make setup     # creates .env from .env.example and generates local dev certificates
make check     # format, vet, build, test, secret scan: the gate before every commit
make up        # starts MongoDB, Redis and notification-service locally
make logs      # follow the service logs
make down
```

Tests that need MongoDB or Redis skip themselves when those aren't reachable, so `make test` works on a bare machine. Start the stack (or run CI) to exercise them.

The service runs on its own here, so anything that calls the other services of the full platform (for example, resolving device tokens through auth-service) will fail gracefully. That is expected: this repository exists to show how the work was done, not to run the whole platform.

## What was changed from production

- Only one service and the shared packages it imports were copied; the code inside them is unchanged.
- History was not copied. This repository starts from a fresh `git init`.
- The Makefile, CI workflow, Compose file, and certificate script were trimmed to fit one service. The production versions are in `reference/` for reading.
- Secrets: none. `.env.example` holds placeholders only, and the tree passes a gitleaks scan. Test files contain fake key-shaped values on purpose; `.gitleaks.toml` documents which.

## License

MIT, see [LICENSE](LICENSE). Use anything here in your own projects.
