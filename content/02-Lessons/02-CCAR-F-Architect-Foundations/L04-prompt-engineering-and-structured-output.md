# CCAR-F Lesson 4 — Prompt Engineering and Structured Output (20%, about 12 questions)

**Picture the application:** An invoice arrives without a printed date, and the intake assistant produces a neat record containing an unsupported date. The expected result preserves what the document actually provides and makes missing information explicit. Prompt engineering, schemas and validation are the technical tools for controlling format without confusing it with factual correctness.

**Time:** 2 hours plus [lab 02, the agent loop, subagents and schema-checked extraction lab](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) (extraction part) · **Practice:** [CCAR-F practice — choose Domain 4](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)
**Scenarios:** 5 CI/CD, 6 Extraction · A colleague who passed said structured output was "heavy" on their exam.


<!-- layered-scenario-migration -->
## Learn this domain through connected case studies

Read and predict; no account, code execution or setup is required for these teaching scenes. Each stage names its application and the requirement that fails. Some stages transfer the same decision to a different application; follow the named people and data rather than assuming every stage belongs to one system. The original reference sections remain below for detail. These are original teaching questions, not claimed live exam items. Write your choice before revealing the repair. Diagrams below show AI reasoning and ordinary software checks explicitly in their labels.

### Stage 1 — A review flags everything that looks unusual

A marketing compliance reviewer flags any mention of price as a violation. The business actually forbids unsupported discount promises, not ordinary published pricing. The prompt says only “find risky copy.”

**Original exam-style practice — choose ONE.** Which prompt revision most directly improves precision without suppressing genuine violations?

A. Ask for fewer findings regardless of evidence.

B. Specify the violation criteria, require supporting text, and give contrasting compliant/noncompliant examples.

C. Tell the model to be absolutely certain without defining the rule.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The model needs to know what counts as a problem. Include a compliant published price and an unsupported discount promise, with the reason for each. A hides real problems; C changes tone rather than the decision rule.

**Follow the changed path:**

```text
copy + explicit criteria + examples → evidence-backed finding → reviewer checks rule fit
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Replay both examples and a new wording. Measure false positives and missed violations separately; a shorter report is not automatically a better report.

</details>

**Changed-constraint decision — choose ONE before revealing:** New documents put payment terms in footnotes. A: add representative input/output examples for varied layouts; B: add only more emphatic wording.

<details><summary>Reveal changed-constraint reasoning</summary>

A. Examples teach the mapping across layouts. Keep a genuine absence example so the system does not invent a field just to satisfy the demonstration.

</details>

**Objective connections:** [4.1](objectives/objective-4.1.md), [4.2](objectives/objective-4.2.md).

### Stage 2 — The handoff parses, but the invoice is wrong

A document worker sends a record to an accounting application. It contains vendor, currency and total. The record is valid JSON, but says USD 900 while the invoice says USD 90. Here JSON is the container crossing this handoff; the business failure is the wrong extracted amount.

**Original exam-style practice — choose ONE.** Which receiving-side validation best prevents schema-valid but unsupported extracted values from reaching the downstream system?

A. Accept every record that parses as JSON.

B. Apply schema/type checks plus source-grounded semantic checks, preserve discrepancies and use bounded repair or review.

C. Ask the model for a higher confidence score and skip the source check.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** Check both the shape and meaning. A schema can verify a numeric amount field, but the source decides which amount is supported. A validates only the container; C does not provide independent evidence. Constrained output helps at its supported boundary; it does not make source facts true.

**Follow the changed path:**

```text
invoice text → extracted record → shape check → source/amount check
wrong amount → specific feedback or review; supported value → eligible downstream record
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Use USD 90 and USD 900 test outputs against the same source. Both may pass type checks; only the supported amount may pass the business check. Preserve the source and failed value.

</details>

**Changed-constraint decision — choose ONE before revealing:** The vendor name is absent from all supplied material. A: keep retrying until one appears; B: mark unresolved and retrieve missing evidence or route to review.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Retry can repair a reading error, not create absent evidence. Optional/nullable fields must match the business contract; do not silently waive a required business fact.

</details>

**Objective connections:** [4.3](objectives/objective-4.3.md), [4.4](objectives/objective-4.4.md).

### Stage 3 — Ten thousand files finish with mixed outcomes

One invoice is easy to inspect. Overnight work now contains 10,000 independent files: 9,700 validate, 180 are unreadable, 100 hit transient service errors and 20 conflict with their sources. Those fictional ledger counts describe content/processing outcomes, not API status names.

