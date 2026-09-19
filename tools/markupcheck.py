#!/usr/bin/env python3
"""Is the revision markup an honest diff, or only a claim to be one?

`revision.sty` shows what changed: additions red, deletions struck through, one source building
both a marked-up PDF and a clean one. That is the easy half. The hard half is that a page full of
red proves nothing about what is *not* on it.

A revision marked up by hand, after the edit, from memory, drifts in exactly two ways, and neither
is visible on the page:

  1. text vanished from the base with no strikeout, so a deletion is invisible;
  2. text is new but black, so an addition reads as if it had always been there.

Neither is dishonesty. Both are what happens when the edit comes first and the markup second. This
script exists for those two and nothing else.

The clean build keeps every addition and drops every deletion. This does the opposite, keeping
every deletion and dropping every addition, which reconstructs the document as it stood at the
frozen base. That reconstruction must equal the base word for word.

    python3 tools/markupcheck.py w00001_your_project
    python3 tools/markupcheck.py w00001_your_project --diff       # show where it differs
    python3 tools/markupcheck.py w00001_your_project --base <ref> # against another git ref

The base is a git ref, recorded in the project's REVISION_BASE file. Freeze it when you start a
revision round; move it when the round is accepted and the markup is cleared.

\\redhere colours material red without wrapping it, for a new row inside an existing display that
no \\add can enclose. This cannot tell such material from kept text, so it counts those and says
so. They are checked by eye or not at all.
"""
import argparse
import difflib
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = {"del", "delcite", "delm", "deleq"}   # was in the base: unwrap it
DROP = {"add", "addeq", "note", "edit"}      # is new: remove it entirely


def brace(s, i):
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return j
    raise ValueError(f"unbalanced brace at {i}")


def expand(path, read, seen=None):
    """Follow \\input and \\include. A project split across sections/ is one document."""
    seen = set() if seen is None else seen
    path = Path(path)
    if not path.suffix:
        path = path.with_suffix(".tex")
    key = str(path)
    text = read(path)
    if text is None or key in seen:
        return ""
    seen.add(key)
    out, pos = [], 0
    for m in re.finditer(r"\\(?:input|include)\{([^}]+)\}", text):
        out.append(text[pos:m.start()])
        out.append(expand(path.parent / m.group(1), read, seen))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def reconstruct(text):
    out = text
    for _ in range(200):
        m = re.search(r"\\(" + "|".join(sorted(KEEP | DROP)) + r")\{", out)
        if not m:
            break
        name = m.group(1)
        j = brace(out, m.end() - 1)
        body_ = out[m.end():j]
        out = out[:m.start()] + (body_ if name in KEEP else "") + out[j + 1:]
    return re.sub(r"\\begin\{cut\}|\\end\{cut\}", "", out)


def body(text):
    """From \\begin{document}, so preamble changes are not counted as prose."""
    i = text.find("\\begin{document}")
    return text[i:] if i >= 0 else text


def words(text):
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    return re.sub(r"\s+", " ", text).strip().split(" ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="a directory under writing/, e.g. w00001_your_project")
    ap.add_argument("--main", default="main.tex")
    ap.add_argument("--base", default=None)
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()

    proj = ROOT / "writing" / a.project
    if not proj.is_dir():
        sys.exit(f"no such project: {proj}")
    basefile = proj / "REVISION_BASE"
    base_ref = a.base or (basefile.read_text().split()[0] if basefile.exists() else None)
    if not base_ref:
        sys.exit(f"no revision base. Freeze one:\n"
                 f"  git rev-parse --short HEAD > {basefile.relative_to(ROOT)}")

    def on_disk(p):
        try:
            return io.open(p, encoding="utf-8").read()
        except OSError:
            return None

    def at_base(p):
        rel = Path(p).resolve().relative_to(ROOT).as_posix()
        r = subprocess.run(["git", "show", f"{base_ref}:{rel}"], cwd=ROOT,
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    cur = expand(proj / a.main, on_disk)
    old = expand(proj / a.main, at_base)
    if not old.strip():
        sys.exit(f"cannot read {a.project}/{a.main} at {base_ref}")

    rebuilt, baseline = words(body(reconstruct(cur))), words(body(old))
    used = body(cur)
    n_add = len(re.findall(r"\\(?:add|addeq)\{", used))
    n_del = len(re.findall(r"\\(?:del|delcite|delm|deleq)\{", used)) \
        + len(re.findall(r"\\begin\{cut\}", used))
    n_red = len(re.findall(r"\\redhere\b", used))

    print(f"project                      : {a.project}")
    print(f"revision base                : {base_ref}")
    print(f"marked additions             : {n_add}")
    print(f"marked deletions             : {n_del}")
    if n_red:
        print(f"\\redhere blocks, eye only    : {n_red}   (red on the page, invisible here)")

    if rebuilt == baseline:
        print(f"markup is an honest diff     : reconstruction matches the base, "
              f"{len(baseline)} words")
        return 0

    sm = difflib.SequenceMatcher(None, baseline, rebuilt, autojunk=False)
    lost = sum(i2 - i1 for t, i1, i2, _, _ in sm.get_opcodes() if t in ("delete", "replace"))
    new = sum(j2 - j1 for t, _, _, j1, j2 in sm.get_opcodes() if t in ("insert", "replace"))
    print(f"FAIL  reconstruction differs : {lost} word(s) of the base are gone with no "
          f"strikeout, {new} word(s) are new and not marked as added")
    if a.diff:
        for t, i1, i2, j1, j2 in sm.get_opcodes():
            if t == "equal":
                continue
            print(f"\n  [{t}]")
            if i2 > i1:
                print("    base    : " + " ".join(baseline[i1:i2])[:300])
            if j2 > j1:
                print("    rebuilt : " + " ".join(rebuilt[j1:j2])[:300])
    else:
        print("  run with --diff to see where")
    return 1


if __name__ == "__main__":
    sys.exit(main())
