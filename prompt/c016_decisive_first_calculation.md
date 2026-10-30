# The Decisive First Calculation

**When to use.** Before committing time to a new research problem, especially
one built by adding something (a state variable, a delay, a constraint) to a
known model.

Companion to `c012` (attempt tree): this is the node you open first.

## Main Principle

**Most proposed problems have one calculation that decides whether they are
new. Find it, run it first, and drop the problem if it comes out the wrong way.**

## 1. Identify the deciding calculation

Ask: *if this calculation came out trivially, would the problem reduce to a
known one?* That is the calculation to run.

Typical example: a new state variable is added to a known controlled loop.
Write the linearization and the characteristic equation. Either the new
variable couples to the controlled loop, or it factors out as a separate
stable (or unstable) block. If it factors out, the "new" problem is the old
problem plus a decoupled scalar, and nobody needs a paper about it.

Other deciding calculations of the same kind:

- whether a new term changes the sign structure a known Lyapunov function
  relies on;
- whether a new coupling survives a change of coordinates that the known
  theory already uses;
- whether a new constraint is ever active along the trajectories of interest.

## 2. Run it before anything else

- Do it by hand or in a short verification script (`c010`), not as part of a
  draft.
- Record the outcome as a node in the attempt tree (`c012`), with the kill
  condition written before the calculation: "drop if the new variable factors
  out of the characteristic equation."
- If it factors out, drop the problem and record the obstruction. A dropped
  problem with a recorded reason is a result.

## 3. Discuss physical meaning before mathematics

Before the deciding calculation, settle with the researcher who owns the
problem:

- what each state variable means physically, and its units;
- what the input actually manipulates;
- whether an analogy to another field is **exact** (the same equations) or
  only suggestive. A suggestive analogy is fine as motivation and wrong as a
  modelling step.

Misreading what a variable means is the cheapest error to prevent and the most
expensive to find after the proof is written.

## Checklist

- [ ] Physical meaning of every state and input agreed with the problem owner
- [ ] Each analogy labelled exact or suggestive
- [ ] The single deciding calculation named, with its kill condition written first
- [ ] Calculation run before any drafting
- [ ] Outcome recorded in the attempt tree, including a drop if it factors out
