#!/usr/bin/env python3
"""Canonical seven-lane Generation-2 entrypoint.

Provider generation occurs outside this workload. StegVerse receives candidate outputs,
never provider API keys. See run_candidate_outputs.py and task.json.
"""
from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).parent
runpy.run_path(str(ROOT / "run_candidate_outputs.py"), run_name="__main__")
