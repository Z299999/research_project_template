# Idea — damped harmonic oscillator (sample experiment)

## Hypothesis / question

The damping ratio `zeta` alone controls whether a second-order system
oscillates. For fixed natural frequency `omega`, sweeping `zeta` across the
three regimes should show:

- `zeta < 1` (underdamped): decaying oscillation with visible overshoot;
- `zeta = 1` (critical): fastest return to zero with no overshoot;
- `zeta > 1` (overdamped): slow, non-oscillatory return.

## Why this experiment exists

This is the repository's **reference example** for the experiment workflow in
`prompt/c008_experiment_structure_guideline.md`. Its scientific content is
deliberately textbook — the point is to demonstrate the structure:

- one stable `src/` kernel (`oscillator.simulate` + `viz.fig_*`);
- three campaigns (AA / AB / AC) that vary **only configuration**, not code;
- immutable, gitignored `runs/`, with the flagship figure copied out to
  `writing/w00003_sample_note/figures/`.

Copy this folder to start a real experiment, then replace `src/` and
`scripts/exps/` with your own model and campaigns.
