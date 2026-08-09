# Research Project Template

A template for AI-assisted academic research projects. Clone or use as a GitHub Template
to bootstrap a new project with a consistent folder layout, LaTeX writing infrastructure,
literature management, and reusable AI prompt library.

## Folder Layout

```
CLAUDE.md         — project instructions for Claude Code (fill in before first session)
TIMELINE.md       — research log, advisor meetings, reading log, and active todo list
writing/          — LaTeX writing projects (w00001, w00002, ...)
  catalog.jsonl   — registry of all writing projects
  w00001_*/       — paper template (article/conference, 6-section)
  w00002_*/       — report/survey template (papercode/personcode clickable links)
  w00003_*/       — worked sample note: builds to a 2-page PDF, includes a
                    figure copied from experiment e00001 (the experiment→paper bridge)
literature/       — paper library and metadata
  bibliography.jsonl  — lightweight metadata index for all registered papers
  pdf_papers/     — papers, organized by topic subfolder
  pdf_books/      — book chapters
  tex/            — TeX sources of manuscripts (collaborator drafts, arXiv sources)
experiments/      — numerical experiments and simulations (e00001, ...)
  catalog.jsonl   — registry of all experiments
  e00001_*/       — worked sample experiment (c008 layout: src/ kernel,
                    scripts/exps/ campaigns, immutable runs/); runnable
drafts/           — email drafts and planning notes for advisor communication
                    (d0001 sample included)
feedbacks/        — advisor feedback notes and revision records
                    (f0001 sample included)
prompt/           — reusable AI prompt templates (c000–c012)
```

## Quick Start

**Day 1 — repo setup:**
Open `TIMELINE.md` and work through the *Getting Started — Repo Setup* checklist.
It walks you through filling in `CLAUDE.md`, renaming the template folders to your
project names, registering your first papers, and building your first LaTeX draft.

**Ongoing — AI prompts:**
The `prompt/` folder contains reusable prompt templates. Invoke them by ID in a
Claude Code session:

| ID | Purpose |
|----|---------|
| `c000` | Write a Markdown reading review for a paper |
| `c001` | Read a proof from literature and write a proof sketch |
| `c002` | Split a monolithic LaTeX file into modular sections |
| `c003` | Register a new paper (downloads arXiv PDF + TeX source automatically) |
| `c004` | Write a full LaTeX reading review with TikZ dependency graph |
| `c005` | Abstract and introduction style checklist |
| `c006` | Proof and mathematical writing checklist |
| `c007` | Commit message checklist |
| `c008` | Experiment structure guideline (stable kernel + frozen campaigns + immutable runs) |
| `c009` | Register a paper from its title alone (identify + fetch + add to `literature/`) |
| `c010` | Freeze a computational claim as a runnable verification script |
| `c011` | Measurement and control checklist (falsifiable controls, pre-fixed criteria, noise floors, recorded obstructions) |
| `c012` | Attempt tree: judged record of what was tried, with verdicts and registered obstructions |

Example: *"perform c003 on arXiv:2301.12345"*, *"perform c009 on 'Attention Is All You Need'"*, or *"perform c000 on b00005"*.

**Writing projects:**
- `w00001_project_name/` — paper template (article class; swap for IEEEtran or similar)
- `w00002_report_template/` — survey/report template with clickable `\papercoderef`
  and `\personcoderef` cross-references and a TikZ citation graph placeholder
- `w00003_sample_note/` — a small worked note that actually builds

**Build:**
```bash
cd writing/w00001_project_name
python3 build.py
```

## Worked samples (end-to-end)

The repo ships a runnable example that threads all four areas together, so a new
user can see the intended pipeline before filling in their own project:

1. **Experiment** — `experiments/e00001_damped_oscillator` runs three campaigns
   (`bash scripts/exps/AA.sh` …) from one stable `src/` kernel, writing immutable
   `runs/` outputs. Follows `prompt/c008`.
2. **Figure → paper** — the flagship figure is copied from `runs/latest/` into
   `writing/w00003_sample_note/figures/` (the single traceable bridge).
3. **Writing** — `w00003_sample_note` builds to a 2-page PDF citing one reference
   (`b00002` in `bibliography.jsonl`).
4. **Feedback loop** — `feedbacks/f0001_*` and `drafts/d0001_*` show the advisor
   feedback and email formats, tied to the same note.

## Notes

- `bibliography.jsonl` uses `b00001`-style IDs. See `literature/README.md` for the
  full field schema and the arXiv TeX source convention.
- Experiment `runs/` folders are gitignored (never commit run outputs). A paper
  figure enters a manuscript only by an explicit copy into
  `writing/<project>/figures/`.
- `CLAUDE.md` is read by Claude Code at the start of every session — keep it current.
