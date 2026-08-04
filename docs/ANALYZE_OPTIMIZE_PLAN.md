# Plan: Repo analyze → map → optimize

Status: **Phase A+B+C shipped (0.2.0 / 0.3.0)** · Target skill: Abraxas Orchestra · Hosts: Hermes, OpenClaw  
Parent version baseline: `0.3.0` · Implementation owner: Cursor / local agent  
Emit-only `structure`/`diagram` contract preserved; `analyze`/`optimize` are additive commands.

---

## 1. Goal

Given a **repository or codebase path**, Orchestra should:

1. **OBSERVE** the mechanical structure (modules, packages, import/call edges).
2. **MAP** observed units onto existing framework loci (`schemas/frameworks.v1.json`) with fail-closed scoring.
3. **OPTIMIZE** only where the map is clean — first as a plan, later as optional apply.

This is an extension of the current generative skill (structure / project / diagram). It does **not** invent symbolic loci. It does **not** rewrite trees without an explicit apply gate.

---

## 2. Non-goals (explicit)

- Runtime ritual / operative magic systems
- Network fetch of remote repos (local path only for v1)
- Multi-language AST intelligence in v1 (Python first)
- Silent “improvements” on `FORCED` or `WEAK` mappings
- Auto-canon promotion into Abraxas
- Replacing `structure` / `diagram` emission paths

---

## 3. Invariants (must hold in every phase)

| ID | Invariant |
|----|-----------|
| I1 | Mechanical names remain the filesystem / public API unless operator requests otherwise |
| I2 | Symbolic names only from `schemas/frameworks.v1.json` + `references/` — never invented |
| I3 | Every mapping carries strength: `STRONG` \| `ADEQUATE` \| `WEAK` \| `FORCED` |
| I4 | `FORCED` / `NOT_COMPUTABLE` blocks optimize-apply; plan may list them as blocked |
| I5 | Writes outside analysis `--out` require `--apply` and path jail (same spirit as `install.sh`) |
| I6 | OBSERVED / INFERRED / SPECULATIVE labels on analysis artifacts |
| I7 | Stdlib-only for v1 CLI path (no new third-party runtime deps) |
| I8 | Human sovereignty: dry-run default for any mutating command |

---

## 4. Phased delivery

### Phase A — `analyze` (read-only) · ship first

**CLI**

```text
python3 scripts/orchestra.py analyze \
  --path DIR \
  [-f FRAMEWORK] \
  [-o OVERLAY] \
  [--lang python] \
  [--max-depth N] \
  [--out DIR]
```

**Behavior**

1. Walk `DIR` (respect `--max-depth`; skip VCS/cache dirs: `.git`, `__pycache__`, `.venv`, `node_modules`, etc.).
2. Build **observed graph**:
   - nodes: packages/modules (mechanical paths)
   - edges: import relationships (Python `ast` parse; best-effort, mark parse failures)
3. If `-f` given, propose mappings from node concerns → loci via existing `_select_loci`-style matching; score strength.
4. If no `-f`, optionally suggest candidate frameworks by structural shape (SPECULATIVE) without committing a map.
5. Write under `--out` (required for files; else stdout JSON summary):

| File | Content |
|------|---------|
| `analysis.json` | schema `orchestra-analysis.v1` |
| `architecture.json` | observed + proposed graph (`orchestra-diagram.v1` compatible where possible) |
| `architecture.html` | reuse diagram HTML emitter |
| `architecture.mmd` | Mermaid of observed (and optional mapped) graph |
| `correspondence-table.json` | only if `-f` produced mappings |

**Exit codes**

| Code | Meaning |
|------|---------|
| 0 | Analysis complete; map CLEAN or no `-f` |
| 1 | Analysis complete with WEAK/FORCED mappings present |
| 2 | NOT_COMPUTABLE (bad path, empty tree, unknown framework) |

**Acceptance (Phase A)**

- [x] `analyze --path <fixture>` produces `analysis.json` with `provenance.kind` fields
- [x] Parse errors recorded per file; do not abort whole run
- [x] Path jail: refuse system roots / outside allowed root without flag (mirror installer policy for safety)
- [x] Unit tests with a tiny fixture package under `tests/fixtures/mini_pkg/`
- [x] Smoke step or dedicated test invokes analyze on fixture
- [x] Docs: this file + SKILL.md command list + README how-to row

