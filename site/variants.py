"""Registry-backed navigation; teaching packets remain in their canonical authored pages."""
from collections import defaultdict
from pathlib import Path
import html
import json
import posixpath
import re

OUT_REL = 'lessons/ccar-f/decision-variants.html'
REGISTRY = '02-Lessons/02-CCAR-F-Architect-Foundations/decision-variants.json'

def records(site):
    p = site.src / REGISTRY
    if not p.exists():
        return []
    data = json.loads(p.read_text())
    return data.get('variants', []) if isinstance(data, dict) else data

def target(site, source):
    return next((out for src, out in site.pages.items() if src.endswith('/' + source) or src == source), None)

def href(out_rel, destination, anchor=''):
    return posixpath.relpath(destination, posixpath.dirname(out_rel)) + ('#' + anchor if anchor else '')

def preview(label):
    # A labelled navigation thumbnail, not an invented solution diagram.
    return ('<svg class="scn-preview" viewBox="0 0 480 80" role="img" aria-label="Decision learning sequence">'
            '<g fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="12" width="138" height="52" rx="8"/>'
            '<path d="M142 38h27m-7-5 7 5-7 5"/><rect x="172" y="12" width="138" height="52" rx="8"/>'
            '<path d="M312 38h27m-7-5 7 5-7 5"/><rect x="342" y="12" width="136" height="52" rx="8"/></g>'
            '<g fill="currentColor" font-size="20" text-anchor="middle"><text x="70" y="44">Scenario</text>'
            '<text x="242" y="44">Constraint</text><text x="410" y="44">Decision</text></g></svg>')

def hub(site, rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row['family_id']].append(row)
    cards = []
    for family, items in groups.items():
        title = items[0].get('family_title', family.replace('-', ' ').title())
        links = []
        for row in items:
            destination = target(site, row['canonical_source'])
            if not destination:
                site.problems.append('variant canonical source missing: ' + row['variant_id'])
                continue
            link = html.escape(href(OUT_REL, destination, row['canonical_anchor']))
            links.append(f'<li><a href="{link}">{html.escape(row["variant_id"] + " · " + row["title"])}</a> — Objective {row["primary_objective"]}</li>')
        cards.append(f'<section class="scn-card" id="{html.escape(family)}"><h2>{html.escape(title)}</h2>{preview(title)}<ul>{"".join(links)}</ul></section>')
    return ('<article class="prose"><h1>Architecture decision variants</h1><p>Practise how a changed constraint changes the architecture choice. Each packet includes a base case, failure and recovery, concrete mechanism, blind check and different retry. These original supplemental scenarios support the official objectives; they are not a complete inventory of possible exam cases.</p>'
            '<p><a href="skill-coverage.html">Inspect all 240 knowledge-and-skill coverage rows</a></p><p><a href="decision-atlas.html">Explore architecture drawings and flowcharts</a> · <a href="decision-conversation.html">Listen and converse</a></p><p><a href="../../exams/ccar-f.html">Return to your Architect Foundations study plan</a> · <a href="../../practice/index.html?exam=CCAR-F">Practise and repair missed decisions</a></p><div class="scenario-map">' + ''.join(cards) + '</div></article>')

def contextual(site, rows, out_rel):
    relevant = []
    objective = re.search(r'objective-(\d\.\d)\.html', out_rel)
    domain = re.search(r'/L0([1-5])-', out_rel)
    for row in rows:
        walk = target(site, row['walkthrough_source'])
        if (objective and row['primary_objective'] == objective.group(1)) or (domain and row['primary_objective'].startswith(domain.group(1)+'.')) or walk == out_rel:
            destination = target(site, row['canonical_source'])
            if destination:
                practice = href(out_rel, 'practice/index.html') + '?exam=CCAR-F&objective=' + row['primary_objective'] + '&variant=' + row['variant_id']
                relevant.append(f'<li><a href="{html.escape(href(out_rel, destination, row["canonical_anchor"]))}">{html.escape(row["variant_id"] + " · " + row["title"])}</a> · <a href="{html.escape(practice)}">Practise this decision</a></li>')
    if not relevant:
        return ''
    if not out_rel.startswith('lessons/ccar-f/'):
        return '<nav class="variant-links" aria-label="Decision variants for this lesson"><b>Practise the architecture choice</b><ul>' + ''.join(relevant) + '</ul><a href="' + href(out_rel, OUT_REL) + '">Explore all seven original decision families</a></nav>'
    return '<details class="variant-links related-decisions"><summary>Related decision practice (' + str(len(relevant)) + ')</summary><nav aria-label="Decision variants for this lesson"><ul>' + ''.join(relevant) + '</ul><a href="' + href(out_rel, OUT_REL) + '">Explore all seven original decision families</a></nav></details>'


