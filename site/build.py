#!/usr/bin/env python3
"""Build the Claude certifications learning site into docs/.

Reads the study workspace (the Drive project) and writes static HTML. No third-party packages.

    python3 site/build.py --src "<path to the Claude Certifications and Training project>"

The source path can also come from the CERT_SRC environment variable.
"""
from __future__ import annotations

import argparse
import posixpath
import csv
import datetime as dt
import io
import hashlib
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import unquote, urlencode
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs"
ASSETS_SRC = REPO / "site" / "assets"
CHANGELOG_SRC = "10-Learning-Site/_repo-staging/CHANGELOG.md"
EXPORT_MARK = "EXPORT.json"
PUBLIC_REDACT = [
    (r" and to #[\w-]+ \(\d{1,2}:\d{2} [A-Z]{3}\)", ""),
    (r"until after CCAR-F was passed \(curriculum weeks 5–6\)", "until after the first exam was passed"),
    (r" \(CCAR-F in progress\)", ""),
    (r"Amar (\d{4}-\d{2}-\d{2}) after passing CCAO-F", r"Decision \1"),
    (r" after passing CCAO-F", ""),
    (r"CCAR-F first \(exam in progress\)", "the first exam first"),
    (r"(?:the )?37 (?:questions )?copied (?:from the official prep course|course questions)", "course questions we can't share"),
]
PRIVATE_ROWS = {"BACKLOG.md": {"B-11"}, "DECISIONS.md": {"7", "8", "9"}}
REQUIRED = {"10-Learning-Site/pages/FAQ.md", "10-Learning-Site/pages/CONTRIBUTE.md", CHANGELOG_SRC}
TODAY = dt.date.today().isoformat()

EXAMS = {
    "ccao-f": dict(code="CCAO-F", name="Claude Certified Associate – Foundations", short="Associate",
                   track="Associate", level="Foundations", color="associate", questions=60,
                   price=99, hours=(8, 12), curriculum="01-Curriculum/01-Associate-Track/CCAO-F.md",
                   labs=["01"],
                   who="Consultants, sellers and delivery leads who guide customers to the right Claude use cases."),
    "ccar-f": dict(code="CCAR-F", name="Claude Certified Architect – Foundations", short="Architect F",
                   track="Architect", level="Foundations", color="architect", questions=60,
                   price=125, hours=(20, 25), curriculum="01-Curriculum/02-Architect-Track/CCAR-F.md",
                   labs=["02", "03", "08"],
                   who="Architects designing agentic systems with Claude, MCP and Claude Code."),
    "ccdv-f": dict(code="CCDV-F", name="Claude Certified Developer – Foundations", short="Developer",
                   track="Developer", level="Foundations", color="developer", questions=53,
                   price=125, hours=(10, 15), curriculum="01-Curriculum/03-Developer-Track/CCDV-F.md",
                   labs=["02", "03", "04", "05"],
                   who="Engineers building with the Claude API, the Agent SDK, Claude Code and MCP."),
    "ccar-p": dict(code="CCAR-P", name="Claude Certified Architect – Professional", short="Architect P",
                   track="Architect", level="Professional", color="architect", questions=63,
                   price=175, hours=(15, 20), curriculum="01-Curriculum/02-Architect-Track/CCAR-P.md",
                   labs=["03", "04", "05"],
                   who="Senior architects owning end-to-end Claude solutions, evaluation and governance."),
}
# One source for the CCAR-F domain names (exam guide wording, "and" not "&"). walkthroughs() reads names from here
# and domain_names_once() rewrites the "&amp;" spelling on every built page, so no page shows a second form.
CCAR_F_DOMAINS = {"1": "Agentic Architecture and Orchestration", "2": "Tool Design and MCP Integration",
                  "3": "Claude Code Configuration and Workflows", "4": "Prompt Engineering and Structured Output",
                  "5": "Context Management and Reliability"}


def domain_names_once(written: dict) -> None:
    for name in CCAR_F_DOMAINS.values():
        amp = name.replace(" and ", " &amp; ")
        for rel, h in written.items():
            if amp in h:
                written[rel] = h.replace(amp, name)


CODE_TO_KEY = {v["code"]: k for k, v in EXAMS.items()}
OFFICIAL_CERTS = "https://anthropic-partners.skilljar.com/page/partner-certifications"
PRACTICE_URL = "https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html"
AMEY_REPO = "https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/"

# Links into these workspace folders aren't published; the link text is kept as plain text.
UNPUBLISHED = {
    "13-Plans": "local project plans and operating controls (not published)",
    "TRACKER.md": "your private progress tracker (not published)",
    "12-Progress": "your own notes",
    "03-Practice-Sessions": "the practice session (in the study workspace)",
    "05-Practice-Tool": "the practice tool (in the study workspace)",
    "08-Reference": "the reference library (in the study workspace)",
}

# Extra study pages inside an exam's lessons folder. The audio course and _build/ stay out (they aren't site pages).
STUDY_DECKS = ("FLASHCARDS.md", "HARD-DRILLS.md")
STUDY_SUBDIRS = ("deep-practice", "objectives", "scenario-walkthroughs", "architecture-studio", "concept-course")
WALK_SUB = "scenario-walkthroughs"
GUIDE_TAG = re.compile(r"\[Guide (\d\.\d(?:,\s*\d\.\d)*)\]")
SIDE_PAGES = {"tie-breaker-rules.md", "decision-charts.md", "sequence-diagrams.md", "code-level-flows.md", "conditions-and-errors.md"}
OUT_STEM = {"PRIORITY-INDUSTRY-TRACKS.md": "finance-legal-marketing-tracks"}
MERMAID_JS = "assets/vendor/mermaid-12.1.0.min.js"
HUB_LESSON = re.compile(r"#/lesson/(L0\d)\?at=s(\d)-(\d+)$")
HUB_CHART = re.compile(r"#/flows\?at=chart-(\w+)$")
GUIDE_TASK = re.compile(r"\btask (\d\.\d)\b", re.I)


# ---------------------------------------------------------------- page registry

class Site:
    def __init__(self, src: Path):
        self.src = src
        mark = src / EXPORT_MARK
        self.exported = mark.exists()
        info = json.loads(mark.read_text()) if self.exported else {}
        self.reviewed: dict[str, str] = info.get("reviewed", {})
        self.sha: dict[str, str] = info.get("sha", {})
        self.pages: dict[str, str] = {}
        self.meta: dict[str, dict] = {}
        self.anon = lambda s: s
        self._text: dict[str, str] = {}
        self.problems: list[str] = []
        self._walk: dict[str, list[dict]] = {}

    def path(self, src_rel: str) -> Path:
        return REPO / "CHANGELOG.md" if src_rel == CHANGELOG_SRC else self.src / src_rel

    def text(self, src_rel: str) -> str:
        if src_rel not in self._text:
            raw = self.path(src_rel).read_text()
            self._text[src_rel] = raw if self.exported else self.anon(scrub(raw, src_rel))
        return self._text[src_rel]

    def title(self, src_rel: str) -> str:
        return short_title(self.text(src_rel))

    def resolve(self, path: str, base: Path) -> str | None:
        path = unquote(path.strip())
        for b in (base, Path(".")):
            norm = os.path.normpath(str(b / path)).replace(os.sep, "/")
            for c in (norm, norm.rstrip("/") + "/README.md"):
                if c in self.pages:
                    return c
        return None

    def register(self, src_rel: str, out_rel: str, **info):
        self.pages[src_rel] = out_rel
        self.meta[out_rel] = dict(src=src_rel, **info)

    def of(self, kind: str, exam: str | None = None):
        for s, o in self.pages.items():
            m = self.meta[o]
            if m["kind"] == kind and (exam is None or m.get("exam") == exam):
                yield s, o, m


def exam_key_from_dir(name: str) -> str | None:
    m = re.search(r"(CCAO-F|CCAR-F|CCDV-F|CCAR-P)", name)
    return CODE_TO_KEY[m.group(1)] if m else None


def discover(site: Site):
    s = site.src
    site.register("01-Curriculum/00-Overview.md", "curriculum.html", kind="page")
    for key, e in EXAMS.items():
        site.register(e["curriculum"], f"exams/{key}.html", kind="exam", exam=key)
    site.register("02-Lessons/README.md", "lessons/index.html", kind="page")
    for d in sorted((s / "02-Lessons").iterdir()):
        key = exam_key_from_dir(d.name)
        if d.is_dir() and key:
            site.register(f"02-Lessons/{d.name}/README.md", f"lessons/{key}/index.html", kind="lesson-index", exam=key)
            for f in sorted(d.glob("L*.md")):
                site.register(f"02-Lessons/{d.name}/{f.name}", f"lessons/{key}/{f.stem}.html", kind="lesson", exam=key)
            for name in STUDY_DECKS:
                if (d / name).exists():
                    site.register(f"02-Lessons/{d.name}/{name}", f"lessons/{key}/{Path(name).stem.lower()}.html", kind="extra", exam=key, side=True)
            if key == 'ccar-f':
                for name in ('decision-atlas.md', 'decision-conversation.md', 'skill-coverage.md', 'scenario-studio.md', 'learning-journey.md', 'last-minute-prep.md', 'mechanism-clinic.md', 'choice-workshop.md'):
                    if (d / name).exists():
                        site.register(f'02-Lessons/{d.name}/{name}', f'lessons/{key}/{Path(name).stem}.html', kind='extra', exam=key, side=True)
            for sub in STUDY_SUBDIRS:
                for f in sorted((d / sub).glob("*.md")) if (d / sub).is_dir() else ():
                    if f.name.startswith("_"):  # drafts and working files never publish
                        continue
                    readme = f.name == "README.md"
                    stem = "index" if readme else OUT_STEM.get(f.name) or f.stem.lower()
                    site.register(f"02-Lessons/{d.name}/{sub}/{f.name}", f"lessons/{key}/{sub}/{stem}.html", kind="extra",
                                  exam=key, sub=sub, side=(readme and sub != "concept-course") or f.name in SIDE_PAGES)
    site.register("04-Simulations/README.md", "simulations/index.html", kind="page")
    for d in sorted((s / "04-Simulations").iterdir()):
        key = exam_key_from_dir(d.name)
        if d.is_dir() and key:
            site.register(f"04-Simulations/{d.name}/README.md", f"simulations/{key}/index.html", kind="sim-index", exam=key)
            for f in sorted(d.glob("SIM-*.md")):
                site.register(f"04-Simulations/{d.name}/{f.name}", f"simulations/{key}/{f.stem}.html", kind="sim", exam=key)
    site.register("06-Labs/README.md", "labs/index.html", kind="page")
    for d in sorted((s / "06-Labs").iterdir()):
        if d.is_dir() and (d / "README.md").exists():
            site.register(f"06-Labs/{d.name}/README.md", f"labs/{d.name}.html", kind="lab", lab=d.name[:2])
    site.register("11-Lessons-Learned/INSIGHTS.md", "insights.html", kind="page")
    site.register("CREW-WORKFLOW.md", "how-we-build.html", kind="page")
    site.register("10-Learning-Site/pages/FAQ.md", "faq.html", kind="page")
    site.register("10-Learning-Site/pages/CONTRIBUTE.md", "contribute.html", kind="page")
    site.register(CHANGELOG_SRC, "whats-new.html", kind="page")


# ---------------------------------------------------------------- privacy transforms

def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


class Anonymizer:
    """Replaces colleague names (from a private file outside the repo) with 'a colleague'."""

    def __init__(self, names_file: Path):
        full, first, allowed, mode = [], [], set(), "blocked"
        if names_file.exists():
            for line in names_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("allowed:"):
                    mode = "allowed"
                    if line[8:].strip():
                        allowed.add(line[8:].strip())
                elif mode == "allowed":
                    allowed.add(line)
                elif line.startswith("first:"):
                    first.append(line[6:].strip())
                else:
                    full.append(line)
        else:
            sys.exit(f"build: {names_file} not found; refusing to build without the names file")
        names = [n for n in full if n not in allowed] + [n for n in first if n not in allowed]
        variants = {v for n in names for v in (n, fold(n))}
        pats = sorted((r"\*{0,2}[\s_-]+\*{0,2}".join(map(re.escape, v.split())) for v in variants), key=len, reverse=True)
        self.rx = re.compile(r"(?<![\w/#.])(?P<lead>\*{0,2})(?:%s)(?P<trail>\*{0,2})(?P<pos>['\u2019]s)?(?![\w-])" % "|".join(pats), re.I) if pats else None

    def __call__(self, text: str) -> str:
        if not self.rx:
            return text

        def repl(m):
            lead, trail = m.group("lead"), m.group("trail")
            if lead == trail:
                lead = trail = ""
            return lead + "a colleague" + trail + ("'s" if m.group("pos") else "")
        text = self.rx.sub(repl, text)

        def collapse(m):
            n = m.group(0).count("a colleague")
            return "a colleague" if n == 1 else f"{n} colleagues"
        text = re.sub(r"\*\*(a colleague(?:'s)?[,;]?)\*\*", r"\1", text, flags=re.I)
        sep = r"(?:\s*,\s*and\s+|\s*,\s*|\s+and\s+|\s*\+\s*|\s*;\s*)"
        text = re.sub(r"a colleague(?:%s(?:\([^)]*\)\s*)?a colleague)+" % sep, collapse, text)
        text = re.sub(r"(^\s*(?:[-*]|\d+\.)\s+|^|[.!?]\s+|\|\s*|\(\s*|\*\*)a colleague",
                      lambda m: m.group(1) + "A colleague", text, flags=re.M)
        return text


SLACK_LINK = re.compile(r"\[([^\]]*)\]\(https?://[a-z0-9.-]*slack\.com[^)]*\)")
SLACK_BARE = re.compile(r"(?:https?://[a-z0-9.-]*slack\.com|slack:/)/\S+")
SLACK_IDS = re.compile(r",?\s*\(?`?\b(?:[CUWT]0[A-Z0-9]{7,10})(?:/p\d{16})?\b`?\)?|`?\bp1\d{15}\b`?")


def decisions_list(md: str, name: str = "") -> str:
    """Simulations whose questions live only in the coach-key table get a public decisions list above the key."""
    if re.search(r"^## The decisions", md, re.M) or not re.search(r"^<details><summary><b>Coach key", md, re.M):
        return md
    m = re.search(r"^<details><summary><b>Coach key[^\n]*\n+((?:\|[^\n]*\n)+)", md, re.M)
    split = lambda r: [c.strip() for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))]
    rows = [split(r) for r in m.group(1).splitlines()] if m else []
    if not rows or "Decision" not in rows[0]:
        print(f"build: warning: {name or 'a simulation'} has a coach key but no Decision column; no public decisions list", file=sys.stderr)
        return md
    head = rows[0]
    si, di = (head.index("Stage") if "Stage" in head else None), head.index("Decision")
    body = [r for r in rows[2:] if len(r) == len(head)]
    items = [f"{i}. " + (f"**{r[si]}:** " if si is not None else "") + r[di] for i, r in enumerate(body, 1)]
    block = "## The decisions (answer these before you open the key)\n\n" + "\n".join(items) + "\n\n"
    return md[:m.start()] + block + md[m.start():]


def scrub(md: str, name: str = "") -> str:
    md = re.sub(r"<!-- site:hide -->.*?(<!-- /site:hide -->|\Z)", "", md, flags=re.S)
    md = decisions_list(md, name)
    md = md.replace("## Scene (Claude reads this to you)", "## Scene (read it yourself, or have Claude read it)")
    md = md.replace("<summary><b>Coach key:", "<summary><b>Answer key (coach key):")
    drill = "[practice-tool drill](" + PRACTICE_URL + ")"
    md = re.sub(r"→\s*S0\d(, twice)?", lambda m: "→ practice drill" + (m.group(1) or ""), md)
    md = re.sub(r"\s*·\s*\[S0\d\]\([^)]*\)", " · " + drill, md)
    md = "\n".join(l for l in md.splitlines() if not re.search(r"\|\s*Practice sessions S0\d", l))
    session = r"(?:\[[^\]]*S0\d[^\]]*\]\([^)]*\)|S0\d)"
    md = re.sub(r"(\s*·\s*\*\*Practice(?: sessions?)?:?\*\*:?\s*)%s(?:\s*(?:,\s*and\b|,|\band\b|&)\s*%s)*(?=(\n\*\*)?)" % (session, session),
                lambda m: m.group(1) + drill + " for this domain" + (" ·" if m.group(2) else ""), md)
    md = re.sub(r"^(\s*[-*] \[[ xX]\] You scored 80% or more on )(?:the |a )?(?:\[[^\]]*S0\d[^\]]*\]\([^)]*\)|(?:practice session )?S0\d)",
                lambda m: m.group(1) + "a " + drill + " for this domain", md, flags=re.M)
    private = "|".join(map(re.escape, UNPUBLISHED))
    label_of = lambda s: next(label for prefix, label in UNPUBLISHED.items() if prefix in s)
    md = re.sub(r"`([^`\n]*(?:%s)(?:/[^`\n]*)?)`" % private, lambda m: label_of(m.group(1)), md)
    md = re.sub(r"\]\(([^)\s]*(?:exam-guide|Exam-Guide)[^)\s]*)\)", "](" + OFFICIAL_CERTS + ")", md)
    md = re.sub(r"\]\([^)\s]*05-Practice-Tool/index\.html\)", "](" + PRACTICE_URL + ")", md)
    md = re.sub(r"\]\([^)\s]*03-Practice-Sessions/[^)\s]*\.md\)", "](" + PRACTICE_URL + ")", md)
    md = re.sub(r"\]\([^)\s]*amey-thakur-CLAUDE-CERTIFICATIONS/([^)\s#?]+\.md(?:[#?][^)\s]*)?)\)", lambda m: "](" + AMEY_REPO + m.group(1) + ")", md)
    md = re.sub(r"\[([^\]\n]+)\]\(([^)\s]*(?:%s)[^)\s]*)\)" % private,
                lambda m: label_of(m.group(2)) if re.search(r"/|\.(md|html|json|pdf)$", m.group(1).strip("`")) else m.group(1).strip("`"), md)
    md = SLACK_LINK.sub(r"\1", md)
    md = SLACK_BARE.sub("", md)
    md = SLACK_IDS.sub("", md)
    md = md.replace(" Generated from `_build/`; edit the data there, not this file.", "")
    md = re.sub(r"\*\*Backlog:\*\* [A-Z]-\d+(?:, [A-Z]-\d+)* · ", "", md)
    md = re.sub(r"^(## Drill set checks) \(computed by `[^`]+`\)", r"\1", md, flags=re.M)
    out = []
    for line in md.splitlines():
        if re.match(r"\s*Full records are in", line) or "stop reading here" in line or re.search(r'\b[Ss]ay \*\*"Run simulation', line):
            continue
        line = re.sub(r"`/debrief [A-Z-]+`", "share what you learned", line)
        line = line.replace("[INSIGHTS](", "[Insights](")
        if "**Progress log:**" in line or "**Guide:**" in line:
            line = " · ".join(p for p in line.split(" · ") if "**Progress log:**" not in p and "**Guide:**" not in p)
            if not line.strip():
                continue
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------- markdown

