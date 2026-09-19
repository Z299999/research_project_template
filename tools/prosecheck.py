#!/usr/bin/env python3
"""Measure the prose, so a rewrite can be checked rather than felt.

A simulated reviewer once called a manuscript "compressed to note-form" and "hard to review", and
scored presentation 2 of 4. That is a judgement. These are the numbers under it, so that the next
draft can be compared to the last one instead of argued about.

Nothing here needs a POS tagger. Every diagnostic is a cheap proxy chosen because moving it in the
right direction is almost always an improvement:

  LENGTH        mean sentence length, and the counts over 40 and over 50 words
  DENSITY       clauses, subordination, nested parentheticals
  HEDGING       how much of the text qualifies rather than states
  REPETITION    phrases that recur often enough to be a tic

    python3 tools/prosecheck.py writing/w00001_your_project/main.tex
    python3 tools/prosecheck.py <main.tex> --compare <other.tex>

A target for any of these is worth setting once and then honoured, because the number that is
never compared to anything is decoration.
"""
import re
import sys as _sys
from pathlib import Path as _P
_sys.path.insert(0, str(_P(__file__).resolve().parent))
from texsrc import expand as _expand
import sys
from pathlib import Path

BE = r"(?:is|are|was|were|be|been|being|becomes|became)"
PARTICIPLE = r"[a-z]+(?:ed|en|wn|ne|de|lt|nt|ut|it)\b"
NOMINAL = re.compile(r"\b[a-z]{4,}(?:tion|tions|ment|ments|ance|ances|ence|ences|ity|ities|"
                     r"ness|nesses|ism|isms)\b", re.I)
PASSIVE = re.compile(rf"\b{BE}\s+(?:\w+ly\s+){{0,2}}{PARTICIPLE}", re.I)


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def scrub(tex, appendix=False):
    """Prose only, with offsets preserved so line numbers point at the real file."""
    t = tex
    if not appendix:
        i = t.find(r"\section*{Reproducibility")
        if i > 0:
            t = t[:i]
    i = t.find(r"\begin{abstract}")
    if i > 0:
        # #426: blank the preamble but KEEP its newlines. Replacing it with plain spaces deleted
        # about forty of them, and every reported line number was then forty short -- which is
        # worse than no line number, because it points confidently at the wrong sentence.
        t = re.sub(r"[^\n]", " ", t[:i]) + t[i:]
    t = re.sub(r"(?<!\\)%[^\n]*", blank, t)
    t = re.sub(r"\\begin\{(tabular|table|figure|equation|align|thebibliography)\*?\}"
               r".*?\\end\{\1\*?\}", blank, t, flags=re.S)
    t = re.sub(r"\\(?:cite[a-z]*|ref|citeauthor|label|input|includegraphics)\*?"
               r"(?:\[[^\]]*\])*\{[^}]*\}", blank, t)
    t = re.sub(r"\$[^$]*\$", lambda m: "X" + " " * (len(m.group(0)) - 1), t)
    t = re.sub(r"\\(?:section|subsection|paragraph|caption|textbf|emph|texttt|color)\s*\{", blank, t)
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", blank, t)
    t = re.sub(r"[{}~]", " ", t)
    return t


def sentences(t):
    """(line, text). The line is where the sentence's first WORD is.

    #426: reporting `m.start()` puts the line at the end of the previous sentence, which after a
    blanked table or figure can be tens of lines earlier, and then the numbers point at nothing.
    Every blank here is length-preserving, so an offset is a real offset; the only thing that was
    wrong was which offset.
    """
    out = []
    for m in re.finditer(r"[^.!?]+[.!?]", t):
        s = " ".join(m.group(0).split())
        if len(s.split()) >= 6 and re.search(r"[a-z]{4}", s):
            w = re.search(r"\w", m.group(0))
            start = m.start() + (w.start() if w else 0)
            out.append((t[:start].count("\n") + 1, s))
    return out


# #446: \textbf at the start of a paragraph is visually a heading and a skimming reader treats
# it as one, so it is counted as one here. Section 7 has no \paragraph at all and is built
# entirely out of these, which the first version of this diagnostic reported as a headingless wall.
HEAD = re.compile(r"\\(section|subsection|paragraph)\{|(?<=\n\n)\s*\{?\\color\{[a-z]+\}\s*(\\textbf)\{"
                  r"|(?<=\n\n)\s*(\\textbf)\{", re.M)


