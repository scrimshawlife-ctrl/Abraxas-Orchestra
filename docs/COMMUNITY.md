# Community skills compliance

Checklist for listing **orchestra** in agent skill hubs (OpenClaw, Hermes Skills Hub, agentskills.io-style registries, Claude/Codex skill directories).

## Spec alignment (Agent Skills open format)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Folder contains `SKILL.md` | Pass | Root entry |
| YAML frontmatter `name` | Pass | `orchestra` (lowercase, hyphens) |
| YAML frontmatter `description` | Pass | What + when-to-use (routing text) |
| `name` matches install directory | Pass | `…/skills/orchestra` |
| Optional `scripts/`, `references/` | Pass | Progressive disclosure |
| Description ≤ 1024 chars | Pass | Keep one line for discovery UIs when possible |
| SKILL body not a full manual | Pass | Deep tables stay in `references/` |

## OpenClaw / Hermes packaging

| Requirement | Status | Notes |
|-------------|--------|-------|
| Install path documented | Pass | `~/.hermes/skills/orchestra`, `~/.openclaw/skills/orchestra` |
| Atomic install + dry-run | Pass | `install.sh` |
| `metadata` for runtime gates | Partial | Prefer declaring `requires.bins: [python3]` in frontmatter |
| No undeclared network/env secrets | Pass | CLI is local stdlib |
| Mutable state outside package | Pass | Documented invariant |

## Security review expectations

Registries often reject or quarantine skills that:

- Download and execute remote code at install time
- Require undeclared API keys
- Write outside the skill/project tree without disclosure
- Obfuscate scripts

**Orchestra:** installer copies local files only; CLI uses stdlib; no default network calls. Still run `python3 scripts/orchestra.py check` after install.

## License gap (important)

Current `LICENSE` is **proprietary / evaluation**. Many community registries require **MIT**, **Apache-2.0**, or similar OSI licenses.

| Option | Effect |
|--------|--------|
| Keep proprietary | Fine for private Hermes/OpenClaw use; may block public skill hubs |
| Dual-license or relicense OSS | Unlocks most community catalogs |
| Publish a stripped OSS “core” | CLI + schema + 1–2 frameworks public; full corpus private |

Until relicense, README and this file must state the restriction clearly.

## Suggested frontmatter hardening (community-ready)

```yaml
---
name: orchestra
description: >
  Structure code and agent systems with dual-named modules using traditional
  correspondence maps (Tree of Life, alchemy, runes, planetary, I Ching,
  Solomonic, Peircean, Numogram, geometry, Enochian, Chaos Magic). Use when
  designing architecture, emitting skeletons, correspondence tables, or
  paradigm overlays. Fail-closed on weak mappings.
version: 0.1.1
license: LicenseRef-Proprietary
compatibility: Requires Python 3.11+
metadata:
  author: Applied Alchemy Labs
  homepage: https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes
  openclaw:
    requires:
      bins: [python3]
  hermes:
    tags: [architecture, symbolic, abraxas, structuring]
---
```

## Human + agent legibility rules

1. **README** — install, how-to, tables, safety, layout (humans first scan).
2. **SKILL.md** — activation, ordered steps, invariants, definition of done (agents on activation).
3. **references/** — load only the active framework (token discipline).
4. **examples/** — one runnable path minimum (`check` + demo).
5. **No silent behavior** — projections and FORCED maps must be explicit.

## Pre-publish checklist

- [ ] `python3 scripts/orchestra.py check` exits 0
- [ ] `bash install.sh --dry-run` succeeds
- [ ] Frontmatter `name` / `description` match discovery needs
- [ ] LICENSE compatible with target registry **or** registry allows proprietary
- [ ] No secrets in repo
- [ ] README “How to use” matches actual CLI flags
- [ ] `VERSION` == manifest version == CHANGELOG latest section

## Out of scope for community “generic” skills

This skill encodes Abraxas-oriented symbolic architecture. It is not a general “write any app” skill. Listings should say so in the description so routers do not over-trigger.
