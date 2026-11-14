#!/usr/bin/env python3
"""Hash the private colleague-names file into tools/blocklist.sha256 (names never enter the repo).

    python3 tools/make_blocklist.py --src "<study workspace path>"
"""
import argparse
import hashlib
import os
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("--src", default=os.environ.get("CERT_SRC"))
arg = ap.parse_args().src
if not arg:
    sys.exit("make_blocklist: pass --src or set CERT_SRC to the study workspace path")
src = Path(arg).expanduser()
names, allowed = [], False
for line in (src / "10-Learning-Site/private/names.txt").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if line.startswith("allowed:"):
        allowed = True
        continue
    if not allowed:
        names.append(line.removeprefix("first:"))
def words_of(text):
    folded = "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))
    return re.findall(r"[^\W\d_]+", folded)


hashes = sorted({hashlib.sha256(" ".join(words_of(n)).encode()).hexdigest() for n in names if words_of(n)})
(REPO / "tools/blocklist.sha256").write_text("# SHA-256 of blocked colleague names, lowercased. Regenerate with tools/make_blocklist.py\n" + "\n".join(hashes) + "\n")
print(f"{len(hashes)} hashes written")
