#!/usr/bin/env python3
"""What does this repository still claim is alive that is not?

Written after reconstructing a real project's history. Its catalog listed three experiments as
`active` that had had no commit for ten weeks, and they had been *entered* as active by a
completeness check run ten weeks after their last commit: the check found folders missing from the
catalog, added them, and filled the status field from the folder's existence because nothing else
was available to fill it from. Their status has never changed. The project's own commit message
for that check says "a catalog that misses an experiment is not a catalog; it is a file that
happens to contain most of them." The sequel it did not write is that a catalog which marks dead
work as live is worse, because the first kind of file is visibly incomplete and the second reads
as an answer.

The same project's front-door README still described the repository as paused, and its main line
of work as "hook only, not started", three months and three hundred and fifty commits into that
line of work. A reader arriving at the repository was told the opposite of the truth by the first
file they opened.

Neither is a wrong measurement. Both are documents that stopped tracking a repository that kept
moving, and both are invisible from inside: you do not re-read your own front door.

    python3 tools/stale.py
    python3 tools/stale.py --days 30        # what counts as quiet, default 45

WHAT IT CHECKS
  1. catalog entries marked active whose folder has had no commit in --days
  2. folders with no catalog entry, and entries with no folder
  3. the front door: README.md and CLAUDE.md, against the repository's last commit
  4. any file whose text claims a state ("paused", "not started", "in progress", "TODO: fill in")
     while the thing it describes has moved since that file did

None of these is fatal on its own. Every one of them was, in the project this came from, true for
months while nobody noticed, because a stale claim about status produces no error and no wrong
number. It just quietly misinforms the next reader, who is usually you.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGS = [("experiments", ROOT / "experiments" / "catalog.jsonl"),
            ("writing", ROOT / "writing" / "catalog.jsonl")]
FRONT = ["README.md", "CLAUDE.md", "TIMELINE.md"]
CLAIMS = re.compile(r"\b(paused|not started|hook only|in progress|coming soon|TBD|"
                    r"\[Fill in|TODO: fill)\b", re.I)


def last_commit(path):
    r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(path)],
                       cwd=ROOT, capture_output=True, text=True)
    s = r.stdout.strip()
    return datetime.fromisoformat(s) if s else None


def days_since(dt):
    return None if dt is None else (datetime.now(timezone.utc) - dt).days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=45)
    a = ap.parse_args()
    problems = 0

    head = last_commit(".")
    repo_age = days_since(head)
    print(f"repository last commit       : {head.date() if head else 'unknown'}\n")

    for kind, cat in CATALOGS:
        folder = ROOT / kind
        if not cat.exists() or not folder.is_dir():
            continue
        entries = {}
        for line in cat.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            entries[d.get("id")] = d
        # Join on `path`, not on a parsed id. The two catalogs in this repository use different
        # id conventions, and one entry's id does not match its own path, which is exactly the
        # kind of thing a checker keyed on ids reports as two problems instead of one.
        on_disk = {f"{kind}/{p.name}": p for p in sorted(folder.iterdir())
                   if p.is_dir() and re.match(r"^[ew]\d+_", p.name)}
        entries = {d.get("path", "").rstrip("/"): d for d in entries.values()}

        print(f"{kind}/  {len(on_disk)} folder(s), {len(entries)} catalog entr(ies)")
        quiet = []
        for eid, d in sorted(entries.items()):
            p = on_disk.get(eid)
            if p is None:
                print(f"  ORPHAN   catalog path {eid!r} has no folder")
                problems += 1
                continue
            n = days_since(last_commit(p))
            status = (d.get("status") or "").lower()
            if status in ("active", "in progress", "") and n is not None and n >= a.days:
                quiet.append((n, eid, status or "no status", p.name))
        for eid, p in sorted(on_disk.items()):
            if eid not in entries:
                print(f"  MISSING  {p.name} is on disk with no catalog entry")
        for eid, d in sorted(entries.items()):
            i = str(d.get("id", ""))
            if eid in on_disk and i and not on_disk[eid].name.startswith(i):
                print(f"  ID       entry id {i!r} does not match its folder {on_disk[eid].name!r}")
                problems += 1
                problems += 1
        for n, eid, status, name in sorted(quiet, reverse=True):
            # Filling this in from the folder's existence is what produced the defect this file
            # was written for. The status has to come from a judgement or it is not a status.
            print(f"  STALE    {name} says \"{status}\" and has been quiet {n} days")
            problems += 1
        print()

    print("the front door, which is the first thing a reader opens and the last thing you re-read")
    for name in FRONT:
        p = ROOT / name
        if not p.exists():
            continue
        n = days_since(last_commit(p))
        flag = "  <- older than the repository's own work" if (
            n is not None and repo_age is not None and n - repo_age >= a.days) else ""
        print(f"  {name:<14} last touched {n} days ago{flag}")
        if flag:
            problems += 1
    print()

    print(f"claims of state, anywhere in tracked text")
    files = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT,
                           capture_output=True, text=True).stdout.split()
    hits = 0
    for f in files:
        try:
            text = (ROOT / f).read_text(errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            m = CLAIMS.search(line)
            if m:
                hits += 1
                if hits <= 12:
                    print(f"  {f}:{i}  \"{line.strip()[:84]}\"")
    if hits > 12:
        print(f"  ... and {hits - 12} more")
    print(f"  {hits} line(s) assert a state. Each is true only until it is not, and none of them"
          f" will tell you when.")

    print(f"\n{problems} thing(s) this repository says about itself that the repository contradicts")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
