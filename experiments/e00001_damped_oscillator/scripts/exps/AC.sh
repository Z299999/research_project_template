#!/usr/bin/env bash
# GOAL AC — overdamped (zeta=2.5): slow non-oscillatory return. Completes the
#           three-regime picture.
# RESULT — overshoot 0.00, settling time 14.6 s (seed 1). Slow non-oscillatory
#          return — slower than critical, as expected.
set -e
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$DIR/run.py" --exp oscillator --config "$DIR/scripts/exps/AC_overdamped.yaml" --tag AC --seed 1
