# Proof and Mathematical Writing Checklist

This checklist records preferences for writing theorem statements, proofs, and
technical mathematical exposition.

It is intended for writing and revising:

- main results sections
- theorem statements
- technical proof sections
- proof sketches and mathematical explanations

## Main Principle

Write proofs so that the mathematical action is visible immediately.

Prefer:

1. explicit objects
2. explicit domains or intervals
3. explicit inequalities
4. one estimate or argument per step
5. final assembly only at the end

Avoid hiding the proof behind abstract wording.

---

## Source Discipline

### 1. Separate facts from derivations

Always distinguish clearly between:

- facts already stated in the manuscript or cited literature
- conclusions derived from those facts in the current proof

Do not blur sourced statements with informal interpretation.

Useful labels when discussing or revising:

- `manuscript / literature fact`
- `derived from the current definitions`
- `based on the current proof structure`

### 2. Keep claims exactly aligned with the mathematics

- If the theorem is about a specific setting or variable, call it that — do not describe
  it more broadly.
- Do not use stronger words in prose than what the theorem or proof supports.
- If a claim requires a separate argument, do not treat it as obvious.

---

## Main Results Writing

### 1. Present methods and designs structurally

For a new method or design, present the logic in this order:

1. the reduced or transformed subsystem that carries the main difficulty
2. the baseline or nominal approach (what works in the simpler case)
3. the target relation the method is meant to enforce
4. the implementable form of the method
5. the resulting closed-loop or post-method dynamics

The method should look motivated, not guessed.

### 2. Use the paper's own language, not copied source language

- Follow the structure of the literature when needed.
- But explain the method in the variables and logic of the current paper.
- Avoid dropping in a formula without first stating what nominal relation it is meant to
  enforce.

---

## Proof Organization Checklist

### 1. Use step titles that state the mathematical action directly

Prefer step titles such as:

- `Bound [quantity] on [domain]`
- `Bound [quantity] using [lemma / estimate]`
- `Combine [case A] and [case B]`
- `Assemble the final estimate`

Avoid abstract titles such as:

- `Transient analysis`
- `Recover the physical variables`
- `Uniform bound`

unless the mathematical object and domain are stated immediately after.

### 2. One step, one job

Each proof step should establish one self-contained estimate or argument.

Typical pattern:

1. state what is being bounded or proved in this step
2. carry out the estimate or argument
3. stop — do not partially merge into the next step

### 3. Assemble only at the end

If the proof breaks into several component estimates (for example, a decay estimate,
a norm equivalence, and an initial-data bound), each component should appear in its own
step, and the full theorem estimate should be assembled only in the final step.

---

## Displayed Mathematics Checklist

### 1. Prefer continuous `aligned` chains

Within a proof step, prefer a continuous `aligned` inequality or equality chain when the
argument is a direct sequence.

Use `aligned` especially when:

- differentiating an energy or Lyapunov functional
- carrying out a norm estimate
- converting one bound into another
- assembling a final inequality

### 2. Do not over-split one chain into many displays

If several lines belong to the same uninterrupted argument, keep them in one `aligned`
block rather than breaking them into many short displays.

### 3. Do not over-pack unrelated estimates

If two lines estimate different objects with different purposes, separate them into
different blocks or different proof steps.

Rule of thumb:
- one mathematical goal → one `aligned`
- different mathematical goals → different displays or steps

---

## Language Checklist

### 1. Prefer concrete mathematical language

Prefer concrete objects, domains, and variables over abstract wording.

Prefer:
- `bound [quantity] on [domain or interval]`
- `bound [quantity] using [specific lemma]`
- `bound the left-hand side of the theorem estimate`

over:
- `control the transient`
- `recover the physical variables`
- `handle the [abstract regime]`

unless the more abstract phrase is genuinely clearer.

### 2. State domain or interval information explicitly

When the proof depends on a specific domain, range, or interval, write it directly:
- `for [variable] in [domain]`
- `on the interval [a, b]`
- `for [condition]`

This is usually clearer than prose such as `the transient regime` or `the shifted window`.

### 3. Avoid undefined quantities

- Do not introduce a quantity in a proof unless it is defined or derivable from the
  definitions already given.
- If a quantity exists only under certain conditions, do not apply it outside those
  conditions without justification.

---

## Technical Narrative Checklist

### 1. Make the role of each subsection explicit

Each technical subsection should answer a clear question. For example:

- transformation subsection: what obstacle does this transformation remove?
- estimation subsection: what part of the full estimate does it control?
- recovery subsection: how do we return from transformed variables to the original ones?

### 2. Explain why a tool appears

When introducing a technical object such as:

- a change of variables or transformation
- an energy functional or Lyapunov candidate
- an imported lemma or abstract result

state explicitly what problem it solves in the proof.

---

## Final Self-Check

Before finalizing a proof section, ask:

- Does each step title tell the reader exactly what is being bounded or proved?
- Does each step perform one independent estimate or argument?
- Are the main inequality chains written in `aligned` form when appropriate?
- Are abstract English labels replaced by concrete mathematical language where possible?
- Are all relevant domains, ranges, or conditions stated explicitly?
- Is the final theorem estimate assembled only after the component bounds are complete?
- Is every claim in the proof traceable to a definition, lemma, or prior result?
