# Research Project Template

Copy this folder to bootstrap a new research project with the same workflow as this repo.

## Folder layout

- `prompt/`: reusable AI prompts.
  - includes `write_reading_review.md`, `read_and_write_proof_sketch.md`, `split_latex.md`
- `literature/`: paper library and metadata.
  - `pdf_papers/`, `tex/`, `bibliography.jsonl`
- `writing/`: LaTeX writing projects.
  - `catalog.jsonl` for writing-project tracking
  - starter project `w00001_project_name/`
- `experiments/`: figures and experiment outputs.

## Quick start

1. Copy the folder to your new location.
2. Rename `writing/w00001_project_name` to your project ID (for example `w00007_my_topic`).
3. Update `writing/catalog.jsonl` with your new project entry.
4. Edit:
   - `writing/<your_project>/main.tex`
   - `writing/<your_project>/references.bib`
   - section files under `writing/<your_project>/sections/`
5. Build:
   - `cd writing/<your_project>`
   - `python3 build.py`
6. Add papers under `literature/pdf_papers/` and update `literature/bibliography.jsonl`.
7. Use prompts in `prompt/` to standardize reading reviews and proof-sketch writing.

## Notes

- The build script runs `pdflatex -> bibtex -> pdflatex -> pdflatex`.
- Auxiliary files are cleaned automatically after successful build.
- SyncTeX is enabled (`-synctex=1`).
- `.gitignore` in this template excludes common Python/macOS/LaTeX artifacts.
