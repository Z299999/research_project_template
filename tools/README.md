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

## Claims, the layer numerical audits are blind to

| | |
|---|---|
| `quantcheck.py` | Every universal claim, as a worklist. "No paper reports it" reached an abstract in a section reporting two. |
| `countcheck.py` | Does a cardinal match the list it introduces? Five instances in two windows, every one found by a person reading prose. |
| `dupclaim.py` | A claim stated in two places, so correcting one shows you the other. You grep the sentence you edited, it appears once, you stop. |
| `qualcheck.py` | Which concessions live only in an appendix? A caveat's value is set by where it sits. |
| `prosecheck.py` | "Compressed to note-form" as numbers, so a rewrite is checked and not felt. |
| `appendices.py` | How much of the argument has been moved out of the part a reviewer must read. |
| `absencecheck.py` | Every sentence claiming something does *not* exist. `dupclaim` finds a claim stated twice; this is the converse, and absence is the one thing a local check cannot see. |
| `settingcheck.py` | Does a caption describe the runs the table is made of? Every other checker compares a claim to its own evidence; this one compares a claim to the configuration that produced the evidence. |

The shared lesson, and it is worth more than the seven programs: **a number can be correct and
its sentence false, and every checker reads numbers.** The count resolves, the interval reproduces,
the quote is verbatim, and the claim around them is still wrong, because what failed was the word
*every*, or the list the count claimed to describe, or the fact that the correction landed in one
of the two places the claim lives.

`texsrc.py` is shared by all of them. A project split across `sections/` is one document, and a
checker handed only the root file reports clean on text it never opened.

## Four things none of these can do

Each was learned the same way, by a defect surviving every check in this directory.

**The most serious defect in a document is rarely an instance of the class you went looking for.**
A search for false novelty claims turned up an undisclosed experimental asymmetry, because
settling "is this the first time" required opening the run metadata. Nine false claims were found
by that search and the one thing it could not classify was worth more than all nine.

**A checker written by the same hand as its subject shares its assumptions, so it confirms them.**
A table was verified cell by cell against its generator and the generator against the data, and
the generator's median was `sorted(d)[n // 2]`, which is the wrong order statistic for even `n`.
Seven of fourteen cells were wrong and nothing in that loop could see it, because both sides of
every comparison used the same definition. For anything load bearing, one independent
reimplementation is worth more than three passes of the original, and it should be made by
something that has not read the original.

**A comparison between two numbers that do not share a denominator is not an arithmetic error and
no checker here sees it.** A caption saying "same setting" beside `/64` in a table titled "at 100
seeds"; a sentence comparing `/100` rates against a `/64` control. Both numbers true, the
operation between them unlicensed. What caught it was a script that *refuses to run* unless the
two files agree row by row. When a comparison matters, make the pairing a precondition the code
enforces, not a property the prose asserts.

**When a measured number will not move under repeated intervention, the intervention is not the
variable.** An overflow measure read the same figure across five successive deletions and was read
as the deletions being too small. It was a block that fits or does not; freeing half a block frees
nothing.

**Watch the ratio of rework to new work.** When the units correcting previous units outnumber the
units producing new ones, the marginal cost of writing has passed the marginal cost of checking,
and the plan should change rather than the effort.

## Why this order

Process before sources, sources before claims. Each layer only becomes visible once the one
before it is running: you cannot see that your citations drift until your units are countable,
and you cannot see that a claim appears in three places until your sources are stable. In the
project this was distilled from the layers arrived in exactly that order, spread over four
months, each one built the week after a failure made it unavoidable.

Why the claim layer cannot come first: until the numbers are trustworthy there is nothing to
notice a discrepancy against. The sentence and the measurement have to disagree before anyone can
see which one is lying. In the project this came from, every tool in that layer was built in the
week after a defect of exactly its shape reached a draft, and none of them would have been
written earlier, because earlier the defects were still in the numbers.
