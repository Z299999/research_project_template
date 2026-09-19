"""Read a LaTeX manuscript the way a reader meets it: as one document.

Every checker in this directory takes a path to a .tex file, and a project here is split across
`sections/`, so a checker that reads only the file it was handed reports clean on text it never
opened. That is not hypothetical: the first run of `citecheck.py` against this repository's own
sample note reported zero citations, while the note cites a textbook in
`sections/01_model/section.tex`.

A green result from a checker that read a fraction of the document is worse than no checker,
because it is trusted. So every tool that reads a manuscript imports `expand` from here.

    from texsrc import expand, body, strip_comments
"""
import re
from pathlib import Path


def expand(path, read=None, seen=None):
    """The manuscript with every \\input and \\include resolved, depth-first, once each.

    `read` maps a path to its text and returns None when there is nothing there; the default
    reads from disk. Passing a different reader is how `markupcheck.py` reads the same document
    as it stood at an earlier commit.
    """
    if read is None:
        def read(p):
            try:
                return Path(p).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                return None
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


def body(text):
    """From \\begin{document} onward, so preamble edits are not counted as prose."""
    i = text.find("\\begin{document}")
    return text[i:] if i >= 0 else text


def strip_comments(text):
    """Drop LaTeX comments, keeping an escaped \\% as the character it is."""
    out = []
    for line in text.split("\n"):
        i, n = 0, len(line)
        while i < n:
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            i += 1
        out.append(line[:i])
    return "\n".join(out)