def slugify(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t, flags=re.U)
    return t.replace(" ", "-")


RESERVED_IDS = ("main", "nav", "paths", "study-plan", "hpw", "hpw-out", "map-t", "map-d")
LIST_RX = re.compile(r"(\s*)([-*+]|\d+[.)])\s+(.*)")


class Renderer:
    def __init__(self, site: Site, src_rel: str, out_rel: str):
        self.site, self.src_rel, self.out_rel = site, src_rel, out_rel
        self.src_dir = Path(src_rel).parent
        self.checks = 0
        self.headings: list[tuple[int, str, str]] = []
        self.ids: dict[str, int] = {k: 1 for k in RESERVED_IDS}

    def rel_url(self, target_out: str) -> str:
        return os.path.relpath(target_out, os.path.dirname(self.out_rel) or ".").replace(os.sep, "/")

    def heading_anchor(self, src_rel: str, rx: str) -> str:
        fenced = False
        for line in self.site.text(src_rel).splitlines():
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if fenced:
                continue
            m = re.match(r"#{2,4}\s+(.*)", line.strip())
            if m and re.match(rx, m.group(1).strip()):
                return slugify(m.group(1).strip())
        return ""

    def hub(self, route: str) -> str | None:
        """Private study-hub routes (#/lesson/L01?at=s1-3, #/flows?at=chart-3) become links to the built pages."""
        exam = exam_key_from_dir(self.src_rel)
        m = HUB_LESSON.match(route)
        if m and exam:
            for s, o, _ in self.site.of("lesson", exam):
                if Path(s).stem.startswith(m.group(1)):
                    a = self.heading_anchor(s, rf"{m.group(2)}\.{m.group(3)}\b")
                    if a:
                        return f"{self.rel_url(o)}#{a}"
        m = HUB_CHART.match(route)
        if m and exam:
            for s, o in self.site.pages.items():
                if s.endswith("deep-practice/decision-charts.md") and exam_key_from_dir(s) == exam:
                    a = self.heading_anchor(s, rf"{re.escape(m.group(1))}\.\s")
                    if a:
                        return f"{self.rel_url(o)}#{a}"
        self.site.problems.append(f"{self.src_rel}: study-hub route {route} has no page to point at")
        return None

    def guide_task(self, text_html: str) -> str | None:
        """'exam guide, task 1.3' links go to that objective's page when the exam has one (RT-10 item I10)."""
        m = GUIDE_TASK.search(re.sub(r"<[^>]+>", "", text_html))
        exam = exam_key_from_dir(self.src_rel)
        if not (m and exam):
            return None
        for s, o in self.site.pages.items():
            if s.endswith(f"objectives/objective-{m.group(1)}.md") and exam_key_from_dir(s) == exam:
                return o
        return None

    def mermaid(self, src: str) -> str:
        def click(m):
            target = self.hub(m.group(2)) if m.group(2).startswith("#/") else m.group(2)
            return f'{m.group(1)}{target or "#"}{m.group(3)}'
        src = re.sub(r'^(\s*click\s+\S+\s+(?:href\s+)?")([^"]*)(")', click, src, flags=re.M)
        big = " mmd-big" if f"/{WALK_SUB}/" in self.src_rel else ""
        block = f'<div class="mmd{big}"><pre class="mermaid">{html.escape(src)}</pre></div>'
        if re.search(r"^\s*sequenceDiagram\b", src, re.M):
            return f'<details class="mmd-toggle" open><summary>Show diagram</summary>{block}</details>'
        return block

    def link(self, text_html: str, url: str) -> str:
        # Hosted practice is a site route: keep local previews and live learners
        # on their current origin instead of crossing to the older published app.
        if url == PRACTICE_URL or url.startswith(PRACTICE_URL + "?") or url.startswith(PRACTICE_URL + "#"):
            return f'<a href="{html.escape(self.rel_url("practice/index.html") + url[len(PRACTICE_URL):], quote=True)}">{text_html}</a>'
        if re.match(r"(https?:|mailto:)", url):
            if "slack.com" in url:
                return text_html
            ext = f'<a class="ext" href="{html.escape(url, quote=True)}" rel="noopener">{text_html}</a>'
            if url == OFFICIAL_CERTS and (task_page := self.guide_task(text_html)):
                return f'{ext} (<a href="{html.escape(self.rel_url(task_page))}">objective page</a>)'
            return ext
        if url.startswith("#/"):
            target = self.hub(url)
            return f'<a href="{html.escape(target)}">{text_html}</a>' if target else text_html
        if url.startswith("#"):
            return f'<a href="{html.escape(url)}">{text_html}</a>'
        if url.startswith("site:"):
            extra = " download" if url[5:].startswith("downloads/") else ""
            return f'<a href="{html.escape(self.rel_url(url[5:]))}"{extra}>{text_html}</a>'
        path, _, anchor = url.partition("#")
        path = unquote(path)
        norm = os.path.normpath(str(self.src_dir / path)).replace(os.sep, "/")
        c = self.site.resolve(path, self.src_dir) if path else None
        if c:
            href = self.rel_url(self.site.pages[c]) + (f"#{anchor}" if anchor else "")
            plain0 = re.sub(r"</?code>", "", text_html)
            if "<a " in text_html or ("/" in plain0 and " " not in plain0.strip()) or re.search(r"\.(md|html)$|^\d\d-", plain0):
                text_html = html.escape(self.site.title(c))
            return f'<a href="{html.escape(href)}">{text_html}</a>'
        # B63-FX-3: the "Objective map" label points at the site's objective list for that exam instead of staying dead text.
        mm = re.search(r"(CCAR-F)-objectives\.md$", norm)
        if mm and not anchor:
            ex = exam_key_from_dir(mm.group(1))
            hub = next((o for s_, o in self.site.pages.items() if s_.endswith("objectives/README.md") and exam_key_from_dir(s_) == ex), None)
            if hub:
                return f'<a href="{html.escape(self.rel_url(hub))}">{text_html}</a>'
        if re.search(r"exam-guide|Exam-Guide", norm):
            return f'<a class="ext" href="{OFFICIAL_CERTS}" rel="noopener">{text_html}</a>'
        plain = re.sub(r"</?code>", "", text_html)
        looks_like_path = "/" in plain or re.search(r"\.(md|html|json|pdf)$", plain)
        for prefix, label in UNPUBLISHED.items():
            if prefix in norm:
                return label if looks_like_path else plain
        if looks_like_path:
            return html.escape(Path(plain.rstrip("/")).name)
        return plain

    def inline(self, s: str) -> str:
        codes: list[str] = []

        def keep_code(m):
            c = self.site.resolve(m.group(1), self.src_dir) if re.match(r"[\w./-]+$", m.group(1)) and "/" in m.group(1) else None
            if c:
                codes.append(f'<a href="{html.escape(self.rel_url(self.site.pages[c]))}">{html.escape(self.site.title(c))}</a>')
                return f"\x00{len(codes) - 1}\x00"
            codes.append(f"<code>{html.escape(m.group(1))}</code>")
            return f"\x00{len(codes) - 1}\x00"
        s = re.sub(r"`([^`]+)`", keep_code, s)
        s = re.sub(r"<(https?://[^>\s]+)>", r"\1", s)
        s = html.escape(s, quote=False)
        s = re.sub(r"&lt;br\s*/?&gt;", "<br>", s)
        links: list[str] = []

        def keep_link(m):
            inner = re.sub(r"\x00(\d+)\x00", lambda k: codes[int(k.group(1))], self.emph(m.group(1)))
            links.append(self.link(inner, html.unescape(m.group(2))))
            return f"\x01{len(links) - 1}\x01"
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", keep_link, s)
        s = re.sub(r"(?<![\"=/\w])(https?://[^\s<]+[^\s<.,;:)])",
                   lambda m: f'<a class="ext" href="{html.escape(html.unescape(m.group(1)), quote=True)}" rel="noopener">{m.group(1)}</a>', s)
        s = self.emph(s)
        s = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)
        s = re.sub(r"\x01(\d+)\x01", lambda m: links[int(m.group(1))], s)
        return s

    @staticmethod
    def emph(s: str) -> str:
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)

    def checkbox(self, text: str) -> str:
        m = re.match(r"\[( |x|X)\]\s*(.*)", text)
        if not m:
            return self.inline(text)
        self.checks += 1
        checked = " checked" if m.group(1).lower() == "x" else ""
        label = self.inline(m.group(2)) if m.group(2) else '<span class="sr">Done</span>'
        return (f'<label class="check"><input type="checkbox" data-k="{self.out_rel}#{self.checks}"{checked}>'
                f'<span>{label}</span></label>')

    def heading(self, level: int, text: str) -> str:
        inner = self.inline(text)
        hid = slugify(text)
        n = self.ids.get(hid, 0)
        self.ids[hid] = n + 1
        if n:
            hid = f"{hid}-{n}"
        # Plain text (entities decoded) so toc() escapes it once: F17, "&amp;amp;" in section lists.
        self.headings.append((level, hid, html.unescape(re.sub(r"<[^>]+>", "", inner))))
        return f'<h{level} id="{hid}">{inner}</h{level}>'

    def table(self, rows: list[str]) -> str:
        def cells(r):
            r = r.strip().removeprefix("|").removesuffix("|")
            spans: list[str] = []
            r = re.sub(r"`[^`]*`", lambda m: spans.append(m.group(0)) or f"\x02{len(spans) - 1}\x02", r)
            out = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", r)]
            return [re.sub(r"\x02(\d+)\x02", lambda m: spans[int(m.group(1))], c) for c in out]
        head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
        private = ("progress log", "practice", "practice session", "practice sessions")
        keep = [j for j, h in enumerate(head) if h.strip("* ").lower() not in private]
        head, body = [head[j] for j in keep], [[r[j] for j in keep if j < len(r)] for r in body]
        out = ['<div class="tbl"><table><thead><tr>', *(f"<th>{self.inline(h)}</th>" for h in head), "</tr></thead><tbody>"]
        for r in body:
            out.append("<tr>" + "".join(f"<td>{self.checkbox(c)}</td>" for c in r) + "</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    def lists(self, lines: list[str]) -> str:
        items = []
        for ln in lines:
            m = LIST_RX.match(ln)
            if m:
                items.append([len(m.group(1).expandtabs(4)), m.group(2)[0].isdigit(), m.group(3)])
            elif items:
                items[-1][2] += " " + ln.strip()
        out, stack = [], []
        for indent, ordered, text in items:
            while stack and indent < stack[-1][0]:
                out.append("</li></%s>" % stack.pop()[1])
            if not stack or indent > stack[-1][0]:
                tag = "ol" if ordered else "ul"
                out.append(f"<{tag}>")
                stack.append((indent, tag))
            else:
                out.append("</li>")
            out.append("<li>" + self.checkbox(text))
        while stack:
            out.append("</li></%s>" % stack.pop()[1])
        return "".join(out)

    def render(self, md: str) -> str:
        md = re.sub(r"<!--\s*/?layered-scenario-migration\s*-->", "", md)
        lines = md.splitlines()
        out, para, i = [], [], 0

        def flush():
            if para:
                # Markdown hard break: a line ending in two spaces (or a backslash) keeps its line break (B63-FX-7).
                joined = ""
                for k, p in enumerate(para):
                    t = p.strip()
                    if k < len(para) - 1:
                        hard = p.rstrip("\n").endswith("  ") or t.endswith("\\")
                        t = (t[:-1].rstrip() if t.endswith("\\") else t) + ("<br>" if hard else " ")
                    joined += t
                out.append("<p>" + self.inline(joined) + "</p>")
                para.clear()
        while i < len(lines):
            ln, st = lines[i], lines[i].strip()
            if st.startswith("```"):
                flush()
                lang, buf = st[3:].strip(), []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1
                if lang == "mermaid":
                    out.append(self.mermaid(chr(10).join(buf)))
                    continue
                out.append(f'<pre><code class="lang-{html.escape(lang or "text")}">{html.escape(chr(10).join(buf))}</code></pre>')
                continue
            if not st:
                flush()
                i += 1
                continue
            if re.fullmatch(r'<a id="[\w-]+"></a>', st):
                flush()
                out.append(st)
                i += 1
                continue
            if re.match(r"</?(details|summary|div|figure|figcaption)\b", st):
                if st.startswith("<details><summary>Compare the offline evidence — after making your decision"):
                    st = st.replace("<details>", '<details class="benchmark-reference">', 1)
                flush()
                st = re.sub(r"<summary>(.*?)</summary>",
                            lambda m: "<summary>" + self.inline(re.sub(r"</?code>", "`", re.sub(r"</?b>", "**", m.group(1)))) + "</summary>", st)
                out.append(st)
                i += 1
                continue
            m = re.match(r"(#{1,6})\s+(.*)", st)
            if m:
                flush()
                out.append(self.heading(len(m.group(1)), m.group(2).strip()))
                i += 1
                continue
            if re.match(r"^(-{3,}|\*{3,})$", st):
                flush()
                out.append("<hr>")
                i += 1
                continue
            if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
                flush()
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(lines[i])
                    i += 1
                out.append(self.table(rows))
                continue
            if st.startswith(">"):
                flush()
                buf = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                sub = Renderer(self.site, self.src_rel, self.out_rel)
                sub.checks, sub.ids, sub.headings = self.checks, self.ids, self.headings
                out.append("<blockquote>" + sub.render("\n".join(buf)) + "</blockquote>")
                self.checks = sub.checks
                continue
            if LIST_RX.match(ln):
                flush()
                buf = []
                while i < len(lines):
                    cur = lines[i]
                    if LIST_RX.match(cur) or (cur.strip() and cur[:1] in (" ", "\t")):
                        buf.append(cur)
                    elif not cur.strip() and i + 1 < len(lines) and re.match(r"\s*([-*+]|\d+[.)])\s+|\s{2,}\S", lines[i + 1]):
                        pass
                    else:
                        break
                    i += 1
                out.append(self.lists(buf))
                continue
            para.append(ln)
            i += 1
        flush()
        return "\n".join(out)


# ---------------------------------------------------------------- page chrome

NAV = [("index.html", "Home"), ("curriculum.html", "Curriculum"), ("exams/ccao-f.html", "CCAO-F"),
       ("exams/ccar-f.html", "CCAR-F"), ("exams/ccdv-f.html", "CCDV-F"), ("exams/ccar-p.html", "CCAR-P"),
       ("lessons/index.html", "Lessons"), ("simulations/index.html", "Simulations"), ("labs/index.html", "Labs"),
       ("insights.html", "Insights"), ("resources.html", "Resources"), ("faq.html", "FAQ"), ("about.html", "About")]


REPO_URL = "https://git.soma.salesforce.com/akumthekar/claude-certifications-training"
PAGES_URL = "https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/"


def report_link(out_rel: str) -> str:
    q = urlencode({"template": "report-a-problem.yml", "page": PAGES_URL + out_rel})
    return f'<a class="ext" href="{REPO_URL}/issues/new?{html.escape(q)}" rel="noopener">Report a problem on this page</a>'


def page(out_rel: str, title: str, body: str, *, exam: str | None = None, side: str = "",
         crumbs: list[tuple[str, str]] | None = None, reviewed: str = TODAY, description: str = "") -> str:
    root = "../" * out_rel.count("/")

    def current(href):
        return href == out_rel or (exam is not None and href == f"exams/{exam}.html")
    nav = "".join(f'<a href="{root}{h}"{" aria-current=\"page\"" if current(h) else ""}>{t}</a>' for h, t in NAV)
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true"> / </span>'.join(
            f'<a href="{root}{h}">{html.escape(t)}</a>' if h else f'<span>{html.escape(t)}</span>' for t, h in crumbs) + "</nav>"
    outline = re.search(r'<nav class="toc-nav".*?</nav>', body, re.S)
    if outline and '<article class="prose">' in body:
        body = body.replace(outline.group(0), '', 1)
        body = '<div class="learning-layout">' + body + '<aside class="learning-outline" aria-label="Page sections">' + outline.group(0) + '</aside></div>'
    color = EXAMS[exam]["color"] if exam else "neutral"
    side_html = f'<aside class="side" aria-label="In this exam"><details class="course-nav" open><summary>Course navigation</summary>{side}</details></aside>' if side else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="reviewed" content="{reviewed}">