def headings(tex_raw):
    """(level, line, text) for every heading, with LaTeX stripped but nothing else.

    Read as a list these are what a reviewer takes from a skim, and a heading that claims more
    than its paragraph is the cheapest possible way to mislead one.
    """
    out = []
    for m in HEAD.finditer(tex_raw):
        i = m.end()
        depth, j = 1, i
        while j < len(tex_raw) and depth:
            if tex_raw[j] == "{":
                depth += 1
            elif tex_raw[j] == "}":
                depth -= 1
            j += 1
        body = tex_raw[i:j - 1]
        body = re.sub(r"\\color\s*\{[a-z]*\}", " ", body)
        body = re.sub(r"\\(?:textbf|emph|texttt)\s*\{", " ", body)
        body = re.sub(r"\\cite[a-z]*\*?\{([^}]*)\}", lambda c: "[" + c.group(1).split(",")[0] + "]", body)
        body = re.sub(r"\\ref\{[^}]*\}", "N", body)
        body = re.sub(r"\\[a-zA-Z]+\s*", " ", body)
        body = re.sub(r"[{}$~]", "", body)
        kind = m.group(1) or "paragraph"
        lvl = {"section": 0, "subsection": 1, "paragraph": 2}.get(kind, 2)
        out.append((lvl, tex_raw[:m.start()].count("\n") + 1, " ".join(body.split())))
    return out


def full_paragraphs(t):
    out = []
    for m in re.finditer(r"(?:\n\s*\n)((?:[^\n]*\n)+?)(?=\s*\n|\Z)", t):
        body = " ".join(m.group(1).split())
        if len(body.split()) >= 40:
            w = re.search(r"\w", m.group(1))
            start = m.start(1) + (w.start() if w else 0)
            out.append((t[:start].count("\n") + 1, body))
    return out


def paragraphs(t):
    out = []
    for m in re.finditer(r"(?:\n\s*\n)((?:[^\n]*\n)+?)(?=\s*\n|\Z)", t):
        body = " ".join(m.group(1).split())
        if len(body.split()) >= 20:
            first = re.split(r"(?<=[.!?]) ", body)[0]
            w = re.search(r"\w", m.group(1))
            start = m.start(1) + (w.start() if w else 0)
            out.append((t[:start].count("\n") + 1, first))
    return out


BARE = re.compile(
    r"(?<![a-z] )\b(?:Table|Figure|Fig|Section|Appendix|Eq|Equation)~?\s*\\ref\{[^}]*\}"
    r"\s+(?:shows|gives|reports|lists|has|is|states|contains|plots)", re.I)


