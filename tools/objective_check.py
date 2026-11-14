#!/usr/bin/env python3
"""B63-FX-7 objective presentation and coverage check for CCAR-F. No third-party packages.

    python3 tools/objective_check.py --src "<study source>"            # check only
    python3 tools/objective_check.py --src "<study source>" --manifest tools/objective-manifest.json

Source Markdown is canonical. For each objective-N.N.md it checks:
  1. presentation: H1 "Objective N.N — topic", Exam/Domain line, Time, Prerequisites, Continue from,
     Official task statement equal to the exam-guide wording in CCAR-F-objectives.md;
  2. coverage: the coverage checklist lists exactly the guide's Knowledge (K1..Kn) and Skills (S1..Sm)
     bullets, in order, none dropped and none invented;
  3. each mapped bullet links to an anchor that exists in the page and is a teaching section
     (not the checklist, Try it, Done when or Sources);
  4. built HTML (docs/) agrees: breadcrumb ends "Domain N / Objective N.N" and <title>/H1 match.
It also writes the bullet-to-section manifest (stable IDs) when --manifest is given. A heading-shape
lint does not close FX-7 alone; accuracy review still owns changed facts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OBJ_DIR = "02-Lessons/02-CCAR-F-Architect-Foundations/objectives"
GUIDE = "01-Curriculum/02-Architect-Track/CCAR-F-objectives.md"
DOCS_OBJ = REPO / "docs/lessons/ccar-f/objectives"
NON_TEACHING = re.compile(r"^(?:coverage checklist|try it|done when|sources|expected output)", re.I)


def slugify(text: str) -> str:  # mirrors site/build.py slugify
    t = re.sub(r"<[^>]+>", "", text).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t, flags=re.U)
    return t.replace(" ", "-")


def guide_weights(text: str) -> dict:
    return {m.group(1): m.group(2) for m in re.finditer(r"^## Domain (\d):.*?(\d+)%\s*$", text, re.M)}


def guide_objectives(text: str) -> dict:
    out = {}
    for m in re.finditer(r"^### (\d\.\d)\s*$(.*?)(?=^### \d\.\d\s*$|^## |\Z)", text, re.M | re.S):
        n, body = m.group(1), m.group(2)
        ts = re.search(r"Task Statement \d\.\d: (.+)", body)
        k = re.search(r"Knowledge of:\s*\n((?:- .*\n?)+)", body)
        s = re.search(r"Skills in:\s*\n((?:- .*\n?)+)", body)
        items = lambda g: [x.strip() for x in re.findall(r"^- (.+)$", g.group(1), re.M)] if g else []
        ki, si = items(k), items(s)
        out[n] = {"task": ts.group(1).strip() if ts else None, "k": len(ki), "s": len(si),
                  "text": dict([(f"{n}-K{i}", t) for i, t in enumerate(ki, 1)] + [(f"{n}-S{i}", t) for i, t in enumerate(si, 1)])}
    return out


def anchors(md: str) -> dict:
    """anchor id -> heading text of the section it starts."""
    ids, lines = {}, md.split("\n")
    for i, line in enumerate(lines):
        for a in re.findall(r'<a id="([^"]+)"></a>', line):
            nxt = next((l for l in lines[i + 1:i + 3] if l.startswith("#")), line)
            ids[a] = nxt.lstrip("# ").strip()
        h = re.match(r"#{1,6} (.+)", line)
        if h:
            ids.setdefault(slugify(h.group(1)), h.group(1).strip())
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--manifest")
    a = ap.parse_args()
    src = Path(a.src)
    gtext = (src / GUIDE).read_text(encoding="utf-8")
    guide, weights = guide_objectives(gtext), guide_weights(gtext)
    text_checked = id_only = role_ok = role_missing = 0
    fails, manifest = [], {"exam": "CCAR-F", "source": GUIDE, "objectives": {}}
    files = sorted((src / OBJ_DIR).glob("objective-*.md"))
    if len(files) != 30:
        fails.append(f"expected 30 objective files, found {len(files)}")
    for f in files:
        n = re.search(r"objective-(\d\.\d)\.md$", f.name).group(1)
        md = f.read_text(encoding="utf-8")
        g = guide.get(n)
        err = lambda m: fails.append(f"{n}: {m}")
        if not g:
            err("not in guide")
            continue
        h1 = md.split("\n", 1)[0]
        if not re.fullmatch(rf"# Objective {re.escape(n)} — \S.+", h1):
            err(f"H1 not 'Objective {n} — topic': {h1[:80]}")
        d = n[0]
        for label, rx in [("exam/domain", rf"^(?:<!-- /site:hide -->)?\*\*Exam:\*\* CCAR-F · \*\*Domain {d}:\*\* \d+% of exam"),
                          ("time", r"^\*\*Time:\*\* \S"), ("prerequisites", r"^\*\*Prerequisites:\*\* \S"),
                          ("continue from", r"^\*\*Continue from:\*\* \[Domain lesson\]\(.+\) · \[Objective map\]"),
                          ("task statement", r"^\*\*Official task statement:\*\* (.+?)\s*$")]:
            m = re.search(rx, md, re.M)
            if not m:
                err(f"missing {label} line")
            elif label == "exam/domain":
                w = re.search(r"(\d+)% of exam", m.group(0)).group(1)
                if w != weights.get(d):
                    err(f"domain weight {w}% differs from guide {weights.get(d)}%")
            elif label == "task statement" and m.group(1).strip() != g["task"]:
                err(f"task statement differs from guide: {m.group(1)[:60]!r}")
        cov = re.search(r"^## Coverage checklist\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
        if not cov:
            err("no coverage checklist")
            continue
        full = re.findall(rf"^\| ({re.escape(n)}-[KS]\d+)\b([^|]*)\| (.+?) \|\s*$", cov.group(1), re.M)
        rows = [(b, c) for b, _, c in full]
        for bid, rest, _ in full:  # where the row quotes the bullet text, it must match the guide word for word
            quoted = rest.strip().lstrip(":").strip()
            if not quoted:
                id_only += 1
            elif quoted != g["text"].get(bid):
                err(f"{bid} text differs from guide: {quoted[:60]!r}")
            else:
                text_checked += 1
        want = [f"{n}-K{i}" for i in range(1, g["k"] + 1)] + [f"{n}-S{i}" for i in range(1, g["s"] + 1)]
        got = [r[0] for r in rows]
        if got != want:
            err(f"coverage IDs {got} != guide {want}")
        ids = anchors(md)
        entry = {"title": h1[2:], "task": g["task"], "bullets": {}}
        for bid, cell in rows:
            links = re.findall(r"\]\(#([^)]+)\)", cell)
            if not links:
                err(f"{bid} has no section link")
            for lk in links:
                if lk not in ids:
                    err(f"{bid} -> #{lk} not found in page")
                elif NON_TEACHING.search(ids[lk]):
                    err(f"{bid} -> #{lk} is not a teaching section ({ids[lk]})")
            entry["bullets"][bid] = [{"anchor": lk, "section": ids.get(lk)} for lk in links]
        manifest["objectives"][n] = entry
        page = DOCS_OBJ / f"objective-{n}.html"
        if page.exists():
            h = page.read_text(encoding="utf-8")
            crumb = re.search(r'<nav class="crumbs".*?</nav>', h, re.S)
            if not crumb or not re.search(rf">Domain {d}</a><span aria-hidden=\"true\"> / </span><span>Objective {re.escape(n)}</span></nav>", crumb.group(0)):
                err("breadcrumb does not end Domain / Objective")
            t = re.search(r"<title>(.*?) · ", h)
            if not t or not t.group(1).startswith(f"Objective {n} — "):
                err("HTML title does not match H1 pattern")
            # role lint: every H2 carries a role tag (Explanation/Exercise/Answer/Done when); no exemptions needed
            for h2 in re.findall(r"<h2\b[^>]*>", h):
                if 'class="role role-' not in h2:
                    err(f"H2 without role tag: {h2[:80]}")
                    role_missing += 1
                else:
                    role_ok += 1
        else:
            err("built page missing (run site/build.py first)")
    if a.manifest:
        Path(a.manifest).write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for x in fails:
        print("FAIL", x)
    nb = sum(len(o["bullets"]) for o in manifest["objectives"].values())
    print(f"objective_check: {len(files)} objectives, {nb} mapped bullets ({text_checked} text-matched to guide, "
          f"{id_only} ID-only rows), H2 role tags {role_ok} ok / {role_missing} missing, {len(fails)} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
