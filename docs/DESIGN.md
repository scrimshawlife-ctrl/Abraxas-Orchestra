# Abraxas Orchestra — Design Specification

**Status**: Hermes/OpenClaw coding-agent skill — design surface + executable CLI + open corpus  
**Version target**: 0.1.0  
**Date**: 2026-08-04  
**Repo**: scrimshawlife-ctrl/Abraxas-Orchestra-Hermes  

This document is the authoritative design record for the first public surface of the skill.

---

## 1. Purpose

Abraxas Orchestra is a Hermes and OpenClaw coding-agent skill that maps software architecture, module organization, interfaces, and data-flow stages onto traditional esoteric and symbolic systems. The resulting structure remains production-usable while carrying explicit symbolic coherence and recoverable provenance.

The skill treats architecture as a correspondence system. Functional requirements are projected onto a chosen traditional framework. The code becomes a living diagram of that map.

Primary value for Abraxas-v2.0 and related systems:
- Forces hierarchical and polar thinking through established maps
- Creates navigable, mnemonic structure that survives long-lived projects
- Aligns with existing rune, governance, and Peircean sign work
- Keeps esoteric names latent by default so mechanical interfaces stay clean

---

## 2. Scope of v0.1

**In scope**
- Framework selection and explicit correspondence tables
- Dual-named directory and module skeletons
- Interface / path generation that respects the chosen map
- Pragmatic projection / collapse when pure mapping harms engineering quality
- Provenance annotations that recover the original symbolic rationale
- Fail-closed behavior on weak or forced correspondences
- Open corpus under `references/` for traditional systems
- Hermes and OpenClaw install packaging

**Explicitly out of scope for v0.1**
- Full multi-agent orchestration runtime
- Automatic mutation of Abraxas canon
- Runtime execution of symbolic rules as side-effecting code
- Audience-facing occult labeling in generated prompts or public APIs

Later versions may expand the Orchestra surface. The v0.1 contract stays stable.

---

## 3. Supported Frameworks (Current)

1. **Tree of Life** (default primary) — Sephirot, Paths, Four Worlds
2. **Alchemical stages** — Nigredo → Rubedo pipelines
3. **Elder Futhark** — aettir boundaries and rune intent names
4. **Planetary / elemental spheres** — domain ownership
5. **I Ching (curated)** — discrete state machines / regimes
6. **Solomonic hierarchy** — ranks, offices, sealed contracts
7. **Peircean signs** — Icon/Index/Symbol and related trichotomies
8. **Numogram** — zones, syzygies, time-circuit, gates
9. **Sacred geometry** — nesting limits, Platonic adjacency, self-similarity
10. **Enochian** — Watchtowers, Aethyrs, Calls as invocation tokens
11. **Chaos Magic** — meta-paradigm, sigilization, banishing, results gates

The corpus remains deliberately open. Additional traditional systems continue to be researched and added under `references/` without requiring changes to the core operating contract.

This repository is a **Hermes and OpenClaw coding-agent skill**. Install roots differ by host; the operating contract (`SKILL.md`) and CLI are shared.

---

## 4. Operating Sequence

When the skill is activated:

1. Distill the request into OBSERVED / INFERRED / SPECULATIVE labels.
2. Propose one or two primary frameworks with short rationale. Accept operator override.
3. Produce an explicit correspondence table mapping functional concerns onto the chosen map.
4. Emit a dual-named skeleton (mechanical name primary, symbolic name secondary).
5. Surface the engineering cost of every non-trivial correspondence.
6. Offer a pragmatic projection when pure mapping would produce baroque or unmaintainable structure.
7. Refuse silent invention. Weak evidence returns `NOT_COMPUTABLE` or an explicit human decision gate.

---

## 5. Dual Naming Convention

Every public module, package, or interface carries:

- A clear mechanical name that describes its engineering role
- An optional symbolic name that encodes its place in the chosen map

Mechanical names are the primary interface used by imports, type checkers, and operators. Symbolic names appear in documentation headers, provenance comments, and internal ledgers.

---

## 6. Fail-Closed and Pragmatic Projection

The skill never invents structure to satisfy a symbolic map.

If a required functional concern has no clean correspondence, or if forcing a correspondence would violate type safety, testability, or long-term maintainability, the skill:

- Marks the mapping as weak
- Returns a clear `NOT_COMPUTABLE` or `FORCED_CORRESPONDENCE` status
- Offers a pragmatic collapse (flat modules, conventional layering, or reduced symbolic surface)

Human operators retain final authority over whether a forced mapping is accepted.

---

## 7. Integration Points

- Compatible with existing Abraxas SEED response discipline and governance lanes
- Can be invoked from Abraxas Orchestrator as a specialized structuring step
- Output skeletons are valid input for Senior Python Architect and Hermes cracked-python flows
- Correspondence tables become first-class provenance artifacts
- Discoverable as an OpenClaw skill under `~/.openclaw/skills/orchestra`

---

## 8. OpenClaw Edition

A permanent `openclaw` branch will carry an edition that installs under `~/.openclaw/skills/orchestra`. Mutable runtime state stays outside the skill package. The reference mappings and core contract remain aligned with the Hermes edition.

Until the branch is cut, install from `main` with:

```bash
./install.sh --target ~/.openclaw/skills/orchestra
```

---

## 9. Versioning and Release Gate

- Current target: 0.1.0
- Semantic versioning thereafter
- CHANGELOG.md records every public change
- Corpus expansion (new traditional systems) is additive and does not bump major version unless the operating contract itself changes

---

## 10. Corpus Expansion Policy

The `references/` directory is intentionally open. New traditional systems may be added after research and operator review. Each new system receives:

- A dedicated markdown mapping file
- An entry in the manifest frameworks list (when stable)
- A short note in CHANGELOG.md under the appropriate version

No change to SKILL.md operating sequence is required for pure additive expansion.
