# 09. When the documentation claimed a change that never happened

**Book chapters:** Ch. 4.4 (keeping documentation alive)
**Area:** documentation drift

## What happened
A context entry recorded that a retry loop had been **removed** from a concurrency test in
`chat-service`. When the code was later verified directly, the loop was **still there**. The
commit that the entry cited had landed other changes, but not that one.

## The fix
The entry was corrected and marked as a correction, with the exact file and lines verified
against the working tree. Whether the loop *should* be removed was recorded as a flagged
follow-up instead of being changed silently during a documentation fix.

## Takeaway
Documentation written by agents describes what they *intended* or *believed*, which isn't always
what landed. Verify claims against the code, keep corrections visible, and don't mix "fix the
docs" with "change the code" in the same step.
