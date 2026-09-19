#!/usr/bin/env python3
r"""A claim stated in two places, so that correcting one shows you the other.

The rule is: correct the number, not the clause, and after correcting a claim, grep the CLAIM and
not the sentence. It failed twice in a way that reached a submitted paper:

  a gloss on a cited work corrected in the introduction and left standing, unchanged, in an
  appendix where no cold read reached it for three weeks;

  a range of numbers corrected in the body and left in the appendix that \input's the very table
  refuting it.

Both are the same failure, and it is a failure of attention and not of care: you grep the sentence
you just edited, it appears once, and you stop. The copy you were about to leave is phrased
differently, so the grep that would find it is not the grep you thought to run.

    python3 tools/dupclaim.py writing/w00001_your_project/main.tex
    python3 tools/dupclaim.py <main.tex> --changed --staged     # only what this edit retired

The `--changed` form is the one worth wiring into a commit hook: at the moment of the fix, before
the copy can be left behind, it says so. Advisory rather than refusing, because a restated
headline is legitimate and a guard that refuses gets disabled within a week.
"""
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path

STOP = set("the a an of in to and or is are was were be been it its this that these those for on "
           "at by with as from we our not but which what when where than then so is if".split())


def sentences(tex):
    """(line, text) for prose sentences.

    Substitutions are LENGTH PRESERVING -- every removed construct becomes the same number of
    spaces -- so an offset into the scrubbed text is an offset into the original and the reported
    line number is the line a person can go and look at. The first version of this computed line
    numbers on the collapsed text and they drifted by tens of lines, which makes the report
    useless for the thing it is for.
    """
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    t = re.sub(r"(?<!\\)%[^\n]*", blank, tex)
    t = re.sub(r"\\begin\{(tabular|table|figure|equation|align)\*?\}.*?\\end\{\1\*?\}", blank,
               t, flags=re.S)
    t = re.sub(r"\\(?:cite[a-z]*|ref|citeauthor)\*?(?:\[[^\]]*\])*\{[^}]*\}", blank, t)
    t = re.sub(r"\$[^$]*\$", blank, t)
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", blank, t)
    t = re.sub(r"[{}~]", " ", t)
    out = []
    for m in re.finditer(r"[^.!?]+[.!?]", t):
        s = " ".join(m.group(0).split())
        if len(s.split()) >= 8:
            out.append((t[:m.start()].count("\n") + 1, s))
    return out


def content(s):
    return [w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 1]


def runs(words, k):
    return {tuple(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}


def norm(s):
    """TeX out, case out, punctuation to space. Phrase matching needs nothing else."""
    s = re.sub(r"\\(?:cite[a-z]*|ref|label|citep|citet)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", s)
    s = re.sub(r"\$[^$]*\$", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = re.sub(r"[^a-zA-Z0-9]+", " ", s)
    return s.lower()


def changed_phrases(path, rev="HEAD~1"):
    """Phrases the last commit deleted from `path`, longest first.

    Only `-` lines matter: a phrase still present on a `+` line was rewritten, not retired.
    """
    import subprocess
    cmd = ["git", "diff"] + ([] if rev == "--cached" else [rev]) + \
          (["--cached"] if rev == "--cached" else []) + ["--unified=0", "--", str(path)]
    d = subprocess.run(cmd, capture_output=True, text=True).stdout
    removed = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    added = " ".join(l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++"))
    added = " ".join(norm(added).split())
    out = []
    for line in removed:
        w = norm(line).split()
        # 4 words is the shortest run that carries a claim rather than a turn of phrase; 9 is
        # long enough that a genuine restatement has usually diverged by then.
        for n in range(9, 3, -1):
            for i in range(len(w) - n + 1):
                ph = " ".join(w[i:i + n])
                if ph in added:
                    continue                      # survived the edit; not retired
                if any(ph in o for o in out):
                    continue                      # already covered by a longer phrase
                out.append(ph)
    return out


def main():
    """Report sentence pairs sharing a contiguous run of content words.

    The first version compared whole-sentence shingle overlap and it does not work: a claim
    restated inside a longer compound sentence has a small Jaccard with its own copy. Measured on
    the state before `#387`, when both copies of the Wenzel gloss were identical, the two
    sentences scored 0.10, well under any threshold that would not also fire on everything.

    A shared contiguous run is the right object. The Wenzel claim is eleven consecutive content
    words appearing in two places six hundred lines apart, which no amount of dilution hides.
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    k = 6
    if "--run" in sys.argv:
        k = int(sys.argv[sys.argv.index("--run") + 1])
    gap = 25
    if "--changed" in sys.argv:
        path = Path(args[0])
        text = " ".join(norm(path.read_text()).split())
        phrases = changed_phrases(path, "--cached" if "--staged" in sys.argv else "HEAD~1")
        if not phrases:
            print("the last commit removed no phrase from this file")
            return 0
        live = [p for p in phrases if p in text]
        print(f"phrases the last commit removed: {len(phrases)}; "
              f"still present elsewhere in the file: {len(live)}\n")
        for ph in live:
            print(f"  STILL THERE  {ph}")
        if not live:
            print("  none. Every phrase the last edit retired is gone from the file.")
        return 0

    sents = sentences(Path(args[0]).read_text())
    words = [content(s) for _, s in sents]

    index = {}
    for i, w in enumerate(words):
        for r in runs(w, k):
            index.setdefault(r, set()).add(i)

    pairs = {}
    for r, where in index.items():
        if len(where) < 2:
            continue
        ws = sorted(where)
        for a in range(len(ws)):
            for b in range(a + 1, len(ws)):
                i, j = ws[a], ws[b]
                if sents[j][0] - sents[i][0] < gap:
                    continue
                key = (i, j)
                cur = pairs.get(key, (0, ()))
                if len(r) >= cur[0]:
                    pairs[key] = (len(r), r)

    # Grow each reported pair to its longest shared run, so the report shows how much is shared.
    out = []
    for (i, j), _ in pairs.items():
        best, bw = 0, ()
        for n in range(k, min(len(words[i]), len(words[j])) + 1):
            common = runs(words[i], n) & runs(words[j], n)
            if not common:
                break
            best, bw = n, sorted(common)[0]
        out.append((best, bw, sents[i], sents[j]))
    out.sort(reverse=True, key=lambda x: x[0])

    print(f"claims sharing a run of {k}+ content words, {gap}+ lines apart : {len(out)}")
    for n, w, (l1, s1), (l2, s2) in out:
        print(f"\n  {n} words shared, L{l1} and L{l2}: \"{' '.join(w)}\"")
        print(f"    L{l1}: {s1[:180]}")
        print(f"    L{l2}: {s2[:180]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
