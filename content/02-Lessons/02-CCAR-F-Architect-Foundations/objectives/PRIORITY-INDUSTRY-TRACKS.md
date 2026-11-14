# Finance, Legal and Marketing: extra architecture tracks

These are original synthetic exercises, not recalled exam items. All policies, organizations, statistics and limits below are invented. Mechanisms come from the linked objective lessons and primary docs. Each track integrates ten objectives; together they cover all 30. Complete the dedicated lessons first: these capstones do not replace the 240-bullet teaching map.

Allow 60–90 minutes per track (3–4.5 hours total). Education and Government extensions add 45–60 minutes each. Their sector names do not establish deployment eligibility, legal compliance or product entitlement. Use only supplied synthetic data. Write answers before reading the worked checks; a design answer is not an executed lab.

## Finance — reconciliation, disputed transactions and reviewed reports

**Primary objectives:** [1.1](objective-1.1.md), [1.4](objective-1.4.md), [1.5](objective-1.5.md), [2.1](objective-2.1.md), [2.2](objective-2.2.md), [2.3](objective-2.3.md), [4.3](objective-4.3.md), [4.4](objective-4.4.md), [5.2](objective-5.2.md), [5.5](objective-5.5.md).

A fictional business banking assistant reconciles invoices, explains disputed charges and prepares a report. It may draft a dispute but cannot issue money movement without the synthetic approval gate. A read-only analyst needs account activity; a dispute handler needs a scoped draft tool; a separate authorized executor owns effects. A single prompt with every tool is tempting because it avoids handoffs. Under binding approval and customer isolation, narrow contracts plus application authorization are justified. If the product becomes a read-only demonstration, the extra execution service may be unnecessary.

### Supplied evidence and interfaces

- Invoice `I17`, source `invoice/I17#page1`, published 2026-09-30: rows 120 and 80 USD; printed total 250 USD. No tax or fee line supplied.
- Statement `S17`, source `statement/S17#row9`, observed 2026-10-02: charged 250 USD, account `A8`, transaction `T9`.
- Customer message: “I expected 200. Please connect me to a person.” Identity verified for account A8 only.
- Synthetic rule `P3`, effective 2026-10-01 section 2: drafts allowed; effects require current identity, validated proposal and approval tied to that proposal version. Missing evidence cannot be treated as zero.
- Tools: `read_activity(account_id)` returns records and source locators; `create_dispute_draft(account_id, transaction_id, evidence_refs)` creates a draft only; `get_operation_status(operation_id)` checks an uncertain operation. A payment tool is absent from analyst scope. Servers check account authorization independently.
- Responses: `lookup_timeout` with retryable=true; `account_out_of_scope` with retryable=false; `no_matching_activity` with success=true and records=[]; `draft_timeout` with commit_status=unknown and operation_id D77.
- Extraction contract: account_id, currency, line_amounts, printed_total, calculated_total, conflict_detected, nullable unsupported_adjustment, evidence_refs. Strict input shape does not establish correct interpretation.

### Work before checking

1. Draw the agent loop with assistant tool request, matching tool result ID, continuation and structured stop reason. Show why an `end_turn` cannot prove D77 committed.
2. Write tool descriptions that distinguish activity lookup, dispute drafting and status checks. Assign role tool pools and an application prerequisite gate. If using named tool choice, state the current model/thinking compatibility check; do not equate forced choice with authorization.
3. Extract the invoice, run arithmetic validation and write a bounded correction request including source, prior output and failed check. Preserve unresolved source discrepancy. Normalize an ISO date after the tool result while retaining raw value; describe handling of an ambiguous `03/04/2026`.
4. Route the explicit human request immediately with account, transaction, competing amounts, sources and action status. Contrast “I'm frustrated” without a human request and an ambiguous identity case.
5. Handle every response category above. For D77 check status before retrying an uncertain write; preserve successful statement retrieval during an invoice timeout.
6. Calculate this synthetic calibration table and choose a defensible review policy:

| Document/field/bin | Reviewed | Correct |
|---|---:|---:|
| Typed invoice/total/≥0.95 | 100 | 99 |
| Scan/total/≥0.95 | 40 | 28 |
| Typed invoice/total/0.80–0.94 | 50 | 45 |
| Scan/total/0.80–0.94 | 20 | 12 |

Tomorrow has 900 typed and 100 scanned invoices. Capacity is 80 reviews. Specify random sampling inside strata, an independent holdout, and overflow behavior; a threshold alone is not a complete answer.

