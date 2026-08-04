# Release notes

Narrative notes for operators and agents. Machine-oriented change lists live in [`CHANGELOG.md`](../CHANGELOG.md).

---

## 0.1.2 — 2026-08-04

**Status:** Production-ready for **private** Hermes / OpenClaw install  
**Skill name:** `orchestra` · **Python:** ≥ 3.11 · **Network:** not required for CLI

### Highlights

1. **Canonical framework data** — `schemas/frameworks.v1.json` is the single source of truth for all 11 framework loci and core-collapse sets. The CLI loads it at startup; do not re-embed tables in Python.
2. **Hardened packaging** — `scripts/smoke.sh`, stdlib unit tests (13), CI on 3.11/3.12, atomic installer with `--dry-run` / `--rollback` / `--target`.
3. **Deploy path** — Ordered host install steps in `docs/DEPLOY.md` (validate → dry-run → install → verify → wire agent).
4. **Worked examples** — Runnable signal-forager pipeline; Enochian + Chaos Magic structure skeleton with dual-named stubs.
5. **Docs for humans and agents** — README how-to, SKILL frontmatter, CONTRIBUTING framework-add checklist, agent posture rules.

### Frameworks (v0.1.2)

| Key | Title |
|-----|-------|
| `tree-of-life` | Tree of Life |
| `alchemical-stages` | Alchemical Stages |
| `elder-futhark` | Elder Futhark |
| `planetary-spheres` | Planetary Spheres |
| `iching-hexagrams` | I Ching (curated) |
| `solomonic` | Solomonic Hierarchy |
| `peircean-signs` | Peircean Signs |
| `numogram` | Numogram |
| `sacred-geometry` | Sacred Geometry |
| `enochian` | Enochian |
| `chaos-magic` | Chaos Magic |

### CLI surface

```bash
python3 scripts/orchestra.py check
python3 scripts/orchestra.py do list-frameworks
python3 scripts/orchestra.py do structure -f <framework> [-o <overlay>] [-c "a,b"] [--out DIR]
python3 scripts/orchestra.py do project -f <framework> [--out DIR]
```

### Upgrade from 0.1.1 / 0.1.0

```bash
git pull
bash scripts/smoke.sh
bash install.sh --dry-run
bash install.sh   # or --target for OpenClaw
```

Ensure `schemas/frameworks.v1.json` is present after pull. Installer and `check` both require it.

### Not in this release

- OSI relicense / public skill-hub listing (see `docs/COMMUNITY.md`)
- Dedicated `openclaw` git branch (use `--target`)
- Runtime ritual / network integrations (out of skill scope)
- Hero image binary may still need a local `git push` if `assets/hero.jpg` is missing on your mirror

### Optional pin

```bash
git tag -a v0.1.2 -m "Orchestra 0.1.2 production-ready private skill"
git push origin v0.1.2
```

---

## 0.1.1 — 2026-08-04

Schema enum coverage for all frameworks, `overlay_note` support, agent posture reference, Enochian/Chaos example surface, community compliance checklist. See `CHANGELOG.md`.

---

## 0.1.0 — 2026-08-04

First public design surface: dual-naming contract, open corpus, CLI structure/project/check, atomic installer, signal-forager example.
