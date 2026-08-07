#!/usr/bin/env python3
"""Unit tests for deeper analyze mapping heuristics — stdlib only."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_repo import (  # noqa: E402
    _map_node_to_locus,
    _score_locus_match,
    _suggest_frameworks,
)


TREE_LOCI = [
    ("intent", "kether", "System intent / entry contract"),
    ("intake", "chokmah", "Raw force intake"),
    ("constraint", "binah", "Schema / form constraint"),
    ("expand", "chesed", "Mercy expansion"),
    ("adversarial", "geburah", "Severity / critique"),
    ("synthesis", "tiphareth", "Synthesis core"),
    ("persist", "netzach", "Persistence"),
    ("analyze", "hod", "Analysis / intellect"),
    ("store", "yesod", "Foundation store"),
    ("output", "malkuth", "Concrete manifestation"),
]

ENOCHIAN_LOCI = [
    ("edge_intake", "air_east", "Edge intake"),
    ("air_comms", "air", "Comms"),
    ("fire_transform", "fire", "Transform"),
    ("water_memory", "water", "Memory"),
    ("earth_persist", "earth", "Persist"),
    ("domain_entry", "domain", "Domain entry"),
    ("root_truth_seal", "seal", "Root seal"),
    ("cross_domain_bus", "bus", "Cross-domain bus"),
    ("sovereign_intent", "intent", "Sovereign intent"),
]


def _node(mid: str) -> dict:
    return {"id": mid, "path": mid.replace(".", "/") + ".py", "kind": "module"}


class TestDeeperMapping(unittest.TestCase):
    def test_exact_still_strong(self) -> None:
        m = _map_node_to_locus(_node("pkg.intake"), TREE_LOCI)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["strength"], "STRONG")
        self.assertEqual(m["mechanical_name"], "intake")

    def test_noise_suffix_strong(self) -> None:
        m = _map_node_to_locus(_node("pkg.intake_handler"), TREE_LOCI)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["mechanical_name"], "intake")
        self.assertIn(m["strength"], {"STRONG", "ADEQUATE"})

    def test_compound_prefix_adequate(self) -> None:
        m = _map_node_to_locus(_node("pkg.user_intake"), TREE_LOCI)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["mechanical_name"], "intake")
        self.assertIn(m["strength"], {"STRONG", "ADEQUATE"})

    def test_role_synonym_repository_to_store(self) -> None:
        m = _map_node_to_locus(
            _node("pkg.user_repository"),
            TREE_LOCI,
            source_text='"""Persistence for user records."""\n',
        )
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["mechanical_name"], "store")
        self.assertIn(m["strength"], {"ADEQUATE", "WEAK"})

    def test_docstring_boosts_output(self) -> None:
        m = _map_node_to_locus(
            _node("pkg.writer"),
            TREE_LOCI,
            source_text='"""Emit final report to the client surface."""\n\ndef emit():\n    pass\n',
        )
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["mechanical_name"], "output")
        self.assertIn(m["strength"], {"ADEQUATE", "WEAK"})

    def test_enochian_edge_compound(self) -> None:
        m = _map_node_to_locus(_node("svc.edge_intake"), ENOCHIAN_LOCI)
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m["mechanical_name"], "edge_intake")
        self.assertEqual(m["strength"], "STRONG")

    def test_never_invents_symbolic(self) -> None:
        m = _map_node_to_locus(
            _node("pkg.totally_unknown_xyz"),
            TREE_LOCI,
            source_text="noise without locus words",
        )
        # May be None or weak on accidental token; symbolic must be from loci
        if m is not None:
            allowed = {s for _, s, _ in TREE_LOCI}
            self.assertIn(m["symbolic_locus"], allowed)
            self.assertIn(m["mechanical_name"], {x for x, _, _ in TREE_LOCI})

    def test_score_prefers_stronger_secondary(self) -> None:
        a = _score_locus_match(
            leaf="intake",
            nid="pkg.intake",
            tokens={"intake"},
            role_tokens={"intake"},
            path_segs={"pkg", "intake"},
            mech="intake",
            sym="chokmah",
            note="Raw force intake",
        )
        b = _score_locus_match(
            leaf="something",
            nid="pkg.something",
            tokens={"raw"},
            role_tokens={"raw"},
            path_segs={"pkg", "something"},
            mech="intake",
            sym="chokmah",
            note="Raw force intake",
        )
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        assert a is not None and b is not None
        self.assertEqual(a[0], "STRONG")
        self.assertEqual(b[0], "WEAK")
        self.assertGreater(a[1], b[1])

    def test_suggest_frameworks_token_aware(self) -> None:
        nodes = [
            _node("a.edge_intake"),
            _node("a.cross_domain_bus"),
            _node("a.sovereign_intent"),
        ]
        frameworks = {
            "enochian": {"default_loci": ENOCHIAN_LOCI},
            "tree-of-life": {"default_loci": TREE_LOCI},
            "numogram": {
                "default_loci": [
                    ("potential", "p", "p"),
                    ("init", "i", "i"),
                ]
            },
        }
        ranked = _suggest_frameworks(nodes, frameworks)
        self.assertTrue(ranked)
        self.assertEqual(ranked[0], "enochian")


if __name__ == "__main__":
    unittest.main()
