"""B-71: source-derived error inventory and honest what-if self-report.

Objective tags come from explicit Guide tags in the authored answer. They remain
author-proposed, not independently reviewed diagnostics or mastery claims.
"""
import html
import json
import re
import posixpath

OUT_REL='lessons/ccar-f/scenario-walkthroughs/signals-and-errors.html'
ROOT='02-Lessons/02-CCAR-F-Architect-Foundations/'


def inventory(site):
    scenarios=[]
    for source,destination,meta in site.of('extra','ccar-f'):
        if meta.get('sub')!='scenario-walkthroughs' or not re.search(r'/WT-\d',source):continue
        raw=site.text(source);number=re.search(r'/WT-(\d+)',source).group(1)
        title=re.search(r'^# (.+)',raw,re.M).group(1)
        errors=[];step='Opening';lines=raw.splitlines();i=0
        while i<len(lines):
            line=lines[i]
            if line.startswith('### Step '):step=line[4:]
            if line.startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|-]+\|$',lines[i+1]):
                headers=[c.strip() for c in line.strip('|').split('|')]
                if len(headers)==3 and any('signal' in c.lower() for c in headers):
                    i+=2
                    while i<len(lines) and lines[i].startswith('|'):
                        cells=[c.strip() for c in lines[i].strip('|').split('|')]
                        if len(cells)==3:errors.append({'step':step,'headers':headers,'cells':cells})
                        i+=1
                    continue
            i+=1
        region=raw.split('## Run it for real: 10 what-if questions',1)[-1].split('## In real life',1)[0]
        questions=[]
        for m in re.finditer(r'<details><summary>(.*?)</summary>(.*?)</details>',region,re.S):
            stem,answer=m.groups();idx=re.match(r'<b>(\d+)\.',stem)
            if not idx:continue
            n=int(idx.group(1));tags=sorted({t for group in re.findall(r'\[Guide (\d\.\d(?:,\s*\d\.\d)*)\]',answer) for t in re.split(r',\s*',group)})
            questions.append({'id':f'WT-{number}-whatif-{n:02}','number':n,'stem':stem,'answer':answer.strip(),'objectives':tags,'mapping_status':'author-proposed from explicit source Guide tags' if tags else 'uncertain: no explicit source Guide tag; choose a task for repair'})
        if len(questions)!=10:site.problems.append(source+': expected10 source what-ifs, found '+str(len(questions)))
        scenarios.append({'source':source,'destination':destination,'number':number,'title':title,'errors':errors,'questions':questions})
    return sorted(scenarios,key=lambda x:x['number'])


def selfcheck(question,outrel):
    tags=question['objectives']; links=[]
    for task in tags:
        dest=f'lessons/ccar-f/objectives/objective-{task}.html'
        links.append(f'<a href="{posixpath.relpath(dest,posixpath.dirname(outrel))}">Objective {task}</a>')
    repair=' · '.join(links) or '<a href="'+posixpath.relpath('lessons/ccar-f/objectives/index.html',posixpath.dirname(outrel))+'">Choose the task that needs repair</a>'
    return ('<div class="scenario-selfcheck"><label><input type="checkbox" data-scenario-miss="'+question['id']+'"> I missed this — self-report in this browser</label>'
            '<p>Repair tags: '+repair+'. <small>'+html.escape(question['mapping_status'])+'. These tags do not certify full skill coverage.</small></p></div>')


def enhance(site,body,outrel,scenarios):
    scenario=next((s for s in scenarios if s['destination']==outrel),None)
    if not scenario:return body
    bynum={q['number']:q for q in scenario['questions']};seen=set()
    def add(m):
        match=re.match(r'<details><summary><(?:b|strong)>(\d+)\.',m.group(0))
        if not match:return m.group(0)
        n=int(match.group(1))
        if n not in bynum or n in seen:return m.group(0)
        seen.add(n);return m.group(0).replace('<details>', '<details id="'+bynum[n]['id'].lower()+'">', 1)+selfcheck(bynum[n],outrel)
    body=re.sub(r'<details><summary><(?:b|strong)>\d+\..*?</details>',add,body,flags=re.S)
    link=posixpath.relpath(OUT_REL,posixpath.dirname(outrel))+'#scenario-'+scenario['number']
    body=body.replace('</h1>','</h1><p><a href="'+link+'">Signals, errors and missed what-ifs for this scenario</a></p>',1)
    return body


def build(site,scenarios,render_fragment=None,render_inline_fragment=None):
    render_md = render_fragment or (lambda source, fragment: '<p>'+html.escape(fragment)+'</p>')
    out='<article class="prose"><h1>Signals and errors by scenario</h1><p>Generated from the six walkthroughs’ actual error tables and 60 original what-ifs. Error rows retain their source headers. Check “I missed this” to record a self-reported repair need; it is not a graded attempt or evidence of mastery. Existing progress is preserved in a separate storage namespace.</p><p>Objective tags below are author-proposed from explicit source Guide references, not independently reviewed diagnostic mappings. Untagged items remain uncertain and offer task selection.</p><p><a href="index.html">Return to scenario walkthroughs</a> · <a href="../objectives/index.html">Choose an objective</a></p><nav aria-label="Scenarios">'
    out+=' · '.join('<a href="#scenario-'+s['number']+'">Scenario '+s['number']+'</a>' for s in scenarios)+'</nav>'
    for s in scenarios:
        rel=posixpath.relpath(s['destination'],posixpath.dirname(OUT_REL))
        out+='<section id="scenario-'+s['number']+'"><h2>'+html.escape(s['title'])+'</h2><p><a href="'+rel+'">Open the source walkthrough</a></p>'
        last=None
        for row in s['errors']:
            if row['step']!=last:
                if last is not None:out+='</tbody></table></div>'
                last=row['step'];out+='<h3>'+html.escape(last)+'</h3><div class="tbl"><table><thead><tr>'+''.join('<th scope="col">'+html.escape(h)+'</th>' for h in row['headers'])+'</tr></thead><tbody>'
            out+='<tr>'+''.join('<td>'+render_md(s['source'], c)+'</td>' for c in row['cells'])+'</tr>'
        if last is not None:out+='</tbody></table></div>'
        out+='<h3>Closed-answer what-ifs and repair</h3>'
        for q in s['questions']:
            stem=re.sub(r'</?b>','',q['stem']);stem=re.sub(r'</?code>', '`', stem)
            stem=render_inline_fragment(s['source'], stem) if render_inline_fragment else html.escape(stem)
            answer=render_fragment(s['source'],q['answer']) if render_fragment else '<p>'+html.escape(q['answer'])+'</p>'
            out+='<details class="scenario-whatif"><summary>'+stem+'</summary>'+answer+'<p>Read the exact source answer after committing to your choice: <a href="'+rel+'#'+q['id'].lower()+'">source what-if '+str(q['number'])+'</a>.</p></details>'+selfcheck(q,OUT_REL)
        out+='</section>'
    out+='<h2>Manage these self-checks</h2><p><button id="scenario-miss-export" type="button">Export missed what-ifs</button> <button id="scenario-miss-reset" type="button">Reset only these self-checks</button></p><p id="scenario-miss-status" role="status">Stored only in this browser.</p></article>'
    return out


def scripts(body,outrel):
    if 'data-scenario-miss=' not in body:return body
    root='../'*outrel.count('/')
    return body.replace('</head>','<script defer src="'+root+'assets/scenario-signals.js"></script></head>')
