#!/usr/bin/env bash
# GOAL AB — critically damped (zeta=1.0): fastest non-oscillatory return, no
#           overshoot. Contrast against AA.
# RESULT — overshoot 0.00, settling time 4.8 s (seed 1). Fastest return, no
#          oscillation — confirms the critical boundary.
set -e
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$DIR/run.py" --exp oscillator --config "$DIR/scripts/exps/AB_critical.yaml" --tag AB --seed 1
