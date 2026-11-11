# 04. Green locally, red on CI: the dangling commit

**Book chapters:** Ch. 4.2 (Git), Ch. 4.3 (CI is the full gate)
**Area:** Git internals, local vs. CI checks

## What happened
While documenting ADR-0012, a commit was created locally, and then the file's "Related Commit
SHA" field was updated to point at an amended version of it. The original commit still existed
as a *loose object* in the local `.git/objects` folder, so the local check (`git cat-file -e`)
passed.

Loose objects that aren't reachable from a branch are **not transferred by `git push`**. On
GitHub's clean checkout the commit didn't exist, and CI failed with
`BLOCKED: fabricated/non-existent SHA`.

## The fix and the rule it produced
Both the pre-push hook and CI now require every cited hash to be an **ancestor of HEAD**
(`git merge-base --is-ancestor "$sha" HEAD`), not merely to exist locally. And a commit whose
hash is already cited anywhere is never amended; a new commit is made instead.

## Takeaway
"It passes on my machine" is a property of your machine. A clean CI checkout is the only
environment that sees the repository the way everyone else will. That's why the production
workflow makes GitHub CI the single full gate.
