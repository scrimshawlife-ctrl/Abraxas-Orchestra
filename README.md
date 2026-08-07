# Abraxas Orchestra

<p align="center">
  <img src="assets/hero.svg" alt="Abraxas Orchestra — symbolic architecture skill" width="720"/>
</p>

<p align="center">
  <strong>Hermes + OpenClaw coding-agent skill</strong> for structuring software with traditional symbolic maps
</p>

Version **0.4.1** · Skill name: `orchestra` · Python ≥ 3.11 · Offline CLI · License: [Apache-2.0](LICENSE)

---

## What this is (plain English)

**Orchestra** is a local skill that helps coding agents (and humans) organize software the way traditional systems organize meaning — Tree of Life, alchemy stages, runes, planetary spheres, I Ching, Solomonic ranks, Peircean signs, Numogram, sacred geometry, Enochian, Chaos Magic.

In practice it does three things:

1. **Scaffold** — emit a dual-named project skeleton (mechanical name + symbolic name) from a chosen map  
2. **Diagram** — write HTML, JSON, and Mermaid architecture graphs next to that skeleton  
3. **Analyze → plan → optionally rename** — read a local Python tree, map modules onto a framework when the fit is honest, propose renames, and only write files when you explicitly confirm

It is **not** a network service, a magic runtime, or a silent auto-refactorer. Weak or forced mappings are labeled and can stop the pipeline. You stay in control of anything that changes the filesystem.

---

## How to use

### Install once

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh                    # must print SMOKE OK
bash install.sh --dry-run
bash install.sh                          # → ~/.hermes/skills/orchestra
# OpenClaw:
# bash install.sh --target ~/.openclaw/skills/orchestra
```

After install, the host discovers the skill from `SKILL.md` (`name: orchestra`).

### Day-to-day commands

All commands work from the repo or from the install root (`~/.hermes/skills/orchestra`).

**List maps**

```bash
python3 scripts/orchestra.py list
```

**Scaffold a dual-named layout** (example: Tree of Life, three concerns)

```bash
python3 scripts/orchestra.py structure \
  -f tree-of-life \
  -c "intent,synthesis,output" \
  --out /tmp/orch-skel
```

Writes under `--out`:

- `SKELETON.md` + per-module stubs  
- `correspondence-table.json`  
- `architecture.html` · `architecture.json` · `architecture.mmd` (auto)

**Project mode** (collapse oversized / forced maps before emit):

```bash
python3 scripts/orchestra.py project -f enochian -o chaos-magic --out /tmp/orch-proj
```

**Diagram only** (no skeleton files):

```bash
python3 scripts/orchestra.py diagram -f numogram --out /tmp/orch-diag
```

**Analyze an existing Python package**

```bash
python3 scripts/orchestra.py analyze \
  --path /path/to/your/package \
  -f tree-of-life \
  --out /tmp/orch-an
```

Produces `analysis.json` plus the same diagram trio. Mapping strengths: `STRONG` / `ADEQUATE` / `WEAK` / `FORCED`. Weak or forced maps fail closed (non-zero exit) so agents do not “paper over” bad fits.

**Optimize plan (read-only)**

```bash
python3 scripts/orchestra.py optimize \
  --from /tmp/orch-an/analysis.json \
  --out /tmp/orch-plan
```

Writes `optimize-plan.json` and `OPTIMIZE.md`. **No source tree changes.**

**Apply gated moves (rename / promote / flatten)**

```bash
# Dry-run first
python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --apply
# Optional: --steps step-1,step-3  or  --actions suggest_rename,suggest_boundary

# Only when you mean it — backs up, then writes; optional re-analyze
python3 scripts/orchestra.py optimize \
  --from /tmp/orch-an/analysis.json \
  --apply --confirm --refresh
```

### When an agent should call this skill

Use Orchestra when the user wants:

- architecture shaped by a traditional symbolic map  
- dual naming (code identifiers + symbolic loci) with provenance  
- automatic Mermaid/HTML/JSON diagrams for a mapped design  
- a fail-closed read of a Python repo before any rename plan  

Agents: prefer `structure` / `project` / `analyze` with `--out` over inventing ad-hoc Mermaid. Do not invent loci that are not in `schemas/frameworks.v1.json`.

### Integrity check

```bash
python3 scripts/orchestra.py check
python3 scripts/bump_version.py check
```

---

## Quick start (minimal)

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh
python3 scripts/orchestra.py list
python3 scripts/orchestra.py structure -f tree-of-life -c "intent,synthesis,output" --out /tmp/orch-skel
```

