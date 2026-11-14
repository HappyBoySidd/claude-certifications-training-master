"""B-113: source-mapped decision teaching across the whole CCAR-F learning arc."""
import hashlib,html,json,re,posixpath
from pathlib import Path
from layered_teaching import PLAIN
ROOT='02-Lessons/02-CCAR-F-Architect-Foundations/'
def norm(code):
    code=re.sub(r'%%\{.*?\}%%\s*','',html.unescape(code),flags=re.S)
    return '\n'.join(x.strip() for x in code.strip().splitlines() if not re.match(r'\s*click\s',x))
def digest(code):return hashlib.sha256(norm(code).encode()).hexdigest()[:20]
def prepare(site,variants,repo):
    pages=json.loads((site.src/ROOT/'page-teaching-map.json').read_text())['pages']
    entries=json.loads((site.src/ROOT/'diagram-teaching-map.json').read_text())['entries']
    assert len(pages)==len({p['route']for p in pages})==103
    plain=json.loads((site.src/ROOT/'question-plain-context.json').read_text())
    patterns=json.loads((site.src/ROOT/'objective-learning-patterns.json').read_text())['objectives']
    assert len(patterns)==30,'Expected contextual patterns for all30objectives'
    for objective,pattern in patterns.items():
        assert pattern['capability']['fixture_scope']=='base-question'
        assert pattern['companion']['fixture_scope']=='companion-example'
        applications=pattern['course_applications']
        assert len(applications)==11 and sorted(a['course_index']for a in applications)==list(range(11)),(objective,'Incomplete course pattern map')
        for a in applications:
            assert a['disposition']in {'applied','supporting','not-needed'}
            assert a['fixture_scope']in {'base-question','companion-example','extension'}
            assert all(a.get(k)for k in ['title','decision','why','how','evidence','reason'])
            if a['disposition']!='applied':assert a['fixture_scope']=='extension'
        assert all(pattern['capability'].get(k)for k in ['concept','what','why','setup_question'])
        assert all(pattern['companion'].get(k)for k in ['what','why','how','evidence','artifact_label','artifact'])
        assert pattern['recall_prompt']
    questions={q['id']:q for q in json.loads((Path(repo)/'practice/question-bank.json').read_text())['questions']}
    valid={v['variant_id']:v for v in variants};diagrams={};byhash={}
    for n,d in enumerate(entries):
        raw=site.text(d['source']);blocks=re.findall(r'```mermaid\s*\n(.*?)```',raw,re.S)
        assert d['index']<len(blocks),(d['source'],d['index'],'Missing diagram')
        assert all(v in valid and valid[v]['primary_objective']in d['objective_ids']for v in d['variant_ids'])
        assert d['technical_prompt'] and d['plain_prompt'] and d['reason']
        key='diagram-'+str(n+1);record={**d,'key':key,'code_hash':digest(blocks[d['index']])};diagrams[key]=record;byhash.setdefault(record['code_hash'],[]).append(record)
    expected={(s,i)for s in {d['source']for d in entries}for i,_ in enumerate(re.findall(r'```mermaid\s*\n(.*?)```',site.text(s),re.S))}
    assert expected=={(d['source'],d['index'])for d in entries},'Incomplete authored diagram map'
    units={}
    atlas=site.text(ROOT+'decision-atlas.md')
    for v in variants:
        assert v['primary_objective']not in units,'Expected one reviewed variant per objective'
        qs=[questions[q]for q in v['question_ids']];assert len(qs)==2
        for q in qs:assert q['exam']=='CCAR-F' and set(q['answer'])<=set(q['options'])
        # Use the actual companion episode drawing, not a broad atlas routing hint.
        source=ROOT+v['canonical_source'];raw=site.text(source)
        episode=re.search(r'<!-- layered-episode:'+re.escape(v['variant_id'])+r':start -->(.*?)<!-- layered-episode:'+re.escape(v['variant_id'])+r':end -->',raw,re.S)
        charts=re.findall(r'```mermaid\s*\n(.*?)```',episode.group(1),re.S)if episode else []
        assert charts,(v['variant_id'],'Missing companion episode drawing')
        graph=charts[0];candidates=byhash.get(digest(graph),[])
        matched=next((d for d in candidates if d['source']==source and v['variant_id']in d['variant_ids']),None)
        assert matched,(v['variant_id'],'Companion diagram not independently mapped')
        assert all(plain[v['primary_objective']].get(k)for k in ['base','transfer'])
        pattern=patterns[v['primary_objective']]
        assert pattern['capability']['setup_question']==plain[v['primary_objective']]['base']
        assert pattern['companion']['what']==v['base_case'] and pattern['companion']['why']==v['failure']
        assert pattern['companion']['artifact']==v['mechanism_artifact']
        for a in pattern['course_applications']:
            if a['fixture_scope']=='base-question':
                assert a['how']==' '.join(qs[0]['options'][key]for key in qs[0]['answer'])
                assert a['evidence']==qs[0]['rationale']
            elif a['fixture_scope']=='companion-example':
                assert a['decision']=='Companion example: '+v['base_case']
                assert a['how']==pattern['companion']['how'] and a['evidence']==pattern['companion']['evidence']
        units[v['primary_objective']]={**v,'learning_patterns':pattern,'question_plain':plain[v['primary_objective']],'questions':qs,'plain_problem':PLAIN[v['variant_id']][0],'plain_repair':PLAIN[v['variant_id']][1],'graph':graph,'graph_key':matched['key']if matched else None}
    assert len(units)==30 and set(patterns)==set(units)
    for p in pages:assert set(p['objectives'])<=set(units)
    return {'pages':{p['route']:p for p in pages},'units':units,'diagrams':diagrams},byhash

