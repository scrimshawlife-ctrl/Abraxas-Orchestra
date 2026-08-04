"""
cross_domain_bus — spirit bus / Black Cross coordination

mechanical: cross_domain_bus
symbolic:   tablet_of_union
locus:      Spirit bus / Black Cross coordination

Routes edge items across opened domains as typed bus messages.
"""

from __future__ import annotations

from models import BusMessage, Domain, EdgeItem


def route(items: list[EdgeItem]) -> list[BusMessage]:
    """Emit bus messages; same-domain items stay local (to_domain=None)."""
    messages: list[BusMessage] = []
    for item in items:
        body = str(item.payload.get("text") or item.payload.get("body") or item.id)
        messages.append(
            BusMessage(
                id=f"bus-{item.id}",
                from_domain=item.domain,
                to_domain=None,
                body=body,
                weight=item.density,
            )
        )
    by_domain: dict[Domain, list[EdgeItem]] = {}
    for item in items:
        by_domain.setdefault(item.domain, []).append(item)
    pairs = [(Domain.FIRE, Domain.WATER), (Domain.AIR, Domain.EARTH)]
    for a, b in pairs:
        if a in by_domain and b in by_domain:
            left, right = by_domain[a][0], by_domain[b][0]
            messages.append(
                BusMessage(
                    id=f"cross-{a.value}-{b.value}",
                    from_domain=a,
                    to_domain=b,
                    body=f"link:{left.id}->{right.id}",
                    weight=min(left.density, right.density),
                )
            )
    return messages
