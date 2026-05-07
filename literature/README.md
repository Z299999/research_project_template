# Literature Folder

This folder holds all reference papers, book chapters, and manuscript TeX sources
for the project.

## Folder Structure

```
pdf_papers/        — papers, organized by topic subfolder
  <topic>/
    b00001_<shortname>/
      <paper>.pdf
      tex_source/    — arXiv TeX source (when available)
pdf_books/         — book chapters (b-series IDs, type = "book")
tex/               — TeX source manuscripts (collaborator drafts, internal reports)
bibliography.jsonl — one JSON line per registered item
```

## bibliography.jsonl Schema

Each line is a JSON object with the following fields:

```json
{
  "id":         "b00001",
  "bib_key":    "smith2023stability",
  "type":       "paper",
  "title":      "Full paper title",
  "authors":    "Smith et al.",
  "year":       2023,
  "arxiv_id":   "2301.12345",
  "path":       "literature/pdf_papers/control/b00001_smith-2023-stability",
  "tex_source": "literature/pdf_papers/control/b00001_smith-2023-stability/tex_source"
}
```

| Field | Notes |
|-------|-------|
| `id` | Unique repo ID — always `b` prefix, zero-padded five digits |
| `bib_key` | BibTeX key used in `references.bib` files — must match exactly |
| `type` | `"paper"`, `"book"`, or `"manuscript"` |
| `arxiv_id` | arXiv ID if available (e.g. `"2301.12345"`); `null` otherwise |
| `path` | Path to the paper folder (contains the PDF) |
| `tex_source` | Path to the extracted arXiv TeX source folder; `null` if not available |

## Topic Subfolder Convention

Organize `pdf_papers/` into topic subfolders as the library grows:

```
pdf_papers/
  control/
  biology/
  ml/
  ...
```

Create a new subfolder when a second paper on a new topic is added.

## arXiv TeX Source Convention

For papers with an arXiv preprint, store **both** the PDF and the TeX source:

```
b00001_smith-2023-stability/
  smith2023stability.pdf      ← downloaded from arxiv.org/pdf/...
  tex_source/                 ← extracted from arxiv.org/e-print/...
    main.tex
    ...
```

The TeX source is searchable for exact equation numbers, theorem labels, and
proof structure — far more useful than PDF for citation and cross-referencing work.

Use prompt `c003` to register a new paper and download both files automatically:

```
perform c003 on arXiv:2301.12345
```
