"""CCAR-F progress page and per-objective cues (B63-FX-12).

Imported by site/build.py. The activity manifest is read from the built objective pages themselves
(every "Done when" checkbox carries a data-k key), so the counts the learner sees always match the
checks on the pages. Progress lives only in this browser (localStorage); nothing is sent anywhere.

Honest states, kept separate:
  - opened:   the page was opened in this browser (not "read", not "learned")
  - checked:  the learner ticked a "Done when" check themselves (self-report, not mastery)
  - practice: shared practice questions carry no objective tag yet, so attempts are not shown per objective
"""
from __future__ import annotations

import html
import json
import re

OUT_REL = "lessons/ccar-f/objectives/progress.html"
REVISIT_DAYS = 7


def manifest(objective_pages: dict, written: dict) -> list[dict]:
    """[{n, title, href, keys}] in course order, keys taken from the rendered page."""
    out = []
    for kids in objective_pages.values():
        for o, n, t in kids:
            keys = re.findall(r'type="checkbox" data-k="([^"]+)"', written.get(o, ""))
            out.append({"n": n, "title": t, "href": o.rsplit("/", 1)[-1], "keys": keys})
    return out


def cue(n: str) -> str:
    """Placeholder on an objective page; progress.js fills it. Without script it still says where progress lives."""
    return (f'<p class="prog-cue" data-prog-obj="{html.escape(n)}">Your checks for this objective are kept only in this browser. '
            f'<a href="progress.html">See your CCAR-F progress</a>.</p>')


def build_progress(items: list[dict]) -> str:
    total_checks = sum(len(i["keys"]) for i in items)
    data = json.dumps({"exam": "ccar-f", "revisitDays": REVISIT_DAYS, "items": items}, separators=(",", ":"))
    rows = "".join(
        f'<tr data-prog-row="{html.escape(i["n"])}"><td><a href="{html.escape(i["href"])}"><b>{html.escape(i["n"])}</b> '
        f'{html.escape(i["title"])}</a></td><td class="prog-opened">Not recorded</td>'
        f'<td class="prog-checked">0 of {len(i["keys"])}</td><td class="prog-why">Not started in this browser</td></tr>'
        for i in items)
    return f"""<h1 id="progress">Your CCAR-F progress</h1>
<p class="lede">What you have opened and checked in this course, what is left, and which objectives to revisit.</p>
<div class="callout"><p><b>What this page can and cannot tell you.</b> A tick means you said you did a "Done when" check. It is not proof that you have mastered the objective, and nothing here predicts your exam result.
Practice attempts are recorded by objective in the <a href="../../../practice/index.html?exam=CCAR-F">practice app</a>; <a href="practice-coverage.html">coverage</a> distinguishes clear and uncertain mappings.
The best evidence of a gap is trying a check again a few days later without looking, and practising on a fresh case.</p>
<p><b>Stored only in this browser.</b> Nothing is sent to a server. Another browser, another device or clearing site data starts from zero. Use Export to keep a copy.</p></div>
<div id="prog-resume" class="prog-resume"><p>Start with <a href="{html.escape(items[0]["href"]) if items else "#"}">Objective {html.escape(items[0]["n"]) if items else ""}</a>.</p></div>
<p id="prog-summary" class="prog-summary">{len(items)} objectives, {total_checks} "Done when" checks in total. Turn on JavaScript to see your ticks.</p>
<div class="tbl"><table class="prog-table"><caption>Objectives in course order</caption>
<thead><tr><th scope="col">Objective</th><th scope="col">Opened here</th><th scope="col">Checks you ticked</th><th scope="col">Next step and why</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p id="prog-stale" class="prog-note" hidden></p>
<h2 id="practice-attempts">Practice evidence by objective</h2><div id="practice-evidence">Open the practice app to record an attempt. Legacy saves without attempt metadata remain separate.</div>
<h2 id="manage">Export or reset</h2>
<p>Export downloads your CCAR-F ticks and dates as a JSON file. Reset clears only CCAR-F objective ticks, dates and the last-opened marker in this browser; your theme and other exams are not touched.</p>
<p><button type="button" id="prog-export">Export CCAR-F progress</button> <button type="button" id="prog-reset">Reset CCAR-F progress</button></p>
<p id="prog-msg" role="status"></p>
<script type="application/json" id="prog-manifest">{data}</script>
"""