def bare_refs(tex_raw):
    """Cross-references carrying no noun phrase, Mermin's Good Samaritan rule.

    "Table 3 shows" makes a skimming reader turn back; "the candidate-set ablation (Table 3)"
    does not. Only the syntactically obvious cases are caught: a float name immediately followed
    by a reporting verb.
    """
    out = []
    for m in BARE.finditer(tex_raw):
        line = tex_raw[:m.start()].count("\n") + 1
        out.append((line, " ".join(tex_raw[max(0, m.start() - 40):m.end() + 40].split())))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    worst = 8
    if "--worst" in sys.argv:
        worst = int(sys.argv[sys.argv.index("--worst") + 1])
    tex = Path(args[0]).read_text()
    t = scrub(tex, appendix="--appendix" in sys.argv)
    sents = sentences(t)
    if not sents:
        print("no prose found"); return 0

    L = [len(s.split()) for _, s in sents]
    runup = [len(re.split(r"[,;:]|--| -- ", s)[0].split()) for _, s in sents]
    commas = [s.count(",") for _, s in sents]
    closures = [s.count(";") + s.count(":") for _, s in sents]
    bare = bare_refs(tex)   # raw, not scrubbed: scrubbing removes the \ref it looks for
    words = len(re.findall(r"[A-Za-z]+", t))
    nom = len(NOMINAL.findall(t))
    pas = sum(1 for _, s in sents if PASSIVE.search(s))

    n = len(sents)
    print(f"{n} sentences, {words} words"
          f"{' (appendices included)' if '--appendix' in sys.argv else ' (main text only)'}")
    # #424: length is REPORTED, not targeted. Gopen and Swan: "Long sentences need not be
    # difficult to read; they are only difficult to write." The run-up is the target.
    print(f"  run-up before 1st break  {sum(runup)/n:5.1f} words     target < 10   <-- primary")
    print(f"  run-up over 15 words     {sum(1 for x in runup if x > 15):5d}          target < 20")
    print(f"  mean sentence            {sum(L)/n:5.1f} words     reported, not a target")
    print(f"  over 40 words            {sum(1 for x in L if x > 40):5d}          reported")
    print(f"  over 50 words            {sum(1 for x in L if x > 50):5d}          target < 3")
    print(f"  mean commas              {sum(commas)/n:5.2f}           target < 1.4")
    print(f"  mean closures (; :)      {sum(closures)/n:5.2f}           more is fine, they help")
    print(f"  bare-reference candidates{len(bare):5d}          read them, do not trust them")
    print(f"  nominalisations          {nom:5d}  ({1000*nom/max(words,1):.1f} per 1000 words)")
    print(f"  passive sentences        {pas:5d}  ({100*pas/n:.0f}%)")

    print(f"\n  the {worst} longest:")
    for l, s in sorted(sents, key=lambda x: -len(x[1].split()))[:worst]:
        print(f"    L{l:<5} {len(s.split()):3d}w  {s[:150]}")

    print(f"\n  the {worst} longest run-ups (words a reader holds before the first break):")
    for l, s in sorted(sents, key=lambda x: -len(re.split(r"[,;:]|--", x[1])[0].split()))[:worst]:
        print(f"    L{l:<5} {len(re.split(r'[,;:]|--', s)[0].split()):3d}w  {s[:150]}")

    if bare and "--refs" in sys.argv:
        print("\n  cross-references with no noun phrase attached:")
        for l, s in bare:
            print(f"    L{l:<5} {s}")

    if "--blah" in sys.argv:
        # Knuth 13: "your sentences should flow smoothly when all but the simplest formulas are
        # replaced by blah". The substitution is mechanical; reading the result is not.
        print("\n  the blah test, longest sentences with the maths replaced:")
        for l, s in sorted(sents, key=lambda x: -len(x[1].split()))[:worst]:
            print(f"    L{l:<5} {re.sub(r'\\bX\\b', 'blah', s)[:230]}")

    if "--headings" in sys.argv:
        # #446: the twenty-minute read of #445 over-read one claim, and the culprit was a bold
        # run-in heading that said more than its paragraph. Every other diagnostic here measures
        # sentences INSIDE paragraphs and scrub() deletes \paragraph{...} before counting, so the
        # part a skimming reviewer reads first was the one part never measured. Printed raw and
        # in order, the headings are the paper's skeleton and the skim's whole content.
        heads = headings(tex)
        print(f"\n  headings as a skimming reader meets them ({len(heads)}):")
        for lvl, l, h in heads:
            print(f"    {'':<{2*lvl}}L{l:<5} {h[:150]}")

    if "--topics" in sys.argv:
        # Gopen and Swan's own diagnostic, and the one they call the No. 1 problem in
        # professional writing: "We can spot one source of difficulty by looking at the topic
        # positions of the sentences: We cannot tell whose story the passage is." Read each
        # paragraph's column of sentence openings; if it does not tell one story, the paragraph
        # has no subject. This cannot be scored, only read, which is why it prints and stops.
        for pl, para in full_paragraphs(t):
            sents_in = [s for s in re.split(r"(?<=[.!?]) ", para) if len(s.split()) >= 6]
            if len(sents_in) < 2:
                continue
            print(f"\n  L{pl}")
            for s in sents_in:
                head = " ".join(s.split()[:6])
                print(f"      {head}")

    if "--openers" in sys.argv:
        paras = paragraphs(t)
        print(f"\n  paragraph openers ({len(paras)}), read as a list they should tell the story:")
        for l, first in paras:
            print(f"    L{l:<5} {first[:165]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
