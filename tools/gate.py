#!/usr/bin/env python3
"""Quality gate for docs/. Exits non-zero if any check fails. No third-party packages.

    python3 tools/gate.py            # checks docs/
    python3 tools/gate.py --verbose  # also lists every page checked

Checks map to the non-functional requirements in the project's SITE-PLAN (NFR-01 to NFR-13).
Colleague names are checked against SHA-256 hashes in tools/blocklist.sha256, so the names
themselves never live in this repository.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
MAX_BYTES = 200_000
FRESH_DAYS = 60
# Mermaid 12.1.0 from npm (MIT). It draws diagrams in the browser; the site loads nothing from outside.
VENDOR = {"mermaid-12.1.0.min.js": ("6484afc32872a3aa16cac9a76ba1816a1ed4cc870a6593cc2e17757750f518b2", "LICENSE-mermaid.txt")}

SCOPE_TERMS = re.compile(r"agentforce|einstein|data cloud|trailhead|salesforce certif", re.I)
SLACK = re.compile(r"slack\.com|slack://|\b[CUWT]0[A-Z0-9]{7,10}\b|\bp1\d{15}\b")
SECRETS = re.compile(r"ghp_[A-Za-z0-9]{20,}|xox[bpas]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|sk-ant-[A-Za-z0-9_-]{10,}|(?<![A-Za-z])sk-[A-Za-z0-9_]{20,}")
TRACKING = re.compile(r"document\.cookie|XMLHttpRequest|\bfetch\(|navigator\.sendBeacon|gtag\(|google-analytics|googletagmanager", re.I)
INTERNAL_HOSTS = re.compile(r"gateway\.[a-z0-9.-]*salesforce|\.internal\.salesforce|\.sfdc\.net", re.I)
SCOPE_RULE = "Never Salesforce Agentforce, Einstein, Data Cloud or Salesforce certifications."
WORKSPACE_FOLDER = re.compile(r"\b(?:01-Curriculum|02-Lessons|03-Practice-Sessions|04-Simulations|05-Practice-Tool|"
                              r"06-Labs|07-Concept-Wiki|08-Reference|09-Proof|10-Learning-Site|11-Lessons-Learned|"
                              r"12-Progress|0\d-(?:Associate|Architect|Developer)-Track|0\d-CC[A-Z]{2}-[FP]-[A-Za-z-]+)\b")
PERSONAL_NOTE = re.compile(r"\bAmar(?:['\u2019]s)?\b|\byour progress log\b|\bin your own study workspace\b|"
                           r"\bsay\W{1,3}(?:start lesson|run practice|drill me|run simulation|run amey)", re.I)
HANG_CODES = [("lesson code", r"\bL0\d\b(?!-\w)"), ("simulation code", r"\bSIM-0\d\b(?!-)"), ("lab code", r"\bLab 0\d\b"),
              ("domain code", r"\bD[1-5]\b"), ("gate code", r"\bG(?:1[0-2]|\d)\b")]
PAGE_TITLES: set = set()
GOVERNANCE_PAGES = {"how-we-build.html"}
ANTHROPIC_SAYS = re.compile(r"\bAnthropic(?:['\u2019]s)?\s+(?:own\s+)?(?:recommend(?:s|ed|ation)?|says|said|advis(?:es|ed)|"
                            r"suggest(?:s|ed)?|advice)\b", re.I)
TIER1_LINK = re.compile(r"href=[\"']https?://(?:[a-z0-9-]+\.)*(?:anthropic\.com|claude\.com|claude\.ai|skilljar\.com)(?:[/:?#\"']|$)", re.I)
BLOCK_EDGE = re.compile(r"</?(?:p|li|td|th|dd|dt|blockquote|figcaption|h[1-6]|ul|ol|dl|div|tr|table|section|article|header|nav|details|summary)\b[^>]*>")
PERSONAL = re.compile(r"(^|/)(TRACKER\.md|12-Progress|session-logs|09-Proof|private|names\.txt)(/|$)")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.assets, self.ids, self.text = [], [], set(), []
        self.h1 = 0
        self.reviewed_source = None
        self.lang = self.title = self.reviewed = self.viewport = None
        self.imgs_no_alt = 0
        self.css = False
        self.in_title = self.in_script = False
        self.svg_unlabelled = 0
        self.attr_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k, v in attrs:
            if v and k not in ("class", "style", "rel", "type", "lang", "role"):
                self.attr_text.append(re.sub(r"[-_/.#?=&%+]", " ", v))
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self.in_title = True
        if tag == "script":
            self.in_script = True
            if a.get("src"):
                self.assets.append(a["src"])
        if tag == "link" and a.get("href"):
            self.assets.append(a["href"])
            if a.get("rel") == "stylesheet" and urlsplit(a["href"]).path.endswith("assets/site.css"):
                self.css = True
        if tag == "img":
            self.assets.append(a.get("src", ""))
            if not a.get("alt"):
                self.imgs_no_alt += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "svg" and a.get("role") != "img" and not a.get("aria-hidden") and not (a.get("role") == "group" and a.get("aria-label")):
            self.svg_unlabelled += 1
        if tag == "meta":
            if a.get("name") == "reviewed-source":
                self.reviewed_source = a.get("content")
            if a.get("name") == "reviewed":
                self.reviewed = a.get("content")
            if a.get("name") == "viewport":
                self.viewport = a.get("content")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data
        if not self.in_script:
            self.text.append(data)


def words_of(text: str) -> list[str]:
    folded = "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))
    return re.findall(r"[^\W\d_]+", folded)


def ngram_hashes(text: str) -> set[str]:
    words = words_of(text)
    out = set()
    for n in (1, 2, 3, 4):
        for i in range(len(words) - n + 1):
            out.add(hashlib.sha256(" ".join(words[i:i + n]).encode()).hexdigest())
    return out


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def css_tokens(css: str, selector: str) -> dict[str, str]:
    m = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S)
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", m.group(1))) if m else {}


def main():
    verbose = "--verbose" in sys.argv
    fails: list[tuple[str, str, str]] = []

    def fail(nfr, where, what):
        fails.append((nfr, where, what))

    for f in REPO.rglob("*"):
        rel = f.relative_to(REPO).as_posix()
        if not rel.startswith(".git/") and PERSONAL.search(rel):
            fail("NFR-05", rel, "personal study file (tracker, progress, session log, proof or names); it stays in the study workspace")

    if not DOCS.exists():
        print("docs/ does not exist; run site/build.py first")
        sys.exit(2)
    blockfile = REPO / "tools" / "blocklist.sha256"
    blocked = {l.strip() for l in blockfile.read_text().splitlines() if l.strip() and not l.startswith("#")} if blockfile.exists() else set()
    if not blocked:
        fail("NFR-05", "tools/blocklist.sha256", "blocklist missing or empty; run tools/make_blocklist.py")

    css_path = DOCS / "assets" / "site.css"
    css = css_path.read_text() if css_path.exists() else ""
    if re.search(r"url\(\s*['\"]?(https?:)?//|@import", css):
        fail("NFR-03", "assets/site.css", "external url() or @import")
    if "@media print" not in css:
        fail("NFR-10", "assets/site.css", "no print stylesheet")
    for sel, label in ((":root", "light"), (':root[data-theme="dark"]', "dark")):
        t = css_tokens(css, sel)
        for fg, bg in (("ink", "bg"), ("muted", "bg"), ("ink", "surface"), ("muted", "surface"),
                       ("associate", "bg"), ("architect", "bg"), ("developer", "bg"),
                       ("associate", "associate-soft"), ("architect", "architect-soft"), ("developer", "developer-soft")):
            if fg in t and bg in t and contrast(t[fg], t[bg]) < 4.5:
                fail("NFR-01", f"site.css {label}", f"contrast {fg} on {bg} is {contrast(t[fg], t[bg]):.2f}, needs 4.5")
    js = "".join(p.read_text() for p in (DOCS / "assets").glob("*.js"))
    if TRACKING.search(js):
        fail("NFR-04", "assets/*.js", "network or tracking call in script")
    for name, (sha, licence) in VENDOR.items():  # third-party code is pinned by hash and ships with its licence
        f = DOCS / "assets" / "vendor" / name
        if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != sha:
            fail("NFR-04", f"assets/vendor/{name}", "missing, or not the pinned release (hash differs)")
        if not (DOCS / "assets" / "vendor" / licence).exists():
            fail("NFR-03", f"assets/vendor/{licence}", "licence file missing for vendored code")
    for f in (DOCS / "assets" / "vendor").glob("*.js"):
        if f.name not in VENDOR:
            fail("NFR-04", f"assets/vendor/{f.name}", "unpinned vendored script")

    pages = sorted(DOCS.rglob("*.html"))
    parsed: dict[Path, Page] = {}
    for p in pages:  # page-title allow-list: an h1 may name a code only if it equals a built page's title
        tm = re.search(r'<title>(.*?) · Claude Certifications Study Site</title>', p.read_text(), re.S)
        if tm:
            PAGE_TITLES.add(html.unescape(re.sub(r'<[^>]+>', '', tm.group(1))).strip())
    for p in pages:
        raw = p.read_text()
        rel = p.relative_to(DOCS).as_posix()
        if p.name.startswith("_"):
            fail("NFR-05", rel, "draft or working file (name starts with _); it stays in the study workspace")
        pg = Page()
        pg.feed(raw)
        parsed[p] = pg
        if p.stat().st_size > MAX_BYTES:
            fail("NFR-02", rel, f"{p.stat().st_size // 1000} KB is over 200 KB")
        for a in pg.assets:
            if re.match(r"(https?:)?//", a):
                fail("NFR-03", rel, f"external asset {a}")
        if TRACKING.search(raw):
            fail("NFR-04", rel, "network or tracking call")
        text = " ".join(pg.text)
        if SCOPE_TERMS.search(raw):
            fail("NFR-05", rel, f"out-of-scope term: {SCOPE_TERMS.search(raw).group(0)}")
        if SLACK.search(raw):
            fail("NFR-05", rel, f"Slack link or ID: {SLACK.search(raw).group(0)}")
        if INTERNAL_HOSTS.search(raw):
            fail("NFR-05", rel, "internal host name")
        hits = (ngram_hashes(text) | ngram_hashes(" ".join(pg.attr_text))) & blocked
        if hits:
            fail("NFR-05", rel, f"{len(hits)} blocklisted colleague name(s); check the names file and rebuild")
        if SECRETS.search(raw):
            fail("NFR-09", rel, "possible secret")
        body0 = (re.search(r"<main.*?</main>", raw, re.S) or re.search(r".*", raw, re.S)).group(0)
        body = re.sub(r"<(code|pre)\b.*?</\1>", " ", body0, flags=re.S)
        prose = html.unescape(re.sub(r"<[^>]+>", " ", body))
        scan = re.sub(r"<(code|pre|a|abbr|script|style)\b.*?</\1>", " ", body0, flags=re.S)
        scan = re.sub(r"<h1\b.*?</h1>", lambda m: " " if re.sub(r"<[^>]+>", "", html.unescape(m.group(0))).strip() in PAGE_TITLES else m.group(0), scan, flags=re.S)
        scan = html.unescape(re.sub(r"<[^>]+>", " ", scan))
        for label, rx in HANG_CODES:
            hm = re.search(rx, scan)
            if hm:
                fail("NFR-12", rel, f"unlinked {label} in body text: ...{scan[max(0, hm.start()-25):hm.end()+25].strip()}...")
        if "**" in prose:
            fail("NFR-05", rel, "leftover ** in page text (unconverted markdown)")
        if rel not in GOVERNANCE_PAGES:
            if WORKSPACE_FOLDER.search(prose):
                fail("NFR-05", rel, f"study-workspace folder name: {WORKSPACE_FOLDER.search(prose).group(0)}")
            if PERSONAL_NOTE.search(prose):
                fail("NFR-05", rel, f"personal study note: {PERSONAL_NOTE.search(prose).group(0)}")
            if re.search(r"\bS0\d\b", prose):
                fail("NFR-05", rel, f"private practice-session code: {re.search(r'\bS0\d\b', prose).group(0)}")
        for block in BLOCK_EDGE.split(body):
            words = html.unescape(re.sub(r"<[^>]+>", " ", block))
            said = ANTHROPIC_SAYS.search(words)
            if said and not TIER1_LINK.search(block) and not re.search(r"\brelayed\b", words, re.I):
                fail("NFR-05", rel, f"\"{said.group(0)}\" with no Tier 1 link in the same paragraph (relayed advice must say so)")
        if not pg.lang:
            fail("NFR-01", rel, "missing <html lang>")
        if not (pg.title or "").strip():
            fail("NFR-01", rel, "missing <title>")
        if pg.h1 != 1:
            fail("NFR-01", rel, f"{pg.h1} <h1> elements, expected 1")
        if pg.imgs_no_alt:
            fail("NFR-01", rel, f"{pg.imgs_no_alt} image(s) without alt text")
        if pg.svg_unlabelled:
            fail("NFR-01", rel, "SVG without role=img or aria-hidden")
        if not pg.viewport:
            fail("NFR-07", rel, "missing viewport meta")
        if not pg.css:
            fail("NFR-10", rel, "page doesn't load assets/site.css (print styles)")
        if rel.startswith("exams/"):
            if not re.search(r'class="review-line">\s*Last reviewed:', raw):
                fail("NFR-06", rel, "no visible 'Last reviewed' line")
            if pg.reviewed_source != "recorded":
                fail("NFR-06", rel, "no recorded review (REVIEWS.json); the date must come from a recorded review, never file time")
            else:
                try:
                    age = (dt.date.today() - dt.date.fromisoformat(pg.reviewed or "")).days
                    if age > FRESH_DAYS:
                        fail("NFR-06", rel, f"reviewed {age} days ago, limit {FRESH_DAYS}")
                except ValueError:
                    fail("NFR-06", rel, "no reviewed date")

    for p, pg in parsed.items():
        rel = p.relative_to(DOCS).as_posix()
        for href in pg.links:
            if re.match(r"(https?:|mailto:)", href):
                continue
            parts = urlsplit(unquote(href))
            path, anchor = parts.path, parts.fragment
            target = (p.parent / path).resolve() if path else p
            if target.is_dir():
                target = target / "index.html"
            if DOCS.resolve() not in target.resolve().parents and target.resolve() != DOCS.resolve():
                fail("NFR-08", rel, f"link leaves docs/: {href}")
            elif not target.exists():
                fail("NFR-08", rel, f"broken link {href}")
            elif anchor and target.suffix == ".html":
                tp = parsed.get(target)
                if tp is not None and anchor not in tp.ids:
                    fail("NFR-08", rel, f"missing anchor {href}")

    sources = sorted((REPO / "content").rglob("*.md")) + sorted(REPO.glob("*.md"))
    for p in sources:
        raw, rel = p.read_text().replace(SCOPE_RULE, ""), p.relative_to(REPO).as_posix()
        for rx, nfr, what in ((SCOPE_TERMS, "NFR-05", "out-of-scope term"), (SLACK, "NFR-05", "Slack link or ID"),
                              (INTERNAL_HOSTS, "NFR-05", "internal host name"), (SECRETS, "NFR-09", "possible secret")):
            if rx.search(raw):
                fail(nfr, rel, f"{what}: {rx.search(raw).group(0)[:40]}")
        hits = ngram_hashes(raw) & blocked
        if hits:
            fail("NFR-05", rel, f"{len(hits)} blocklisted colleague name(s); re-export from the workspace")

    bank = REPO / "practice" / "question-bank.json"
    if bank.exists():
        shareable = ("Anthropic official exam guide", "Amey Thakur CLAUDE-CERTIFICATIONS repo")
        qs = json.loads(bank.read_text())["questions"]
        authored = REPO / "practice" / "project-authored-originals.json"
        approved_originals = {q["id"]: q for q in json.loads(authored.read_text()).get("questions", [])} if authored.exists() else {}
        vr = REPO / "assessment" / "variant-review.json"
        approved_variants = set(json.loads(vr.read_text()).get("approved_ids", [])) if vr.exists() else set()
        variant_source = REPO / "assessment" / "ccarf-variant-items.json"
        source_records = {q["id"]: q for q in json.loads(variant_source.read_text()).get("questions", [])} if variant_source.exists() else {}
        reviews = json.loads(vr.read_text()).get("items", {}) if vr.exists() else {}
        for q in qs:
            if q["id"] not in approved_variants:
                continue
            original = source_records.get(q["id"])
            expected = reviews.get(q["id"], {}).get("content_sha256")
            if not original or hashlib.sha256(json.dumps(original, sort_keys=True).encode()).hexdigest() != expected:
                fail("NFR-05", "assessment/", "approved variant changed since independent review: " + q["id"])
            elif any(q.get(k) != value for k, value in original.items()):
                fail("NFR-05", "practice/", "adapter changed an approved original field: " + q["id"])
        bad = [q["id"] for q in qs if not (q["source"].startswith(shareable) or
              (q.get("origin") == "project-authored" and (q["id"] in approved_variants or approved_originals.get(q["id"]) == q)))]
        if bad:
            fail("NFR-05", "practice/question-bank.json", f"{len(bad)} question(s) from a source we may not share, e.g. {bad[0]}")
        if not (REPO / "practice" / "LICENSE-amey-thakur.txt").exists():
            fail("NFR-05", "practice/", "Amey Thakur's MIT licence file is missing")
        page = REPO / "practice" / "index.html"
        if not page.exists():
            fail("NFR-05", "practice/", "index.html is missing; run python3 tools/build_practice.py")
        else:
            embedded = re.search(r"const DATA = (.*?);\nconst STORE_KEY", page.read_text(), re.S)
            try:
                built_data = json.loads(embedded.group(1)) if embedded else None
                if not built_data or built_data.get("questions") != qs:
                    fail("NFR-05", "practice/index.html", "question records do not match question-bank.json; rebuild practice")
            except (ValueError, AttributeError):
                fail("NFR-05", "practice/index.html", "embedded question payload cannot be parsed")
            if "MIT License" not in page.read_text():
                fail("NFR-05", "practice/index.html", "the MIT licence notice is missing from the page")
        sys.path.insert(0, str(REPO / "tools"))
        from build_practice import EXCLUDE
        back = sorted({q["id"] for q in qs} & set(EXCLUDE))
        if back:
            fail("NFR-05", "practice/question-bank.json", f"{len(back)} question(s) the accuracy check left out are back, e.g. {back[0]}")
        for p in (bank, page):
            if not p.exists():
                continue
            raw = p.read_text()
            for rx, what in ((SLACK, "Slack link or ID"), (INTERNAL_HOSTS, "internal host name"), (SECRETS, "possible secret")):
                if rx.search(raw):
                    fail("NFR-05", p.relative_to(REPO).as_posix(), f"{what}: {rx.search(raw).group(0)[:40]}")
            if ngram_hashes(raw) & blocked:
                fail("NFR-05", p.relative_to(REPO).as_posix(), "blocklisted colleague name(s)")

    # NFR-13 (B63-FX-5): flashcard decks. Answers start hidden; an advertised download exists, parses as CSV and has
    # the page's card count and questions; the download carries no secrets or blocklisted names.
    import csv as _csv
    plain = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
    for page in sorted(DOCS.rglob("flashcards.html")):
        rel = page.relative_to(DOCS).as_posix()
        raw = page.read_text()
        cards = re.findall(r'<div class="fc" id="card-\d+">.*?<p class="fc-q">(.*?)</p><details class="fc-a">', raw, re.S)
        if not cards:
            fail("NFR-13", rel, "no question-first cards found")
            continue
        if re.search(r'<details class="fc-a" open', raw):
            fail("NFR-13", rel, "an answer is open by default")
        for href in re.findall(r'<a href="([^"#]+\.csv)" download>', raw):
            f = page.parent / href
            if not f.exists():
                fail("NFR-13", rel, f"advertised download {href} is missing")
                continue
            text = f.read_text(encoding="utf-8")
            try:
                rows = [r for r in list(_csv.reader(text.splitlines()))[1:] if r]
            except _csv.Error as e:
                fail("NFR-13", href, f"does not parse as CSV: {e}")
                continue
            if len(rows) != len(cards) or any(len(r) != 3 for r in rows):
                fail("NFR-13", href, f"{len(rows)} rows (3 columns each expected); page has {len(cards)} cards")
            fronts = " ".join(re.sub(r"\s+", " ", r[0]) for r in rows)
            missing = [q for q in cards if plain(q) not in fronts]
            if missing:
                fail("NFR-13", href, f"{len(missing)} page question(s) not in the download, e.g. {plain(missing[0])[:60]}")
            for rx, what in ((SLACK, "Slack link or ID"), (INTERNAL_HOSTS, "internal host name"), (SECRETS, "possible secret")):
                if rx.search(text):
                    fail("NFR-05", href, f"{what}: {rx.search(text).group(0)[:40]}")
            if ngram_hashes(text) & blocked:
                fail("NFR-05", href, "blocklisted colleague name(s)")

    # NFR-12 (B63-FX-7): CCAR-F objective header shape, official task statement, domain weight and bullet coverage
    # (IDs in guide order; quoted bullet text word for word). Needs the study source, so it runs when CERT_SRC is set.
    import os, subprocess
    src = os.environ.get("CERT_SRC")
    if src and (Path(src) / "01-Curriculum/02-Architect-Track/CCAR-F-objectives.md").exists():
        r = subprocess.run([sys.executable, str(REPO / "tools/objective_check.py"), "--src", src], capture_output=True, text=True)
        print((r.stdout.strip().splitlines() or ["no output"])[-1])
        for line in r.stdout.splitlines():
            if line.startswith("FAIL "):
                fail("NFR-12", "objective_check.py", line[5:])
        if r.returncode != 0 and not any(l.startswith("FAIL ") for l in r.stdout.splitlines()):
            fail("NFR-12", "objective_check.py", (r.stderr or r.stdout)[-200:])
    else:
        print("objective_check: skipped (set CERT_SRC to the study source; publish.sh always runs it)")

    # NFR-14 (B63-FX-13): every shared CCAR-F question is mapped to real objectives or explicitly unmapped,
    # and bank, domain and status totals reconcile. Needs no study source.
    r = subprocess.run([sys.executable, str(REPO / "tools/question_map_check.py")], capture_output=True, text=True)
    print((r.stdout.strip().splitlines() or ["no output"])[-1])
    for line in r.stdout.splitlines():
        if line.startswith("FAIL "):
            fail("NFR-14", "question_map_check.py", line[5:])
    if r.returncode != 0 and not any(l.startswith("FAIL ") for l in r.stdout.splitlines()):
        fail("NFR-14", "question_map_check.py", (r.stderr or r.stdout)[-200:])

    # NFR-11 (HR-23): no hanging references. Runs the private study-site checker when it is present (it is not in the pushed repo).
    import os, subprocess
    cr = Path(os.environ.get("CERT_SRC", str(REPO.parent.parent))) / "10-Learning-Site/private/ccar-f-study-site/check_refs.py"
    if cr.exists():
        # A render saved by the private pw_jobs.py (Playwright MCP, no sandbox escape) is used when it is newer than both pages.
        saved = Path("/tmp/check_refs_dump.pw.json")
        pages_in = [cr.parent / "site/index.html", cr.parent.parent / "index.html"]
        fresh = saved.exists() and all(q.exists() and saved.stat().st_mtime >= q.stat().st_mtime for q in pages_in)
        args = [sys.executable, str(cr)] + (["--dump", str(saved)] if fresh else [])
        print("check_refs:", "using the saved Playwright render" if fresh else "rendering in headless Chrome (needs elevation)")
        try:
            r = subprocess.run(args, capture_output=True, text=True, timeout=1500)
        except subprocess.TimeoutExpired:
            r = subprocess.CompletedProcess(args, 1, "check_refs.py timed out after 1500 s", "")
        tail = [l for l in r.stdout.splitlines() if l.startswith(("TOTAL HITS", "links clicked"))]
        print("check_refs:", " | ".join(tail) or r.stdout[-200:] + r.stderr[-200:])
        if r.returncode != 0:
            fail("NFR-11", "check_refs.py", "hanging references found; run it for the list: " + " | ".join(tail))
    else:
        print("check_refs: skipped (private study site not present here)")

    print(f"gate: {len(pages)} pages and {len(sources)} page sources checked")
    if verbose:
        for p in pages:
            print("  ", p.relative_to(DOCS).as_posix())
    if fails:
        by = {}
        for nfr, where, what in fails:
            by.setdefault(nfr, []).append(f"{where}: {what}")
        for nfr in sorted(by):
            print(f"FAIL {nfr} ({len(by[nfr])})")
            for line in by[nfr][:25]:
                print("   ", line)
            if len(by[nfr]) > 25:
                print(f"    … {len(by[nfr]) - 25} more")
        sys.exit(1)
    print("PASS: NFR-01 to NFR-14; NFR-11 and NFR-12 say above if they were skipped (NFR-07 checks the viewport only; test on a phone before each release)")


if __name__ == "__main__":
    main()
