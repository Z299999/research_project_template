# Write Reading Review Prompt

Use this prompt when you want a structured reading review for one paper in this repository.

## Prompt

You are helping me read and summarize one technical paper.

Paper ID/path:
- `{PAPER_ID_OR_PATH}`

Task:
1. Read the paper carefully.
2. Write a reading review in Markdown.
3. Save the review to:
   - `{OUTPUT_MD_PATH}`

Required output structure:

1. `# Reading Review: {paper_id}`
2. Paper metadata:
   - Title
   - Authors
   - Year
   - Optional: DOI / venue
3. Section-by-section summary:
   - Include each section title exactly (including subsections when useful)
   - For each section, write 2-5 concise sentences explaining:
     - Main goal
     - Key methods/arguments
     - Main conclusion/result from that section
4. Result-tracking list (checkbox format):
   - Theorems
   - Lemmas
   - Propositions
   - Corollaries
   - Definitions / assumptions (if important)
   For each item include:
   - Number and name (e.g., Theorem 2.1)
   - One-line purpose/meaning
   - Where it is used later (if identifiable)
5. Short overall assessment (5-10 lines):
   - Main contributions
   - Strengths
   - Limitations/assumptions
   - Relevance to age-structured PDE/control work
6. Optional follow-up notes:
   - Open questions
   - Ideas to reuse in our writing

Quality requirements:
- Be faithful to the paper (no invented claims).
- Keep math statements precise and concise.
- Use clear Markdown headings.
- Prefer short paragraphs and bullet lists.
- If any part is uncertain, explicitly mark it as uncertain.

After writing, print a short confirmation with the saved file path.
