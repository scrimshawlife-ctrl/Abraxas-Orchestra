# Orchestra 0.4.1

Hardening and docs follow-up to 0.4.0.

## Highlights

- **Integrity check** — `scripts/integrity_check.py` + CI `integrity` job (line floors / markers to catch CLI truncation)
- **Apply module split** — `optimize_enrich.py` + `optimize_rewrite.py`; public API remains `optimize_apply`
- **Framework fit guide** — `docs/FRAMEWORK_FIT.md`
- **Mapping** — hyphen/underscore normalized locus match for STRONG/ADEQUATE

## Install

```bash
git clone --branch v0.4.1 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh
bash install.sh
```
