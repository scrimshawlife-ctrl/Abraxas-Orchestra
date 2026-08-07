## Orchestra 0.3.2

Hermes + OpenClaw coding-agent skill for symbolic code architecture.

### Highlights

- **Semantic versioning** — `docs/SEMVER.md` + `scripts/bump_version.py` (`show` / `check` / `patch` / `minor` / `major` / `set`)
- CI `version-parity` enforces `VERSION` ↔ CLI / SKILL / manifest / installer
- Full surface: `structure` · `project` · `diagram` · `analyze` · `optimize` (plan + gated apply)
- Auto HTML / JSON / Mermaid diagrams on `--out`
- Path jail on install + analyze; apply requires `--confirm`

### Install

```bash
git clone --branch v0.3.2 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh
bash install.sh --dry-run && bash install.sh
```

OpenClaw:

```bash
bash install.sh --target ~/.openclaw/skills/orchestra
```

### Security

Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`. CLI is stdlib-only; no network I/O on structure/analyze/optimize paths. Optimize writes require `--apply --confirm`.

License: Apache-2.0

### Docs

- Release notes: `docs/RELEASE_NOTES.md`
- Deploy: `docs/DEPLOY.md`
- Semver: `docs/SEMVER.md`
- Security: `docs/SECURITY.md` / `docs/SECURITY_AUDIT.md`