<meta name="reviewed-source" content="{'recorded' if exam and reviewed else 'none' if exam else 'n/a'}">
<meta name="description" content="{html.escape(description or title)}">
<title>{html.escape(title)} · Claude Certifications Study Site</title>
<link rel="stylesheet" href="{root}assets/site.css">
{f'<link rel="stylesheet" href="{root}assets/viewer.css">' + chr(10) if 'class="mermaid"' in body else ""}{f'<script defer src="{root}{MERMAID_JS}"></script>' + chr(10) + f'<script defer src="{root}assets/viewer.js"></script>' + chr(10) if 'class="mermaid"' in body else ""}<script defer src="{root}assets/site.js"></script>{chr(10) + f'<script defer src="{root}assets/progress.js"></script>' if 'data-prog-' in body else ""}
</head>
<body class="t-{color}">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="{root}index.html"><span class="mark" aria-hidden="true">✳</span> Claude Certifications <span class="brand-sub">Study Site</span></a>
  <button class="menu" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav id="nav" aria-label="Main">{nav}</nav>
  <button class="theme" aria-label="Switch between light and dark theme">◐</button>
</header>
<div class="wrap {'with-side' if side else 'no-side'}">
{side_html}
<main id="main">
{crumb_html}
{body}
</main>
</div>
<footer class="foot">
  <p>An internal study site for Anthropic's Claude certifications, made by colleagues. It isn't affiliated with or endorsed by Anthropic.
  Facts come from Anthropic's own material first (<a href="{root}about.html#source-tiers">source tiers</a>), and the official exam guide always wins.</p>
  <p>{report_link(out_rel)} · <a href="{root}contribute.html">Contribute</a> · <a href="{root}whats-new.html">What's new</a> · <a href="{root}faq.html">FAQ</a></p>
  <p>No real exam questions. Your checklist ticks stay in this browser. Built {TODAY} · <a href="{root}how-we-build.html">How this site is built and checked</a></p>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- scenario walkthroughs

def _num_key(n: str):
    return tuple(int(x) for x in n.split("."))


def objective_page(site: Site, exam: str, num: str) -> str | None:
    for s, o in site.pages.items():
        if s.endswith(f"objectives/objective-{num}.md") and exam_key_from_dir(s) == exam:
            return o
    return None


def walkthroughs(site: Site, exam: str) -> list[dict]:
    """Facts read from each walkthrough page, so the hub and the back-links can't drift from it."""
    if exam in site._walk:
        return site._walk[exam]
    out = []
    for s, o, m in site.of("extra", exam):
        if m.get("sub") != WALK_SUB or o.endswith("/index.html"):
            continue
        md = site.text(s)
        title = re.sub(r",\s*start to finish\s*$", "", first_heading(md))
        dom = re.search(r"Primary domains:\s*([^*\n]+)", md)
        rem = re.search(r"\*\*Remember it as:\*\*\s*(.+?)(?:\n\s*\n|\Z)", md, re.S)
        num = re.search(r"Exam scenario (\d+)", md)
        for label, found in (("Exam scenario N", num), ("Primary domains", dom), ("Remember it as", rem)):
            if not found:
                site.problems.append(f"{s}: walkthrough has no '{label}' line for the scenario map")
        doms = sorted((d, CCAR_F_DOMAINS.get(d, n)) for d, n in re.findall(r"(\d) ([^,]+?)(?=, \d |$)", dom.group(1).strip())) if dom else []
        # Low item: take the simulation from the explicit "- [Simulation N: ...](...SIM-0N-....md)" line, not the first mention anywhere.
        sim = re.search(r"^\s*[-*]\s*\[Simulation \d+[^\]]*\]\([^)\s]*?(SIM-\d+)[^)\s]*\.md\)", md, re.M)
        sim_out = None
        if sim:
            sim_out = next((so for ss, so, _ in site.of("sim", exam) if Path(ss).name.startswith(sim.group(1))), None)
        nums = sorted({n for g in GUIDE_TAG.findall(md) for n in re.split(r",\s*", g)}, key=_num_key)
        domains = (f"Domains {', '.join(d for d, _ in doms[:-1])} and {doms[-1][0]}" if len(doms) > 1 else
                   f"Domain {doms[0][0]}" if doms else "")
        out.append(dict(src=s, out=o, title=title, short=title.split(":", 1)[-1].strip(), num=num.group(1) if num else "",
                        domains=(domains + ": " + " · ".join(n.strip() for _, n in doms)) if doms else "", remember=rem.group(1).strip() if rem else "",
                        sim=sim.group(1) if sim else "", sim_out=sim_out, objectives=nums))
    out.sort(key=lambda w: int(w["num"] or 99))
    site._walk[exam] = out
    return out


def link_guide_tags(site: Site, r: "Renderer", exam: str, body: str) -> str:
    def one(m):
        links = []
        for n in re.split(r",\s*", m.group(1)):
            o = objective_page(site, exam, n)
            links.append(f'<a href="{html.escape(r.rel_url(o))}">{n}</a>' if o else n)
        return "[Guide " + ", ".join(links) + "]"
    parts = re.split(r"(<pre\b.*?</pre>|<code\b.*?</code>|<a\b.*?</a>)", body, flags=re.S)
    return "".join(p if p.startswith(("<pre", "<code", "<a")) else GUIDE_TAG.sub(one, p) for p in parts)


def scenario_map(site: Site, r: "Renderer", exam: str) -> str:
    whatifs = slugify("Run it for real: 10 what-if questions")
    cards = []
    for w in walkthroughs(site, exam):
        href = html.escape(r.rel_url(w["out"]))
        links = [f'1. <a href="{href}">Walkthrough</a>', f'2. <a href="{href}#{whatifs}">What-ifs</a>']
        if w["sim_out"]:
            links.append(f'3. <a href="{html.escape(r.rel_url(w["sim_out"]))}">Simulation {int(w["sim"].split("-")[1])}</a>')
        objs = [f'<a href="{html.escape(r.rel_url(o))}">{n}</a>' for n in w["objectives"] if (o := objective_page(site, exam, n))]
        cards.append(
            '<div class="scn-card">'
            f'<p class="scn-title"><span class="scn-num">{w["num"]}</span> <a href="{href}">{html.escape(w["short"])}</a></p>'
            + (f'<p class="scn-key"><b>Remember it as:</b> {r.inline(w["remember"])}</p>' if w["remember"] else "")
            + (f'<p class="scn-dom">{html.escape(w["domains"])}</p>' if w["domains"] else "")
            + '<p class="scn-time">About 45 minutes: read 20 min, then what-ifs 10 min, then simulation 15 min</p>'
            + f'<p class="scn-links">{" · ".join(links)}</p>'
            + (f'<p class="scn-obj">Fill gaps with objective lessons (optional): {" · ".join(objs)}</p>' if objs else "")
            + "</div>")
    return '<div class="scenario-map">' + "".join(cards) + "</div>"


def enrich_page(site: Site, r: "Renderer", src_rel: str, out_rel: str, kind: str, exam: str | None, body: str) -> tuple[str, str]:
    """Returns the body and a callout for the top of the page (placed under the h1 after the page parts are added)."""
    walks = walkthroughs(site, exam) if exam else []
    if not walks:
        return body, ""
    in_walk = f"/{WALK_SUB}/" in src_rel
    if in_walk:
        body = link_guide_tags(site, r, exam, body)
    if in_walk and out_rel.endswith("/index.html"):
        body, n = re.subn(r'<div class="tbl"><table><thead><tr><th>#</th><th>Scenario</th>.*?</table></div>',
                          lambda _: scenario_map(site, r, exam), body, count=1, flags=re.S)
        if not n:
            site.problems.append(f"{src_rel}: no '# | Scenario' table to turn into the scenario map")
    if in_walk and not out_rel.endswith("/index.html"):
        m = re.search(r'<h2 id="in-real-life[^"]*">.*?</h2>', body)
        if not m:
            site.problems.append(f"{src_rel}: no 'In real life' section to fold away from the exam content")
        else:
            end = body.find("<h2", m.end())
            end = len(body) if end < 0 else end
            body = (body[:m.start()] + '<details class="beyond"><summary>In real life: beyond the exam '
                    '<span>(not exam rules, open when you want the real-world view)</span></summary>'
                    + body[m.start():end] + "</details>" + body[end:])
    note = ""
    if in_walk and not out_rel.endswith("/index.html"):
        # Reading time = words in the source page / 200 words per minute, rounded up to the next 5 minutes.
        words = len(site.text(src_rel).split())
        note = f'<p class="walk-time">About {((words + 999) // 1000) * 5} minutes to read.</p>'
    if kind == "sim":
        w = next((w for w in walks if w["sim_out"] == out_rel), None)
        if w:
            note = (f'<p class="walk-first"><b>Study the walkthrough first (about 20 min):</b> <a href="{html.escape(r.rel_url(w["out"]))}">'
                    f'{html.escape(w["title"])}</a>. It has the flowchart, each step\'s decision and what can go wrong. Then come back here.</p>')
    elif kind == "extra" and (om := re.search(r"objectives/objective-(\d\.\d)\.md$", src_rel)):
        seen = [w for w in walks if om.group(1) in w["objectives"]]
        if seen:
            note = ('<p class="walk-first"><b>Seen in scenario:</b> ' + ", ".join(
                f'<a href="{html.escape(r.rel_url(w["out"]))}">{html.escape(w["title"])}</a>' for w in seen) + ".</p>")
    elif kind == "lesson-index":
        hub = next((o for s, o, m in site.of("extra", exam) if m.get("sub") == WALK_SUB and o.endswith("/index.html")), None)
        if hub:
            note = (f'<p class="walk-first"><b>New: <a href="{html.escape(r.rel_url(hub))}">Scenario walkthroughs</a>.</b> '
                    "One page for each official scenario: the whole job as a flowchart, each step's decision, "
                    "what can go wrong, and 10 what-if questions. Start with Scenario 1; each takes about 45 minutes.</p>")
    return body, note


def first_heading(md: str) -> str:
    m = re.search(r"^#\s+(.*)$", md, re.M)
    return m.group(1).strip() if m else "Untitled"


def lesson_meta(md: str) -> dict:
    title = first_heading(md)
    m = re.search(r"\((\d+(?:\.\d+)?)%", title)
    name = title.split("—", 1)[1].strip() if "—" in title else title
    return dict(title=title, weight=float(m.group(1)) if m else None, name=re.sub(r"\s*\(.*\)\s*$", "", name))


def short_title(md: str) -> str:
    return re.sub(r"\s*\(.*\)\s*$", "", first_heading(md).split("—", 1)[-1].strip())


def side_label(site: Site, src: str) -> str:
    label = re.sub(r"^CC[A-Z]{2}-[FP] ", "", short_title(site.text(src))).split(":")[0]
    return label[:1].upper() + label[1:]


def objective_pages(site: Site, exam: str) -> dict:
    """{domain: [(out_rel, '1.2', friendly title)]} for exams with objective lessons, in number order."""
    found: dict[int, list] = {}
    for src, out in site.pages.items():
        m = re.search(r"objectives/objective-(\d)\.(\d+)\.md$", src)
        if m and exam_key_from_dir(src) == exam:
            title = first_heading(site.text(src))
            title = title.split("\u2014", 1)[1].strip() if "\u2014" in title else title
            found.setdefault(int(m.group(1)), []).append((int(m.group(2)), out, f"{m.group(1)}.{m.group(2)}", title))
    return {d: [(o, n, t) for _, o, n, t in sorted(v)] for d, v in sorted(found.items())}


# B63-FX-7 r3: section roles. One shared marker per h2 so Explanation, Exercise, Answer and Done-when read differently.
SECTION_ROLES = (
    ("answer", "Answer", ("worked-example",)),
    ("exercise", "Exercise", ("try-it", "supplied-", "production-challenge")),
    ("done", "Done when", ("done-when", "coverage-checklist")),
    ("explain", "Explanation", ("big-idea", "foundation", "applied-skills", "production-transfer", "traps", "sources")),
)


def mark_section_roles(body: str) -> str:
    """Mark known section roles without repeating a heading that is already its role."""
    def tag(m):
        hid, title = m.groups()
        key, label = "explain", "Explanation"
        for candidate, name, prefixes in SECTION_ROLES:
            if any(hid == p or hid.startswith(p if p.endswith("-") else p + "-") for p in prefixes):
                key, label = candidate, name
                break
        text = html.unescape(re.sub(r"<[^>]+>", "", title)).strip().casefold()
        role = "" if text.startswith(label.casefold()) else f'<span class="role-tag">{label}</span> '
        return f'<h2 id="{hid}" class="role role-{key}">{role}{title}</h2>'
    return re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', tag, body, flags=re.S)


def objective_metadata(site: Site, r: "Renderer", exam: str, body: str) -> str:
    """Separate first-page metadata into scanable labels and link known prerequisites."""
    m = re.search(r'<p><strong>Exam:</strong>(.*?)</p>', body, re.S)
    if not m:
        return body
    text = '<strong>Exam:</strong>' + m.group(1)
    fields = re.split(r'<br\s*/?>\s*', text)
    rows = []
    for field in fields:
        f = re.match(r'<strong>(Exam|Time|Prerequisites|Continue from|Scenario setting):</strong>\s*(.*)', field, re.S)
        if not f:
            continue
        label, value = f.groups()
        if label == 'Prerequisites':
            parts = re.split(r'(<a\b.*?</a>)', value, flags=re.S)
            def link_number(match):
                target = objective_page(site, exam, match.group(0))
                return f'<a href="{html.escape(r.rel_url(target))}">Objective {match.group(0)}</a>' if target else match.group(0)
            value = ''.join(part if part.startswith('<a') else re.sub(r'\b[1-5]\.[1-7]\b', link_number, part) for part in parts)
        rows.append(f'<dt>{label}</dt><dd>{value}</dd>')
    return body.replace(m.group(0), '<dl class="objective-meta">' + ''.join(rows) + '</dl>', 1) if len(rows) >= 3 else body


def objective_nav(site: Site, exam: str, out_rel: str, where: str) -> str:
    """Previous/next for objective lessons. Endpoints offer the course start / the course review instead of an invented neighbour."""
    seq = [(o, n, t) for kids in objective_pages(site, exam).values() for o, n, t in kids]
    outs = [o for o, _, _ in seq]
    if out_rel not in outs:
        return ""
    i = outs.index(out_rel)
    root = "../" * out_rel.count("/")

    def lab(j, side):
        n, t = seq[j][1], seq[j][2]
        d = n.split(".")[0]
        note = ""
        if d != seq[i][1].split(".")[0]:
            note = f" (Domain {d}{' begins' if side == 'next' else ''})"
        return f'<small>Objective {n}{note}</small> {html.escape(t)}'
    if i > 0:
        prev = f'<a class="prev" rel="prev" href="{root}{outs[i-1]}">\u2190 {lab(i-1, "prev")}</a>'
    else:
        prev = f'<a class="prev" href="{root}lessons/{exam}/L00-orientation.html">\u2190 <small>Start of course</small> Lesson 0: orientation</a>'
    if i + 1 < len(outs):
        nxt = f'<a class="next" rel="next" href="{root}{outs[i+1]}">{lab(i+1, "next")} \u2192</a>'
    else:
        nxt = f'<a class="next" href="{root}exams/{exam}.html"><small>End of the {len(seq)} objectives</small> Review in the {EXAMS[exam]["code"]} study plan \u2192</a>'
    pos = f'<span class="objpos">Objective {seq[i][1]} \u00b7 {i+1} of {len(seq)}</span>'
    return f'<nav class="prevnext objnav objnav-{where}" aria-label="Previous and next objective ({where})">{prev}{pos}{nxt}</nav>'


def side_for(site: Site, exam: str, current: str) -> str:
    e = EXAMS[exam]
    root = "../" * current.count("/")
    items = [f'<p class="side-exam"><span class="pill">{e["code"]}</span> {html.escape(e["short"])}</p><ul class="side-list">']

    def li(href, text):
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{root}{href}"{cur}>{text}</a></li>')
    li(f"exams/{exam}.html", "Study plan")
    if exam == "ccar-f":
        li("lessons/ccar-f/architecture-studio/00-foundations.html", "Start: picture an application")
    items.append('<li class="side-h">Lessons</li>')
    objs = objective_pages(site, exam)
    for s, o, _ in site.of("lesson", exam):
        lm = lesson_meta(site.text(s))
        w = f' <span class="w">{lm["weight"]:g}%</span>' if lm["weight"] else ""
        label = f'<b>{Path(s).stem[:3]}</b> {html.escape(lm["name"])}{w}'
        dom = re.match(r"L0(\d)-", Path(s).name)
        kids = objs.get(int(dom.group(1)), []) if dom else []
        if not kids:
            li(o, label)
            continue
        # B63-FX-3: objectives nest under their domain. The current domain is open; closed <details> keeps hidden links out of the tab order.
        is_open = current == o or any(co == current for co, _, _ in kids)
        items.append(f'<li class="side-dom"><details{" open" if is_open else ""}><summary>{label}</summary><ul class="side-objs">')
        li(o, "Domain lesson")
        for co, num, title in kids:
            here = co == current
            mark = '<span class="here"> (you are here)</span>' if here else ""
            cur = ' aria-current="page"' if here else ""
            items.append(f'<li><a href="{root}{co}"{cur}><b>{num}</b> {html.escape(title)}{mark}</a></li>')
        items.append("</ul></details></li>")
    extras = [(s, o) for s, o, m in site.of("extra", exam) if m.get("side")]
    if extras:
        items.append('<li class="side-h">Practice and reference</li>')
        for s, o in extras:
            li(o, html.escape(side_label(site, s)))
    if exam == "ccar-f":  # B63-FX-13: coverage page lives in the sidebar too
        if not extras:
            items.append('<li class="side-h">Practice and reference</li>')
        li("lessons/ccar-f/objectives/practice-coverage.html", "Practice coverage by objective")
        li("lessons/ccar-f/objectives/progress.html", "Your progress (this browser)")
        li("lessons/ccar-f/scenario-walkthroughs/signals-and-errors.html", "Signals, errors and missed what-ifs")
    items.append('<li class="side-h">Simulations</li>')
    for s, o, _ in site.of("sim", exam):
        li(o, f'<b>{"-".join(Path(s).stem.split("-")[:2])}</b> {html.escape(short_title(site.text(s)))}')
    items.append('<li class="side-h">Labs</li>')
    for s, o, m in site.of("lab"):
        if m["lab"] in e["labs"]:
            li(o, f'<b>Lab {m["lab"]}</b> {html.escape(short_title(site.text(s)))}')
    items.append("</ul>")
    return "".join(items)


