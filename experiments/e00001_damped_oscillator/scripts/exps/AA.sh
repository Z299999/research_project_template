#!/usr/bin/env bash
# GOAL AA — underdamped regime (zeta=0.2): a decaying oscillation with clear
#           overshoot. This is the flagship figure used by writing/w00003.
# RESULT — overshoot 0.53, settling time 13.8 s (seed 1). Clean decaying
#          oscillation; used as the flagship figure.
set -e
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$DIR/run.py" --exp oscillator --config "$DIR/scripts/exps/AA_underdamped.yaml" --tag AA --seed 1
