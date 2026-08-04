# Security policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.3+  | Yes |
| 0.1.2   | Security fixes only until 0.1.3 is adopted |
| < 0.1.2 | No |

## Reporting a vulnerability

**Do not open a public GitHub issue for security reports.**

1. Email the repository owner (see GitHub profile for contact), **or**
2. Open a **private** security advisory on this repository if available.

Include:

- Affected version / commit
- Reproduction steps
- Impact (path overwrite, unexpected network, privilege boundary, etc.)
- Optional: patch or mitigation idea

You should receive an acknowledgment within a few days when contact is monitored.

## Scope

In scope:

- `install.sh` path handling and destructive install behavior
- `scripts/orchestra.py` local file write via `--out`
- Supply-chain claims (dependency / network use)
- Secrets accidentally committed to the repo

Out of scope:

- Misuse of generated symbolic architecture as operational ritual advice
- Host agent (Hermes/OpenClaw) vulnerabilities outside this package
- Issues that require the operator to pass `--allow-outside-home` to a hostile path

## Hardening already applied (0.1.3)

- Installer refuses targets outside `$HOME` unless `--allow-outside-home`
- Installer refuses system path prefixes (`/etc`, `/usr`, …)
- CLI is stdlib-only; no network I/O in `check` / `structure` / `project`
- No `eval` of untrusted content in the CLI path