def prev_next(site: Site, out_rel: str, exam: str, kind: str) -> str:
    seq = [(o, s) for s, o, _ in site.of(kind, exam)]
    outs = [o for o, _ in seq]
    if out_rel not in outs:
        return ""
    i = outs.index(out_rel)
    root = "../" * out_rel.count("/")

    def label(j):
        s = seq[j][1]
        tag = (Path(s).stem.split("-")[0] if kind == "lesson" else f"Lab {Path(s).parent.name[:2]}" if kind == "lab"
               else "-".join(Path(s).stem.split("-")[:2]))
        return f'<small>{tag}</small> {html.escape(short_title(site.text(s)))}'
    parts = ['<nav class="prevnext" aria-label="Previous and next">']
    parts.append(f'<a class="prev" href="{root}{outs[i-1]}">← {label(i-1)}</a>' if i > 0 else "<span></span>")
    back = (f'<a class="next" href="{root}exams/{exam}.html">Back to the {EXAMS[exam]["code"]} plan →</a>' if exam
            else f'<a class="next" href="{root}labs/index.html">All labs →</a>')
    parts.append(f'<a class="next" href="{root}{outs[i+1]}">{label(i+1)} →</a>' if i + 1 < len(outs) else back)
    parts.append("</nav>")
    return "".join(parts)


DECK_EXPORTS = {"FLASHCARDS.md": "flashcards-anki.csv"}  # maintained, project-authored exports generated beside the deck


def deck_rows(path: Path) -> list[list[str]]:
    """The export's card rows (front, back, tags), header dropped. Empty when the export is absent."""
    if not path.exists():
        return []
    rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8"))))
    return [r for r in rows[1:] if r]


FC_CARD = re.compile(r'<p><strong>(\d+)\.</strong>( <strong>TRAP</strong>)?</p>\s*<p>Q: (.*?)</p>\s*<p>A: (.*?)</p>\s*'
                     r'(<p>Source: .*?</p>)', re.S)


def flashcard_deck(body: str, src_rel: str, csv_href: str | None, n_csv: int, site: "Site") -> str:
    """B63-FX-5: question-first cards. Each answer sits in its own closed disclosure (keyboard and tap, no page jump),
    each objective links to its teaching page, and a Reference mode opens every answer. Card text and sources are kept."""
    heads = [(m.start(), m.group(1)) for m in re.finditer(r'<h3 id="[^"]*">(\d\.\d+) ', body)]
    obj_dir = Path(src_rel).parent / "objectives"

    def card(m):
        n, trap, q, a, source = m.groups()
        obj = next((o for pos, o in reversed(heads) if pos < m.start()), None)
        ctx = f" · Objective {obj}" if obj else ""
        kind = ' · <span class="fc-trap">TRAP: name why it is wrong</span>' if trap else ""
        return (f'<div class="fc" id="card-{n}"><p class="fc-meta"><b>Card {n}</b>{ctx}{kind}</p>'
                f'<p class="fc-q">{q}</p><details class="fc-a"><summary>Show answer'
                f'<span class="sr-only"> to card {n}</span></summary><p>{a}</p>{source}</details></div>')

    body, n_cards = FC_CARD.subn(card, body)

    def teach(m):
        obj = m.group(2)
        if (obj_dir / f"objective-{obj}.md").as_posix() not in site.pages:
            return m.group(0)
        return m.group(0) + f'<p class="fc-teach"><a href="objectives/objective-{obj}.html">Study objective {obj}</a> before or after these cards.</p>'

    body = re.sub(r'(<h3 id="[^"]*">(\d\.\d+) .*?</h3>)', teach, body)
    if csv_href and n_csv == n_cards:
        imp = (f'<a href="{csv_href}" download>Download the deck</a> ({Path(csv_href).name}: CSV, {n_csv} cards; '
               f'columns front, back, tags) for Anki or Quizlet.')
    else:  # no maintained export that matches the page, so no download is offered
        imp = "no downloadable copy of this deck is available; study it here in the browser."
        if csv_href:
            site.problems.append(f"{src_rel}: deck export has {n_csv} cards, page has {n_cards}; download withheld")
    body = re.sub(r'<strong>Import:</strong>.*?(?=</p>)', lambda _: f"<strong>Import:</strong> {imp}", body, count=1, flags=re.S)
    bar = (f'<div class="fc-bar" role="group" aria-label="Deck mode"><p><b>Study mode:</b> {n_cards} cards, answers hidden. '
           'Say your answer, then open it. <button type="button" class="fc-all" aria-pressed="false">'
           'Reference mode: show all answers</button></p>'
           '<p class="fc-note">Opening an answer is a self-check, not a score. Nothing here records or shows mastery.</p></div>')
    return re.sub(r'(<h2 id="domain-1)', lambda m: bar + m.group(1), body, count=1)


def toc(headings) -> str:
    h2 = [(hid, t) for lvl, hid, t in headings if lvl == 2]
    if len(h2) < 4:
        return ""
    # Page navigation (this page's sections), labeled apart from the Course outline. Open on wide screens
    # (site.js closes it on phones); long outlines show the first 8 and tuck the rest under "Show all".
    lis = [f'<li><a href="#{hid}">{html.escape(t)}</a></li>' for hid, t in h2]
    more = ""
    if len(lis) > 10:
        more = (f'<details class="toc-more"><summary>Show {len(lis) - 8} more sections</summary><ol start="9">'
                + "".join(lis[8:]) + "</ol></details>")
        lis = lis[:8]
    return (f'<nav class="toc-nav" aria-label="Sections on this page"><details class="toc">'
            f'<summary>Sections on this page ({len(h2)})</summary><ol>' + "".join(lis) + "</ol>" + more
            + "</details></nav>")


# ---------------------------------------------------------------- generated pages

def weight_bars(site: Site, exam: str, from_root: str, link=True) -> str:
    rows = [(lesson_meta(site.text(s)), o) for s, o, _ in site.of("lesson", exam)]
    rows = sorted((r for r in rows if r[0]["weight"]), key=lambda r: -r[0]["weight"])
    mx = max((r[0]["weight"] for r in rows), default=1)
    out = [f'<ul class="bars{"" if link else " compact"}" aria-label="Domain weights">']
    for lm, href in rows:
        label = html.escape(lm["name"])
        if link:
            label = f'<a href="{from_root}{href}">{label}</a>'
        out.append(f'<li><span class="bl">{label}</span><span class="bt" aria-hidden="true"><span class="bf" style="width:{lm["weight"]/mx*100:.0f}%"></span></span>'
                   f'<span class="bv">{lm["weight"]:g}%</span></li>')
    out.append("</ul>")
    return "".join(out)


def counts(site: Site, exam: str) -> dict:
    sims = [s for s, _, _ in site.of("sim", exam)]
    return dict(lessons=len(list(site.of("lesson", exam))), sims=len(sims),
                scen=len([s for s in sims if not s.endswith("SIM-01-full-mock.md")]), labs=len(EXAMS[exam]["labs"]))


def curriculum_map() -> str:
    lanes = [("Associate", "associate", [("CCAO-F", "ccao-f", "Foundations")]),
             ("Architect", "architect", [("CCAR-F", "ccar-f", "Foundations"), ("CCAR-P", "ccar-p", "Professional")]),
             ("Developer", "developer", [("CCDV-F", "ccdv-f", "Foundations")])]
    w, lh = 760, 78
    p = [f'<svg class="map" viewBox="0 0 {w} {lh*3+12}" role="img" aria-labelledby="map-t map-d">',
         '<title id="map-t">Curriculum map</title>',
         '<desc id="map-d">Three tracks. Associate: CCAO-F. Architect: CCAR-F, then CCAR-P; CCAR-F is recommended first but not required. Developer: CCDV-F, which overlaps about two-thirds with CCAR-F.</desc>',
         '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z"/></marker></defs>']
    for i, (lane, color, nodes) in enumerate(lanes):
        y = 6 + i * lh
        p.append(f'<g class="lane l-{color}"><rect class="lane-bg" x="0" y="{y}" width="{w}" height="{lh-10}" rx="12"/>'
                 f'<text x="20" y="{y+40}" class="lane-t">{lane}</text>')
        for j, (code, key, lvl) in enumerate(nodes):
            x = 190 + j * 300
            p.append(f'<a href="exams/{key}.html" class="node" data-code="{code}"><rect x="{x}" y="{y+10}" width="210" height="{lh-30}" rx="10"/>'
                     f'<text x="{x+16}" y="{y+33}" class="node-c">{code}</text><text x="{x+16}" y="{y+51}" class="node-l">{lvl}</text></a>')
            if j:
                p.append(f'<path class="edge" d="M{x-88} {y+34} H{x-6}" marker-end="url(#arr)"/>'
                         f'<text x="{x-86}" y="{y+26}" class="edge-t">recommended</text>')
        p.append("</g>")
    p.append("</svg>")
    return "".join(p)


def latest_update(site: Site) -> str:
    """The newest release heading from the repo CHANGELOG, as a one-line note on the home page."""
    f = REPO / "CHANGELOG.md"
    m = re.search(r"^## (v[\d.]+) — ([\d-]+) — (.+)$", f.read_text(), re.M) if f.exists() else None
    if not m:
        return ""
    return (f'<p class="latest small"><b>Latest update:</b> {html.escape(m.group(1))}, {html.escape(m.group(2))}: '
            f'{html.escape(m.group(3))} · <a href="whats-new.html">What\'s new</a> · <a href="faq.html">FAQ</a></p>')


def build_home(site: Site) -> str:
    cards = []
    for key, e in EXAMS.items():
        c = counts(site, key)
        cards.append(f"""
<article class="card c-{e['color']}">
  <p class="card-k"><span class="pill">{e['code']}</span> {e['track']} · {e['level']}</p>
  <h3><a href="exams/{key}.html">{html.escape(e['name'])}</a></h3>
  <p class="card-who">{html.escape(e['who'])}</p>
  <dl class="facts">
    <div><dt>Questions</dt><dd>{e['questions']}</dd></div><div><dt>Time</dt><dd>120 min</dd></div>
    <div><dt>Pass</dt><dd>720</dd></div><div><dt>List price</dt><dd>${e['price']}</dd></div>
    <div><dt>Study</dt><dd>{e['hours'][0]}–{e['hours'][1]} h</dd></div>
  </dl>
  {weight_bars(site, key, "", link=False)}
  <p class="card-count">{c['lessons']} lessons · {c['scen']} scenario simulations + mock plan · {c['labs']} {"lab" if c['labs'] == 1 else "labs"}</p>
  <a class="btn" href="exams/{key}.html">Open the {e['code']} plan</a>
</article>""")
    hours = html.escape(json.dumps({EXAMS[k]["code"]: [EXAMS[k]["hours"], k] for k in EXAMS}), quote=True)
    return f"""
<section class="hero">
  <p class="eyebrow">Four Anthropic exams · three tracks · one plan</p>
  <h1>Pass the Claude certifications, one clear step at a time.</h1>
  <p class="lede">Lessons written from Anthropic's own exam guides and docs, scenario simulations with coach keys,
  hands-on labs, and what colleagues who passed wish they'd known.</p>
  <p class="start"><b>Where to start:</b> if you don't write code, start with <a href="exams/ccao-f.html">CCAO-F</a> (8–12 hours, $99).
  If you design or build with Claude, start with <a href="exams/ccar-f.html">CCAR-F</a>: Anthropic's partner training advised architects to start there (relayed by a colleague, see <a href="insights.html">Insights</a>), and a colleague who passed all four says everything else builds on it.</p>
  <div class="hero-cta"><a class="btn" href="#paths">Choose your path</a> <a class="btn ghost" href="curriculum.html">See the whole curriculum</a></div>{latest_update(site)}
</section>
<section id="paths" class="block">
  <h2>Which path fits you?</h2>
  <div class="chooser" role="group" aria-label="Pick your role">
    <button type="button" data-path="CCAO-F,CCAR-F" aria-pressed="false"><b>I don't write code</b><small>I help teams use Claude. CCAO-F first teaches the question style, then CCAR-F.</small></button>
    <button type="button" data-path="CCAR-F,CCAR-P" aria-pressed="false"><b>I design Claude solutions</b><small>Architect Foundations, then Professional while it's fresh.</small></button>
    <button type="button" data-path="CCAR-F,CCDV-F" aria-pressed="false"><b>I write code with Claude</b><small>CCAR-F, then CCDV-F within two weeks: they overlap by about two-thirds.</small></button>
    <button type="button" data-path="CCAR-F,CCAR-P,CCDV-F,CCAO-F" aria-pressed="true"><b>I want all four</b><small>The core exam first, the easiest last.</small></button>
  </div>
  <div class="planner" data-hours="{hours}">
    <label for="hpw">Hours a week I can study: <output id="hpw-out" for="hpw">8</output></label>
    <input id="hpw" type="range" min="2" max="20" value="8">
    <ol class="plan-out" aria-live="polite"></ol>
    <p class="muted small">Uses the upper end of each exam's study-hours range. The reasons for each order are in the <a href="curriculum.html#1-recommended-order-it-depends-on-who-you-are">curriculum</a>.</p>
  </div>
  <div class="curriculum-map-frame" tabindex="0" role="group" aria-label="Curriculum map; scroll horizontally on narrow screens">{curriculum_map()}</div><p class="map-scroll-hint">On a narrow screen, scroll the map left and right. Each exam box is a link.</p>
</section>
<section class="block">
  <h2>The four exams</h2>
  <div class="cards">{''.join(cards)}</div>
  <p class="src-note">Question counts, time, pass mark and price: the official exam guides, section 5. Study hours: this curriculum.</p>
</section>
<section class="block">
  <h2>How every exam is studied here</h2>
  <ol class="steps">
    <li><b>Choose a learning route</b><span>Start with your exam plan. For CCAR-F, use <a href="lessons/ccar-f/concept-course/index.html">concept coaching</a> before deeper objectives when the application is unfamiliar.</span></li>
    <li><b>Learn or diagnose</b><span>Build understanding first when you are new. Experienced learners can use an optional diagnostic to identify weak domains, then repair them.</span></li>
    <li><b>Connect lessons and objectives</b><span>Follow the recommended route, trace the data and compare technical alternatives. Use domain weights to allocate practice, not to skip prerequisites.</span></li>
    <li><b>Trace and practise</b><span>Begin with the supplied paper exercises, then follow each relevant lab's prerequisites. Keep simulated controls and actual tool execution evidence separate.</span></li>
    <li><b>Simulate decisions</b><span>Commit to a mechanism before opening the coach key. Explain alternatives and retry later with a changed constraint.</span></li>
    <li><b>Check readiness, then book</b><span>Review fresh decisions and remaining objective gaps before choosing an exam date. Practice scores do not predict certification marks; confirm current registration and ID requirements.</span></li>
  </ol>
</section>
<section class="block">
  <h2>Where the facts come from</h2>
  <div class="tier-row">
    <div class="tier t1"><b>Tier 1 · Anthropic original</b><span>Exam guides, docs, Anthropic Academy courses, Anthropic posts and videos. Always wins.</span></div>
    <div class="tier t2"><b>Tier 2 · Guides and lessons by others</b><span>Study guides, courses, repos and video lessons. Only where Tier 1 is silent, and labelled.</span></div>
    <div class="tier t3"><b>Tier 3 · Blogs and sites</b><span>Useful for ideas. Never the only source for a fact.</span></div>
    <div class="tier tf"><b>Field reports</b><span>What colleagues who passed said. Changes emphasis, never facts.</span></div>
  </div>
</section>
"""


