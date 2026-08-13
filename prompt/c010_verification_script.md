# Verification Script Checklist

This checklist records how to freeze a computational claim so that it stays
checked after the session that made it has ended.

Use it whenever a claim in prose rests on a calculation — a symbolic
manipulation, a scaling argument, an integral, a counterexample, a numerical
threshold.

## Main Principle

**Prose is not evidence. A script that runs is.**

Every non-obvious claim gets a small, self-contained script that a fresh
session can run without context and that prints a pass/fail line per assertion.
The script is *frozen*: once committed it is not edited to keep pace with new
understanding. A later correction is a new script that says what changed.

The reader should be able to answer, from the script alone:

1. what exactly is asserted
2. under what assumptions
3. what is deliberately *not* asserted

## Required Structure

### 1. Open with a scope line

The first comment states the setting in which every later line is true —
dimension, domain, regime, and whether the object is the real system or a
simplified model.

```python
# SCOPE: three-dimensional, incompressible, on the whole space. This is a change
# of variables on the exact system -- no term is dropped -- so it is a statement
# about the equations and NOT about a model.
```

Say **model or not**. A reduction that drops a term, or prescribes a quantity
the system would determine, is a model, and a reader must not have to infer it.

### 2. One printed assertion per claim

```python
print("CHECK the kernel is homogeneous of degree -1:", sp.simplify(ratio - 1/lam))
```

The label states the claim; the value is `0` (or an expression that simplifies
to `0`) when the claim holds. A grep for a nonzero result then finds every
failure.

### 3. Include a positive control

An assertion that something does **not** vanish, or that a nearby case
**fails**. Without one, a bug that makes everything vanish passes silently.

```python
# NOT VACUOUS: the undifferentiated kernel has degree 0, so the -1 comes from d_z.
print("CHECK the undifferentiated kernel has degree 0:", sp.simplify(ratio0 - 1))
```

### 4. Close with a `NOT ASSERTED` block

State what the script does *not* establish: unread sources, ansatz assumptions,
constants not computed, cases not covered.

## Failure Modes To Avoid

These are recorded from real incidents, not predicted.

- **The vacuous assertion.** `print("CHECK ...", 0)` passes whatever the code
  does. So does `0 if True else 1`, `X - X == 0`, arithmetic on literals like
  `0 if 1/2 + 3/2 == 2 else 1`, and `... or True`. A check that asserts nothing
  is **worse** than no check, because it makes the suite look larger.
- **The mislabelled assertion.** A real computation printed under a label it
  does not test. Worse than plain vacuity: the number is honest and the
  sentence is not.
- **The restatement.** Asserting a definition you just wrote, or a positivity
  you just declared. Derive it instead — compute the sphere area from the
  general formula rather than typing `2*pi**2`.
- **Silenced failure.** `grep`-ing a script's output for failing lines misses a
  script that *crashed*. **Check the exit code, not the output.**

## A Caution About The `NOT ASSERTED` Block

Measured across 89 scripts in one project: 74 carried either three or four
items, and never two, five or six. **A caveat list that is always three or four
long is a form, not an inventory.**

The block still earns its place — it bounds a claim, and it is what lets a
later correction say precisely what survives. But it is **not a queue**.
Writing a risk down does not schedule it. In that project the same concern was
written into three consecutive blocks and read zero times, and two units of
work were withdrawn for exactly that unchecked concern.

If a concern recurs across consecutive scripts, address it or say explicitly
why it stays open.

## When A Listed Failure Mode Keeps Happening, Gate It

**The list above did not stop the first item on it.**

In one project `X - X == 0` was written into that list after two instances were
found in a single unit, together with the conclusion *"the reread is catching it
every time, which is the only reason it is not accumulating."* A scan run
twenty-five units later found **nine more in the committed corpus, across eight
files**. Two sat one line from an explicit `# NOT VACUOUS:` comment — the author
was reasoning about vacuity in that very paragraph and missed the conjunct
anyway. A third sat two lines below a comment that named self-division by name.

**A reread does not scale to a corpus.** It catches the instance in front of
you; it is a habit, and habits decay as the corpus grows.

### Gate only a form with a syntactic signature

Most vacuity has none. *"This computation is honest but does not test the
sentence above it"* has no signature and never will. Two recurring forms do:

| form | signature |
|---|---|
| `print("CHECK ...", 0)` | a bare literal as the printed value |
| `X - X`, `X / X`, `X == X` | two operands that are the **same subtree** |

The second is zero-heuristic — `X - X` is zero for every `X`, so no subject
knowledge is used. Compare two syntax trees for structural identity, and stop
there. Resist adding a word list; a pattern fitted to the instances you already
found will only re-catch the past.

### Run the scan before writing the rule

The exemptions decide whether the gate is usable, and **they are found, not
predicted.** The raw scan above returned 13 hits, and four were legitimate:

- `name == name` is the **NaN test** — false for NaN, so it asserts something.
- `1 - 1` written as a *substitution argument* displays an endpoint rather than
  asserting a quantity.

Both were in live use, and neither was on anyone's list before the scan ran. **A
gate that also blocks the legitimate idiom is worse than no gate**, because it
teaches everyone to bypass the hook.

### If scripts are frozen, ratchet — and grandfather by name

This checklist says a correction is a **new script, never an edit**. That makes
a plain gate a permanent wall: the nine existing hits cannot be repaired, so it
would block every commit forever.

Ratchet instead. Generate a baseline of `path:line:kind` and block only what is
absent from it. **Grandfather by name, never by a count** — a count hides
exactly the instances the scan exists to expose, and it is the kind of number
that then gets quoted as if it were a clean bill of health.

### Ship the gate with its limit stated

The structural-identity gate does **not** catch the same tautology written in
two groupings — `total - (a + b) - (c + d)`, where `total` was typed as
`a + b + c + d` two lines earlier. That was found by rereading, four units after
the gate was built, in the gate author's own new script. A gate is a floor.
Saying where the floor ends is part of shipping it.

## Final Self-Check

- [ ] Does the first line say the scope, and whether this is a model?
- [ ] Does every claim in the prose have a printed assertion here?
- [ ] Is there at least one positive control?
- [ ] Would a fresh session, running only this file, reach the same verdict?
- [ ] Did I check the **exit code**, not just the printed lines?
- [ ] Is any check here a tautology of how I *typed* the expression, rather than
      a statement about the mathematics?
