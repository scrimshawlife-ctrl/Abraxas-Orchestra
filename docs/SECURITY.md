# Security notes

Abraxas Orchestra is a **local** Hermes/OpenClaw skill package.

## Threat model (v0.1.2)

| Surface | Behavior |
|---------|----------|
| CLI | Stdlib only; no network I/O in `check` / `structure` / `project` |
| Installer | Copies package files; backs up prior target; no remote fetch |
| Schema / JSON | Loaded from skill root on disk only |
| Examples | Local demos; no credentials required |

## Operator rules

1. Do not paste secrets into correspondence tables or module stubs.
2. Review `FORCED` mappings before implementing generated skeletons.
3. Prefer `--dry-run` before first install to a shared host path.
4. Keep mutable agent state **outside** the skill install root.

## Reporting

This is a private package. Report issues to the repository owner through the normal private channel.

## Out of scope

Runtime ritual systems, remote model calls, and third-party skill-hub trust chains are not part of this package’s security boundary.
