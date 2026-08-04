# Abraxas Orchestra

**Hermes + OpenClaw coding-agent skill** for symbolic code architecture  
*v0.1.1 — design surface, open corpus, executable CLI, schema-validated check*

Structure modules, pipelines, interfaces, and agent systems according to traditional esoteric maps while remaining production-grade.

Observed form first.  
Mechanical names primary.  
Symbolic rationale recoverable.  
Human sovereignty over every forced mapping.  
Corpus open for expansion.

---

## What this is

A self-contained skill that maps software architecture concerns onto traditional symbolic systems (Tree of Life, alchemy, runes, planetary spheres, I Ching, Solomonic hierarchy, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic) and emits dual-named skeletons with provenance tables.

Hosts: **Hermes** and **OpenClaw** coding agents.

---

## Quick start

```bash
# Validate skill integrity (files + schema emission)
python3 scripts/orchestra.py check

# List frameworks
python3 scripts/orchestra.py do list-frameworks

# Emit dual-named skeleton
python3 scripts/orchestra.py do structure -f tree-of-life

# With secondary overlay and disk write
python3 scripts/orchestra.py do structure -f enochian -o chaos-magic \
  -c "edge_intake,domain_entry,root_truth_seal" --out /tmp/orch-out

# Pragmatic projection (collapse oversized maps)
python3 scripts/orchestra.py do project -f tree-of-life
```

### Install (atomic)

```bash
bash install.sh --dry-run
bash install.sh                          # → ~/.hermes/skills/orchestra
bash install.sh --target ~/.openclaw/skills/orchestra
```

---

## Examples

`examples/signal-forager-skeleton/` — working forage pipeline on Tree of Life + alchemical overlay.

`examples/enochian-chaos-skeleton/` — dual-named Enochian domains with Chaos Magic overlay (seals, Calls, banishing posture).

```bash
cd examples/signal-forager-skeleton && python3 run_demo.py
python3 scripts/orchestra.py do structure -f enochian -o chaos-magic \
  -c "edge_intake,domain_entry,root_truth_seal"
```

---

## Layout

```
SKILL.md                 # Hermes/OpenClaw operating contract
orchestra.manifest.yaml  # Skill discovery + install targets
scripts/orchestra.py     # CLI (structure / project / check)
references/              # Framework correspondence tables (open corpus)
schemas/                 # Correspondence table schema
examples/                # Worked examples
docs/DESIGN.md           # Authoritative design
docs/OPENCLAW.md         # OpenClaw packaging notes
install.sh               # Atomic installer
```

---

## Governance

Fail-closed on weak mappings. No silent pragmatic projection. Human sovereignty over forced correspondences. Corpus remains open for additive traditional systems.
