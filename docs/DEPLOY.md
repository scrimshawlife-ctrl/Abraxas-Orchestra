# Deployment — next steps

Ordered path from this repo to a live Hermes or OpenClaw skill install.

Skill name: `orchestra` · Version: see `VERSION` · Hosts: Hermes, OpenClaw

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

---

## 2. Choose host and target path

| Host | Target | Command |
|------|--------|---------|
| **Hermes** (default) | `~/.hermes/skills/orchestra` | `bash install.sh` |
| **OpenClaw** | `~/.openclaw/skills/orchestra` | `bash install.sh --target ~/.openclaw/skills/orchestra` |
| Custom | any dir | `bash install.sh --target /path/to/skills/orchestra` |

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
2. Backs up any existing target under `~/.hermes/receipts/orchestra-backups/` (Hermes default layout)  
3. Atomic stage → swap  

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

Optional functional probe:

```bash
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py do structure \
  -f tree-of-life -c "intent,synthesis,output" --out /tmp/orchestra-probe
ls /tmp/orchestra-probe
```

---

## 5. Wire the agent host

### Hermes

1. Confirm skill root is on Hermes skill search path (`~/.hermes/skills/` or configured extra dirs).
2. Restart or reload agent session so `SKILL.md` frontmatter is re-indexed.
3. Invoke with an architecture / dual-name / correspondence request, or explicit skill use if the host supports `/orchestra` or skill pinning.

### OpenClaw

1. Target must be under OpenClaw skills discovery (`~/.openclaw/skills/orchestra` or documented extraDirs).
2. Frontmatter `metadata.openclaw.requires.bins: [python3]` must be satisfied on PATH.
3. Reload skills list (`openclaw skills list` or host equivalent).
4. Confirm `orchestra` appears; run a structure task.

Agents should load `references/*` only for the active framework (progressive disclosure).

---

## 6. First real use (recommended)

1. State functional concerns (modules, pipeline stages, domains).  
2. Let the skill propose a primary framework (+ optional Chaos overlay).  
3. Accept or override framework.  
4. Emit with CLI or agent:

```bash
python3 scripts/orchestra.py do structure -f <framework> -c "a,b,c" --out ./skeleton
```

5. Review correspondence table status (`CLEAN` vs `FORCED`).  
6. Implement only after human acceptance of forced maps.  
7. Apply `references/agent-posture.md` while filling stubs.

---

## 7. Upgrade / redeploy

```bash
git pull
bash scripts/smoke.sh
bash install.sh --dry-run
bash install.sh   # or --target for OpenClaw
```

Previous install is copied to receipts before replace. Prefer smoke green on the new revision before swapping production agent hosts.

---

## 8. Optional later steps (not required for private deploy)

| Step | When |
|------|------|
| Relicense OSI | Before public skill-hub listing (`docs/COMMUNITY.md`) |
| Hub submit | After license + pre-publish checklist |
| Pin version in agent config | Multi-skill environments that need freeze |
| Corpus expansion | New framework → update refs, CLI, schema, manifest, installer together |

---

## Failure cheat sheet

| Symptom | Action |
|---------|--------|
| `CHECK FAILED` missing ref | Incomplete checkout; pull full `references/` |
| Install dies on validation | Run `python3 scripts/orchestra.py check` in repo root |
| Skill not discovered | Path not on host search path; name ≠ `orchestra`; reload session |
| `NOT_COMPUTABLE` on structure | Unknown framework key or overlay == primary |
| Smoke demo fails | Inspect `examples/signal-forager-skeleton/run_demo.py` output |

---

## Definition of deployed

The skill is **deployed** when:

1. Files exist under the host skills path  
2. `check` exits 0 on the **installed** copy  
3. Host skill index lists `orchestra`  
4. One structure emission succeeds in a live agent or CLI session  
