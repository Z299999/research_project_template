# Process log

What the process did, and what it got wrong. Kept apart from `TIMELINE.md`, which records what
the research found. Merging them buries the second kind, and the second kind is the one that
improves how you work.

`tools/commit.py` refuses a sixth work unit until a lookback appears here under a heading of the
form `## Lookback at \`#N\``. Run `python3 tools/lookback.py` and answer its four questions in
writing. In writing matters: an answer thought and not typed is indistinguishable from one
skipped.

Each lookback is worth ending with one sentence naming what the stretch taught you. Those
sentences accumulate into the most useful document the project will produce about itself.

---

## Lookback at `#5`

The first real one in this repository, and it exists because `commit.py` refused the sixth unit
until it did. That refusal is the whole mechanism; read it as a demonstration.

**1. What did they claim?**

- `#1` The cadence is three programs, not three good intentions.
- `#2` The citation layer, and the denominator nobody prints.
- `#3` Point at the tools, and say why they are not a checklist.
- `#4` One source, two PDFs, additions red and deletions struck.
- `#5` A red page proves nothing about what is not on it.

**2. Is each still true?**

Yes, and two were tested against this repository's own contents rather than asserted. `#2`'s
citecheck found that the sample note's bibliography entry was metadata-only with nothing recording
what it had been checked against, which is now filled from Open Library; and that reading only
`main.tex` reported zero citations for a note that cites a textbook in `sections/01_model/`. `#5`'s
markupcheck was run against a forged edit in that same note and named it: eleven words of the base
gone with no strikeout.

**3. What was deferred?**

Two items in `TODO.md`. The claim-integrity layer is named in `tools/README.md` and deliberately
not shipped; it belongs here when a project in this repository has a document under review.

**4. The finding worth keeping.**

Every tool added in these five units was first a rule someone wrote down and then stopped
following. That is not a coincidence, it is the selection criterion: a practice that survives on
discipline does not need a program, and a practice that needs a program is one that has already
failed on discipline at least once. When deciding whether something here should become code, the
question is not "is this important" but "has this been written down before and ignored".

**What the next five are for.** Nothing yet. Fill this in before spending them, which is what
question 4 is for.

---

## Lookback at `#10`

**1. What did they claim?**

- `#6` A practice needing a program has already failed once.
- `#7` A red page proves nothing about what is not on it.
- `#8` The revision layer documented, and a defect in `commit.py` recorded not fixed.
- `#9` Both builds of the worked note, so the convention ships runnable.
- `#10` The claim layer, for defects that are not in the numbers.

**2. Is each still true?**

Yes. `#10` was tested against this repository's own sample note rather than asserted, and the
testing paid: `appendices.py` fell back to the whole document when there was no `\appendix`
marker and counted a main-text section as an appendix, silently. A tool in a directory built to
catch plausible wrong answers was producing one. It now refuses and says why.

**3. What was deferred?**

`t01` still describes the example item nobody has replaced. `t02`, `commit.py` losing a parked
message, has now cost three messages across two repositories and is still open by choice.

**4. The finding worth keeping.**

Every tool in `#10` exists for the same blind spot, and naming it is worth more than the six
programs: **a number can be correct and its sentence false, and every checker reads numbers.**
The count resolves, the interval reproduces, the quote is verbatim, and the claim around them is
still wrong, because what failed was the word "every", or the list the count claimed to describe,
or the fact that the correction landed in one of the two places the claim lives.

That is why this layer arrives last and cannot arrive first. Until the numbers are trustworthy
there is nothing to notice the discrepancy against; the sentence and the measurement have to
disagree before anyone can see which one is lying.

**What the next five are for.** The experiment layer, if the reconstruction now under way shows
one worth shipping. Nothing else is planned, which is the honest answer.

## Lookback at `#15`

**1. What did they claim?**

- `#11` A number can be correct and its sentence false.
- `#12` The claim layer, for defects that are not in the numbers.
- `#13` Four layers, and why the last one cannot come first.
- `#14` What a repository claims about itself that is no longer true.
- `#15` The arc of the source project, including what it got wrong.

**2. Is each still true?**

Yes, and `#14` proved itself on this repository within a minute of being written: the writing
catalog's first entry carried an id that did not match its own folder, so the two catalogs here
were using different conventions and nobody had noticed. The checker was keyed on a parsed id and
reported that as six problems instead of one, which is its own small lesson about joining on the
field a file actually carries.

`#15` is the only unit here that is not a tool, and it exists because the tools without it teach
the wrong thing.

**3. What was deferred?**

`t01`, the example item nobody has replaced. `t02`, `commit.py` losing a parked message, now four
messages across two repositories and still open by choice.

**4. The finding worth keeping.**

Distilling a working method from a real project turned up more by reconstructing what the project
did **badly** than by cataloguing what it did well. The practices worth shipping were already
half-visible in the tools. What was invisible, and what only the git history gave up, was the
shape of the failures: fifteen experiments stopping with no ending in a project that demonstrably
knew how to write one, a status field filled from a folder's existence, a front door that lied
for three months, and a pre-registration discipline that arrived *after* the paper rather than
before it.

A project's own account of itself is written from what its author can remember, which is the
recent part. The history is written from what happened. Where the two disagree, the disagreement
is the finding, and it is not available to anyone working from the account.

**What the next five are for.** Nothing is planned. The distillation that motivated `#1` through
`#15` is complete; further units should wait for a project here to need something.