def build_ccarf_concept_entry() -> str:
    """One scenario-first route; concepts are explained where the decision arises."""
    jobs = [
        ('as-01-action-service', 'Resolve a customer case', 'An order, a refund request and a receipt', 'Identity, tool selection, authorization, safe recovery and human handoff', 'WT-01-customer-support-agent', 'SIM-02-customer-support-agent'),
        ('as-02-document-pipeline', 'Turn documents into trustworthy records', 'Invoices and imperfect scans become checked records', 'Missing facts, receiving-side validation, review and partial failures', 'WT-06-structured-data-extraction', 'SIM-07-structured-data-extraction'),
        ('as-03-grounded-assistant', 'Answer from authorized sources', 'A question and a restricted evidence packet', 'Retrieval, current evidence, MCP and source attribution', 'WT-03-multi-agent-research', 'SIM-04-multi-agent-research'),
        ('as-04-research-system', 'Investigate an unfamiliar question', 'A broad comparison becomes an evidence-backed recommendation', 'Decomposition, specialist briefs, handoff validation and incomplete findings', 'WT-03-multi-agent-research', 'SIM-04-multi-agent-research'),
        ('as-05-code-change', 'Change an unfamiliar application', 'A business request becomes a focused, verified code change', 'Search, instruction scope, planning and cross-file review', 'WT-02-code-generation-claude-code', 'SIM-03-code-generation-claude-code'),
        ('as-06-ci-review', 'Review a change with nobody at the keyboard', 'A code diff becomes reliable machine-readable findings', 'Headless execution, output contracts, precision and honest failure', 'WT-05-claude-code-ci-cd', 'SIM-06-claude-code-ci-cd'),
        ('as-07-work-queue', 'Handle urgent and overnight work', 'Many jobs finish at different times, and some fail', 'Dependencies, deadlines, item IDs, retries and reconciliation', 'WT-06-structured-data-extraction', 'SIM-07-structured-data-extraction'),
        ('as-08-resumable-case', 'Continue a case after the world changes', 'A checkpoint meets changed facts and permissions', 'Context, fresh evidence, resume/fork and durable state', 'WT-04-developer-productivity', 'SIM-05-developer-productivity'),
    ]
    cards = ''.join(f'<section class="scn-card"><h3><a href="../lessons/ccar-f/architecture-studio/{slug}.html">{title}</a></h3><p>{scene}.</p><p><b>Decisions:</b> {decisions}.</p><p><a href="../lessons/ccar-f/architecture-studio/{slug}.html">Learn the story</a> · <a href="../lessons/ccar-f/scenario-walkthroughs/{wt.lower()}.html">Walk through the family</a> · <a href="../simulations/ccar-f/{sim}.html">Try independently</a></p></section>' for slug,title,scene,decisions,wt,sim in jobs)
    return f"""
<section class="block prose" id="ccarf-learning-route">
<nav aria-label="Your next CCAR-F study action" class="variant-links">
<a href="../lessons/ccar-f/architecture-studio/00-foundations.html">Learn · understand an application</a> ·
<a href="../labs/08-CCAR-F-architecture-decisions.html">Build · prove a decision</a> ·
<a href="../practice/index.html?exam=CCAR-F">Practice · fresh questions or saved session</a> ·
<a href="../simulations/ccar-f/SIM-01-full-mock.html">Mock · rehearse independently</a> ·
<a href="../lessons/ccar-f/last-minute-prep.html">Reference · checklist and PDF</a>
</nav>
<p><b>Suggested next action:</b> new to application architecture? Start with the application below. Returning to a saved question? <a href="../practice/index.html?exam=CCAR-F&amp;resume=1">Resume practice</a>; if no session is saved, choose practice settings.</p>
<h2>Learn architecture through situations you can picture</h2>
<p>A customer asks a support representative for a refund. A screen sends the request to your application; Claude helps interpret it, tools retrieve evidence, and trusted application code decides whether a protected action may run. A receipt shows what actually happened. Start with that simple story, then see what changes when something fails.</p>
<p><a class="btn" href="../lessons/ccar-f/architecture-studio/00-foundations.html">Start learning: picture one application</a></p>
<p>Reading and paper exercises need no installation. Each runnable lab states its setup. Start with the customer case, or choose a familiar job below. You do not need to complete a separate technical course first.</p>
<h3>Choose a job, then build its architecture layer by layer</h3>
<p><b>See it work → see what breaks → answer a technical decision question → explain it simply → add the repair → prove it → change a constraint.</b> Questions are original exam-style practice, not actual exam items. Everyday explanations follow the question and choices; optional hints do not replace the technical decision.</p>
<div class="scenario-map">{cards}</div>
<p><a href="../lessons/ccar-f/concept-course/06-putting-it-together.html">Put the whole bank assistant together</a> connects identity, tools, state, privacy, evaluation and cost in one evolving application.</p>
<h3>Practise, repair and remember</h3>
<p><a href="../lessons/ccar-f/decision-variants.html">Rehearse all 30 changed-constraint decisions</a> · <a href="../practice/index.html?exam=CCAR-F">Practice and timed mocks</a> · <a href="../lessons/ccar-f/flashcards.html">Recall later</a> · <a href="../lessons/ccar-f/last-minute-prep.html">Last-minute checklist and PDF</a>.</p>
<p><a href="../lessons/ccar-f/learning-journey.html">Follow the full learning-to-exam route</a>. For a decision you miss, use its explanation and return to the same practice state.</p>
<details><summary>Concept explanations, objective coverage and references</summary><p><a href="../lessons/ccar-f/concept-course/index.html">Six concept explanations</a> · <a href="../lessons/ccar-f/objectives/index.html">All 30 objectives</a> · <a href="../lessons/ccar-f/decision-atlas.html">Architecture drawings</a> · <a href="../lessons/ccar-f/mechanism-clinic.html">Compare similar mechanisms</a> · <a href="../lessons/ccar-f/skill-coverage.html">Exact coverage and assessment limits</a>.</p><p>The saved mapping reports 44 of 240 skill bullets with dedicated reviewed diagnostics and 196 without. New guided teaching does not itself establish independent assessment coverage. The six saved-guide families, eight application cases and 30 variants overlap and do not exhaust possible exam stories. Industry examples are teaching choices, not official industry weighting.</p></details>
</section>
"""


def build_exam(site: Site, key: str, curriculum_html: str) -> str:
    e, c = EXAMS[key], counts(site, key)

    def lesson_li(s, o):
        lm = lesson_meta(site.text(s))
        w = f'{lm["weight"]:g}%' if lm["weight"] else "start here"
        return f'<li><a href="../{o}"><b>{Path(s).stem[:3]}</b> {html.escape(lm["name"])}</a><span class="w">{w}</span></li>'
    lessons = "".join(lesson_li(s, o) for s, o, _ in site.of("lesson", key))
    sims = "".join(f'<li><a href="../{o}"><b>{"-".join(Path(s).stem.split("-")[:2])}</b> {html.escape(short_title(site.text(s)))}</a></li>'
                   for s, o, _ in site.of("sim", key))
    labs = "".join(f'<li><a href="../{o}"><b>Lab {m["lab"]}</b> {html.escape(short_title(site.text(s)))}</a></li>'
                   for s, o, m in site.of("lab") if m["lab"] in e["labs"])
    extras = [(s, o) for s, o, m in site.of("extra", key) if m.get("side")]
    extra_li = "".join(f'<li><a href="../{o}">{html.escape(side_label(site, s))}</a></li>'
                       for s, o in extras)
    extras_kit = f'<h3>Practice and reference ({len(extras)})</h3><ul class="linklist">{extra_li}</ul>' if extras else ""
    if key == "ccar-f":  # B63-FX-13
        extras_kit += ('<p><a href="../lessons/ccar-f/objectives/practice-coverage.html">Practice coverage by objective</a>: '
                       'which objectives the shared questions test, the gaps, and industry cases by objective.</p>')
    study_time = 'Core 20–25 h; extra study varies' if key == 'ccar-f' else f"{e['hours'][0]}–{e['hours'][1]} h"
    lesson_label = 'Core summaries' if key == 'ccar-f' else 'Lessons'
    app_kit = '<h3>Coached application course</h3><p><a href="../lessons/ccar-f/learning-journey.html">Full teaching-to-exam journey</a> · <a href="../lessons/ccar-f/architecture-studio/index.html">Primer and eight applications</a> · <a href="../lessons/ccar-f/objectives/index.html">30 objective lessons</a></p>' if key == 'ccar-f' else ''
    return f"""
<section class="exam-hero c-{e['color']}">
  <p class="eyebrow"><span class="pill">{e['code']}</span> {e['track']} track · {e['level']}</p>
  <h1>{html.escape(e['name'])}</h1>
  <p class="lede">{html.escape(e['who'])}</p>
{'<p><a class="btn" href="../lessons/ccar-f/architecture-studio/00-foundations.html">Start learning: picture an application</a> · <a href="#ccarf-learning-route">Choose your next study step</a></p>' if key == "ccar-f" else ""}
  {'<details class="exam-facts"><summary>Exam facts and study-time estimate</summary>' if key == "ccar-f" else ""}
  <dl class="facts big">
    <div><dt>Questions</dt><dd>{e['questions']}</dd></div><div><dt>Time</dt><dd>120 min</dd></div>
    <div><dt>Pass mark</dt><dd>720 of 1,000</dd></div><div><dt>List price</dt><dd>${e['price']}</dd></div>
    <div><dt>Study time</dt><dd>{study_time}</dd></div><div><dt>Valid</dt><dd>12 months</dd></div>
  </dl>
  <p class="src-note">Source: the official {e['code']} exam guide, "Exam Details at a Glance" (section {3 if key == 'ccar-f' else 5}) (<a class="ext" href="{OFFICIAL_CERTS}" rel="noopener">Partner Academy</a>). Study time is our own estimate, not Anthropic's.
  Items are multiple-choice or multiple-response; each one says how many answers to pick. Renewing on time is a free online assessment.</p>
  {review_line(key)}
  {'</details>' if key == "ccar-f" else ""}
</section>
{build_ccarf_concept_entry() if key == "ccar-f" else ""}
<section class="block two">
  <div><h2>Domain weights</h2><p class="muted">Use weights to guide emphasis, then adjust for your objective gaps. Click a domain to open its lesson.</p>
  {weight_bars(site, key, "../")}</div>
  <div class="kit">
    <h2>Your study kit</h2>
    {app_kit}<h3>{lesson_label} ({c['lessons']})</h3><ul class="linklist">{lessons}</ul>
    <h3>Simulations ({c['scen']} scenarios + mock plan)</h3><ul class="linklist">{sims}</ul>
    <h3>Labs ({c['labs']})</h3><ul class="linklist">{labs}</ul>
    {extras_kit}
  </div>
</section>
{"" if 'id="before-you-book"' in curriculum_html else f'''<section class="block before-book">
  <h2>Before you book</h2>
  <ul class="plain">
    <li><label class="check"><input type="checkbox" data-k="exams/{key}.html#bb1"><span>Register on the Partner Academy with your <b>work email</b>, and sign in with it directly, not "Sign in with Google".</span></label></li>
    <li><label class="check"><input type="checkbox" data-k="exams/{key}.html#bb2"><span>Check the price at checkout. If you'll be charged, get expense or training pre-approval <b>before</b> you pay.</span></label></li>
    <li><label class="check"><input type="checkbox" data-k="exams/{key}.html#bb3"><span>Make your profile name match your government photo ID exactly.</span></label></li>
    <li><label class="check"><input type="checkbox" data-k="exams/{key}.html#bb4"><span>Testing online? Run the OnVUE system test on the <b>same laptop</b> a few days ahead. Company-managed laptops have blocked it; if the test fails, book a test center.</span></label></li>
  </ul>
  <p class="src-note">Sources: official guide sections 10–11 (registration and ID); field reports, see <a href="../insights.html#registration-price-and-paying">Insights</a> and <a href="../insights.html#exam-day">Exam day</a>.</p>
</section>'''}
<section class="block prose">
<h2 id="study-plan">Study plan</h2>
{curriculum_html}
</section>
"""


def build_study_index(site: Site, kind: str) -> str:
    if kind == "lab":
        out = ['<h1>Labs</h1><p class="lede">Choose a lab and check its prerequisites. Local simulations and actual API/MCP builds provide different execution evidence.</p><div class="cards">']
        for s, o, m in site.of("lab"):
            used = [k for k, e in EXAMS.items() if m["lab"] in e["labs"]]
            pills = " ".join(f'<a class="pill p-{EXAMS[k]["color"]}" href="../exams/{k}.html">{EXAMS[k]["code"]}</a>' for k in used)
            out.append(f'<article class="card"><p class="card-k">Lab {m["lab"]}</p><h3><a href="../{o}">{html.escape(site.title(s))}</a></h3>'
                       f'<p class="card-who">Used by {pills}</p></article>')
        return "".join(out) + "</div>"
    label = {"lesson": "Lessons", "sim": "Simulations"}[kind]
    lede = {"lesson": "One lesson per exam domain. Read it, do its Try it, and check the Done when before moving on.",
            "sim": "How to run one: read the scene, answer the decisions on paper (or paste the scene and the decisions list into Claude and ask it to quiz you), then open the coach key. About 16–20 minutes each; each page says its pass mark. SIM-01 is the full mock-exam plan."}[kind]
    out = [f'<h1>{label}</h1><p class="lede">{lede}</p><div class="cards">']
    for key, e in EXAMS.items():
        items = []
        for s, o, _ in site.of(kind, key):
            tag = Path(s).stem[:3] if kind == "lesson" else "-".join(Path(s).stem.split("-")[:2])
            w = ""
            if kind == "lesson":
                lm = lesson_meta(site.text(s))
                w = f'<span class="w">{lm["weight"]:g}%</span>' if lm["weight"] else '<span class="w">start</span>'
            items.append(f'<li><a href="../{o}"><b>{tag}</b> {html.escape(site.title(s))}</a>{w}</li>')
        out.append(f'<article class="card c-{e["color"]}"><p class="card-k"><span class="pill">{e["code"]}</span> {e["track"]} · {e["level"]}</p>'
                   f'<h3><a href="../exams/{key}.html">{html.escape(e["name"])}</a></h3><ul class="linklist">{"".join(items)}</ul></article>')
    return "".join(out) + "</div>"


RESOURCES = {
    "Tier 1 · Anthropic original": [
        ("Partner Academy: certifications and exam guides", OFFICIAL_CERTS, "Exam pages, official guides, registration"),
        ("Pearson VUE: Anthropic exams", "https://www.pearsonvue.com/us/en/anthropic.html", "Scheduling, ID and test-day rules"),
        ("Anthropic Academy", "https://anthropic.skilljar.com/", "AI Fluency, Claude 101, Building with the Claude API, Claude Code in Action, MCP courses"),
        ("Claude developer docs", "https://platform.claude.com/docs/en/home", "The API, models, tools, caching, batch and structured outputs"),
        ("Prompt engineering overview", "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview", "CCAO-F L01 · CCAR-F L04 · CCDV-F L04"),
        ("Choosing a model", "https://platform.claude.com/docs/en/about-claude/models/choosing-a-model", "CCAO-F L03 · CCDV-F L02 · CCAR-P L06"),
        ("Tool use", "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview", "CCAR-F L02 · CCDV-F L05"),
        ("Prompt caching", "https://platform.claude.com/docs/en/build-with-claude/prompt-caching", "CCDV-F L01–L02 · Lab 04"),
        ("Batch processing", "https://platform.claude.com/docs/en/build-with-claude/batch-processing", "CCDV-F L01 · Lab 04"),
        ("Structured outputs", "https://platform.claude.com/docs/en/build-with-claude/structured-outputs", "CCAR-F L04 · Lab 02"),
        ("Claude Code docs", "https://docs.claude.com/en/docs/claude-code/overview", "CCAR-F L03 · CCDV-F L07 · CCAR-P L07"),
        ("Building effective agents", "https://www.anthropic.com/engineering/building-effective-agents", "CCAR-F L01 · CCAR-P L02"),
        ("Model Context Protocol", "https://modelcontextprotocol.io", "CCAR-F L02 · CCDV-F L05 · CCAR-P L01"),
        ("Claude's constitution", "https://www.anthropic.com/constitution", "Background for the governance lessons"),
    ],
    "Tier 2 · Guides and lessons by others": [
        ("Amey Thakur: CLAUDE-CERTIFICATIONS", "https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS", "Notes, cheat sheets and mocks for all four exams"),
        ("dnacenta: claude-certified-architect", "https://github.com/dnacenta/claude-certified-architect", "CCAR-F notes by domain"),
    ],
}


def build_resources() -> str:
    out = ['<h1>Resources</h1><p class="lede">Start with Tier 1. Use Tier 2 only where Anthropic\'s own material is silent, '
           'and check it against Tier 1. Practice-question banks by other authors aren\'t copied here; follow their links.</p>']
    for tier, items in RESOURCES.items():
        cls = "t1" if tier.startswith("Tier 1") else "t2"
        out.append(f'<section class="block"><h2 class="tier-h {cls}">{html.escape(tier)}</h2><ul class="res">')
        out += [f'<li><a class="ext" href="{u}" rel="noopener">{html.escape(n)}</a><span>{html.escape(use)}</span></li>' for n, u, use in items]
        out.append("</ul></section>")
    out.append('<section class="block"><h2>Video lessons</h2><p>Videos are being transcribed and reviewed before they\'re added. '
               'A video counts as Tier 1 only if it\'s from Anthropic\'s own channel; other channels are Tier 2.</p></section>')
    return "".join(out)


def build_about() -> str:
    return """
<h1>About this site</h1>
<p class="lede">A study site for colleagues preparing for Anthropic's four Claude certifications. It covers Claude and Anthropic only.</p>
<section class="block prose">
<h2 id="whats-here">What's here</h2>
<ul>
<li>A plan for each exam, with a checklist that remembers your ticks in this browser.</li>
<li>One lesson per exam domain, written from the official exam guide and Anthropic's docs.</li>
<li>Scenario simulations: eight to ten decisions each, with a coach key to open when you're done.</li>
<li>For CCAR-F: deep practice by domain, decision charts and sequence diagrams, objective pages, flashcards and hard drills.</li>
<li>Five hands-on labs, and what colleagues who passed said. Names are withheld until each person agrees.</li>
</ul>
<h2 id="whats-not-here-on-purpose">What's not here, on purpose</h2>
<ul>
<li><b>No real exam questions.</b> Candidates sign a confidentiality agreement, and we respect it.</li>
<li><b>No copied question banks.</b> Practice sets by other people stay with their authors; see Resources.</li>
<li><b>No personal scores,</b> no tracking, no cookies and no calls to other sites.</li>
</ul>
<h2 id="third-party-code">Third-party code</h2>
<p>The diagrams are drawn in your browser by <a class="ext" href="https://github.com/mermaid-js/mermaid" rel="noopener">Mermaid</a> 12.1.0 (MIT licence). A copy ships with the site, with <a href="assets/vendor/LICENSE-mermaid.txt">its licence</a>, so nothing is loaded from outside.</p>
<h2 id="source-tiers">Source tiers</h2>
<div class="tbl"><table><thead><tr><th>Tier</th><th>What counts</th><th>How it's used</th></tr></thead><tbody>
<tr><td><b>1 · Anthropic original</b></td><td>Exam guides and FAQs, Claude docs, Anthropic Academy courses, Anthropic posts, Anthropic's YouTube channel</td><td>Taught first. Always wins a conflict.</td></tr>
<tr><td><b>2 · Guides and lessons by others</b></td><td>Study guides, courses, repos and video lessons</td><td>Only where Tier 1 is silent, and labelled</td></tr>
<tr><td><b>3 · Blogs and sites</b></td><td>Articles, posts and practice sites</td><td>Never the only source for a fact</td></tr>
<tr><td><b>Field reports</b></td><td>Debriefs from colleagues who passed</td><td>Change emphasis (hours, order, practice), never facts</td></tr>
</tbody></table></div>
<h2 id="studying-with-claude">Studying with Claude</h2>
<p>Paste any lesson into Claude and say <em>"Teach me this in short parts and check my understanding."</em>
For a simulation, say <em>"Run this simulation: one decision at a time, four options, no hints, and score me at the end."</em></p>
<h2 id="found-a-problem">Found a problem, or have an idea?</h2>
<p>Use the <b>Report a problem on this page</b> link at the bottom of any page, or see <a href="contribute.html">Contribute</a> for ideas, content requests and exam debriefs. Every defect gets a root cause and a check that stops it coming back. Common questions are in the <a href="faq.html">FAQ</a>, and each release is listed in <a href="whats-new.html">What's new</a>.</p>
</section>
"""


