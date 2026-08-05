# Public release packaging — debut guide

Public debut checklist for Abraxas Orchestra.  
Private freeze gates: [`COMPLETION.md`](COMPLETION.md). CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

## Version

**Current public line:** `0.3.1` (analyze → map → optimize apply + CI gates)

First public packaging baseline was `0.1.3` (Apache-2.0 + installer path jail). That posture still holds; capability surface is now 0.3.1.

## Capability surface (0.3.1)

| Command | Role |
|---------|------|
| `structure` / `project` / `diagram` | Emit dual-named skeletons + diagrams |
| `analyze` | OBSERVED Python import graph + optional framework map |
| `optimize` | Plan only by default |
| `optimize --apply --confirm` | Gated mechanical renames + backup |
| `--refresh` | Re-analyze after confirmed apply |

## Pre-publish gate (must all pass)

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
cd Abraxas-Orchestra-Hermes

bash scripts/smoke.sh
python3 scripts/orchestra.py check

# Version parity (also enforced in CI)
V=$(tr -d '[:space:]' < VERSION)
grep -q "VERSION = \"$V\"" scripts/orchestra.py
grep -q "^VERSION=\"$V\"$" install.sh

# Path refusals (expect non-zero / exit 2):
bash install.sh --dry-run --target /etc/orchestra ; echo install_exit:$?
python3 scripts/orchestra.py analyze --path /etc ; echo analyze_exit:$?

# Happy path dry-run (expect zero):
bash install.sh --dry-run

test -f LICENSE && test -f NOTICE && test -f .github/SECURITY.md
```

Or: `bash scripts/release_preflight.sh`

## Debut sequence (operator)

1. Confirm Actions run green on `main` (jobs: `version-parity`, `path-jail`, `smoke`, aggregate **`ci-ok`**)
2. Optional: Settings → Branches → protect `main` → require status check **`ci-ok`**
3. Tag and push:
   ```bash
   git tag -a v0.3.1 -m "Orchestra 0.3.1 analyze/optimize"
   git push origin v0.3.1
   ```
4. GitHub → Releases → Draft from tag `v0.3.1`  
   Body: copy § 0.3.1 (and summary of 0.3.0 / 0.2.0) from [`RELEASE_NOTES.md`](RELEASE_NOTES.md)
5. Host install once: [`DEPLOY.md`](DEPLOY.md)
6. Optional: registry submit with [`COMMUNITY.md`](COMMUNITY.md)

## Messaging (what to say in public)

**Is:** Local coding-agent skill; dual-named architecture skeletons from traditional maps; repo analyze + fail-closed optimize plan/apply; stdlib CLI.  
**Is not:** Network service, secret broker, silent tree rewriter, or operational magic runtime.

## Security one-liner for registries

> Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`. Analyze/apply path-jailed. CLI performs no network I/O. Optimize writes require `--apply --confirm`. No third-party runtime dependencies.

## After debut

- Treat schema/CLI/install as stable unless major bump  
- Security reports via `.github/SECURITY.md`  
- Corpus expansion still open via `schemas/frameworks.v1.json`  
- Broader `safe_apply` actions and multi-language analyze remain deferred (`ROADMAP.md`)
