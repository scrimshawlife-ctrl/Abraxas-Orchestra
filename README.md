# Abraxas Orchestra

<p align="center">
  <img src="assets/hero.svg" alt="Abraxas Orchestra — symbolic architecture skill" width="720"/>
</p>

<p align="center">
  <strong>Hermes + OpenClaw coding-agent skill</strong> for symbolic code architecture
</p>

Version **0.3.0** · Skill name: `orchestra` · Python ≥ 3.11 · Network: not required · License: Apache-2.0

Maps software structure onto traditional correspondence systems (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic) and emits **dual-named skeletons** with recoverable provenance.

Fail-closed on weak mappings. Human sovereignty over forced maps. Corpus open for expansion.

---

## Quick start

**Deploy to Hermes/OpenClaw:** follow [`docs/DEPLOY.md`](docs/DEPLOY.md) (validate → dry-run → install → verify → wire host).

**Freeze checklist:** [`docs/COMPLETION.md`](docs/COMPLETION.md) · **Public debut:** [`docs/PUBLIC_RELEASE.md`](docs/PUBLIC_RELEASE.md)

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
cd Abraxas-Orchestra-Hermes

bash scripts/smoke.sh
python3 scripts/orchestra.py check
python3 scripts/orchestra.py do list-frameworks
python3 scripts/orchestra.py do structure -f tree-of-life -c "intent,synthesis,output"
```

Install into an agent host:

```bash
bash install.sh --dry-run
bash install.sh                                          # → ~/.hermes/skills/orchestra
bash install.sh --target ~/.openclaw/skills/orchestra    # OpenClaw
```

Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`.

---

## Release notes

**Current: [0.3.0](docs/RELEASE_NOTES.md#030--2026-08-04)** (2026-08-04) — analyze → map → optimize apply.

| Theme | What landed |
|-------|-------------|
| Analyze | `analyze --path` OBSERVED Python import graph + optional framework map |
| Optimize plan | `optimize --from analysis.json` (no tree writes) |
| Optimize apply | `--apply` dry-run; `--apply --confirm` gated renames + backup |
| Diagrams | Auto HTML/JSON/Mermaid on structure/project/analyze `--out` |

Full narrative: **[`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md)** · Machine changelog: [`CHANGELOG.md`](CHANGELOG.md) · Plan: [`docs/ANALYZE_OPTIMIZE_PLAN.md`](docs/ANALYZE_OPTIMIZE_PLAN.md)

---

## How to use

### For humans

| Goal | Command |
|------|---------|
| Validate install | `python3 scripts/orchestra.py check` |
| Full smoke | `bash scripts/smoke.sh` |
| See frameworks | `python3 scripts/orchestra.py list` |
| Emit skeleton (stdout) | `python3 scripts/orchestra.py structure -f <framework>` |
| Emit + write disk | `… structure -f <framework> --out ./my-skeleton` |
| Overlay second map | `… structure -f enochian -o chaos-magic` |
| Collapse oversized map | `… project -f tree-of-life --out ./projected` |
| Analyze a repo | `… analyze --path ./pkg -f tree-of-life --out ./analysis` |
| Optimize plan | `… optimize --from ./analysis/analysis.json --out ./plan` |
| Optimize dry-run | `… optimize --from ./analysis/analysis.json --apply` |
| Optimize apply | `… optimize --from ./analysis/analysis.json --apply --confirm` |
| Working pipeline demo | `cd examples/signal-forager-skeleton && python3 run_demo.py` |

**Framework keys:** `tree-of-life` · `alchemical-stages` · `elder-futhark` · `planetary-spheres` · `iching-hexagrams` · `solomonic` · `peircean-signs` · `numogram` · `sacred-geometry` · `enochian` · `chaos-magic`

### For agents

1. **Discover** — Frontmatter `name` + `description` in `SKILL.md`.
2. **Activate** — Mandatory sequence in `SKILL.md`.
3. **Deepen on demand** — Open only needed `references/` files.
4. **Execute** — Prefer `scripts/orchestra.py`.
5. **Build code** — Apply `references/agent-posture.md`.

Do **not** invent symbolic loci to satisfy a map. Return `NOT_COMPUTABLE` or mark `FORCED` and stop.

### Definition of done

- Dual-named module list (mechanical primary, symbolic secondary)
- Correspondence table JSON matching `schemas/correspondence-table.v1.schema.json`
- Status `CLEAN`, or explicit `FORCED_CORRESPONDENCE` / pragmatic projection note
- No silent collapse; no occult names as sole public API unless requested

---

## What this skill is / is not

| Is | Is not |
|----|--------|
| Architecture structuring skill | Runtime ritual / operative magic |
| Dual-name + provenance emitter | Auto-canon promotion into Abraxas |
| Hermes + OpenClaw portable package | Network service or SaaS |
| Open correspondence corpus | Speculative deep trees without projection |

---

## Repository layout

```text
assets/hero.svg          # README hero (JPEG optional)
SKILL.md                 # Agent contract
orchestra.manifest.yaml  # Install / discovery metadata
scripts/orchestra.py     # CLI
scripts/smoke.sh         # Production smoke
references/              # Framework tables + agent-posture
schemas/                 # correspondence-table.v1 + frameworks.v1
examples/                # signal-forager; enochian-chaos
tests/                   # stdlib unittest
docs/                    # DESIGN, DEPLOY, COMPLETION, PUBLIC_RELEASE, …
install.sh               # Atomic installer (path jail)
LICENSE / NOTICE         # Apache-2.0
```

---

## Documentation map

| Doc | Audience |
|-----|----------|
| `SKILL.md` | Agents |
| `README.md` | Humans + agents |
| `docs/COMPLETION.md` | Private production freeze checklist |
| `docs/PUBLIC_RELEASE.md` | Public debut packaging checklist |
| `docs/SECURITY_AUDIT.md` | Security audit record (0.1.3) |
| `docs/RELEASE_NOTES.md` | Narrative release notes |
| `docs/DEPLOY.md` | Ordered deployment next steps |
| `docs/ROADMAP.md` | Done / deferred / production bar |
| `docs/DESIGN.md` | Design rationale |
| `docs/OPENCLAW.md` | OpenClaw packaging |
| `docs/COMMUNITY.md` | Community-skills compliance |
| `docs/SECURITY.md` | Local threat model |
| `references/agent-posture.md` | Code implementation posture |
| `CHANGELOG.md` | Machine version history |
| `.github/SECURITY.md` | Vulnerability reporting |

---

## Safety and requirements

Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`. CLI performs no network I/O. No third-party runtime dependencies. See [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md).

- **Runtime:** Python 3.11+ standard library only for the CLI
- **Network:** Not required for `check` / `structure` / `project`
- **State:** Mutable state stays outside the install root
- **Destructive ops:** Installer replaces target after backup; use `--dry-run` first
- **License:** Apache-2.0 — see `LICENSE` and `NOTICE`

---

## Links

- Repo: https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes
- Freeze checklist: [`docs/COMPLETION.md`](docs/COMPLETION.md)
- Public debut: [`docs/PUBLIC_RELEASE.md`](docs/PUBLIC_RELEASE.md)
- Security audit: [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md)
- Release notes: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md)
- Deploy: [`docs/DEPLOY.md`](docs/DEPLOY.md)
