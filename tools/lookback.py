#!/usr/bin/env python3
"""Every five work units, stop and re-check the last five. Then keep going.

Why five, and why a program
---------------------------
In the project this came from, the single highest-yield habit was not a checklist and not a
review. It was stopping every fifth unit to ask whether the previous five were still true. Over
ninety of these were run. They found, among much else: a claim that had reached five places in
four days and been corrected in one; a number that was right while the noun beside it was wrong;
an experiment that landed while the paper stayed unaware of it; and a whole framing that the
first honest run refuted.

None of those was found by working harder on the next unit. They were found by looking back at
units that had already been committed and called done.

The habit was adopted once and then missed at three consecutive checkpoints, so `commit.py`
refuses the sixth unit until a lookback is written. That refusal, not this file, is what makes
it happen.

    python3 tools/lookback.py

Then answer its four questions in writing, into SPRINT.md, under `## Lookback at `#N``.
In writing matters. An answer thought and not typed is indistinguishable from one skipped.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
N = 5

log = subprocess.run(["git", "log", "-80", "--format=%h%x00%s%x00%b%x01"],
                     capture_output=True, text=True, cwd=ROOT).stdout
cycles = []
for rec in log.split("\x01"):
    if not rec.strip():
        continue
    h, subj, body = (rec.strip().split("\x00") + ["", ""])[:3]
    m = re.search(r"^Cycle:\s*#(\d+)", body, re.M)
    if m:
        cycles.append((h, f"#{m.group(1)}", subj))
    if len(cycles) >= N:
        break

if not cycles:
    raise SystemExit("no `Cycle: #N` trailers found in the last 80 commits.\n"
                     "Add one to each work unit (see prompt/c007) and this becomes countable.")

print(f"LOOKBACK over the last {len(cycles)} units ({cycles[-1][1]} -> {cycles[0][1]})\n")
for h, cyc, subj in reversed(cycles):
    print(f"  {cyc:<8}{h}  {subj}")

print("""
Answer these in writing, into SPRINT.md, before starting the next unit:

  1. WHAT DID THEY CLAIM?  One line per unit. If a unit's claim cannot be stated in one
     line, it did not have one, and that is itself the finding.

  2. IS EACH STILL TRUE?   Against everything measured since, including results that landed
     after the unit was committed. A claim that fails here is CORRECTED NOW, in the document
     and in the log, not recorded as a caveat for later.

  3. WHAT WAS DEFERRED?    Anything queued, promised in a commit message, or quietly dropped.
     Compare against TODO.md rather than trying to remember; that is what it is for.

  4. WHAT ARE THE NEXT FIVE FOR?  If the answer is "keep going", the next five have no
     target and should be planned before they are spent.
""")

# Question 3 was answered from memory for a long time, into prose that nothing read back. Three
# debts survived hundreds of units that way. Printing the standing list here turns that question
# from a recollection into a comparison.
todo = ROOT / "tools" / "todo.py"
if todo.exists():
    out = subprocess.run([sys.executable, str(todo)], capture_output=True, text=True).stdout
    if out.strip():
        print("STANDING DEBTS (tools/todo.py), so that question 3 is checked and not recalled:\n")
        print(out.rstrip() + "\n")
