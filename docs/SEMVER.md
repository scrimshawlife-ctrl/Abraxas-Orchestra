# Semantic versioning

Orchestra follows [Semantic Versioning 2.0.0](https://semver.org/).

**Single source of truth:** the `VERSION` file at the repo root (`MAJOR.MINOR.PATCH` only).

All of these must match `VERSION` (enforced by CI `version-parity`):

| Location | Form |
|----------|------|
| `scripts/orchestra.py` | `VERSION = "x.y.z"` |
| `SKILL.md` frontmatter | `version: x.y.z` |
| `orchestra.manifest.yaml` | `version: x.y.z` |
| `install.sh` | `VERSION="x.y.z"` (+ header comment) |

## Pre-1.0 policy (`0.y.z`)

Until `1.0.0`, the public contract is still evolving. Bumps still mean something:

| Bump | When | Examples |
|------|------|----------|
| **MAJOR** (`1.0.0` or later `x.0.0`) | Breaking change to documented CLI flags, install layout, required schema fields, or default mutation safety | Remove a command; rename required `--out` artifact; apply without `--confirm` by default |
| **MINOR** (`0.y.0` / `x.y.0`) | Backward-compatible capability | New command (`analyze`, `optimize`); new optional flag; new schema file consumed by CLI |
| **PATCH** (`0.y.z` / `x.y.z`) | Backward-compatible fix or packaging/docs/CI | Path-jail fix; version drift; smoke coverage; additive **framework** in corpus |

### Corpus exception

Adding a framework to `schemas/frameworks.v1.json` + `references/` is a **PATCH** when:

- Existing framework keys and loci shapes stay valid
- CLI flags and schemas do not change required fields
- Tests/smoke still pass

Changing or removing an existing framework key or canonical locus id is **MINOR** if CLI still accepts old callers via alias, else **MAJOR**.

### Optimize apply exception

Any new **write** action under `optimize --apply` (beyond mechanical rename) is at least **MINOR**.  
Any apply that can run without `--confirm`, or that invents file content, is **MAJOR**.

## Post-1.0

Same table. `1.0.0` means: CLI surface + install paths + schema required fields are a stability promise; breaking changes require MAJOR and a migration note in `CHANGELOG.md` + `docs/RELEASE_NOTES.md`.

## What is not a version bump alone

- Issue/PR text
- Operator-only host install
- Git tag without code change (tag must match existing `VERSION`)

## Operator workflow

```bash
# 1. Decide bump class (see table)
python3 scripts/bump_version.py patch    # or minor | major | set 0.4.0

# 2. Edit CHANGELOG.md + docs/RELEASE_NOTES.md for the new version

# 3. Local gates
bash scripts/release_preflight.sh

# 4. Commit, push, wait for ci-ok

# 5. Tag must equal VERSION
V=$(tr -d '[:space:]' < VERSION)
git tag -a "v${V}" -m "Orchestra ${V}"
git push origin "v${V}"
```

Dry-run:

```bash
python3 scripts/bump_version.py minor --dry-run
```

## CI guarantees

- `VERSION` matches semver core `MAJOR.MINOR.PATCH` (no `v` prefix, no pre-release suffix in the file)
- Parity across CLI / SKILL / manifest / installer
- Tag policy is operator-enforced; GitHub Release should use tag `v` + `VERSION`

## Anti-patterns

- Editing only `scripts/orchestra.py` VERSION and forgetting `install.sh`
- Tagging `v0.4.0` while `VERSION` still says `0.3.2`
- Shipping a new mutating apply path as PATCH
- Inventing locus ids to “support” a map without a versioned corpus change
