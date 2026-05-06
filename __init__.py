"""
triad package

This package implements validation, sandbox receipt generation, replay,
and tamper‑detection logic for the so‑called "Triad" admissibility
transform.  The Triad combines five lower‑level governance layers—
GCAT, BCAT, ECAT, ICAT, and PE—into a single decision engine.  Each
layer must individually return an ALLOW outcome for the Triad to
authorize a transition.  If any layer returns a FAIL_CLOSED result,
the Triad also returns FAIL_CLOSED; if any layer returns DENY, the
Triad returns DENY unless a FAIL_CLOSED has already been detected.

The Triad modules mirror the structure used for the ECAT/ICAT/PE
components in the ecat_icat package.  The key entry point is
``triad_validator.py`` which reads candidates, applies the individual
validators, aggregates the results and costs, and determines whether
a scalar constant (shared base_cost) exists across all five layers.

Other scripts in this package provide sandbox receipt generation and
replay, as well as a simple tamper‑detection test.  See the
``README.md`` file in this directory for usage instructions.
"""
