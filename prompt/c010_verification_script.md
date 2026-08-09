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

## Final Self-Check

- [ ] Does the first line say the scope, and whether this is a model?
- [ ] Does every claim in the prose have a printed assertion here?
- [ ] Is there at least one positive control?
- [ ] Would a fresh session, running only this file, reach the same verdict?
- [ ] Did I check the **exit code**, not just the printed lines?
