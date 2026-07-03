# Experiment Log — e00001 damped oscillator

Lab notebook: one entry per campaign, in run order. Fields: Question / Setup /
Result / Verdict / Next. This is a research record, not a file changelog — it
says what was tried and what happened, including negative results. (Two entries
below are enough to show the format for this sample.)

---

## AA — underdamped baseline ★

- **Question:** Does `zeta=0.2` produce a decaying oscillation with clear
  overshoot, suitable as the flagship figure?
- **Setup:** `bash scripts/exps/AA.sh` — `oscillator` campaign, `omega=1.0`,
  `zeta=0.2`, `x0=1.0`, `t_max=30`, `seed=1`.
- **Result:** overshoot 0.53, settling time 13.8 s (seed 1). Clean decaying
  oscillation. `trajectory.png` copied to
  `writing/w00003_sample_note/figures/oscillator_underdamped.png`.
- **Verdict:** ★ flagship figure for the writing sample.
- **Next:** run AB (critical) as the no-overshoot contrast.

## AB — critically damped contrast

- **Question:** Does `zeta=1.0` remove the oscillation and return fastest?
- **Setup:** `bash scripts/exps/AB.sh` — same kernel, `zeta=1.0`, `seed=1`.
- **Result:** overshoot 0.00, settling 4.8 s (seed 1) — fastest return, no
  oscillation. AC (overdamped) later settles at 14.6 s, i.e. slower than
  critical, as expected.
- **Verdict:** confirms the regime boundary; useful teaching contrast.
- **Next:** AC (overdamped) to complete the three-regime picture.
