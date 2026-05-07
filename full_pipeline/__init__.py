"""
full_pipeline package
---------------------

This package provides a minimal proof‑of‑concept "full stack" governance
validator that wraps the existing Triad validator and illustrates how
additional layers could be composed on top.  The goal is to show how
the Triad layer—combining GCAT/BCAT, ECAT, ICAT, Probability of
Existence and the Inference Window—can be plugged into a larger
evaluation harness without altering the Triad logic itself.

The ``full_pipeline_validator`` exports a single function
``validate_full_candidate`` which accepts a candidate JSON object
formatted for the Triad validator and returns an overall outcome
(ALLOW, DENY or FAIL_CLOSED), a reason string, and a details
dictionary.  At present the implementation simply delegates to the
Triad validator and assumes that any additional layers (e.g. Rigel,
reconstruction, temporal lag) would either return ``ALLOW`` or
contribute their own cost components.  The structure of the return
value mirrors that of ``validate_triad_candidate`` but nests the
Triad layer results under a ``"triad"`` key.

Future extensions can replace the stubbed sections with actual
validators for the remaining admissibility layers.
"""

from .full_pipeline_validator import validate_full_candidate  # noqa:F401