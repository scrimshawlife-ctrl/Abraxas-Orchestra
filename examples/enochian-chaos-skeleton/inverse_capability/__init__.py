"""
inverse_capability — inverse / adversarial fail-mode surface

mechanical: inverse_capability
symbolic:   cacodemon_mirror
locus:      Inverse / adversarial fail-mode surface

Mirrors each edge item against fail criteria (density floor, empty body).
"""

from __future__ import annotations

from models import EdgeItem, EpistemicLabel, InverseFinding


def mirror(
    items: list[EdgeItem],
    *,
    min_density: float = 0.2,
) -> list[InverseFinding]:
    findings: list[InverseFinding] = []
    for item in items:
        text = str(item.payload.get("text") or item.payload.get("body") or "").strip()
        if item.density < min_density:
            findings.append(
                InverseFinding(
                    item_id=item.id,
                    kept=False,
                    reason=f"density {item.density:.3f} < min {min_density}",
                    label=EpistemicLabel.OBSERVED,
                )
            )
            continue
        if not text:
            findings.append(
                InverseFinding(
                    item_id=item.id,
                    kept=False,
                    reason="empty body",
                    label=EpistemicLabel.OBSERVED,
                )
            )
            continue
        findings.append(
            InverseFinding(
                item_id=item.id,
                kept=True,
                reason="pass inverse mirror",
                label=EpistemicLabel.INFERRED,
            )
        )
    return findings
