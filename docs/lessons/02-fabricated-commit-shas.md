# 02. Commit hashes that didn't exist

**Book chapters:** Introduction (hallucination), Ch. 1.6 (sampling: never trust one run), Ch. 4.2 (Git), Ch. 4.4 (docs)
**Area:** documentation and Git history

## What happened
The project's changelogs and ADRs cite the commit that implemented each change. Agents wrote
those citations. Sometimes the 40-character hash they wrote **did not exist**: it looked exactly
like a real commit hash, and it pointed nowhere. A model predicts plausible tokens; a plausible
hash is easy to produce and impossible to tell apart from a real one by looking.

In one recorded incident, a fabricated hash was pushed from an environment where the local
pre-push hook had not been activated, so the local check never ran.

## How it was caught
GitHub CI. A "Verify Markdown Commit SHAs" step checks every full-length hash in every Markdown
file against the repository, and it blocked the push immediately.

## The fix and the rules it produced
- CI and the pre-push hook verify **every** 40-character hash in **every** Markdown file
  (originally only the changelog folder was checked; it was widened after a fabricated hash
  appeared elsewhere).
- Agents may not write full hashes at all on their task branches. The owner adds real hashes
  after merging, taken from `git rev-parse HEAD` and checked with `git cat-file` and
  `git show --stat` (does this commit actually contain the feature described?).
- Any non-citation mention of a hash is written truncated (`05b5ca7...`) so it can never be
  mistaken for a live citation.
- "If the real hash can't be determined, mark the entry unverified. Never write a placeholder."

See the full rule set in [reference/CLAUDE.production.md](../../reference/CLAUDE.production.md),
section *Commit SHA citation rules*.

## Takeaway
Anything an agent writes that *looks like an identifier* (a hash, a version, a file path, an API
field, a package name) must be checked against reality by a machine, not by eye.
