"""Diagram-first narrated application lessons, backed by authored scenario JSON."""
from pathlib import Path
import html
import json
import re

ROOT='02-Lessons/02-CCAR-F-Architect-Foundations/'
FILES=('visual-walkthroughs.json','visual-walkthroughs-other.json')

def stories(site):
    lessons={}
    for filename in FILES:
        p=site.src/ROOT/filename
        if p.exists():
            data=json.loads(p.read_text())['lessons']
            if lessons.keys() & data.keys():raise ValueError('Duplicate visual story')
            lessons.update(data)
    from integrated_teaching import apply
    lessons=apply(site,lessons)
    detail_path=site.src/ROOT/'visual-connection-details.json'
    if not detail_path.exists():raise ValueError('Missing authored visual connection details')
    details=json.loads(detail_path.read_text())['lessons']
    notes=json.loads((site.src/ROOT/'visual-focus-notes.json').read_text())
    cues=json.loads((site.src/ROOT/'boundary-decision-cues.json').read_text())['lessons']
    intro=json.loads((site.src/ROOT/'boundary-intro-decision.json').read_text())
    for slug,lesson in lessons.items():
        cue=cues[slug]
        assert set(cue['nodes'])==set(lesson['nodes']),(slug,'Missing boundary node')
        assert set(cue['edges'])==set(details[slug]),(slug,'Missing boundary edge')
        for item in list(cue['nodes'].values())+list(cue['edges'].values()):
            assert item.get('prompt') and item.get('why_here')
            target=item.get('target_stage')
            assert (target is None and item.get('reason')) or (isinstance(target,int) and 0<=target<len(lesson['stages']) and lesson['stages'][target].get('question')),(slug,'Invalid boundary decision target')
        lesson['boundaryCues']=cue
        if slug=='as-01-action-service':lesson['introDecision']=intro
        lesson['focusNotes']=notes['lessons'][slug]
        lesson['purposes']=notes['purposes'][slug]
        assert set(lesson['purposes'])==set(lesson['nodes'])
        assert all(isinstance(v,str) and v.strip() for v in lesson['purposes'].values()),(slug,'Empty component purpose')
        assert len(lesson['focusNotes'])==len(lesson['stages'])
        if slug not in details:raise ValueError('Missing connection detail set '+slug)
        lesson['connectionDetails']=details[slug]
        assert lesson['connectionDetails'],(slug,'Empty connection detail set')
        for detail in lesson['connectionDetails'].values():
            assert all(isinstance(detail.get(k),str) and detail[k].strip() for k in ('summary','payload','instruction','check')),(slug,'Incomplete connection detail')
    for slug,lesson in lessons.items():
        for i,stage in enumerate(lesson['stages']):
            for ph,part in [('setup',stage),('repair',stage.get('repair',{}))]:
                assert set(lesson['focusNotes'][i][ph])==set(part.get('highlight',[])),(slug,i,ph,'Missing why-now notes')
                assert all(isinstance(v,str) and v.strip() for v in lesson['focusNotes'][i][ph].values()),(slug,i,ph,'Empty why-now note')
            for state in [stage,stage.get('repair',{})]:
                if lesson.get('connectionDetails'):
                    for a,b,label in state.get('edges',[]):assert a+'>'+b+'|'+label in lesson['connectionDetails'],(slug,a,b,label)
                for key in ('visible','highlight','focus'):
                    assert set(state.get(key,[])) <= lesson['nodes'].keys(),(slug,stage['title'],key)
                for a,b,*_ in state.get('edges',[]):assert a in lesson['nodes'] and b in lesson['nodes']
            if 'question' in stage:
                q=stage['question'];assert 0<=q['answer']<len(q['options'])
                assert 'repair' in stage
    return lessons

