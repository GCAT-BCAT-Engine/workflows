#!/usr/bin/env python3
import json
import pathlib
from semantic_validation import validate

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
SOURCE = OUT / "results.json"

if not SOURCE.exists():
    raise SystemExit("results/results.json not found")

summary = json.loads(SOURCE.read_text())
rejudged = []
for lane in summary.get("results", []):
    lane_rows = []
    highest = "NONE"
    for stage in lane.get("stages", []):
        verdict = validate(stage["stage_id"], stage.get("output", ""))
        lane_rows.append({
            "stage_id": stage["stage_id"],
            "original": stage.get("validation", {}),
            "offline": verdict,
            "changed": bool(stage.get("validation", {}).get("admitted")) != verdict["admitted"],
            "output_hash": stage.get("output_hash"),
        })
        if verdict["admitted"]:
            highest = stage["stage_id"]
        else:
            break
    rejudged.append({
        "lane_id": lane["lane_id"],
        "original_highest": lane.get("highest_admitted_stage", "NONE"),
        "offline_highest": highest,
        "available_stage_count": len(lane.get("stages", [])),
        "stages": lane_rows,
        "requires_provider_rerun_from": None if highest == "S6" else f"S{int(highest[1:]) + 1}" if highest != "NONE" else "S0",
    })

out = {
    "experiment_id": summary.get("experiment_id"),
    "adjudication_status": "OFFLINE_RESCORING_ONLY",
    "validator": "semantic-structural-v2",
    "lanes": rejudged,
    "boundary": "This rescoring uses retained outputs only. It does not invent missing downstream stages or alter observed provider tokens, cost, or latency.",
}
(OUT / "offline-adjudication.json").write_text(json.dumps(out, indent=2))

lines = [
    "# Offline Semantic Adjudication",
    "",
    "| Lane | Original stage | Offline stage | Available outputs | Next required stage |",
    "|---|---:|---:|---:|---:|",
]
for lane in rejudged:
    lines.append(
        f"| {lane['lane_id']} | {lane['original_highest']} | {lane['offline_highest']} | "
        f"{lane['available_stage_count']} | {lane['requires_provider_rerun_from'] or 'none'} |"
    )
lines += ["", "## Boundary", "", out["boundary"]]
(OUT / "offline-adjudication.md").write_text("\n".join(lines) + "\n")
print(json.dumps(out, indent=2))
