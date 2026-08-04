# Abraxas Orchestra

**Hermes + OpenClaw coding-agent skill** for symbolic code architecture  
*v0.1.0 — design surface, open corpus, executable CLI*

Structure modules, pipelines, interfaces, and agent systems according to traditional esoteric maps while remaining production-grade.

Observed form first.  
Mechanical names primary.  
Symbolic rationale recoverable.  
Human sovereignty over every forced mapping.  
Corpus open for expansion.

---

## What this is

A self-contained **Hermes** skill (with **OpenClaw** edition) that treats software architecture as a correspondence system. Functional requirements are mapped onto established traditional frameworks. The resulting structure carries explicit symbolic coherence and full provenance while staying usable by ordinary engineering tools.

Esoteric names remain latent by default. Public interfaces use clear mechanical names. Symbolic annotations live in documentation headers and provenance records.

## Hosts

| Host | Install path | Install |
|------|--------------|----------|
| Hermes | `~/.hermes/skills/orchestra` | `./install.sh` |
| OpenClaw | `~/.openclaw/skills/orchestra` | `./install.sh --target ~/.openclaw/skills/orchestra` |

Same `SKILL.md` contract. Same CLI. Different install roots and state isolation paths.

## Quick start

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
cd Abraxas-Orchestra-Hermes
./install.sh
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py check
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py do list-frameworks
python3 ~/.hermes/skills/orchestra/scripts/orchestra.py do structure -f tree-of-life -c "intake,synthesis,output"
```

## Supported frameworks (11)

| Key | Primary use |
|-----|-------------|
| `tree-of-life` | Hierarchical modules, paths, worlds |
| `alchemical-stages` | Pipelines and refinement loops |
| `elder-futhark` | Subsystem boundaries and intent names |
| `planetary-spheres` | Domain separation and ownership |
| `iching-hexagrams` | Discrete state machines and regimes |
| `solomonic` | Authority tiers, offices, sealed contracts |
| `peircean-signs` | Sign-relation / representation discipline |
| `numogram` | Zones, syzygies, time-circuit, gates |
| `sacred-geometry` | Nesting limits, adjacency, self-similarity |
| `enochian` | Watchtowers, Aethyrs, Calls as tokens |
| `chaos-magic` | Meta-paradigm, sigils, banishing, results gates |

## CLI

```bash
python3 scripts/orchestra.py do list-frameworks
python3 scripts/orchestra.py do structure -f <framework> [-c concerns] [-o overlay] [--out DIR]
python3 scripts/orchestra.py do project -f <framework> [...]   # pragmatic collapse
python3 scripts/orchestra.py check
```

## Core rules

- Dual naming: mechanical primary; symbolic secondary and recoverable
- Fail-closed: weak mappings marked; no silent invention
- Pragmatic projection when pure mapping harms maintainability
- No auto-promotion into Abraxas canon
- Compatible with Abraxas SEED and governance patterns
- Corpus open for additive expansion

## Example

`examples/signal-forager-skeleton/` — working forage pipeline on Tree of Life + alchemical overlay.

```bash
cd examples/signal-forager-skeleton && python3 run_demo.py
```

## Layout

```
SKILL.md                 # Hermes/OpenClaw operating contract
orchestra.manifest.yaml  # Skill manifest (hosts, frameworks, intents)
install.sh               # Atomic installer (Hermes or OpenClaw target)
scripts/orchestra.py     # CLI
references/              # Framework correspondence tables (open corpus)
schemas/                 # JSON schemas for artifacts
docs/DESIGN.md           # Design specification
docs/OPENCLAW.md         # OpenClaw packaging notes
examples/                # Worked examples
```

## License

Proprietary — all rights reserved.

---

Structure before narrative.  
Evidence before authority.  
Governance before autonomy.