### Worked checks and changed constraints

The computed invoice total is 200; printed total and charge remain 250, so `conflict_detected=true`, adjustment=null. Inventing a 50 fee to reconcile them fails. A retry might resolve transcription; if the source genuinely says 250, preserve and hand off. D77 is unknown, not failed-empty. A status read precedes any new draft attempt; production idempotency controls are an extension beyond the blueprint's core error handling. A PostToolUse normalization stage shapes results; a pre-effect application gate controls action. Instructions cannot substitute for that gate.

Observed bin accuracies are 99%, 70%, 90% and 60%. High-confidence scans are unreliable despite their scores. Reviewing all 100 scans exceeds 80 capacity even before sampled typed invoices. Queue overflow or suspend automatic processing of that segment; do not quietly authorize 20 scans. Randomly select typed samples within confidence/document strata, preserve denominators and seed/selection method, then evaluate the chosen policy on untouched labels. A sample of 40 cannot establish a universal error rate. No fixed confidence threshold is guaranteed by these invented numbers.

**Pass evidence:** ten objective-linked artifacts: loop trace; escalation packet; normalization/effect boundary; three tool contracts; categorized error actions; scoped tool matrix; extracted schema; arithmetic/retry trace; ambiguity-versus-request handoffs; calibration calculations with sampling/overflow/holdout. Explain which design becomes simpler when effects are removed, and which steps remain necessary for accurate reporting.

## Legal — contract review, attributable synthesis and deadlines

**Primary objectives:** [1.2](objective-1.2.md), [1.3](objective-1.3.md), [1.6](objective-1.6.md), [4.1](objective-4.1.md), [4.2](objective-4.2.md), [4.5](objective-4.5.md), [4.6](objective-4.6.md), [5.1](objective-5.1.md), [5.3](objective-5.3.md), [5.6](objective-5.6.md).

A fictional legal operations team needs clause extraction and a reviewed risk summary across 80 contracts by 16:00. It needs attributable evidence, not an autonomous legal conclusion. A short agreement can be reviewed sequentially. Independent documents can be extracted concurrently, but synthesis depends on their findings; disagreement resolution and final review belong after extraction. Multiple agents add coordination cost and are justified here by independent evidence work and a separately checked synthesis.

### Supplied records and examples

- Contract C1 section 8, signed 2026-09-10: “Either party may terminate with thirty days' written notice.” section 12: “No automatic renewal.”
- Contract C2 section 8, signed 2026-09-12: “Customer may terminate for material breach after a 60-day cure period.” section 12: “Renews annually unless notice is received 45 days before expiry.”
- Amendment A2 section 1, signed 2026-09-25: “For C2, replace the cure period in section 8 with 30 days.” Retrieval status: verified; original C2 retained.
- Locator `C3#section 8` unavailable after two transient attempts. Other C3 sections succeeded. Coverage is partial, not “no termination clause.”
- Example pair A input C1 section 8 -> `{notice_days:30,cure_days:null,basis:"ordinary termination",source:"C1#section 8"}`.
- Example pair B input C2 section 8 plus A2 section 1 -> `{notice_days:null,cure_days:30,basis:"breach and signed amendment",sources:["C2#section 8","A2#section 1"]}`.
- Nearby negative: “Board receives a quarterly report every 30 days.” -> neither termination notice nor cure period. An unseen input says “Either party may terminate for convenience on 45 days' notice; breach has a 15-day cure period.” Extract both fields separately.
- Batch ledger at 14:00: C1 succeeded; C2 succeeded; C3 errored/transient; C4 errored/invalid_request; C5 expired; C6 canceled; C7 pending. Results arrive out of order. Current docs describe up to 24-hour processing and expiry; this does not guarantee the 16:00 business deadline.
- Prompt pilot: simple C1 succeeds; amended C2 incorrectly retains 60; table-layout C8 mistakes “45-day payment term” for notice. Held-out C9 fixture (do not use to tune the prompt): original C9 section 8, signedSep18, says “Either party may terminate for convenience on 90 days’ notice; material breach has a 20-day cure period.” Signed amendment A9 section 1, Sep28, says “For C9 section 8 replace the convenience notice period with 60 days; leave the cure period unchanged.” C9 table T1 row2 says “Payment term: 45 days.” Locators are C9#section 8, A9#section 1 and C9#T1-row2.
- Evidence conflict: report R1, published Sep1, collected Aug1–Aug31, 40 reviewed contracts, 8 amended (20%); R2 published Sep20, collected Sep1–Sep15, 20 new contracts, 8 amended (40%). Different populations/time windows; neither proves the other false.