def build_style_guide(site: Site) -> str:  # noqa: ARG001
    """Generate the Design style guide page, parsed live from site.css tokens."""
    css_text = (ASSETS_SRC / "site.css").read_text()

    def _lum(h: str) -> float:
        h = h.lstrip("#")
        rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    def _cr(a: str, b: str) -> float:
        la, lb = sorted((_lum(a), _lum(b)), reverse=True)
        return (la + 0.05) / (lb + 0.05)

    def _expand3(h: str) -> str:
        """Expand a 3-digit hex colour to 6 digits."""
        s = h.lstrip("#")
        if len(s) == 3:
            s = s[0] * 2 + s[1] * 2 + s[2] * 2
        return "#" + s

    ALL_GUIDE_TOKENS = [
        "bg", "surface", "sunk", "ink", "muted", "line", "accent",
        "associate", "architect", "developer",
        "associate-soft", "architect-soft", "developer-soft",
        "t1", "t2", "t3", "tf",
    ]
    _GUIDE_SET = set(ALL_GUIDE_TOKENS)

    def _block(sel: str, required: bool = False) -> dict:
        m = re.search(re.escape(sel) + r"\s*\{(.*?)\}", css_text, re.S)
        if not m:
            if required:
                sys.exit(
                    f"build_style_guide: CSS block '{sel}' not found in site.css. "
                    "Check that the selector exists in site/assets/site.css."
                )
            return {}
        block_text = m.group(1)
        # Detect any hex value that isn't exactly 3 or 6 digits and fail loudly.
        bad_hex = [
            (n, v)
            for n, v in re.findall(r"--([\w][\w-]*):\s*(#[0-9a-fA-F]+)\b", block_text)
            if len(v.lstrip("#")) not in (3, 6)
        ]
        if bad_hex:
            sys.exit(
                f"build_style_guide: unsupported hex value(s) in '{sel}' block: "
                + ", ".join(f"--{n}: {v}" for n, v in bad_hex)
                + ". Use #rgb or #rrggbb only."
            )
        # Detect guide tokens whose value is rgb/hsl/var or any other non-hex colour syntax.
        _valid_hex = re.compile(r"#[0-9a-fA-F]{3}$|#[0-9a-fA-F]{6}$")
        for prop_m in re.finditer(r"--([\w][\w-]*):\s*([^;}\n]+)", block_text):
            name, val = prop_m.group(1), re.sub(r"/\*.*?\*/", "", prop_m.group(2)).strip()
            if name not in _GUIDE_SET:
                continue
            if not _valid_hex.match(val):
                sys.exit(
                    f"build_style_guide: unsupported colour value for '--{name}' in '{sel}': {val!r}. "
                    "Colour tokens used in the contrast table must be #rgb or #rrggbb."
                )
        result = {}
        for name, val in re.findall(r"--(\w[\w-]*):\s*(#[0-9a-fA-F]{3,6})", block_text):
            stripped = val.lstrip("#")
            if len(stripped) in (3, 6):
                result[name] = _expand3(val)
        return result

    light = _block(":root")
    dark = _block(':root[data-theme="dark"]', required=True)
    if not dark:
        sys.exit(
            "build_style_guide: dark token block ':root[data-theme=\"dark\"]' parsed empty "
            "(no --token: #hex entries found). Check site/assets/site.css."
        )
    missing = [t for t in ALL_GUIDE_TOKENS if t not in light]
    if missing:
        sys.exit(
            "build_style_guide: token(s) missing from :root in site.css — "
            + ", ".join(f"--{t}" for t in missing)
            + ". Add the token to :root or remove it from the guide token list."
        )

    # Background tokens are never used as foreground text — no contrast badge.
    BG_TOKENS = {"bg", "surface", "sunk", "line", "associate-soft", "architect-soft", "developer-soft"}

    bg_l, sf_l = light["bg"], light["surface"]
    bg_d = dark.get("bg", bg_l)
    sf_d = dark.get("surface", sf_l)

    def badge(r: float) -> str:
        sym, cls = ("✓", "cr-ok") if r >= 4.5 else ("✗", "cr-fail")
        return f'<span class="{cls}">{sym}&thinsp;{r:.1f}:1</span>'

    def swatch_row(tok: str) -> str:
        lhex = light.get(tok, "")
        if not lhex:
            return ""
        dhex = dark.get(tok)
        dark_cell = dhex if dhex else "same as light"
        dhex_eff = dhex if dhex else lhex
        if tok in BG_TOKENS:
            return (
                f'<tr><td><span class="swatch" style="background:var(--{tok})"></span></td>'
                f'<td><code>--{tok}</code></td><td>{lhex}</td><td>{dark_cell}</td>'
                f'<td class="cr" colspan="2"><em>background only</em></td></tr>'
            )
        return (
            f'<tr><td><span class="swatch" style="background:var(--{tok})"></span></td>'
            f'<td><code>--{tok}</code></td><td>{lhex}</td><td>{dark_cell}</td>'
            f'<td class="cr">{badge(_cr(lhex, bg_l))} / {badge(_cr(lhex, sf_l))}</td>'
            f'<td class="cr">{badge(_cr(dhex_eff, bg_d))} / {badge(_cr(dhex_eff, sf_d))}</td></tr>'
        )

    def tbl(toks: list) -> str:
        rows = "".join(swatch_row(t) for t in toks)
        return (
            '<div class="tbl"><table><thead><tr>'
            '<th>Swatch</th><th>Token</th><th>Light</th><th>Dark</th>'
            '<th>Light contrast (bg / surface)</th><th>Dark contrast (bg / surface)</th>'
            '</tr></thead><tbody>' + rows + '</tbody></table></div>'
        )
    return f"""
<h1>Design style guide</h1>
<p class="lede">A reference for contributors. Use these tokens and components so every page looks and feels consistent.</p>

<section class="block prose">
<h2>1. Principles</h2>
<ul>
<li><b>One idea at a time.</b> Each section or paragraph covers one concept. Split anything that spans two.</li>
<li><b>No outside fonts, scripts or images.</b> Nothing loads from a CDN or third-party domain.</li>
<li><b>4.5:1 contrast minimum.</b> Every foreground token passes WCAG AA against its background (see swatches below).</li>
<li><b>Works on phones and in print.</b> Responsive layout down to 320 px; the print stylesheet hides navigation.</li>
<li><b>Dark mode built in.</b> All colours are CSS custom properties; dark values swap automatically via the toggle or <code>prefers-color-scheme</code>.</li>
<li><b>No tracking.</b> No cookies, no analytics, no calls to other domains.</li>
</ul>
</section>

<section class="block">
<h2>2. Colour</h2>

<p class="muted" style="margin-bottom:8px"><em>Background tokens are never used for text, so they have no contrast badge.</em></p>
<h3>Neutrals</h3>
<p class="muted">Background, surface, text and border tokens used on every page.</p>
{tbl(["bg", "surface", "sunk", "ink", "muted", "line", "accent"])}

<h3>Track colours</h3>
<p class="muted">Each colour is the identity of one certification group. Apply it only on content that belongs to that track.</p>
<div class="tier-row" style="margin:12px 0">
  <div class="tier" style="border-left-color:var(--associate)"><b style="color:var(--associate)">Associate \u00b7 teal</b><span>CCAO-F \u2014 for consultants, sellers and delivery leads who guide customers to the right Claude use cases.</span></div>
  <div class="tier" style="border-left-color:var(--architect)"><b style="color:var(--architect)">Architect \u00b7 indigo</b><span>CCAR-F and CCAR-P \u2014 for architects designing agentic systems with Claude, MCP and Claude Code.</span></div>
  <div class="tier" style="border-left-color:var(--developer)"><b style="color:var(--developer)">Developer \u00b7 amber</b><span>CCDV-F \u2014 for engineers building with the Claude API, the Agent SDK, Claude Code and MCP.</span></div>
</div>
{tbl(["associate", "architect", "developer", "associate-soft", "architect-soft", "developer-soft"])}

<h3>Tier colours</h3>
<p class="muted">Tell readers how much weight to give a fact. T1 = Anthropic original (always wins). T2 = guides by others. T3 = blogs and sites. TF = field reports from colleagues.</p>
{tbl(["t1", "t2", "t3", "tf"])}
</section>

<section class="block prose">
<h2>3. Type</h2>
<p><b>System sans</b> (<code>--font</code>) \u2014 ui-sans-serif, -apple-system, Segoe\u00a0UI, Roboto, Helvetica\u00a0Neue, Arial, sans-serif. Body text everywhere.</p>
<p><b>Serif</b> (<code>--serif</code>) \u2014 ui-serif, Iowan\u00a0Old\u00a0Style, Palatino\u00a0Linotype, Georgia, serif. Used for <code>h1</code> and card headings.</p>
<p><b>Monospace</b> (<code>--mono</code>) \u2014 ui-monospace, SF\u00a0Mono, Menlo, Consolas, monospace. Inline code and code blocks.</p>
<ul>
<li>Body: 17\u00a0px\u00a0/\u00a01.62 line-height.</li>
<li><span class="lede">Lede: 1.15\u00a0rem, muted \u2014 the one-sentence purpose of a page or section.</span></li>
<li><span class="eyebrow">Eyebrow: 0.78\u00a0rem, uppercase, track colour \u2014 context label above an h1.</span></li>
<li>H1 uses <code>--serif</code>, clamp 1.9\u20132.7\u00a0rem. H2: 1.45\u00a0rem. H3: 1.12\u00a0rem. Both sans-serif.</li>
</ul>
</section>

<section class="block">
<h2>4. Components</h2>
<p class="muted">Rendered live with the real CSS classes. Copy the markup; don't recreate styles by hand.</p>

<h3>Buttons</h3>
<p><a class="btn" href="#">Primary button</a> <a class="btn ghost" href="#" style="margin-left:10px">Ghost button</a></p>
<p class="muted small">Use <code>.btn</code> for the main call-to-action. Use <code>.btn.ghost</code> for a secondary action beside a primary.</p>

<h3>Pills</h3>
<p>
  <span class="pill" style="background:var(--associate)">CCAO-F</span>
  <span class="pill" style="background:var(--architect);margin-left:6px">CCAR-F</span>
  <span class="pill" style="background:var(--developer);margin-left:6px">CCDV-F</span>
</p>
<p class="muted small">Exam-code badges on cards and sidebar entries. The background is the track colour via <code>var(--track)</code>.</p>

<h3>Card</h3>
<div class="cards" style="max-width:360px">
  <article class="card c-architect">
    <p class="card-k"><span class="pill">CCAR-F</span> Architect \u00b7 Foundations</p>
    <h3>Claude Certified Architect \u2013 Foundations</h3>
    <p class="card-who">For architects designing agentic systems.</p>
    <a class="btn" href="#">Open the plan</a>
  </article>
</div>
<p class="muted small">Use <code>.card</code> with a <code>.c-&lt;track&gt;</code> modifier. The top border uses <code>--track</code>. Cards stack to full width on mobile.</p>

<h3>Tier boxes</h3>
<div class="tier-row" style="max-width:540px;margin:12px 0">
  <div class="tier t1"><b>Tier\u00a01 \u00b7 Anthropic original</b><span>Exam guides, docs, Academy courses. Always wins a conflict.</span></div>
  <div class="tier t2"><b>Tier\u00a02 \u00b7 Guides by others</b><span>Only where Tier\u00a01 is silent, and labelled.</span></div>
</div>
<p class="muted small">Use <code>.tier.t1</code>, <code>.tier.t2</code>, <code>.tier.t3</code>, <code>.tier.tf</code>.</p>

<h3>Eyebrow and lede</h3>
<p class="eyebrow">Section label</p>
<p class="lede">A lede describes the section purpose in one plain sentence, 64 characters or fewer.</p>

<h3>Table</h3>
<div class="tbl"><table><thead><tr><th>Token</th><th>Light value</th><th>Used for</th></tr></thead><tbody>
<tr><td><code>--bg</code></td><td>#fbfaf7</td><td>Page background</td></tr>
<tr><td><code>--ink</code></td><td>#1d2433</td><td>Body text</td></tr>
</tbody></table></div>
<p class="muted small">Wrap every table in <code>&lt;div class="tbl"&gt;</code> for horizontal scroll on mobile.</p>

<h3>External link</h3>
<p><a class="ext" href="#" rel="noopener">External link</a> \u2014 the CSS appends \u2197 automatically.</p>
</section>

<section class="block prose">
<h2>5. Writing style</h2>
<ul>
<li><b>Short sentences.</b> One idea per sentence. If it needs a semicolon, split it into two sentences.</li>
<li><b>Plain words.</b> Write \u201cuse\u201d not \u201cutilise\u201d. Write \u201ccheck\u201d not \u201cverify the accuracy of\u201d.</li>
<li><b>Cite source and tier for every fact.</b> For example: <em>Source: CCAR-F exam guide \u00a73 (Tier\u00a01).</em></li>
<li><b>No real exam questions.</b> Candidates sign a confidentiality agreement. Simulations and practice items are original.</li>
<li><b>Colleague names withheld</b> until each person agrees. Use \u201ca colleague\u201d as the placeholder.</li>
</ul>
<h3>Lesson shape</h3>
<ol>
<li><b>Big idea.</b> One sentence \u2014 what this lesson proves.</li>
<li><b>What to know.</b> The exam-weight domain, named sections and key terms.</li>
<li><b>Worked example.</b> A realistic scenario with a clear right answer and an explanation of why.</li>
<li><b>Traps.</b> The two or three wrong answers the exam expects you to confuse with the right one.</li>
<li><b>Try it.</b> One concrete action: paste a prompt, run an API call, or sketch a diagram.</li>
<li><b>Done when.</b> The observable outcome that confirms you understood the lesson.</li>
</ol>
</section>

<section class="block prose">
<h2>6. How to propose a design change</h2>
<p>Open an issue through the <a href="contribute.html">Contribute</a> page. Include:</p>
<ol>
<li>What looks or behaves wrong, and which page.</li>
<li>Which token or class is involved (for example <code>--accent</code> or <code>.btn</code>).</li>
<li>A concrete suggestion: a new token value, a class change, or a new component.</li>
</ol>
<p>Every change goes through the design-system review gate. One fix regenerates all impacted pages from the same token.</p>
</section>
"""


# ---------------------------------------------------------------- main

def fingerprint(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()[:16]


def public_rows(name: str, md: str) -> str:
    drop = PRIVATE_ROWS[name]
    for rx, sub in PUBLIC_REDACT:
        md = re.sub(rx, sub, md)
    keep = [l for l in md.splitlines() if not (l.startswith("| ") and l.split("|")[1].strip() in drop)]
    note = f"\n\n> Copied from the maintainer's workspace on every publish. Personal study rows ({', '.join(sorted(drop))}) are left out."
    return re.sub(r"^# .*$", lambda m: m.group(0) + note, "\n".join(keep), count=1, flags=re.M) + "\n"


def export_content(site: Site, dest: Path, reviewed: dict[str, str]):
    if dest.exists():
        if any(dest.iterdir()) and not (dest / EXPORT_MARK).exists():
            sys.exit(f"build: {dest} exists and isn't an export folder; refusing to overwrite it")
        shutil.rmtree(dest)
    n = 0
    for src_rel in site.pages:
        if src_rel != CHANGELOG_SRC and site.path(src_rel).exists():
            p = dest / src_rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(site.text(src_rel))
            n += 1
            export = DECK_EXPORTS.get(Path(src_rel).name)
            if export and (site.path(src_rel).parent / export).exists():
                shutil.copyfile(site.path(src_rel).parent / export, p.parent / export)
    # These public authored dependencies are not Markdown routes. Export only the
    # explicit files the registry navigation and downloadable lab need; never a
    # whole source directory or the maintainer's question-bank/private files.
    supplemental = {}
    for src_rel in (
        '02-Lessons/02-CCAR-F-Architect-Foundations/decision-variants.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/visual-walkthroughs.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/visual-walkthroughs-other.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/visual-connection-details.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/visual-focus-notes.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/application-teaching-a.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/application-teaching-b.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/objective-learning-patterns.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/question-plain-context.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/page-teaching-map.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/diagram-teaching-map.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/boundary-decision-cues.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/boundary-intro-decision.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/technical-objective-bridges.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/technical-scenario-bridges.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/technical-component-bridges.json',
        '02-Lessons/02-CCAR-F-Architect-Foundations/technical-bridge-placements.json',
        '06-Labs/02-CCAR-F-coordinator-extraction/decision_variant_fixtures.py',
        '06-Labs/08-CCAR-F-architecture-decisions/architecture_decisions.py',
        '06-Labs/08-CCAR-F-architecture-decisions/benchmark_exercises.py',
        '06-Labs/08-CCAR-F-architecture-decisions/benchmark-fixtures.json',
    ):
        source = site.path(src_rel)
        if not source.exists():
            continue
        target = dest / src_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == '.json':
            data = json.loads(source.read_text())
            def sanitize(value):
                if isinstance(value, str):
                    return site.anon(scrub(value, src_rel))
                if isinstance(value, list):
                    return [sanitize(item) for item in value]
                if isinstance(value, dict):
                    return {key: sanitize(item) for key, item in value.items()}
                return value
            target.write_text(json.dumps(sanitize(data), indent=2) + '\n')
        else:
            # Synthetic standard-library fixture; preserve executable syntax.
            compile(source.read_text(), src_rel, 'exec')
            shutil.copyfile(source, target)
        supplemental[src_rel] = fingerprint(target)
        n += 1
    for seat in sorted((site.src / ".claude/agents").glob("*.md")):
        p = dest / "crew" / seat.name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(site.anon(scrub(seat.read_text())))
    for name in PRIVATE_ROWS:
        (dest / name).write_text(public_rows(name, site.anon(scrub((site.src / name).read_text()))))
    (dest / EXPORT_MARK).write_text(json.dumps({
        "note": "Page sources for the site, already anonymized. Build with: python3 site/build.py --src content",
        "reviewed": dict(sorted(reviewed.items())),
        "supplemental_sha": supplemental,
        "sha": {k: fingerprint(dest / k if k != CHANGELOG_SRC else REPO / "CHANGELOG.md") for k in sorted(reviewed)
                if (dest / k).exists() or k == CHANGELOG_SRC},
    }, indent=1) + "\n")
    return n


def check_question_leak(src: Path, pages: dict[str, str]) -> list[str]:
    qfile = src / "05-Practice-Tool/build/questions.json"
    if not qfile.exists():
        return [f"{qfile} not found; can't check for question-bank leaks"]
    data = json.loads(qfile.read_text())
    qs = data["questions"] if isinstance(data, dict) else data
    norm = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).lower()
    corpus = {k: norm(v) for k, v in pages.items()}
    hits = []
    for q in qs:
        stem = norm(q.get("question", ""))[:70].strip()
        if len(stem) >= 50:
            hits += [f"{rel}: matches question-bank item {q.get('id')}" for rel, t in corpus.items()
                     if stem in t and not published_drill(rel, q.get("id", ""))]
    return hits


