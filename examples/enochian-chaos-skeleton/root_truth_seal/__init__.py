"""
root_truth_seal — session authority seal

mechanical: root_truth_seal
symbolic:   sigillum_dei_aemeth
locus:      Root truth / session authority seal
Overlay:    overlay:chaos-magic/banishing_clear (Session / context banishing)

Validates operator + session identity before any domain work begins.
Banishing semantics: a failed seal clears residual session state.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from models import Provenance, RootTruthSeal


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def issue_seal(
    session_id: str,
    operator: str,
    *,
    require_operator: bool = True,
) -> RootTruthSeal:
    """Issue or refuse a root truth seal for this session."""
    if not session_id or not session_id.strip():
        return RootTruthSeal(
            session_id=session_id or "",
            operator=operator or "",
            valid=False,
            reason="empty session_id",
            provenance=Provenance("root_truth_seal", "issue_seal", _utc()),
        )
    if require_operator and not (operator and operator.strip()):
        return RootTruthSeal(
            session_id=session_id.strip(),
            operator="",
            valid=False,
            reason="operator required",
            provenance=Provenance("root_truth_seal", "issue_seal", _utc()),
        )
    return RootTruthSeal(
        session_id=session_id.strip(),
        operator=operator.strip(),
        valid=True,
        reason="seal issued",
        provenance=Provenance("root_truth_seal", "issue_seal", _utc()),
    )


def banishing_clear(seal: RootTruthSeal) -> dict[str, Any]:
    """Chaos overlay: clear residual session claim when seal is invalid."""
    if seal.valid:
        return {"cleared": False, "session_id": seal.session_id, "note": "seal holds"}
    return {
        "cleared": True,
        "session_id": seal.session_id,
        "note": "residual session cleared after failed seal",
    }
