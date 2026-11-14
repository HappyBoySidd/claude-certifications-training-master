# CCAR-F Lesson 5 — Context Management and Reliability (15%; about 9 of 60 questions by our arithmetic, not a number the guide gives)

**Picture the application:** A long support conversation mentions a precise refund amount and order number early on. Later, its summary remembers only that a refund was requested. The service needs the original details and current status to remain available. Context management and reliability are the technical topics behind keeping that business case intact.

**Time:** 90 min · **Practice:** [CCAR-F practice — choose Domain 5](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)
**Scenarios:** 1 Support, 2 Code generation, 3 Research, 6 Extraction. It shows up in more
scenarios than any other domain.


<!-- layered-scenario-migration -->
## Learn this domain through connected case studies

Read and predict; no account, code execution or setup is required for these teaching scenes. Each stage names its application and the requirement that fails. Some stages transfer the same decision to a different application; follow the named people and data rather than assuming every stage belongs to one system. The original reference sections remain below for detail. These are original teaching questions, not claimed live exam items. Write your choice before revealing the repair. Diagrams below show AI reasoning and ordinary software checks explicitly in their labels.

### Stage 1 — A resumed case remembers the old approval

A support case continues tomorrow. A summary remembers the customer’s goal and yesterday’s approved proposal, but the amount has changed. The application needs continuity without treating remembered state as fresh permission.

**Original exam-style practice — choose ONE.** Which resumption strategy best preserves useful context while respecting changing external facts?

A. Restore a bounded state packet containing goal, decisions, sources and unresolved work, then refresh volatile facts and revalidate approvals before effects.

B. Paste the entire transcript and assume every old fact remains current.

C. Start from nothing and discard the case identifier.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice A.** A summary is a handover note, not a live bank record. A retains useful work and rechecks time-sensitive facts. B keeps old errors and stale authority; C loses continuity. Session resumption and business authorization are different layers.

**Follow the changed path:**

```text
case checkpoint → restored task/state → refreshed evidence and authority → next permitted step
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Change the amount or expire approval between sessions. The restored case must request the necessary fresh check instead of submitting based on the old summary.

</details>

**Changed-constraint decision — choose ONE before revealing:** Only a small repository area matters. A: read every file into context; B: retain the map and search/read relevant paths as needed.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Keep the route to evidence and fetch what matters. Context size alone does not guarantee relevant understanding.

</details>

**Objective connections:** [5.1](objectives/objective-5.1.md), [5.4](objectives/objective-5.4.md).

### Stage 2 — One source fails, but the report sounds complete

A legal research coordinator has two successful sources and one inaccessible mandatory source. The report combines the available facts and announces that every requirement is satisfied.

**Original exam-style practice — choose ONE.** Which synthesis and escalation pattern best preserves provenance and handles a failed mandatory dependency?

A. Hide the failed source because most work succeeded.

B. Discard all successful evidence and restart every worker.

C. Retain attributed successful findings, mark the failed dependency and withhold conclusions that require it; hand off the unresolved question and attempted recovery.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice C.** Keep what is known, show what is not, and connect each conclusion to its evidence. A presents unsupported certainty; B wastes valid work. A useful handoff says what remains blocked and what would resolve it.

**Follow the changed path:**

```text
successful sources → attributed claims
mandatory source failure → blocked dependent conclusion → actionable review packet
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Inspect each final claim for source, date and uncertainty. A partial result must never be relabeled complete simply because its JSON fields are present.

</details>

**Changed-constraint decision — choose ONE before revealing:** Two credible sources disagree. A: silently average their claims; B: show both claims with scope/date and investigate or escalate the unresolved contradiction.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Preserve the disagreement until evidence supports resolving it. Agreement cannot be manufactured by smoothing the prose.

</details>

**Objective connections:** [5.2](objectives/objective-5.2.md), [5.3](objectives/objective-5.3.md), [5.6](objectives/objective-5.6.md).

