# Make The Corpus Retrievable

**When to use.** Once a project has accumulated more of anything — sources,
verified claims, entries, decisions — than one session can hold in its head.
That threshold arrives much earlier than it feels like it does.

Recorded from measured incidents in one long-running project.

## Main Principle

**Recording and retrieving are two different builds, and finishing the first
feels like finishing both.**

A corpus you cannot reach is not an asset. It is worse than an absent one,
because its existence is the reason nobody goes looking elsewhere.

## 1. The failure looks like ordinary productive work

That project accumulated **468 machine-checked assertions** across some eight
hundred units of work, and **nothing indexed them.** The sources had an index.
The vocabulary had one. The most expensively verified material in the
repository had none.

In one working session, **five units rebuilt or nearly rebuilt something the
corpus already held.** One reconstructed a table another unit had produced 117
units earlier. Another came within one step of re-deriving two already-checked
facts.

None of those units felt like waste while they were happening. **That is the
whole difficulty**: rebuilding is indistinguishable from working, from the
inside.

## 2. One ranking mode per class of artefact, and rank on the right field

A single search box over everything ranks badly, because the informative field
differs by class:

| class | rank on | not on |
|---|---|---|
| sources | **what the source turned out to contain** | the title — that is only why you fetched it |
| vocabulary entries | relevance, then structural fan-in | recency alone |
| verified claims | **the assertion text** | the header comment, or the filename |

**Print the match, not the file.** A pointer to a two-hundred-line script is a
second search. Show the assertion that matched — and show the opening of the
file's scope header beneath it, because the assertion says what was proved and
the header says under what assumptions. In that project a unit took a result
from a one-line summary without opening the file; the scope word that would
have stopped it was sitting in the header, unshown. The error cost three units
and two debts.

## 3. Validate the retriever on the misses you actually made

Not on a query you invent afterwards. Invented queries are written by someone
who already knows the answer, and they always pass.

> Take a real occasion where the project rebuilt something it already held.
> Require the tool to rank the held thing **first**. Pin it as a regression.

Add a control in the other direction too — an off-topic question must match
almost nothing. A retriever that matches everything is not a ranking. One
version of that project's source ranker matched **121 of 121** records before a
stoplist was added; another expanded queries so aggressively it went from 12
matches to 104 and was worse than no expansion.

## 4. Query on the claim you are about to write, not the topic you are reading

This is the difference between a retriever that fires and one that does not.
*"What do we know about X"* is a browsing question and gets asked rarely.
*"Have we already established this exact sentence"* is answerable, has a sharp
answer, and is asked at precisely the moment the answer is worth money.

The same applies to absence. **Before writing *blocked*, *unknown*, or *no
source exists*, run the retrieval.** Those words instruct every future reader
not to try, so they are the most expensive claims in the repository. In that
project, three separate times in one day, something was recorded as unknown
while the corpus already held it — once with a better statement than the one
being sought.

## 5. Records are retrieved by the words the *recorder* used

A source was registered, its relevant section marked as read, and the note was
accurate. **581 units later** someone reopened it and found the sentence that
mattered.

The retriever was not broken. The source wrote a quantity in its own notation;
the project asked in the project's own vocabulary. The **topic** query ranked
that source first. The **content** query, phrased the way the project actually
thinks, did not surface it at all — even after the verbatim quote was added.
Adding one translating sentence moved it from absent to rank one.

**So record both:** the source's words verbatim, *and* one sentence saying what
it means in the vocabulary your project queries in. The first is required for
honesty. The second is what makes it findable.

## 6. Provide a mode for when you do not know what to ask

Ranking answers a question. Something must also answer *"what is in here?"* —
and it must be **derived**, or it becomes a hand-maintained README over a
growing corpus, which is the same staleness in a new place.

Derive the groups from the filenames, and the claim shown for each item from its
**first assertion**, not from its header comment: what a script proves is what
it asserts, not what its comment says it asserts.

Two defects worth avoiding, both from a first build: splitting names on the
first separator produced a group called *"the"* holding seven unrelated items —
grouping on a stopword is not grouping — and an over-eager placeholder strip ate
a subscripted symbol out of a plain string that was never a template.

## 7. Say where coverage comes from, or do not claim it

If a map reports complete coverage, name the gate that guarantees it. That
project's map inherited totality from a **separate rule** requiring every frozen
script to assert something. The map itself had an *"(no assertion)"* branch and
was not complete by construction.

The difference matters the day someone relaxes the other gate: the map starts
under-reporting for a reason nothing in the map records.

## Quick pass

- [ ] Which class of artefact here has grown past a hundred with nothing
      ranking it?
- [ ] Am I querying the **claim** I am about to write, or the topic I am reading?
- [ ] Did I run a retrieval before writing *unknown*, *blocked*, or *no source*?
- [ ] Does each record carry the source's words **and** a translation into my
      project's own vocabulary?
- [ ] Is the retriever pinned to a real miss, and to an off-topic control?