**Original exam-style practice — choose ONE.** Which bulk-processing recovery design preserves completed work while making unresolved files visible?

A. Resubmit all 10,000 items whenever any result fails.

B. Join results by stable request IDs, keep per-item states, retry eligible transient failures within bounds, repair/quarantine bad inputs and reconcile downstream acknowledgements.

C. Mark the whole workload successful once the batch reports completion.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The ledger lets you recover the 100 temporary failures without replaying 9,700 accepted items. The unreadable inputs need preparation; the conflicting records need evidence review. A risks duplicate downstream writes; C hides unresolved work. Batch results can arrive out of order.

**Follow the changed path:**

```text
file ID → preparation → request ID → API outcome → output checks → downstream acknowledgement
unresolved item → retry / repair / quarantine; accepted item → retain checkpoint
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Reconcile 9,700 + 180 + 100 + 20 = 10,000 before retries. After retries, count every item in exactly one current state and preserve attempt history. An API success still needs content validation.

</details>

**Changed-constraint decision — choose ONE before revealing:** The next job requires an answer in seconds. A: use asynchronous batch processing regardless of latency; B: select an interactive path with its own bounded recovery.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Deadline and dependency shape the design. Batch is for eligible independent work that can wait; it does not replace interactive or ordered workflows.

</details>

**Objective connections:** [4.5](objectives/objective-4.5.md), [4.6](objectives/objective-4.6.md).

<!-- /layered-scenario-migration -->

## Connect plain reasoning to technical choices

Start with the business constraint, then learn the documentation term and the option it rules out. These worked application bridges show both levels: [AS-02-document-pipeline](architecture-studio/AS-02-document-pipeline.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-03-grounded-assistant](architecture-studio/AS-03-grounded-assistant.md#connect-the-simple-explanation-to-technical-design-choices). Read [artifact types and study mode](architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course) before interpreting examples as build instructions. Reading needs no API setup; runnable activities retain their own prerequisites.


## 4.0 The big idea

Vague instructions give vague results: name exact criteria and show 2–4 examples instead. For
output a program will read, use a compatible schema-constrained interface for shape, then validate meaning against evidence and business rules. Tool selection alone does not ensure strict conformance. Deferred independent work may suit Batches only when dependencies, actual processing window and recovery fit its deadline.

## 4.1 Explicit criteria reduce false positives

- "Flag comments **only when claimed behavior contradicts the actual code**" beats "check that
  comments are accurate".
- **"Be conservative" and "only report high-confidence findings" don't improve precision.** Specific
  categories do.
- A category with lots of false positives drags down trust in the accurate ones. **Switch off the
  noisy category temporarily** while you fix its prompt.
- Define severity with **concrete code examples for each level**.

## 4.2 Few-shot examples

- The most effective way to get **consistent, actionable format** when instructions alone vary.
- Use **2–4 targeted examples** of *ambiguous* cases, showing **why** one action beat the
  alternatives.
- Show the format (location, issue, severity, suggested fix). Show acceptable patterns next to real
  issues. Show varied document structures (inline citations vs a bibliography).
- They reduce made-up values and empty required fields in extraction, and they **generalize** to new
  cases.

## 4.3 Structured output through tool use

- **A declared tool input schema describes expected arguments.** For enforced conformance use a supported strict/schema-constrained mode, and check exceptional outcomes; ordinary tool invocation is not an unconditional shape guarantee.
- It does **not** remove *semantic* errors: line items that don't add up, or a value in the wrong
  field.
- **Today, not the exam:** the API can go further with **structured outputs** (`strict: true` on
  a tool, or a JSON schema in `output_config.format`). Structured outputs guarantee the shape: the
  reply always matches your schema's fields and types. Two exceptions: a refusal, or a reply cut
  off at `max_tokens`, so check `stop_reason`. They don't guarantee the values are right, so still
  check the values in code
  ([structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs),
  Tier 1, checked 2026-10-12). The saved objective emphasizes schema-based tool output; compare the actual stated constraints and supported interface rather than memorize a universal answer. See
  [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).
- `tool_choice` is the request setting that says whether Claude must call a tool: `auto` = Claude
  decides (text allowed), `any` = it must call some tool, a named tool = it must call that one
  (full table: [Lesson 2, section 2.3](L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones)).
  It's the add-on to tool use, for when no tool gets called or one must run first (exam guide,
  task 4.3). Use `"any"` when there are several schemas and the document type is unknown. Force
  `{"type":"tool","name":"extract_metadata"}` to make it run first.
- Changed since the guide: on Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1, `any` and forced
  `tool` return a 400 error. Use `auto` with `strict: true` on the tool, or `output_config.format`,
  in real code. On the exam, keep `any` / forced
  ([tool use docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools),
  Tier 1; see [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
  Model names change; check the
  [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) (checked 2026-10-21).
- **Schema design:**
  - Make a field **nullable/optional** when the source may not have it, so the model doesn't
    invent a value to fill a required field.
  - Add **`"unclear"`** for ambiguous cases, and **`"other"` plus a detail string** for categories
    that need to grow.
  - Put format-normalization rules in the prompt as well as the schema.

## 4.4 Validate, retry, feed back

- **Retry with error feedback:** send back the original document, the failed extraction and the
  **specific** validation errors.
- **Retries don't help when the information isn't in the source**, for example when it's in an
  external document you didn't provide. They do help with format and structure errors.
- Self-checking fields: `calculated_total` next to `stated_total`, and a `conflict_detected` flag.
- A **`detected_pattern`** field lets you analyze false positives when developers dismiss findings.

## 4.5 Batch processing

**What a batch is.** Think of a laundry service. You drop off a big bag, you pay about half what
the express counter charges, and they promise it back within a day, but not at a set hour. You
can't stand at the counter while they wash, and they won't phone you mid-wash to ask a question.
The Message Batches API works the same way: you send many separate requests at once, Claude
works through them when it can, and you collect the results later.

**How it runs, in three steps.**

1. Submit one batch holding many requests, each with its own `custom_id`.
2. Check the batch's status now and then (polling) until it says it has ended. The guide lists
   "polling for completion" as a batch feature (exam guide, technologies list).
   Polling tells you *when* it's done; it doesn't promise *how soon*.
3. Download the results and match each one to its request by `custom_id`
   (exam guide, task 4.5).

Endpoint and field names for these steps are not printed in the guide: check the current docs
([Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing), Tier 1).

**The facts, in the guide's own words** (official wording):

- "The Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed
  latency SLA" (exam guide, task 4.5)
- Good for "non-blocking, latency-tolerant workloads (overnight reports, weekly audits, nightly
  test generation)" and "inappropriate for blocking workflows (pre-merge checks)"
  (exam guide, task 4.5)
- "The batch API does not support multi-turn tool calling within a single request (cannot execute
  tools mid-request and return results)" (exam guide, task 4.5). Caveat: batches do support tools,
  including server tools that Anthropic runs; what they can't do is pause for *your* code's tool (Anthropic docs, Message Batches, Tier 1, checked 2026-10-12).
- "custom_id fields for correlating batch request/response pairs" (exam guide, task 4.5)

"No guaranteed latency SLA" means no promised finish time. Each row is one question you might ask
about it; the right column answers it.

| Question | Answer |
| --- | --- |
| Where doesn't it fit? | **Blocking pre-merge checks**, which need the synchronous API (the normal Messages API: you send one request and wait for the reply) (exam guide, task 4.5) |
| How do I match results to requests? | **`custom_id`** on every request; resubmit only failed ids (exam guide, task 4.5) |

**Why no multi-turn tools.** A normal agentic loop goes: Claude asks for a tool (`stop_reason`
is `"tool_use"`), *your code* runs the tool, you send the result back, Claude continues. In a
batch, nobody is on the line. The batch can't pause, come back to your code to run the tool, and
pick up again. So any job that needs a tool loop (look something up, then decide) belongs on the
synchronous API. Server tools, which Anthropic runs, do work in a batch (Anthropic docs, Message Batches, Tier 1, checked 2026-10-12). A one-shot job, such as "extract these fields from this document", fits a batch.

**The 3-question decision test.**

1. **Is someone waiting on the answer?** A developer who can't merge, a customer in a chat, a
   pipeline step that blocks. If yes, use the synchronous API. Batch has no finish-time promise.
2. **Does your own code need to run a tool and send the result back partway through the request?**
   If yes, use the synchronous API. Tools that Anthropic runs (server tools) are fine in a batch.
3. **Does your deadline still hold if the batch hits 24 hours and you have to resend the expired
   requests?** If no, use the synchronous API.

Three "no, no, yes" answers mean batch it.

**SLA window math, worked.**

**Nominal budget: interval + processing window + recovery/validation time ≤ deadline. Under the saved 24-hour-window assumption, SLA − 24 is a ceiling, not proof of delivery;
pick an interval below it.** The margin is for the resubmit: a batch can end at 24 hours with requests
`expired` and no output, and those must be resent or run synchronously in time (Anthropic docs, Message Batches, Tier 1, checked 2026-10-12).

Your promise to the business: every document is processed within
30 hours of arriving. A batch can take up to 24 hours (exam guide, task 4.5).
The worst case for a document is: it arrives just after a submission, waits for the next one,
then that batch takes the full 24 hours.

- Worst case = submission interval + 24 hours. It must be 30 hours or less.
- So the ceiling is 30 − 24 = 6 hours. At exactly 6 there is no margin at all.
- The saved guide's **4-hour window** example illustrates nominal budgeting against a **30-hour target**, not a production delivery guarantee
  (exam guide, task 4.5): 4 + 24 = 28 hours worst case, which leaves
  two hours remaining. That does not prove recovery fits: a failed/expired request may require a measured synchronous fallback or explicit incomplete outcome; another batch can take up to 24 hours
  too; [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing),
  Tier 1.
- Try another: a 36-hour SLA: the ceiling is 12 hours, so submit every 8 hours or so to leave
  margin (see Drill 24 in [HARD-DRILLS.md](HARD-DRILLS.md)).

**Resubmit only the failures.** Each request carries a `custom_id` you choose, such as the
document's id. When results come back, match them by `custom_id`, not by order. Find the ones
that failed, fix the cause (for example, split documents that were too long for the context
window into chunks), and resubmit just those (exam guide, task 4.5). Don't
rerun the whole batch.

**Refine the prompt on a sample first,** then run the full volume. A better first pass means
fewer resubmissions (exam guide, task 4.5).

**Quick check (done when you can answer all three without looking):**

- (a) A 48-hour SLA: what is the ceiling, and what interval would you pick?
- (b) A nightly test-generation job that calls no tools: batch or synchronous?
- (c) 40 of 1,000 requests failed. What do you resubmit?

<details><summary>Answers</summary>

(a) Ceiling 24 hours; pick less, for example 20, to leave a margin. (b) Batch. (c) Only
the 40 failed `custom_id`s, after fixing the cause.

</details>

The batch traps are in the lesson's main [Traps](#traps) list below.

**Practise (about 10 min):** the batch module [Objective 4.5](objectives/objective-4.5.md) under
[Objective modules](#objective-modules), then the 4.5 cards in
[FLASHCARDS.md](FLASHCARDS.md#45-design-efficient-batch-processing-strategies).

## 4.6 Multi-instance and multi-pass review

- A model reviewing its own work in the same session keeps its reasoning and is less likely to
  question it. An **independent instance** does better than "review your work" or extended thinking
  (letting Claude reason step by step before answering).
- **Multi-pass:** per-file passes for local issues, plus a cross-file integration pass for data
  flow.
- A verification pass where each finding has **its own confidence** lets you route reviews by
  confidence.

## Worked example

An extraction model sometimes fills `invoice_date` with a made-up date on invoices that don't have
one. **Answer:** make `invoice_date` nullable (and add few-shot examples of documents without a
date). Retries or "never make things up" in the prompt don't solve it, because the model is filling
a *required* field.

## Traps

- "Add 'be conservative' to the review prompt."
- "JSON mode (just asking for JSON in the prompt), or asking nicely, guarantees the schema."
  The saved guide describes schema-based output (wording: "eliminating JSON syntax errors"); verify strict-mode support and exceptional outcomes for actual enforcement,
  never the meaning.
- "Use batches for the pre-merge check to save money."
- "Retry until it finds the missing field."
- **Batch traps (4.5):**
  - "Batch everything to save 50%." Wrong whenever someone is waiting on the answer.
  - "Polling or a fallback timer makes batch safe for blocking work." Neither creates a promised
    finish time; pick the synchronous API for blocking steps.
  - "Batch can't work because results come back unordered." Match results by `custom_id`.
  - "Batch an agent that calls tools step by step." Batch can't run tools mid-request.
  - "Resubmit the entire batch after some failures." Resubmit only the failed `custom_id`s,
    adjusted.
  - "Submit every 24 hours for a 30-hour SLA." Worst case is 48 hours. SLA − 24 is the ceiling;
    pick an interval below it.
  - (All exam guide, task 4.5.)

## Try it (60 min), lab 02: the agent loop, subagents and extraction lab, extraction part

Define an `extract_invoice` tool with nullable fields, an `unclear` enum and
`calculated_total`/`stated_total`. In code today, use `tool_choice: auto` with `strict: true` on
the tool (on Opus 5.5 and Sonnet 5.5, forcing returns 400). On the exam, the answer is tool use
with a JSON schema; forcing it with `tool_choice` is the add-on when Claude skips the tool. Check that the reply is a `tool_use` block; `auto` can still
answer in text. Validate the result in code, and retry once with the specific
errors.

Done when a document with no date returns `invoice_date: null`, and one retry fixes a deliberately
wrong total.

## Done when

- [ ] You can explain the difference between syntax and semantic errors
- [ ] Given a field missing from the source, a date in the wrong format and a total that doesn't add
  up, you can say which ones a retry fixes (only the format one, and the total if the source has
  the right numbers)
- [ ] You know batch facts (50%, 24 hours, no client-side tool loop, `custom_id`) and can do the SLA math
- [ ] You scored 80% or more on [CCAR-F practice — choose Domain 4](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)

**Go deeper:**

- **Deep practice:** [Deep practice 4](deep-practice/04-prompt-engineering-and-structured-output.md), which takes every section of this lesson further.
- **Official course:** the prompting and structured-output parts of the official course *Building with the Claude API* from the [CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) (Anthropic, Tier 1, checked 2026-10-02).
- **Flashcards and drills:** the Domain 4 section of the [flashcards](FLASHCARDS.md) and the 8 Domain 4 drills (20–25, 39, 40) in [HARD-DRILLS.md](HARD-DRILLS.md).
- **Charts:** decision charts [1 Batch or synchronous](deep-practice/decision-charts.md#1-batch-api-or-synchronous-calls), [1b Running a batch](deep-practice/decision-charts.md#1b-running-a-batch-when-to-submit-what-to-resend), [2 Which `tool_choice`](deep-practice/decision-charts.md#2-which-tool_choice-setting) and [12 Schema, retry or a check in code](deep-practice/decision-charts.md#12-the-output-is-wrong-schema-retry-or-a-check-in-code); sequence diagrams [5 Message Batches](deep-practice/sequence-diagrams.md#5-message-batches-how-do-you-get-results-and-resend-failures) and [Tree B, noisy review comments](deep-practice/sequence-diagrams.md#tree-b-review-comments-are-noisy-or-uneven-which-prompt-fix).

**Next:** [Deep practice 4](deep-practice/04-prompt-engineering-and-structured-output.md), then [Lesson 3](L03-claude-code-configuration-and-workflows.md).

## Sources

- Official exam guide v1.0, task statements 4.1–4.6, including the 4-hour batch example (Tier 1).

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  docs (Tier 1).
- [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing) docs
  (Tier 1).
- A colleague's debrief (tier F): emphasis only.

## Objective modules

For deeper learning and a separate practice/completion check for each objective:

- [Objective 4.1](objectives/objective-4.1.md)
- [Objective 4.2](objectives/objective-4.2.md)
- [Objective 4.3](objectives/objective-4.3.md)
- [Objective 4.4](objectives/objective-4.4.md)
- [Objective 4.5](objectives/objective-4.5.md)
- [Objective 4.6](objectives/objective-4.6.md)

## Decisions in this domain

| Objective | Decision variant and exact repair |
| --- | --- |
| 4.1 | [FV-19 — Define a finding with evidence criteria](objectives/objective-4.1.md#variant-fv-19) |
| 4.2 | [FV-20 — Teach the edges with representative examples](objectives/objective-4.2.md#variant-fv-20) |
| 4.3 | [FV-21 — Validate shape and truth separately](objectives/objective-4.3.md#variant-fv-21) |
| 4.4 | [FV-22 — Repair the failed check within a budget](objectives/objective-4.4.md#variant-fv-22) |
| 4.5 | [FV-23 — Choose batch by dependencies and deadline](objectives/objective-4.5.md#variant-fv-23) |
| 4.6 | [FV-24 — Give the critic independent evidence](objectives/objective-4.6.md#variant-fv-24) |

**Interpret local practice targets:** any 80% target above is an optional project study heuristic, not a validated mastery threshold or conversion to the official scaled score. Use fresh decisions, explanations and delayed transfer alongside remaining objective gaps.