---

### Phase B — `optimize` plan (no tree writes)

**CLI**

```text
python3 scripts/orchestra.py optimize \
  --from analysis.json \
  [--out DIR] \
  [--min-strength ADEQUATE]
```

**Behavior**

1. Load Phase A artifact.
2. Emit ordered **refactor plan** only for mappings ≥ `--min-strength` (default `ADEQUATE`).
3. Plan items are descriptive and mechanical, e.g.:
   - suggest package boundary aligned to locus X
   - suggest rename mechanical module to match dual-name table (optional)
   - suggest extracting a stage boundary between nodes on a flow
4. Blocked items listed with reason (`FORCED`, weak import evidence, etc.).
5. Write `optimize-plan.json` + `OPTIMIZE.md` (human).

**Acceptance (Phase B)**

- [x] Plan references only OBSERVED nodes + schema loci
- [x] No file under the analyzed repo is modified
- [x] Empty plan when nothing meets strength threshold (exit 0 with explicit message)

---

### Phase C — `optimize --apply` (gated mutation)

**CLI**

```text
python3 scripts/orchestra.py optimize \
  --from analysis.json \
  --apply \
  [--dry-run] \
  [--backup-dir DIR]
```

**Behavior**

1. Default: if `--apply` missing → plan only (Phase B).
2. Recommended: `--apply` alone = dry-run of apply; `--apply --confirm` required for writes.
3. Backup touched paths before write.
4. Apply only plan steps marked `safe_apply: true` (mechanical renames/moves within root; no content invention).
5. Refuse apply when any critical FORCED mapping is in the selected set.

**Acceptance (Phase C)**

- [x] Path jail identical to install policy (analyzed root + system prefix deny)
- [x] Backup + restore path documented (`RESTORE.md`, `docs/SECURITY.md`)
- [x] Tests use temp dirs only
- [x] SECURITY.md note updated for write surface

---

## 5. Schemas

### `orchestra-analysis.v1` (new)

```json
{
  "schema": "orchestra-analysis.v1",
  "path": "/abs/path",
  "language": "python",
  "framework": "enochian|null",
  "secondary_overlay": null,
  "status": "CLEAN|WEAK_MAPPINGS|FORCED_CORRESPONDENCE|NOT_COMPUTABLE|OBSERVED_ONLY",
  "nodes": [
    {
      "id": "pkg.module",
      "path": "relative/path.py",
      "kind": "module|package",
      "provenance": "OBSERVED",
      "imports": ["other.module"],
      "parse_error": null
    }
  ],
  "edges": [
    { "from": "a", "to": "b", "kind": "import", "provenance": "OBSERVED" }
  ],
  "mappings": [],
  "provenance": {
    "operator": "orchestra-cli",
    "timestamp": "ISO-8601",
    "skill_version": "0.1.x"
  }
}
```

Reuse mapping entry shape from `correspondence-table.v1` when `-f` is set.

### `orchestra-optimize-plan.v1` (new)

```json
{
  "schema": "orchestra-optimize-plan.v1",
  "from_analysis": "analysis.json",
  "min_strength": "ADEQUATE",
  "steps": [
    {
      "id": "step-1",
      "action": "suggest_boundary|suggest_rename|suggest_extract",
      "targets": ["module.id"],
      "locus": "symbolic_or_mechanical",
      "strength": "ADEQUATE",
      "safe_apply": false,
      "notes": ""
    }
  ],
  "blocked": [],
  "provenance": {}
}
```

Add JSON Schema files under `schemas/` when implementing Phase A/B.

---

## 6. Code touch list (implementation map)

| Path | Change |
|------|--------|
| `scripts/orchestra.py` | Register `analyze`, `optimize`; wire parsers |
| `scripts/analyze_repo.py` (new) | Walk, AST import graph, analysis.json builder |
| `scripts/optimize_plan.py` (new) | Plan synthesis from analysis |
| `scripts/diagram_emit.py` | Accept observed graphs (not only loci sequences) |
| `scripts/diagram_mermaid.py` | Same |
| `schemas/analysis.v1.schema.json` (new) | Phase A |
| `schemas/optimize-plan.v1.schema.json` (new) | Phase B |
| `tests/fixtures/mini_pkg/` (new) | Tiny Python package for tests |
| `tests/test_analyze.py` (new) | Phase A tests |
| `tests/test_optimize.py` (new) | Phase B (+ C later) |
| `SKILL.md` | Commands + when-to-use analyze/optimize |
| `README.md` | How-to rows |
| `docs/SECURITY.md` | Write surface when Phase C lands |
| `orchestra.manifest.yaml` | intents list |
| `CHANGELOG.md` / `docs/RELEASE_NOTES.md` | Per phase version bump |