### Stage 3 — A strong average hides the difficult cases

An extraction system scores 96% on a sample dominated by utility bills. The team wants to remove human review of insurance claims too. Claims are rare in the sample and their high-risk fields have not been examined separately.

**Original exam-style practice — choose ONE.** Which evaluation best supports risk-based human review across heterogeneous document types?

A. Use the aggregate accuracy as proof every document type is ready.

B. Measure field/type-specific performance on representative labeled data, calibrate confidence and retain risk-based review plus sampled audits of high-confidence outputs.

C. Review only outputs where the model says it feels unsure, without calibration.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** Ask whether the score means the same thing for claim amounts as for utility invoice dates. A hides weak slices; C trusts a confidence number without checking what it predicts. Review capacity should follow error risk and demonstrated performance.

**Follow the changed path:**

```text
labeled examples by type/field → measured errors and confidence calibration
contradiction / risk / uncertain field → human review; high confidence → sampled audit
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Report the denominators and error rates for claims, bills and high-risk fields. Inspect confident mistakes as well as uncertain ones.

</details>

**Changed-constraint decision — choose ONE before revealing:** The reviewer can inspect only 10% of records. A: choose the first tenth; B: prioritize uncertain/contradictory/high-risk cases and reserve a stratified sample to detect confident failures.

<details><summary>Reveal changed-constraint reasoning</summary>

B. The review budget must detect both known risk and hidden overconfidence. No fixed threshold is justified solely by its numeric appearance.

</details>

**Objective connections:** [5.5](objectives/objective-5.5.md).

<!-- /layered-scenario-migration -->

## Connect plain reasoning to technical choices

Start with the business constraint, then learn the documentation term and the option it rules out. These worked application bridges show both levels: [AS-07-work-queue](architecture-studio/AS-07-work-queue.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-08-resumable-case](architecture-studio/AS-08-resumable-case.md#connect-the-simple-explanation-to-technical-design-choices). Read [artifact types and study mode](architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course) before interpreting examples as build instructions. Reading needs no API setup; runnable activities retain their own prerequisites.


## 5.0 The big idea

Long conversations and big tool outputs blur the details that matter, so keep key facts in a
structured, source-linked state that is deliberately preserved and refreshed across summaries. Escalate for clear reasons (the customer asks,
policy has a gap, no progress), not because someone sounds upset. Report failures and uncertainty
honestly, with sources, instead of hiding them.

## 5.1 Keeping the facts that matter in long conversations

- **Progressive summarization blurs the details:** amounts, percentages, dates and what the
  customer said they expected.
- **Position effects:** important facts can be missed in long inputs, including material in the middle; no position guarantees reliable interpretation.
  Put a **summary of key findings first** and use clear section headers.
- Tool results pile up. A 40-field order lookup where 5 fields matter wastes tokens. **Trim tool
  output** to the relevant fields before it builds up.
- Keep a persistent **"case facts" block** (amounts, dates, order numbers, statuses) in every
  prompt, **outside** the summarized history. For sessions with several issues, keep a separate
  structured layer for each issue.
- Upstream agents should return **structured key facts and citations**, not long reasoning, when
  downstream context is tight. Subagents include metadata such as dates and sources.
- The saved guide asks for conversation continuity. In current application design, supply coherent relevant history; retain linked tool calls/results when needed and use verified summaries, exact case facts and retrieval for long work. Do not resend every raw message forever. A summary must preserve constraints, provenance and unresolved issues, not merely shorten prose.

## 5.2 Escalation and ambiguity

**Escalate when:**

- the customer **asks for a human**. Do it **right away**, without investigating first.
- policy has an **exception or gap**, or is silent. For example, a competitor price match when the
  policy only covers the company's own site.
- the agent **can't make meaningful progress**.

**Don't:**

- escalate based on **sentiment** or **self-reported confidence**. Neither reflects how complex the
  case really is.
- escalate just because a case is complex.

**Frustrated but the case is simple:** acknowledge the frustration and offer to resolve it. Escalate
if they ask again.

**Watch out:** low confidence is a bad *escalation* trigger but a valid *review-routing* signal for
extractions, once the scores are calibrated (5.5). And conflicting sources get annotated with their
attribution, not settled by whichever has the higher confidence score (5.6) (exam guide tasks 5.2,
5.5, 5.6, Tier 1).

**Several matching customers:** **ask for another identifier**. Don't guess using a heuristic.

Put the escalation criteria **and few-shot examples** in the system prompt.

## 5.3 Passing errors between agents

- Pass up **structured error context:** failure type, what was tried, partial results, and
  alternatives.
- **An access failure (timeout) is not an empty result (no matches).**
- Both of these are **anti-patterns:**
  - **silently suppressing errors** by returning empty as if it succeeded
  - **stopping the whole workflow** because one part failed
- Subagents recover locally from transient errors. The synthesis output carries **coverage
  notes**: which findings are well supported and where there are gaps.

## 5.4 Exploring a large codebase

- Signs of degradation: inconsistent answers, and talk of "typical patterns" instead of the
  specific classes found earlier.
- **Scratchpad files** keep key findings across context boundaries.
- **Subagents** handle verbose exploration ("find all test files", "trace refund flow") while the
  main agent coordinates.
- **Summarize each phase** before starting subagents for the next one.
- **Crash recovery:** each agent exports its state to a known location, and the coordinator loads
  a **manifest** (a small index file listing each agent's saved state and where it is) when it
  resumes.
- **`/compact`** frees space when context fills with verbose output. Compaction summarizes, so it
  can drop detail. Keep facts that must survive in a case-facts block or a file. `/clear` starts
  fresh; `/context` shows what is filling the window. ([context guidance](https://code.claude.com/docs/en/best-practices), checked 2026-10-21.)
- **Long-context design choices:** load data just in time instead of upfront;
  server-side compaction; prompt caching, which cuts cost and latency but does **not** free context
  space; and the memory tool, which stores facts outside the window. A fifth lever is **context
  editing**, which clears old tool results or old thinking blocks server-side (beta header
  `context-management-2025-06-27`); the docs say compaction is generally preferred for long runs.
  (Source: https://platform.claude.com/docs/en/build-with-claude/context-editing, checked 2026-10-21.)

These API features depend on supported models, platforms and configuration. They are current
implementation context, not additional official objectives. Memory requires actual storage and
retrieval; preserve exact decisions before clearing their supporting context.

## 5.5 Human review and confidence

- **97% overall accuracy can hide** poor performance on one document type or field.
  **Check accuracy by document type and by field** before you automate.
- Use **stratified random sampling** (pick a random sample from each group, such as each document
  type, so small groups aren't missed) of high-confidence extractions to track error rates and
  spot new patterns.
- Output **confidence for each field** and **calibrate the thresholds on a labeled validation
  set** (set the "send to a human" cut-off by checking which confidence scores were actually right
  on documents where you already know the answer). Send low-confidence or contradictory items to
  humans, whose time is limited.

## 5.6 Provenance and uncertainty

- Summarizing loses attribution unless you keep **claim-source mappings** (URL, document,
  excerpt) all the way through synthesis.
- **Conflicting statistics** from credible sources: **note the conflict and credit each source**.
  Don't pick one at random. Let the coordinator decide how to reconcile them.
- **Record dates** (publication or collection) so a change over time isn't mistaken for a
  contradiction.
- Separate what's well established from what's contested. Show financial data as tables, news as
  prose, and technical findings as lists.

## Worked example

After 30 turns, the support agent's summary says "the customer wants a refund" and has lost the
$247.83 amount and the order number. **Answer:** a persistent case-facts block kept outside the
summarized history, with explicit preservation and refresh checks. In this case the defect is lossy state management; a larger context window alone does not repair the missing facts. Larger capacity can still help when measured limits remain after state and retrieval design are sound.

## Traps

- "Escalate when the customer sounds angry."
- "Pick the most recent customer record when there are 3 matches."
- "Return an empty list when the search tool times out."
- "97% accuracy, so remove human review."

## Try it (45 min)

Take (or write) a 30-turn support transcript that mentions a dollar amount and an order number
early on. Write a case-facts block for it: customer ID, order number, amount, dates, status, and
what the customer expects. Then have Claude summarize the transcript with the block kept outside
the summary, and compare.

Done when the dollar amount and the order number survive the summary word for word.

## Done when

- [ ] You can list the 3 escalation triggers and the 2 unreliable signals
- [ ] You can explain access failure vs empty result, and both error anti-patterns
- [ ] Case facts, scratchpads, manifests and `/compact`: you can say which problem each one
      solves, in one line each
- [ ] You scored 80% or more on [CCAR-F practice — choose Domain 5](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)

**Go deeper:**

- **Deep practice:** [Deep practice 5](deep-practice/05-context-management-and-reliability.md), which takes every section of this lesson further (5.2 is in [deep practice 1](deep-practice/01-agentic-architecture-and-orchestration.md#52-escalation-and-ambiguity-resolution) and 5.5 in [deep practice 4](deep-practice/04-prompt-engineering-and-structured-output.md#55-human-review-and-confidence-calibration)).
- **Official course:** the context-management parts of the official course *Building with the Claude API* from the [CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) (Anthropic, Tier 1, checked 2026-10-02).
- **Flashcards and drills:** the Domain 5 section of the [flashcards](FLASHCARDS.md) and the 9 Domain 5 drills (26–30, 41, 43–45) in [HARD-DRILLS.md](HARD-DRILLS.md).
- **Charts:** decision charts [13 Escalation or human review](deep-practice/decision-charts.md#13-hand-it-to-a-person-escalation-or-human-review) and [14 Context filling up](deep-practice/decision-charts.md#14-context-is-filling-up-or-facts-are-getting-lost-which-fix).

**Next:** do the diagnostic again and compare with your L00 score, then [Deep practice 5](deep-practice/05-context-management-and-reliability.md), then the [scenario simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md).

## Sources

- Official exam guide v1.0, task statements 5.1–5.6 (Tier 1; saved scope, latest revision not certified).
- [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Anthropic primary source; targeted context corrections checked 2026-10-17). Exact-state persistence here is an application design pattern and needs its own validation.

## Objective modules

For deeper learning and a separate practice/completion check for each objective:

- [Objective 5.1](objectives/objective-5.1.md)
- [Objective 5.2](objectives/objective-5.2.md)
- [Objective 5.3](objectives/objective-5.3.md)
- [Objective 5.4](objectives/objective-5.4.md)
- [Objective 5.5](objectives/objective-5.5.md)
- [Objective 5.6](objectives/objective-5.6.md)

## Decisions in this domain

| Objective | Decision variant and exact repair |
| --- | --- |
| 5.1 | [FV-25 — Compact the decision state, not just prose](objectives/objective-5.1.md#variant-fv-25) |
| 5.2 | [FV-26 — Honor explicit escalation with context](objectives/objective-5.2.md#variant-fv-26) |
| 5.3 | [FV-27 — Propagate partial success without hiding failure](objectives/objective-5.3.md#variant-fv-27) |
| 5.4 | [FV-28 — Build a minimal code evidence ledger](objectives/objective-5.4.md#variant-fv-28) |
| 5.5 | [FV-29 — Test risk slices and review capacity](objectives/objective-5.5.md#variant-fv-29) |
| 5.6 | [FV-30 — Keep sources through a join](objectives/objective-5.6.md#variant-fv-30) |

**Interpret local practice targets:** any 80% target above is an optional project study heuristic, not a validated mastery threshold or conversion to the official scaled score. Use fresh decisions, explanations and delayed transfer alongside remaining objective gaps.