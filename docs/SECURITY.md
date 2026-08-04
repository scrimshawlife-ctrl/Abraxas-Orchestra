# Security notes

Abraxas Orchestra is a **local** Hermes/OpenClaw skill package.

Public debut audit: [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) · Policy: [`.github/SECURITY.md`](../.github/SECURITY.md)

## Threat model (v0.1.3)

| Surface | Behavior |
|---------|----------|
| CLI | Stdlib only; no network I/O in `check` / `structure` / `project` |
| Installer | Local copy only; **path jail** under `$HOME` unless `--allow-outside-home` |
| Schema / JSON | Loaded from skill root on disk only |
| Examples | Local demos; no credentials required |

## Installer guarantees (0.1.3)

1. Refuses `/`, `$HOME` as target, and system prefixes (`/etc`, `/usr`, `/bin`, …)
2. Refuses targets outside `$HOME` unless `--allow-outside-home` is set
3. Backs up existing skill target before atomic swap
4. Uses argv-style command execution (no `eval` of install operations)
5. Prefer `--dry-run` before first install

## Operator rules

1. Do not paste secrets into correspondence tables or module stubs.
2. Review `FORCED` mappings before implementing generated skeletons.
3. Prefer `--dry-run` before first install to a shared host path.
4. Keep mutable agent state **outside** the skill install root.
5. Do not use `--allow-outside-home` on multi-user hosts unless you accept directory replace risk.

## Reporting

See [`.github/SECURITY.md`](../.github/SECURITY.md) for coordinated disclosure.

## Out of scope

Runtime ritual systems, remote model calls, and third-party skill-hub trust chains outside this repository are not part of this package’s security boundary.
