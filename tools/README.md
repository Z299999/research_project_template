# tools/

Eight programs. Each one exists because something went wrong repeatedly after being written down
somewhere polite, and each one's docstring tells that story. **Read the docstring before the
code**; the code is short and the reason is the part that transfers.

    python3 tools/commit.py --help-ish     # just read the top of the file
    head -40 tools/citecheck.py

## The one idea

A rule that depends on remembering is not a rule. Every practice here was first written into a
checklist, obeyed for a while, and then quietly dropped. What made them stick was moving them
into the path you have to walk anyway: `commit.py` refuses, rather than `CLAUDE.md` reminding.

Checklists are still useful. `prompt/c000`–`c014` are checklists. The difference is that a
checklist teaches and a refusal enforces, and the two fail in opposite directions: a checklist
fails silently when you are tired, which is exactly when you need it.

## Process, the cadence

| | |
|---|---|
| `commit.py` | Commit with the rules checked before the commit exists. Refuses an over-long subject, a missing `Cycle:` trailer, an overdue lookback, and a lookback quietly carrying real edits. A refusal parks your message rather than destroying it. |
| `lookback.py` | Every fifth work unit, four questions about the previous five, answered in writing into `SPRINT.md`. This is the highest-yield habit in the whole set. |
| `todo.py` | The open-debt list in `TODO.md`, printed by `lookback.py` so that "what did we defer" is a comparison and not a recollection. |

Use them in that order and the cadence runs itself: number your units, get refused every fifth
one, answer the four questions, see your debts while you answer question three.

## Sources, the integrity layer

| | |
|---|---|
| `citecheck.py` | Every quotation must appear in the cited work's local source. Also prints the denominator: how many cited keys you hold, how many are metadata-only with a named catalogue check, how many have no record at all. That last number is the one people never look at. |
| `lit_index.py` | Is `literature/` a bijection with `bibliography.jsonl`? A library you cannot enumerate is one you will cite from memory. |
| `source.py` | What a cited work actually says, by bib key, in one call. Makes reading the source cheaper than trusting a memory of it. |
| `verify_arxiv.py` | Check arXiv ids against real titles before downloading. A wrong id does not fail, it fetches a different paper. |

## Revision, the honesty layer

| | |
|---|---|
| `writing/revision.sty` | `\add` red, `\del` struck through, a `cut` block for what a strikeout cannot cross, and the maths variants. One source; `build.py` runs a second pass with `\CLEANBUILD` so `main.pdf` shows every change and `main_clean.pdf` is what you submit. Any page limit belongs to the clean one, because struck-out text still occupies space. |
| `markupcheck.py` | Reconstructs the base by keeping every deletion and dropping every addition, and requires it to match the frozen ref in the project's `REVISION_BASE`. Catches base text deleted with no strikeout, and new text left black. |

The package is the easy half. A page full of red proves nothing about what is *not* on it, and
markup applied after the edit, from memory, drifts in exactly those two ways. The checker is what
turns "this is everything I changed" into something a build reports.

## Why this order

Process before sources, sources before claims. Each layer only becomes visible once the one
before it is running: you cannot see that your citations drift until your units are countable,
and you cannot see that a claim appears in three places until your sources are stable. In the
project this was distilled from the layers arrived in exactly that order, spread over four
months, each one built the week after a failure made it unavoidable.

Two layers are not here yet, and are worth building when you meet them rather than in advance:
**claim integrity** (the same claim stated in two places, a number that does not match the list
it describes, a universal claim nobody has counted) and **honesty** (a concession that lives only
in an appendix, an argument filed where a reviewer will not read it).
