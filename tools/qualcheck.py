#!/usr/bin/env python3
"""Which concessions live only in an appendix?

A lookback once found one defect twice. Both times a qualification already existed in the
document and the reader met the unqualified claim first. Neither was a wrong number, so no
checker could see either, and both were found by accident.

The conclusion was that a caveat's value is set by where it sits. A concession filed where the
reader reaches it after the claim it qualifies does not read as scope declared; it reads as
something the reader caught you at. That is not checkable in general. This checks the cheap half.

    python3 tools/qualcheck.py writing/w00001_your_project/main.tex

It finds hedging and conceding language, reports which of it is in the main text and which only
in appendices, and pairs a concession with the claim it qualifies where it can. Read the appendix
column: every line in it is a caveat that a reviewer will meet, if at all, only after deciding
what they think.
"""
import argparse
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path

# A lead-in concedes if it says something is absent, failed, limited or mistaken. These are the
# words the paper actually uses for that; the list was read off its own appendix headings rather
# than invented, so it matches this document's voice and not a general one.
CONCEDE = re.compile(
    r"\b(no|not|never|cannot|can't|nothing|none|fails?|failed|failure|only|without|"
    r"un\w+able|missing|absent|wrong|mistake|should have|we had not|do(?:es)? not|"
    r"did not|is not|are not|disappears?|vanishes|untested|unmeasured|open)\b", re.I)

LEADIN = re.compile(r"\\(?:paragraph|textbf)\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}")
LABEL = re.compile(r"\\label\{(app:[^}]+)\}")
HEAD = re.compile(r"\\section\{")

def strip(s):
    s = re.sub(r"\{\\color\{red\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    return re.sub(r"[{}$\\]", "", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--orphans-only", action="store_true",
                    help="only appendices the main text never cites")
    a = ap.parse_args()
    tex = _expand(a.tex)

    if "\\appendix" not in tex:
        sys.exit("no \\appendix marker; this tool needs one to split main text from appendices")
    split = tex.index("\\appendix")
    body, app = tex[:split], tex[split:]
    refs = set(LABEL.sub("", body) and re.findall(r"\\ref\{(app:[^}]+)\}", body))

    # Pair every app: label with the \section that introduces it, by position. Titles nest braces
    # and span lines, so matching the title and the label in one pattern missed five of twenty-nine
    # on the first try and then silently mis-sliced every chunk after the first miss.
    heads = [m.start() for m in HEAD.finditer(app)]
    marks = []
    for m in LABEL.finditer(app):
        before = [h for h in heads if h < m.start()]
        if not before:
            continue
        start = before[-1]
        title = app[start:m.start()]
        marks.append((start, m.group(1), strip(title)))
    marks.sort()
    if not marks:
        sys.exit("no appendix labels found after \\appendix")

    print(f"main text cites {len(refs)} of {len(marks)} appendices by label\n")
    rows = []
    for i, (start, label, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(app)
        chunk = app[start:end]
        conc = [strip(x.group(1)) for x in LEADIN.finditer(chunk)
                if CONCEDE.search(strip(x.group(1))) and len(strip(x.group(1))) > 12]
        rows.append((label, title, label in refs, conc))

    orphan = [r for r in rows if not r[2]]
    if orphan:
        print(f"{len(orphan)} appendix(es) the main text never cites:\n")
        for label, title, _, conc in orphan:
            print(f"  {label}  {title[:70]}")
            for c in conc:
                print(f"      concedes: {c[:96]}")
        print()
    if a.orphans_only:
        return 1 if orphan else 0

    cited = [r for r in rows if r[2] and r[3]]
    print(f"concessions inside appendices the main text DOES cite ({len(cited)} appendices).")
    print("Read each against the sentence that cites it: does the citing sentence say this?\n")
    for label, title, _, conc in sorted(cited, key=lambda r: -len(r[3])):
        print(f"  {label}  ({len(conc)})  {title[:64]}")
        for c in conc:
            print(f"      {c[:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
