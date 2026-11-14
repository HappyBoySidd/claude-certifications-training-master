#!/usr/bin/env python3
"""B63-FX-7 computed coverage report for the 30 CCAR-F objective pages. No third-party packages.

    python3 tools/coverage_report.py --src "<study source>" [--out 10-Learning-Site/OBJECTIVE-COVERAGE-REPORT.md]

Per objective: official bullets (exam guide) vs mapped bullets (coverage checklist rows), manifest anchors
missing from the built HTML, explicit legacy <a id> anchors in the source that survive in the built HTML,
and H2 sections without a role tag. Exit 1 on any gap.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import objective_check as oc

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); ap.add_argument("--out")
    a = ap.parse_args(); src = Path(a.src)
    guide = oc.guide_objectives((src / oc.GUIDE).read_text(encoding="utf-8"))
    manifest = json.loads((oc.REPO / "tools/objective-manifest.json").read_text(encoding="utf-8"))["objectives"]
    rows, T = [], dict(off=0, mapped=0, man=0, man_miss=0, leg=0, leg_miss=0, h2=0, h2_untagged=0)
    for n in sorted(guide):
        md = (src / oc.OBJ_DIR / f"objective-{n}.md").read_text(encoding="utf-8")
        page = oc.DOCS_OBJ / f"objective-{n}.html"
        h = page.read_text(encoding="utf-8") if page.exists() else ""
        ids = set(re.findall(r'\bid="([^"]+)"', h))
        off = set(guide[n]["text"])
        cov = re.search(r"^## Coverage checklist\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
        mapped = {m[0] for m in re.findall(rf"^\| ({re.escape(n)}-[KS]\d+)\b([^|]*)\| (.+?) \|\s*$", cov.group(1), re.M)} if cov else set()
        man = {x["anchor"] for v in manifest.get(n, {}).get("bullets", {}).values() for x in v}
        man_miss = sorted(x for x in man if x not in ids)
        legacy = set(re.findall(r'<a id="([^"]+)"></a>', md))
        leg_miss = sorted(x for x in legacy if x not in ids)
        h2 = re.findall(r"<h2\b[^>]*>", h); untag = [x for x in h2 if 'class="role role-' not in x]
        rows.append((n, len(off), len(off & mapped), len(off - mapped) + len(mapped - off), len(man), len(man_miss),
                     len(legacy), len(leg_miss), len(h2), len(untag), man_miss + leg_miss))
        for k, v in zip(("off", "mapped", "man", "man_miss", "leg", "leg_miss", "h2", "h2_untagged"),
                        (len(off), len(off & mapped), len(man), len(man_miss), len(legacy), len(leg_miss), len(h2), len(untag))):
            T[k] += v
    bad = T["mapped"] != T["off"] or T["man_miss"] or T["leg_miss"] or T["h2_untagged"] or any(r[3] for r in rows)
    out = ["# Objective coverage report (computed by tools/coverage_report.py)", "",
           "| Obj | Official bullets | Mapped | Mismatch | Manifest anchors | Missing in HTML | Legacy anchors | Legacy missing | H2s | H2 no role |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    out += ["| " + " | ".join(str(c) for c in r[:10]) + " |" for r in rows]
    out += ["", f"**Totals:** {len(rows)} objectives; official bullets {T['off']}; mapped {T['mapped']}; manifest anchors {T['man']} "
            f"(missing from built HTML {T['man_miss']}); legacy anchors {T['leg']} (missing {T['leg_miss']}); "
            f"H2 sections {T['h2']} (without role tag {T['h2_untagged']}).", "", "**Result:** " + ("GAPS" if bad else "no gaps")]
    for r in rows:
        if r[10]: out.append(f"- {r[0]} missing anchors: {r[10]}")
    txt = "\n".join(out) + "\n"
    print(txt)
    if a.out: Path(a.out).write_text(txt, encoding="utf-8")
    return 1 if bad else 0
if __name__ == "__main__": sys.exit(main())