### Work before checking

1. Design coordinator responsibilities, decomposition order and explicit structured handoffs carrying clause text, locator, signature/date, amendment linkage, uncertainty and retrieval status. Reassign a failed subtask without discarding successful evidence.
2. Write criteria for extraction versus substantive review. Supply varied positive/negative examples; extract the unseen clause. Design an independent review prompt that does not merely endorse the generator's earlier reasoning.
3. Revise the pilot prompt to link signed amendments to affected clauses and distinguish payment terms. Test on held-out C9 before scale. Choose interactive/synchronous or batch paths for the deadline; state the tradeoff and fallback trigger.
4. Reconcile out-of-order statuses by custom_id. Retry eligible failed work with cause-specific changes: transient error can retry, invalid request must be repaired, expired work needs resubmission and remaining time check; canceled/pending require their own state handling. Do not reprocess successful C1/C2 merely because arrival order changed.
5. Build a compact synthesis packet retaining action-critical clause/date/source fields and partial coverage. Detect this faulty summary: “All contracts have 30-day termination; no gaps.” Preserve both statistical claims with their denominators and dates. Render numbers as a table, a synthetic amendment announcement as dated prose, and technical limitations as a list.

### Worked checks and changed constraints

The unseen clause has notice_days45 and cure_days15; merging both into one field fails. Held-out C9 has notice_days60, cure_days20, sources C9#section 8 and A9#section 1; the 45-day payment term at C9#T1-row2 is excluded. Score those distinct fields and amendment linkage before any further tuning; once used to revise the prompt, C9 is no longer an untouched holdout. C2's signed amendment changes cure30, not ordinary notice30. Parallel C1/C2 extraction is suitable; synthesis must wait for needed outputs. C3's missing section limits conclusions. The summary “all30” loses distinct concepts and source coverage, so it must be rejected.

A complete few-shot prompt includes outputs and locators, nearby negatives and varied layouts. A representative pilot needs the amendment and table cases, followed by the unseen holdout; polishing C1 alone does not address observed failures. A 24-hour maximum batch window is unsuitable as the sole route to a two-hour deadline. An earlier batch submission could be economical; urgent late work needs a timely authorized route or an honest missed-deadline escalation. Batch is a cost/latency design decision, not always the best answer.

R1 and R2 can both be accurate: 8/40 and 8/20 describe different collections. Show separate rows rather than calling this a trend for the same cohort. A technical output should say coverage partial for C3, how retrieval failed and what recovery remains possible. Keep evidence-derived claims separate from your proposed review design. These are architecture exercises; supplied rules do not establish real legal advice.

**Pass evidence:** ten objective-linked artifacts: coordinator plan; handoff packet; staged decomposition; explicit criteria; actual example/negative/unseen outputs; batch pilot/status/deadline policy; independent review; retained context projection; partial-failure recovery; attributable synthesis in three formats. Explain when a single short contract would justify a simpler sequential workflow.

## Marketing — campaign research, content operations and repository changes

**Primary objectives:** [1.7](objective-1.7.md), [2.4](objective-2.4.md), [2.5](objective-2.5.md), [3.1](objective-3.1.md), [3.2](objective-3.2.md), [3.3](objective-3.3.md), [3.4](objective-3.4.md), [3.5](objective-3.5.md), [3.6](objective-3.6.md), [5.4](objective-5.4.md).

A fictional marketing team maintains a campaign repository and drafts advertisements from approved research. Draft generation is read-only; publishing needs separate approval. It wants consistent reusable briefs, scoped analytics access, reversible code changes and reliable restart after a crash. A small one-off copy edit needs little orchestration. A multi-file campaign renderer migration with shared rules and a failing test needs exploration, planning and validated execution.

### Supplied repository and state

```text
campaigns/CLAUDE.md         @../standards/brand.md; do not publish; preserve campaign IDs
standards/brand.md          approved claims only; dates and attribution required
.claude/rules/metrics.md    paths: analytics/** ; retain attribution-window definition
campaigns/.claude/skills/draft-campaign/SKILL.md  reusable draft procedure, manual invocation intended
campaigns/renderer.js       export {formatSpend as renderSpend} from '../lib/spend.js'
lib/spend.js                formatSpend(null) => '$0'; formatSpend(12.5) => '$12.50'
analytics/render.js        import {renderSpend} from '../campaigns/renderer.js'
tests/spend.test.js         12.5 => '$12.50' passes; null => 'unavailable' fails
```

