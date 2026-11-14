"""Shared at-point coaching for reference surfaces; existing bank data is read-only.

The same approved question IDs are reused for learning, never rescored or rewritten.
Source-specific pages keep their authored diagrams and deeper reference sections.
"""
import html
import json
import posixpath
import re
from pathlib import Path

ROOT = '02-Lessons/02-CCAR-F-Architect-Foundations/'
PLAIN = {
'FV-01': ('The assistant has stopped talking, but the payment might still be unfinished.', 'The payment receipt, not the assistant’s final message, tells you whether money moved.'),
'FV-02': ('A comparison looks finished even though one required topic has no evidence.', 'Keep a checklist of the requested topics. Ask for the missing evidence before calling the comparison complete.'),
'FV-03': ('A helper is asked to use information it has never received.', 'Send the actual question, allowed evidence and expected return fields. A helper cannot read another conversation just because you named it.'),
'FV-04': ('Someone approved one payment; the account or amount then changed.', 'Approval belongs to the particular action that was checked. The application must check the current action before it runs.'),
'FV-05': ('A check notices a problem only after the action has happened.', 'A check before the action can prevent it. A check afterward can detect it and start recovery, but cannot make the action never have happened.'),
'FV-06': ('The task may be a known sequence or an investigation whose next step depends on findings.', 'Use fixed steps when the path is known. Allow bounded exploration when new evidence determines the path; define when to stop.'),
'FV-07': ('A paused investigation restarts after files or access changed.', 'Remembering the old conversation does not make old facts or permissions current. Check what changed before continuing.'),
'FV-08': ('Two tools sound alike, and the assistant selects a write when it only needs to read.', 'Make each tool’s purpose and limits clear. The application must still reject an unsafe action.'),
'FV-09': ('A tool fails, but the next move depends on the kind of failure.', 'A temporary service failure, a bad request and an uncertain completed write need different recovery. Find out what happened before repeating an effect.'),
'FV-10': ('A specialist receives more capabilities than its job needs.', 'Give it the tools needed for that job. Requiring a tool call does not prove the arguments are sensible or the action permitted.'),
'FV-11': ('An external service connects, but the assistant still does not have the relevant document.', 'Connecting to a service and putting a permitted document into the assistant’s working information are separate steps.'),
'FV-12': ('A broad code replacement touches unrelated behavior.', 'Find and read the relevant code first. Make the smallest justified edit, then inspect what changed and test it.'),
'FV-13': ('A rule is placed where the intended team or project will not reliably receive it.', 'Put shared instructions at shared scope and personal preferences at personal scope. Resolve conflicts using the actual runtime’s rules.'),
'FV-14': ('A reusable task runs without an essential input.', 'A reusable instruction needs a clear input and result. If the input is missing, stop and say what is needed rather than inventing it.'),
'FV-15': ('A file moves and the rule intended for it no longer applies.', 'A path rule is like a label on a folder: check that the file’s current path still matches, and that unrelated paths do not.'),
'FV-16': ('A small-looking code change turns out to affect another system.', 'Reconsider the plan when the scope changes. A short request can still require investigation and coordination.'),
'FV-17': ('Repeating the same attempt produces the same wrong result.', 'Use the failure to test a different cause. Better feedback identifies the exact mismatch; repetition alone adds no evidence.'),
'FV-18': ('An unattended review produces no useful findings because the run failed.', 'A failed review must look failed to the pipeline. An empty report cannot quietly stand for a clean review.'),
'FV-19': ('A reviewer reports too many harmless issues.', 'Define what counts as a finding and what must be excluded. Test those rules on borderline examples.'),
'FV-20': ('All examples are easy successes, so the assistant mishandles missing or unusual facts.', 'Show representative edge cases and the expected response to missing evidence, not only more clean examples.'),
'FV-21': ('A returned record has the right fields and types but may contain the wrong fact.', 'Check both the record’s shape and its agreement with the source. A well-formed number can still be the wrong number.'),
'FV-22': ('A correction attempt keeps failing.', 'Return the exact failed check and relevant evidence. Limit repair attempts, then hand unresolved work to the right reviewer.'),
'FV-23': ('Many independent jobs can wait, but some do not finish successfully.', 'Track each job separately. Match results to IDs, preserve successes and recover only the items whose outcome requires it.'),
'FV-24': ('Two reviewers agree because both received the same misleading summary.', 'Agreement is weak proof if both reviewers share the same missing evidence. Give an independent check the original source or a different test.'),
'FV-25': ('A shorter conversation summary drops an important exception.', 'Preserve facts that change the decision, including restrictions and unresolved questions. A shorter story must not change the rules.'),
'FV-26': ('A case transfers to a person with a misleading action status.', 'Pass what is known, what was attempted, what really happened and what remains blocked. Proposed and completed are different states.'),
'FV-27': ('One helper succeeds and another required helper fails.', 'Keep the successful evidence but show the missing part. Recover the required evidence or limit the conclusion; do not fill the gap with a guess.'),
'FV-28': ('The code investigation grows until the important exception is lost.', 'Keep a small map of the files and facts needed for the change. Re-read current code when a lost detail could affect the decision.'),
'FV-29': ('A quality score looks good overall but hides risky mistakes or an overloaded review queue.', 'Test important groups separately and check what reviewers can actually handle. A changed input population can make yesterday’s threshold unreliable.'),
'FV-30': ('Two systems report different facts about the same subject.', 'Keep each fact attached to its source, time and scope. Do not erase a disagreement by joining records under one name.'),
}


