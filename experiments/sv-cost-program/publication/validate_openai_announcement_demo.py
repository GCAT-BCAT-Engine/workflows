#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "experiments/sv-cost-program/publication/openai-announcement-demo-manifest.json"
COPY = ROOT / "docs/OPENAI_ANNOUNCEMENT_STREAM_GOVERNANCE_DEMO.md"
DECISION = ROOT / "experiments/sv-cost-program/stream-governance/results/stream_governance_decision.json"
COSTS = ROOT / "experiments/sv-cost-program/stream-governance/results/lane_costs.json"


def main() -> int:
    m = json.loads(MANIFEST.read_text())
    d = json.loads(DECISION.read_text())
    c = json.loads(COSTS.read_text())
    text = COPY.read_text()

    assert m["status"] == "READY_FOR_HUMAN_POSTING"
    assert m["evidence_class"] == "SYNTHETIC_DETERMINISTIC_CALIBRATION"
    assert d["status"] == "SYNTHETIC_PILOT_COMPLETE"
    assert d["stream_cost_ratio"] == c["comparison"]["native_to_governed_cost_ratio"]
    assert d["replay_cost_ratio"] == c["comparison"]["replay_savings_ratio"]
    assert "This is not a claim of observed OpenAI billing savings or production ROI." in text
    assert "Mechanism demonstrated. Live provider validation next." in text
    assert all(m["publication_gates"].values())
    print(json.dumps({
        "valid": True,
        "publication_id": m["publication_id"],
        "status": m["status"],
        "stream_cost_ratio": d["stream_cost_ratio"],
        "replay_cost_ratio": d["replay_cost_ratio"]
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