def enhance(site,written,variants,repo):
    data,byhash=prepare(site,variants,repo);manifest=[]
    expected={r for r in written if r.startswith(('lessons/ccar-f/','simulations/ccar-f/'))or r=='exams/ccar-f.html'or(r.startswith('labs/')and'CCAR-F'in r)}|{'practice/index.html'}
    assert expected==set(data['pages']),('Reconcile full CCAR-F page map',expected^set(data['pages']))
    utility={'lessons/ccar-f/objectives/progress.html','lessons/ccar-f/objectives/practice-coverage.html'}
    for route,p in data['pages'].items():
        if route=='practice/index.html':manifest.append({'route':route,'disposition':'post-answer repair link only; timed items unchanged'});continue
        doc=written[route];prefix='../'*route.count('/');found=[]
        def diagram(m):
            code=html.unescape(m.group(2));candidates=byhash.get(digest(code),[])
            own=[d for d in candidates if d['route']==route]
            preferred=own or [d for d in candidates if set(d['objective_ids'])&set(p['objectives'])] or candidates
            if not preferred:raise ValueError('Unmapped rendered diagram: '+route+' '+digest(code)+' '+repr(code[:700]))
            record=preferred[0];found.append({'key':record['key'],'source':record['source'],'source_index':record['index'],'reused':record['route']!=route})
            return m.group(1)+(' id="cc-chart-'+str(len(found))+'"'if not re.search(r'\bid=',m.group(1))else'')+' data-teaching-key="'+record['key']+'">'+m.group(2)+'</pre>'
        doc=re.sub(r'(<pre\b[^>]*class="mermaid"[^>]*?)>(.*?)</pre>',diagram,doc,flags=re.S)
        nav='<nav class="cc-route" aria-label="Connected architecture learning"><a href="'+prefix+'exams/ccar-f.html#decision-workbench">Learning home and decision coach</a> · <a href="'+prefix+'lessons/ccar-f/objectives/index.html">Objective map</a> · <a href="'+prefix+'lessons/ccar-f/architecture-studio/index.html">Application stories</a></nav>'
        if 'data-visual-story=' in doc:
            doc=doc.replace('<section class="vl-player"',nav.replace('<nav ','<nav id="decision-workbench" ',1)+'<section class="vl-player"',1);disposition='Existing40stage/72phase boundary player retained; shared diagram coaching added to retained reference charts'
        elif route in utility:
            doc=doc.replace('</h1>','</h1>'+nav.replace('<nav ','<nav id="decision-workbench" ',1)+'<p class="cc-context-note">This is a progress or coverage utility. Recorded activity is not mastery; use the linked objective to study and practise.</p>',1);disposition='Context-only utility; no invented assessment'
        else:
            gate='<button type="button" class="cc-attempt-gate">I have attempted the exercise — open a separate worked example</button>'if p['help_policy']=='after-commitment'else''
            setup='Reading and paper reasoning need no setup. Runnable exercises retain their own prerequisites below.'if p['family']=='lab'else'No installation or API key is required for this reading and decision coach.'
            block='<details class="cc-course" id="decision-workbench" data-course-route="'+html.escape(route)+'"'+(' open'if p['family']=='entry-and-curriculum'else'')+'><summary>Learn, decide and inspect a worked architecture example here</summary><p>'+html.escape(p['intent'])+'</p><p>'+setup+'</p>'+gate+'<div class="cc-mount"'+(' hidden'if gate else'')+'></div><noscript><p><a href="'+prefix+'lessons/ccar-f/objectives/index.html">Read the full objective lessons and their diagrams</a></p></noscript></details>'
            entrance = ''
            if route == 'exams/ccar-f.html':
                # Put the primary routes before optional coaching, especially on phones.
                lead = re.search(r'<nav aria-label="Your next CCAR-F study action".*?</nav>\s*<p><b>Suggested next action:</b>.*?</p>', doc, flags=re.S)
                if lead:
                    entrance = lead.group(0)
                    doc = doc[:lead.start()] + doc[lead.end():]
            doc=doc.replace('</h1>','</h1>'+entrance+nav+block,1);disposition='Attempt-first related worked example'if gate else'In-page staged decision coach'
        includes='<link rel="stylesheet" href="'+prefix+'assets/course-coach.css"><script defer src="'+prefix+'assets/course-coach-data.js"></script><script defer src="'+prefix+'assets/course-coach.js"></script>'
        if 'assets/technical-bridges.js'not in doc:includes+='<link rel="stylesheet" href="'+prefix+'assets/technical-bridges.css"><script defer src="'+prefix+'assets/technical-bridges-data.js"></script><script defer src="'+prefix+'assets/technical-bridges.js"></script>'
        if 'assets/viewer.js'not in doc:includes+='<link rel="stylesheet" href="'+prefix+'assets/viewer.css"><script defer src="'+prefix+'assets/vendor/mermaid-12.1.0.min.js"></script><script defer src="'+prefix+'assets/viewer.js"></script>'
        written[route]=doc.replace('</head>',includes+'</head>');manifest.append({'route':route,'family':p['family'],'mode':p['mode'],'policy':p['help_policy'],'disposition':disposition,'rendered_diagrams':found})
    return data,manifest

def asset(data):
    public={**data,'pages':{r:{k:v for k,v in p.items()if k!='sources'}for r,p in data['pages'].items()},'diagrams':{k:{f:v for f,v in d.items()if f!='source'}for k,d in data['diagrams'].items()}}
    return 'window.CCS_COURSE_COACH = '+json.dumps(public,ensure_ascii=False).replace('</','<\\/')+';\n'
