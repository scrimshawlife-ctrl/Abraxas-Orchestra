# Framework fit guide

When to pick which map for `structure` / `project` / `analyze -f`, and how to read strength scores.

Live threat model: [`SECURITY.md`](SECURITY.md) · CLI surface: [`DESIGN.md`](DESIGN.md)

## Strength labels (fail-closed)

| Strength | Meaning | Optimize apply |
|----------|---------|----------------|
| `STRONG` | Leaf or module id equals mechanical or symbolic locus | Eligible if other gates pass |
| `ADEQUATE` | Path segment / normalized name / token overlap with locus | Eligible |
| `WEAK` | Loose token overlap only | Plan may list; apply blocked for that step |
| `FORCED` | Required concern with no honest locus | Blocks apply entirely |

Analyze exit codes: `0` CLEAN / OBSERVED_ONLY · `1` WEAK_MAPPINGS present · `2` NOT_COMPUTABLE.

**Agent rule:** Do not invent loci. Prefer `analyze` without `-f` first when the tree is unfamiliar, then pick a framework from suggestions or this guide.

## Which framework for which shape

| Shape of the code | Prefer | Why |
|-------------------|--------|-----|
| Linear pipeline / stages (intake → process → out) | `alchemical-stages`, `tree-of-life` | Ordered stages map cleanly to modules |
| Layered agent / multi-domain system | `enochian`, `chaos-magic` (overlay) | Domains + seals + intent layers |
| Ranked authority / command hierarchy | `solomonic`, `planetary-spheres` | Clear rank order |
| Token / sign / interface taxonomy | `peircean-signs` | Types of signs ↔ API roles |
| Cyclic zones / zones of recursion | `numogram` | Zone graph, not a single pipeline |
| Discrete rune-like capabilities | `elder-futhark` | Many peer modules with distinct roles |
| Decision / oracle branching | `iching-hexagrams` | Branching states |
| Geometry / layout / structure-first | `sacred-geometry` | Spatial / structural metaphors |

## Practical workflow

```bash
# 1. Observe only
python3 scripts/orchestra.py analyze --path ./pkg --out /tmp/orch-an

# 2. If suggestions look right, re-run with -f
python3 scripts/orchestra.py analyze --path ./pkg -f alchemical-stages --out /tmp/orch-an

# 3. Plan only — never apply on WEAK/FORCED without human review
python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --out /tmp/orch-plan

# 4. Dry-run apply, then confirm
python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --apply
python3 scripts/orchestra.py optimize --from /tmp/orch-an/analysis.json --apply --confirm
```

## Naming tips that improve fit

- Name modules after **mechanical locus** strings in `schemas/frameworks.v1.json` when you own the tree.
- Underscores / hyphens normalize for matching (`edge_intake` ≈ `edge-intake` style loci).
- Put role words in the **module leaf** or package segment, not only deep in comments.
- For greenfield work, prefer `structure` / `project` emit over force-fitting a messy tree.

## When not to map

- Polyglot repos (Python-only analyze in 0.4.x)
- Generated / vendor trees — exclude or narrow `--path`
- Pure libraries with no architectural stages — use OBSERVED graph + diagrams only

Canonical loci: `schemas/frameworks.v1.json` · Human tables: `references/`
