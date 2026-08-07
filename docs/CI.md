# Continuous integration

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

## Triggers

- Push to `main`
- Pull request targeting `main`
- Manual `workflow_dispatch`

## Jobs

| Job | Purpose |
|-----|---------|
| `version-parity` | Semver format + `python3 scripts/bump_version.py check` |
| `path-jail` | Installer refuses `/etc/orchestra`; `analyze --path /etc` exits 2 |
| `integrity` | Critical-file line floors + markers (`scripts/integrity_check.py`) |
| `smoke` | Full `scripts/smoke.sh` on Python 3.11 and 3.12 |
| `ci-ok` | Aggregate — all of the above must succeed |

Permissions: `contents: read` only.

Version policy: [`SEMVER.md`](SEMVER.md).

## Branch protection (recommended)

GitHub → **Settings** → **Branches** → **Add rule** for `main`:

1. Require a pull request before merging (optional but preferred)
2. Require status checks to pass before merging
3. Required check name: **`ci-ok`**
4. Do not allow bypassing the above settings (org policy dependent)

Until the first Actions run completes on `main`, the check name may not appear in the dropdown — push any commit or use **Re-run jobs**, then select `ci-ok`.

## Local mirror

```bash
bash scripts/release_preflight.sh
```

## Release workflow

Workflow: [`.github/workflows/release.yml`](../.github/workflows/release.yml)

| Trigger | Behavior |
|---------|----------|
| Push tag `v*` | Validate `VERSION` matches tag, smoke, create/update GitHub Release |
| `workflow_dispatch` | Same checks; optional dry-run |

**Tag rule:** annotated tag `vX.Y.Z` must equal `VERSION` file (`X.Y.Z`).

Release notes preference:

1. `docs/RELEASE_BODY_vX.Y.Z.md` if present
2. Else CHANGELOG section for that version

Operator:

```bash
bash scripts/publish.sh
git push origin v$(tr -d '[:space:]' < VERSION)
# Actions → release workflow creates the GitHub Release
```
