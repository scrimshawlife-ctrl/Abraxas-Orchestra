"""Enochian primary + Chaos Magic overlay session pipeline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cross_domain_bus import route
from domain_entry import open_domains
from edge_intake import ingest_edge
from inverse_capability import mirror
from models import Domain, Provenance, SessionReport
from root_truth_seal import banishing_clear, issue_seal
from sovereign_intent import make_contract, results_gate


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_session(
    *,
    session_id: str,
    operator: str,
    intent_id: str,
    statement: str,
    edge_items: list[dict[str, Any]],
    domains: list[Domain] | None = None,
    min_density: float = 0.2,
    max_items: int = 8,
    report_path: str | None = None,
) -> SessionReport:
    domains = domains or [Domain.AIR, Domain.FIRE, Domain.WATER, Domain.EARTH]
    contract = make_contract(
        intent_id,
        statement,
        max_items=max_items,
        allowed_domains=domains,
        min_density=min_density,
    )

    seal = issue_seal(session_id, operator)
    clear = banishing_clear(seal)
    if not seal.valid:
        report = SessionReport(
            session_id=session_id,
            intent_id=intent_id,
            seal_valid=False,
            accepted_calls=0,
            edge_count=0,
            bus_count=0,
            kept=[],
            rejected_count=len(edge_items),
            summary=f"Session refused: {seal.reason}",
            provenance=Provenance("pipeline", "run_session", _utc()),
            meta={"banishing": clear, "results_gate": results_gate(contract, 0, len(edge_items))},
        )
        _maybe_write(report, report_path)
        return report

    token = open_domains(seal, contract.allowed_domains, call_id=f"call-{intent_id}")
    accepted, edge_rejected = ingest_edge(token, edge_items, source="demo_edge")
    findings = mirror(accepted, min_density=contract.min_density)
    kept_ids = {f.item_id for f in findings if f.kept}
    kept_items = [i for i in accepted if i.id in kept_ids][: contract.max_items]
    rejected_count = len(edge_rejected) + sum(1 for f in findings if not f.kept)

    bus = route(kept_items)
    gate = results_gate(contract, len(kept_items), rejected_count)

    kept_payload = [
        {
            "id": i.id,
            "domain": i.domain.value,
            "density": i.density,
            "payload": i.payload,
            "source": i.source,
        }
        for i in kept_items
    ]

    report = SessionReport(
        session_id=seal.session_id,
        intent_id=contract.intent_id,
        seal_valid=True,
        accepted_calls=1 if token.accepted else 0,
        edge_count=len(accepted),
        bus_count=len(bus),
        kept=kept_payload,
        rejected_count=rejected_count,
        summary=(
            f"Session {seal.session_id}: kept {len(kept_items)}, "
            f"rejected {rejected_count}, bus {len(bus)}; gate={'pass' if gate['pass'] else 'fail'}"
        ),
        provenance=Provenance("pipeline", "run_session", _utc()),
        meta={
            "seal_reason": seal.reason,
            "token_reason": token.reason,
            "domains": [d.value for d in token.domains],
            "bus": [
                {
                    "id": m.id,
                    "from": m.from_domain.value,
                    "to": m.to_domain.value if m.to_domain else None,
                    "weight": m.weight,
                    "body": m.body,
                }
                for m in bus
            ],
            "inverse": [
                {
                    "item_id": f.item_id,
                    "kept": f.kept,
                    "reason": f.reason,
                    "label": f.label.value,
                }
                for f in findings
            ],
            "results_gate": gate,
            "edge_rejected": edge_rejected,
        },
    )
    _maybe_write(report, report_path)
    return report


def _maybe_write(report: SessionReport, report_path: str | None) -> None:
    if not report_path:
        return
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
