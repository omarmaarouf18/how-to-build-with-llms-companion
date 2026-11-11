# 03. "Illustrative" output

**Book chapters:** Introduction, Ch. 4.6 (Review: show me the evidence), Ch. 5
**Area:** agent task reports

## What happened
Agent task reports included command output (test results, build logs, hook output) that was
**not actually captured**: lines written to "represent" what the output would typically look
like. Sometimes the underlying work was even correct. But a fabricated-but-plausible log line is
indistinguishable from a hallucinated one to anyone reading the report, so the report stops
proving anything.

## The rule it produced
From the production instruction file:

> When presenting command output (test results, build logs, hook output, etc.) in a chat
> response, you must paste the EXACT text that was actually captured from the tool call,
> character for character. You must NEVER write lines that "represent" or "illustrate" what
> output would typically look like [...] If you did not directly capture a piece of output, you
> must say so explicitly.

The final report of every task must contain the **literal** output of `git log`, `git diff --stat`,
and each verification command, plus "anything claimed but not verified, with the reason."

## Takeaway
Evidence only counts if it's real. Ask agents for the literal output, and treat any output you
can't trace back to a tool call as unverified.

<!-- Omar: if you remember the specific incident that triggered this rule, add it here. -->
