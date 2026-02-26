# Read And Write Proof Sketch Prompt

Use this prompt to ask an AI coding agent to read a proof from literature and write a rigorous proof sketch into your note.

```text
Please help me transfer a proof idea from literature into my writing project.

Inputs:
- Source literature file (proof to read): <SOURCE_TEX_OR_PDF_PATH>
- Target writing file (where to write): <TARGET_SECTION_TEX_PATH>
- Target theorem label/name in my note: <TARGET_THEOREM_LABEL_OR_TITLE>
- Desired norm/style (e.g., L2, L-infinity): <TARGET_STYLE>

Task:
1) Read the source proof and extract the key proof architecture (not every derivation detail).
2) Identify the variable/state mapping from source model to my model.
3) State clearly which parts transfer directly and which parts need adaptation.
4) In my target section, write:
   - a rigorous theorem statement in my notation;
   - a `\begin{proof}...\end{proof}` sketch that lists key steps only.
5) In the proof sketch, organize steps in this order:
   - Step 1: rewrite controller/system into a transformed form;
   - Step 2: derive transformed closed-loop dynamics;
   - Step 3: obtain Lyapunov (or equivalent) decay for transformed states;
   - Step 4: handle startup interval `[0,\tau]`;
   - Step 5: derive delayed-history bound using `\sup_{s\in[t-\tau,t]}(\cdot)`;
   - Step 6: combine bounds and conclude final estimate.
6) Keep all math statements rigorous and paper-style:
   - no internal IDs like bib000xx/w000xx in the prose;
   - use `\sup` notation (not informal max wording) for history norms;
   - do not claim details that are not shown.
7) Do NOT fully derive every inequality unless explicitly asked; keep it as a proof roadmap.
8) Preserve existing labels/citations unless a new label is required.

Output requirements:
- Edit the target `.tex` file directly.
- Then summarize:
  - what theorem statement was added/updated,
  - what proof steps were added,
  - what remains for me to complete.
```

## Notes

- If source is PDF and text extraction is limited, still extract structure first (theorem form, transformed system, Lyapunov step, delay-window step, combination step).
- Prefer faithful structure transfer over symbolic copying.
- Keep notation consistent with the target note.
