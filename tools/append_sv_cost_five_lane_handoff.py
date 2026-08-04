#!/usr/bin/env python3
"""Append the completed five-lane publication state after terminal handoff reconciliation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "SV_COST_MIRROR_HANDOFF.md"
CONSOLIDATION = ROOT / "experiments/sv-cost-program/five-lane-results/session-consolidation.json"
START = "<!-- SV_COST_FIVE_LANE_PUBLICATION:BEGIN -->"
END = "<!-- SV_COST_FIVE_LANE_PUBLICATION:END -->"


def main() -> int:
    state = json.loads(CONSOLIDATION.read_text(encoding="utf-8"))
    if state.get("state") != "ARCHIVE_READY":
        raise SystemExit("five-lane session consolidation is not ARCHIVE_READY")
    if state.get("archive_conditions", {}).get("archive_ready") is not True:
        raise SystemExit("five-lane archive conditions are incomplete")

    block = f"""{START}
## Adjacent completed five-lane publication

- Goal ID: `SV-COST-FIVE-LANE-PUBLICATION-001`
- State: `ARCHIVE_READY`
- Operation class: `governed_state_reconstruction`
- Comparison unit: `successful equivalent admissible outcome`
- Five-lane result: `experiments/sv-cost-program/five-lane-results/results/five_lane_results.json`
- Session consolidation: `experiments/sv-cost-program/five-lane-results/session-consolidation.json`
- Publisher handoff: `GCAT-BCAT-Engine/Publisher/docs/SV_COST_FIVE_LANE_PUBLICATION_MIRROR_HANDOFF.md`
- Site handoff: `StegVerse-Labs/Site/papers/SV_COST_FIVE_LANE_MIRROR_HANDOFF.md`

| Lane | Cost per successful equivalent admissible outcome | Status |
|---|---:|---|
| OpenAI raw | $0.006875 | PASS |
| OpenAI governed | $0.006880 | PASS |
| Anthropic raw | $0.010656 | PASS |
| Anthropic governed | $0.007116 | PASS |
| StegVerse-only deterministic reconstruction | $0.000000002885 | PASS |

Hosted publication evidence:

- experimental evidence commit: `3720211a1cfaaf2db697f3e26194d083db21e94f`;
- Publisher PDF run: `30930126860`;
- Publisher PDF job: `92062384747`;
- Publisher immutable artifact: `8900768707`;
- Publisher PDF commit: `dc684109351e3b0b0148a69b116d120415489a02`;
- PDF SHA-256: `sha256:e19bfb6f59d11d4abe21400846cdc050678a89eb1a0b07da745a22b7b33ea1f6`;
- Site public verification run: `30928531888`;
- Site public verification issue: `StegVerse-Labs/Site#173`, closed;
- all publication implementation, validation, and integration claims: `COMPLETE — RELEASED`.

Claim boundary: this is one bounded deterministic reconstruction operation. It does not establish universal provider economics, invoice-reconciled provider charges, enterprise-wide savings, company ROI, or fresh-inference equivalence.

The earlier statement that no downstream propagation was claimed is superseded only for this bounded five-lane publication. No favorable general savings or ROI propagation is admitted. Issue `#13` remains the only canonical continuation for a future favorable general ROI revision and is not an archival dependency of the completed publication session.

MERGED INTO:

- `GCAT-BCAT-Engine/workflows/experiments/sv-cost-program/five-lane-results/session-consolidation.json`
- `GCAT-BCAT-Engine/Publisher/docs/SV_COST_FIVE_LANE_PUBLICATION_MIRROR_HANDOFF.md`
- `StegVerse-Labs/Site/papers/SV_COST_FIVE_LANE_MIRROR_HANDOFF.md`

The originating five-lane publication session contains no unique remaining authority and is archive-ready.
{END}"""

    text = HANDOFF.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    HANDOFF.write_text(text, encoding="utf-8")
    print("SV_COST_FIVE_LANE_HANDOFF_APPEND_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
