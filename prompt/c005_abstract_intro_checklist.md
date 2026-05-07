# Abstract and Introduction Checklist

This checklist applies to the abstract and introduction of a technical research paper,
especially when presenting a new method, design, or theoretical result.

It is not a proof checklist. It is a writing checklist for the opening of a paper.

## Main Principle

Do not jump too quickly from the problem statement to "we design / we prove."
First explain the mathematical or conceptual structure that makes the contribution natural.

Prefer a structure-driven narrative:

1. problem
2. reduction or decomposition
3. resulting mathematical or conceptual structure
4. method or design enabled by that structure
5. theorem-level or result-level conclusion

## Abstract Checklist

### 1. Start with the precise problem class

- State the model, system, or setting precisely.
- Name the key difficulty or challenge explicitly.
- Avoid opening with only a vague application description.

### 2. State the key reduction or insight before the method

- Say what transformation, decomposition, or insight is introduced.
- Name the resulting mathematical objects explicitly.
- Prefer concrete phrases such as:
  - `the system is reduced to ...`
  - `the model is decomposed into ...`
  - `the dynamics are rewritten as a ... cascade`

Do not move directly from `we consider ...` to `we design / we propose ...` unless the
method is already obvious from the problem statement.

### 3. Name the structure that enables the method

- Identify the exact structural property used in the design or proof.
- Use mathematical names rather than generic phrases.

Avoid overusing vague labels such as:
- `a key structural feature`
- `a suitable decomposition`
- `a cascade structure`

unless they are immediately followed by the precise structure.

### 4. Present the method as a consequence of the structure

- Write contributions in a `because ... therefore ...` style whenever possible.
- Show why the method or result is possible.

Prefer:
- `Since [structural property], we construct ...`
- `Exploiting ... enables ...`
- `This representation allows ...`

over:
- `We also design ...`
- `A key feature is ...`
- `We further show ...`

### 5. Separate the handling of different difficulties

- If the paper handles two different subsystems, mechanisms, or challenges, indicate how
  each is treated.
- Make the reader see where each difficulty is resolved.

### 6. State the theorem-level result precisely

- Say what is proved or shown.
- Say in which variables, metrics, or norms.
- Avoid broad claims that are not matched exactly by the main result.

### 7. End with simulations or experiments briefly

- One short sentence is usually enough.
- Simulations or experiments confirm the result; they do not replace it.

---

## Introduction Checklist

### Recommended Four-Paragraph Introduction Structure

#### Paragraph 1: background and literature positioning

This paragraph should:

1. define the problem class and application context
2. place the paper in the main literature line
3. identify what the existing work has already achieved
4. state the common limitation or open gap that motivates this work

The paragraph should end by making the reader feel the exact gap.

#### Paragraph 2: problem statement and high-level result

This paragraph should:

1. state the precise problem considered in this paper
2. explain the main structural reason the problem is tractable
3. state the main theorem-level or result-level contribution

This is the paragraph where the paper says clearly what it does.

#### Paragraph 3: technical proof or method narrative

This paragraph should explain the technical approach in plain English, without heavy
notation or symbols.

Its job is not to restate the theorem. Its job is to let the reader see, before entering
the technical sections, how the method or proof actually works.

This paragraph should typically answer:

1. how the original problem is transformed or decomposed
2. which part carries the main technical difficulty
3. what transformation, algorithm, or argument handles that difficulty
4. what part of the work is already standard or autonomous
5. what argument closes the result
6. how the argument connects back to the original problem

In other words, the third paragraph should tell the technical story from beginning to end,
in plain English.

#### Paragraph 4: paper organization

This paragraph should remain short and factual.

---

### Detailed Introduction Guidelines

#### 1. First paragraph: build the literature bridge, not just a citation list

The first paragraph should do four jobs:

1. define the problem class
2. place the paper in the main literature line
3. identify the common limitation of the existing works
4. explain what changes when the main difficulty of this paper is introduced

Do not stop at a sequence of paper summaries.

#### 2. Second paragraph: state the paper through the mechanism, not only the result

The second paragraph should answer:

- what exact problem is solved?
- what specific structural property makes the solution possible?
- what is the main result?

Prefer the order:

1. problem solved
2. structural reason the method works
3. consequence for the main result

#### 3. Name the mathematical or conceptual objects early

- Let the reader know which object or quantity carries the main technical difficulty.
- If the paper relies on a key decomposition, transformation, or representation, name it
  early enough that the reader can orient themselves.

#### 4. Be careful with novelty wording

- Novelty should be factual, not promotional.
- Every strong sentence in the introduction should be traceable to a theorem, proposition,
  or explicit derivation later in the paper.

Before keeping a sentence, ask:
- Is this proved later?
- Is this mathematically defined later?
- Is this the exact result, or am I overselling?

#### 5. Prefer mechanism words over advertising words

Prefer:
- `reduced to`
- `rewritten as`
- `consists of`
- `decomposes into`
- `allows`
- `yields`
- `implies`

Use sparingly:
- `novel`
- `powerful`
- `remarkable`
- `significant`
- `key`

#### 6. Keep the proof-preview paragraph structural

If a third paragraph previews the proof or method, it should say:

- what decomposition or transformation is used
- what argument or tool handles the main difficulty
- what closes the result

It should not repeat the same contribution claims from the second paragraph.

#### 7. No heavy notation in the introduction proof narrative

For the introduction, especially the third paragraph:

- do not use displayed equations when plain English suffices
- do not introduce proof-driving notation if it can be avoided
- do not force the reader to parse symbols before reaching the model section

The reader should understand the mechanism from English prose alone.

Good introduction proof-preview language:

- `The system is decomposed into a [structure A] component and a [structure B] component.`
- `The main difficulty is handled by [transformation/argument].`
- `The remaining dynamics are already stable and require no further control effort.`
- `A composite energy argument then yields [main result] in the original variables.`

---

## Sentence-Level Style Checklist

### Prefer these habits

- Use concrete mathematical or technical nouns.
- Make the logic visible with `because`, `since`, `thus`, `therefore`, `which yields`.
- Let the structure explain the method.
- Let the method explain the result.

### Avoid these habits

- announcing results before giving the structural reason
- stacking multiple contribution verbs in a row
- using generic phrases without naming the actual mathematical or technical object
- claiming a stronger result in prose than what the theorem or main result supports

---

## Quick Self-Check Before Finalizing

For the abstract:

- Does the reader see the key reduction or insight before the method?
- Does the reader see why the method or design is possible?
- Are the main technical difficulties separated clearly?
- Is the result-level claim matched exactly by the actual theorem or main result?

For the introduction:

- Does paragraph 1 identify the literature gap precisely?
- Does paragraph 2 explain the paper through structure, not only result?
- Does paragraph 3 tell the technical story clearly in plain English?
- Are the main mathematical or conceptual objects named early enough?
- Could any sentence be accused of overclaiming?

---

## Short Template

### Abstract template

1. We consider [precise problem class] with [key difficulty].
2. By [reducing / decomposing / rewriting] ..., the problem is reduced to ...
3. Exploiting [structural property], we [design / propose / prove] ...
4. We [prove / show / establish] [main result].
5. Numerical simulations / experiments confirm the result.

### Introduction template

Paragraph 1:
- problem class
- main literature line
- existing limitation
- why this paper's difficulty changes the problem

Paragraph 2:
- exact problem solved
- structural mechanism enabling the method
- main result

Paragraph 3:
- decomposition or transformation used
- difficulty-handling mechanism
- standard or autonomous part
- closing argument
- connection back to original problem

Paragraph 4:
- paper organization only