def inline_aids(site, rows, out_rel, text):
    """Render canonical diagram code beside its authored at-point link, not a cloned lesson."""
    if not out_rel.startswith('lessons/ccar-f/'):
        return text
    atlas = site.src / '02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md'
    if not atlas.exists():
        return text
    raw = atlas.read_text()
    inserted = set()
    atlas_rel = href(out_rel, 'lessons/ccar-f/decision-atlas.html')
    pattern = r'<a href="' + re.escape(atlas_rel) + r'#diagram-(d\d+)">([^<]+)</a>'
    def aid(match):
        did = match.group(1).upper()
        if did in inserted:
            return match.group(0)
        section = re.search(r'^## ' + re.escape(did) + r' .*?(?=^## D\d+|\Z)', raw, re.M | re.S)
        if not section:
            return match.group(0)
        charts = re.findall(r'```mermaid\n(.*?)```', section.group(0), re.S)
        if not charts:
            return match.group(0)
        inserted.add(did)
        procedure = re.search(r'\*\*Equivalent decision procedure:\*\* (.*)', section.group(0))
        equivalent = procedure.group(1) if procedure else 'Follow the labelled decisions and recovery boundary; consult the full source for assumptions.'
        return match.group(0) + '<details class="point-aid"><summary>Inspect ' + did + ' here</summary><p>' + html.escape(equivalent) + '</p>' + ''.join('<div class="mmd"><pre class="mermaid">'+html.escape(c)+'</pre></div>' for c in charts) + '</details>'
    text = re.sub(pattern, aid, text)
    if inserted and 'assets/viewer.js' not in text:
        root = '../' * out_rel.count('/')
        includes = f'<link rel="stylesheet" href="{root}assets/viewer.css"><script defer src="{root}assets/vendor/mermaid-12.1.0.min.js"></script><script defer src="{root}assets/viewer.js"></script>'
        text = text.replace('</head>', includes+'</head>')
    return text


def walkthrough_gallery(site, rows):
    """Six actual canonical job charts, not generic decorative thumbnails."""
    cards, seen = [], set()
    for row in sorted(rows, key=lambda item: (int(m.group(1)) if (m := re.search(r"WT(\d+)", item["walkthrough_source"].rsplit("/", 1)[-1], re.I)) else 999, item["walkthrough_source"])):
        source = row['walkthrough_source']
        if source in seen:
            continue
        seen.add(source)
        full = next((s for s in site.pages if s.endswith('/'+source)), None)
        if not full:
            continue
        text = site.path(full).read_text()
        chart = re.search(r'```mermaid\n(.*?)```', text, re.S)
        if not chart:
            continue
        destination = site.pages[full]
        cards.append('<section class="scn-card"><h3><a href="'+html.escape(href('lessons/ccar-f/scenario-walkthroughs/index.html',destination))+'">'+html.escape(source.rsplit('/',1)[-1].replace('.md','').replace('-',' '))+'</a></h3><details class="point-aid"><summary>Inspect this walkthrough flow here</summary><div class="mmd"><pre class="mermaid">'+html.escape(chart.group(1))+'</pre></div><p>Use the labelled choices, exceptions and recovery paths. Open the walkthrough for the full textual step-by-step explanation.</p></details></section>')
    return '<section><h2>The six job flows at a glance</h2><div class="scenario-map">'+''.join(cards)+'</div></section>'


def miss_repair_anchors(site, variants, outrel, body):
    """Stable repair targets for learner-reported mistake categories; no grading inference."""
    categories = {
        'wrong-signal': 'Choose in the base case.',
        'wrong-mechanism': 'Inspect the artifact',
        'wrong-scope': 'Change one constraint.',
        'wrong-timing': 'Change one constraint.',
        'missing-validation': 'Proof before accepting success:',
        'unsafe-recovery': 'What failed, and who recovers?',
        'provenance-loss': 'Proof before accepting success:',
        'instruction-conflict': 'Why not the nearest alternative?',
    }
    for variant in variants:
        source = variant['canonical_source']
        if target(site, source) != outrel:
            continue
        anchor = variant['canonical_anchor']
        pattern = re.compile(r'(<a id="'+re.escape(anchor)+r'"></a>\s*<h2\b[^>]*>.*?</h2>)(.*?)(?=<h2\b|\Z)', re.S)
        def annotate(match):
            region = match.group(2)
            for category, label in categories.items():
                needle = '<p><strong>' + label
                if needle not in region:
                    raise ValueError(anchor+': missing precise repair section '+category)
                region = region.replace(needle, '<a id="'+anchor+'-'+category+'"></a>'+needle, 1)
            return match.group(1)+region
        body, count = pattern.subn(annotate, body, count=1)
        if count != 1:
            raise ValueError(anchor+': expected one canonical variant packet for category repairs')
    return body
