#!/usr/bin/env python3
"""Build the preserved practice tool and publish the same app under docs/practice/.

    python3 tools/build_practice.py --src "<study workspace path>"   # refresh the bank from the workspace
    python3 tools/build_practice.py                                  # rebuild practice/index.html from practice/

Only questions whose licence allows sharing are copied: Anthropic's published sample questions
and Amey Thakur's MIT-licensed repo (licence file kept). Items the accuracy spot-check marked
wrong are listed in EXCLUDE and left out; items it corrected are in FIXES. No third-party packages.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "practice"
BANK = OUT / "question-bank.json"
TEMPLATE = OUT / "src" / "template.html"
AMEY_LICENCE = "08-Reference/00-All-Exams-Shared/amey-thakur-CLAUDE-CERTIFICATIONS/LICENSE"

ALLOWED_SOURCES = ("Anthropic official exam guide", "Amey Thakur CLAUDE-CERTIFICATIONS repo")
EXCLUDE: dict[str, str] = {
    "amey-developer-foundations-mock2-10": "keyed answer puts an iteration cap ahead of stop_reason, "
    "which the CCAR-F exam guide names as an anti-pattern (G4, S-16)",
}
FIXES: dict[str, dict] = {
    "amey-associate-foundations-practice-5": {
        "answer": ["B"],
        "rationale_prefix": "**A** ",
    },
    "amey-architect-foundations-practice-23": {
        "rationale_suffix": " Note: forced tool use alone does not guarantee schema compliance; "
        "Anthropic's structured outputs (a JSON-schema output format, or strict tool use with "
        "`strict: true`) is what makes the output always match the schema.",
    },
}
PUBLIC_COPY = (
    ("<b>Official course</b> means copied from the Partner Academy prep course, but the answers "
     "were worked out by the person who copied them.\n", ""),
    ("<b>Community</b> means written by coworkers or open-source authors.",
     "<b>Community</b> means written by open-source authors: Amey Thakur's questions are Copyright (c) 2026 "
     "Amey Thakur, shared under the MIT licence (full notice in this file's source)."),
    ('const TIER_LABEL = {1: "Official", 2: "Official course (reasoned answers)", 3: "Community", 4: "Project-authored (written by us)"};',
     'const TIER_LABEL = {1: "Official (Anthropic)", 2: "Community (Tier 2, MIT licence)", 3: "Other community", 4: "Project-authored (written by us)"};'),
)


def allowed(q: dict) -> bool:
    return (q["source"].startswith(ALLOWED_SOURCES) or q.get("origin") == "project-authored") and q["id"] not in EXCLUDE


def fix(q: dict) -> dict:
    q = dict(q)
    if q["source"].startswith(ALLOWED_SOURCES[0]):
        q["source"] = f"Anthropic official exam guide v1.0 for {q['exam']} (sample question)"
    else:
        q["tier"] = 2
    f = FIXES.get(q["id"])
    if not f:
        return q
    if "answer" in f:
        q["answer"] = f["answer"] if isinstance(q["answer"], list) else f["answer"][0]
    q["rationale"] = f.get("rationale_prefix", "") + q["rationale"] + f.get("rationale_suffix", "")
    return q


def export(src: Path):
    """Refresh only eligible source records, preserving legacy data and approved originals."""
    tool = src / "05-Practice-Tool" / "build"
    data = json.loads((tool / "questions.json").read_text())
    register = json.loads((tool / "bank-sources.json").read_text())
    eligible = [row for row in register["sources"] if row.get("exam") == "CCAR-F" and row.get("origin") == "project-authored" and row.get("status") == "approved" and all(str(row.get("gates", {}).get(g, "")).lower() == "pass" for g in ("G3", "G4", "G6", "G12"))]
    approved_ids = set()
    for row in eligible:
        raw = json.loads((tool / row["file"]).read_text())
        items = raw if isinstance(raw, list) else raw.get("questions", [])
        approved_ids.update(q["id"] for q in items)
    projects = [q for q in data["questions"] if q["id"] in approved_ids and q.get("origin") == "project-authored"]
    OUT.mkdir(exist_ok=True)
    (OUT / "project-authored-originals.json").write_text(json.dumps({"questions": projects, "eligibility": eligible}, ensure_ascii=False, indent=1) + "\n")
    # Existing released licensed records remain unchanged, including original answer identities.
    legacy = OUT / "legacy-question-bank.json"
    if not legacy.exists():
        if BANK.exists():
            shutil.copyfile(BANK, legacy)
        else:
            legacy.write_text(json.dumps({"exams": data["exams"], "questions": [fix(q) for q in data["questions"] if q["source"].startswith(ALLOWED_SOURCES) and allowed(q)]}, ensure_ascii=False, indent=1))
    print(f"practice source intake: {len(projects)} project-authored records from approved register rows")


def assemble():
    legacy = OUT / "legacy-question-bank.json"
    if not legacy.exists():
        shutil.copyfile(BANK, legacy)
    data = json.loads(legacy.read_text())
    original_ids = {q["id"] for q in data["questions"]}
    project_file = OUT / "project-authored-originals.json"
    if project_file.exists():
        for q in json.loads(project_file.read_text())["questions"]:
            if q["id"] not in original_ids:
                data["questions"].append(q)
                original_ids.add(q["id"])
    variant_file = REPO / "assessment" / "ccarf-variant-items.json"
    review_file = REPO / "assessment" / "variant-review.json"
    if variant_file.exists() and review_file.exists():
        reviewed = json.loads(review_file.read_text())
        approved = set(reviewed.get("approved_ids", []))
        raw = json.loads(variant_file.read_text())
        for q in (raw if isinstance(raw, list) else raw["questions"]):
            if q["id"] in approved and q["id"] not in original_ids:
                expected = reviewed.get("items", {}).get(q["id"], {}).get("content_sha256")
                actual = hashlib.sha256(json.dumps(q, sort_keys=True).encode()).hexdigest()
                if not expected or expected != actual:
                    sys.exit("build_practice: approved variant changed after review: " + q["id"])
                # Canonical adapter does not rewrite original teaching/answers.
                q = dict(q)
                q["origin"] = "project-authored"
                q["origin_tier"] = 4
                q["review_status"] = "approved"
                data["questions"].append(q)
                original_ids.add(q["id"])
    review_path = REPO / "assessment" / "canonical-item-review.json"
    data["reviewMap"] = json.loads(review_path.read_text()).get("items", {}) if review_path.exists() else {}
    for q in data["questions"]:
        r = data["reviewMap"].get(q["id"])
        if r and r.get("content_sha256") != hashlib.sha256(json.dumps(q, sort_keys=True).encode()).hexdigest():
            sys.exit("build_practice: canonical original changed after review: " + q["id"])
    # A content-derived revision lets existing resume logic recognize bank changes without resetting IDs/history.
    data["version"] = "ccarf-bank-" + hashlib.sha256(json.dumps(data["questions"], sort_keys=True).encode()).hexdigest()[:12]
    mapping_file = REPO / "tools" / "question-objective-map.json"
    data["objectiveMap"] = json.loads(mapping_file.read_text()).get("questions", {}) if mapping_file.exists() else {}
    BANK.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    return data


def build(site_out: Path | None = None):
    for need in (BANK, TEMPLATE, OUT / "LICENSE-amey-thakur.txt"):
        if not need.exists():
            sys.exit(f"build_practice: {need} not found; run once with --src <study workspace>")
    data = assemble()
    bad = [q["id"] for q in data["questions"] if not allowed(q)]
    if bad:
        sys.exit(f"build_practice: {len(bad)} question(s) from a source we may not share, e.g. {bad[0]}")
    bridge_file=REPO/'content/02-Lessons/02-CCAR-F-Architect-Foundations/technical-objective-bridges.json'
    data['technicalBridges']=json.loads(bridge_file.read_text())['objectives'] if bridge_file.exists() else {}
    # Runtime teaching is attached only after assemble() has written the unchanged bank.
    # Base-question fixtures belong to their authored lesson, not arbitrary questions
    # that happen to share an objective. Ship only explicitly separate companions
    # and conditional implementation extensions to this post-answer repair panel.
    pattern_file = REPO / 'content/02-Lessons/02-CCAR-F-Architect-Foundations/objective-learning-patterns.json'
    patterns = json.loads(pattern_file.read_text()).get('objectives', {}) if pattern_file.exists() else {}
    # Descriptive selection labels are runtime metadata, never question-bank records.
    data['objectiveNames'] = {}
    for objective in patterns:
        lesson = pattern_file.parent / 'objectives' / f'objective-{objective}.md'
        if lesson.exists():
            heading = lesson.read_text().splitlines()[0]
            title = heading.split(' — ', 1)[-1].lstrip('# ').strip()
            if title and title != heading:
                data['objectiveNames'][objective] = title
    if patterns and set(data['objectiveNames']) != set(patterns):
        sys.exit('build_practice: objective selection names missing from authored lesson headings')
    data['learningPatterns'] = {
        objective: {
            'companion': pattern['companion'],
            'course_applications': [row for row in pattern.get('course_applications', [])
                                    if row.get('fixture_scope') in ('companion-example', 'extension')],
            'technical_terms': pattern.get('technical_terms', []),
            'technical_reference_url': pattern.get('technical_reference_url', ''),
        }
        for objective, pattern in patterns.items()
        if pattern.get('companion', {}).get('fixture_scope') == 'companion-example'
    }
    template = TEMPLATE.read_text()
    if "Partner Academy" in template or "coworkers" in template:
        sys.exit("build_practice: template still describes course or coworker questions")
    if "/*__DATA__*/null" not in template:
        sys.exit("build_practice: template has no /*__DATA__*/null placeholder")
    if not template.startswith("<!DOCTYPE html>\n"):
        sys.exit("build_practice: template must start with <!DOCTYPE html>")
    licence = (OUT / "LICENSE-amey-thakur.txt").read_text().replace("--", "- -").strip()
    notice = ("<!--\nCommunity questions in this file come from Amey Thakur's CLAUDE-CERTIFICATIONS repo\n"
              "(https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS), under this licence:\n\n" + licence + "\n-->\n")
    page = template.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + notice, 1)
    (OUT / "index.html").write_text(page.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False)))
    site_out = site_out or (REPO / "docs")
    served = site_out / "practice"
    served.mkdir(parents=True, exist_ok=True)
    for filename in ("question-bank.json", "LICENSE-amey-thakur.txt"):
        shutil.copyfile(OUT / filename, served / filename)
    # Hosted UI stays small and loads a bundled same-origin script. Offline export remains one file.
    hosted = page.replace("/*__DATA__*/null", "window.CCT_PRACTICE_DATA")
    hosted = hosted.replace("</head>", '<link rel="stylesheet" href="../assets/site.css"><script src="question-bank.js"></script></head>')
    (served / "index.html").write_text(hosted)
    (served / "question-bank.js").write_text("window.CCT_PRACTICE_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")
    counts: dict[str, dict[str, int]] = {}
    for q in data["questions"]:
        c = counts.setdefault(q["exam"], {"official": 0, "community": 0, "project": 0})
        c["project" if q.get("origin") == "project-authored" else "official" if q["source"].startswith(ALLOWED_SOURCES[0]) else "community"] += 1
    print(f"practice: {len(data['questions'])} questions into {OUT / 'index.html'}")
    for exam, c in counts.items():
        print(f"  {exam}: {c['official']} Anthropic samples, {c['community']} licensed community, {c['project']} project-authored")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, help="study workspace; refreshes practice/question-bank.json from it")
    args = ap.parse_args()
    if args.src:
        export(args.src.expanduser().resolve())
    build()


if __name__ == "__main__":
    main()
