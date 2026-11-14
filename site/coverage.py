"""CCAR-F practice coverage by objective, and industry transfer cases by objective (B63-FX-13).

Imported by site/build.py. Counts come from tools/question_map_check.summarize, so the page and the
gate check always report the same numbers. No question text is printed (the leak check forbids it).
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import question_map_check as qmc  # noqa: E402

OUT_REL = "lessons/ccar-f/objectives/practice-coverage.html"
CASE_FILES = (("PRIORITY-INDUSTRY-TRACKS.md", "finance-legal-marketing-tracks.html", "Primary objectives"),
              ("INDUSTRY-CASES.md", "industry-cases.html", "Objectives"))
CASE_DIR = "02-Lessons/02-CCAR-F-Architect-Foundations/objectives"


def industry_cases(src: Path, slugify) -> dict[str, list[tuple[str, str]]]:
    """{objective: [(link text, href relative to the objectives folder)]} from the case files' objective lines."""
    found: dict[str, list[tuple[str, str]]] = {}
    for name, out, label in CASE_FILES:
        f = src / CASE_DIR / name
        if not f.exists():
            continue
        heading = None
        for line in f.read_text().splitlines():
            h = re.match(r"^##\s+(.*)$", line)
            if h:
                heading = h.group(1).strip()
                continue
            if heading and line.startswith(f"**{label}:**"):
                short = re.split(r"\s+[—-]\s+", heading)[0]
                for o in re.findall(r"\[(\d\.\d)\]", line):
                    found.setdefault(o, []).append((short, f"{out}#{slugify(heading)}"))
    return found


def build_coverage(src: Path, objective_pages: dict, slugify, domain_lessons=()) -> str:
    fails, t = qmc.summarize(*qmc.load())
    cases = industry_cases(src, slugify)
    s = t["status"]
    rows = []
    for domain, kids in objective_pages.items():
        rows.append(f'<tr class="dom"><th colspan="5" scope="colgroup">Domain {domain}</th></tr>')
        for out, num, title in kids:
            c = t["per_obj"].get(num)
            clear, unc = (c["clear"], c["uncertain"]) if c else (0, 0)
            href = Path(out).name
            gap = ' class="gap"' if not clear + unc else ""
            qcell = "<b>none yet</b>" if not clear + unc else f"{clear} clear" + (f", {unc} uncertain" if unc else "")
            case_links = ", ".join(f'<a href="{h}">{html.escape(n)}</a>' for n, h in cases.get(num, [])) or "none"
            rows.append(f'<tr{gap}><th scope="row"><a href="{href}">{num}</a></th><td>{html.escape(title)}</td>'
                        f'<td>{qcell}</td><td>{case_links}</td>'
                        f'<td><a href="{href}#try-it">Try it</a></td></tr>')
    def lesson_for(d):  # domain label -> its domain lesson, matched on the first word
        first = d.split()[0].lower()
        return next((h for n, h in domain_lessons if n.split()[0].lower() == first), None)

    def unmapped_cell(d, n):
        h = lesson_for(d)
        return f'{n}, <a href="{h}">see domain lesson</a>' if n and h else str(n)
    doms = "".join(f'<tr><th scope="row">{html.escape(d)}</th><td>{c["clear"]}</td><td>{c["uncertain"]}</td>'
                   f'<td>{unmapped_cell(d, c["unmapped"])}</td><td>{sum(c.values())}</td></tr>' for d, c in sorted(t["by_domain"].items()))
    lesson_links = ", ".join(f'<a href="{h}">{html.escape(n)}</a>' for n, h in domain_lessons) or "the domain lessons"
    zero = ", ".join(t["zero"]) or "none"
    warn = ("<p class=\"callout\"><b>Check failed:</b> " + html.escape("; ".join(fails[:3])) + "</p>") if fails else ""
    reviewed = t["reviewed"] or "not yet"
    return f"""<article class="prose">
<h1 id="practice-coverage">CCAR-F practice coverage by objective</h1>
<p class="lede">Which of the 30 objectives the shared practice questions actually test, how sure we are, and where to go when you miss one.</p>
<p><b>Next step:</b> use this after a practice set. Find the objectives you missed, then work through each one (a target of about 10 minutes per objective).</p>
{warn}
<h2 id="how-to-read">How to read this page</h2>
<ul>
<li>The shared practice bank has <b>{t['bank']} CCAR-F questions</b>: {s['clear']} mapped with a <b>clear</b> fit, {s['uncertain']} mapped with an <b>uncertain</b> fit, and {s['unmapped']} <b>unmapped</b>. These add up to {t['bank']}.</li>
<li><b>Clear</b> means one official task statement plainly describes what the question tests. <b>Uncertain</b> means more than one fits, or the fit is loose. <b>Unmapped</b> means no single task statement fits; for those, use the domain lesson: {lesson_links}.</li>
<li>{t['multi']} questions map to two objectives, so they appear under both. The objective column therefore adds up to more than {t['bank']}; the bank total counts each question once.</li>
<li>Mappings retain author history plus the dated independent item/legacy review. Independent check: <b>{html.escape(reviewed)}</b>. Treat every mapping as a pointer, not a verdict.</li>
<li><b>{len(t['zero'])} objectives have no question at all</b> ({zero}). Task coverage does not establish complete individual skill-bullet mastery; consult the <a href="../skill-coverage.html">per-bullet ledger</a>. Practise those objectives with the lesson's Try it section and the industry cases.</li>
<li>The practice app records objective-level first-attempt, repeat and assisted evidence; your progress page shows these separately from checklist ticks.</li>
</ul>
<h2 id="by-domain">Totals by domain (as labelled in the bank)</h2>
<p class="muted">The bank's domain labels were set before objective mapping, and some sample-question domains are estimates. A question can sit in one domain here and map to an objective in another.</p>
<div class="tablewrap"><table><thead><tr><th scope="col">Domain</th><th scope="col">Clear</th><th scope="col">Uncertain</th><th scope="col">Unmapped</th><th scope="col">Total</th></tr></thead>
<tbody>{doms}<tr><th scope="row">All</th><td>{s['clear']}</td><td>{s['uncertain']}</td><td>{s['unmapped']}</td><td>{t['bank']}</td></tr></tbody></table></div>
<h2 id="by-objective">By objective: questions, industry cases and practice</h2>
<p>Missed a question on an objective? The middle column shows each objective's lesson title, which may be shorter than the official task statement; the lesson page quotes the official wording. Open the objective lesson, re-read the section it points to, then do its <b>Try it</b> exercise and an industry case that uses it. The industry cases are invented (synthetic) scenarios that practise real objectives; the industry names are a preference for context, not an official exam weighting.</p>
<div class="tablewrap"><table class="coverage"><thead><tr><th scope="col">Objective</th><th scope="col">Objective (lesson title)</th><th scope="col">Shared questions</th><th scope="col">Industry cases that practise it</th><th scope="col">Practice</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
<h2 id="industry">Find a case by industry</h2>
<ul>
<li><a href="finance-legal-marketing-tracks.html">Finance, Legal and Marketing tracks</a>: three capstones of ten objectives each; together they cover all 30.</li>
<li><a href="industry-cases.html">Production transfer cases</a>: Insurance, Logistics, Manufacturing, Healthcare software, Legal operations and Retail software, five objectives each.</li>
</ul>
<p class="src-note">Sources: official task statements from the CCAR-F exam guide via the objective lessons (Tier 1); mapping by this project (pending an independent check); industry cases are original synthetic exercises written by this project.</p>
</article>"""
