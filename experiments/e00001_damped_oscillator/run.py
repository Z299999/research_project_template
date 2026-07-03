#!/usr/bin/env python3
"""Main entry point for e00001.

Usage:
    python run.py run      - run the experiment
    python run.py status   - show current output status
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS_DIR = ROOT / "runs"
FIGURE_DIR = ROOT / "figure"


def make_run_dir(tag: str = "") -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{stamp}_{tag}" if tag else stamp
    run_dir = RUNS_DIR / name
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def cmd_run() -> int:
    run_dir = make_run_dir("run")
    print(f"Run output → {run_dir}")
    # TODO: replace with actual experiment logic
    print("(placeholder: add your experiment code in scripts/ and call it here)")
    return 0


def cmd_status() -> None:
    print("=== Status ===")
    if RUNS_DIR.exists():
        runs = sorted(RUNS_DIR.iterdir())
        print(f"Runs ({len(runs)} total):")
        for r in runs[-5:]:
            print(f"  {r.name}")
        if len(runs) > 5:
            print(f"  ... and {len(runs) - 5} more")
    else:
        print("No runs yet.")
    figs = list(FIGURE_DIR.glob("*")) if FIGURE_DIR.exists() else []
    print(f"Figures: {len(figs)} file(s) in figure/")


COMMANDS = {
    "run": cmd_run,
    "status": cmd_status,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        print("Commands:", ", ".join(COMMANDS))
        return 1
    result = COMMANDS[sys.argv[1]]()
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
