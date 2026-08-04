# Abraxas Orchestra

**Hermes + OpenClaw coding-agent skill** for symbolic code architecture.

Version **0.1.1** · Skill name: `orchestra` · Python ≥ 3.11 · Network: not required

Maps software structure onto traditional correspondence systems (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic) and emits **dual-named skeletons** with recoverable provenance.

Fail-closed on weak mappings. Human sovereignty over forced maps. Corpus open for expansion.

---

## Quick start

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
cd Abraxas-Orchestra-Hermes

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

---

## How to use

### For humans

| Goal | Command |
|------|---------|
| Validate install | `python3 scripts/orchestra.py check` |
| See frameworks | `python3 scripts/orchestra.py do list-frameworks` |
| Emit skeleton (stdout) | `python3 scripts/orchestra.py do structure -f <framework>` |
| Emit + write disk | `… do structure -f <framework> --out ./my-skeleton` |
| Overlay second map | `… do structure -f enochian -o chaos-magic` |
| Collapse oversized map | `… do project -f tree-of-life --out ./projected` |
| Working pipeline demo | `cd examples/signal-forager-skeleton && python3 run_demo.py` |

**Framework keys:** `tree-of-life` · `alchemical-stages` · `elder-futhark` · `planetary-spheres` · `iching-hexagrams` · `solomonic` · `peircean-signs` · `numogram` · `sacred-geometry` · `enochian` · `chaos-magic`

### For agents

1. **Discover** — Frontmatter `name` + `description` in `SKILL.md` (load only when the task matches architecture / dual-name / correspondence work).
2. **Activate** — Follow the mandatory sequence in `SKILL.md` (intent → framework → table → skeleton → projection → fail-closed → provenance).
3. **Deepen on demand** — Open only the needed file under `references/` (do not preload the full corpus).
4. **Execute** — Prefer `scripts/orchestra.py` over inventing directory layouts by hand.
5. **Build code** — Apply `references/agent-posture.md` (layered growth, current requirements only, gated compatibility).

Do **not** invent symbolic loci to satisfy a map. Return `NOT_COMPUTABLE` or mark `FORCED` and stop.

### Definition of done

A successful run produces:

- Dual-named module list (mechanical primary, symbolic secondary)
- Correspondence table JSON matching `schemas/correspondence-table.v1.schema.json`
- Status `CLEAN`, or explicit `FORCED_CORRESPONDENCE` / pragmatic projection note
- No silent collapse; no occult names as the sole public API unless the operator asked

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
SKILL.md                 # Agent contract (frontmatter + procedure)
orchestra.manifest.yaml  # Install / discovery metadata
scripts/orchestra.py     # CLI (structure, project, check)
references/              # Framework tables + agent-posture (load on demand)
schemas/                 # correspondence-table.v1
examples/                # signal-forager; enochian-chaos
docs/                    # DESIGN, OPENCLAW, COMMUNITY
install.sh               # Atomic installer (--dry-run, --rollback, --target)
```

Progressive disclosure: keep `SKILL.md` in context; open `references/*` only for the active framework.

---

## Examples

| Path | What it shows |
|------|----------------|
| `examples/signal-forager-skeleton/` | Tree of Life + alchemy; runnable forage pipeline |
| `examples/enochian-chaos-skeleton/` | Enochian primary + Chaos overlay; Mermaid map |

---

## Safety and requirements

- **Runtime:** Python 3.11+ standard library only for the CLI (no pip deps)
- **Network:** Not required for `check` / `structure` / `project`
- **State:** Skill package is read-mostly; mutable state stays outside the install root
- **Destructive ops:** Installer can replace a target skill dir after backup; use `--dry-run` first
- **License:** Proprietary evaluation terms — see `LICENSE` (community registry notes in `docs/COMMUNITY.md`)

---

## Documentation map

| Doc | Audience |
|-----|----------|
| `SKILL.md` | Agents (procedure + invariants) |
| `README.md` | Humans + agents (this file) |
| `docs/DESIGN.md` | Design rationale |
| `docs/OPENCLAW.md` | OpenClaw packaging |
| `docs/COMMUNITY.md` | Community-skills compliance checklist |
| `references/agent-posture.md` | How to implement code under this skill |
| `CHANGELOG.md` | Version history |

---

## Contributing / corpus expansion

New frameworks must update **together**:

1. `references/<name>.md`
2. `FRAMEWORKS` in `scripts/orchestra.py`
3. Schema enum in `schemas/correspondence-table.v1.schema.json`
4. `orchestra.manifest.yaml` frameworks list
5. `install.sh` reference list
6. `SKILL.md` framework table

Then run `python3 scripts/orchestra.py check`.

---

## Links

- Repo: https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes
- Version: see `VERSION`
