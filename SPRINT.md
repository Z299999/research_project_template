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
