"""Inference Window package.

This package contains a proof‑of‑concept implementation of an
"inference window" admissibility gate.  The inference window layer
evaluates whether the model’s window of observed information is
sufficient to make a reliable decision.  Each candidate encodes a
``window.size`` value between 0 and 1 and parameters defining a
minimum acceptable window size and cost scaling factors.  The
inference window module supports standalone validation, sandbox
receipt generation, replay verification and tamper detection.

"""

__all__ = [
    "iw_validator",
    "sandbox_adapter",
    "receipt_replay",
    "tamper_test",
]