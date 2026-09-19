#!/usr/bin/env python3
"""Build this writing project twice: marked up, and clean.

main.pdf shows every change (additions red, deletions struck through); main_clean.pdf is the
version you submit. Both come from the same source, so they cannot drift. The second pass simply
defines \\CLEANBUILD, which revision.sty reads.

Struck-out text still occupies space, so the marked-up build runs longer than the clean one. Any
page limit belongs to main_clean.pdf.

After building, run `python3 tools/markupcheck.py <this directory>` to check that the markup is an
honest diff against the base recorded in REVISION_BASE.
"""
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MAIN_TEX = "main.tex"
AUX_BASENAME = pathlib.Path(MAIN_TEX).stem
CLEAN_BASENAME = AUX_BASENAME + "_clean"
AUX_SUFFIXES = [".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".fdb_latexmk", ".fls"]

# writing/revision.sty is shared by every project here, so put its directory on the search path
# rather than copying the package into each one.
ENV = dict(os.environ)
ENV["TEXINPUTS"] = str(ROOT.parent) + os.pathsep + ENV.get("TEXINPUTS", "") + os.pathsep


def run(cmd):
    print(">", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, env=ENV)


def run_bibtex(base):
    print(">", "bibtex", base)
    # Exit code 2 means "no citations" - benign for a template with no \\cite yet.
    result = subprocess.run(["bibtex", base], cwd=ROOT, env=ENV)
    if result.returncode not in (0, 2):
        raise subprocess.CalledProcessError(result.returncode, "bibtex")


def cleanup_aux_files(base=AUX_BASENAME):
    removed = []
    for suffix in AUX_SUFFIXES:
        path = ROOT / f"{base}{suffix}"
        if path.exists():
            path.unlink()
            removed.append(path.name)
    print("Removed auxiliary files:", ", ".join(removed) if removed else "none")


def main():
    try:
        run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", MAIN_TEX])
        run_bibtex(AUX_BASENAME)
        run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", MAIN_TEX])
        run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", MAIN_TEX])
        cleanup_aux_files()

        clean = ["pdflatex", "-interaction=nonstopmode", f"-jobname={CLEAN_BASENAME}",
                 r"\def\CLEANBUILD{}\input{" + AUX_BASENAME + "}"]
        run(clean)
        run_bibtex(CLEAN_BASENAME)
        run(clean)
        run(clean)
        cleanup_aux_files(CLEAN_BASENAME)

        print("Build succeeded:", ROOT / f"{AUX_BASENAME}.pdf", "(markup)")
        print("                ", ROOT / f"{CLEAN_BASENAME}.pdf", "(the version you submit)")
        print("Next:  python3 ../../tools/markupcheck.py", ROOT.name)
    except FileNotFoundError:
        print("Error: pdflatex/bibtex not found. Install a LaTeX distribution first.")
        return 127
    except subprocess.CalledProcessError as exc:
        print(f"Build failed with code {exc.returncode}")
        return exc.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
