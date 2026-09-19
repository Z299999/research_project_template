#!/usr/bin/env python3
r"""What is in the appendix, how much of it, and what kind.

Written after a manuscript reached twenty-nine appendix sections and two thousand lines behind
nine pages of main text, with nobody having counted them. The first two attempts to count were
both wrong in the same way, which is why this is a file and not a shell one-liner.

THE TRAP. Headings come in more than one shape once a document has been revised:

    \section{The selector in full}
    \section{{\color{red}The crossing under every analysis we could have chosen}}

A pattern anchored on `\section{` followed by a letter misses the second and undercounts, and
the undercount looks plausible, which is why it survives.

    python3 tools/appendices.py writing/w00001_your_project/main.tex

An appendix that nobody has counted is an appendix nobody has decided about. The number is worth
seeing next to the page limit it is not subject to, because the ratio is the real question: how
much of the argument has been moved out of the part a reviewer is required to read.
"""
import argparse
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path


def brace_span(s, i):
    """Index of the '}' closing the '{' at i, counting nesting."""
    d = 0
    for k in range(i, len(s)):
        if s[k] == "{":
            d += 1
        elif s[k] == "}":
            d -= 1
            if d == 0:
                return k
    return len(s) - 1


def inventory(tex):
    # Falling back to the whole document when there is no \appendix counted a main-text section
    # as an appendix and said nothing, which is the defect class this directory exists for.
    # Falling back to the whole document when there is no \appendix counted a main-text section
    # as an appendix and said nothing, which is the defect class this directory exists for. A tool
    # here producing a plausible wrong answer in silence is worse than one that refuses.
    if "\\appendix" not in tex:
        return None
    app = tex[tex.index("\\appendix"):]
    marks = []
    for m in re.finditer(r"\\section\{", app):
        i = m.end() - 1
        marks.append((m.start(), app[i + 1:brace_span(app, i)]))
    labs = {m.start(): m.group(1) for m in re.finditer(r"\\label\{(app:[^}]+)\}", app)}
    out = []
    for i, (s, title) in enumerate(marks):
        e = marks[i + 1][0] if i + 1 < len(marks) else len(app)
        chunk = app[s:e]
        lab = next((l for p, l in sorted(labs.items()) if s <= p < e), "?")
        out.append(dict(
            label=lab,
            title=re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", title).strip(),
            lines=chunk.count("\n"),
            table="tabular" in chunk or "\\input{tables_" in chunk,
            figure="includegraphics" in chunk,
            # An appendix that names no run and no script is either not about data or is not
            # traceable; `#531` walked this list once and fixed four of them.
            source=bool(re.search(r"runs/|log[A-Z]{2}|scripts/|\.py", chunk)),
        ))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--csv", action="store_true")
    a = ap.parse_args()
    rows = inventory(_expand(a.tex))
    if rows is None:
        print("no \\appendix marker; this tool needs one to know where the appendix starts")
        return 0
    if a.csv:
        print("label,lines,table,figure,source,title")
        for r in rows:
            print(f"{r['label']},{r['lines']},{int(r['table'])},{int(r['figure'])},"
                  f"{int(r['source'])},\"{r['title']}\"")
        return 0
    total = sum(r["lines"] for r in rows)
    print(f"{len(rows)} appendix sections, {total} lines of LaTeX\n")
    print(f"  {'lines':>6}  TFS  {'label':<20}title")
    for r in sorted(rows, key=lambda x: -x["lines"]):
        flags = ("T" if r["table"] else "-") + ("F" if r["figure"] else "-") + \
                ("S" if r["source"] else "-")
        print(f"  {r['lines']:>6}  {flags}  {r['label']:<20}{r['title'][:54]}")
    print(f"\n  with a table {sum(r['table'] for r in rows)}, "
          f"with a figure {sum(r['figure'] for r in rows)}, "
          f"naming a run or script {sum(r['source'] for r in rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
