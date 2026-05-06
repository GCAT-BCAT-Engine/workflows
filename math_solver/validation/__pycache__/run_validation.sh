#!/bin/bash
# StegVerse Validation Run - Quick Start
# Usage: ./run_validation.sh

echo "=== StegVerse Validation Run VAL-001 ==="
echo "Budget ceiling: $10.00"
echo ""

# Check if validation spec exists
if [ ! -f "validation_run_v1.yml" ]; then
    echo "Error: validation_run_v1.yml not found"
    exit 1
fi

echo "Phase 1: Preprocessing (Haiku 4.5, ~$2.00)"
echo "  - Load problem_spec_sv_math_001.yml"
echo "  - Generate complexity estimate"
echo ""

echo "Phase 2: Quick Probe (Sonnet 4.6, ~$6.00)"
echo "  - 30-minute reasoning trace"
echo "  - Generate proof sketch"
echo ""

echo "Phase 3: Sandbox (GitHub Actions, ~$0.10)"
echo "  - Lean syntax validation"
echo "  - Determinism check"
echo ""

echo "Phase 4: Cost Tracking (StegDB, $0.00)"
echo "  - Verify dashboard displays"
echo ""

echo "Phase 5: TV/TVC Status (TV artifact, $0.00)"
echo "  - API key valid"
echo "  - Budget ceiling active"
echo ""

echo "=== Ready to execute ==="
echo "To run: python3 validation_runner.py"
echo "Or manually trigger each phase via your preferred method"
