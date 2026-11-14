# CCAR-F SIM-07 — Scenario 6: Structured Data Extraction

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

### Stage 1 — The handoff parses, but the invoice is wrong

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

**Objective connections:** [4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md), [4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md).

### Stage 2 — Ten thousand files finish with mixed outcomes

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

**Objective connections:** [4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.5.md), [4.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.6.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** A document arrives as prose, a table or another unstructured layout, while the receiving business system needs a usable record. The expected output preserves supported information, handles awkward cases and makes unresolved data visible. This simulation explores the extraction, validation and review decisions between document and record.

**Build the application picture first:** [AS 02 document pipeline](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-02-document-pipeline.md) · [AS 07 work queue](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-07-work-queue.md) · [AS 08 resumable case](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-08-resumable-case.md)

**Primary domains:** 4 Prompting and Structured Output, 5 Context and Reliability ·
**Decisions:** 11 · **Time:** 20 min for the decisions, plus about 5 for the twist and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 6, Tier 1)

You're building a structured data extraction system with Claude. It pulls information out of
unstructured documents, **validates the output against JSON schemas** and keeps accuracy high. It
must handle edge cases gracefully and feed downstream systems.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. What's the most reliable way to get output that matches your schema?
2. The document type is unknown and there are 3 extraction schemas. Answering the way the exam
   guide describes it, how do you set `tool_choice`?
3. Metadata must be extracted before enrichment. Answering the way the exam guide describes it,
   how do you make sure it happens first?
4. The model invents dates for documents that don't have one. What do you change?
5. A document's category doesn't fit any enum value. What should the schema allow?
6. The line items don't add up to the stated total. How do you catch and fix it?
7. A required PO number exists only in an attachment you didn't send. What do you do?
8. Documents arrive all day, about 50,000 a week, and each one's results are due within 30 hours
   of when it arrives. How do you plan the processing?
9. On a 500-document test set the system scores 96% accuracy, but 80% of that set is utility
   bills. The operations lead now wants to stop human review of insurance claim forms too. What do
   you check first?
10. Reviewers can check only about 1 in 10 extractions. The extraction tool can return a
    confidence score for each field. How do you decide which extractions a human sees?
