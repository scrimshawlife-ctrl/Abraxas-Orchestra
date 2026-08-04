"""
domain_entry — invocation / domain-entry token

mechanical: domain_entry
symbolic:   enochian_call
locus:      Invocation / domain-entry token
Overlay:    overlay:chaos-magic/sigil_glyph (Compressed intent token)

Opens Watchtower domains only when a valid root seal is present.
"""

from __future__ import annotations

from models import Domain, DomainEntryToken, RootTruthSeal


def open_domains(
    seal: RootTruthSeal,
    domains: list[Domain],
    *,
    call_id: str,
) -> DomainEntryToken:
    """Compress intent into a domain-entry token (Chaos sigil overlay)."""
    if not seal.valid:
        return DomainEntryToken(
            call_id=call_id,
            domains=[],
            seal_session_id=seal.session_id,
            accepted=False,
            reason=f"seal refused: {seal.reason}",
        )
    if not domains:
        return DomainEntryToken(
            call_id=call_id,
            domains=[],
            seal_session_id=seal.session_id,
            accepted=False,
            reason="no domains requested",
        )
    seen: set[Domain] = set()
    ordered: list[Domain] = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            ordered.append(d)
    return DomainEntryToken(
        call_id=call_id,
        domains=ordered,
        seal_session_id=seal.session_id,
        accepted=True,
        reason=f"opened {len(ordered)} domain(s)",
    )
