#!/usr/bin/env python3
"""Check arXiv ids against the real titles BEFORE downloading anything.

A wrong id does not fail. It silently fetches a different paper, which is worse than failing: the
folder, the index, and eventually a citation would all be confidently wrong, and each step would
look like it had worked. This queries the arXiv API for each id and prints a match verdict, so a
mistyped id is caught while it is still cheap to fix.

The general form of the lesson: when a wrong input produces a plausible output instead of an
error, put the check before the work, not after it.

    python3 tools/verify_arxiv.py manifest.jsonl

where the manifest has one JSON object per line with at least `arxiv` and `title`.
"""
import json, re, sys, time, urllib.request, urllib.parse
from difflib import SequenceMatcher

UA = "research-literature-verify/1.0 (academic use)"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def meta(arxiv):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": arxiv, "max_results": 1})
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                timeout=60) as r:
        x = r.read().decode()
    t = re.search(r"<entry>.*?<title>(.*?)</title>", x, re.S)
    a = re.findall(r"<author>\s*<name>(.*?)</name>", x, re.S)
    y = re.search(r"<published>(\d{4})", x)
    if not t:
        return None
    return dict(title=re.sub(r"\s+", " ", t.group(1)).strip(),
                authors=a, year=int(y.group(1)) if y else None)


bad = 0
for line in open(sys.argv[1]):
    if not line.strip():
        continue
    e = json.loads(line)
    m = meta(e["arxiv"])
    if m is None:
        print(f"  NOT FOUND  {e['arxiv']}  (claimed: {e['title'][:60]})"); bad += 1
    else:
        r = SequenceMatcher(None, norm(e["title"]), norm(m["title"])).ratio()
        tag = "ok      " if r > 0.75 else "MISMATCH"
        if r <= 0.75:
            bad += 1
        print(f"  {tag} {e['arxiv']}  {r:.2f}  real: {m['title'][:78]}")
        if e.get("authors") == "unverified" and m["authors"]:
            print(f"           -> authors: {', '.join(m['authors'][:4])}"
                  f"{' et al.' if len(m['authors']) > 4 else ''}  ({m['year']})")
    time.sleep(3)
print(f"\n{bad} problem(s)")
sys.exit(1 if bad else 0)
