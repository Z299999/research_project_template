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
literature/       — paper library and metadata
  bibliography.jsonl  — lightweight metadata index for all registered papers
  pdf_papers/     — papers, organized by topic subfolder
  pdf_books/      — book chapters
  tex/            — TeX sources of manuscripts (collaborator drafts, arXiv sources)
experiments/      — numerical experiments and simulations (e00001, ...)
  catalog.jsonl   — registry of all experiments
  e00001_*/       — experiment template (config, run.py, scripts/, figure/, runs/)
drafts/           — email drafts and planning notes for advisor communication
feedbacks/        — advisor feedback notes and revision records
prompt/           — reusable AI prompt templates (c000–c007)
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

Example: *"perform c003 on arXiv:2301.12345"* or *"perform c000 on b00005"*.

**Writing projects:**
- `w00001_project_name/` — paper template (article class; swap for IEEEtran or similar)
- `w00002_report_template/` — survey/report template with clickable `\papercoderef`
  and `\personcoderef` cross-references and a TikZ citation graph placeholder

**Build:**
```bash
cd writing/w00001_project_name
python3 build.py
```

## Notes

- `bibliography.jsonl` uses `b00001`-style IDs. See `literature/README.md` for the
  full field schema and the arXiv TeX source convention.
- Experiment `runs/` folders are gitignored. Paper-ready figures go in `figure/`
  inside each experiment folder (tracked).
- `CLAUDE.md` is read by Claude Code at the start of every session — keep it current.
