# CLAUDE.md

## Project Overview

[Fill in: one paragraph describing the research project, field, and main writing goals.
Include advisor names, institution, and current active manuscript.]

Advisors: [Fill in: Professor Names, Institution]

## Repository Structure

```
writing/          LaTeX writing projects (w00001, w00002, ...)
literature/       Reference PDFs and TeX sources (b00001, b00002, ...)
  pdf_papers/     Papers, organized by topic subfolder
  pdf_books/      Book chapters
  tex/            TeX sources of manuscripts (e.g., collaborator drafts)
experiments/      Numerical experiments and simulations (e00001, ...)
drafts/           Email drafts and planning notes for advisor communication
feedbacks/        Advisor feedback notes and revision records
prompt/           Reusable prompt templates (c000, c001, ...)
TIMELINE.md       Research timeline, advisor meetings, reading log
```

## Active Writing Project

[Fill in: short project ID and topic. Update as the active project changes.]

Path: `writing/w0000X_project_name/`

**Current focus:** [Fill in: which section, theorem, or revision pass is active]

**Current structure:**
[Fill in: numbered list of section folders, e.g.:
1. Introduction (`01_introduction`)
2. Problem Setup (`02_problem_setup`)
3. Main Results (`03_main_results`)
4. Proof (`04_proof`)
5. Simulations (`05_simulations`)
6. Conclusion (`06_conclusion`)]

**Build:** `cd writing/w0000X_project_name && python3 build.py`

## Prompt Templates

Files in `prompt/` are reusable prompts invoked by ID:
- **c000** — Write a structured Markdown reading review for a paper
- **c001** — Read a proof from literature and write a proof sketch into a writing project
- **c002** — Split/modularize a large LaTeX manuscript into sections
- **c003** — Register a new paper in `literature/`, with arXiv PDF and TeX source download when available
- **c004** — Write a full LaTeX reading review with TikZ dependency graph
- **c005** — Style checklist for abstracts and introductions
- **c006** — Style checklist for theorem statements, proofs, and mathematical exposition
- **c007** — Checklist for typed commit subjects and detailed commit bodies

Usage: "perform c000 on b00006 chapter 3" means run the reading review prompt on that source.

## Key References

[Fill in: table of frequently cited papers and their repo IDs, e.g.:

| ID | BibTeX key | Notes |
|----|-----------|-------|
| b00001 | vaswani2017attention | Attention Is All You Need (example paper) |
]

## Literature Storage Convention

Papers are stored in `literature/pdf_papers/` organized by topic subfolder.

For each paper, **prefer storing the arXiv TeX source** alongside the PDF, because TeX
is directly searchable for equation numbers, theorem labels, and proof structure. PDF is
used only when no arXiv preprint exists.

When an arXiv TeX source is available, it is stored in a `tex_source/` subfolder within
the paper's folder.

Each paper has two identifiers recorded in `literature/bibliography.jsonl`:
- `id`: repo ID (e.g., `b00001`)
- `bib_key`: BibTeX key used in writing projects (e.g., `vaswani2017attention`)

**When the user refers to a paper by its bib key**, always look up the local path in
`literature/bibliography.jsonl` and read the file directly — do not fetch from the web.

## Conventions

- BibTeX keys must match between `literature/bibliography.jsonl` and per-project
  `references.bib` files
- Do not use internal IDs (b000xx, w000xx) in LaTeX prose — use proper citations
- Section folders use snake_case with numeric prefix (e.g., `03_main_results/`)
- Each section folder contains `section.tex` with `% !TeX root = ../../main.tex` header

## Workflow Preferences

- Always build and verify after LaTeX edits: `python3 build.py`
- Keep mathematical writing precise and concise; prefer short paragraphs and display
  equations
- When reorganizing sections, update both folder names and `main.tex` \input paths
- The repo may temporarily track some generated LaTeX outputs during active review
  cycles; respect the current tracked state rather than deleting or untracking files
  unless asked
- Commit meaningful source changes only; do not add unrelated caches or artifacts
  unless they are already intentionally tracked
- Use `TIMELINE.md` to track research progress, advisor feedback, and next steps
- Commit messages should always use a typed subject line; see
  `prompt/c007_commit_message_checklist.md` for the full prefix list
- When a session touches several distinct areas, split into multiple focused commits
  rather than one large bundle
- Commit messages should always include a blank line plus a detailed flat bullet-point
  body explaining what changed, why it changed, and any rebuilt artifacts or synced
  outputs

## Writing Preferences

- Keep claims precise: name the exact theorem or result; do not oversell
- When discussing literature or proofs, explicitly distinguish between:
  - facts already present in the manuscript or cited literature
  - inferences or judgments based on those facts
- For explanations to the user, [Fill in: preferred language]
- In introductions, prefer citation-only style; avoid using people's names in prose
- For proof writing, prefer concrete mathematical language over abstract wording;
  step titles should say exactly what quantity is being bounded and on which domain
- Use `aligned` chains whenever they make a proof easier to read

[Fill in: any additional domain-specific or project-specific writing conventions]
