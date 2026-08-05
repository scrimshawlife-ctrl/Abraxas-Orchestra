# Public release packaging — debut guide

Public debut checklist for Abraxas Orchestra.  
Private freeze gates: [`COMPLETION.md`](COMPLETION.md). CI: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

**Current public line:** `0.4.0`  
Helper: `bash scripts/publish.sh`  
Release body: [`RELEASE_BODY_v0.4.0.md`](RELEASE_BODY_v0.4.0.md)  
**Automated release:** [`.github/workflows/release.yml`](../.github/workflows/release.yml) (runs on `v*` tag push)

## Capability surface (0.4.0)

| Command | Role |
|---------|------|
| `structure` / `project` / `diagram` | Emit dual-named skeletons + diagrams |
| `analyze` | OBSERVED Python import graph + optional framework map |
| `optimize` | Plan only by default |
| `optimize --apply --confirm` | Gated mechanical rename / promote / flatten + backup |
| `--steps` / `--actions` | Selective apply |
| `--refresh` | Re-analyze after confirmed apply |

## Pre-publish gate

```bash
bash scripts/release_preflight.sh
```

## Debut sequence (you — requires credentials)

1. Confirm Actions **`ci-ok`** green on `main`
2. Optional: protect `main` → require status check **`ci-ok`** (`docs/CI.md`)
3. Tag and push:
   ```bash
   bash scripts/publish.sh
   git push origin main
   git push origin v0.4.0
   ```
4. Push tag → **Actions `release` workflow** creates the GitHub Release  
   (notes from [`RELEASE_BODY_v0.4.0.md`](RELEASE_BODY_v0.4.0.md))
5. Host install: [`DEPLOY.md`](DEPLOY.md)
6. Optional: registry submit [`COMMUNITY.md`](COMMUNITY.md)

## Messaging

**Is:** Local coding-agent skill; dual-named architecture skeletons; repo analyze + fail-closed optimize; stdlib CLI.  
**Is not:** Network service, secret broker, silent tree rewriter, or operational magic runtime.

## Security one-liner

> Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`. Analyze/apply path-jailed. CLI performs no network I/O. Optimize writes require `--apply --confirm`. No third-party runtime dependencies.

License: Apache-2.0