def published_drill(rel: str, qid: str) -> bool:
    """Hard drills are published on purpose as their own page, and the bank carries the same items (BACKLOG RT-23)."""
    m = re.match(r"lessons/([\w-]+)/hard-drills\.html$", rel)
    return bool(m) and qid.startswith(EXAMS.get(m.group(1), {}).get("code", "?").replace("-", "") + "-HD-")


# ---------------------------------------------------------------- recorded reviews, auto-linker, "Used in"
import json as _json
REVIEWS: dict = {}


def load_reviews() -> dict:
    """REVIEWS.json: {"exams": {"ccar-f": {"date": "YYYY-MM-DD", "by": "...", "ref": "<BACKLOG or DECISIONS id>"}}}.
    A review date exists only if a person or seat recorded it here. The build refuses malformed or future records."""
    p = REPO / "REVIEWS.json"
    d = _json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    out = {}
    for k, v in d.get("exams", {}).items():
        if k not in EXAMS:
            sys.exit(f"build: REVIEWS.json names unknown exam {k}")
        try:
            day = dt.date.fromisoformat(v["date"])
        except (KeyError, ValueError):
            sys.exit(f"build: REVIEWS.json {k}: date must be YYYY-MM-DD")
        if day > dt.date.today() or not v.get("ref") or not v.get("by"):
            sys.exit(f"build: REVIEWS.json {k}: needs a date not in the future, 'by' and 'ref'")
        out[k] = v
    return out


def review_line(key: str) -> str:
    r = REVIEWS.get(key)
    if r:
        return f'<p class="review-line">Last reviewed: <time datetime="{r["date"]}">{r["date"]}</time></p>'
    return '<p class="review-line">Last reviewed: not yet recorded</p>'


TECH_HELP = {
    "idempotency": "Repeating the same identified operation should not create an extra effect. This requires service-side implementation and correct operation identity.",
    "reconciliation": "Check authoritative operation status when an effect is uncertain before deciding whether it is safe to repeat.",
    "tool_choice": "Request setting controlling which tool Claude may or must request, where supported. It does not establish authorization or successful prerequisites.",
    "PreToolUse": "A supported hook event before tool execution. A blocking check must use the correct runtime decision and cover the relevant execution path.",
    "PostToolUse": "A hook event after successful tool execution. Useful for observing or transforming results; it cannot prevent the effect already performed.",
    "input_schema": "The declared structure of a tool's accepted arguments. Enforced conformance depends on a supported strict/schema-constrained interface.",
    "prerequisite gate": "An executable check requiring a prior condition to hold before a dependent action. A prompt instruction alone is not this gate.",
    "schema": "A structural contract for fields and types. Matching it does not prove the values agree with evidence or business rules.",
    "provenance": "The source identity, location and version supporting a claim. Preserve it when results move between components.",
    "grounding": "Basing an answer on supplied or retrieved evidence, with its access, scope and source limitations intact.",
    "checkpoint": "Saved work state for resuming. It records earlier observations; refresh changed facts and authority before acting.",
    "context isolation": "A worker reasons with its supplied context, not an assumed shared conversation. Give it a self-contained task and relevant evidence.",
    "structured output": "A machine-readable result with a declared shape. Check supported schema constraints, exceptional outcomes and semantic validity separately.",
    "calibration": "Compare confidence signals with measured correctness on representative labeled examples, including segments and held-out data.",
    "nullable": "The field may explicitly contain null. Required presence, allowed null and factual completeness are separate decisions.",
    "handoff": "Transfer unresolved work with evidence, current state, reason and next owner; do not label it successful completion.",
}
TECH_RX = r"(?P<tech>\b(?:" + "|".join(re.escape(x) for x in sorted(TECH_HELP, key=len, reverse=True)) + r")\b)"

LES_RX = (r"(?P<les>\b(?:(?P<lx>CC[A-Z]{2}-[FP])\s+)?L0\d(?![\w]|-\w)(?:\s*(?:,|and|&|–|-|/)\s*(?:and\s+)?L0\d(?![\w]|-\w))*)")
AUTO = re.compile("|".join([
    TECH_RX,
    LES_RX,
    r"(?P<sim>\b(?:(?P<sx>CC[A-Z]{2}-[FP])\s+)?SIM-0(?P<sn>\d)\b(?!-)(?:\s*#(?P<sd>\d+))?)",
    r"(?P<lab>\bLab 0(?P<bn>\d)\b)",
    r"(?P<gate>\bG(?P<gn>1[0-2]|\d)\b)",
    r"(?P<dom>\bD(?P<dn>[1-5])\b)",
    r"(?P<tier>\bTier (?P<tn>[123])\b)",
    r"(?P<coach>\b[Cc]oach key\b)",
    r"(?P<task>\b(?:official )?exam guide,? task (?P<tk>[1-5]\.\d)\b)",
]))
TIER_TIP = {"1": "Tier 1: Anthropic's own material. It wins every conflict.",
            "2": "Tier 2: guides and lessons by others. Used only where Tier 1 is silent, and labelled.",
            "3": "Tier 3: a lower source tier. See the source tiers table on the About page."}
COACH_TIP = "The answer key at the end of a simulation. Work the decisions first, then open it."
SKIP_TAGS = re.compile(r"<(/?)(a|code|pre|abbr|h1|script|style|button)\b", re.I)


def make_autolinker(site: Site):
    les, sim, lab, gates, tasks = {}, {}, {}, {}, {}
    for s_, o in site.pages.items():
        tm = re.search(r"objectives/objective-(\d\.\d)\.md$", s_)
        if tm:
            tasks[(exam_key_from_dir(s_), tm.group(1))] = o
    for key in EXAMS:
        for s_, o, _ in site.of("lesson", key):
            les[(key, int(Path(s_).stem[2]))] = (o, re.sub(r"[`*]", "", lesson_meta(site.text(s_))["name"]))
        for s_, o, _ in site.of("sim", key):
            sim[(key, int(Path(s_).stem.split("-")[1]))] = (o, re.sub(r"[`*]", "", short_title(site.text(s_))))
    for s_, o, m in site.of("lab"):
        lab[int(m["lab"])] = (o, re.sub(r"[`*]", "", short_title(site.text(s_))))
    for n, nm in re.findall(r"\*\*G(\d+) ([^*]+)\*\*", site.text("CREW-WORKFLOW.md")):
        gates[int(n)] = nm.strip()
    E = html.escape

    def auto(h: str, out_rel: str) -> str:
        a, b = h.find("<main"), h.rfind("</main>")
        if a < 0 or b < 0:
            return h
        root = "../" * out_rel.count("/")
        cm = re.match(r"(?:lessons|simulations)/([\w-]+)/", out_rel) or re.match(r"exams/([\w-]+)\.html", out_rel)
        ctx = cm.group(1) if cm and cm.group(1) in EXAMS else None
        if out_rel == "how-we-build.html":
            seen_gates = set()
            def gate_id(m):
                n = m.group(3)
                attr = '' if n in seen_gates else f' id="gate-{n}"'
                seen_gates.add(n)
                return f'<{m.group(1)}{attr}>{m.group(2)}</{m.group(1)}>'
            h = re.sub(r"<(strong|b)>(G(\d+) [^<]+)</\1>", gate_id, h)
            a, b = h.find("<main"), h.rfind("</main>")

        seen_tech = set()
        tech_context = ctx == 'ccar-f' or out_rel.startswith(('labs/02-CCAR-F-', 'labs/03-CCAR-F-', 'labs/08-CCAR-F-'))
        def fn(m):
            g, t = m.lastgroup, m.group(0)
            if m.group("tech"):
                if not tech_context or t in seen_tech:
                    return t
                seen_tech.add(t)
                return f'<abbr data-tip="{E(TECH_HELP[t], quote=True)}" aria-label="{E(t, quote=True)}">{E(t)}</abbr>'
            if g == "les" or m.group("les"):
                exam = CODE_TO_KEY.get(m.group("lx")) if m.group("lx") else ctx

                def one(x):
                    n = int(x.group(1))
                    hit = les.get((exam, n)) if exam else None
                    if hit:
                        return f'<a class="xref" href="{root}{hit[0]}">Lesson {n}: {E(hit[1])}</a>'
                    return f'<a class="xref" href="{root}lessons/index.html">Lesson {n}</a>'
                return re.sub(r"L0(\d)", one, t)
            if m.group("sim"):
                exam = CODE_TO_KEY.get(m.group("sx")) if m.group("sx") else ctx
                n = int(m.group("sn"))
                hit = sim.get((exam, n)) if exam else None
                pre = (m.group("sx") + " ") if m.group("sx") else ""
                tail = f", decision {m.group('sd')}" if m.group("sd") else ""
                if hit:
                    return f'{pre}<a class="xref" href="{root}{hit[0]}">Simulation {n}{tail}: {E(hit[1])}</a>'
                return f'{pre}<a class="xref" href="{root}simulations/index.html">Simulation {n}{tail}</a>'
            if m.group("lab"):
                n = int(m.group("bn"))
                hit = lab.get(n)
                return f'<a class="xref" href="{root}{hit[0]}">Lab 0{n}: {E(hit[1])}</a>' if hit else t
            if m.group("gate"):
                n = int(m.group("gn"))
                if n not in gates:
                    return t
                tip = E(f"Gate {n}: {gates[n]}", quote=True)
                return f'<a class="gate" href="{root}how-we-build.html#gate-{n}"><abbr data-tip="{tip}" aria-label="{tip}">G{n}</abbr></a>'
            if m.group("dom"):
                n = m.group("dn")
                href = f"{root}exams/{ctx}.html#study-plan" if ctx else f"{root}curriculum.html"
                tip = f"Domain {n} of the exam guide" + (f" for {EXAMS[ctx]['code']}" if ctx else "")
                return f'<a class="xref" href="{href}"><abbr data-tip="{tip}" aria-label="{tip}">D{n}</abbr></a>'
            if m.group("tier"):
                n = m.group("tn")
                return f'<a class="xref" href="{root}about.html#source-tiers"><abbr data-tip="{E(TIER_TIP[n], quote=True)}" aria-label="{E(TIER_TIP[n], quote=True)}">{t}</abbr></a>'
            if m.group("coach"):
                return f'<abbr data-tip="{COACH_TIP}" aria-label="{COACH_TIP}">{t}</abbr>'
            if m.group("task"):
                hit = tasks.get((ctx, m.group("tk")))
                return f'<a class="xref" href="{root}{hit}">{t}</a>' if hit else t
            return t
        parts = re.split(r"(<[^>]*>)", h[a:b])
        depth = 0
        for i, p in enumerate(parts):
            if i % 2:
                mm = SKIP_TAGS.match(p)
                if mm and not p.endswith("/>"):
                    depth = max(0, depth + (-1 if mm.group(1) else 1))
            elif depth == 0 and p.strip():
                parts[i] = AUTO.sub(fn, p)
        return h[:a] + "".join(parts) + h[b:]
    return auto


