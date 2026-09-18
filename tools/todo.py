#!/usr/bin/env python3
"""The open-debt list, read aloud so that it is read at all.

Why this is not just a file
---------------------------
The project this came from kept its debts in prose, in a log it wrote diligently and read never.
Three of them were found still open after hundreds of work units: a directory recorded at 492 MB
that had grown to 716 MB, a reframing named as "the next thing" twice and started zero times, and
a section called the next item and then abandoned mid-sentence. Every one had been written down.
Writing them down was never the failure.

What changed was that `lookback.py` prints this list, and `commit.py` refuses a sixth unit
without a lookback. The debts are now spoken on a schedule nobody has to remember. Items older
than 100 units are marked, because those are the ones that die quietly.

Closed lines stay in the file. An item dropped on purpose is evidence, and an item that keeps
reopening is a finding.

    python3 tools/todo.py                # open items, oldest debt first
    python3 tools/todo.py --all          # closed ones too
    python3 tools/todo.py --close t01    # mark closed at the current unit

TODO.md format:  `- [ ] (id) owner | opened #N | what it is`

`owner: user` means it is not yours to start. List it anyway. An item nobody can start and
nobody can see is worse than one blocked in the open.
"""
import argparse, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODO = ROOT / "TODO.md"
LINE = re.compile(r"^- \[(?P<done>[ x])\] \((?P<id>t\d+)\) (?P<owner>\w+) \| opened #(?P<open>~?\d+)"
                  r"(?: \| closed #(?P<closed>~?\d+))? \| (?P<what>.*)$")


def current_cycle():
    log = subprocess.run(["git", "log", "-40", "--format=%b"], capture_output=True, text=True,
                         cwd=ROOT).stdout
    m = re.search(r"^Cycle: #(\d+)", log, re.M)
    return int(m.group(1)) if m else 0


def items():
    if not TODO.exists():
        return []
    out = []
    section = ""
    for line in TODO.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        m = LINE.match(line)
        if m:
            d = m.groupdict()
            d["section"] = section
            d["raw"] = line
            out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--close", metavar="ID")
    a = ap.parse_args()
    cyc = current_cycle()

    if a.close:
        text = TODO.read_text()
        hit = [i for i in items() if i["id"] == a.close]
        if not hit:
            sys.exit(f"no item {a.close} in TODO.md")
        it = hit[0]
        if it["done"] == "x":
            sys.exit(f"{a.close} is already closed")
        new = it["raw"].replace("- [ ]", "- [x]", 1)
        new = new.replace(f"| opened #{it['open']} |", f"| opened #{it['open']} | closed #{cyc} |", 1)
        TODO.write_text(text.replace(it["raw"], new, 1))
        print(f"closed {a.close} at #{cyc}: {it['what'][:70]}")
        return 0

    rows = items()
    open_rows = [i for i in rows if i["done"] == " "]
    show = rows if a.all else open_rows
    if not show:
        print("TODO.md: nothing open")
        return 0

    def age(i):
        return cyc - int(str(i["open"]).lstrip("~")) if cyc else 0

    # Oldest first, because the debts that rot here are the ones that were never loud.
    for i in sorted(show, key=age, reverse=True):
        mark = "x" if i["done"] == "x" else " "
        tag = "!!" if age(i) > 100 and mark == " " else "  "
        who = "" if i["owner"] == "me" else f"[{i['owner']}] "
        print(f"{tag} [{mark}] {i['id']}  {age(i):>4} cycles  {who}{i['what'][:96]}")
    mine = sum(1 for i in open_rows if i["owner"] == "me")
    stale = sum(1 for i in open_rows if age(i) > 100)
    print(f"\n{len(open_rows)} open, {mine} mine, {stale} older than 100 cycles"
          + ("   <- these are the ones that die quietly" if stale else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
