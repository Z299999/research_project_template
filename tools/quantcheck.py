#!/usr/bin/env python3
"""Every universal claim in the manuscript, as a worklist.

Two defects reached an abstract in nine work units and both survived every other checker:

    "across this literature ... with NO PAPER reporting it"   -- the same section reports two
    "it fails 0 of 64 on BOTH hard tasks"                     -- it fails 1/64 and 2/64 at one rung

The second is the instructive one. A numerical audit resolved "0 of 64" without complaint, because
0/64 IS a measured cell; it is measured at two other settings. What was false was the word around
it.

**A number can be correct and its sentence false, and every checker reads numbers.** That is the
whole reason this file exists. Words like every, all, none, no, only, always, never, both, and
the first and the last convert a measurement into a quantified claim over a set nobody enumerated.

    python3 tools/quantcheck.py writing/w00001_your_project/main.tex

It cannot decide whether a universal is true. It produces the list, and the list is short enough
to check by hand, which is the point: this class is invisible until somebody is handed the
sentences one at a time.
"""
import argparse
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path

# Words that assert something about EVERY member of a set, or about the ABSENCE of any member.
# Both defects were in this list. "only" and "alone" are here because they are universals about
# the complement, which is the same claim wearing a different hat.
WORDS = (r"\b(no|none|nobody|never|nothing|nowhere|not one|every|everything|all|any|"
         r"always|both|only|alone|exactly|the first|unique|uniquely|without exception)\b")
QUANT = re.compile(WORDS, re.I)

# `#591`: a second list, for a defect the first cannot see. Twice in six cycles a word in the main
# text was stronger than the statistic under it, and both times the number was right:
#
#     "PINNACLE ... and BADGE at the same ratio"   -- presented as two rules AGREEING. One score.
#     "the V axis SATURATING, flat from 30 to 500" -- an odds ratio of 0.912, [0.502, 1.655]. Null.
#
# Neither is a wrong number. Both are a verb or a noun claiming a relation the number does not
# license. `audit_numbers` resolves the count, `pcheck` the p-value, `statcheck` the interval,
# `quantcheck` the quantifier, and nothing reads the word that says what the number MEANS.
STRENGTH = re.compile(
    r"\b(saturat\w+|agree\w*|confirm\w*|corroborat\w*|establish\w*|prove[sdn]?|proof|"
    r"demonstrat\w+|show[sn]?\b|identical|equivalent|the same (?:operator|quantity|object|score)|"
    r"dominat\w+|eliminat\w+|guarantee[sd]?|ensure[sd]?|implies|therefore|hence|so that|"
    r"because|explains?|causes?|rules? out|settle[sd]?|decides?|determines?|follows? from)\b",
    re.I)

# A universal inside a quotation belongs to the cited work and is `citecheck`'s problem, not ours.
QUOTE = re.compile(r"``[^']*''", re.S)


def strip_tex(s):
    s = re.sub(r"\{\\color\{red\}", "", s)
    s = re.sub(r"\\(?:cite[a-z]*|ref|label)\{[^}]*\}", " CITE ", s)
    s = re.sub(r"\$[^$]*\$", " MATH ", s)
    s = re.sub(r"\\(?:emph|textbf|texttt|textit)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    return re.sub(r"[{}\\]", "", s)


def sentences(text):
    """Split on sentence enders, keeping enough context that a lone clause is readable."""
    for part in re.split(r"(?<=[.!?])\s+(?=[A-Z``])", text):
        p = " ".join(part.split())
        if p:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--all", action="store_true", help="include appendices")
    ap.add_argument("--word", help="only this quantifier")
    ap.add_argument("--strength", action="store_true",
                    help="read the STRENGTH list instead: words claiming a relation, not a size")
    a = ap.parse_args()
    raw = _expand(a.tex)

    body = raw if a.all else raw[: raw.index("\\appendix")] if "\\appendix" in raw else raw
    # Length-preserving blank-out, so a quotation cannot shift what follows it. `dupclaim` and
    # `prosecheck` were each written with the shifting bug once; there is no reason for a third.
    body = QUOTE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), body)

    pattern = STRENGTH if a.strength else QUANT
    hits, counts = [], {}
    for s in sentences(strip_tex(body)):
        found = {m.group(1).lower() for m in pattern.finditer(s)}
        if a.word:
            found &= {a.word.lower()}
        if not found:
            continue
        for w in found:
            counts[w] = counts.get(w, 0) + 1
        hits.append((sorted(found), s))

    scope = "whole document" if a.all else "main text only"
    kind = "relation claims" if a.strength else "universal claims"
    print(f"{kind} in the {scope}: {len(hits)} sentence(s)\n")
    print("Read each and ask: true at every rung, on every task, for every paper?\n"
          if not a.strength else
          "Read each and ask: does the number under this word license this word?\n")
    for words, s in hits:
        print(f"  [{','.join(words)}]")
        print(f"      {s[:300]}")
    print(f"\nby word: " + ", ".join(f"{w} {n}" for w, n in sorted(counts.items(), key=lambda x: -x[1])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
