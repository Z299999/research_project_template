#!/usr/bin/env python3
"""Commit, with the rules checked BEFORE the commit exists rather than after.

Why this is a program and not a line in CLAUDE.md
-------------------------------------------------
The project this template was distilled from wrote down "measure the subject line before
committing" and then broke it one command later, and five more times after that. Two of those
had already been pushed; one needed a force-with-lease to repair. Writing a rule down does not
make it a rule. A rule that depends on remembering is a suggestion.

So the checks live here, in the path you have to walk anyway. Everything this file refuses is
something that actually went wrong, repeatedly, after being written down somewhere polite.

    python3 tools/commit.py <<'EOF'
    type: subject line, 72 characters or fewer

    Body explaining what changed and why. See prompt/c007.

    Cycle: #NNN
    EOF

    python3 tools/commit.py --parked     # retry a refused message after editing it

What it refuses, and what each refusal cost before it existed
-------------------------------------------------------------
1. A subject over 72 characters. Six of them, each caught after the commit existed.
2. A missing `Cycle: #NNN` trailer. Without it the work has no unit, and `lookback.py`
   has nothing to count, so the whole cadence below silently stops.
3. A lookback that is overdue. See `lookback.py`. Adopted once, then missed at three
   consecutive checkpoints, which is why this refuses instead of reminding.
4. A lookback commit that quietly carries real edits. A look-back is not a work unit, so a
   `git add -A` before writing one swallows a section and a tool fix and the ledger never
   knows. Naming them in a `Carries:` line clears it; the point is to say it out loud.

A refusal never destroys the message. It parks it, because the first version of this guard
sent the author back to retype forty lines of body over one bad subject, which taught them to
write shorter bodies instead of shorter subjects. A guard that is expensive to obey gets obeyed
in the wrong direction.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMIT = 72
LOOKBACK_EVERY = 5
# The process log, kept apart from TIMELINE.md on purpose: TIMELINE.md is what the research
# found, SPRINT.md is what the process did and what it got wrong. Merging them buries the second.
LOG = ROOT / "SPRINT.md"
PARKED = ROOT / ".git" / "COMMIT_REFUSED"


def refuse(reason):
    PARKED.write_text(msg + "\n")
    sys.exit(f"REFUSED: {reason}\n"
             f"  the message is parked at {PARKED}, nothing was lost.\n"
             f"  fix it there, then:  python3 tools/commit.py --parked")


if "--parked" in sys.argv[1:]:
    if not PARKED.exists():
        sys.exit("no parked message to retry")
    msg = PARKED.read_text().strip()
else:
    msg = sys.stdin.read().strip()

subject = msg.split("\n", 1)[0]
if len(subject) > LIMIT:
    refuse(f"subject is {len(subject)} chars, limit {LIMIT}\n  {subject}\n"
           f"  drop {len(subject) - LIMIT} more")

if "Lookback" in msg:
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=ROOT,
                            capture_output=True, text=True).stdout.split()
    carried = [f for f in staged if Path(f).name != LOG.name]
    if carried and "Carries:" not in msg:
        refuse("a lookback is staging files beyond the log:\n  "
               + "\n  ".join(carried[:12])
               + f"\n  ({len(carried)} file(s) total)\n"
               "A look-back is not a work unit, so carried edits must be named.\n"
               "Either unstage them and commit them separately, or add a line\n"
               '"Carries: <what and why>" to the message.')

if "Cycle:" not in msg:
    refuse("no Cycle: trailer. Every work unit needs one (see prompt/c007).")

m = re.search(r"Cycle:\s*#(\d+)", msg)
if m and "Lookback" not in msg:
    cyc = int(m.group(1))
    seen = [int(x) for x in re.findall(r"^## Lookback at `#(\d+)`", LOG.read_text(), re.M)] \
        if LOG.exists() else []
    last = max(seen) if seen else 0
    if cyc - last >= LOOKBACK_EVERY:
        refuse(f"lookback overdue. Last recorded at #{last}, this commit is #{cyc}, "
               f"which is {cyc - last} cycles.\n"
               f"  Run `python3 tools/lookback.py`, answer its four questions into "
               f"{LOG.name} under\n"
               f"  a heading `## Lookback at \\`#{cyc}\\``, and commit that first.\n"
               f"  A commit whose message contains the word Lookback is exempt.")

print(f"subject {len(subject)}/{LIMIT} chars — ok")
subprocess.run(["git", "commit", "-q", "-F", "-"], input=msg, text=True, cwd=ROOT, check=True)
PARKED.unlink(missing_ok=True)
print(subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=ROOT,
                     capture_output=True, text=True).stdout.strip())
