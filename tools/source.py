#!/usr/bin/env python3
"""Show what a cited work actually says, by bib key, in one call.

A finding from a paper is not usable until the source has been read at first hand, and that costs
roughly ten minutes per finding. Most of those ten minutes are spent getting to the text: resolve
the key to a folder, find the file inside it, run pdftotext, grep, then widen the match to see the
sentence around it. This does those four steps, so that reading the source is cheaper than
trusting a recollection of it.

    python3 tools/source.py vaswani2017attention "scaled dot-product"
    python3 tools/source.py vaswani2017attention --list      # what is in the folder
    python3 tools/source.py --keys transformer               # bib keys matching a string

It prints line numbers into the pdftotext output, which is what citecheck.py also reads, so a
line number here is quotable in a note and findable again later.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import citecheck as cc  # noqa: E402


def pdftext(folder, layout=False):
    """Concatenated text of every PDF in the folder, with the file each line came from.

    `--layout` preserves column structure. Without it `pdftotext` interleaves a table's columns
    and a row's numbers arrive in an order nothing can be read off. An agent once reported a
    claim about a paper's baseline table as unverifiable for exactly that reason; with layout the
    two rows read cleanly and the claim was true. An extraction artefact that looks like
    a missing fact is worse than no check at all, so this is one flag away at all times.
    """
    out = []
    for pdf in sorted(folder.rglob("*.pdf")):
        cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        for i, line in enumerate(r.stdout.splitlines(), 1):
            out.append((pdf.name, i, line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bib_key", nargs="?")
    ap.add_argument("pattern", nargs="?")
    ap.add_argument("--context", type=int, default=1, help="lines of context either side")
    ap.add_argument("--list", action="store_true", help="list the files held for this key")
    ap.add_argument("--keys", help="list bibkeys whose name or folder matches this")
    ap.add_argument("--layout", action="store_true",
                    help="preserve columns; essential for reading a table")
    a = ap.parse_args()

    m = cc.load_bib()
    if a.keys:
        hits = [(k, v[0].name) for k, v in sorted(m.items())
                if a.keys.lower() in k.lower() or a.keys.lower() in v[0].name.lower()]
        for k, folder in hits:
            print(f"  {k:<30} {folder}")
        print(f"\n{len(hits)} of {len(m)} bibkeys match {a.keys!r}")
        return 0

    if not a.bibkey:
        ap.error("give a bibkey, or --keys to search for one")
    if a.bibkey not in m:
        near = [k for k in m if a.bibkey.lower()[:6] in k.lower()]
        sys.exit(f"no bibkey {a.bibkey!r}" + (f"; did you mean {near}?" if near else ""))
    folder, held = m[a.bibkey]
    if not held:
        sys.exit(f"{a.bibkey} resolves to {folder} but nothing readable is in it")

    if a.list or not a.pattern:
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                print(f"  {p.relative_to(folder)}  ({p.stat().st_size:,} bytes)")
        return 0

    text = pdftext(folder, a.layout)
    if not text:
        sys.exit(f"no PDF under {folder}")
    pat = re.compile(a.pattern, re.I)
    # The pattern is often a phrase the paper breaks across a line, so match on a joined window
    # as well as on single lines. A quotation that spans a line break is the single most common
    # reason a first-hand check comes back "not found" when the text is in fact there.
    joined = " ".join(l for _, _, l in text)
    hits = [i for i, (_, _, line) in enumerate(text) if pat.search(line)]
    print(f"{a.bibkey}  ->  {folder.name}\n")
    for i in hits:
        name, lineno, _ = text[i]
        lo, hi = max(0, i - a.context), min(len(text), i + a.context + 1)
        print(f"  {name} line {lineno}:")
        for j in range(lo, hi):
            mark = ">" if j == i else " "
            print(f"    {mark} {text[j][2]}")
        print()
    if not hits:
        if pat.search(joined):
            print("  NOT on any single line, but present once lines are joined: the phrase is\n"
                  "  broken across a line break. Widen the pattern or search a shorter fragment.")
        else:
            print("  no match")
    print(f"{len(hits)} line(s) matched {a.pattern!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
