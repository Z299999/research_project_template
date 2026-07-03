# Experiment Structure Guideline

This is the repository standard for how numerical experiments are written and
organized under `experiments/`. **Every new experiment, and every extension of
an existing one, must follow this structure.**

The worked reference example is
`experiments/e00001_damped_oscillator/` — mirror it when starting a new
experiment.

Use this guideline whenever you create a new experiment folder, add a campaign
to an existing one, or refactor experiment code.

## Main Principle

**The code is a stable kernel; each experiment is a frozen, reproducible
record.**

Concretely:

- The model / solver / plotting code lives in `src/` and does **not** change
  from one experiment to the next. Different experiments vary *configuration*,
  not source.
- Each experimental run is captured by a frozen shell record and an immutable,
  timestamped output directory, so any result in the paper can be traced back to
  the exact command and code that produced it.

If you find yourself copy-pasting and editing the model code to run a variant,
stop: the variation belongs in a config preset, not in a forked kernel.

## Standard Layout

```
experiments/eXXXXX_<short_name>/
  README.md               how to run (campaign table) + where figures go
  idea.md                 the scientific idea / hypothesis in prose
  EXPERIMENT_LOG.md       lab notebook: one entry per campaign
  requirements.txt        minimal deps (prefer numpy + matplotlib only)
  config.yaml             the default preset (usually a copy of the flagship)
  .gitignore              runs/, __pycache__/, *.pyc
  run.py                  single entry point (dispatch table over campaigns)
  src/                    STABLE kernel — does not change between campaigns
    __init__.py
    <model>.py            simulate(...) returning a results dict
    viz.py                fig_*(res, out_path) plotting functions
  scripts/exps/           frozen campaign records (not drivers)
    AA.sh                 GOAL/RESULT header + one reproducible command
    AA_<name>.yaml        config preset for that campaign
    AB.sh
    ...
  runs/                   GITIGNORED. one immutable dir per run + latest/
    20260703_141530_AA_seed1/
    latest/               mirror of the most recent run
```

## The Rules

### 1. `src/` is the stable kernel

- Put every model variant and every plotting routine here. Fixing a bug in
  `src/` must fix it uniformly for all campaigns — never keep forked copies of
  the model.
- Model functions expose a single `simulate(...)` with keyword arguments and
  defaults, and return a plain results dict (arrays keyed by name).
- Plotting functions have the shape `fig_<name>(res, out_path, ...)` and write a
  figure file; they never re-run the simulation.

### 2. A campaign is a frozen record, not a driver

- Each experiment you actually run is frozen in `scripts/exps/<CODE>.sh`. The
  shell file is a **record**: a top comment with `GOAL` and (after running)
  `RESULT`, followed by the one exact, reproducible command. It is not a place
  for logic or loops beyond the single invocation.
- Campaign codes are a **flat two-letter sequence in run order**: `AA`, `AB`,
  `AC`, ..., `AZ`, `BA`, .... The letters carry **no meaning** — they are just
  the order in which campaigns were run. Do not encode topic or status in the
  code; that goes in the paired preset name and the log.
- The shell record is named `<CODE>.sh`; its paired config preset carries a
  descriptive suffix, `scripts/exps/<CODE>_<name>.yaml`.

Example `scripts/exps/AA.sh`:

```bash
#!/usr/bin/env bash
# GOAL AA — underdamped regime (zeta=0.2): show a decaying oscillation with
#           clear overshoot.
# RESULT — overshoot ~0.53, settling time ~19 s; flagship trajectory figure.
set -e
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$DIR/run.py" --exp oscillator --config "$DIR/scripts/exps/AA_underdamped.yaml" --tag AA --seed 1
```

### 3. Config presets, loosely parsed

- Presets are flat `key: value` YAML (`scripts/exps/<CODE>_<name>.yaml`). Keep
  `config.yaml` at the root as the default preset (usually the flagship).
- `run.py` filters preset keys against each function's signature (see the
  `only_kwargs` contract below), so a preset may carry extra keys (e.g. viz-only
  options) without breaking `simulate`.

### 4. Runs are immutable and gitignored

- Every invocation writes a fresh directory
  `runs/<YYYYMMDD_HHMMSS>_<tag>_seed<N>/` and **never overwrites** an existing
  one. Each run's outputs live entirely inside its own subdirectory; runs never
  share files or write into each other.
