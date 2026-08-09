# Measurement and Control Checklist

This checklist applies whenever a measurement will be used to **close a branch, choose
between methods, or justify shipping something**. It is not a statistics tutorial and it
does not prescribe tests; it lists the failure modes that survive ordinary care.

It is a companion to `c008` (experiment structure). `c008` governs how a campaign is laid
out; this one governs whether its numbers may be believed.

## Main Principle

A control that passes while checking something **other than what you think** is worse than
no control at all.

With no control you know you have not verified anything. With one that checks the wrong
proposition, you count the unverified part as verified — and the passing result actively
increases confidence in the wrong direction.

## 1. Before trusting a control, say what would make it fail

If you cannot name a state of the world in which the control fires, it is not a control.
Write that state down **before** running it.

Controls that cannot fail, and what each was mistaken for:

| The check | What it actually verifies | What it was read as |
|---|---|---|
| A reproduction that matches bit-for-bit | The evaluation path is correct | The two models are comparable |
| Recorded metadata fields all agree | *Those* fields agree | The configurations are the same |
| A replication at a second condition | Nothing differs at that condition | The original effect does not replicate |
| "The script ran and printed a number" | It terminated | It used the whole dataset |

The last two are worth expanding, because they look like diligence:

- A replication attempt has **no power at a condition where the effect never existed**.
  Check that the effect is present in the control condition before using it to replicate.
- A default argument can silently change *what was measured* (a truncation, a filter, a
  path). Print the sample count next to every result and read it.

## 2. Write the acceptance criterion before seeing the number

Fix the bands in advance, and state what each one licenses:

- clearly positive → act
- clearly negative → close the branch and record the obstruction
- in between → collect more evidence; **do not** announce a direction

Also allow a fourth outcome: **the criterion cannot be applied**. If a diagnostic's input
turns out to be uninterpretable, the criterion fires in neither direction. Reading a voided
number as negative evidence is the same error as reading it as positive.

When a criterion passes by a hair, say so in the same sentence that reports the pass.

## 3. Measure the noise floor before reading a difference

Repeat the **same** configuration, varying only the seed, and use that spread as the
resolution limit. A difference smaller than the floor is not a small effect; it is
unreadable.

Two mistakes to avoid:

- **Do not infer the floor from two runs that differ in configuration.** That measures the
  configuration difference, not the noise, and it will usually overstate the floor — which
  then causes real effects to be dismissed.
- **Report paired differences** (same seed, one variable changed) rather than differences
  of means. Pairing removes the shared randomness and is often several times tighter.

## 4. A measurement carries its context

Before reusing any number, ask under what conditions it was produced and whether those
still hold:

- dataset and its size
- the scoring definition or metric version
- the operating point (a ratio measured at one scale is rarely constant across scales)
- the code path that produced it
- the objective or loss the model was trained under

The failure is silent — nothing errors when a number is moved out of its context. The only
reliable remedy is to re-measure under the current conditions rather than to be more
careful.

## 5. An optimum on a search boundary is not converged

If a one-dimensional sweep returns its endpoint, the range stopped the search, not the
data. Widen and re-read before quoting the value.

## 6. Closing a branch requires an obstruction; parking requires a reopen condition

- **Closed** — record *why* it cannot be re-entered, concretely enough that a reader six
  months later does not have to redo the experiment.
- **Parked** — record an **executable** reopen condition ("if X is measured above Y").
  "Revisit later" is a silent permanent closure.
- Never delete a failed branch. A closed branch with a recorded obstruction is what stops
  the same neighbourhood from being re-entered.

## 7. Generate derived surfaces, and make staleness fail

Any document that restates state kept elsewhere — a status page, a summary table, a tree of
attempts — will drift from it.

- Generate the derived document from its source, between explicit markers.
- Add a check that fails when the generated block and the source disagree, and run it on a
  schedule that is hard to skip.
- **Compare content, not a freshness marker.** A marker that is updated by hand gets
  updated without the content, and every gate that reads only the marker then passes while
  the content rots.

## Quick pass before recording a result

1. What would have made my control fail? Could it have?
2. Was the criterion written before the number was seen?
3. Is the difference above the measured noise floor, and is it paired?
4. Under what conditions was each number I am reusing produced?
5. Did any optimum land on a search boundary?
6. If this closes a branch, is the obstruction recorded? If it parks one, is the reopen
   condition executable?
