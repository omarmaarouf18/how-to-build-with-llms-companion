# 08. CI permission gotchas

**Book chapters:** Ch. 4.1 (CI from day one), Ch. 4.3 (GitHub)
**Area:** GitHub Actions. Source: [reference/docs/CI_CD_AND_HOOKS.md](../../reference/docs/CI_CD_AND_HOOKS.md), section 8

Three failures that cost real debugging time, each with a one-line fix:

1. **The checkout step silently overrode a token.** `actions/checkout` persists the workflow's
   `GITHUB_TOKEN` in the git config by default. A later cross-repository push that embedded a
   different personal access token in its URL was silently authenticated as the bot instead,
   failing with `Permission denied to github-actions[bot]`.
   **Fix:** `persist-credentials: false` on checkout steps before cross-repo pushes.
2. **A token couldn't push workflow files.** Syncing the mobile app into its own repository
   also updated a workflow file, and GitHub refused: a personal access token needs the
   **Workflows** permission to create or update workflow files.
   **Fix:** grant `Contents: read and write` *and* `Workflows: read and write`.
3. **Release creation returned 403.** `gh release create` failed with
   `Resource not accessible by integration`.
   **Fix:** `permissions: contents: write` on that job.

## Takeaway
CI permissions are least-privilege by default, which is good, and confusing, which is why the
production repo keeps a "Known limitations, failure modes and gotchas" section. Write yours down
the first time; agents (and you, in six months) will read it.
