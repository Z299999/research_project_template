# Split LaTeX Prompt

Use this prompt to ask an AI coding agent to modularize a large LaTeX manuscript.

```text
Please refactor this LaTeX project like this:
1) In <TARGET_DIR>, create a folder named sections.
2) Read <TARGET_DIR>/main.tex and detect all top-level \section / \section* blocks.
3) For each section, create a subfolder under sections and write its content into section.tex.
4) Create <TARGET_DIR>/template.sty containing all preamble config from main (packages/macros/theorems), excluding \documentclass and \begin{document}/\end{document}.
5) Rewrite <TARGET_DIR>/main.tex as a thin skeleton:
   - keep \documentclass
   - add \usepackage{template}
   - keep front matter (e.g., \maketitle, \tableofcontents)
   - replace inline section bodies with \input{sections/.../section.tex}
   - keep bibliography and \end{document}
6) Create <TARGET_DIR>/build.py that compiles with:
   - pdflatex -synctex=1 -interaction=nonstopmode main.tex
   - bibtex main
   - pdflatex -synctex=1 -interaction=nonstopmode main.tex
   - pdflatex -synctex=1 -interaction=nonstopmode main.tex
   Use relative paths (based on __file__) so it works after git pull on another machine.
7) Create or normalize bibliography file:
   - ensure <TARGET_DIR>/references.bib exists
   - if another bib file exists (e.g., literature.bib), copy/split entries into references.bib
   - update main.tex bibliography command to use \bibliography{references}
8) Do not alter mathematical content.
9) After edits, list all created/modified files.
```

## Notes

- Prefer safe folder names for section directories (replace spaces/special chars with `_` if needed).
- Keep all citations/labels unchanged.
- Preserve bibliography commands in `main.tex`.
- Ensure `build.py` runs from any current working directory by setting `cwd` to the script directory.
- Keep bib keys unchanged when copying/splitting into `references.bib`.
