#!/usr/bin/env python3
"""Is literature/ a bijection with bibliography.jsonl?

Why this exists
---------------
In the project this came from, the index was found holding 52 of 65 folders, with three ids used
twice and thirteen papers absent. Among the absent were the four baselines the paper compared
itself against. The failure was silent in both directions: a folder can sit on disk unindexed,
and the fetch tool minted the next id from the INDEX, so it handed out ids that already existed
on disk. Nothing in the repository would have said so, and nothing did, for a long time.

A library you cannot enumerate is a library you will cite from memory.

    python3 tools/lit_index.py          # exits 1 on any violation

Checks, each of which had a real instance behind it:
  1. no id is used by two folders
  2. every folder appears in bibliography.jsonl
  3. every entry's path exists              (a rename breaks this)
  4. every entry's id matches its folder    (a hand-edit breaks this)
  5. bib keys are unique                    (two entries for one paper is a silent duplicate)
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "literature"
# This template's ids are five digits (b00001). Change WIDTH if yours differ; everything else
# follows from it, which is the point of keeping the shape in one constant.
WIDTH = 5
PAT = re.compile(r"^b\d{%d}_" % WIDTH)

disk = defaultdict(list)
for d in LIB.rglob("b" + "[0-9]" * WIDTH + "_*"):
    if d.is_dir() and PAT.match(d.name):
        disk[d.name[:WIDTH + 1]].append(d.relative_to(ROOT).as_posix())

recs = [json.loads(l) for l in (LIB / "bibliography.jsonl").read_text().splitlines() if l.strip()]
idx = {r["id"]: r for r in recs}

bad = []
for i, paths in sorted(disk.items()):
    if len(paths) > 1:
        bad.append(f"id {i} used by {len(paths)} folders: {', '.join(paths)}")
for i in sorted(set(disk) - set(idx)):
    bad.append(f"{i} on disk but not in bibliography.jsonl ({disk[i][0]})")
for r in recs:
    # A work cited but not held is legitimate: books, paywalled journals, anything you verified
    # against a catalogue instead of downloading. It carries source_type "metadata_only" and a
    # `verified_against` field naming what was checked, and it is not a folder, so skip it here.
    # citecheck.py is what counts these and insists the verification is named.
    if r.get("source_type") == "metadata_only":
        if not r.get("verified_against"):
            bad.append(f"{r['id']} is metadata_only with no verified_against: "
                       f"name the catalogue it was checked against, or hold a copy")
        continue
    p = ROOT / r["path"]
    if not p.is_dir():
        bad.append(f"{r['id']} indexed at a path that does not exist: {r['path']}")
    elif not p.name.startswith(r["id"] + "_"):
        bad.append(f"{r['id']} indexed at a folder named {p.name}")
keys = defaultdict(list)
for r in recs:
    keys[r["bib_key"]].append(r["id"])
for k, ids in sorted(keys.items()):
    if len(ids) > 1:
        bad.append(f"bibkey {k} used by {', '.join(ids)}")

print(f"{len(disk)} folders on disk, {len(recs)} indexed")
if bad:
    print(f"\n{len(bad)} violation(s):")
    for b in bad:
        print("  " + b)
    sys.exit(1)
print("bijection holds")
