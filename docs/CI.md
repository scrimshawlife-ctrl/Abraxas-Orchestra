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
| `coverage-soft` | Soft quality report — **informational** artifact |
| `coverage-gate` | Hard floors + linkage (`coverage_report.py --gate`); subprocess-aware via in-process CLI under trace — **required** by `ci-ok` |
| `ci-ok` | Aggregate — version-parity, path-jail, integrity, smoke, coverage-gate |

Local reports:

```bash
python3 scripts/coverage_report.py          # soft
python3 scripts/coverage_report.py --gate  # hard floors (CI gate)
```

Permissions: `contents: read` only.

Version policy: [`SEMVER.md`](SEMVER.md).

## Branch protection (required for this repo)

`main` is protected. **Do not bypass** status checks or force-push.

| Setting | Value |
|---------|--------|
| Required status check | **`ci-ok`** (strict: branch up to date) |
| Enforce for administrators | **On** (no admin bypass) |
| Require pull request | **On** (0 approving reviews — solo-friendly) |
| Dismiss stale reviews | On |
| Force pushes | **Off** |
| Branch deletions | **Off** |

### Operator workflow (no direct push to main)

```bash
# 1. Feature branch
git checkout -b fix/my-change
# … edit, commit …

# 2. Push branch and open PR
git push -u origin HEAD
gh pr create --fill

# 3. Wait for CI
gh pr checks
# required: ci-ok green

# 4. Merge only via PR (UI or gh)
gh pr merge --squash
```

If you see `Bypassed rule violations for refs/heads/main`, protection was not enforcing admins — that must stay **enabled**.

### Re-apply protection (API)

```bash
gh api -X PUT repos/scrimshawlife-ctrl/Abraxas-Orchestra/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": { "strict": true, "contexts": ["ci-ok"] },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

Until the first Actions run completes on a new fork, the check name may not appear in the UI dropdown — push a PR or re-run jobs, then select **`ci-ok`**.

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

Tags can still be pushed after `main` has the release commit via merged PR:

```bash
bash scripts/publish.sh
git push origin v$(tr -d '[:space:]' < VERSION)
# Actions → release workflow creates the GitHub Release
```

Release notes preference:

1. `docs/RELEASE_BODY_vX.Y.Z.md` if present  
2. Else CHANGELOG section for that version  
