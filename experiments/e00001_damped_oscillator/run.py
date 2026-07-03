#!/usr/bin/env python3
"""Single entry point for the damped-oscillator sample experiment.

Usage:
    python3 run.py --exp oscillator --config scripts/exps/AA_underdamped.yaml \
                   --tag AA --seed 1

Campaigns are selected by --exp (see CAMPAIGNS). Each invocation writes a fresh,
immutable run directory under runs/ and mirrors it to runs/latest/. This file is
the same across every campaign; campaigns differ only in the --config preset.
See ../../prompt/c008_experiment_structure_guideline.md for the full contract.
"""

from __future__ import annotations

import argparse
import datetime as dt
import inspect
import json
import shutil
from pathlib import Path

from src import oscillator, viz

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"


# ---------------------------------------------------------------- config utils
def load_config(path: Path) -> dict:
    """Parse flat `key: value` YAML by hand (default python3 may lack pyyaml).

    Each value is cast to int, then float, else kept as a string. Blank lines
    and `#` comments are ignored.
    """
    cfg: dict = {}
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, raw = (p.strip() for p in line.split(":", 1))
        for cast in (int, float):
            try:
                cfg[key] = cast(raw)
                break
            except ValueError:
                continue
        else:
            cfg[key] = raw
    return cfg


def only_kwargs(func, cfg: dict) -> dict:
    """Keep only the config keys `func` actually accepts."""
    ok = set(inspect.signature(func).parameters)
    return {k: v for k, v in cfg.items() if k in ok}


# ------------------------------------------------------------------ run dirs
def new_run_dir(tag: str, seed: int) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = RUNS / f"{stamp}_{tag}_seed{seed}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def mirror_latest(out: Path) -> None:
    latest = RUNS / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    shutil.copytree(out, latest)


# ------------------------------------------------------------------ campaigns
def exp_oscillator(cfg: dict, out: Path, seed: int) -> dict:
    """Run one oscillator regime and write both figures. Returns metrics."""
    res = oscillator.simulate(seed=seed, **only_kwargs(oscillator.simulate, cfg))
    title = cfg.get("title")
    viz.fig_trajectory(res, out / "trajectory.png", title=title)
    viz.fig_phase(res, out / "phase.png", title=title)
    return oscillator.metrics(res)


CAMPAIGNS = {
    "oscillator": exp_oscillator,
}


# ------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--exp", required=True, choices=sorted(CAMPAIGNS))
    ap.add_argument("--config", type=Path, default=ROOT / "config.yaml")
    ap.add_argument("--tag", default="XX")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    cfg = load_config(args.config)
    out = new_run_dir(args.tag, args.seed)

    metrics = CAMPAIGNS[args.exp](cfg, out, args.seed)

    (out / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    shutil.copy(args.config, out / "config.yaml")
    mirror_latest(out)

    print(f"[{args.tag}] {args.exp}  seed={args.seed}")
    print(f"  out     -> {out.relative_to(ROOT)}")
    print(f"  metrics -> {metrics}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
