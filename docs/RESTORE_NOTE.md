# Restore note (0.3.2)

On 2026-08-04, `scripts/orchestra.py` was briefly truncated during a failed Contents API update.

**Resolution:** `.github/workflows/restore-cli.yml` restored the full CLI from commit `107b0f65` and set `VERSION = "0.3.2"`.

Verified locally: `python3 scripts/orchestra.py check` and `bash scripts/smoke.sh` green.

This note is a no-op documentation marker so Actions runs on the restored tree (bot commits from `GITHUB_TOKEN` do not re-trigger workflows).