def question(q):
    e = html.escape
    count = q.get('select_count', len(q.get('answer', [])) or 1)
    opts = q.get('options', {})
    if not isinstance(opts, dict):
        raise ValueError('Expected option map for '+q['id'])
    choices = ''.join('<li><b>'+e(k)+'.</b> '+e(v)+'</li>' for k,v in opts.items())
    return '<div class="layer-question" data-assessment-exposure="'+e(q['id'])+'"><p><small>Original exam-style practice · Choose '+str(count)+' · '+e(q['id'])+'</small></p><p><b>'+e(q['question'])+'</b></p><ul class="layer-options">'+choices+'</ul></div>'


def unit(site, row, questions, outrel):
    e = html.escape
    base = questions[row['question_ids'][0]]
    transfer = questions[row['question_ids'][1]]
    everyday, why = PLAIN[row['variant_id']]
    rationales = base.get('option_rationales', base.get('explain', {}))
    explain = ''.join('<li><b>'+e(k)+':</b> '+e(v)+'</li>' for k,v in rationales.items())
    other = ''.join('<li><b>'+e(k)+':</b> '+e(v)+'</li>' for k,v in transfer.get('option_rationales', transfer.get('explain', {})).items())
    canonical = next((out for src,out in site.pages.items() if src.endswith('/'+row['canonical_source'])), None)
    target = posixpath.relpath(canonical, posixpath.dirname(outrel))+'#learn-'+row['variant_id'].lower() if canonical else '#'
    practice = posixpath.relpath('practice/index.html',posixpath.dirname(outrel))+'?exam=CCAR-F&objective='+row['primary_objective']+'&variant='+row['variant_id']
    return ('<details class="layer-unit" id="layer-'+row['variant_id'].lower()+'"><summary>'+e(row['variant_id']+' · '+row['title'])+'</summary>'
        '<p><b>Picture the problem:</b> '+e(everyday)+'</p>'
        +question(base)+'<details class="layer-hint"><summary>What is this asking? — plain-language hint</summary><p>Which option meets the exact requirement in the question? Ask what must be known, what may run, and what the result would prove. Choose before opening the explanation.</p></details>'
        '<details class="layer-answer"><summary>I have chosen — explain the decision and show the next layer</summary>'
        '<p><b>In everyday language:</b> '+e(why)+'</p><p><b>A separate worked application of the same mechanism:</b> '+e(row['base_case'])+'</p><p><b>What breaks in that companion example:</b> '+e(row['failure'])+'</p>'
        '<p><b>Read the artifact:</b> This illustrative decision-state record belongs to the companion example above, not the exact practice question. It is not a complete runnable SDK request. Read the field names as the facts that application must keep separate.</p>'
        '<pre><code>'+e(row['mechanism_artifact'])+'</code></pre>'
        '<p><b>Why these choices:</b></p><ul>'+explain+'</ul><p><b>Reject the close alternative:</b> '+e(row['nearest_alternative'])+'</p>'
        '<p><b>Replay and prove:</b> Use the concrete failure above as the test input. Explain the recorded state before the failure, the check that changes the next action, and the receipt, source or error that must remain visible. Then trace the relevant diagram and proof in the <a href="'+e(target)+'">full objective episode</a>; a proposed repair is not execution evidence.</p></details>'
        '<p><b>Change the situation — choose again before opening the explanation.</b></p>'+question(transfer)+'<details class="layer-answer"><summary>I have chosen again — compare the changed decision</summary><p>'+e(transfer.get('rationale',''))+'</p><ul>'+other+'</ul></details>'
        '<p><a href="'+e(practice)+'">Practise the base decision</a> · <a href="'+e(target)+'">Open the complete objective and drawing</a></p></details>')


