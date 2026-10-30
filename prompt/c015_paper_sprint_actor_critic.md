# Paper Sprint: Actor, Critics, Steward

**When to use.** A short draft (a few pages, one main result) has to reach a
submittable state inside a fixed time box, typically one hour. The protocol
below was run end to end on a 6-page two-column control-conference draft about
a structured dynamical model, with five critic rounds and four checkpoint
uploads. Everything here is what that run did or what it got wrong.

## Main Principle

**The person who writes the draft must not be the only person who judges it,
and every judgment must be written down with a decision next to it.**

Critics find problems; they do not decide. A Steward decides, and records why.

## 1. Roles

- **Actor.** Writes and fixes. Owns the source. Re-reads the rendered pages
  while critics run.
- **Literature agent.** Runs first. Returns exact pointers (section, theorem or
  equation number) for every result the draft will lean on, each verified
  against a local source. Nothing is cited from memory. It also checks the
  older bibliography files and catches wrong DOIs and wrong titles.
- **Critics.** Independent. They never read each other's reports. Typical set:
  - *Rigor*: hypotheses, quantifiers, constants, every step of every proof.
  - *Fresh referee*: reads only the PDF, as a human reviewer would.
  - *House style*: runs the checklists (`c005`, `c006`).
  - *Senior reviewer*: novelty, homage to the work built on, and dialogue with
    each community the paper touches; writes a coffee-break pitch (two
    sentences) per community and says whether it lands.
- **Steward.** Maps every critic item to *accept* or *reject* with a reason, in
  a decision table:

  | item | source | decision | reason |
  |---|---|---|---|
  | hypothesis stated on the solution | rigor r1 | accept | restate on data |
  | "Fig. 2 missing" | referee r1 | reject | critic read a stale build |

  A rejection needs a reason as much as an acceptance does. The table is what
  keeps the loop honest when time runs short.

## 2. Timeline for 60 minutes

| minutes | work |
|---|---|
| 0–5 | Write the brief. Launch the literature agent and a figure agent. |
| 5–15 | Write the mathematical core first: setting, assumptions, theorem, proof. |
| 15–25 | Round-1 critics in parallel. Actor re-reads the render meanwhile. |
| 25–35 | Steward decisions; fixes. Checkpoint upload. |
| 35–45 | Round-2 critics: rigor recheck of the rewritten parts only, and one fresh reader. |
| 45–55 | Final fixes, final build, final upload. |
| 50–60 | Distillation: what the sprint taught, written into `SPRINT.md`. |

Upload a checkpoint after every round (v1, v2, ...). In the recorded run a late
round broke the build; the previous checkpoint was already out.

## 3. Rounds that turned out to be worth running

The recorded run used more rounds than the template above, in this order:

1. rigor; 2. fresh referee; 3. house style; 4. novelty and community;
5. round-2 rigor recheck of rewritten parts, plus a fresh reader;
6. a full final read;
7. **citation fidelity**: every sentence about a cited work compared with the
   verified pointers from the literature agent;
8. **readability**: a reader one level less expert than the audience;
9. **late-edit audit**: hunt specifically for damage done by cuts.

What each stage found, observed:

- The mathematics converged by round 3. After that no critic found a
  mathematical error.
- Later rounds found other things: prose drifting beyond what the pointers
  support, sentences garbled by cuts, and terminology drift after a model
  change (an old word for a quantity survived in two places after the quantity
  was redefined).
- One critic reviewed a stale PDF. **Always give critics the source and a
  fresh build, and state the build time in the brief.**

## 4. Discipline during the sprint

- A background rebuild every two minutes, logging the page count.
- A timestamped Steward self-check every few minutes, three lines: what
  changed, what is weakest now, what is next.
- Look at the rendered pages, not only the page count. Two-column layouts hide
  overfull displays that the log reports only as a warning.
- Meet the page limit by cutting prose. Never shrink fonts or margins. After
  each cut, check that no bridge sentence (the one telling the reader why the
  next step is needed) went with it.

## 5. Mathematical honesty

- **Hypotheses go on the data, not on the solution.** A critic caught an
  assumption stated on the unknown trajectory. It was replaced by a condition
  on the initial data plus a short regularity lemma showing the property
  propagates.
- **When a theorem is a direct application of a cited result, say so.** Claim
  the reduction (the transformation, the verification of the cited result's
  hypotheses), not the proof.
- **Name the idea you build on.** Replace "these works do not ..." with a
  sentence naming the specific idea from those works that this paper uses.

## 6. What the recorded run got wrong

- The page count oscillated around the limit for several rounds, because cuts
  and critic-driven additions alternated without a budget. Fix: give each round
  a line budget before it starts.
- The Actor's own overclaims survived into round 2. One ("cannot be removed"
  where the theorem gives only a lower bound) was noticed while processing the
  novelty round; another (a stated trade-off that was false under the model's
  own assumptions) was caught by the round-2 fresh referee. Fix: the Actor
  rereads every claim sentence against the exact theorem statement before
  round 1, as strictly as a critic would, and citation fidelity runs no later
  than round 2.

## Checklist

- [ ] Literature pointers verified locally before any citing sentence is written
- [ ] Critics independent; each given source plus a fresh, timestamped build
- [ ] Every critic item in the Steward table with a decision and a reason
- [ ] Checkpoint uploaded after every round
- [ ] Rendered pages inspected, not only the page count
- [ ] Page limit met by cutting prose, bridge sentences checked after cuts
- [ ] Every hypothesis stated on data; reductions to cited results claimed as reductions
- [ ] Citation fidelity pass done; terminology checked after any model change
- [ ] Sprint lessons written into `SPRINT.md`
