# e00001 — Damped Harmonic Oscillator (sample experiment)

A minimal, runnable worked example of the repository's experiment workflow
(`prompt/c008_experiment_structure_guideline.md`). It integrates

    x'' + 2 zeta omega x' + omega^2 x = 0

and shows how a single stable kernel yields three regimes from configuration
alone. Supports the writing sample `writing/w00003_sample_note`.

## Run it

```bash
pip install -r requirements.txt
bash scripts/exps/AA.sh   # underdamped   (zeta=0.2) — flagship
bash scripts/exps/AB.sh   # critical      (zeta=1.0)
bash scripts/exps/AC.sh   # overdamped    (zeta=2.5)
```

Each run writes an immutable `runs/<timestamp>_<CODE>_seed<N>/` containing
`trajectory.png`, `phase.png`, `metrics.json`, and a `config.yaml` snapshot, and
refreshes `runs/latest/`. `runs/` is gitignored.

## Campaigns

| Code | Preset                      | Regime            |
|------|-----------------------------|-------------------|
| AA   | `AA_underdamped.yaml`       | underdamped, ζ=0.2 (flagship) |
| AB   | `AB_critical.yaml`          | critically damped, ζ=1.0 |
| AC   | `AC_overdamped.yaml`        | overdamped, ζ=2.5 |

## Where figures go

The flagship AA `trajectory.png` is copied to
`writing/w00003_sample_note/figures/oscillator_underdamped.png`. That explicit
copy is the only bridge from experiment to paper (see `EXPERIMENT_LOG.md`).

## Layout

```
src/            stable kernel — oscillator.simulate(...) + viz.fig_*(res, out)
run.py          single entry point (--exp / --config / --tag / --seed)
config.yaml     default preset (= flagship AA)
scripts/exps/   frozen campaign records: <CODE>.sh + <CODE>_<name>.yaml
runs/           immutable timestamped outputs + latest/  (gitignored)
idea.md         the hypothesis
EXPERIMENT_LOG.md   lab notebook, one entry per campaign
```