- `runs/latest/` is a convenience mirror of **only the most recent run**: each
  invocation wipes the old `latest/` and replaces it with a copy of the new run,
  so `latest/` always shows the newest outputs and never a mix of old and new.
  The timestamped directories are the permanent record; `latest/` is disposable.
- Each run directory contains the outputs (figures), a `metrics.json` summary,
  and a `config.yaml` snapshot of the exact settings used.
- `runs/` is in `.gitignore`. **Never commit run outputs** — they are
  regenerable from the frozen script + preset.

### 5. Paper figures are copied out explicitly

- A figure enters a manuscript only by an explicit copy from `runs/latest/` to
  `writing/<project>/figures/`. This copy is the single, traceable bridge
  between an experiment and the paper.
- Record which campaign produced each paper figure in `EXPERIMENT_LOG.md`.

### 6. `EXPERIMENT_LOG.md` is the lab notebook

- One entry per campaign, in run order, using the fields:
  **Question / Setup / Result / Verdict / Next**. Put a one-line verdict in the
  entry title and mark a successful campaign with `★`.
- The Setup line names the command and the key parameters; the Result line
  states what actually happened (including negative results and why).

## `run.py` Minimal Contract

`run.py` is the single entry point. It must provide:

- CLI: `--exp <name>` (required, selects a campaign function), `--config <yaml>`,
  `--tag <CODE>`, `--seed <int>`.
- A `CAMPAIGNS` dispatch table mapping `--exp` names to functions
  `exp_<name>(cfg, out)` that call `src` and write figures into `out`.
- `only_kwargs(func, cfg)` — keep only the config keys `func` accepts, via
  `inspect.signature`, so presets can carry extra keys.
- `new_run_dir(tag, seed)` — make `runs/<timestamp>_<tag>_seed<N>/` (never
  overwrite); `mirror_latest(out)` — copy it into `runs/latest/`.
- After the campaign runs, write `metrics.json` (a small dict of headline
  numbers) and a `config.yaml` snapshot into the run directory.

```python
def only_kwargs(func, cfg):
    ok = set(inspect.signature(func).parameters)
    return {k: v for k, v in cfg.items() if k in ok}

def new_run_dir(tag, seed):
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = ROOT / "runs" / f"{stamp}_{tag}_seed{seed}"
    out.mkdir(parents=True, exist_ok=True)
    return out
```

Prefer parsing the flat config by hand (default `python3` may lack `pyyaml`);
cast each value to `int`, then `float`, else keep the string.

## Naming and Registration

- Experiment folders: `eXXXXX_<short_name>` (five-digit, matching the writing
  project it serves, e.g. `e00001` ↔ `w00001`).
- Register every experiment in `experiments/catalog.jsonl`.
- Campaign codes `AA, AB, ...` are local to each experiment's `scripts/exps/`.

## Quick Checklist (before committing an experiment change)

- [ ] Variation lives in a config preset, not a forked copy of `src/`.
- [ ] The campaign is frozen in `scripts/exps/<CODE>.sh` with GOAL/RESULT.
- [ ] Campaign code is the next flat `AA/AB/...` in run order.
- [ ] Run wrote a fresh `runs/<timestamp>_<tag>_seedN/`; nothing was overwritten.
- [ ] `runs/` is gitignored; no run outputs are staged.
- [ ] Paper figures copied to `writing/.../figures/` and noted in the log.
- [ ] `EXPERIMENT_LOG.md` has a Question/Setup/Result/Verdict/Next entry.
- [ ] Experiment registered in `experiments/catalog.jsonl`.

## Scaffolding a New Experiment (recipe)

To create `experiments/eXXXXX_<name>/`:

1. Copy the layout above (fastest: mirror the reference
   `experiments/e00001_damped_oscillator/`, then empty `src/` and
   `scripts/exps/`).
2. Write `idea.md` (the hypothesis) and a first `src/<model>.py` with a
   `simulate(...)` returning a results dict, plus `viz.fig_*` plotters.
3. Add a campaign in `run.py`'s `CAMPAIGNS` table and a first
   `scripts/exps/AA.sh` + `AA_<name>.yaml`.
4. Add `.gitignore` (`runs/`, `__pycache__/`, `*.pyc`), `requirements.txt`,
   `config.yaml`, `README.md`, and start `EXPERIMENT_LOG.md`.
5. Register the experiment in `experiments/catalog.jsonl`.
6. Run `bash scripts/exps/AA.sh`, then fill the AA `RESULT:` line and the
   log entry.
