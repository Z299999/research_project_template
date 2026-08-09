# Attempt Tree Checklist

This checklist records how to keep a searchable, judged record of what a
project has *tried* — including everything that did not work.

Use it whenever starting a line of attack expected to outlast one session.
Do not use it for a calculation; use it for a **bet**.

## Main Principle

**A dead end without a verdict is lost knowledge.**

Most research effort goes into routes that fail. If failure leaves only an
absence, the next person — or the same person in three months — walks the same
route again. The tree exists so that pruning enters the vocabulary instead of
disappearing.

Second principle, equally load-bearing:

**The bet is written before the work, and the kill condition before the result.**
A kill condition invented afterwards is a rationalisation, and a node without
one runs forever.

## Layout

```
attempts/
  TREE.md            the map, plus a "routes checked and NOT opened" table
  PROBLEMS.md        the problem list, maintained and sharpened over time
  a00001_<name>/
    README.md        one paragraph: what this is, how to resume it cold
    idea.md          the bet, written once
    ATTEMPT_LOG.md   one entry per probe, in run order
    verdict.md       written at close
    notes/           scripts and scratch
```

Probe codes are **flat and meaningless** — `AA`, `AB`, `AC` in run order. Do not
encode topic or status in the code; the log says what happened.

## `idea.md` — written once, never rewritten

| Field | Requirement |
|---|---|
| **Target** | what settling this would actually establish. An attempt that cannot name its target is not an attempt |
| **Claim** | stated so a reader can later judge whether it was achieved |
| **Why it might work** | the mechanism, one paragraph. Named concepts, not vibes |
| **Expected obstruction** | which known barrier is expected to bite, and at which step. "None expected" needs a reason |
| **Kill condition** | the observation that would make this node dead. Concrete and checkable |
| **Parent** | the node this branched from, or `root` |

Amendments go in `ATTEMPT_LOG.md`, never into `idea.md`. **The value of the bet
is that it records what was believed before the outcome was known.**

**An amended claim re-derives its kill conditions.** A kill condition written
against a claim that has since changed is not a kill condition; it is a fossil.
When the claim moves, say of each killer: still live, misaimed and retired, or
replaced — and derive the replacement from the amended claim.

## Before opening: two different questions

1. **What has already stopped us?** — the registered obstructions.
2. **What have we already read?** — the literature already on the shelf.

These are not the same, and the second is the one that gets skipped. An
obstruction index knows only what has already killed you; it cannot contain the
paper that would kill the node you are about to open, because that entry does
not exist yet.

In one project a node ran ten units before being killed by a **registered
paper** that a shelf query ranked *first* on that node's own question. The
obstruction index could not have found it. Record what the shelf query returned
in `idea.md`, **including when it returned nothing** — a null result is what
stops the next person repeating the query.

## Closing: `verdict.md`

A node is not closed until `verdict.md` exists. It must judge the claim **as
written**, not the sharpened version that survived, and state:

- the verdict, the probes run, and which probe triggered it
- each kill condition, dispositioned: fired, moot, or **not dispositioned** —
  and if a live question survives the node, promote it to `PROBLEMS.md` rather
  than burying it in the verdict
- what the node bought, and **what it cost**, plainly

If the verdict is `dead`, register the obstruction as a named concept and cite
it from the verdict. That is the step that turns a failure into something the
next node can consult in one lookup.

## The Failure Mode To Expect

**This is the part a template usually omits, and it is the part that decides
whether the tree is used at all.**

Opening nodes decays. Measured in one project: **16 nodes, none of them open**,
and **193 commits between two consecutive openings**. Verdicts were written,
obstructions were registered, the machinery worked — and for long stretches
nobody used it.

Two things were happening, both worth watching for:

- **Node-shaped questions were being written somewhere else** — into the caveat
  blocks of verification scripts, where they accumulated and were never
  promoted. The questions were not missing; they were misfiled.
- **The decision to open one was deferred in conversation and never recorded**,
  so a fresh session saw a long-cold instrument with no explanation at all —
  not a decision, not a deferral, nothing.

Cheap countermeasures, both derived rather than hand-maintained:

- Report the **date of the newest open node** beside the newest closed one. A
  long gap is a finding, not a background fact.
- When a question is deferred rather than opened, **write the deferral down**.
  An undocumented deferral is indistinguishable from an oversight.

## Final Self-Check

- [ ] Did I ask both questions — what stopped us, and what have we read?
- [ ] Does `idea.md` name a target and a checkable kill condition?
- [ ] Is `parent` set, so the tree stays a tree?
- [ ] Could someone with no context resume this from `README.md` alone?
- [ ] At close: is every kill condition dispositioned, and did a surviving
      question get promoted rather than buried?
