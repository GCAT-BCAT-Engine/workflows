#!/usr/bin/env python3
"""Compatibility entrypoint for the former direct-key DeepSeek pair runner.

Generation 2 no longer permits provider API keys inside the StegVerse test workload.
DeepSeek output must be supplied through candidate-inputs/deepseek.json and is processed
by the canonical credentialless seven-lane candidate-output runner.
"""
from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).parent
runpy.run_path(str(ROOT / "run_candidate_outputs.py"), run_name="__main__")
