# Read And Write Proof Sketch Prompt

Use this prompt to ask an AI coding agent to read a proof from literature and write a
rigorous proof sketch into your writing project.

```text
Please help me transfer a proof idea from literature into my writing project.

Inputs:
- Source literature file (proof to read): <SOURCE_TEX_OR_PDF_PATH>
- Target writing file (where to write): <TARGET_SECTION_TEX_PATH>
- Target theorem label/name in my note: <TARGET_THEOREM_LABEL_OR_TITLE>
- Proof style or conventions to follow: <TARGET_STYLE>
  (e.g., norm used, main functional, key intermediate objects)

Task:
1) Read the source proof and extract the key proof architecture (not every
   derivation detail).
2) Identify the variable, state, or object mapping from the source model to
   my model. State which parts transfer directly and which need adaptation.
3) In my target section, write:
   - a rigorous theorem statement in my notation;
   - a `\begin{proof}...\end{proof}` sketch that lists key steps only.
4) Organize the proof sketch with clearly labeled steps. A typical structure is:

   - Step 1: introduce or construct the main technical object
     (e.g., an energy functional, a transformed variable, a Lyapunov candidate).
   - Step 2: derive the key dynamics or estimate for that object.
   - Step 3: obtain the main decay or bound.
   - Step 4: handle any secondary case, initial interval, or boundary term.
   - Step 5: combine the component bounds and conclude the theorem estimate.

   Adjust the number and content of steps to match the actual proof structure.
   Do not force a fixed template onto a proof that naturally has a different shape.

5) Keep all math statements rigorous and paper-style:
   - no internal IDs (bXXXXX, wXXXXX) in the prose;
   - do not claim details that are not shown;
   - mark any step that is inferred rather than explicitly stated in the source
     as uncertain (e.g., "(inferred)" or a \todo comment).
6) Do NOT fully derive every inequality unless explicitly asked; the goal is a
   proof roadmap, not a complete proof.
7) Preserve existing labels and citations unless a new label is required.

Output requirements:
- Edit the target `.tex` file directly.
- Then summarize:
  - what theorem statement was added or updated,
  - what proof steps were added,
  - what mapping was used between source and target notation,
  - what remains for the user to complete.
```

## Notes

- If the source is PDF only and text extraction is limited, extract the structure
  first (theorem form, key transformed system, main estimate, combination step)
  before attempting symbolic transfer.
- Prefer faithful structure transfer over symbolic copying.
- Keep notation consistent with the target writing project.
- If a step from the source proof does not transfer cleanly to the target model,
  flag it explicitly rather than silently omitting it.
