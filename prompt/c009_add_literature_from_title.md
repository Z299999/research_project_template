# Add Literature From Title Prompt

Use this prompt when you give **only a title** (or a rough title) and want the
paper identified, fetched, and registered. It is the title-only sibling of
`c003_add_new_paper.md`: c003 assumes you already know the arXiv ID or have the
PDF on disk; c009 starts from the title and figures the rest out.

## Prompt

You are helping me add one literature item to this repository from its title
alone.

Input (fill in placeholder):
- Literature title: `{LITERATURE_TITLE}`

## Task

**Step 1: Identify the item and confirm metadata.**

Identify the paper/book from `{LITERATURE_TITLE}` and determine:
- Title (canonical), Authors (e.g., `Vaswani et al.`), Year
- Venue/journal if available
- arXiv ID if one exists
- A BibTeX key `{BIBKEY}` in `firstauthorYEARkeyword` style (e.g.,
  `vaswani2017attention`)

If the title plausibly matches **more than one** item, **stop** and report the
candidates instead of guessing. Do not invent metadata you are unsure of.

**Step 2: Choose the repository identifiers.**

- Assign the next free `b000xx` ID by scanning `literature/bibliography.jsonl`
  (monotonically increasing).
- Choose a `{SHORTNAME}` in `firstauthor-year-keyword` style (no spaces).
- Choose the `{TOPIC_SUBFOLDER}` under `literature/pdf_papers/` (e.g., `control`,
  `biology`) — reuse an existing subfolder when one fits.

**Step 3: Decide the source type and fetch.**

Pick exactly one:

- **`arxiv`** — an arXiv ID exists. Fetch the PDF and TeX source exactly as in
  `c003` Steps 1–3 (create `literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/`,
  `curl` the PDF to `{BIBKEY}.pdf`, download and extract `tex_source/`).
- **`pdf_only`** — no arXiv preprint, but a stable, legal PDF is available.
  Create the folder and save the PDF as `{BIBKEY}.pdf`; no `tex_source/`.
- **`metadata_only`** — no reliable PDF can be obtained (e.g., a textbook).
  Do **not** create a paper folder; register the metadata only and note the
  absence.

Prefer arXiv TeX source whenever available; prefer stable, legal sources.

**Step 4: Append a JSON line to `literature/bibliography.jsonl`.**

For `arxiv` (TeX source extracted successfully):
```json
{"id":"{BID}","bib_key":"{BIBKEY}","type":"paper","title":"{TITLE}","authors":"{AUTHORS}","year":{YEAR},"arxiv_id":"{ARXIV_ID}","source_type":"arxiv","path":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}","tex_source":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}/tex_source"}
```

For `pdf_only`:
```json
{"id":"{BID}","bib_key":"{BIBKEY}","type":"paper","title":"{TITLE}","authors":"{AUTHORS}","year":{YEAR},"arxiv_id":null,"source_type":"pdf_only","path":"literature/pdf_papers/{TOPIC_SUBFOLDER}/{BID}_{SHORTNAME}","tex_source":null}
```

For `metadata_only`:
```json
{"id":"{BID}","bib_key":"{BIBKEY}","type":"{book|paper}","title":"{TITLE}","authors":"{AUTHORS}","year":{YEAR},"source_type":"metadata_only","path":null,"note":"No local PDF stored; metadata only."}
```

**Step 5: Confirm.**

Report:
- The identified title/authors/year and the `source_type` chosen
- The paper folder path (or that none was created, for `metadata_only`)
- Whether PDF and TeX source were obtained, and how many `.tex` files are present
- The exact `bibliography.jsonl` line appended
- Any missing materials the user may want to supply manually

## Failure Handling

- **Ambiguous title** → stop and list the candidate items; do not pick one.
- **Uncertain metadata** → do not guess; ask or mark the uncertain field.
- **arXiv source extraction fails / yields no `.tex`** → set `tex_source` to
  `null` and report it (same rule as c003).
- **No reliable, legal PDF** → fall back to `metadata_only` and explain.

## Quality Requirements

- No spaces in folder names or the SHORTNAME.
- Keep `{BID}` unique and monotonically increasing.
- `bib_key` must match the key you would `\cite` in a writing project (and any
  per-project `references.bib`).
- Ensure each JSON line uses double quotes and has no trailing comma.
