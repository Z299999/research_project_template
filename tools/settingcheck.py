#!/usr/bin/env python3
"""Does a table's caption describe the runs the table is made of?

Written after the worst defect a paper carried was found by an outside reader doing something
else. Its main table's caption said "B = 40 kept of V = N = 1,200 scored" for the whole table.
The runs' recorded argv carried `--visible 200`, the internal candidate window of two of the
eight arms, so five arms scored 1,200 candidates and two scored 200 -- on the axis the paper was
about, in the direction favouring the authors' own arms, with the caption denying it and the
setup section enumerating the exceptions and leaving it out.

Nothing caught it, and nothing could have. **Every other checker compares a claim to its own
evidence; none compares a claim to the configuration that produced the evidence.** A numerical
audit resolves a quoted count to a cell on disk without ever asking what that cell was run at.
That gap is this file.

    python3 tools/settingcheck.py writing/w00001_your_project/main.tex
    python3 tools/settingcheck.py <tex> --runs experiments/e00001_your_experiment/runs

It reads each caption for the settings it asserts, resolves the run tags named in it, and
compares against each run's recorded argv. A disagreement the caption does not mention is a FAIL;
one the caption states is a note to read. Adapt ASSERTS below to your own flags: the pairing of a
phrase in a caption with a flag in an argv is the whole mechanism.

Two things this requires of you, and both are worth doing anyway. Captions must name their runs,
or there is nothing to check. Runs must record their own argv, or there is nothing to check it
against.

A caption naming no run is not checked, and the defect this file exists for was in exactly such a
caption, so a clean run here is not a clean paper. The script says so every time.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# What a caption can assert, and where the same quantity lives in a run's argv.
ASSERTS = [
    # LaTeX writes a thousands separator as 1{,}200, so a digit class that stops at the brace
    # reads it as 1. That silently turned a real disagreement into agreement with a number the
    # caption never stated, which is the failure mode this whole file exists to prevent.
    ("B",       r"\$?B\$?\s*=\s*\$?(\d[\d,{}]*)",             "--target-n"),
    ("V",       r"\$?V\$?\s*=\s*(?:\$?N\$?\s*=\s*)?\$?(\d[\d,{}]*)", "--visible"),
    ("N",       r"\$?N\$?\s*=\s*\$?(\d[\d,{}]*)",             "--n-pool"),
    ("seeds",   r"(\d[\d,{}]*)\s+seeds",                       "--seeds"),
    ("steps",   r"(\d[\d,{}]*)\s+Adam steps",                  "--epochs"),
    ("cadence", r"re-selection every \$?(\d[\d,{}]*)",         "--exam-every"),
]


def num(s):
    return int(str(s).replace(",", "").replace("{", "").replace("}", "").strip())


def argv_of(run):
    p = ROOT / run / "latest" / "metadata.json"
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text())
    except Exception:
        return None
    a = d.get("argv")
    a = a if isinstance(a, list) else str(a).split()
    out = {}
    for i, tok in enumerate(a):
        if tok.startswith("--") and i + 1 < len(a) and not a[i + 1].startswith("--"):
            out[tok] = a[i + 1]
    return out


def captions(tex):
    """Every \\caption{...} with the run tags and generator named inside it."""
    out = []
    for m in re.finditer(r"\\caption\{", tex):
        i, d, j = m.end() - 1, 0, m.end() - 1
        while j < len(tex):
            if tex[j] == "{":
                d += 1
            elif tex[j] == "}":
                d -= 1
                if d == 0:
                    break
            j += 1
        body = tex[m.end():j]
        # A caption writes a tag as logDB\_\{task\}\_s100. Strip the LaTeX escapes first, or the
        # class stops at the first backslash and the tag is never seen, which is a checker that
        # reports "nothing to check" on the one table it was built for.
        plain = body.replace("\\_", "_").replace("\\{", "{").replace("\\}", "}")
        # One optional {..} group only. A greedy class swallows the \texttt closing braces too
        # and the tag never resolves to a directory, which reads as "no run named" and is the
        # silence this file was written to remove.
        tags = re.findall(r"(log[A-Z]{2}[A-Za-z0-9_]*(?:\{[^}]*\}[A-Za-z0-9_]*)?)", plain)
        out.append((body, tags))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--runs", default="experiments/e016_ntk_general_selection/runs")
    a = ap.parse_args()

    tex = Path(a.tex).read_text()
    caps = captions(tex)
    checked = named = fails = 0

    for body, tags in caps:
        asserted = {}
        for name, pat, _ in ASSERTS:
            m = re.search(pat, body)
            if m:
                try:
                    asserted[name] = num(m.group(1))
                except ValueError:
                    pass
        if not asserted:
            continue
        checked += 1
        # Expand a braced tag like logDB_{crenel,poisson1d}_s100 into its members.
        runs = []
        for t in tags:
            m = re.match(r"(.*?)\{([^}]*)\}(.*)", t)
            if not m:
                runs.append(t)
                continue
            inner = m.group(2)
            # A caption writes either an explicit list, logDB_{crenel,poisson1d}_s100, or a
            # placeholder, logDB_{task}_s100. Expand the first by its members and the second by
            # globbing the directory, so a placeholder checks every run it stands for rather than
            # none of them.
            if "," in inner or (ROOT / a.runs / f"{m.group(1)}{inner}{m.group(3)}").is_dir():
                runs += [f"{m.group(1)}{x.strip()}{m.group(3)}" for x in inner.split(",")]
            else:
                runs += [d.name for d in (ROOT / a.runs).glob(f"{m.group(1)}*{m.group(3)}")
                         if d.is_dir()]
        runs = [r for r in runs if (ROOT / a.runs / r).is_dir()]
        if not runs:
            print(f"warn  caption asserts {asserted} and names no run this script can find")
            continue
        named += 1
        head = body.split(".")[0][:58].replace("\n", " ")
        for r in runs:
            av = argv_of(Path(a.runs) / r)
            if av is None:
                print(f"warn  {r}: no metadata.json")
                continue
            for name, _, flag in ASSERTS:
                if name not in asserted or flag not in av:
                    continue
                got = num(av[flag])
                if got == asserted[name]:
                    continue
                # A caption may disagree on purpose and say so. The defect is an UNDISCLOSED
                # disagreement, so a caption that names the flag, or says plainly that the
                # comparison is not at equal V, is a warning to read rather than a failure.
                disclosed = (flag.lstrip("-") in body
                             or re.search(r"not (?:an |read at )?equal[- ]\$?" + name, body)
                             or re.search(r"window(?:s)? (?:internally|at)", body))
                if disclosed:
                    print(f"note  {r}: caption says {name} = {asserted[name]} and {flag} recorded "
                          f"{got}; the caption discloses a difference. Read it.")
                    continue
                fails += 1
                print(f"FAIL  {r}: caption says {name} = {asserted[name]}, "
                      f"{flag} recorded {got}")
                print(f"        \u201c{head}...\u201d")

    print(f"\ncaptions asserting a setting : {checked}")
    print(f"  of those, naming a run      : {named}"
          + ("" if named == checked else "   (the rest cannot be checked here)"))
    print(f"FAIL  caption disagrees with the run it names : {fails}")
    if not fails:
        print("  Note: a caption that names no run is not checked. The defect this file exists")
        print("  for was in exactly such a caption, so a clean run here is not a clean paper.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
