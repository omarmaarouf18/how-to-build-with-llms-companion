# 07. Databases reachable from the internet

**Book chapters:** Ch. 4.1 (environments and secrets), Ch. 5 (security)
**Area:** infrastructure

## What happened
The early Docker Compose setup published MongoDB and Redis ports without authentication. On a
server, a published port is reachable from the internet unless something else blocks it.

## The fix
- MongoDB root authentication and a Redis password were enforced.
- Port bindings were restricted to localhost (`127.0.0.1:27017:27017`, `127.0.0.1:6380:6379`),
  while the services keep talking to each other over the internal Docker network.
- A deployment guide was written covering firewall rules, TLS, and backups.

You can see the result in [infrastructure/docker-compose.yml](../../infrastructure/docker-compose.yml):
every published port is bound to `127.0.0.1`.

## Takeaway
Agents generate configuration that *works*, and "works" often means "open." Defaults in
generated Compose files, CORS settings, and cloud resources deserve a security review just like
code does.
