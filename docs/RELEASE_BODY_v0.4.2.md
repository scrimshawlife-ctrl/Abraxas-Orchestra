# Orchestra 0.4.2

Deeper analyze → map heuristics (still fail-closed).

## Highlights

- Role synonyms (`repository`→store, `writer`/`emit`→output, `cli`→entry, …)
- Compound names + boilerplate suffix stripping (`user_intake`, `intake_handler`)
- Docstring / `def` / `class` name signals
- Secondary `match_score` for tie-breaks; better `candidate_frameworks` ranking
- Docs: `docs/FRAMEWORK_FIT.md` scoring table

## Install

```bash
git clone --branch v0.4.2 https://github.com/scrimshawlife-ctrl/Abraxas-Orchestra.git
cd Abraxas-Orchestra
bash scripts/smoke.sh && bash install.sh
```