def enhance(site, written, rows, repo):
    bank = json.loads((Path(repo)/'practice/question-bank.json').read_text())
    questions = {q['id']:q for q in (bank.get('questions',[]) if isinstance(bank,dict) else bank)}
    for row in rows:
        for key in row['question_ids']:
            if key not in questions: raise ValueError('Layered teaching missing existing question '+key)
    changed = {}
    for source,outrel in site.pages.items():
        if not source.startswith(ROOT) or outrel not in written: continue
        tail = source[len(ROOT):]
        if tail.startswith(('objectives/objective-','scenario-walkthroughs/','architecture-studio/','concept-course/')) or re.match(r'L0[1-5]',tail): continue
        raw = site.text(source)
        objectives = set(re.findall(r'objective-(\d\.\d)',raw)) | set(re.findall(r'^## (\d\.\d)\b',raw,re.M)) | set(re.findall(r'\[Guide (\d\.\d)',raw))
        selected = [row for row in rows if row['primary_objective'] in objectives]
        if not selected and tail in {'HARD-DRILLS.md','deep-practice/code-level-flows.md','deep-practice/conditions-and-errors.md','deep-practice/tie-breaker-rules.md'}: selected = rows
        if not selected: continue
        root = '../' * outrel.count('/')
        options = ''.join('<option value="'+html.escape(row['variant_id'])+'">'+html.escape(row['variant_id']+' · '+row['title'])+'</option>' for row in selected)
        block = ('<details class="layer-coaching" data-layer-root="'+root+'"><summary>Optional: work through a related decision here</summary>'
            '<p>Choose a situation. Read the technical question and options first; open the everyday explanation after you decide. These checks reuse existing questions and do not change saved practice results.</p>'
            '<label>Decision to work through <select class="layer-picker">'+options+'</select></label><div class="layer-stage"></div>'
            '<noscript><p>For the same teaching without scripts, open <a href="'+root+'lessons/ccar-f/objectives/index.html">the objective lessons</a>.</p></noscript></details>')
        written[outrel] = written[outrel].replace('</h1>','</h1>'+block,1).replace('</body>','<script defer src="'+root+'assets/layered-teaching.js"></script></body>')
        changed[source] = [row['variant_id'] for row in selected]
    return changed


def asset(site, rows, repo):
    bank = json.loads((Path(repo)/'practice/question-bank.json').read_text())
    questions = {q['id']:q for q in (bank.get('questions',[]) if isinstance(bank,dict) else bank)}
    panels = {row['variant_id']:unit(site,row,questions,'index.html') for row in rows}
    return '(() => { "use strict"; const panels = '+json.dumps(panels,ensure_ascii=False)+""";
    document.querySelectorAll('.layer-coaching[data-layer-root]').forEach(box => {
        const picker = box.querySelector('.layer-picker');
        const stage = box.querySelector('.layer-stage');
        const saved = new Map();
        let current = null;
        function show() {
            if (current) saved.set(current, stage.firstElementChild);
            const next = picker.value;
            const existing = saved.get(next);
            stage.replaceChildren();
            if (existing) stage.append(existing);
            else {
                const template = document.createElement('template');
                template.innerHTML = panels[next] || '';
                const panel = template.content.firstElementChild;
                if (!panel) return;
                panel.open = true;
                panel.querySelectorAll('a[href]').forEach(a => {
                    const href = a.getAttribute('href');
                    if (!/^(https?:|#)/.test(href)) a.setAttribute('href', box.dataset.layerRoot + href);
                });
                stage.append(panel);
            }
            current = next;
            // Mark only the selected scene as exposed. Keep all attempts, scores and active sessions.
            try {
                const key = 'claude-cert-practice.v1';
                const state = JSON.parse(localStorage.getItem(key) || '{}');
                state.q = state.q || {};
                stage.querySelectorAll('[data-assessment-exposure]').forEach(el => {
                    const id = el.dataset.assessmentExposure;
                    const record = state.q[id] || (state.q[id] = {seen:0,right:0});
                    record.exposed = true;
                    record.exposure_reason = 'Opened this original practice scene in local teaching';
                });
                localStorage.setItem(key, JSON.stringify(state));
            } catch (e) { /* Reading remains available when browser storage is unavailable. */ }

        }
        box.addEventListener('toggle', () => { if (box.open && !current) show(); });
        picker.addEventListener('change', show);
    });
})();
"""
