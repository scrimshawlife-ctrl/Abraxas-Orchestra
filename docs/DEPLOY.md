# Deployment — next steps

Ordered path from this repo to a live Hermes or OpenClaw skill install.

Freeze checklist: [`COMPLETION.md`](COMPLETION.md). Public debut: [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).

Skill name: `orchestra` · Version: see `VERSION` · Hosts: Hermes, OpenClaw · License: Apache-2.0

---

## 0. Preconditions

| Check | Command / note |
|-------|----------------|
| Python 3.11+ | `python3 --version` |
| Repo on disk | clone or pull `main` |
| Smoke green | `bash scripts/smoke.sh` |

Do not install if smoke fails.

---

## 1. Local validation (mandatory)

```bash
cd Abraxas-Orchestra-Hermes
bash scripts/smoke.sh
python3 scripts/orchestra.py check
python3 scripts/orchestra.py do list-frameworks
```

Expected: `SMOKE OK`, `CHECK OK — Orchestra <version>`, eleven frameworks listed.

Optional security sanity:

```bash
bash install.sh --dry-run --target /etc/orchestra   # must fail
bash install.sh --dry-run                           # must pass
```

---

## 2. Choose host and target path

| Host | Target | Command |
|------|--------|---------|
| **Hermes** (default) | `~/.hermes/skills/orchestra` | `bash install.sh` |
| **OpenClaw** | `~/.openclaw/skills/orchestra` | `bash install.sh --target ~/.openclaw/skills/orchestra` |
| Custom (under `$HOME`) | any dir under home | `bash install.sh --target /path/under/home/orchestra` |
| Custom (outside `$HOME`) | requires explicit flag | `bash install.sh --target /path --allow-outside-home` |

Install directory **name** should remain `orchestra` so frontmatter `name` matches discovery.

---

## 3. Dry-run then install

```bash
bash install.sh --dry-run
bash install.sh
# OpenClaw:
bash install.sh --dry-run --target ~/.openclaw/skills/orchestra
bash install.sh --target ~/.openclaw/skills/orchestra
```

Installer behavior:

1. Validates required files + all framework refs  
2. **Path jail:** refuses system prefixes and targets outside `$HOME` (override: `--allow-outside-home`)  
3. Backs up any existing target under `~/.hermes/receipts/orchestra-backups/` (Hermes default layout)  
4. Atomic stage → swap  

Rollback if needed:

```bash
bash install.sh --rollback
# or with same --target used at install
bash install.sh --rollback --target ~/.openclaw/skills/orchestra
```

---

## 4. Post-install verification

```bash
# Hermes
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py check
bash ~/.hermes/skills/orchestra/scripts/smoke.sh

# OpenClaw
python3 ~/.openclaw/skills/orchestra/scripts/orchestra.py check
```

Optional structure emission:

```bash
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py do structure \
  -f tree-of-life -c "intent,synthesis,output" --out /tmp/orch-skel
```

---

## 5. Wire the host

- Confirm skill discovery picks up `SKILL.md` frontmatter (`name: orchestra`).
- Keep mutable agent state **outside** the skill install root.
- Prefer `--dry-run` after upgrades before swapping a live target.

---

## Optional: pin a release tag

Public debut tag:

```bash
git tag -a v0.1.3 -m "Orchestra 0.1.3 public debut — Apache-2.0 + installer path jail"
git push origin v0.1.3
```

Install from a tag when you need freeze:

```bash
git clone --branch v0.1.3 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
```

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `CHECK FAILED` missing ref | Incomplete checkout; pull full `references/` |
| Unknown framework | `do list-frameworks`; keys must match `schemas/frameworks.v1.json` |
| Install denied (outside home) | Use a path under `$HOME`, or pass `--allow-outside-home` deliberately |
| Install denied (system path) | Never target `/etc`, `/usr`, etc. |

See also: [`COMPLETION.md`](COMPLETION.md) · [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md) · [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) · [`ROADMAP.md`](ROADMAP.md) · [`SECURITY.md`](SECURITY.md).
