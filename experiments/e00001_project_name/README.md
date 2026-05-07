# e00001 — [Experiment Name]

## Goal

[One paragraph: what hypothesis or question this experiment tests, and
how it connects to the writing project it supports.]

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run the main experiment
python run.py run

# Show current status
python run.py status
```

Run outputs are written to `runs/<YYYYMMDD_HHMMSS>/` (gitignored).
Paper-ready figures are saved to `figure/` (tracked).

## Structure

```
config.yaml    — hyperparameters and settings
run.py         — main entry point / CLI dispatcher
scripts/       — helper modules
figure/        — paper-ready output figures (tracked)
runs/          — timestamped run outputs (gitignored)
```