Full deploy path (Hermes/OpenClaw): [`docs/DEPLOY.md`](docs/DEPLOY.md)  
Publish freeze: [`docs/COMPLETION.md`](docs/COMPLETION.md) · Public debut: [`docs/PUBLIC_RELEASE.md`](docs/PUBLIC_RELEASE.md)

---

## Release notes

**Current: 0.4.1** — integrity CI floors, apply module split, framework-fit guide (see `CHANGELOG.md`). Prior: [0.4.0](docs/RELEASE_NOTES.md#040--2026-08-05) broader `safe_apply`.

| Theme | What landed |
|-------|-------------|
| Semver | `docs/SEMVER.md`, `scripts/bump_version.py`, CI parity |
| Analyze | OBSERVED Python import graph + optional framework map |
| Optimize | Plan only by default; `--apply --confirm` gated rename/promote/flatten + backup |
| Diagrams | Auto HTML/JSON/Mermaid on structure/project/analyze `--out` |
| Release | `.github/workflows/release.yml` on tag push |

Narrative: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md) · Changelog: [`CHANGELOG.md`](CHANGELOG.md)

---

## Frameworks

Eleven maps ship in `schemas/frameworks.v1.json`:

`tree-of-life` · `alchemical-stages` · `elder-futhark` · `planetary-spheres` · `iching-hexagrams` · `solomonic` · `peircean-signs` · `numogram` · `sacred-geometry` · `enochian` · `chaos-magic`

Human-readable tables: `references/`. Agent posture when filling stubs: `references/agent-posture.md`.

---

## Layout

```text
SKILL.md                 # Agent contract + triggers
scripts/orchestra.py     # CLI entry
scripts/bump_version.py  # Semver parity tool
scripts/publish.sh       # Operator publish helper
scripts/smoke.sh         # Production smoke
references/              # Framework tables + agent-posture
schemas/                 # correspondence, frameworks, analysis, optimize-plan
examples/                # signal-forager; enochian-chaos
tests/                   # stdlib unittest + fixtures
docs/                    # DESIGN, DEPLOY, COMPLETION, SEMVER, …
install.sh               # Atomic installer (path jail)
LICENSE / NOTICE         # Apache-2.0
```

---

## Documentation map

**Canonical (source of truth for the current tree):**

| Doc | Role |
|-----|------|
| `VERSION` | Single version number for the package |
| `CHANGELOG.md` | Machine-oriented version history |
| `docs/SECURITY.md` | Live threat model and write surfaces |
| `SKILL.md` | Agent contract + current commands |
| `README.md` | Humans + agents (this file) |
| `docs/DESIGN.md` | Current design rationale / executable surface |
| `docs/SEMVER.md` | Version bump policy |
| `docs/DEPLOY.md` | Install and host wiring |

**Supporting (still accurate, not version history):**

| Doc | Audience |
|-----|----------|
| `docs/CI.md` | Actions + branch protection |
| `docs/FRAMEWORK_FIT.md` | Which map to use; strength labels |
| `docs/ANALYZE_OPTIMIZE_PLAN.md` | Analyze → optimize design (shipped) |
| `docs/OPENCLAW.md` | OpenClaw packaging |
| `docs/COMMUNITY.md` | Community-skills notes |
| `references/agent-posture.md` | How agents fill skeletons |
| `docs/SECURITY_AUDIT.md` | Audit history + status addenda (see SECURITY.md for live rules) |

**Historical / freeze notes (not the live CLI surface):**

| Doc | Role |
|-----|------|
| `docs/COMPLETION.md` | Production freeze checklist (point-in-time) |
| `docs/PUBLIC_RELEASE.md` | Public debut notes |
| `docs/RELEASE_NOTES.md` | Narrative releases |
| `docs/RELEASE_BODY_v*.md` | Tag release body drafts |
| `docs/RESTORE_NOTE.md` | 0.3.2 CLI restore incident marker |

---

## Safety and requirements

- **Runtime:** Python 3.11+ standard library only for the CLI  
- **Network:** Not required for check / structure / project / diagram / analyze / optimize  
- **Install jail:** Refuses system paths and targets outside `$HOME` unless `--allow-outside-home`  
- **Writes:** Installer backs up then swaps; optimize apply requires `--confirm`; prefer dry-run first  
- **State:** Keep mutable agent state outside the skill install root  
- **License:** Apache-2.0 — see `LICENSE` and `NOTICE`  

Details: [`docs/SECURITY.md`](docs/SECURITY.md) (live) · [`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md) (history)

---

## Links

- Repo: https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra  
- Deploy: [`docs/DEPLOY.md`](docs/DEPLOY.md)  
- Freeze: [`docs/COMPLETION.md`](docs/COMPLETION.md)  
- Semver: [`docs/SEMVER.md`](docs/SEMVER.md)  
- Release notes: [`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md)  