A synthetic overgrown CLAUDE.md repeats brand rules, says “auto-publish everything,” and elsewhere says “never publish without approval.” Retain the current no-publish requirement, flag the conflict, remove duplication and preserve a checklist of retained obligations. Do not silently choose an unsafe rule because it appears later.

MCP configuration exercise: a project-scoped analytics server uses a secret reference, not a literal credential. Read-only research can list resources for approved briefs; authorized querying uses narrowly described tools. Unrelated publishing tools are not available to the drafting role. Resource discovery is not itself permission to execute a server tool.

Campaign fixture: id M42, budget cap1200 USD, draft versionv3, approved claim sourceB4#p2 datedSep30, countryUK, publish_approved=false. Crash ledger: discoverydone, draftdone, approvalpending, publishnotstarted. A compacted summary incorrectly says “M42 is ready to publish; budget around1500.” Session S1 holds exploratory reasoning; S2 is a fork for a rendering alternative. Resuming must distinguish conversation state from verified external effect state.

CI prior finding F7: null displayed as zero, still open. Prior finding F8: missing date citation, resolved in v3. Existing test covers decimal12.5. New proposed test duplicates that decimal case. A model returns valid JSON with no findings despite the null bug; another returns empty stdout. Both need independent interpretation, not automatic pass.

### Work before checking

1. Map session resume/fork use and durable ledger boundaries. Write an explicit /compact preservation instruction and diff the lossy summary against M42 constraints. Resume at approvalpending, not publishing.
2. Split the overgrown instructions into project context, focused rules and referenced standards. Identify path applicability, memory/config verification and which files actually load. Write retained-obligations and conflict records.
3. Define a skill with description, manual invocation behavior and tool controls. Explain that allowed-tools pre-approval is not a restriction; check current disallowed-tools support separately from the exam wording. Provide a structured command example in the current skills model and note legacy commands remain supported. Do not put credentials into either format.
4. Specify MCP project/user scope and discovery-versus-tool use. Trace renderer alias to implementation with filename search followed by content search and targeted reads; report caller, implementation and existing test.
5. Explore/plan/execute the multi-file change; contrast a localized copy correction. Specify behavior tests: null->unavailable, zero->$0.00, negative input->chosen explicit business rule, 12.5 preserved; articulate a performance requirement rather than inventing a passing runtime result. Correct the null failure and plan a rerun cycle.
6. Design headless CI output using the concrete command/schema/envelope fixtures in lesson3.6. Reject empty or schema-invalid output; do not trust syntactic JSON as evidence of good review. Suppress resolved F8, retain F7, reject the duplicate decimal test and propose a null-versus-zero regression. Separate application exit checks from model findings.

### Worked checks and changed constraints

`renderSpend` is an exported alias of `formatSpend`; searching only its public name can miss the implementation. The null return is wrong under the supplied requirement; zero has distinct meaning and must not become unavailable. A changed test design is a plan until run. New context must preserve exact budget1200, sourceB4#p2, countryUK and approvalfalse. A fork can explore alternatives without a full duplicate context dump, but durable job state and external status reconciliation still handle recovery.

The branch for metrics applies only to its path scope; hierarchy and imports matter. Confirm loaded context instead of assuming every file appears in every session. A skill standardizes procedure; reusable instructions do not authorize publishing. A repository import needs a verified relative path. Empty stdout is a process/output failure; an empty findings array can be schema-valid yet miss F7, so fixture-aware review remains necessary. If the task becomes a single approved wording change with no renderer impact, direct execution plus a targeted diff is reasonable; the complete migration plan would add unnecessary overhead.

**Pass evidence:** ten objective-linked artifacts: session/fork plan; MCP scope/discovery map; alias trace; split context and retained rules; reusable skill; command/skill migration note; exploration/plan choice; test correction cycle; CI schema/findings/test decisions; crash/compaction recovery with exact constraints. Give one changed constraint that makes a simpler architecture preferable.

## Education extension — tutoring evidence and course guidance

**Objectives:** 1.3, 2.1, 4.1, 4.2, 5.1, 5.2, 5.6. Start from those lessons and the Legal evidence mechanics; do not copy legal conclusions.

