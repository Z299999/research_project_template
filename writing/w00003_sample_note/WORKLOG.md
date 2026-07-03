# Worklog — w00003 sample note

Writing notebook (analog of an experiment's `EXPERIMENT_LOG.md`): one entry per
work session, newest last. A research record of writing decisions — not a file
changelog (git covers that). Two entries below show the format.

---

## Draft the note and wire in the experiment figure

- **Goal:** stand up a minimal note that builds and consumes the e00001 figure.
- **Did:** wrote the abstract + `01_model` section; stated the three-regime
  behaviour as a `proposition`; copied `e00001/runs/latest/trajectory.png` into
  `figures/oscillator_underdamped.png` and included it as Fig. 1.
- **Result:** `python3 build.py` produces `main.pdf` (2 pages).
- **Next:** add the citation and confirm BibTeX resolves it.

## Add the citation and confirm the BibTeX loop

- **Goal:** exercise `\cite` end-to-end.
- **Did:** added `strogatz2015nonlinear` to `references.bib` and the matching
  `b00002` entry to `literature/bibliography.jsonl`; cited it in `01_model`.
- **Result:** BibTeX resolves; the reference renders. Note builds clean.
- **Next:** none — this is a template sample, not an active manuscript.
