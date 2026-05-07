# Add New Paper Prompt

Use this prompt when you want to register a new paper in the repository.
The paper may already be on disk as a PDF, or may be fetched from arXiv.

## Prompt

You are helping me register a new paper in this repository.

Inputs (fill in placeholders):
- Paper ID (unique, monotonically increasing): `{BID}` (e.g., `b00027`)
- Short name for folder: `{SHORTNAME}` (e.g., `smith-2023-stability`)
- Topic subfolder under `literature/pdf_papers/`: `{TOPIC_SUBFOLDER}` (e.g., `control`, `biology`)
- Metadata:
  - Title: `{TITLE}`
  - Authors: `{AUTHORS}` (e.g., `Smith et al.`)
  - Year: `{YEAR}`
  - BibTeX key: `{BIBKEY}` (e.g., `smith2023stability`)
- Source (choose one):
  - arXiv ID: `{ARXIV_ID_OR_EMPTY}` (e.g., `2301.12345`; leave empty if not on arXiv)
  - Existing PDF already in `literature/pdf_papers/`: `{EXISTING_PDF_FILENAME_OR_EMPTY}`

## Task

**Step 1: Create the paper folder.**

```bash
mkdir -p "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}"
```

**Step 2: Obtain the PDF.**

If `{ARXIV_ID_OR_EMPTY}` is provided:
```bash
curl -L "https://arxiv.org/pdf/{ARXIV_ID_OR_EMPTY}" \
  -o "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/{BIBKEY}.pdf"
```

If instead `{EXISTING_PDF_FILENAME_OR_EMPTY}` is provided (PDF already on disk):
```bash
mv "literature/pdf_papers/{EXISTING_PDF_FILENAME_OR_EMPTY}" \
   "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/"
```

**Step 3: Download and extract arXiv TeX source (only if arXiv ID is provided).**

```bash
mkdir -p "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/tex_source"
curl -L "https://arxiv.org/e-print/{ARXIV_ID_OR_EMPTY}" \
  -o "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/tex_source/source.tar.gz"
```

Then attempt to extract:
```bash
cd "literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/tex_source" && \
  tar xzf source.tar.gz && rm source.tar.gz
```

If the `tar` command fails (some arXiv submissions are a single `.tex` file rather than a
tarball), rename the downloaded file instead:
```bash
mv source.tar.gz main.tex
```

After extraction, verify that `.tex` files are present in the `tex_source/` folder and
report how many were found.

**Step 4: Append a new JSON line to `literature/bibliography.jsonl`.**

If arXiv TeX source was downloaded and extracted successfully:
```json
{"id":"{BID}","bib_key":"{BIBKEY}","type":"paper","title":"{TITLE}","authors":"{AUTHORS}","year":{YEAR},"arxiv_id":"{ARXIV_ID_OR_EMPTY}","path":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}","tex_source":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/tex_source"}
```

If no arXiv TeX source (or extraction failed):
```json
{"id":"{BID}","bib_key":"{BIBKEY}","type":"paper","title":"{TITLE}","authors":"{AUTHORS}","year":{YEAR},"arxiv_id":null,"path":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}","tex_source":null}
```

**Step 5: Confirm.**

Report:
- The paper folder path
- Whether the PDF was downloaded from arXiv or moved from disk
- Whether the TeX source was downloaded and extracted, and how many `.tex` files are present
- The exact bibliography.jsonl line that was appended

## Quality Requirements

- Do not use spaces in folder names or the SHORTNAME.
- Keep `{BID}` unique and monotonically increasing.
- Ensure the JSON line uses double quotes around strings and has no trailing comma.
- If arXiv source extraction fails or yields no `.tex` files, set `tex_source` to `null`
  in the JSON and report the issue clearly so the user can retry manually.
