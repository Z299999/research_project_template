#!/usr/bin/env python3
"""Every sentence claiming something does NOT exist, as a worklist .

Written the unit after a sentence of mine said the appendix it introduced was "the first time the
paper states it as a paired difference", while a table doing exactly that had been `\\input` into
another appendix for weeks. Nothing caught it. `dupclaim` finds a claim stated twice; this class
is the converse, a claim that something is stated *nowhere*, and absence is the one thing a local
check cannot see.

The pattern is not rare and it is always load bearing, because a novelty claim is what a reviewer
tests first:

    "the first time"            "does not carry"        "no method here"
    "nowhere else"              "exists nowhere"        "this paper does not"
    "never reported"            "the only"              "no paper reports"

None is decidable by a program. What a program can do is put them in front of you one at a time,
with the search that would settle each one already written out, which is the whole cost of the
defect: the grep takes ten seconds and is never run because the sentence feels true.

    python3 tools/absencecheck.py writing/w010_iclr2027/paper.tex
    python3 tools/absencecheck.py <tex> --context 2

It reads `\\input` files too, because a claim of absence is false exactly when the thing it denies
is in a file the checker did not open.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEG = re.compile(
    r"\b(the first (?:time|such|to)|for the first time|nowhere (?:else|in)|no (?:other|such|"
    r"method|paper|rule|arm|work|one) \w+|never (?:reported|stated|measured|run|shown)|"
    r"does not (?:carry|exist|appear|report|state)|exists? nowhere|the only \w+|"
    r"we are not aware|to our knowledge|has not been (?:reported|measured|stated))\b", re.I)


def expand(path, seen=None):
    seen = set() if seen is None else seen
    path = Path(path)
    if not path.suffix:
        path = path.with_suffix(".tex")
    if not path.exists() or str(path) in seen:
        return ""
    seen.add(str(path))
    text = path.read_text(errors="ignore")
    out, pos = [], 0
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", text):
        out.append(text[pos:m.start()])
        out.append(expand(path.parent / m.group(1), seen))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def sentences(text):
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    text = re.sub(r"\$[^$]*\$", " MATH ", text)
    text = re.sub(r"\s+", " ", text)
    return re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--context", type=int, default=0)
    a = ap.parse_args()

    text = expand(a.tex)
    hits = []
    for s in sentences(text):
        m = NEG.search(s)
        if m:
            hits.append((m.group(0), " ".join(s.split())))

    print(f"claims of absence or novelty : {len(hits)}")
    print("Each is a grep, not a judgement. Run the search that would settle it, in this edit.\n")
    for phrase, s in hits:
        print(f"  [{phrase}]")
        print(f"    {s[:200]}")
        # The search that settles it, spelled out, because writing it is the step that gets skipped.
        key = [w for w in re.findall(r"[a-z]{5,}", s.lower())
               if w not in {"paper", "which", "there", "these", "those", "their", "state",
                            "first", "never", "other", "where", "every", "against"}][:3]
        if key:
            print(f"    settle with:  git grep -i -n '{key[0]}'"
                  + (f"   and  git grep -i -n '{key[1]}'" if len(key) > 1 else ""))
        if a.context:
            print()
    print(f"\n{len(hits)} sentence(s). None is decidable here; the point is that you see them "
          f"one at a time.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
