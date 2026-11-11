# 14. MongoDB crash-looping under the test suites

**Book chapters:** Ch. 4.5 (fast, reliable tests)
**Area:** local infrastructure

## What happened
`mongod` keeps one file handle per collection, index, and connection. The test suites create
hundreds of uniquely named test databases (so parallel runs never collide), and Docker's default
open-file limit (1024) ran out. MongoDB's storage engine failed with `EMFILE` and the container
crash-looped, which looked like flaky tests.

## The fix
`ulimits: nofile: 64000` on the Mongo container, the value the MongoDB image documents. You'll
find it, with the explanation, in [infrastructure/docker-compose.yml](../../infrastructure/docker-compose.yml).
Separately, every test run uses a per-run suffix for database names and Redis keys
(`shared/infra/testutil`) so concurrent runs from parallel agents can't interfere.

## Takeaway
Flaky tests are poison for agents: they learn to ignore failures. When tests fail randomly,
suspect the environment before the code, and fix it at the root.
