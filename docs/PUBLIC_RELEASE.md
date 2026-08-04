# Public release packaging — debut guide

This document is the **public debut** checklist for Abraxas Orchestra.  
Private install readiness is covered in `COMPLETION.md`. This file adds license, security, and registry posture.

## Version

**Debut target:** `0.1.3` (security + public packaging over 0.1.2)

## Why 0.1.3 for public

| Change | Reason |
|--------|--------|
| Apache-2.0 LICENSE | Hub / registry eligibility |
| NOTICE | Apache attribution |
| Installer path jail | Public trust — refuse `/etc`, outside `$HOME` |
| `.github/SECURITY.md` | Coordinated disclosure path |
| `docs/SECURITY_AUDIT.md` | Audit record for reviewers |

## Pre-publish gate (must all pass)

```bash
git clone https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra-Hermes.git
cd Abraxas-Orchestra-Hermes
bash scripts/smoke.sh
# Path refusals (expect non-zero):
bash install.sh --dry-run --target /etc/orchestra ; echo exit:$?
bash install.sh --dry-run --target /tmp/orch-test ; echo exit:$?
# Happy path dry-run (expect zero):
bash install.sh --dry-run
test -f LICENSE && test -f NOTICE && test -f .github/SECURITY.md
```

## Debut sequence

1. Merge/push 0.1.3 packaging to `main`  
2. Confirm CI green  
3. Tag:
   ```bash
   git tag -a v0.1.3 -m "Orchestra 0.1.3 public debut — Apache-2.0 + installer path jail"
   git push origin v0.1.3
   ```
4. GitHub Release: attach short notes from `docs/RELEASE_NOTES.md`  
5. Optional: submit to OpenClaw / Hermes skill directories with `docs/COMMUNITY.md` matrix  

## Messaging (what to say in public)

**Is:** Local coding-agent skill; dual-named architecture skeletons from traditional maps; fail-closed; stdlib CLI.  
**Is not:** Network service, secret broker, or operational magic runtime.

## Security one-liner for registries

> Installer refuses system paths and targets outside `$HOME` unless `--allow-outside-home`. CLI performs no network I/O. No third-party runtime dependencies.

## After debut

- Treat schema/CLI/install as stable unless major bump  
- Security reports via `.github/SECURITY.md`  
- Corpus expansion still open via `schemas/frameworks.v1.json`
