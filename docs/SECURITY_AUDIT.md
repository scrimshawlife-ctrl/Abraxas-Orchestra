# Security audit — Abraxas Orchestra

**Live threat model (always current):** [`SECURITY.md`](SECURITY.md)

This file is the **audit history** for public packaging. For day-to-day operator rules and the full 0.4.0 write-surface description (including promote / flatten / `--steps` / `--actions`), use **`docs/SECURITY.md`**.

---

## Status at 0.4.0 (2026-08-06)

| Rating | Finding |
|--------|---------|
| **Acceptable for public skill release** at tree VERSION **0.4.0** | No remote code execution surface in CLI; no undeclared network; no secret store; optimize apply remains gated |

### Addendum — 0.4.0 broader `safe_apply`

| Check | Result |
|-------|--------|
| Network in apply path | **None** |
| Writes without `--confirm` | **None** (`--apply` alone is dry-run) |
| Rename / promote / flatten | Mechanical only; destinations under analyzed root |
| Selective apply | `--steps` / `--actions` still require `safe_apply: true` |
| FORCED mappings | **Refuse** apply |
| Content invention | **None** — no `suggest_extract` apply |
| Backup / restore | `apply-report.json` + `RESTORE.md` under `--backup-dir` |
| Path jail | Analyzed root + system prefix deny (installer + analyze + apply) |

Details and operator rules: [`SECURITY.md`](SECURITY.md) (optimize apply write surface, threat model v0.4.0).

### Package identity note

Canonical repository: `https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra`  
(Older packaging strings that said `Abraxas-Orchestra-Hermes` were packaging drift, not a second product.)

---

## Historical — 0.1.3 public debut (2026-08-04)

**Scope:** Package at `main` for first public release packaging  
**Method:** Static review of installer, CLI, examples, schemas, docs; smoke execution; path-refusal tests  

### Summary (0.1.3)

| Rating | Finding |
|--------|---------|
| **Acceptable for public skill release** after installer path hardening in 0.1.3 | No remote code execution surface in CLI; no undeclared network; no secret store |

### Surfaces reviewed (0.1.3)

#### 1. CLI (`scripts/orchestra.py`)

| Check | Result |
|-------|--------|
| Network (`requests`, `urllib`, sockets) | **None** |
| `eval` / `exec` / dynamic import of user code | **None** |
| Dependencies | **Stdlib only** |
| `--out` write | Writes under operator-supplied path via `Path.expanduser().resolve()` — **expected**; operator-controlled |
| JSON load | Local skill-root schema only |

**Residual risk:** Operator can point `--out` at sensitive directories they already can write. Mitigate with least-privilege OS user for agent hosts.

#### 2. Installer (`install.sh`)

| Check | Result |
|-------|--------|
| Remote fetch at install | **None** |
| Prior `eval` style | **Removed** in 0.1.3 — `run_cmd` uses argv array |
| `rm -rf` on target | Present (atomic swap); **gated** by `validate_target` |
| Target outside `$HOME` | **Blocked** unless `--allow-outside-home` |
| System prefixes (`/etc`, `/usr`, …) | **Blocked** |
| Install to `$HOME` root | **Blocked** |
| Staging | `mktemp` + `trap` cleanup on failure |

**Residual risk:** With `--allow-outside-home`, a mistaken target can still destroy that directory after backup-of-prior-only-if-exists. Documented; prefer never using the flag on shared machines.

#### 3. Examples

| Check | Result |
|-------|--------|
| Credentials / API keys | **None** |
| Network | **None** |
| Writes | Local `_demo_out/` under example dirs |

#### 4. Supply chain

| Check | Result |
|-------|--------|
| Third-party Python packages | **None** for CLI |
| CI | Runs unittest + smoke on checkout only |

#### 5. Content / misuse

Symbolic framework text is architectural metaphor. Package does **not** implement remote invocation of external systems. Public README states what the skill is and is not.

### Findings fixed in 0.1.3

1. **P1** Installer could target any writable path → home-jail + system prefix deny + explicit escape hatch  
2. **P2** Installer used `eval` for dry-run/real commands → replaced with `run_cmd` argv form  
3. **P2** Public release still carried proprietary LICENSE → Apache-2.0 for hub eligibility  

### Findings accepted (document only)

1. **`--out` unrestricted** within filesystem permissions — intentional CLI tool behavior  
2. **Backup only of previous skill target** — not a full system backup  
3. **Operator tag / release publish** remains human-gated  

### Public debut recommendation (historical)

Ship **0.1.3** as the first public-tagged release after smoke green, path-refusal checks, Apache-2.0 LICENSE + NOTICE, `.github/SECURITY.md`, and annotated tag `v0.1.3`. See `docs/PUBLIC_RELEASE.md`.

---

## Historical addendum — 0.3.0 optimize apply

| Check | Result |
|-------|--------|
| Network in apply path | **None** |
| Writes without `--confirm` | **None** (`--apply` is dry-run) |
| Path jail | Destinations under analyzed `path`; system backup-dir denied |
| FORCED mappings | **Refuse** apply |
| Content invention | **None** — mechanical rename/move + import-line alias rewrite only |
| Backup / restore | `apply-report.json` + `RESTORE.md` under `--backup-dir` |

Superseded in detail by the **0.4.0** addendum above and by live [`SECURITY.md`](SECURITY.md).
