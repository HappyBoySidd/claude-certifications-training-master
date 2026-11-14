# CCAR-F SIM-01 — Full mock exams

<!-- layered-scenario-migration -->
## Keep learning and exam rehearsal separate

For a timed mock, use the practice app's mock mode and keep lesson explanations, hints, coach keys and failure-layer replays closed until submission. Existing item identifiers, scoring and progress remain unchanged. The authored scenario layers are learning material, not additional scored mock items.

After submission, classify each miss before opening its lesson: did you misunderstand the application, miss the constraint, confuse similar mechanisms, trust a successful-looking result, or fail to change your answer when a condition changed? Record the governing constraint and the closest rejected alternative, not just the answer letter.

| Decision to repair | Revisit the plain-language scenario | Independent retest |
| --- | --- | --- |
| Tool selection, approval or ambiguous effects | [Support simulation](SIM-02-customer-support-agent.md) | Change target/amount or timeout state; choose the mechanism again |
| Repository scope, planning or specific feedback | [Code-change simulation](SIM-03-code-generation-claude-code.md) | Contrast a local edit with a cross-file change |
| Missing specialist context or partial evidence | [Research simulation](SIM-04-multi-agent-research.md) | Remove a mandatory source and identify the blocked conclusion |
| Capability discovery or stale resumed context | [Developer simulation](SIM-05-developer-productivity.md) | Separate connection, inclusion and authority |
| Headless output or noisy review | [CI simulation](SIM-06-claude-code-ci-cd.md) | Contrast a job error with a valid zero-finding report |
| Handoff validation or mixed file failures | [Extraction simulation](SIM-07-structured-data-extraction.md) | Distinguish wrong shape, wrong fact and missing evidence |

These diagnostic categories support learning; they are not official scoring categories or a pass guarantee. A retest on the same memorized wording is weaker evidence than explaining the decision under a changed constraint.

<!-- /layered-scenario-migration -->


**Build the application picture first:** [AS 01 action service](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-01-action-service.md) · [AS 02 document pipeline](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-02-document-pipeline.md) · [AS 03 grounded assistant](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-03-grounded-assistant.md) · [AS 04 research system](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-04-research-system.md) · [AS 05 code change](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-05-code-change.md) · [AS 06 ci review](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-06-ci-review.md) · [AS 07 work queue](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-07-work-queue.md) · [AS 08 resumable case](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-08-resumable-case.md)

Take runs A, B, D and E in order, **on different days**, using the exam-day conditions in [the simulations README](../README.md). Run C (last row) is an optional warm-up you can do any time.

| Run | Mock | Length | Notes |
| --- | --- | --- | --- |
| A | [claudecertificationguide.com diagnostic](https://claudecertificationguide.com/learn/diagnostic) (Tier 2) | about 15 min | The baseline from lesson L00. A colleague said it matched the real exam (field report). |
| B | [Practice tool](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) ([published app](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)), CCAR-F **Start mock** | 60 questions, 120 min | A draw using saved domain weights. The app displays the current eligible pool; learning-only caveats, quarantined items and delayed retries are excluded from normal mixed mocks. Practice accuracy is not an official scaled score. |
| D | [claudecertificationguide.com full mock](https://claudecertificationguide.com/mock-exam/start) (Tier 2) | 60 questions, 120 min | A colleague said the link was sometimes down. If it is, skip to run E. |
| E | **The exam guide's 12 sample questions** (CCAR-F exam guide v1.0 (Anthropic), section 9 sample questions, Tier 1) | 12 questions | **All correct, with the reason each wrong option is wrong.** The official practice exam was retired in the move to Pearson, the company that now runs the exam ([Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1, checked 2026-10-02). |
| C (optional warm-up) | Amey Thakur mocks (Tier 2, MIT licence): [1](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/architect-foundations/mock-exam-1.md), [2](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/architect-foundations/mock-exam-2.md), [3](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/architect-foundations/mock-exam-3.md) | 45 questions, untimed | **Warm-up only, not scored**: in these mocks the right answer is nearly always the longest option, so a score here says little about readiness. Use them for recall. Don't count the score as a mock. They return as a timed run once these questions are rewritten. |

Tier 2 mocks are written by other people. Where one disagrees with the official exam guide or the
Claude docs, the guide and docs win.

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

Use the studio to repair a missed decision after the mock, then return to practice without resetting your saved session. Record the objective, deciding signal and changed-condition answer; local mock results do not predict an official scaled score.

**Build the mechanism:** [Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.

## After each run

1. Redo only the questions you got wrong (**Fix my mistakes** in the tool).
2. For a weak domain, reread the lesson, then drill that domain in the tool.
3. For runs A, B, D and E, note the date, run, score and two weakest domains. Run C is a warm-up: don't log it as a mock score.

A colleague's advice from Slack (field report): **full-length practice exams matter most**. It's
the one exam where he needed all 120 minutes.

Sources: CCAR-F exam guide v1.0 (Anthropic)
and the [Partner Academy certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) (Tier 1); mock sites and repos as
labelled above (Tier 2); colleague comments (F, field reports).


## External mock: return to local repair

[Open Claude Certification Guide mock](https://claudecertificationguide.com/mock-exam/start) in another tab, then return here. This is an independent supplementary publisher, not Anthropic. Quick mode 28 questions/56 minutes; full mode 60/120 minutes (source reviewed 2026-10-12). The inspected catalog has79unique IDs,73rationales reviewed and6pending; the advertised250+pool was not exhausted. Questions have not been imported.

Some explanations need qualifications: schema validity does not prove truth; nullable fields do not fix wrong non-null values; post-action processing cannot undo earlier effects; tool forcing alone is not full semantic validation. Use official task guidance and current primary documentation when a mock rationale conflicts.

Record only your missed objective IDs, confidence and your own takeaway. Nothing is transmitted; the note stays in this browser. Do not paste question-bank text or confidential exam questions.

<div class="external-repair"><form id="external-repair-form"><label>Missed objectives <input name="objectives" placeholder="1.2, 3.6" required></label><label>Confidence <select name="confidence"><option>Unsure</option><option>Partly confident</option><option>Confident</option></select></label><label>Your decision takeaway <textarea name="takeaway" maxlength="2000"></textarea></label><button type="submit">Save missed tasks and show repair links</button></form><div id="external-repair-results" role="status"></div><script defer src="../../assets/external-practice.js"></script></div>

Use [local objective practice](../../practice/index.html?exam=CCAR-F) to work a different case after repair.