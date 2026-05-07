# Write LaTeX Reading Review Prompt

Use this prompt when you want a compile-ready LaTeX reading review for one paper or manuscript in this repository.

## Prompt

You are helping me read one technical reference and turn the reading review into a standalone LaTeX note.

Inputs:
- Paper ID/path:
  - `{PAPER_ID_OR_PATH}`
- Optional review title override:
  - `{REVIEW_TITLE_OR_AUTO}`
- Optional author name:
  - `{AUTHOR_NAME_OR_AUTO}`

Path resolution rules:
1. Resolve `{PAPER_ID_OR_PATH}` to an actual local file or folder.
   - If it is a paper ID like `b00020`, look it up in `literature/bibliography.jsonl`.
2. Derive the output directory automatically from the resolved path:
   - If the resolved path is `literature/pdf_papers/.../<paper>.pdf`, write to:
     - `<parent_folder>/tex_review/`
   - If the resolved path is `literature/pdf_books/.../<book_or_chapter>.pdf`, write to:
     - `<parent_folder>/tex_review/`
   - If the resolved path is `literature/tex/<project_folder>/`, write to:
     - `<project_folder>/tex_review/`
3. Do not ask me for an output directory.
4. Do not place the review under `writing/`.
5. Do not place the review in a repo-global review folder.

Task:
1. Read the paper carefully.
2. Extract the exact section structure and the theorem-like result structure as faithfully as possible.
3. Create a standalone LaTeX project in the derived `tex_review/` directory containing:
   - `main.tex`
   - `sections/`
   - `references.bib`
   - `build.py`
4. Compile the review with `build.py` after writing.

Required review content:
1. Paper metadata and a short abstract-style overview.
2. A TikZ dependency graph near the beginning of the document.
   - This graph is required.
   - It must emphasize:
     - assumptions;
     - major definitions if they matter structurally;
     - key lemmas;
     - main theorems;
     - prerequisite knowledge only when it directly supports a proof step.
   - Arrows should represent logical dependence or proof dependence.
   - The graph should show how one arrives at the main results, not just list statements.
   - Treat this graph as one of the most important deliverables in the review, not as decoration.
3. A section on key mathematical assumptions.
4. A section on key claims/results.
5. A section on proof-sketch architecture for the main results.
   - In the review body, do not reduce the mathematics to prose only when the original paper's key content is formula-driven.
   - In particular, include complete displayed formulas where needed in:
     - the problem formulation;
     - the main theorem statements;
     - the key transformed dynamics or structural identities, if those are central to understanding the proof.
   - The reader should be able to see the actual mathematical objects, not only a verbal paraphrase of them.
6. A section on theorem/lemma dependency tracking.
7. A section on prerequisite knowledge and imported tools used by the paper.
8. A section on section-by-section structural notes.
9. A short final section on reuse notes / open questions.

Result-tracking requirements:
- Use exact numbering for theorem-like items when available.
- For each important theorem / lemma / proposition / corollary / definition / assumption, include:
  - number and name;
  - one-line meaning;
  - what it depends on;
  - where it is used later, if identifiable.
- Distinguish clearly between:
  - paper-internal dependencies;
  - imported background tools;
  - numerical or implementation material that is not part of the proof backbone.

Proof-sketch requirements:
- Give theorem-by-theorem proof roadmaps for the main results.
- Focus on key steps only, not full derivations.
- State clearly which assumptions, lemmas, or abstract results each proof uses.
- If a dependency is inferred rather than explicitly stated in the paper, mark it as uncertain.

Dependency-graph requirements:
- Prefer a top-to-bottom DAG-style layout unless there is a strong reason not to.
- Prefer clear layers such as:
  - assumptions / imported tools;
  - structural spectral or setup results;
  - abstract detectability results;
  - paper-specific verification lemmas;
  - main theorem(s);
  - implementation / numerical consequences.
- Prefer straight or nearly straight arrows. Do not introduce bent, routed, or decorative paths unless they clearly improve readability.
- Avoid visual clutter:
  - no overlapping nodes;
  - no node text collisions;
  - no arrows running through node text;
  - no dense bundles of nearly identical edges if a simpler summary edge set can express the same logic.
- If one edge is logically true but visually redundant, omit it in favor of a clearer graph.
- Keep node text concise enough that the graph remains readable on the compiled page.
- Use the graph to summarize the main proof spine and the key side branch(es), not every minor dependency in the paper.
- The graph must be readable in the compiled PDF without zooming aggressively.

Graph review loop:
- Do not stop after writing the first TikZ version.
- Compile the LaTeX review and inspect the rendered graph on the page.
- If needed, export the relevant PDF page to an image and inspect that image.
- Revise the TikZ layout repeatedly until the graph is visually clear.
- Treat visual checking as an iterative review process, not a one-shot check.
- Expect that the graph may need multiple render-review-revise passes before it is actually acceptable.
- In particular, keep revising until:
  - there are no overlapping nodes;
  - there are no unreadable edge crossings in the main proof spine;
  - the lower part of the graph is not compressed into ambiguous overlaps;
  - the graph is satisfactory as a study aid, not merely technically compilable.
- If the graph is still crowded after reasonable cleanup, simplify the dependency set before adding more routing complexity.

Quality requirements:
- Be faithful to the paper. Do not invent claims or proof steps.
- Keep math statements precise and concise.
- When quoting the paper's mathematics in review form, preserve the essential formulas completely enough to be usable for later study.
- If the source is PDF-only, reconstruct the structure from the PDF and avoid guessing when the dependency chain is unclear.
- Prefer short LaTeX paragraphs, concise itemized lists, and explicit theorem references.
- Keep the review readable as a study document, not just a raw extraction dump.
- The final compiled PDF should be visually reviewed, not just compilation-checked.

After writing:
1. Run `build.py`.
2. Print a short confirmation containing:
   - the resolved paper path;
   - the derived `tex_review/` path;
   - the PDF output path;
   - a short note confirming that the dependency graph was rendered and visually checked;
   - any major uncertainties that were kept explicit in the review.