def add_used_in(written: dict) -> None:
    """Every lesson, simulation and lab page gets a generated 'Used in' box: the pages whose body links to it."""
    import posixpath
    tgt = re.compile(r"(lessons|simulations)/[\w-]+/(L0|SIM-0)\d[^/]*\.html$|labs/\d\d-[^/]*\.html$")
    back: dict = {}
    titles = {}
    for rel, h in written.items():
        tm = re.search(r"<title>(.*?) · Claude Certifications Study Site</title>", h, re.S)
        titles[rel] = tm.group(1) if tm else rel
        mm = re.search(r"<main.*?</main>", h, re.S)
        body = re.sub(r"<(nav|aside|header|footer)\b.*?</\1>|<details class=\"toc\">.*?</details>", " ", mm.group(0) if mm else "", flags=re.S)
        for href in set(re.findall(r'<a [^>]*href="([^"#]+\.html)[^"]*"', body)):
            t = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href))
            if t != rel and tgt.match(t):
                back.setdefault(t, set()).add(rel)
    for rel in [r for r in written if tgt.match(r)]:
        root = "../" * rel.count("/")
        srcs = sorted(back.get(rel, ()), key=lambda r: (r.endswith("index.html"), r))
        # F12: a lab's separate "Used by: <exams>" strip folds into this one box (its links kept).
        um = re.search(r'<p class="uses">Used by: (.*?)</p>', written[rel], re.S)
        exams = ""
        if um:
            written[rel] = written[rel].replace(um.group(0), "", 1)
            exams = f'<p class="usedin-exams">Exams: {um.group(1)}</p>'
        if srcs:
            lis = "".join(f'<li><a href="{root}{r}">{titles[r]}</a></li>' for r in srcs)
            summ = (f'Used in {len(srcs)} page{"s" if len(srcs) != 1 else ""}' if "/simulations/" in "/" + rel
                    else f'<b>Linked from</b> {len(srcs)} other page{"s" if len(srcs) != 1 else ""}')
            box = (f'<aside class="usedin" aria-label="Linked from other pages"><details><summary class="usedin-h">'
                   f'{summ}</summary>'
                   f'{exams}<ul>{lis}</ul></details></aside>')
        else:
            box = (f'<aside class="usedin" aria-label="Linked from other pages"><p class="usedin-h"><b>Linked from</b> no other page yet.</p>'
                   f'{exams}</aside>')
        top = re.search(r'</h1>(<p class="walk-first">.*?</p>)?', written[rel], re.S)
        if not top:
            continue  # no h1 on this page: nowhere to anchor the box (G9 later item)
        # Backlink inventory supports navigation, but does not displace the lesson opening.
        end_article = written[rel].rfind('</article>')
        if end_article >= 0:
            written[rel] = written[rel][:end_article] + box + written[rel][end_article:]
        else:
            written[rel] = written[rel][:top.end()] + box + written[rel][top.end():]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.environ.get("CERT_SRC"))
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--export", type=Path, help="also write the anonymized page sources here (for example content)")
    args = ap.parse_args()
    if not args.src:
        sys.exit("Give --src <study workspace path, or content> or set CERT_SRC")
    REVIEWS.update(load_reviews())
    site = Site(Path(args.src).expanduser().resolve())
    out = args.out.resolve()
    if site.exported and args.export:
        sys.exit("build: --export needs the study workspace as --src; content/ is already an export")
    if out.exists() and any(out.iterdir()) and not (out / ".nojekyll").exists():
        sys.exit(f"build: {out} isn't a built site (no .nojekyll); refusing to delete it")
    discover(site)
    if not site.exported:
        site.anon = Anonymizer(site.src / "10-Learning-Site/private/names.txt")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    (out / ".nojekyll").write_text("")
    shutil.copytree(ASSETS_SRC, out / "assets")

    written, exam_curriculum, deck_files = {}, {}, {}
    for src_rel, out_rel in site.pages.items():
        f = site.path(src_rel)
        if not f.exists():
            if src_rel in REQUIRED:
                sys.exit(f"build: {f} not found; it is required (nav and footer link to it)")
            print(f"skip missing {src_rel}", file=sys.stderr)
            continue
        md = site.text(src_rel)
        if out_rel == "whats-new.html":
            md = re.sub(r"\A.*?(?=^## )", "# What's new\n\nEvery update to the site, newest first. Updates that add pages or exercises, or change a fact or an answer, are also announced in the study cohort's Slack channel.\n\n", md, count=1, flags=re.M | re.S)
        stored = site.reviewed.get(src_rel)
        if stored and site.sha.get(src_rel, fingerprint(f)) != fingerprint(f):
            stored = None
        reviewed = stored or dt.date.fromtimestamp(f.stat().st_mtime).isoformat()
        site.reviewed[src_rel] = reviewed
        meta = site.meta[out_rel]
        kind, exam = meta["kind"], meta.get("exam")
        if kind == "exam":  # the review date comes only from a recorded review (REVIEWS.json), never from file time
            reviewed = REVIEWS.get(exam, {}).get("date", "")
        r = Renderer(site, src_rel, out_rel)
        if kind == "exam":
            md = re.sub(r"^#\s+.*\n", "", md, count=1)
            md = re.sub(r"^\*\*(Exam|Study time):\*\*.*\n", "", md, flags=re.M)
            exam_curriculum[exam] = r.render(md)
            meta["reviewed"] = reviewed
            continue
        generated = {"02-Lessons/README.md": "lesson", "04-Simulations/README.md": "sim", "06-Labs/README.md": "lab"}
        if src_rel in generated:
            body = build_study_index(site, generated[src_rel])
            title = {"lesson": "Lessons", "sim": "Simulations", "lab": "Labs"}[generated[src_rel]]
            written[out_rel] = page(out_rel, title, f'<article class="prose">{body}</article>',
                                    crumbs=[("Home", "index.html"), (title, "")], reviewed=reviewed)
            continue
        body = r.render(md)
        export = DECK_EXPORTS.get(Path(src_rel).name)
        if export:
            exp_src = site.path(src_rel).parent / export
            rows = deck_rows(exp_src)
            if rows:
                deck_files[(Path(out_rel).parent / export).as_posix()] = exp_src
            body = flashcard_deck(body, src_rel, export if rows else None, len(rows), site)
        body, top_note = enrich_page(site, r, src_rel, out_rel, kind, exam, body)
        title = re.sub(r"<[^>]+>", "", r.inline(first_heading(md)))
        crumbs = [("Home", "index.html")] + ([(EXAMS[exam]["code"], f"exams/{exam}.html")] if exam else [])
        if kind in ("lesson", "sim"):
            idx = "lessons" if kind == "lesson" else "simulations"
            crumbs.append(("Lessons" if kind == "lesson" else "Simulations", f"{idx}/{exam}/index.html"))
        if kind == "lab":
            crumbs.append(("Labs", "labs/index.html"))
            used = [k for k, e in EXAMS.items() if meta["lab"] in e["labs"]]
            uses = '<p class="uses">Used by: ' + " · ".join(f'<a href="../exams/{k}.html">{EXAMS[k]["code"]}</a>' for k in used) + "</p>"
            body = body.replace("</h1>", "</h1>" + uses + toc(r.headings), 1) + prev_next(site, out_rel, None, "lab")
        if kind == "page":
            body = body.replace("</h1>", "</h1>" + toc(r.headings), 1)
        if kind == "extra":
            crumbs.append(("Lessons", f"lessons/{exam}/index.html"))
            sub = meta.get("sub")
            if sub and not out_rel.endswith("/index.html"):
                sub_src = f"{Path(src_rel).parent.as_posix()}/README.md"
                if sub_src in site.pages:
                    crumbs.append((short_title(site.text(sub_src)), site.pages[sub_src]))
            # B63-FX-7: objective pages show their domain in the breadcrumb (exam / lessons / objectives / domain / objective).
            om = re.search(r"objectives/objective-(\d)\.\d+\.md$", src_rel)
            if om:
                lesson_dir = Path(src_rel).parent.parent.as_posix()
                dom = sorted(s for s in site.pages if Path(s).parent.as_posix() == lesson_dir
                             and re.match(rf"L0{om.group(1)}-", Path(s).name))
                if dom:
                    crumbs.append((f"Domain {om.group(1)}", site.pages[dom[0]]))
            top_nav = bot_nav = ""
            if om:
                top_nav, bot_nav = objective_nav(site, exam, out_rel, "top"), objective_nav(site, exam, out_rel, "bottom")
            if om and exam == "ccar-f":  # B63-FX-12: honest per-objective check cue + resume marker
                from progress import cue as prog_cue
                top_nav += prog_cue(re.search(r"objective-(\d\.\d+)\.md$", src_rel).group(1))
            if om:
                body = objective_metadata(site, r, exam, body)
                body = mark_section_roles(body)
            body = body.replace("</h1>", "</h1>" + top_nav + toc(r.headings), 1) + bot_nav
        if kind in ("lesson", "sim"):
            extra = toc(r.headings)
            if kind == "sim" and "SIM-01" not in out_rel:
                extra += ('<p class="sim-how"><b>How to use this:</b> read the scene, then work through the decisions on paper, '
                          'or paste the scene and the decisions list (not the answer key) into Claude and ask it to run the simulation one decision at a time with no hints. '
                          "Open the coach key only when you've finished.</p>")
            body = body.replace("</h1>", "</h1>" + extra, 1) + prev_next(site, out_rel, exam, kind)
        if top_note:
            body = body.replace("</h1>", "</h1>" + top_note, 1)
        crumb = re.sub(r",\s*start to finish$", "", title.split("—")[0].strip())
        written[out_rel] = page(out_rel, title, f'<article class="prose">{body}</article>', exam=exam,
                                side=side_for(site, exam, out_rel) if exam else "",
                                crumbs=crumbs + [(crumb[:60], "")], reviewed=reviewed)

    for key, e in EXAMS.items():
        out_rel = f"exams/{key}.html"
        written[out_rel] = page(out_rel, e["name"], build_exam(site, key, exam_curriculum.get(key, "")), exam=key,
                                side=side_for(site, key, out_rel), crumbs=[("Home", "index.html"), (e["code"], "")],
                                reviewed=site.meta[out_rel].get("reviewed", TODAY),
                                description=f"Study plan, lessons, simulations and labs for {e['name']}.")
    if "ccar-f" in EXAMS:  # B63-FX-13: honest question coverage per objective, with industry cases
        from coverage import OUT_REL as cov_rel, build_coverage
        written[cov_rel] = page(cov_rel, "CCAR-F practice coverage by objective",
                                build_coverage(site.src, objective_pages(site, "ccar-f"), slugify,
                                               [(lesson_meta(site.text(s))["name"], "../" + Path(o).name)
                                                for s, o, _ in site.of("lesson", "ccar-f") if re.match(r"L0[1-5]-", Path(s).name)]), exam="ccar-f",
                                side=side_for(site, "ccar-f", cov_rel),
                                crumbs=[("Home", "index.html"), ("CCAR-F", "exams/ccar-f.html"), ("Practice coverage", "")],
                                description="Which CCAR-F objectives the shared practice questions test, and where to practise the rest.")
    if "ccar-f" in EXAMS:  # B63-FX-12: checked / opened / remaining, from the built pages' own checks
        from progress import OUT_REL as prog_rel, build_progress, manifest as prog_manifest
        written[prog_rel] = page(prog_rel, "Your CCAR-F progress",
                                 f'<article class="prose">{build_progress(prog_manifest(objective_pages(site, "ccar-f"), written))}</article>',
                                 exam="ccar-f", side=side_for(site, "ccar-f", prog_rel),
                                 crumbs=[("Home", "index.html"), ("CCAR-F", "exams/ccar-f.html"), ("Your progress", "")],
                                 description="CCAR-F objectives you opened and checked in this browser, what is left and what to revisit.")
    written["index.html"] = page("index.html", "Home", build_home(site),
                                 description="Study plans, lessons, simulations and labs for Anthropic's four Claude certifications.")
    written["resources.html"] = page("resources.html", "Resources", build_resources(), crumbs=[("Home", "index.html"), ("Resources", "")])
    written["about.html"] = page("about.html", "About", build_about(), crumbs=[("Home", "index.html"), ("About", "")])
    written["style-guide.html"] = page("style-guide.html", "Design style guide", build_style_guide(site), crumbs=[("Home", "index.html"), ("Design style guide", "")])

    from variants import records as variant_records, hub as variant_hub, contextual as variant_context, OUT_REL as variant_rel
    variants = variant_records(site)
    skill_src = site.src / '02-Lessons/02-CCAR-F-Architect-Foundations/skill-coverage.md'
    if skill_src.exists():
        skill_rel = 'lessons/ccar-f/skill-coverage.html'
        skill_r = Renderer(site, '02-Lessons/02-CCAR-F-Architect-Foundations/skill-coverage.md', skill_rel)
        written[skill_rel] = page(skill_rel, 'Official skill coverage', skill_r.render(skill_src.read_text()), exam='ccar-f', side=side_for(site, 'ccar-f', skill_rel))
    if variants:
        written[variant_rel] = page(variant_rel, 'Architecture decision variants', variant_hub(site, variants), exam='ccar-f',
                                  side=side_for(site, 'ccar-f', variant_rel), crumbs=[('Home', 'index.html'), ('CCAR-F', 'exams/ccar-f.html'), ('Decision variants', '')])
        for rel in list(written):
            context = variant_context(site, variants, rel)
            if context:
                written[rel] = written[rel].replace('</h1>', '</h1>' + context, 1)
        card = '<p class="muted">After a coached lesson, <a href="../lessons/ccar-f/decision-variants.html">compare decision mechanisms and alternatives</a>.</p>'
        # The exam entrance already includes the complete concept-to-practice route.

    studio_rel = 'lessons/ccar-f/scenario-studio.html'
    if studio_rel in written:
        for rel in list(written):
            if rel == studio_rel or not (rel.startswith(('lessons/ccar-f/', 'simulations/ccar-f/', 'labs/02-CCAR-F-', 'labs/03-CCAR-F-', 'labs/08-CCAR-F-')) ):
                continue
            studio_href = posixpath.relpath(studio_rel, posixpath.dirname(rel))
            course_href = posixpath.relpath('lessons/ccar-f/architecture-studio/index.html', posixpath.dirname(rel))
            route = '<nav class="variant-links" aria-label="Scenario learning route"><a href="' + posixpath.relpath('lessons/ccar-f/architecture-studio/00-foundations.html', posixpath.dirname(rel)) + '">Start with an application</a> · <a href="' + posixpath.relpath('lessons/ccar-f/learning-journey.html', posixpath.dirname(rel)) + '">Full learning journey</a> · <a href="' + course_href + '">Learn architecture through eight application cases</a> · <a href="' + studio_href + '">Practise 30 decision variants</a></nav>'
            written[rel] = written[rel].replace('</h1>', '</h1>' + route, 1)

    from variants import inline_aids, miss_repair_anchors
    for rel in list(written):
        written[rel] = miss_repair_anchors(site, variants, rel, written[rel])
        written[rel] = inline_aids(site, variants, rel, written[rel])

    from variants import walkthrough_gallery
    gallery_rel = 'lessons/ccar-f/scenario-walkthroughs/index.html'
    if variants and gallery_rel in written:
        gallery = walkthrough_gallery(site, variants)
        written[gallery_rel] = written[gallery_rel].replace('</article>', gallery+'</article>', 1)
        if 'assets/viewer.js' not in written[gallery_rel]:
            root = '../' * gallery_rel.count('/')
            written[gallery_rel] = written[gallery_rel].replace('</head>', f'<link rel="stylesheet" href="{root}assets/viewer.css"><script defer src="{root}assets/vendor/mermaid-12.1.0.min.js"></script><script defer src="{root}assets/viewer.js"></script></head>')

    from scenario_signals import inventory as signal_inventory, build as build_signals, enhance as enhance_signals, scripts as signal_scripts, OUT_REL as signals_rel
    signal_rows = signal_inventory(site)
    if signal_rows:
        written[signals_rel] = page(signals_rel, 'Signals and errors by scenario', build_signals(site, signal_rows, lambda src, md: link_guide_tags(site, Renderer(site, src, signals_rel), "ccar-f", Renderer(site, src, signals_rel).render(md)), lambda src, md: Renderer(site, src, signals_rel).inline(md)), exam='ccar-f',
                                   side=side_for(site, 'ccar-f', signals_rel), crumbs=[('Home', 'index.html'), ('CCAR-F', 'exams/ccar-f.html'), ('Signals and errors', '')])
        for rel in list(written):
            written[rel] = signal_scripts(enhance_signals(site, written[rel], rel, signal_rows), rel)
        if gallery_rel in written:
            written[gallery_rel] = written[gallery_rel].replace('</h1>', '</h1><p><a href="signals-and-errors.html">Signals, errors and missed what-ifs across all six scenarios</a></p>', 1)

    from layered_teaching import enhance as add_layered_reference_teaching
    layered_destinations = {}  # B-113: the unified in-page coach reuses these same packets without duplicate generated panels.

    auto = make_autolinker(site)
    for rel in list(written):
        written[rel] = auto(written[rel], rel)
    domain_names_once(written)
    add_used_in(written)

    # Put the authored concrete scene before generated menus and metadata.
    # This moves one paragraph only; assessment ordering and progress keys are untouched.
    for rel in list(written):
        if rel.startswith(('lessons/ccar-f/', 'simulations/ccar-f/')):
            scene = re.search(r'<p><strong>Picture (?:the application|it)[^<]*</strong>.*?</p>', written[rel], re.S)
            if scene:
                paragraph = scene.group(0)
                written[rel] = written[rel][:scene.start()] + written[rel][scene.end():]
                written[rel] = written[rel].replace('</h1>', '</h1>' + paragraph, 1)

    from visual_walkthrough import enhance as visual_lessons, asset as visual_asset
    visual_stories = visual_lessons(site, written)

    from technical_bridges import enhance as add_technical_bridges, asset as technical_asset
    technical = add_technical_bridges(site, written, visual_stories)

    from course_coach import enhance as add_course_coach, asset as course_asset
    course_data, course_manifest = add_course_coach(site, written, variants, REPO)

    for rel in written:
        if 'assets/viewer.js' in written[rel] or 'assets/visual-walkthrough.js' in written[rel] or 'class="scn-preview"' in written[rel] or 'class="map"' in written[rel]:
            prefix='../'*rel.count('/')
            written[rel]=written[rel].replace('</head>', f'<link rel="stylesheet" href="{prefix}assets/diagram-annotations.css"></head>')
            written[rel]=written[rel].replace('<script', f'<script defer src="{prefix}assets/diagram-annotations.js"></script><script',1)

    # Version viewer assets so a published fix also reaches already-open study sessions.
    for asset in ('viewer.js', 'viewer.css', 'site.js', 'site.css', 'visual-walkthrough.js', 'visual-walkthrough.css', 'diagram-annotations.js', 'diagram-annotations.css', 'technical-bridges.js', 'technical-bridges.css', 'course-coach.js', 'course-coach.css'):
        digest = hashlib.sha256((ASSETS_SRC / asset).read_bytes()).hexdigest()[:12]
        for rel in written:
            written[rel] = written[rel].replace('assets/' + asset + '"', 'assets/' + asset + '?v=' + digest + '"')

    technical_data = technical_asset(technical['objectives'])
    technical_digest = hashlib.sha256(technical_data.encode()).hexdigest()[:12]
    for rel in written:
        written[rel] = written[rel].replace('assets/technical-bridges-data.js"', 'assets/technical-bridges-data.js?v=' + technical_digest + '"')
    course_payload = course_asset(course_data)
    course_digest = hashlib.sha256(course_payload.encode()).hexdigest()[:12]
    for rel in written:
        written[rel] = written[rel].replace('assets/course-coach-data.js"', 'assets/course-coach-data.js?v=' + course_digest + '"')
    visual_data = visual_asset(visual_stories)
    visual_digest = hashlib.sha256(visual_data.encode()).hexdigest()[:12]
    for rel in written:
        written[rel] = written[rel].replace('assets/visual-walkthrough-data.js"', 'assets/visual-walkthrough-data.js?v=' + visual_digest + '"')

    for rel, text in written.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    (out / 'assets/visual-walkthrough-data.js').write_text(visual_data)
    (out / 'assets/course-coach-data.js').write_text(course_payload)
    (REPO / 'output/sitewide-coach').mkdir(parents=True, exist_ok=True)
    (REPO / 'output/sitewide-coach/IMPLEMENTED-SURFACES.json').write_text(json.dumps(course_manifest,indent=2)+'\n')
    from layered_teaching import asset as layered_asset
    (out / 'assets/layered-teaching.js').write_text(layered_asset(site, variants, REPO))
    sys.path.insert(0, str(REPO / 'tools'))
    (out / 'assets/technical-bridges-data.js').write_text(technical_data)
    (REPO / 'output/technical-bridge').mkdir(parents=True, exist_ok=True)
    (REPO / 'output/technical-bridge/IMPLEMENTED-PLACEMENTS.json').write_text(json.dumps(technical['pages'],indent=2)+'\n')
    from build_practice import build as build_practice
    build_practice(site_out=out)
    fixture = site.src / '06-Labs/02-CCAR-F-coordinator-extraction/decision_variant_fixtures.py'
    if fixture.exists():
        (out / 'downloads').mkdir(exist_ok=True)
        shutil.copyfile(fixture, out / 'downloads/decision_variant_fixtures.py')
    architecture_fixture = site.src / '06-Labs/08-CCAR-F-architecture-decisions/architecture_decisions.py'
    if architecture_fixture.exists():
        (out / 'downloads').mkdir(exist_ok=True)
        shutil.copyfile(architecture_fixture, out / 'downloads/architecture_decisions.py')
    # Explicitly approved original offline exercises only; never publish the research package.
    for filename in ('benchmark_exercises.py', 'benchmark-fixtures.json'):
        source = site.src / '06-Labs/08-CCAR-F-architecture-decisions' / filename
        if source.exists():
            (out / 'downloads').mkdir(exist_ok=True)
            shutil.copyfile(source, out / 'downloads' / filename)
    for rel, f in deck_files.items():  # the deck downloads the flashcard pages advertise
        shutil.copyfile(f, out / rel)

    if site.exported:
        problems = []
        print("question-bank leak check skipped: it runs when the sources are exported from the workspace")
    else:
        problems = check_question_leak(site.src, written)
        if args.export:
            n = export_content(site, args.export.resolve(), site.reviewed)
            print(f"exported {n} page sources into {args.export}")
    problems += sorted(set(site.problems))
    print(f"built {len(written)} pages into {out}")
    for k, e in EXAMS.items():
        c = counts(site, k)
        print(f"  {e['code']}: {c['lessons']} lessons, {c['scen']} scenario simulations, {c['labs']} labs")
        if c["scen"] < 4:
            problems.append(f"depth parity: {e['code']} has {c['scen']} scenario simulations; every exam needs at least 4")
    if problems:
        print("BUILD PROBLEMS:", *problems, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