11. The required `payment_terms` field comes back empty on about 1 in 5 supplier contracts, but
    a person finds the terms in every one. Some contracts have a payment clause. Others hide the
    terms in a fee-table footnote or a schedule at the back. You already added detailed
    instructions on where terms can appear, and results are still patchy. What do you change?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | The most reliable way to get output that matches the schema | **Tool use with a JSON schema** as the tool's input. On the exam, this is the answer. Today, also add `strict: true` to the tool to enforce the shape; the shape holds unless the reply is a refusal or is cut off at `max_tokens`, so check `stop_reason` (Structured outputs docs, Tier 1, checked 2026-10-12); see [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | "Respond in JSON" in the prompt; a regex fixer on the output; a bigger model | D4 4.3 Structured output via tool use | [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 2 | The document type is unknown and there are 3 extraction schemas | **`tool_choice: "any"`**. Also accept `tool_choice: "auto"` with `strict: true` on all three tools plus a check that the reply is a `tool_use` block (strict fixes the shape but doesn't force a call), or structured outputs with one schema that covers all three document types, as right for today's product, where `any` returns a 400 error on the newest models; on the exam, pick `"any"`. See [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | `"auto"`, which lets it reply in plain text; forcing one tool; three separate calls, one per schema, keeping whichever parses | D4 4.3 Structured output via tool use | [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 3 | Metadata must be extracted before enrichment | **Force `{"type":"tool","name":"extract_metadata"}`**, then do the rest in later turns. Also accept "a first request that returns the metadata through structured outputs (`output_config.format`), then enrichment in later turns" as right for today's product, where a forced tool returns a 400 error on the newest models; on the exam, pick forced tool selection. See [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | Ask for it first in the prompt; leave `tool_choice` on `"auto"` and hope; a longer prompt explaining why order matters | D2 2.3 Tool distribution and tool_choice; D4 4.3 Structured output via tool use | [Lesson 2, section 2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md), [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 4 | The model invents dates for documents that don't have one | **Make the field nullable/optional** | "Never make things up" in the prompt; retry until a date looks right; fill a default such as 1970-01-01 | D4 4.3 Structured output via tool use | [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 5 | A category doesn't fit the enum | Add **`"other"` plus a detail string**, and **`"unclear"`** | Force the closest enum value; drop the enum for free text; a longer prompt describing each category | D4 4.3 Structured output via tool use | [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 6 | The line items don't add up to the total | **A semantic check in code:** `calculated_total` against `stated_total`, then **retry with the specific error** | Trust the schema, since tool use guarantees it; ask the model to "double-check the arithmetic"; add `minimum: 0` to every amount in the schema, though a schema checks each amount, never whether they add up | D4 4.3 Structured output via tool use; D4 4.4 Validation and retry loops | [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md), [Lesson 4, section 4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 7 | A required PO number exists only in an attachment you didn't send | **Don't retry.** Send it for review, or get the attachment. | Retry 3 times with the error; ask the model to infer it from the invoice number; make the field optional and pass the record on silently | D4 4.4 Validation and retry loops | [Lesson 4, section 4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 8 | About 50,000 documents a week arrive all day; each is due within 30 hours of arrival | **Submit a batch about every 4 hours, below the 6-hour ceiling (30 − 24), so the worst case is 28 hours, a 2-hour safety margin.** Refine the prompt on a sample first, and resubmit failures by `custom_id` | Synchronous calls for every document, at double the cost; start sending full volume before testing the prompt on a sample; one batch a day, where a document that arrives just after a submission waits about 24 hours, then up to 24 more in the batch | D4 4.5 Batch processing | [Lesson 4, section 4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 9 | 96% on a test set that's 80% utility bills; the lead wants to drop review of claim forms too | **Check accuracy by document type and by field**, since the average hides the claim forms, and use stratified sampling of high-confidence results | Drop review now, because 96% is high; review only the low-confidence results; retest on a bigger sample of the same utility-heavy mix | D5 5.5 Human review and confidence calibration | [Lesson 5, section 5.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 10 | Deciding which extractions a human sees | **Field-level confidence calibrated on a labeled set.** Send low-confidence or contradictory ones to humans. | The model's overall "I'm sure" rating; a fixed 0.9 cut-off on scores nobody has calibrated; review only the documents that took longest to process | D5 5.5 Human review and confidence calibration | [Lesson 5, section 5.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 11 | `payment_terms` comes back empty on 1 in 5 contracts because the terms sit in different layouts | **Add 2–4 few-shot examples, one per layout**: a short excerpt with a payment clause, one with the terms in a fee-table footnote, one with them in a schedule, each showing the correct extracted value. Add one where the terms truly aren't there, so null stays reserved for real absence. Examples of varied formats teach the model to find the field in layouts it hasn't seen, which instructions alone didn't. | Make the field non-nullable so the model must fill it: forces a value, so it may invent terms for the few contracts that lack them (see decision 4); write even longer instructions listing every place terms might hide: instructions already failed to give consistent results, and more of them won't; add one example for every supplier template you have: too many to maintain, and it teaches matching known layouts instead of generalizing to new ones | D4 4.2 Few-shot prompting | [Lesson 4, section 4.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |

**Scoring:** 9 or more is a pass. Decisions 4, 6 and 7 are where people usually go wrong: a schema
fixes the syntax, not the facts.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 6 and task statements 2.3, 4.2–4.5, 5.5 (Tier 1); Claude API docs on tool use and Message
Batches at platform.claude.com (Tier 1). Taught in lessons
[L02](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md),
[L04](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md)
and [L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: dates arrive in mixed formats

**What changed:** the schema says `invoice_date` is a string, and every output passes the schema.
But the dates come back as "03/04/2026", "4 March 2026" and "2026-03-04", and the downstream
system needs one format.

**Question:** what do you change?

<details><summary><b>Answer and why</b></summary>

**Add format rules to the prompt next to the strict schema**, for example "write every date as
YYYY-MM-DD; these suppliers write the day first", with a short example. The schema makes sure
there is a string; the prompt rule tells the model how to read the source and how to write it.

**Why the others lose:** the strongest wrong move is putting a date pattern in the schema alone.
A pattern forces the shape YYYY-MM-DD, but it can't tell the model how to read "03/04/2026"
(March 4 or April 3?), so you can still get a well-shaped wrong date. Trusting the plain string
schema fails because every format is a valid string. A regex clean-up downstream has to guess
what "03/04" means after the model, which saw the document, could have told you. Dropping the
date field loses data the business needs.

**Tests:** Domain 4, task statement 4.3 (structured output via tool use).

**Lesson:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use) · [Deep practice, Domain 4](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/04-prompt-engineering-and-structured-output.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 4.3 (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: the most reliable way to match the schema**

- **What's going on:** every answer has to come back in exactly the same shape.
- **Under the hood:** a tool's `input_schema` (its input rules) is your schema; the `tool_use` block (Claude's tool call) holds the data. On the exam, tool use is the answer. Today, add `strict: true` to enforce the shape (the shape holds unless the reply is a refusal or is cut off at `max_tokens`, so check `stop_reason` (Structured outputs docs, Tier 1, checked 2026-10-12)); without it, a type or required field can still be off.
- **How to make the call:** if code downstream needs fixed fields, define an extraction tool with your schema and read the data from the `tool_use` block; if only a person reads the answer, prose is fine. Exam wording (task statement 4.3): "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors".
- **Why the tempting answers are wrong:**
  - **"Respond in JSON" prompt:** a request; the syntax can still break.
  - **Regex fixer:** repairs afterwards and guesses.
  - **A bigger model:** better guesses, no guarantee.
- **Go deeper:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use)

**Decision 2: unknown document type, three schemas**

- **What's going on:** three forms; which one fits is unknown.
- **Under the hood:** `tool_choice` (the tool-call setting) has three modes the exam tests (a fourth, `"none"`, turns tools off). `"auto"` allows a plain-text answer. `"any"` makes it call a tool of its choice. Forcing names the one tool to call.
- **How to make the call:** if it must call a tool but should pick which, use `"any"`; if one specific tool must run, force it; if text is fine, use `"auto"`. Exam wording (task statement 4.3): "Setting tool_choice: "any" to guarantee structured output when multiple extraction schemas exist and the document type is unknown". On the exam, `"any"`. Today that's a 400 error on the newest models; use `"auto"` with `strict: true` and check a tool was called ([exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
- **Why the tempting answers are wrong:**
  - **Leave it on `"auto"`:** may reply in text.
  - **Force one tool:** wrong schema for other types.
  - **Three calls, keep one:** triple cost; a wrong schema may parse.
- **Go deeper:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use)

**Decision 3: metadata must come before enrichment**

- **What's going on:** one step must happen first, every time.
- **Under the hood:** forcing `{"type":"tool","name":"extract_metadata"}` in `tool_choice` makes that response call that tool. Later turns use a different `tool_choice` so the enrichment tools can run.
- **How to make the call:** if a step must always run first, force that tool on the first request, then change `tool_choice` after; if order doesn't matter, don't force anything. Exam wording (task statement 2.3): "Using tool_choice forced selection to ensure a specific tool is called first (e.g., forcing extract_metadata before enrichment tools), then processing subsequent steps in follow-up turns". On the exam, force it. Today that returns a 400 error on the newest models; get the metadata first with structured outputs (`output_config.format`), then enrich in later turns ([exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
- **Why the tempting answers are wrong:**
  - **Prompt it first:** a request; order isn't guaranteed.
  - **`"auto"` and hope:** may skip or reorder it.
  - **Explain why order matters:** still just a request.
- **Go deeper:** [Lesson 2, section 2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones), [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use)

**Decision 4: the model invents dates**

- **What's going on:** the form demands a date, so the model makes one up.
- **Under the hood:** a `required` field (one that must be filled) has to get a value to fit the schema. With no value in the document, the model guesses. A nullable field (one allowed to be `null`, meaning empty) gives it an honest way out. Nullable only handles missing values: a wrong non-null value still passes the schema, so keep a semantic check in code (Anthropic docs, Structured outputs, Tier 1, checked 2026-10-12).
- **How to make the call:** if some documents may not have the value, make the field nullable or optional; if every document always has it, required is fine. Exam wording (task statement 4.3): "Designing schema fields as optional (nullable) when source documents may not contain the information, preventing the model from fabricating values to satisfy required fields".
- **Why the tempting answers are wrong:**
  - **"Never make things up":** the schema still demands a value.
  - **Retry until it looks right:** there's no date to find.
  - **A default like 1970-01-01:** a fake date that looks real.
- **Go deeper:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use)

**Decision 5: the category isn't in the enum**

- **What's going on:** the list of choices is missing the right box.
- **Under the hood:** an `enum` (a fixed list of allowed values) forces one listed value. With nothing that fits, the model picks the nearest wrong one. `"other"` plus a detail string, and `"unclear"`, give it honest choices.
- **How to make the call:** if new categories can appear, add `"other"` with a detail field; if documents can be ambiguous, add `"unclear"`; if the list is truly complete and documents are clear, keep it as is. Exam wording (task statement 4.3): "Adding enum values like "unclear" for ambiguous cases and "other" + detail fields for extensible categorization".
- **Why the tempting answers are wrong:**
  - **Force the closest value:** quietly wrong data.
  - **Free text instead:** downstream systems can't group it.
  - **Longer category descriptions:** still no box for new ones.
- **Go deeper:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use)

**Decision 6: the line items don't add up**

- **What's going on:** the form is filled in neatly, but the maths is wrong.
- **Under the hood:** a schema checks each field's shape and type, never whether fields agree. Your code compares `calculated_total` with `stated_total`. On a mismatch, it retries with the document, the failed extraction and the specific error.
- **How to make the call:** if values must agree with each other, check that in code, and on a mismatch retry with the exact error; if the problem is shape or type, the schema already covers it. Exam wording (task statement 4.3): "That strict JSON schemas via tool use eliminate syntax errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in wrong fields)".
- **Why the tempting answers are wrong:**
  - **Trust the schema:** it checks shape, not sums.
  - **"Double-check the arithmetic":** a request; nothing checks it.
  - **`minimum: 0` everywhere:** checks each amount, not the total.
- **Go deeper:** [Lesson 4, section 4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use), [Lesson 4, section 4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#44-validate-retry-feed-back)

**Decision 7: the PO number is in an attachment you didn't send**

- **What's going on:** you're asking for something that isn't in what you sent.
- **Under the hood:** a retry with the error message fixes format and structure mistakes, because the right answer is in the input. It can't create a fact the input doesn't hold; the model can only guess.
- **How to make the call:** if the value is in the document but came out wrong, retry with the error; if it isn't in what you sent, don't retry: get the attachment or send the record to human review. Exam wording (task statement 4.4): "Identifying when retries will be ineffective (e.g., information exists only in an external document not provided) versus when they will succeed (format mismatches, structural output errors)".
- **Why the tempting answers are wrong:**
  - **Retry 3 times:** same input, same gap.
  - **Infer from invoice number:** a guess dressed up as data.
  - **Optional, pass it on:** nobody sees the gap.
- **Go deeper:** [Lesson 4, section 4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#44-validate-retry-feed-back)

**Decision 8: documents arrive all day, each due within 30 hours**

- **What's going on:** a steady stream, a deadline, and a cheap but slow lane.
- **Under the hood:** a batch costs half, but can take up to 24 hours. If a document waits at most 4 hours for the next submission, then up to 24 in the batch, it's done within 28 hours.
- **How to make the call:** if documents keep arriving and each is due 30 hours after arrival, then submit about every 4 hours: 30 − 24 = 6 is the ceiling, and staying below it leaves a safety margin; if you wait longer than 6, some documents miss the deadline. Resend failures by `custom_id`. Exam wording (task statement 4.5): "Calculating batch submission frequency based on SLA constraints (e.g., 4-hour windows to guarantee 30-hour SLA with 24-hour batch processing)".
- **Why the tempting answers are wrong:**
  - **Synchronous calls for all:** double the cost.
  - **Untested full volume:** a prompt flaw hits everything.
  - **One batch a day:** up to 24 hours waiting plus 24 processing passes 30.
- **Go deeper:** [Lesson 4, section 4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#45-batch-processing)

**Decision 9: 96% accuracy on a test set that's mostly utility bills**

- **What's going on:** a great average can hide one bad type of document.
- **Under the hood:** with 80% utility bills, the overall number mostly measures bills. Claim forms are a small slice, so their accuracy barely moves the average. Only numbers split by document type and by field show it.
- **How to make the call:** before cutting human review for any document type, check accuracy for that type and each of its fields; if it holds, keep stratified sampling (random checks drawn from each group) of high-confidence results. Exam wording (task statement 5.5): "Analyzing accuracy by document type and field to verify consistent performance across all segments before reducing human review".
- **Why the tempting answers are wrong:**
  - **Drop review now:** the 96% is mostly bills.
  - **Review only low-confidence results:** confident mistakes on claim forms slip through.
  - **Bigger test set, same mix:** the same bills-heavy average.
- **Go deeper:** [Lesson 5, section 5.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#55-human-review-and-confidence)

**Decision 10: deciding which extractions a human sees**

- **What's going on:** reviewers are few, so send them the riskiest fields.
- **Under the hood:** the model can give a confidence number for each field, but raw numbers can't be trusted until checked against a labeled set (documents with known right answers). Calibrating shows which cut-off really separates right from wrong.
- **How to make the call:** if field-level confidence has been calibrated on labeled data, send low-confidence fields and contradictory documents to people; if it hasn't been calibrated, calibrate it first. Exam wording (task statement 5.5): "Field-level confidence scores calibrated using labeled validation sets for routing review attention".
- **Why the tempting answers are wrong:**
  - **One overall "I'm sure" rating:** hides which fields are often wrong.
  - **A fixed 0.9 cut-off:** nobody checked what 0.9 means.
  - **Slowest documents first:** time taken doesn't track errors.
- **Go deeper:** [Lesson 5, section 5.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#55-human-review-and-confidence)

**Decision 11: `payment_terms` comes back empty on 1 in 5 contracts**

- **What's going on:** the terms are always there, just hidden in different places.
- **Under the hood:** instructions describe where to look; examples show it. Seeing a clause, a footnote and a schedule each extracted correctly lets the model handle layouts it hasn't seen before.
- **How to make the call:** if detailed instructions still miss a field across varied layouts, add 2–4 short examples, one per layout, each with the correct value, plus one where the terms are truly absent and the answer is null; if instructions alone already get it right, skip the examples. Exam wording (task statement 4.2): "Adding few-shot examples showing correct extraction from documents with varied formats to address empty/null extraction of required fields".
- **Why the tempting answers are wrong:**
  - **Make it non-nullable:** forces invented terms where none exist.
  - **Even longer instructions:** instructions already failed.
  - **One example per supplier template:** too many to maintain; matches layouts instead of generalizing.
- **Go deeper:** [Lesson 4, section 4.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#42-few-shot-examples)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-01, the full mock](SIM-01-full-mock.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-19 — decision checkpoint

The policy owner cannot say whether conditional pass-through costs count as prohibited fees. Which next step fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Request the missing policy interpretation or label those cases unresolved before classifying them. An unresolved business definition cannot be repaired by confident model wording.

**Base choice:** A legal clause review flags only an explicit unilateral termination right without the fictional required notice. Provide threshold, exclusions and source locator expectations.

**Changed constraint and recovery:** The policy wording is ambiguous about mutual termination. Ask for clarification or label the case uncertain instead of treating every termination mention as a violation.

**Failure:** False positives cluster around historical examples. Add the exclusion and test borderline cases against actual text.

**Nearest alternative:** “Be careful” does not operationalize the criterion. A longer prompt without measurable boundaries can preserve the same errors.

**Conditional cue:** Name trigger, exclusion and evidence before flagging.

**Proof:** Inspect `finding_rule={trigger:unilateral_right,required:notice,evidence:clause_locator,exclude:historical_example}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.1.md#variant-fv-19).

</details>

### SIM-FV-20 — decision checkpoint

A new market introduces a promotion structure absent from the original examples; held-out results show systematic mistakes. What should the team do?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Revise or add examples for the changed distribution and evaluate on a separate held-out set. Distribution change needs evidence-driven example revision and independent measurement.

**Base choice:** A finance extraction prompt includes ordinary invoices, absent tax IDs and source conflicts, with explanations of allowed nulls and unresolved values.

**Changed constraint and recovery:** A new document population uses credit notes and negative amounts. Revise the example distribution and validate on unseen cases.

**Failure:** All examples are clean positive invoices; the model invents rare fields. Add realistic counterexamples rather than simply adding more clean examples.

**Nearest alternative:** Few-shot consistency is not a factual guarantee. Examples should represent the relevant error modes, not leak held-out answers.

**Conditional cue:** Examples teach boundaries; holdouts test transfer.

**Proof:** Inspect `examples=[ordinary,missing_field,conflict,credit_note]; holdout=unseen_edge_cases` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.2.md#variant-fv-20).

</details>

### SIM-FV-21 — decision checkpoint

Another invoice explicitly states PO-782, but the schema-valid output says PO-728. What validation fixes this defect?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Compare the field against source evidence and correct the non-null value through semantic validation. The wrong value has valid shape but conflicts with the source.

**Base choice:** Use supported strict schema enforcement for an extraction tool, then independently validate source evidence and arithmetic. Tool selection, structural conformance and semantic validity are separate checks.

**Changed constraint and recovery:** A field truly absent from the source may be null only when the declared contract allows it. A wrong non-null amount does not call for a nullable-only repair.

**Failure:** The JSON is well typed but says 900 where the source says 90. Reject the semantic mismatch and return the exact failed check.

**Nearest alternative:** Forcing a tool call does not prove schema adherence unless the applicable mechanism enforces it; even conforming output can be wrong.

**Conditional cue:** Call, shape, truth: three proofs, not one.

**Proof:** Inspect `candidate={amount:900,currency:USD}; source={amount:90}; shape=pass; source_match=fail` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md#variant-fv-21).

</details>

### SIM-FV-22 — decision checkpoint

After the allowed correction attempts, two source pages still disagree about the invoice total. What should happen?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Keep the discrepancy unresolved and escalate with source evidence and attempt history. Persistent source conflict cannot be resolved by inventing agreement.

**Base choice:** An invoice candidate’s subtotal plus tax differs from total. Return the precise values, source locators and failed arithmetic check for a bounded correction.

**Changed constraint and recovery:** The source itself contains contradictory totals. Preserve both values and route review instead of asking Claude to manufacture reconciliation.

**Failure:** The retry budget is exhausted. Escalate with source, previous outputs, failed checks and unresolved discrepancy.

**Nearest alternative:** Retrying the whole document without diagnostic feedback can repeat the error or mutate correct fields.

**Conditional cue:** Repair the named failure; stop when evidence cannot resolve it.

**Proof:** Inspect `failed_check={subtotal:80,tax:8,total:100,expected:88}; retry_budget=2; status=unresolved` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md#variant-fv-22).

</details>

### SIM-FV-24 — decision checkpoint

A low-risk internal formatting task has an exact deterministic validator; no substantive conclusion is produced. What review approach is proportionate?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Use the deterministic validator and bounded human or automated spot checks appropriate to the low risk. Additional model passes need to justify their cost and failure exposure for this bounded task.

**Base choice:** A producer proposes extracted claims; a separate critic checks source locators, omissions and contradictions under explicit criteria. Resolve disagreement by evidence.

**Changed constraint and recovery:** A simple low-risk formatting task has deterministic validation. Extra model passes may not justify their cost.

**Failure:** Both instances share a misleading summary and agree. Give the critic original sources or a different check; agreement alone is not validation.

**Nearest alternative:** Repeated identical prompts can amplify the same blind spot. Independence needs evidence and criteria, not just another instance.

**Conditional cue:** Separate the reviewer’s evidence; resolve with the source.

**Proof:** Inspect `producer={claims,sources}; critic={criteria,original_sources,failed_checks}; dispute={claim,source,verdict}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.6.md#variant-fv-24).

</details>

### SIM-FV-29 — decision checkpoint

The routing team has calibrated scores but reviewer demand exceeds daily capacity; a published policy forbids silently dropping flagged claims. What is required?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Define and test a capacity and overflow policy with observable escalation for unresolved review demand. A review design must specify what happens when its required human queue exceeds capacity.

**Base choice:** A finance extractor has high overall accuracy but weaker rare-currency performance. Evaluate severity-weighted slices on independent holdout and calibrate review thresholds with actual human capacity.

**Changed constraint and recovery:** A review queue exceeds available capacity. Apply a declared overflow policy or reduce scope; do not silently accept low-confidence items.

**Failure:** Distribution drift breaks calibration. Recalibrate on suitable data and evaluate on a separate holdout; do not tune against the final test set.

**Nearest alternative:** The average can hide dangerous categories; confidence scores alone are not calibrated correctness probabilities.

**Conditional cue:** Average, slice, severity, capacity: check all four.

**Proof:** Inspect `metrics={overall:0.98,rare_currency:0.70}; capacity=20; queued=35; overflow=hold` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.5.md#variant-fv-29).

</details>


<span data-assessment-exposure="cct-fv-19-base-v1,cct-fv-19-retry-v1,cct-fv-20-base-v1,cct-fv-20-retry-v1,cct-fv-21-base-v1,cct-fv-21-retry-v1,cct-fv-22-base-v1,cct-fv-22-retry-v1,cct-fv-24-base-v1,cct-fv-24-retry-v1,cct-fv-29-base-v1,cct-fv-29-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-19 — Define a finding with evidence criteria](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.1.md#variant-fv-19) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.1&variant=FV-19)
- [FV-20 — Teach the edges with representative examples](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.2.md#variant-fv-20) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.2&variant=FV-20)
- [FV-21 — Validate shape and truth separately](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md#variant-fv-21) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.3&variant=FV-21)
- [FV-22 — Repair the failed check within a budget](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md#variant-fv-22) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.4&variant=FV-22)
- [FV-24 — Give the critic independent evidence](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.6.md#variant-fv-24) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.6&variant=FV-24)
- [FV-29 — Test risk slices and review capacity](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.5.md#variant-fv-29) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.5&variant=FV-29)

**Build the mechanism:** [Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.