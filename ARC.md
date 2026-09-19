# The arc of one project, including what it got wrong

This template's structure and its `tools/` were distilled from a single research project that ran
from May to September 2026 and ended in a conference submission. This file is the reconstruction
of how that actually went, taken from its git history rather than from its own account of itself.

It is here because the tools alone teach the wrong lesson. Read as a list, they suggest a project
that was disciplined from the start. It was not. Every one of them was built in the week after a
defect of its exact shape reached a draft, and the most expensive failures happened in the months
when none of them existed.

## The shape, measured

| period | commits | what happened |
|---|---|---|
| May | 98 | two course reports |
| June | 562 | **sixteen experiments in nine days**, plus eight writing projects |
| July | **0** | silence |
| August | 75 | on one day: a sprint document, a decision, and a paper project |
| September | 658 | the paper |

## Act I: sixteen experiments in nine days

Experiments `e001` to `e016` were all first committed between 9 and 18 June. Most lived about a
week. Then fifteen of them stopped.

**The finding is that not one of those fifteen has a written ending.** The project knew how: it
had recorded a supersession in June (`"status": "superseded"`, plus a matching row in the
human-readable catalog), and had retired a sub-line inside one experiment with a dated note and a
pointer to its successor. It wrote a proper death certificate for a later experiment, five times
over, in five places. The habit existed and worked. It was simply not applied to the fifteen.

What the record shows instead, to the minute:

```
11:08   e014/e015: gitignore runs/ + caches (stop dangling run artifacts)   <- last commit ever
11:09   w002/note: add attempts.md selector ledger + README pointer          <- results filed
11:09   e016: new general-NN testbed for NTK-guided subset selection         <- successor born
```

Sixty seconds. A handover in behaviour with no handover in words. The ledger filed in the middle
of it ends by naming two next steps for the experiments that were about to be abandoned, and
neither was ever done.

**How the surviving experiment was chosen: by momentum.** There is no decision record. The
project named this mechanism itself, two months later and about a different choice, in the commit
that restarted it:

> "Writing the options down is the point: without this the answer defaults to whichever option is
> furthest along."

In June nobody wrote that sentence, so the default operated unexamined.

**And the catalog made it permanent.** Three of the dead experiments were not in the machine-
readable catalog at all while alive. They were added ten weeks after their last commit, by a
completeness check that found folders missing and filled the status field from the folder's
existence, because nothing else was available to fill it from. All three were entered as
`"active"`. They are still `"active"`. `tools/stale.py` exists for this.

> **Transfer.** Write the options down before choosing, or the answer defaults to whichever is
> furthest along. Close what you stop, in the same commit that starts its successor. A status
> field filled from a folder's existence is not a status. `tools/todo.py`'s rule that closed
> lines are never deleted is the same idea: an ending that is recorded is evidence, and one that
> is inferred is not.

## Act II: the silence

Sixty-one days, no commits. The last June commit is a LaTeX float-placement fix; the project stops
mid-typesetting, not at a milestone. Nothing anywhere plans for the gap, and nothing on return
refers to it. There is no re-orientation commit, no "where we left off".

The gap is invisible in the project's own record, and it has a cost that surfaced three months
later. In September the project wrote a disclosure of how it had worked, and got its own origin
wrong. Its lookback says why:

> "written from what was in my head that week, which was two weeks of experiments, and not from
> the June record where the programme starts."

Meanwhile the front-door README still said the repository was paused and the main line of work was
"hook only, not started" — three months and three hundred and fifty commits into that line of
work. The first file any reader opens told them the opposite of the truth, for months, because
nobody re-reads their own front door.

> **Transfer.** A project's self-narrative collapses to the period you can remember. Write the
> re-entry down: what state the work was in, what you were about to do, what you now think it is
> for. And run something that checks the front door against the repository, because you will not.

## Act III: the day the process arrived

On one day at the end of August the project created, in this order: a sprint document with a
clock read from the venue's own page rather than estimated; a three-way decision recorded as
**open**; a unit discipline where one unit is one commit whose subject states what was *learned*;
a five-unit lookback ladder; and a rule that a lookback may not add process, only cut, merge,
retire or record a debt. Then a paper project, a page budget decided before any text moved, and
three checkers.

Two things about that day are worth carrying.

**The first checker it built immediately found something worse than the thing it was built for.**
A catalog check written to stop one omission from recurring found, on its first run, that the
experiment every number in the paper came from had never been registered at all. Its commit says:

> "Registering the one I noticed rather than building the check is why this went five more units."

**The convention it imported broke the same day and was measured rather than defended.** The unit
numbering was audited within forty commits: 34 of 40 used a prefix the repository's own checklist
did not define, and all 40 exceeded its length rule, median 152 characters against the repo's
median of 85. `git log --oneline` had become unreadable. The scheme was changed.

> **Transfer.** When you notice one instance, build the check instead of fixing the instance.
> And measure a convention against the log a month in, because a convention nobody can read is
> not a convention.

## Act IV: the paper, and the inversion

The paper project and the pre-registration apparatus arrived together, and this is the fact that
most contradicts the tidy version of the story:

**Thirty-six of the project's thirty-seven experiment design notes were created on or after the
day the paper file was created.** The pre-registration discipline is not what produced the paper.
It is what the paper produced. Writing something that had to survive a stranger's reading is what
made the project start freezing its predictions before it ran anything.

From there the sequence in `tools/README.md` is the real one, and it is an order, not a menu:
process, then sources, then claims, then honesty. Each layer only becomes visible once the one
before it runs. You cannot see that your citations drift until your units are countable, and you
cannot see that a claim appears in three places until your sources are stable.

> **Transfer.** If you are not yet writing for a reader outside the project, you will not
> pre-register, and no checklist will make you. Get something in front of a stranger early; the
> discipline follows the audience, not the intention.

## What this template does with all that

It ships the instruments. It cannot ship the four months, and the instruments will look like
overhead until you have paid for one of them yourself.

So the honest advice is: take `commit.py`, `lookback.py` and `todo.py` on day one, because the
cadence costs almost nothing and everything else grows out of it. Take the rest when a defect of
its shape has cost you something. A practice that survives on discipline does not need a program;
a practice that needs a program is one that has already failed on discipline at least once, and
until it has, you will not follow it anyway.
