# Peircean Sign Trichotomies

Seventh framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide sign-relation modules, representation layers, and provenance annotation. They are not runtime rules.

## First Trichotomy — Sign in Itself (Qualisign / Sinsign / Legisign)

| Category   | Peircean definition                          | Architectural role                                      | Typical modules / packages                          |
|------------|----------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Qualisign  | A quality that is a sign (tone, feeling)     | Pure quality / tone carriers, undifferentiated signal   | `quality/`, `tone/`, `raw_feel/`                    |
| Sinsign    | An actual existent thing that is a sign      | Concrete token instances, singular events, occurrences  | `token/`, `instance/`, `event/`                     |
| Legisign   | A general type / law that is a sign          | Types, schemas, laws, general patterns                  | `type/`, `schema/`, `law/`, `pattern/`              |

## Second Trichotomy — Sign in Relation to Object (Icon / Index / Symbol)

| Category   | Peircean definition                          | Architectural role                                      | Typical modules / packages                          |
|------------|----------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Icon       | Sign that shares quality with its object     | Similarity-based representation, likeness, analogy      | `icon/`, `likeness/`, `analogy/`                    |
| Index      | Sign that is really affected by its object   | Causal / contiguity links, pointers, traces, symptoms   | `index/`, `pointer/`, `trace/`, `symptom/`          |
| Symbol     | Sign that refers by convention / law         | Conventional names, codes, abstract symbols, language   | `symbol/`, `code/`, `convention/`, `name/`          |

## Third Trichotomy — Sign in Relation to Interpretant (Rheme / Dicent / Argument)

| Category   | Peircean definition                          | Architectural role                                      | Typical modules / packages                          |
|------------|----------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Rheme      | Sign of qualitative possibility              | Possibility surfaces, open hypotheses                   | `possibility/`, `hypothesis/`, `rheme/`             |
| Dicent     | Sign of actual existence                     | Assertoric statements, factual claims                   | `assertion/`, `fact/`, `dicent/`                    |
| Argument   | Sign of law / necessary relation             | Inferential structures, proofs                          | `argument/`, `inference/`, `proof/`                 |

## Dual-Naming Pattern

```
# mechanical: similarity_repr
# symbolic:   iconic_layer  (Peircean — Icon)
```

## Practical Projection Notes

- Icon / Index / Symbol separation is the highest-leverage application.
- Peircean discipline pairs with OBSERVED / INFERRED / SPECULATIVE labeling.

Load this file when Peircean sign relations are selected as primary or secondary framework.

## CLI default loci (mechanical → symbolic)

| Mechanical | Symbolic | Note |
|------------|----------|------|
| `likeness` | `icon` | Similarity representation |
| `trace` | `index` | Causal / contiguity link |
| `convention` | `symbol` | Conventional code |
| `type_schema` | `legisign` | General type / law |
| `instance` | `sinsign` | Concrete token / event |
| `inference` | `argument` | Necessary consequence |

Core collapse for `do project`: **`trace`, `convention`, `inference`**.

Canonical machine table: `schemas/frameworks.v1.json`.
