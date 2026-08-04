# Abraxas Orchestra — Design Specification

**Status**: Hermes/OpenClaw coding-agent skill — design surface + executable CLI + open corpus  
**Version target**: 0.1.1  
**Date**: 2026-08-04  
**Repo**: scrimshawlife-ctrl/Abraxas-Orchestra-Hermes  

This document is the authoritative design record for the first public surface of the skill.

---

## 1. Purpose

Orchestra is a coding-agent skill that structures software architecture using traditional esoteric correspondence systems while remaining production-grade: dual naming, fail-closed gates, recoverable provenance, and pragmatic projection when pure maps become unmaintainable.

---

## 2. Scope of v0.1

**In scope**

- Eleven framework reference tables (open for expansion)
- CLI: `do list-frameworks`, `do structure`, `do project`, `check`
- Correspondence table schema + emission
- Atomic installer for Hermes and OpenClaw paths
- Worked examples (signal-forager; enochian-chaos structure)
- Schema validation inside `check` (v0.1.1)

**Explicitly out of scope for v0.1**

- Runtime ritual execution or operative magic
- Automatic promotion of SPECULATIVE maps to canon
- Networked multi-agent orchestration beyond local skill install

Later versions may expand the Orchestra surface. The v0.1 contract stays stable.

---

## 3. Dual naming

Every emitted locus carries:

- **mechanical** name — public, importable, conventional
- **symbolic** name — recoverable provenance into the chosen framework

Correspondence tables record strength (`STRONG` / `ADEQUATE` / `WEAK` / `FORCED`) and optional overlay notes.

---

## 4. Fail-closed and projection

Unknown frameworks, identical overlay=primary, and empty projected loci return `NOT_COMPUTABLE`.

`do project` may drop FORCED loci and collapse oversized maps to each framework’s core set. Projections are always recorded in the table; never silent.

---

## 5. Framework inventory

See `SKILL.md` and `references/`. Enochian includes Dee vs neo streams, seals taxonomy, Heptarchia, Parts of the Earth, and inverse (cacodemon) surfaces. Chaos Magic is the meta-paradigm overlay.

---

## 6. Host packaging

- Hermes: `~/.hermes/skills/orchestra`
- OpenClaw: `~/.openclaw/skills/orchestra` via `--target`
- Manifest kind: `hermes-openclaw-skill`

See `docs/OPENCLAW.md`.

---

## 7. Versioning

- Current target: 0.1.1
- Schema: `correspondence-table.v1` (enum covers all frameworks + composite)
- Corpus remains open; additive frameworks do not break v0.1 CLI contracts when registered in `FRAMEWORKS`, schema enum, manifest, and installer refs together.
