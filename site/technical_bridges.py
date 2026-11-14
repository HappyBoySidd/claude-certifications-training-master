"""Paired plain/technical teaching. Source artifacts stay classified; assessments stay separate."""
import html,json,re
from pathlib import Path
ROOT='02-Lessons/02-CCAR-F-Architect-Foundations/'
ATLAS='lessons/ccar-f/technical-bridges.html'
FIELDS=('plain','terms','example_label','example','read_it','not_equivalent','source_url')
def load(site):
    data=json.loads((site.src/ROOT/'technical-objective-bridges.json').read_text())['objectives']
    expected={f'{d}.{n}' for d,count in [(1,7),(2,5),(3,6),(4,6),(5,6)] for n in range(1,count+1)}
    assert set(data)==expected,'Incomplete technical objective bridge coverage'
    for key,b in data.items():
        assert all(b.get(f) for f in FIELDS),(key,'Empty technical bridge field')
        assert b['source_url'].startswith(('https://platform.claude.com/','https://code.claude.com/','https://modelcontextprotocol.io/','https://www.anthropic.com/','https://anthropic.com/')),(key,'Non-primary bridge source')
    return data

def card(b,key='',context='',open_example=True):
    e=html.escape
    terms=' '.join('<code>'+e(t)+'</code>' for t in b['terms'])
    urls=list(dict.fromkeys([b['source_url']]+b.get('source_urls',[])))
    sources=' · '.join('<a href="'+e(u,quote=True)+'">'+('Official mechanism reference' if i==0 else 'Additional official reference')+'</a>' for i,u in enumerate(urls))
    example='<p class="tb-artifact-label">'+e(b['example_label'])+'</p><pre tabindex="0" aria-label="Technical example"><code>'+e(b['example'])+'</code></pre><p><strong>Read it as:</strong> '+e(b['read_it'])+'</p>'
    example+=''.join('<details><summary>'+e(x['title'])+'</summary><p class="tb-artifact-label">'+e(x['label'])+'</p><pre tabindex="0"><code>'+e(x['example'])+'</code></pre><p>'+e(x['read_it'])+'</p></details>' for x in b.get('extra_examples',[]))
    if not open_example:example='<details><summary>Inspect the technical example</summary>'+example+'</details>'
    return '<div class="tb-pair" data-objective="'+e(key)+'"><div class="tb-plain"><h3>In everyday language</h3>'+('<p class="tb-context">'+e(context)+'</p>' if context else '')+'<p>'+e(b['plain'])+'</p><p><strong>Does not establish:</strong> '+e(b['not_equivalent'])+'</p></div><div class="tb-precise"><h3>In technical terms</h3><p class="tb-terms">'+terms+'</p>'+example+'<p class="tb-source">'+sources+'</p></div></div>'

