"""Authored integrated architecture teaching overlays. Never infer semantic course coverage."""
import json,copy
from pathlib import Path
ROOT='02-Lessons/02-CCAR-F-Architect-Foundations/'
FILES=('application-teaching-a.json','application-teaching-b.json')
def apply(site,lessons):
    supplied={}
    for name in FILES:
        p=site.src/ROOT/name
        assert p.exists(),('Missing integrated overlay',name)
        if p.exists():
            records=json.loads(p.read_text())['lessons']
            assert not supplied.keys()&records.keys(),'Duplicate integrated app overlay'
            supplied.update(records)
    for slug,overlay in supplied.items():
        assert slug in lessons and slug!='as-03-grounded-assistant',slug
        lesson=lessons[slug]
        for n,override in enumerate(overlay.get('stageOverrides',[])):
            lesson['stages'][n].update(override.get('setup',{}))
            if override.get('repair'):
                assert 'repair'in lesson['stages'][n],(slug,n)
                lesson['stages'][n]['repair'].update(override['repair'])
        lesson.update({k:v for k,v in overlay.items()if k!='stageOverrides'})
    assert set(supplied)==set(lessons)-{'as-03-grounded-assistant'},'Incomplete application rollout'
    lessons['as-03-grounded-assistant']['teachingEdition']='integrated-v2'
    for slug,l in lessons.items():
        if l.get('teachingEdition')!='integrated-v2':continue
        assert len(l['fluencyLayers'])==len(l['stages']),(slug,'fluency count')
        assert len(l['courseConnections'])==11,(slug,'course denominator')
        assert sorted(r['course_index']for r in l['pathApplications'])==list(range(11)),slug
        for i,unit in enumerate(l['fluencyLayers']):
            assert unit['focus']and unit['integration']['what']and unit['integration']['why']and unit['integration']['setup'],(slug,i)
            if l['stages'][i].get('repair'):assert unit['integration']['repair']and unit['integration']['proof'],(slug,i)
            assert all(0<=n<11 for n in unit['courses'])
        for row in l['pathApplications']:
            assert all(row.get(k)for k in ['where','what','why','how','evidence','not_demonstrated','technical_artifact']),slug
        layout=l.get('layout')
        if layout:
            assert set(layout['nodes'])==set(l['nodes']),(slug,'layout node mismatch')
            edges={a+'>'+b for st in l['stages']for part in [st,st.get('repair',{})]for a,b,_ in part.get('edges',[])}
            assert edges<=set(layout['routes']),(slug,'layout edges missing',edges-set(layout['routes']))
    return lessons
