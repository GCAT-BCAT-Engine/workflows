#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

from gcat_bcat_receipt_replay import run_replay


def read_jsonl(path: Path):
    receipts = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                receipts.append(json.loads(line))
    return receipts


def write_jsonl(path: Path, receipts):
    with path.open("w", encoding="utf-8") as f:
        for receipt in receipts:
            f.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")


def build_tampered_receipts(source: Path, out_path: Path):
    receipts = read_jsonl(source)
    if not receipts:
        raise RuntimeError("No receipts to tamper with")

    tampered = [dict(r) for r in receipts]

    # Tamper with the first receipt's decision while leaving receipt_hash unchanged.
    tampered[0] = json.loads(json.dumps(tampered[0]))
    original = tampered[0]["decision"]["outcome"]
    tampered[0]["decision"]["outcome"] = "DENY" if original != "DENY" else "ALLOW"
    tampered[0]["decision"]["reason"] = "tampered_decision"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_path, tampered)
    return {
        "tampered_file": str(out_path),
        "tampered_candidate_id": tampered[0].get("candidate_id"),
        "original_outcome": original,
        "tampered_outcome": tampered[0]["decision"]["outcome"],
    }


def build_tamper_summary(meta, replay_report):
    return "\n".join([
        "# GCAT/BCAT Tamper Detection Summary",
        "",
        "## Tamper Operation",
        "",
        f"- Tampered file: `{meta['tampered_file']}`",
        f"- Tampered candidate: **{meta['tampered_candidate_id']}**",
        f"- Original outcome: **{meta['original_outcome']}**",
        f"- Tampered outcome: **{meta['tampered_outcome']}**",
        "",
        "## Detection Result",
        "",
        f"- Receipts replayed: **{replay_report['summary']['total']}**",
        f"- Replay failures detected: **{replay_report['summary']['failed']}**",
        f"- Tamper detected: **{replay_report['summary']['failed'] > 0}**",
        f"- Chain valid after tamper: **{replay_report['chain_valid']}**",
        "",
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipts", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    source = Path(args.receipts)
    out_dir = Path(args.out_dir)
    tampered_path = out_dir / "gcat_bcat_sandbox_receipts_tampered.jsonl"

    meta = build_tampered_receipts(source, tampered_path)
    replay_report = run_replay(
        tampered_path,
        out_dir,
        report_prefix="gcat_bcat_tamper_replay",
        title="GCAT/BCAT Tampered Receipt Replay Summary",
    )

    tamper_report = {
        "schema": "stegverse.sandbox.gcat_bcat.tamper_detection_report.v1",
        "tamper": meta,
        "tamper_detected": replay_report["summary"]["failed"] > 0,
        "replay_summary": replay_report["summary"],
        "chain_valid_after_tamper": replay_report["chain_valid"],
    }

    (out_dir / "gcat_bcat_tamper_detection_report.json").write_text(
        json.dumps(tamper_report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "gcat_bcat_tamper_detection_summary.md").write_text(
        build_tamper_summary(meta, replay_report),
        encoding="utf-8",
    )

    print(json.dumps(tamper_report, indent=2, sort_keys=True))
    return 0 if tamper_report["tamper_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
