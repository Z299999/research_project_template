# Making A Practice Survive

**When to use.** Whenever you are about to adopt a rule, a habit, a checklist
item, or a tool — and whenever you are about to write down that one of those is
*working*.

Everything below is recorded from measured incidents in one long-running
project, not predicted.

## Main Principle

**A written rule is not a practice.** The only question worth asking about any
method you adopt is what will still be running once nobody remembers adopting
it. Almost every method document answers a different question — what a careful
person *should* do — and then never measures whether anyone did.

## 1. Measure the decay curve, because it is steeper than it feels

One project required a retrieval step to be run by hand before writing any
claim. Compliance, measured in three consecutive windows of twenty units:

| window | ran the step |
|---|---|
| while it was being built and actively enforced | 7 of 20 |
| the next twenty | 1 of 20 |
| the next twenty | 0 of 20 |

**A hand-run requirement that nobody runs is worse than not having one, because
it makes the check look adequate.** The rule was retired and replaced by a
trigger that fires from a pre-commit hook, unasked.

Note the shape: adoption was never high. The window where it looked healthiest
was the window in which its author was personally watching.

## 2. What survives is what fires unasked

Same project, several years of tooling, sorted by outcome:

| survived | why |
|---|---|
| invariant checker, staleness advisory, verification runner, regression suite | run from a commit hook; nobody has to remember |
| a ranking mode used to answer a **directed question** | it is a query, not a ritual — it is reached for because there is a question |

| died | why |
|---|---|
| a required session-start retrieval | had to be remembered |
| the same tool as a pre-writing requirement | had to be remembered |
| a state file that a design document said would hold the system's state | never created; the document had one commit in a thousand |

The distinction is not *useful vs useless*. All of the dead ones were useful.
The distinction is **who has to remember**.

## 3. Retire on measurement, and treat retiring as the hard half

Systems accrete. Removing a practice feels like admitting waste, so it does not
happen, and the dead practice keeps signalling that a check exists.

Retire when a **count** says so, not when it feels stale — and record the count
in the retirement, so the next person does not restore it on a hunch. In the
project above, four practices were retired this way, each with the measurement
that killed it written beside it.

## 4. Announce a tool in the same commit that builds it

Four separate times in that project a tool was built and then referenced in no
document. A fresh session, reading only the repository, could not have
discovered any of them. Each was fixed later as a separate repair.

**If the capability is not recoverable from the files alone, it lives in a
conversation and expires with it.** The test is mechanical: *would a fresh
session, with no context, reading only these files, take the same action?*

## 5. A claim pinned to a growing artefact goes stale silently

A commit hook in that project carried the comment *"a commit touching the notes
pays about nine seconds."* Measured later: **three minutes twenty**.

The comment was written when the corpus held **eight scripts**. It held **246**
when the number was finally re-measured, some seven hundred units later. Nobody
lied and nobody was careless — the number was correct when written, and the
thing it described grew by a factor of thirty underneath it.

**Any number you write about a growing thing carries its denominator beside
it**, so that a reader who notices the denominator is stale knows the number is
too. *"about nine seconds"* teaches nothing. *"about nine seconds, over eight
scripts"* expires visibly.

## 6. Run your regression suite against old data to find the ones pinned to growth

Section 5's failure has a silent cousin in the test suite: a regression case
that passes today **because the data grew**, not because the code is correct.
Such a case looks green forever and is testing nothing.

There is a cheap experiment that separates them:

> Check out the **data** at an old commit. Drop **today's** tools on top of it.
> Run the **current** test suite.

A case whose evidence is the code passes. A case pinned to an artefact that has
since grown fails. First run in that project: **7 of 71 cases were sliding.**

One refinement is not optional. Some cases fail only because they are *younger
than the base commit* and their fixtures do not exist there — that is not
sliding. Separate the two by asking version control when each case's name first
entered the suite, and report the two groups apart. Without that split the
experiment reports a number roughly twice the real one.

## 7. Give a scheduled measurement a due date, and pay it by name

A commitment written only in prose — *"this can honestly be scored twenty units
from now"* — is not scheduled. It is a sentence.

- Write the condition **and** the unit or date it comes due, in a structured
  field a tool can read.
- Have the tool announce it when that point arrives.
- **Discharge it by naming what was paid**, not by a bare acknowledgement. In
  that project a bare payment closed every open item of the same origin,
  including a measurement that had been deliberately scheduled for later — it
  was closed by side effect and never ran.

A date is a schedule, not a condition, so it must not be dischargeable by
accident.

## Quick pass before adopting a practice

- [ ] Who has to remember this? If the answer is a person, it will decay.
- [ ] What fires it? If nothing does, it is prose — say so honestly rather than
      writing it as a rule.
- [ ] What number would tell me in three months that it stopped working?
- [ ] Is it discoverable by someone reading only the repository?
- [ ] Does every number I just wrote carry the denominator it was measured over?