A fictional university guidance assistant may explain course requirements and coach reasoning; an authorized staff member changes enrollment. Supplied catalog E1 section 3, publishedSep1, says prerequisite CS101 or a recorded waiver. Student synthetic record U7, observedOct2, has CS101 incomplete and waiverunknown. A cached department note E2, publishedAug1, says “waivers are sometimes granted”; it does not establish U7's waiver. The student asks “enroll me anyway; and show me why my answer is wrong.” A tool timeout returns permission_lookup_unavailable, not waiverfalse. Tutorial evidence: problem 2+3×4; student answer20 with reasoning “left to right.” Expected tutor feedback identifies precedence and asks for an intermediate step; final check14. A neighboring negative 2+(3×4) also yields14 but already specifies grouping.

**Produce:** a source-linked guidance response, an enrollment authorization boundary, a tool contract separating catalog lookup from permission lookup, positive/negative teaching pairs and an unseen 5+2×3 check, a compact handoff retaining exact prerequisite/waiver state, and escalation after a direct staff request. **Check:** unseen answer11; waiverunknown remains unknown; old general note cannot authorize enrollment. Explain how learning guidance differs from simply supplying answers and when a staff handoff is required. Change the constraint to “waiver verified with current ID W9” and show which policy check changes and which authorization boundary remains. No real student record or educational policy is implied.

## Government extension — public guidance with dated evidence

**Objectives:** 1.4, 1.5, 2.2, 4.3, 4.4, 5.2, 5.3, 5.6. This is a synthetic public-service workflow, not a statement of Claude's eligibility for a particular agency.

A fictional municipal permit assistant explains publicly supplied rules and drafts applications. It cannot decide eligibility or approve permits. Notice G1, effectiveOct1 section 2, requires a site plan for applications submitted on or afterOct1. Archived G0, effectiveJan1, omitted it. Applicant A4 submittedSep30; A5 reports submitting Oct2, but that date is unverified. Tool evidence: A4 record retrieved, A5 submission lookup transiently unavailable. A scanned fee schedule G2 lists base40 plus inspection25, printed total75 with no extra line. A news notice G3, publishedOct2, says a new office opened Oct1; this does not change permit requirements. Review staff can handle10 uncertain cases today, but12 arrive.

**Produce:** separate dated rule applicability claims with locators; nullable submission state for A5; fee validation40+25=65 versus printed75; immediate handoff after an explicit human request; categorized recovery for unavailable versus ineligible; a pre-effect approval gate; an overflow policy and a news-prose summary that does not imply legal eligibility. **Check:** A4's known date precedes the new rule; A5 cannot be classified until its submission date is verified. Retain both fee values and route contradiction. Queue or pause excess uncertain work instead of relaxing criteria. Contrast a read-only informational assistant with a system authorized to submit a draft; distinguish submission acknowledgement from permit approval. Exact applicability here follows the invented rule, not real municipal law.

## Source and completion record

Mechanisms: [saved official guide section 6](https://anthropic-partners.skilljar.com/page/partner-certifications); [tool definitions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools); [Claude Code memory](https://code.claude.com/docs/en/memory); [skills](https://code.claude.com/docs/en/skills); [headless](https://code.claude.com/docs/en/headless); [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs); [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing). Current APIs require compatibility checking; illustrative paper designs are not executed integrations.

Industry context only: [Qonto](https://claude.com/customers/qonto), [Spellbook](https://claude.com/customers/spellbook), [Anthropic's internal team use report, marketing and legal sections](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf), [education help](https://support.claude.com/en/articles/11139144-use-claude-for-education-at-your-university), [historical public-sector announcement](https://www.anthropic.com/news/expanding-access-to-claude-for-government). These establish context, not validation of our designs. The government announcement is historical and is not evidence of current procurement availability.

For each track save your artifacts, reviewer corrections, a changed-constraint answer and a later unseen attempt in your private objective progress record. Track content reviewed separately from learner attempted, learner passed and lab executed. Passing this capstone does not waive any objective lesson or independently tagged question practice.

## Practice changed constraints

Use the [decision atlas](../decision-atlas.md) to compare the base choice, changed constraint and failure path. Finance changes approval, monetary consistency and source-age risk; Legal changes evidence attribution, privilege/access and ambiguity; Marketing changes consent, segment criteria and false-positive cost. These are synthetic transfer contexts, not official industry weightings. Keep the underlying Claude mechanism explicit.