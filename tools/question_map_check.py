#!/usr/bin/env python3
"""Check the CCAR-F question-to-objective map (B63-FX-13). No third-party packages.

    python3 tools/question_map_check.py           # prints totals; exit 1 and FAIL lines on a problem

Every CCAR-F question in practice/question-bank.json must appear in tools/question-objective-map.json
exactly once, as `mapped` (one or more objective IDs that exist in tools/objective-manifest.json, with
a confidence of `clear` or `uncertain`) or `unmapped` (no objective IDs). Totals must reconcile: the
bank count equals mapped plus unmapped, and per-domain counts add up. A question mapped to two
objectives counts once in the bank total and once under each objective (the per-objective sum can be
larger than the bank; that is reported, not hidden). Zero-question objectives are listed.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BANK = REPO / "practice/question-bank.json"
MAP = REPO / "tools/question-objective-map.json"
MANIFEST = REPO / "tools/objective-manifest.json"


def load():
    bank = [q for q in json.loads(BANK.read_text())["questions"] if q["exam"] == "CCAR-F"]
    qmap = json.loads(MAP.read_text())
    objectives = list(json.loads(MANIFEST.read_text())["objectives"])
    return bank, qmap, objectives


def summarize(bank, qmap, objectives):
    """Return (fails, totals). totals is reused by the site build so both report the same numbers."""
    fails: list[str] = []
    rows = qmap["questions"]
    ids = [q["id"] for q in bank]
    for qid in sorted(set(ids) - set(rows)):
        fails.append(f"{qid}: in the bank but not in the map (mark it mapped or unmapped)")
    for qid in sorted(set(rows) - set(ids)):
        fails.append(f"{qid}: in the map but not in the shareable CCAR-F bank")
    if len(ids) != len(set(ids)):
        fails.append("duplicate question ids in the bank")
    per_obj = {o: Counter() for o in objectives}
    status = Counter()
    by_domain: dict[str, Counter] = {}
    domain_of = {q["id"]: q["domain"] for q in bank}
    for qid, r in rows.items():
        if qid not in domain_of:
            continue
        objs, st, conf = r.get("objectives", []), r.get("status"), r.get("confidence")
        if r.get("domain") != domain_of[qid]:
            fails.append(f"{qid}: map domain {r.get('domain')!r} differs from bank domain {domain_of[qid]!r}")
        if st == "mapped":
            if not objs or conf not in ("clear", "uncertain"):
                fails.append(f"{qid}: mapped needs objective IDs and confidence clear or uncertain")
        elif st == "unmapped":
            if objs or conf is not None:
                fails.append(f"{qid}: unmapped must have no objectives and no confidence")
        else:
            fails.append(f"{qid}: status {st!r} is not mapped or unmapped")
        if not r.get("note"):
            fails.append(f"{qid}: no note saying why")
        for o in objs:
            if o not in per_obj:
                fails.append(f"{qid}: objective {o} is not in the CCAR-F manifest")
                continue
            per_obj[o][conf] += 1
        key = "unmapped" if st == "unmapped" else conf
        status[key] += 1
        by_domain.setdefault(domain_of[qid], Counter())[key] += 1
    if sum(status.values()) != len(set(ids) & set(rows)):
        fails.append("status totals do not add up to the bank")
    if sum(sum(c.values()) for c in by_domain.values()) != sum(status.values()):
        fails.append("domain totals do not add up to the bank")
    totals = dict(bank=len(ids), status=status, by_domain=by_domain, per_obj=per_obj,
                  zero=[o for o, c in per_obj.items() if not c],
                  clear_only_zero=[o for o, c in per_obj.items() if not c["clear"]],
                  multi=sum(1 for r in rows.values() if len(r.get("objectives", [])) > 1),
                  reviewed=qmap.get("review", {}).get("independent_check"))
    return fails, totals


def main():
    fails, t = summarize(*load())
    for f in fails:
        print("FAIL", f)
    s = t["status"]
    print(f"question map: {t['bank']} CCAR-F questions = {s['clear']} clear + {s['uncertain']} uncertain + "
          f"{s['unmapped']} unmapped; {t['multi']} map to two objectives; "
          f"{len(t['zero'])} of {len(t['per_obj'])} objectives have no question; "
          f"independent check: {t['reviewed'] or 'not yet'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
