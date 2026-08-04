"""Enochian primary + Chaos Magic overlay session pipeline."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cross_domain_bus import route
from domain_entry import open_domains
from edge_intake import ingest_edge
from inverse_capability import mirror
from models import (
    Domain,
    PipelineError,
    Provenance,
    SessionReport,
    StageError,
    ValidationError,
)
from root_truth_seal import banishing_clear, issue_seal
from sovereign_intent import make_contract, results_gate

log = logging.getLogger("orchestra.enochian.pipeline")


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validate_inputs(
    session_id: str,
    operator: str,
    intent_id: str,
    statement: str,
    edge_items: list[dict[str, Any]] | None,
    min_density: float,
    max_items: int,
) -> list[dict[str, Any]]:
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValidationError("input", "session_id must be a non-empty string")
    if not isinstance(operator, str) or not operator.strip():
        raise ValidationError("input", "operator must be a non-empty string")
    if not isinstance(intent_id, str) or not intent_id.strip():
        raise ValidationError("input", "intent_id must be a non-empty string")
    if not isinstance(statement, str) or not statement.strip():
        raise ValidationError("input", "statement must be a non-empty string")
    if edge_items is None:
        raise ValidationError("input", "edge_items is required (use [] for empty feed)")
    if not isinstance(edge_items, list):
        raise ValidationError(
            "input",
            "edge_items must be a list",
            details={"type": type(edge_items).__name__},
        )
    for i, item in enumerate(edge_items):
        if not isinstance(item, dict):
            raise ValidationError(
                "input",
                f"edge_items[{i}] must be a dict",
                details={"index": i, "type": type(item).__name__},
            )
    if not isinstance(min_density, (int, float)) or min_density < 0 or min_density > 1:
        raise ValidationError(
            "input",
            "min_density must be a number in [0, 1]",
            details={"min_density": min_density},
        )
    if not isinstance(max_items, int) or max_items < 1:
        raise ValidationError(
            "input",
            "max_items must be an integer >= 1",
            details={"max_items": max_items},
        )
    return edge_items


def _coerce_domains(domains: list[Domain] | list[str] | None) -> list[Domain]:
    if domains is None:
        return [Domain.AIR, Domain.FIRE, Domain.WATER, Domain.EARTH]
    out: list[Domain] = []
    for d in domains:
        if isinstance(d, Domain):
            out.append(d)
            continue
        if isinstance(d, str):
            try:
                out.append(Domain(d.lower().strip()))
            except ValueError as exc:
                raise ValidationError(
                    "input",
                    f"unknown domain: {d!r}",
                    details={"allowed": [x.value for x in Domain]},
                ) from exc
        else:
            raise ValidationError(
                "input",
                f"domain must be Domain or str, got {type(d).__name__}",
            )
    if not out:
        raise ValidationError("input", "domains list is empty")
    return out


def _maybe_write(report: SessionReport, report_path: str | None) -> None:
    if not report_path:
        return
    path = Path(report_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise StageError(
            "output",
            f"failed to write report to {path}: {exc}",
            details={"path": str(path), "errno": getattr(exc, "errno", None)},
        ) from exc


def run_session(
    *,
    session_id: str,
    operator: str,
    intent_id: str,
    statement: str,
    edge_items: list[dict[str, Any]],
    domains: list[Domain] | list[str] | None = None,
    min_density: float = 0.2,
    max_items: int = 8,
    report_path: str | None = None,
) -> SessionReport:
    """
    Execute one Enochian + Chaos session.

    Raises:
        ValidationError: bad inputs (fail closed before side effects)
        StageError: unexpected failure inside a stage
        PipelineError: other pipeline failures
    """
    try:
        items = _validate_inputs(
            session_id, operator, intent_id, statement, edge_items, min_density, max_items
        )
        domain_list = _coerce_domains(domains)
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError("input", str(exc)) from exc

    try:
        contract = make_contract(
            intent_id,
            statement,
            max_items=max_items,
            allowed_domains=domain_list,
            min_density=float(min_density),
        )
    except Exception as exc:
        raise StageError("sovereign_intent", f"contract failed: {exc}") from exc

    try:
        seal = issue_seal(session_id, operator)
        clear = banishing_clear(seal)
    except Exception as exc:
        raise StageError("root_truth_seal", f"seal failed: {exc}") from exc

    if not seal.valid:
        log.warning("session refused: %s", seal.reason)
        report = SessionReport(
            session_id=session_id,
            intent_id=intent_id,
            seal_valid=False,
            accepted_calls=0,
            edge_count=0,
            bus_count=0,
            kept=[],
            rejected_count=len(items),
            summary=f"Session refused: {seal.reason}",
            provenance=Provenance("pipeline", "run_session", _utc()),
            meta={
                "banishing": clear,
                "results_gate": results_gate(contract, 0, len(items)),
                "error": None,
            },
        )
        _maybe_write(report, report_path)
        return report

    try:
        token = open_domains(
            seal, contract.allowed_domains, call_id=f"call-{intent_id}"
        )
    except Exception as exp:
        raise StageError("domain_entry", f"open_domains failed: {exp}") from exp

    try:
        accepted, edge_rejected = ingest_edge(token, items, source="demo_edge")
    except Exception as exp:
        raise StageError("edge_intake", f"ingest failed: {exp}") from exp

    try:
        findings = mirror(accepted, min_density=contract.min_density)
    except Exception as exp:
        raise StageError("inverse_capability", f"mirror failed: {exp}") from exp

    kept_ids = {f.item_id for f in findings if f.kept}
    kept_items = [i for i in accepted if i.id in kept_ids][: contract.max_items]
    rejected_count = len(edge_rejected) + sum(1 for f in findings if not f.kept)

    try:
        bus = route(kept_items)
    except Exception as exp:
        raise StageError("cross_domain_bus", f"route failed: {exp}") from exp

    try:
        gate = results_gate(contract, len(kept_items), rejected_count)
    except Exception as exp:
        raise StageError("sovereign_intent", f"results_gate failed: {exp}") from exp

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
            f"rejected {rejected_count}, bus {len(bus)}; "
            f"gate={'pass' if gate['pass'] else 'fail'}"
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
            "error": None,
        },
    )
    _maybe_write(report, report_path)
    return report


def run_session_safe(
    **kwargs: Any,
) -> tuple[SessionReport | None, PipelineError | None]:
    """
    Soft-fail wrapper: returns (report, None) or (None, error).

    Prefer ``run_session`` when the caller wants exceptions.
    """
    try:
        return run_session(**kwargs), None
    except PipelineError as exp:
        log.error("pipeline failed at %s: %s", exp.stage, exp)
        return None, exp
