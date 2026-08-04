# Peircean Sign Trichotomies

Seventh framework for Abraxas Orchestra (v0.1 corpus expansion).

These mappings are design references. They guide sign-relation modules, representation layers, and provenance annotation. They are not runtime rules.

Charles Sanders Peirce’s semiotic provides a precise vocabulary for how signs relate to their objects and interpretants. For software architecture this becomes a clean way to separate representation kinds, enforce sign discipline, and prevent category errors between icon, index, and symbol.

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

This is the most frequently used trichotomy for architectural separation.

## Third Trichotomy — Sign in Relation to Interpretant (Rheme / Dicent / Argument)

| Category   | Peircean definition                          | Architectural role                                      | Typical modules / packages                          |
|------------|----------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Rheme      | Sign of qualitative possibility              | Possibility surfaces, open hypotheses, qualitative prompts | `possibility/`, `hypothesis/`, `rheme/`           |
| Dicent     | Sign of actual existence                     | Assertoric statements, factual claims, existence reports | `assertion/`, `fact/`, `dicent/`                    |
| Argument   | Sign of law / necessary relation             | Inferential structures, proofs, necessary consequences  | `argument/`, `inference/`, `proof/`                 |

## Ten-Class Sign Combinations (Selected High-Value)

Peirce’s full ten classes arise from combining the three trichotomies. Only the most architecturally useful are listed here.

| Class (short)              | Composition                     | Architectural usefulness                                      |
|----------------------------|---------------------------------|---------------------------------------------------------------|
| Rhematic Iconic Qualisign  | Pure quality possibility        | Tone / mood carriers, undifferentiated qualitative input      |
| Rhematic Iconic Sinsign    | Singular likeness               | Concrete analogy instances, example images                    |
| Rhematic Indexical Sinsign | Singular causal trace           | Individual symptoms, single-event pointers                    |
| Dicent Indexical Sinsign   | Assertoric actual trace         | Factual event reports, logged causal occurrences              |
| Rhematic Symbolic Legisign | Conventional possibility type   | Abstract type names, open symbolic schemas                    |
| Dicent Symbolic Legisign   | Conventional factual type       | Typed factual assertions, schema-validated claims             |
| Argument Symbolic Legisign | Conventional necessary law      | Inferential engines, proof systems, necessary consequence modules |

## Dual-Naming Pattern

```
# mechanical: similarity_repr
# symbolic:   iconic_layer  (Peircean — Icon)
```

```
# mechanical: causal_trace
# symbolic:   indexical_pointer  (Peircean — Index)
```

```
# mechanical: conventional_code
# symbolic:   symbolic_legisign  (Peircean — Symbol + Legisign)
```

```
# mechanical: inferential_engine
# symbolic:   argument_symbol  (Peircean — Argument)
```

## Practical Projection Notes

- The Icon / Index / Symbol separation is the highest-leverage application. Keeping these representation kinds in distinct modules prevents category errors (treating a causal trace as a conventional name, or a likeness as a law).
- Legisigns own schemas and types; sinsigns own concrete runtime tokens and events.
- Arguments are the natural home for inference engines, Brier-scored forecasting logic, and necessary-consequence modules.
- Peircean discipline pairs cleanly with Abraxas OBSERVED / INFERRED / SPECULATIVE labeling: OBSERVED tends toward indexical and dicent forms; SPECULATIVE toward rhematic and iconic forms.
- When combining with other frameworks, a Peircean class can sit inside a planetary domain, Sephira, or Solomonic office without conflict; record the dual mapping.

Load this file when Peircean sign relations, representation kinds, or semiotic discipline are selected as primary or secondary framework.
