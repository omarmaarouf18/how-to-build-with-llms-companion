# 12. A cheap model on a big job

**Book chapter:** Ch. 3.5, "A story from production: the fast model that planned a feature"

This lesson is told in full in the book. In short: a cheap, fast "flash"-class model was given
a feature to plan *and* implement, with short instructions. It drifted: it changed a lot of
working code outside the feature and filled the gaps in the instructions with its own guesses.
Finding and repairing the damage took a week.

What changed afterwards:
- Planning goes to the strongest model, at high effort, and the plan is reviewed before any code.
- Cheap models get narrow, fully specified tasks with a check they can't fake (tests).
- Every task states its lane; anything outside it means stop and ask
  (see [CLAUDE.md](../../CLAUDE.md)).
- Work happens on a branch in small commits, so a wrong direction costs a revert, not a week.

> A cheap model is only cheap when its mistakes are cheap to find.