def enhance(site,written,lessons):
    data=load(site)
    scenario=json.loads((site.src/ROOT/'technical-scenario-bridges.json').read_text())['lessons']
    components=json.loads((site.src/ROOT/'technical-component-bridges.json').read_text())['lessons']
    for slug,lesson in lessons.items():
        assert len(scenario[slug])==len(lesson['stages']),(slug,'Missing stage technical bridge')
        assert set(components[slug])==set(lesson['nodes']),(slug,'Missing component technical bridge')
        for nid,c in components[slug].items():
            assert c.get('objective_id') in data and all(c.get(f) for f in ['short','terms','meaning']),(slug,nid,'Incomplete component bridge')
            assert len(c['short'])<=30,(slug,nid,'Technical subtitle too long')
        lesson['technicalStages']=scenario[slug];lesson['technicalNodes']=components[slug]
        for i,stage in enumerate(lesson['stages']):
            entry=scenario[slug][i];assert entry['objective_id'] in data
            assert set(entry)==({'objective_id','setup','repair'} if stage.get('repair') else {'objective_id','setup'}),(slug,i,'Phase mismatch')
            for ph in ['setup']+(['repair'] if stage.get('repair') else []):
                assert all(entry[ph].get(f) for f in FIELDS),(slug,i,ph,'Empty phase bridge field')
    placements=json.loads((site.src/ROOT/'technical-bridge-placements.json').read_text())['pages']
    registered={route for src,route in site.pages.items() if route in written and (route.startswith(('lessons/ccar-f/','simulations/ccar-f/')) or route=='exams/ccar-f.html' or (route.startswith('labs/') and 'CCAR-F' in route))}
    assert registered=={p['route'] for p in placements},('Update technical bridge placement inventory for added/removed routes',registered^{p['route'] for p in placements})
    manifest=[]
    for p in placements:
        route=p['route'];assert route in written,('Missing CCAR-F bridge destination',route)
        root='../'*route.count('/')
        doc=re.sub(r'&lt;!--\s*layered-episode:.*?--&gt;','',written[route],flags=re.S)
        ids=[i for i in p['page_objective_links'] if i in data]
        m=re.search(r'objective-(\d\.\d)\.html$',route)
        if m:ids=[m.group(1)]
        if p['family']=='domain-lesson':
            domain=re.search(r'/L0([1-5])-',route)
            if domain:ids=[i for i in data if i.startswith(domain.group(1)+'.')]
        if not ids or p['family'] in {'entry-and-curriculum','orientation','navigation'}:ids=list(data)
        links=' · '.join('<a href="'+root+ATLAS+'#technical-'+i+'">'+i+'</a>' for i in ids)
        nav='<nav class="tb-route" aria-label="Plain language to technical learning"><strong>Plain ↔ technical:</strong> <a href="'+root+ATLAS+'">Mechanism examples and terminology</a> · '+links+'</nav>'
        if 'class="vl-hero"' in doc:
            doc=doc.replace('<p class="vl-scope">','<section class="tb-stage" id="technical-current-stage" aria-label="Current stage plain and technical bridge"></section><p class="vl-scope">',1)
            doc=doc.replace('<section class="vl-player"',nav+'<section class="vl-player"',1)
        else:doc=doc.replace('</h1>','</h1>'+nav,1)
        sections={s['anchor']:s for s in p['sections'] if s['mechanism_candidate'] and s['role']!='assessment/review'}
        inserted=[]; rendered={}
        def add_section(match):
            anchor=match.group(2);s=sections.get(anchor)
            if not s or re.search(r'learn the decision in context|^layer [0-9]|change one (?:constraint|condition)',s['title'],re.I):return match.group(0)
            section_ids=[i for i in s['objective_ids'] if i in ids] or ids
            # This is explicitly related objective help, not a fabricated artifact for the current scene.
            selected=section_ids[0]
            if selected in rendered:
                inserted.append({'anchor':anchor,'objectives':section_ids,'mapping_status':s['mapping_status'],'kind':'local-related-reference','target':rendered[selected]})
                return match.group(0)+'<p class="tb-section-link"><a href="#'+rendered[selected]+'">Related technical reference · '+html.escape(' / '.join(data[selected]['terms'][:2]))+'</a></p>'
            local_id='tb-mechanism-'+selected.replace('.','-');rendered[selected]=local_id
            choices=''.join('<option value="'+i+'">'+i+' · '+html.escape(' / '.join(data[i]['terms'][:2]))+'</option>' for i in section_ids)
            block='<details class="tb-inline" id="'+local_id+'" data-technical-bridge="'+selected+'"><summary>Plain ↔ technical · '+html.escape(' / '.join(data[selected]['terms'][:2]))+'</summary><p>Related objective example. Keep the current case\'s facts and chosen answer separate. For a decision, choose before opening this study help.</p><label>Mechanism <select class="tb-select">'+choices+'</select></label><div class="tb-slot">'+card(data[selected],selected,open_example=False)+'</div></details>'
            inserted.append({'anchor':anchor,'objectives':section_ids,'mapping_status':s['mapping_status'],'kind':'related-objective-help'})
            return match.group(0)+block
        # Keep cards out of the live practice application and graded bank; source study help is explicit disclosure.
        doc=re.sub(r'(<h[2]\b[^>]*\bid="([^"]+)"[^>]*>.*?</h[2]>)',add_section,doc,flags=re.S)
        doc=doc.replace('</head>','<link rel="stylesheet" href="'+root+'assets/technical-bridges.css"><script defer src="'+root+'assets/technical-bridges-data.js"></script><script defer src="'+root+'assets/technical-bridges.js"></script></head>')
        written[route]=doc
        manifest.append({'route':route,'family':p['family'],'objectives':ids,'sections':inserted,'section_semantics':'Source-mapped related objective help, not independent validation of every knowledge/skill bullet'})
    # A durable direct destination exists for every technical term and objective, even on navigation pages.
    body='<nav class="crumbs"><a href="../../exams/ccar-f.html">Architect Foundations</a> / Plain ↔ technical</nav><h1>Connect the explanation to the technical mechanism</h1><p>Keep the ordinary meaning and exact terms together. These are learning examples, not exam questions. API fragments omit surrounding request fields; application pseudocode is labeled separately. No setup or API key is required to read them.</p>'
    body+='<nav class="tb-route" aria-label="All technical objectives">'+' · '.join('<a href="#technical-'+i+'">'+i+'</a>' for i in data)+'</nav>'
    for i,b in data.items():body+='<section class="tb-atlas" id="technical-'+i+'"><h2>Objective '+i+' · '+html.escape(' / '.join(b['terms'][:2]))+'</h2>'+card(b,i,open_example=i=='1.1')+'<p><a href="objectives/objective-'+i+'.html">Continue the full objective lesson →</a> · <a href="../../exams/ccar-f.html">Return to learning home</a></p></section>'
    # Reuse an existing site shell; retain navigation and footer, replace only main content.
    shell=written['lessons/ccar-f/index.html']
    shell=re.sub(r'<title>.*?</title>','<title>Plain ↔ technical mechanism guide · Claude Certifications</title>',shell,count=1,flags=re.S)
    # Atlas is one directory shallower than objective index.
    shell=re.sub(r'(<main\b[^>]*>).*?(</main>)',lambda m:m.group(1)+body+m.group(2),shell,count=1,flags=re.S)
    written[ATLAS]=shell
    return {'objectives':data,'pages':manifest,'atlas':ATLAS}

def asset(data):return 'window.CCS_TECHNICAL_BRIDGES = '+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';\n'