def enhance(site,written):
    lessons=stories(site)
    for slug,lesson in lessons.items():
        rel='lessons/ccar-f/architecture-studio/'+slug+'.html'
        if rel not in written:raise ValueError('Missing visual story destination '+rel)
        doc=written[rel];match=re.search(r'<main\b[^>]*>(.*?)</main>',doc,re.S)
        if not match:raise ValueError('Missing main '+rel)
        reference=re.sub(r'<h1\b([^>]*)>(.*?)</h1>',r'<h2\1>Detailed reference: \2</h2>',match[1],count=1,flags=re.S)
        e=html.escape;stage=lesson['stages'][0]
        steps=''.join('<li><button type="button" data-stage="'+str(i)+'"'+(' aria-current="step"' if i==0 else '')+'><span>'+str(i+1)+'</span> '+e(s['title'])+'</button></li>' for i,s in enumerate(lesson['stages']))
        new=f'''<nav class="crumbs" aria-label="Breadcrumb"><a href="../../../exams/ccar-f.html">Architect Foundations</a> / <a href="index.html">Application stories</a> / {e(lesson['subtitle'].split(' · ')[0])}</nav>
<header class="vl-hero"><p class="vl-eyebrow">VISUAL ARCHITECTURE WALKTHROUGH · {e(lesson['subtitle'])}</p><h1>{e(lesson['title'])}</h1><p>{e(lesson['story'])}</p><div class="vl-badges"><span>No setup</span><span>Read or listen</span><span>Fictional example</span></div><p class="vl-route"><a href="../../../exams/ccar-f.html">← Learning home</a> · <a href="#visual-reference">Reference, contracts & exercises</a> · <button type="button" class="vl-course-toggle" aria-expanded="false">Course map</button></p></header>
<section class="vl-player" data-visual-story="{slug}" aria-label="Visual architecture lesson">
<nav class="vl-stage-nav" aria-label="Walkthrough stages"><ol>{steps}</ol></nav>
<nav class="vl-controls" aria-label="Lesson playback"><button type="button" class="vl-prev" disabled>← Back</button><button type="button" class="vl-replay">Replay this stage</button><div class="vl-audio"><button type="button" class="vl-play">Listen</button><button type="button" class="vl-stop" disabled>Stop</button><span>Browser voice</span></div><span class="vl-progress" role="status">Stage 1 of {len(lesson['stages'])}</span><button type="button" class="vl-next">Next layer →</button></nav><div class="vl-workspace"><section class="vl-visual" id="visual-diagram" aria-label="Evolving application diagram"><div class="vl-change"><span class="vl-step-count">1 / {len(lesson['stages'])}</span><span class="vl-map-status">{e(stage['kicker'])}</span></div><div class="vl-map-toolbar" aria-label="Diagram controls"><button type="button" data-zoom="out" aria-label="Zoom out diagram">−</button><button type="button" data-zoom="in" aria-label="Zoom in diagram">+</button><button type="button" data-zoom="fit">Fit all</button><button type="button" data-zoom="focus">Focus change</button><span>Hover for a preview · Select Details to read and practise</span><a href="#technical-current-stage">Plain ↔ technical example ↓</a></div><section class="vl-flow" aria-label="Trace diagram connections"><p class="vl-flow-caption" role="status"></p><div><button type="button" class="vl-flow-prev">← Previous connection</button><button type="button" class="vl-flow-next">Next connection →</button></div><small>One connection at a time. Numbers identify connections; branches still depend on their stated conditions.</small></section><div class="vl-map-frame" tabindex="0" aria-label="Architecture map. Scroll to pan; use the controls to zoom."><svg class="vl-map" viewBox="0 0 960 660" role="group" aria-label="Architecture for {e(lesson['title'])}"></svg></div><div class="vl-legend"><span class="kind-ai">AI proposes</span><span class="kind-software">Software enforces</span><span class="kind-data">External evidence / service</span><span>+ Added or changed</span></div><details class="vl-connections"><summary>Connections at this stage</summary><ul></ul></details></section>
<section class="vl-coach" aria-label="Current scene"><p class="vl-eyebrow vl-kicker">{e(stage['kicker'])}</p><h2 class="vl-title" tabindex="-1">{e(stage['title'])}</h2><p class="vl-narration">{e(stage['narration'])}</p><p class="vl-audio-status sr" role="status"></p><section id="vl-technical" class="vl-technical" aria-label="Technical diagram details"><p class="vl-eyebrow">APPLICATION TRACE <span class="vl-detail-status" role="status"></span></p><section class="vl-connection-detail"><h3></h3><p class="vl-technical-summary"></p><p class="vl-context-label">Illustrative message · current outcome is under Stage evidence</p><pre class="vl-technical-payload"></pre><dl></dl></section><section class="vl-inspector" hidden aria-label="Component details"><h3></h3><p></p><dl></dl><button type="button" class="vl-inspector-close">← Return to connection</button></section></section><details class="vl-stage-evidence"><summary>Stage evidence</summary><div class="vl-packet"><span></span><pre></pre></div></details><div class="vl-decision"></div></section></div>
<p class="vl-scope">You control the pace. These are unscored teaching decisions; listening or advancing does not mark mastery. Voice is generated by your browser, not a recorded soundtrack.</p>
</section>
<section class="vl-finish"><h2>Take the design into practice</h2><a href="#visual-reference">Inspect the contract, LAB and independent SIM below</a> · <a href="{e(lesson['next'])}">Continue to the next application →</a></section>
<details class="vl-reference" id="visual-reference" open><summary>Detailed reference · contracts, examples, LAB and SIM</summary>{reference}</details>'''
        doc=doc[:match.start(1)]+new+doc[match.end(1):]
        doc=doc.replace('<body','<body class="visual-lesson"',1) if '<body>' in doc else re.sub(r'<body class="([^"]*)"',r'<body class="\1 visual-lesson"',doc,count=1)
        prefix='../'*rel.count('/')
        doc=doc.replace('</head>',f'<link rel="stylesheet" href="{prefix}assets/visual-walkthrough.css"></head>')
        doc=doc.replace('</body>',f'<script defer src="{prefix}assets/visual-walkthrough-data.js"></script><script defer src="{prefix}assets/visual-walkthrough.js"></script></body>')
        written[rel]=doc
    return lessons

def asset(lessons):
    return 'window.CCS_VISUAL_STORIES = '+json.dumps(lessons,ensure_ascii=False).replace('</','<\\/')+';\n'
