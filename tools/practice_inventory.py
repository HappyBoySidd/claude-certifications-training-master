#!/usr/bin/env python3
"""Read-only inventory of distinct practice populations using the shipped runtime pool().
Never assembles a bank, changes keys or reads learner storage.
"""
import argparse,ast,collections,datetime,hashlib,json,re,subprocess
from pathlib import Path
REPO=Path(__file__).resolve().parent.parent

def load(p):return json.loads(p.read_text())
def questions(d):return d if isinstance(d,list)else d['questions']
def run(src,repo=REPO):
    canonical=load(src/'05-Practice-Tool/build/questions.json');published=load(repo/'practice/question-bank.json');legacy=load(repo/'practice/legacy-question-bank.json')
    ca={q['id']:q for q in questions(canonical)};pub={q['id']:q for q in questions(published)};le={q['id']:q for q in questions(legacy)}
    assert len(ca)==len(questions(canonical))and len(pub)==len(questions(published)),'Duplicate IDs'
    originals={q['id']for q in questions(load(repo/'practice/project-authored-originals.json'))}
    variants=load(repo/'assessment/variant-review.json');variant_ids=set(variants.get('approved_ids',[]))
    module=ast.parse((repo/'tools/build_practice.py').read_text());exclude={}
    for n in module.body:
        if isinstance(n,ast.AnnAssign)and isinstance(n.target,ast.Name)and n.target.id=='EXCLUDE':exclude=ast.literal_eval(n.value)
    # Evaluate the exact trusted shipped pool function; do not recreate its eligibility rules.
    template=(repo/'practice/src/template.html').read_text();pool=template[template.index('function pool('):template.index('function warmups(')]
    node="""const fs=require('fs'),data=JSON.parse(fs.readFileSync(process.argv[1],'utf8')),source=fs.readFileSync(process.argv[2],'utf8');const f=source.slice(source.indexOf('function pool('),source.indexOf('function warmups('));const compute=new Function('DATA',f+';return Object.fromEntries(Object.keys(DATA.exams).map(exam=>[exam,{general:pool(exam,[1,2,3,4]).map(q=>q.id),withWarmups:pool(exam,[1,2,3,4],true).map(q=>q.id),mockCandidates:pool(exam,[1,2,3,4]).filter(q=>DATA.reviewMap?.[q.id]?.disposition!==\"caveated\").map(q=>q.id)}]));');process.stdout.write(JSON.stringify(compute(data)));"""
    runtime=json.loads(subprocess.check_output(['node','-e',node,str(repo/'practice/question-bank.json'),str(repo/'practice/src/template.html')],text=True))
    ledger=[]
    for ident in sorted(ca.keys()|pub.keys()):
        a,b=ca.get(ident),pub.get(ident);q=b or a
        if a and b:reason='Present in canonical local bank and released assembly; released record/answer identity is preserved.'
        elif ident in exclude:reason='Explicit publisher EXCLUDE: '+exclude[ident]
        elif a and q.get('origin')=='project-authored'and q.get('exam')!='CCAR-F':reason='Canonical-only other-exam original; publisher export() intentionally selects approved CCAR-F originals. Not automatically admitted by this inventory.'
        elif a and q.get('origin')=='community-licensed'and not q.get('source','').startswith(('Anthropic official exam guide','Amey Thakur CLAUDE-CERTIFICATIONS repo')):reason='Canonical-only additional licensed source outside this publisher ALLOWED_SOURCES intake; retain its source/license register; no silent migration.'
        elif b and ident in variant_ids:reason='Published-only reviewed contrastive item from assessment/ccarf-variant-items.json; separate approved source beyond the canonical local bank.'
        else:raise AssertionError('Unexplained bank difference: '+ident)
        assembly=[]
        if ident in le:assembly.append('legacy-question-bank.json; stable released record')
        if ident in originals:assembly.append('project-authored-originals.json; append if ID absent')
        if ident in variant_ids:assembly.append('approved variant; append if ID absent and review hash matches')
        rules=[]
        if b:
            if b.get('origin_tier')not in [1,2,3,4]:rules.append('origin tier outside all-tier selection')
            if b.get('warmup_only'):rules.append('warmup_only excluded from general pool')
            if b.get('review_status')=='quarantined':rules.append('record quarantined')
            review=published.get('reviewMap',{}).get(ident,{})
            if review.get('disposition')=='quarantined':rules.append('review map quarantined')
            if b.get('stage')=='delayed-retry':rules.append('delayed retry: separate transfer workflow')
            if review.get('disposition')=='caveated':rules.append('caveated: excluded from general mock candidates')
        ledger.append({'id':ident,'exam':q['exam'],'canonical':bool(a),'published':bool(b),'reason':reason,'assembly_sources':assembly,'runtime_exclusions':rules,'shared_record_identical':a==b if a and b else None})
    counts={}
    for exam in sorted(set(q['exam']for q in list(ca.values())+list(pub.values()))):
        x=runtime[exam];counts[exam]={'canonical_local':sum(q['exam']==exam for q in ca.values()),'published_records':sum(q['exam']==exam for q in pub.values()),'general_all_tiers':len(x['general']),'with_warmups':len(x['withWarmups']),'mock_candidates_before_blueprint_and_freshness':len(x['mockCandidates']),'published_only':sum(r['exam']==exam and r['published']and not r['canonical']for r in ledger),'canonical_only':sum(r['exam']==exam and r['canonical']and not r['published']for r in ledger)}
    for exam,v in runtime.items():
        expected={r['id']for r in ledger if r['exam']==exam and r['published']and not any(t!='caveated: excluded from general mock candidates'for t in r['runtime_exclusions'])}
        assert expected==set(v['general']),('Runtime rule reconciliation failed',exam)
    return {'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'populations':'Record inventory, not a score, fresh-item count, calibrated mock or all-skill assessment claim. No browser progress read. Tier/freshness/session choices can further reduce runtime candidates.','runtime_pool_sha256':hashlib.sha256(pool.encode()).hexdigest(),'counts':counts,'totals':{'canonical':len(ca),'published':len(pub),'shared':len(ca.keys()&pub.keys()),'canonical_only':len(ca.keys()-pub.keys()),'published_only':len(pub.keys()-ca.keys())},'runtime':runtime,'records':ledger}

def readme_section(d):
    text='<!-- generated-populations:start -->\nThe published bank, canonical local bank and runtime-eligible pool serve different purposes. Counts below are generated by `tools/practice_inventory.py`, using the shipped `pool()` rules. They are not fresh-question counts or readiness scores.\n\n| Exam | Published records | General all-tier pool | Mock candidates before blueprint/freshness |\n|---|---:|---:|---:|\n'
    for e,c in d['counts'].items():text+=f"| {e} | {c['published_records']} | {c['general_all_tiers']} | {c['mock_candidates_before_blueprint_and_freshness']} |\n"
    return text+'\n[Full population reconciliation](INVENTORY.md) explains the canonical/local and released record differences. Its JSON ledger records each ID and exclusion reason without question text. Regenerate after bank or eligibility-rule changes; existing answer keys and progress are preserved.\n<!-- generated-populations:end -->'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--src',type=Path,required=True);ap.add_argument('--repo',type=Path,default=REPO);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--update-readme',action='store_true');ap.add_argument('--check-readme',action='store_true');a=ap.parse_args();d=run(a.src,a.repo);a.out.mkdir(parents=True,exist_ok=True);(a.out/'PRACTICE-INVENTORY.json').write_text(json.dumps(d,indent=2)+'\n')
    text='# Generated practice population reconciliation\n\n'+d['populations']+'\n\nGenerated from current files and the exact shipped `pool()` function. No bank or learner-state mutation.\n\n| Exam | Canonical local | Published records | General all-tier pool | Mock candidates before sampling/freshness |\n|---|---:|---:|---:|---:|\n'
    for e,c in d['counts'].items():text+=f"| {e} | {c['canonical_local']} | {c['published_records']} | {c['general_all_tiers']} | {c['mock_candidates_before_blueprint_and_freshness']} |\n"
    t=d['totals'];text+=f"\nCanonical-only: {t['canonical_only']}; published-only: {t['published_only']}; shared IDs: {t['shared']}. The JSON ledger explains every ID difference and runtime exclusion. Published-only reviewed variants are an independent source; other-exam originals/additional sources are not silently admitted. This report does not assess freshness/mistake UI correctness or integrate the offline 20-question pilot (B-119 remains open).\n"
    (a.out/'PRACTICE-INVENTORY.md').write_text(text)
    readme=a.repo/'practice/README.md';old=readme.read_text();pattern=r'<!-- generated-populations:start -->.*?<!-- generated-populations:end -->';matched=re.search(pattern,old,re.S);assert matched,'Missing generated README markers'
    if a.update_readme:readme.write_text(re.sub(pattern,lambda _:readme_section(d),old,flags=re.S))
    if a.check_readme:assert re.search(pattern,readme.read_text(),re.S)[0]==readme_section(d),'Stale practice README inventory; regenerate with --update-readme'
    print(json.dumps(d['totals']))
if __name__=='__main__':main()
