#!/usr/bin/env python3
"""Check that what a document says a citation says, that citation actually says.

Why this exists
---------------
In the project this template came from, every other instrument checked a number, a page count or
a process. Nothing checked a CITATION, and in one stretch four defects of exactly that shape got
through four look-backs: a foundational paper absent from a bibliography that claimed novelty in
its area; a related-work paraphrase whose "notes that" attributed its argument to nobody; an
opening quotation credited to the paper that restates a rule rather than the one that introduced
it; and a wording that let a classical inequality read as new.

Two of those are mechanically catchable, and this catches them.

  1. QUOTES. Every quoted string near a cite must appear in that work's local source, if the
     repository holds it. Normalised on whitespace, LaTeX escapes and typographic ligatures. A
     quote that cannot be found is either a misquote or attributed to the wrong paper, and both
     are worth failing on.
  2. FLOATING ATTRIBUTIONS. A sentence with an attributive verb (states, notes, reports, shows,
     proposes, ...) and no citation is asserting what somebody said without saying who. Your own
     claims are exempt, detected by "we", "our", "this paper" or a cross-reference.

The denominator, which is the part people skip
----------------------------------------------
This tool once printed "51 quotes verified, 0 failures" while nine of the document's eighty-six
cited references had no record of any kind in the repository. It was built to ask whether a quote
is in a PDF, and it answered exactly that. Nobody had looked at the references cited for
background and never quoted, which is precisely where a fabricated citation would sit: no quote
to check, no reason to open the file, nobody looking.

"0 failures" reads as nothing is wrong and means nothing is wrong with the things I looked at. So
this prints a denominator: how many cited keys have a source held locally, how many are
metadata-only with the catalogue they were checked against named, and how many have no record at
all. That last count is a FAIL. Read every green line in any tool as a fraction until its
denominator is printed.

For a work you cite but do not hold, add a metadata-only entry to bibliography.jsonl with a
`verified_against` field naming what you checked it against: a DOI through Crossref, an OpenAlex
or Open Library record, a publisher's own proceedings page. The audit then lives on disk rather
than in somebody's memory of having once looked. literature/bibliography.jsonl ships one worked
example.

What it cannot do
-----------------
It cannot check that a paraphrase is faithful, or that a missing citation is missing. Those stay
human. What it removes is the class where the source is on disk and nobody looked.

    python3 tools/citecheck.py writing/w00001_your_project/main.tex
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "literature" / "bibliography.jsonl"

ATTRIB = (r"\b(states?|stated|notes?|noted|reports?|reported|shows?|showed|finds?|found|"
          r"argues?|argued|proposes?|proposed|proves?|proved|observes?|observed|writes?|wrote|"
          r"calls?|called|claims?|claimed)\b")
MINE = re.compile(r"\b(we|our|ours|this paper|here)\b", re.I)


# pdftotext returns typographic ligatures as single code points, so a source that sets
# "trade-off" with an ff ligature normalises to "trade o" while our LaTeX normalises to
# "trade off", and a verbatim quote fails. Two quotes failed on this in one cycle.
LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl",
             "\ufb05": "st", "\ufb06": "st", "\u2019": "'", "\u2018": "'",
             "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-"}


def norm(t):
    for a, b in LIGATURES.items():
        t = t.replace(a, b)
    t = re.sub(r"\\[a-zA-Z]+\s*", " ", t)
    t = re.sub(r"[{}$\\~]", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t.lower())
    return t.strip()


def longest_plain(q):
    """The longest run of the quote containing no maths.

    A quote can have an equation in the middle ("around $4\\times$ as large as the selected
    budget"), and `sentences` replaces maths with MATH before quotes are read, so neither the
    whole string nor its first words will match a source that writes 4x. Comparing the
    longest maths-free run keeps the check honest without making it credulous: a run of five or
    more words is still specific enough that a misquote fails it."""
    # Split on the token, not on " math " with spaces either side. A quote ENDING in
    # maths ("a set of randomly sampled locations $\\mathcal{S}$") normalises to "... locations
    # math", which the literal split left whole, so the tool failed a quote that is verbatim
    # correct in its source.
    runs = [r.strip() for r in re.split(r"\bmath\b", norm(q))]
    runs = [r for r in runs if len(r.split()) >= 5]
    return max(runs, key=len) if runs else "\x00"


def elided_runs(q):
    """Fragments of a quote that elides text with \\dots or an ellipsis.

    A quote written as "the sum in the denominator ... to be over a random subset" is
    verbatim on both sides of the gap, but neither `norm` nor `longest_plain` can match it,
    because the source has words where the quote has nothing. `norm` eats `\\dots` before we
    ever see it, so the split happens on the raw string. Every fragment of five or more words
    must be present for the quote to pass, which is stricter than checking the longest one.
    """
    if not re.search(r"\\dots|\\ldots|\u2026|\.\.\.", q):
        return []
    parts = [norm(r).strip() for r in re.split(r"\\l?dots\s*\\?|\u2026|\.\.\.", q)]
    return [r for r in parts if len(r.split()) >= 5]


def load_bib():
    m = {}
    if BIB.exists():
        for line in BIB.open():
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = d.get("bib_key") or d.get("bibkey")
            if key and d.get("path"):
                folder = ROOT / d["path"]
                # Do not trust the index's has_tex_source flag. It reads False for entries whose
                # folder does hold a source/*.tex, which made the first run of this tool report
                # "0 quotes verified" while sitting on the very file that verifies them. Ask the
                # filesystem.
                # A PDF counts as held too. Before this, "held" meant a LaTeX source,
                # so nine of the paper's twelve quotes were reported as uncheckable while their
                # PDFs sat on disk, and a cold read found two misdescriptions among
                # exactly those. pdftotext is already a dependency of pagecheck.
                m[key] = (folder, any(folder.rglob("*.tex")) or any(folder.rglob("*.pdf")))
    return m


def source_text(folder):
    parts = []
    for f in sorted(folder.rglob("*.tex")):
        try:
            parts.append(f.read_text(errors="ignore"))
        except OSError:
            pass
    if parts:
        return norm("\n".join(parts))
    # No LaTeX source: read the PDF. A quote that spans a line break still matches, because
    # `norm` collapses whitespace, and curly quotes and ligatures fall out of it as well.
    for f in sorted(folder.rglob("*.pdf")):
        try:
            out = subprocess.run(["pdftotext", "-q", str(f), "-"],
                                 capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if out.returncode == 0 and out.stdout.strip():
            return norm(out.stdout)
    return None


ABBREV = re.compile(r"\b(et al|e\.g|i\.e|cf|vs|Fig|Eq|Sec|App|Dr|Prof|Ref)\.$", re.I)


def sentences(tex):
    r"""Split on sentence ends, not on every period.

    The first version split on `(?<=[.!?])\s+`, which cuts "et al." and "$0.5$" in half and then
    pairs a quote with whatever citation happened to land in the fragment. That produced a report
    blaming jacot2018ntk for a quote from a 2020 NLP paper, which is exactly the kind of confident
    wrong answer this tool exists to prevent, so it is worth the extra care."""
    body = tex.split(r"\begin{document}", 1)[-1]
    body = re.sub(r"(?m)^\s*%.*$", "", body)
    body = re.sub(r"\$[^$]*\$", " MATH ", body)          # periods inside math are not sentence ends
    buf = []
    # A sentence can end at ".}" or ".''" as well as ". ": the paper wraps new passages in
    # {\color{red}...}, so a closing brace sat between the period and the space and two paragraphs
    # merged into one "sentence", which is how a 2020 NLP quote got blamed on jacot2018ntk.
    for tok in re.split(r"(?<=[.!?])[}\'\"\]]*\s+", body):
        buf.append(tok)
        joined = " ".join(buf)
        if ABBREV.search(tok.strip()):
            continue                                    # "et al." is not a sentence end
        yield " ".join(joined.split())
        buf = []
    if buf:
        yield " ".join(" ".join(buf).split())


def expand(path, seen=None):
    """Follow \\input and \\include, because this template splits a paper across section files.

    The first run of this tool against the template's own sample note reported zero citations
    while the note cites a textbook in sections/01_model/section.tex. A checker that reads only
    the root file reports clean on a document it never opened, which is the most expensive kind
    of green there is."""
    seen = seen if seen is not None else set()
    path = Path(path)
    if not path.exists() and path.suffix != ".tex":
        path = path.with_suffix(".tex")
    rp = path.resolve()
    if not path.exists() or rp in seen:
        return ""
    seen.add(rp)
    text = path.read_text(errors="ignore")
    out = []
    pos = 0
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", text):
        out.append(text[pos:m.start()])
        out.append(expand(path.parent / m.group(1), seen))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def main():
    tex = expand(sys.argv[1])
    bib = load_bib()
    quoted, floating, checked, unheld = [], [], 0, 0
    cache = {}

    for sent in sentences(tex):
        keys = re.findall(r"\\cite[tp]?\{([^}]*)\}", sent)
        keys = [k.strip() for grp in keys for k in grp.split(",")]

        for q in re.findall(r"``(.+?)''", sent) + re.findall(r'"([^"]{12,})"', sent):
            if len(norm(q).split()) < 4:
                continue
            if not keys:
                quoted.append((q, None, "quoted with no citation in the sentence"))
                continue
            hit = False
            for k in keys:
                if k not in bib:
                    continue
                folder, has_tex = bib[k]
                if not has_tex:
                    continue
                if k not in cache:
                    cache[k] = source_text(folder)
                src = cache[k]
                frags = elided_runs(q)
                if src and (norm(q) in src or longest_plain(q) in src
                            or (frags and all(f in src for f in frags))):
                    hit = True
                    break
            held = [k for k in keys if k in bib and bib[k][1]]
            # If ANY cited key in the sentence is one we do not hold, the quote may belong to it,
            # so a miss proves nothing. All four "failures" in this tool's first working run were
            # of this kind or of the prefix kind: a source writing the last word as a macro
            # (\samples for "examples"), or our own $4\times$ becoming MATH before comparison.
            # Both are the tool being wrong about a quote the paper had right.
            unheld_here = [k for k in keys if k not in bib or not bib[k][1]]
            if not held or (unheld_here and not hit):
                unheld += 1
            elif hit:
                checked += 1
            else:
                quoted.append((q, ",".join(held), "not found in the cited source"))

        if not keys and re.search(ATTRIB, sent) and not MINE.search(sent) \
                and not re.search(r"\\(ref|autoref|eqref)\{", sent) and len(sent.split()) > 8:
            floating.append(sent)

    # Keys carried in the bibliography and cited nowhere. The one defect class this tool said it
    # could not see is an ABSENT citation, and that is what killed two claims in the project this
    # came from: two works sat in the bibliography, uncited, for two hundred work units, while a
    # planning document said in writing that the paper owed them. An entry nobody cites is either
    # dead weight or an unpaid debt, and both are worth printing.
    here = Path(sys.argv[1]).parent
    bibfile = next((here / n for n in ("references.bib", "refs.bib")
                    if (here / n).exists()), here / "references.bib")
    if bibfile.exists():
        declared = re.findall(r"@\w+\{([^,]+),", bibfile.read_text())
        cited = set()
        for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", tex):
            cited.update(k.strip() for k in m.group(1).split(","))
        never = [k.strip() for k in declared if k.strip() not in cited]
        print(f"warn  in {bibfile.name}, cited nowhere{'':<7}: {len(never)}"
              f"   (dead weight, or a debt the text owes)")
        for k in never:
            print(f"        {k}")

    # The gap a reader asks about first, and the one this tool was blind to. Verifying every
    # QUOTE says nothing about a reference cited only for background, which is where a fabricated
    # citation would hide. Every cited key is checked against literature/bibliography.jsonl, so a
    # key with no record at all is printed rather than assumed. A metadata-only record is not a
    # failure: it says we hold no copy and names the catalogue the metadata was checked against.
        indexed, meta_only, unknown = set(), {}, []
        for line in BIB.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            k = d.get("bib_key") or d.get("bibkey")
            if not k:
                continue
            # source_type decides, not the presence of a path: a metadata-only entry may still
            # carry a path to the shelf it would live on. Getting this backwards counted a book
            # nobody holds as held, which is exactly the silence this block exists to break.
            if d.get("source_type") == "metadata_only" or not d.get("path"):
                meta_only[k] = d.get("verified_against", "NO RECORD OF A CHECK")
            else:
                indexed.add(k)
        for k in sorted(cited):
            if k in indexed or k in meta_only:
                continue
            unknown.append(k)
        print(f"cited, PDF or source held on disk      : {len(cited & indexed)}")
        print(f"cited, metadata-only, catalogue-checked: {len(cited & set(meta_only))}")
        for k in sorted(cited & set(meta_only)):
            print(f"        {k}: {meta_only[k]}")
        print(f"FAIL  cited, no record of any kind     : {len(unknown)}"
              f"   (no local copy and no catalogue check: verify or drop)")
        for k in unknown:
            print(f"        {k}")

    hard = [x for x in quoted if x[1]]          # a source we hold does not contain the quote
    soft = [x for x in quoted if not x[1]]      # quoted with nothing to check it against
    print(f"quotes verified against a local source : {checked}")
    print(f"quotes whose source we do not hold     : {unheld}")
    print(f"FAIL  quote absent from the cited work : {len(hard)}")
    for q, k, why in hard:
        print(f"        [{k}] {why}\n        \u201c{q[:110]}\u201d")
    print(f"warn  quoted with no citation          : {len(soft)}"
          f"   (often our own phrasing in scare quotes)")
    for q, _, _ in soft:
        print(f"        \u201c{q[:100]}\u201d")
    print(f"warn  attributive verb, no citation    : {len(floating)}")
    for s in floating:
        print(f"        {s[:140]}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
