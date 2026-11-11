# reference/ — production files, for reading

These files are copied from the production repository so you can read the real machinery.
They are **not wired** to this repository: they reference five services, a Flutter app,
integration branches, and scripts that aren't here. Don't run them as-is; read them, and take
what fits your project.

| File | What to look for | Book |
|---|---|---|
| [CLAUDE.production.md](CLAUDE.production.md) | The full instruction file: lanes, hot paths, stop conditions, stamped commits, push policy, commit-hash rules, the "no illustrative output" rule, final report contents | Ch. 2.5, 4.4 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | Running several agents in parallel: one worktree and `agent/<TASK-ID>-<slug>` branch per task, an integration branch, the owner merges and pushes; how the push block works | Ch. 4.2, 4.6 |
| [docs/CI_CD_AND_HOOKS.md](docs/CI_CD_AND_HOOKS.md) | The local gate vs. CI, scoped checks, pass stamps, pinned tool versions, real incidents, a secrets inventory, and "known failure modes and gotchas" | Ch. 4.1, 4.3 |
| [docs/RELEASE.md](docs/RELEASE.md), [docs/RELEASE-GATE.md](docs/RELEASE-GATE.md) | A guarded single-command release, and the gate that must be green before production | Ch. 4.6 (Test) |
| [githooks/pre-commit](githooks/pre-commit) | Blocks raw `git commit` unless a passing check stamped the exact tree being committed | Ch. 4.2 |
| [githooks/pre-push](githooks/pre-push) | The scoped local gate, the commit-hash verification, and the push block for agent worktrees | Ch. 4.2 |
| [scripts/agent-worktree.sh](scripts/agent-worktree.sh) | Creates a task worktree and branch, and sets a per-worktree push URL that makes pushing impossible from it | Ch. 4.2 |
| [scripts/changed-scope.sh](scripts/changed-scope.sh) | Maps changed paths to the checks they need, so the local gate runs only what's affected | Ch. 3.6, 4.1 |
| [scripts/commit.sh](scripts/commit.sh), [scripts/gate-stamp.sh](scripts/gate-stamp.sh) | The stamped-commit mechanism | Ch. 4.2 |
| [scripts/ci-lock.sh](scripts/ci-lock.sh) | A lock so parallel agents' test runs don't fight over the shared local databases | Ch. 4.5 |
| [scripts/gitleaks-scan.sh](scripts/gitleaks-scan.sh) | Secret scanning of commit ranges and uncommitted changes | Ch. 4.1 |
| [Makefile.production](Makefile.production) | Everything above, behind one command per job | Ch. 4.1 |
| [workflows/](workflows/) | The production CI, the release gate with end-to-end tests, and the build-and-publish pipeline | Ch. 4.1, 4.3 |
| [infrastructure/](infrastructure/) | The development and production Compose files for the full platform | Ch. 4.1 |
| [tools/versions.env](tools/versions.env) | Every gate tool pinned to one version, read by both the local hooks and CI | Ch. 4.1 |

One honest note from the production docs themselves: the push block is "a guardrail, not a
security boundary — it prevents accidents, not determined evasion." The real wall is the
protected `main` branch on GitHub.
