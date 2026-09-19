#!/usr/bin/env python3
"""Does a number describing a list match the list?

The defect this exists for produced five instances in two windows, and every single one was found
by a person reading prose rather than by any checker:

    "Seven more, kept here for room"          over eleven items
    "those three tasks"                       against an appendix saying two
    "Five registered predictions failed"      over six
    "a target with two sharp jumps"           over five
    "fifteen more"                            over sixteen, an hour after the same sentence
                                              had been fixed for the same reason

None is a wrong measurement. Every number was true of something; what was false was the list it
claimed to count. Numerical checkers cannot see this class, because the number is not the error.

    python3 tools/countcheck.py writing/w00001_your_project/main.tex

It finds cardinals in the prose ("three", "seven of the nine", "all four") and pairs each with the
list nearest it, then prints both for you to read. It does not decide; it puts the two things on
one screen, which is all the defect ever needed.
"""
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path

WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "twenty-one": 21, "thirty": 30,
}
CARDINAL = re.compile(r"\b(" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")\b", re.I)
# A plural noun within two words of the cardinal. Deliberately loose: this half is a suspects
# list, and the two-word gap is there because "two sharp jumps" and "five registered predictions"
# are both instances this tool exists for.
PLURAL = re.compile(
    r"\b(" + "|".join(sorted(WORDS, key=len, reverse=True)) + r")\s+"
    r"((?:[a-z-]{3,}\s+){0,2}[a-z]{4,}s)\b", re.I)

# Ordinals, so a caption that says "three ladders and a fourth that runs the other way" is not
# reported as disagreeing with its four rows. A caption which names the extra has accounted for it.
ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
            "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10}
ORDINAL = re.compile(r"\b(" + "|".join(ORDINALS) + r")\b", re.I)


def strip_comments(t):
    return re.sub(r"(?<!\\)%.*", "", t)


def blocks(t, env):
    """(start_index, body) for every environment of this kind."""
    out, i = [], 0
    b, e = f"\\begin{{{env}}}", f"\\end{{{env}}}"
    while True:
        s = t.find(b, i)
        if s < 0:
            return out
        f = t.find(e, s)
        if f < 0:
            return out
        out.append((s, t[s + len(b):f]))
        i = f + len(e)


def lead_sentence(t, start, back=420):
    """The prose just before an environment, where the count that describes it is written."""
    seg = t[max(0, start - back):start]
    seg = re.split(r"\\(?:begin|end)\{[^}]*\}", seg)[-1]
    return " ".join(seg.split())


def item_count(body):
    """`\\item`s at this level, not inside a nested list."""
    depth, n = 0, 0
    for tok in re.finditer(r"\\begin\{(itemize|enumerate)\}|\\end\{(itemize|enumerate)\}|\\item\b", body):
        s = tok.group(0)
        if s.startswith("\\begin"):
            depth += 1
        elif s.startswith("\\end"):
            depth -= 1
        elif depth == 0:
            n += 1
    return n


def row_count(body):
    """Body rows of a tabular: `\\\\` outside the header, ignoring rules."""
    body = re.sub(r"\\(?:top|mid|bottom|cmid)rule(\[[^\]]*\])?(\{[^}]*\})?", "\x00", body)
    parts = [p for p in body.split("\x00")]
    if len(parts) >= 3:                      # header | body | after
        body = "\x00".join(parts[1:-1])
    return len([r for r in body.split(r"\\") if r.strip() and "\x00" not in r])


def main():
    tex = _expand(sys.argv[1])
    t = strip_comments(tex)
    hard, soft = [], []

    for env in ("itemize", "enumerate"):
        for start, body in blocks(t, env):
            n = item_count(body)
            lead = lead_sentence(t, start)
            for m in CARDINAL.finditer(lead):
                v = WORDS[m.group(1).lower()]
                # Only a cardinal in the last clause plausibly describes the list.
                if len(lead) - m.end() > 160:
                    continue
                if v != n:
                    hard.append((f"{env} with {n} items", f"...{lead[max(0,m.start()-70):][:150]}",
                                 f"says {m.group(1)} ({v}), counted {n}"))

    for start, body in blocks(t, "tabular"):
        n = row_count(body)
        lead = lead_sentence(t, start, back=600)
        caps = re.findall(r"\\caption\{(.{0,300})", lead)
        if not caps:
            continue
        cap = caps[-1]
        # A caption that names an ordinal reaching the row count has accounted for the extra rows.
        if any(ORDINALS[o.lower()] == n for o in ORDINAL.findall(cap)):
            continue
        if any(WORDS[c.lower()] == n for c in CARDINAL.findall(cap)):
            continue
        for m in CARDINAL.finditer(cap):
            v = WORDS[m.group(1).lower()]
            if 2 <= v <= 20 and 2 <= n <= 20:
                hard.append((f"tabular with {n} body rows",
                             f"...{cap[:150]}", f"caption says {m.group(1)} ({v}), counted {n}"))
                break

    prose = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", " ", t, flags=re.S)
    for m in PLURAL.finditer(prose):
        line = prose[:m.start()].count("\n") + 1
        ctx = " ".join(prose[max(0, m.start() - 60):m.end() + 60].split())
        soft.append((line, m.group(1).lower(), m.group(2), ctx))

    print(f"HARD  count disagrees with the list it introduces : {len(hard)}")
    for what, ctx, verdict in hard:
        print(f"        {what}: {verdict}")
        print(f"          {ctx}")
    print(f"suspects  a cardinal followed by a plural noun    : {len(soft)}"
          f"   (not decidable here; --suspects to list)")
    if "--suspects" in sys.argv:
        for line, num, noun, ctx in soft:
            print(f"        L{line:<5} {num} {noun}")
            print(f"          {ctx[:150]}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
