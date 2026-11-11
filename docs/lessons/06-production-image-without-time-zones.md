# 06. The business that was "closed" every morning

**Book chapters:** Ch. 4.6 (Test: does it work for real?), Ch. 5
**Area:** production environment vs. development environment

## What happened
An owner set working hours of 09:00–21:00 in the app. Saving looked fine. But customers saw the
business as **closed** with the wrong reopening time (for example, noon).

## How it was found
The obvious suspects were all cleared with evidence: the real screen interaction produced a
byte-exact 09:00/21:00 payload, the backend stored it verbatim, and the evaluation logic agreed
at real local time. The bug was not in the code at all.

The production image was `alpine:3.20`, which ships **no time zone database**. In production,
`time.LoadLocation("Africa/Cairo")` failed, and the code silently fell back to UTC. A 09:00–21:00
Cairo business was evaluated as 09:00–21:00 UTC.

## The fix
One line: `import _ "time/tzdata"` embeds the time zone database in the Go binary, so it works
wherever the binary runs. A regression test pins that Cairo **never degrades to UTC**, and it
was proven to fail first and then pass **inside a bare `alpine:3.20` container**: the same
environment as production.

## Takeaway
Tests on your machine test your machine. Two lessons: run at least some checks in an
environment identical to production, and never let code silently fall back to a default when
something required is missing. Fail loudly instead.