Keep **stdlib only** for analyze/optimize v1.

---

## 7. Algorithm notes (Phase A detail)

### Walk

- Include: `*.py` under `--path`
- Exclude dir names: `.git`, `.hg`, `.svn`, `__pycache__`, `.venv`, `venv`, `node_modules`, `.tox`, `.mypy_cache`, `.ruff_cache`, `dist`, `build`, `.eggs`
- Cap files processed (`--max-files`, default e.g. 2000) to avoid pathological trees

### Import edges (Python)

- `ast.parse` each file; collect `ast.Import` / `ast.ImportFrom`
- Resolve relative imports best-effort against package layout
- Unresolved imports: keep as edge to external id with `provenance: OBSERVED` and `external: true` — do not map externals to loci by default

### Mapping heuristic

- Tokenize module path + docstring first line + top-level names
- Match against framework `default_loci` mechanical/symbolic/note strings (same spirit as `_select_loci`)
- Strength:
  - `STRONG` — direct mechanical name match or clear single locus
  - `ADEQUATE` — path segment / concern overlap
  - `WEAK` — loose token overlap only
  - `FORCED` — operator-required concern with no locus (should be rare in analyze unless concerns passed explicitly)

### Diagram

- Prefer **import topology** layout for observed graphs (not only linear sequence)
- Linear sequence layout remains for pure loci emission (`structure`)

---

## 8. Cursor execution order

Work in this order; stop at phase gates.

1. **Fixture** — `tests/fixtures/mini_pkg/` with 3–4 modules and clear import chain  
2. **`analyze_repo.py`** — walk + AST graph → `analysis.json`  
3. **Wire `analyze` CLI** + tests  
4. **Optional `-f` mapping** into correspondence table + diagram bundle  
5. **`optimize_plan.py`** + `optimize` CLI (plan only)  
6. **Docs/SKILL/manifest/CHANGELOG** for the version that ships A (and B if same train)  
7. **Phase C** only after explicit operator request and security note update  

Versioning suggestion:

- Phase A alone → `0.2.0` (new command surface)
- Phase B → `0.2.1` or fold into `0.2.0` if same PR train
- Phase C → `0.3.0` (mutating capability)

---

## 9. Test plan (minimum)

| Test | Asserts |
|------|---------|
| `test_analyze_fixture_graph` | nodes ≥ N, edges ≥ 1, status OBSERVED_ONLY or CLEAN |
| `test_analyze_unknown_path` | exit 2 |
| `test_analyze_with_framework` | mappings array present; no invented symbolic names |
| `test_analyze_skips_venv` | no nodes under `.venv` |
| `test_optimize_plan_no_write` | repo mtime unchanged |
| `test_optimize_blocks_forced` | forced mappings appear in `blocked` |

---

## 10. Security

- Analyze is read-only on `--path`; writes only to `--out`
- Optimize apply (Phase C): path must resolve under analyzed root; system prefix deny list; backup before mutate
- No network in analyze/optimize paths
- Document in `docs/SECURITY.md` when Phase C merges

---

## 11. Definition of done (operator)

Phase A is done when:

1. `bash scripts/smoke.sh` green including analyze fixture  
2. Cursor/agent can run analyze on Abraxas-Orchestra-Hermes itself and get a coherent graph  
3. SKILL.md lists `analyze` with fail-closed language  
4. This plan’s Phase A checkboxes are checked in a follow-up commit or issue  

Phase B/C done when their sections’ checkboxes are checked and version bumped accordingly.

---

## 12. References

- Current emit CLI: `scripts/orchestra.py` (`structure`, `project`, `diagram`)
- Loci source: `schemas/frameworks.v1.json`
- Diagram emitters: `scripts/diagram_emit.py`, `scripts/diagram_mermaid.py`
- Install path jail precedent: `install.sh`
- Agent contract: `SKILL.md`, `references/agent-posture.md`
