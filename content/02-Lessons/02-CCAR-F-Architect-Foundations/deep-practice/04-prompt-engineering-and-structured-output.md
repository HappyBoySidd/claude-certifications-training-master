# Deep practice 4: prompt engineering and structured output

**Picture the application:** An invoice reader must turn a messy document into fields another program can consume, while a code reviewer must return useful findings instead of noise. Start with the source and the required output. The sections below distinguish instructions, examples, output structure and evidence validation in those workflows.

This page covers Domain 4 of CCAR-F, prompt engineering and structured output, one task statement at a time. It goes
deeper than [Lesson 4](../L04-prompt-engineering-and-structured-output.md): each section gives the core idea, how it works under the hood,
the look-alike wrong answers, a worked example and a one-line exam reflex. Read the lesson first.
Objective lessons for this page: [2.3](../objectives/objective-2.3.md) · [4.1](../objectives/objective-4.1.md) · [4.2](../objectives/objective-4.2.md) · [4.3](../objectives/objective-4.3.md) · [4.4](../objectives/objective-4.4.md) · [4.5](../objectives/objective-4.5.md) · [4.6](../objectives/objective-4.6.md) · [5.5](../objectives/objective-5.5.md).

Domain 4 is 20% of the exam. Sections 4.1 to 4.6 come first, in number order. Two sections from other
domains come last, 2.3 (`tool_choice`) and 5.5 (confidence routing), because they live in the same
extraction scenario. Builds on
[L04](../L04-prompt-engineering-and-structured-output.md).
Citation keys like `[SO]` are listed at the bottom.

## Exam answer vs today's docs (read this once, then trust the exam column)

The exam guide is from July 2026. Some API behaviour changed after it. **On the exam, pick the
exam's answer.** In real code, use today's.

| Topic | Exam's expected answer | What changed since (one line; details in the notes below) |
|---|---|---|
| Guarantee a tool call | `tool_choice: {"type": "any"}` or `{"type": "tool", "name": "..."}` [Guide 4.3, 2.3] | The newest models return `400` for forced `tool_choice` (note 1). |
| Most reliable structured output | "Tool use (tool_use) with JSON schemas" [Guide 4.3] | The docs add JSON outputs as a second schema-guaranteed feature next to strict tool use (note 2). |
| Prefill the reply with `{` | A weak method, below tool use | Confirmed: prefill returns `400` on Claude 4.6 and later models (note 3). |

**On the exam: pick tool use with a JSON schema** for output that must match the schema [Guide 4.3]. An option worded "strict JSON schemas via tool use" is the same answer, because the guide uses "strict" for this same mechanism. Add `tool_choice` only when the problem is that no tool gets called: `any` for several schemas or an unknown document type, a named tool when one extraction must run first. `strict: true` and `output_config.format` are today's notes, not exam discriminators. The full list is in [exam answer vs today](conditions-and-errors.md#exam-answer-vs-today).

Notes (read once; you don't need them on the exam):

1. On Claude Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1, `any` and `tool` "return a 400 error".
   Forced tool use also errors with manual extended thinking (`thinking: {type: "enabled"}`). The docs
   say use `auto` with strict tool use, or structured outputs, instead [Tools], [Errors].
2. JSON outputs (`output_config.format`) and strict tool use (`strict: true`) [SO]. Without strict mode,
   "Claude might return incompatible types (`"2"` instead of `2`) or omit required fields" [Strict].
3. "Starting with Claude 4.6 models and Claude Mythos Preview ... Requests with prefilled assistant
   messages to these models return a 400 error" [Prompting]. The error is `400` `invalid_request_error`,
   "This model does not support assistant message prefill. The conversation must end with a user
   message." [Errors]. JSON outputs are also incompatible with prefill [SO].

---

## 4.1 Explicit criteria to cut false positives

Lesson: [L04 section 4.1](../L04-prompt-engineering-and-structured-output.md#41-explicit-criteria-reduce-false-positives) · Objective: [4.1](../objectives/objective-4.1.md)

**Exam wording:** `Task Statement 4.1: Design prompts with explicit criteria to improve precision and reduce false positives` [Guide]

### Core idea

"Be careful" doesn't help. Say exactly what counts as a problem and what doesn't.

### Under the hood

- Explicit beats vague. Exam example: "flag comments only when claimed behavior contradicts actual
  code behavior" vs "check that comments are accurate" [Guide 4.1].
- "be conservative" or "only report high-confidence findings" **fail** to improve precision compared
  to "specific categorical criteria" [Guide 4.1].
- Write report vs skip lists: report bugs and security issues; skip minor style and local patterns
  [Guide 4.1].
- Define each severity level with a concrete code example [Guide 4.1].
- False positives destroy trust in the *accurate* categories too. Fix: "Temporarily disabling high
  false-positive categories to restore developer trust while improving prompts for those categories"
  [Guide 4.1].

### Look-alikes

- **"Only report findings you are 90% confident about."** Confidence filtering; the guide names it as
  the weak fix.
- **"Add 'be conservative' to the prompt."** Vague.
- **"Keep all categories on so nothing is missed."** The noisy category is eroding trust in the rest.

### Worked example (scenario: Claude Code for continuous integration)

PR review comments: developers ignore them because 60% of "documentation" findings are nitpicks.
Turn off the documentation category for now. Rewrite it as "flag only when a docstring states a
parameter, return type or behaviour that the code contradicts", with one example per severity. Turn
it back on when its false-positive rate is low.

**Exam reflex:** *Replace "be careful" with report/skip categories and per-severity examples. Mute
the noisiest category while you fix it.*

---

## 4.2 Few-shot prompting

Lesson: [L04 section 4.2](../L04-prompt-engineering-and-structured-output.md#42-few-shot-examples) · Objective: [4.2](../objectives/objective-4.2.md)

**Exam wording:** `Task Statement 4.2: Apply few-shot prompting to improve output consistency and quality` [Guide]

### Core idea

When instructions alone give inconsistent output, show 2 to 4 examples. Pick the *tricky* cases,
and show *why* each choice was made, so Claude can generalize.

### Under the hood

- "the most effective technique for achieving consistently formatted, actionable output when
  detailed instructions alone produce inconsistent results" [Guide 4.2].
- "2-4 targeted few-shot examples for ambiguous scenarios that show reasoning for why one action was
  chosen over plausible alternatives" [Guide 4.2].
- Examples teach judgment that generalizes "to novel patterns rather than matching only
  pre-specified cases" [Guide 4.2].
- They show the output format (location, issue, severity, suggested fix) [Guide 4.2].
- They reduce extraction hallucination with varied formats, including "empty/null extraction of
  required fields" when documents are laid out differently [Guide 4.2].
- They separate acceptable patterns from real issues, which cuts false positives [Guide 4.2].

**How many examples?** The exam says "2-4" for few-shot prompting [Guide 4.2] and "2-3 concrete
input/output examples" for refining Claude Code output [Guide 3.5]; those are two different task
statements, so both are right in their place. What changed since: the docs say "Include 3–5 examples
for best results" [Prompting]. **On the exam: pick the guide's numbers (2–4 for TS 4.2, 2–3 for TS 3.5).**

**Order of fixes:** clear instructions and good tool descriptions come first; few-shot examples
come next, for what is still ambiguous (see section 2.3 at the end of this page).

### Look-alikes

- **"Add 20 examples covering every case."** The guide says 2 to 4 *targeted* examples. Many easy
  examples teach matching, not judgment.
- **"Show only correct outputs, no reasoning."** The guide asks for the reasoning: why A over B.
- **"Write a longer instruction paragraph."** Already failed; that's why you're adding examples.

### Worked example (scenario: structured data extraction)

Research papers cite sources two ways: inline and in a bibliography. The extractor returns empty
`citations` for bibliography papers. Add three examples: one inline, one bibliography, one mixed,
each with a line on where the citations were found.

**Exam reflex:** *Inconsistent output → 2 to 4 examples of the hard cases, with reasons.*

---

## 4.3 Enforce structured output

Lesson: [L04 section 4.3](../L04-prompt-engineering-and-structured-output.md#43-structured-output-through-tool-use) · Objective: [4.3](../objectives/objective-4.3.md)

**Exam wording:** `Task Statement 4.3: Enforce structured output using tool use and JSON schemas` [Guide]

### Core idea

Downstream code needs JSON it can parse every time. Asking nicely in the prompt is not enough.
You make Claude *fill in a form* (a tool's `input_schema`), and you design the form so Claude
never has to make something up to complete it.

There are two separate problems here. Keep them apart in your head:

1. **Syntax:** is it valid JSON with the right fields and types? Tool use with a schema solves this.
2. **Meaning:** are the values true? Do the line items add up to the total? Is the date in the
   right field? A schema **cannot** solve this. Exam wording: strict schemas "eliminate syntax
   errors but do not prevent semantic errors (e.g., line items that don't sum to total, values in
   wrong fields)" [Guide 4.3]. That is TS 4.4's job.

### Under the hood

**The reliability ladder (best first):**

1. **Schema-guaranteed:** strict tool use (`strict: true` on the tool) or JSON outputs
   (`output_config.format` with `type: "json_schema"`) [SO]. Decoding is constrained to the schema.
   That means: as Claude writes the answer one piece at a time, the API only lets it write pieces that
   keep the JSON valid for your schema. It literally can't type a character that breaks the schema.
2. **Plain tool use** with an `input_schema`. Very good, but not guaranteed: "Without strict mode,
   Claude might return incompatible types (`"2"` instead of `2`) or omit required fields" [Strict].
3. **Prompt-only JSON** ("Respond only in JSON"). Can add prose, miss a brace, rename keys.
4. **Prefill** (start the assistant turn with `{`). Weakest, and it returns `400` on Claude 4.6 and
   later models [Prompting], [Errors].

The guide agrees on the top rung: it names "Tool use (tool_use) with JSON schemas" as the most
reliable approach, and says "strict JSON schemas via tool use eliminate syntax errors but do not
prevent semantic errors" [Guide 4.3]. What changed since: today's docs add a second schema-guaranteed
feature, JSON outputs (`output_config.format`) [SO].

(Same rule as the table above.)

**Reading the answer back.** With tool use, the data is in the `tool_use` content block's `input`
field, not in a text block. Exam skill wording: "extracting structured data from the tool_use
response" [Guide 4.3]. With forced `any`/`tool`, the API prefills the assistant turn, so Claude
"will not emit a natural language response or explanation before `tool_use` content blocks" [Tools].

**Where the schema guarantee stops (Extra, beyond the guide: current-docs depth).** Even schema-guaranteed output can miss your schema [SO]:

- `stop_reason: "refusal"`: the refusal "takes precedence over schema constraints".
- `stop_reason: "max_tokens"`: the output was cut off mid-JSON. Raise `max_tokens` and retry.
- **Enum capitalization:** structured outputs "don't guarantee the capitalization of string `enum`
  and `const` values". The response looks normal with no error. Compare enums case-insensitively.
- **Unsupported constraints:** `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`,
  recursive schemas, and `additionalProperties` other than `false` are **not supported**. Sent raw,
  they give a `400`. The SDK helpers strip them, copy them into the field description, and check
  them on the client [SO]. So "the schema enforces `maximum: 100`" is false at the decoding level.
- **Citations:** incompatible with `output_config.format`; enabling both "Returns 400 error" [SO].
- Every object needs `additionalProperties: false` [SO].

### Schema design: required, nullable, enums

This is where you lost points. Learn these four patterns cold.

**Pattern 1. Required but nullable (the key fix).** If a field is `required` and its type is plain
`string`, but the document doesn't have the value, the model is pushed to *invent* one to satisfy
the schema. Exam wording: design fields "as optional (nullable) when source documents may not
contain the information, preventing the model from fabricating values to satisfy required fields"
[Guide 4.3].

```json
"invoice_po_number": {
  "anyOf": [{"type": "string"}, {"type": "null"}],
  "description": "The PO number exactly as printed. Use null if the document has no PO number. Never guess."
}
```

The shorter form does exactly the same job, and both are valid in strict schemas:

```json
"invoice_po_number": {"type": ["string", "null"], "description": "... Use null if not printed."}
```

Keep it in `required`, so the key is always present, but let the value be `null`. Your code can then
tell "missing from the source" (`null`) apart from "the model forgot the key". The structured-outputs
page counts both `anyOf` and type arrays like `"type": ["string", "null"]` as union types [SO].
(Extra, beyond the guide: at most 16 parameters may use `anyOf` or type arrays, counted across all
strict schemas in one request; non-strict tools don't count toward it [SO].)

**Pattern 2. Optional field.** Leave it out of `required`. Fine for data that is truly extra. The
downside: your code can't tell "absent" from "forgot". For extraction, Pattern 1 is usually cleaner.
On the exam, "optional (nullable)" are used together, and both beat "required, non-null" for data
that may be missing.

**Pattern 3. Enum with `"other"` plus a detail string.** For categories that will grow.

```json
"doc_type": {"type": "string", "enum": ["invoice", "receipt", "credit_note", "other"]},
"doc_type_detail": {
  "anyOf": [{"type": "string"}, {"type": "null"}],
  "description": "If doc_type is 'other', describe the type in a few words. Otherwise null."
}
```

Exam wording: "enum fields with "other" + detail string patterns for extensible categories"
[Guide 4.3]. Without `"other"`, a new document type is forced into the closest wrong bucket.

**Pattern 4. An `"unclear"` value.** For cases that are ambiguous, not new. Exam wording: "Adding
enum values like "unclear" for ambiguous cases" [Guide 4.3]. `"unclear"` is also a clean routing
signal for TS 5.5: send it to a person.

**Pattern 5. Format rules in the prompt, next to the schema.** The schema says "string"; it can't
say "ISO 8601". Exam wording: "Including format normalization rules in prompts alongside strict
output schemas to handle inconsistent source formatting" [Guide 4.3]. For example: "Write dates as
YYYY-MM-DD. Write amounts as numbers with no currency symbol; put the currency in `currency`."

### Look-alikes

- **"Add 'respond only in valid JSON' to the system prompt."** Sounds fine. It is prompt-only JSON,
  rung 3. Tool use with a schema removes the whole class of syntax errors; the prompt only makes
  them rarer.
- **"Make every field required so nothing is missed."** This is the trap that causes made-up values.
  Required + non-nullable + missing data = fabrication.
- **"Use strict mode so the totals always match."** A schema guarantees shape, not truth. Totals are
  a meaning check, done in code (TS 4.4).
- **"Add `maximum: 10000` to the amount field so bad amounts can't appear."** Not enforced by
  decoding; check the range in your own code.

### Worked example (scenario: structured data extraction)

A pipeline pulls fields from scanned supplier invoices. About 8% of invoices have no PO number.
Reviewers find made-up PO numbers like `PO-0001`. The schema has `po_number` as required `string`.

- **Best fix:** keep `po_number` required, allow `null`, and say "use null if not printed" in the
  description. Code sends `null` PO numbers to the right queue.
- **Why not "add a few-shot example with a PO number"?** It shows the format but still forces a value.
- **Why not "lower the temperature"?** The cause is the schema, not randomness.
- **Why not "retry when the PO looks fake"?** The data isn't in the document. A retry can't find it
  (TS 4.4).

**Exam reflex:** *Schema fixes syntax, never truth. If the value may be missing, the field must be
allowed to be `null`. Growing categories get `"other"` + detail; ambiguous ones get `"unclear"`.*

---

## 4.4 Validation, retry and feedback loops

Lesson: [L04 section 4.4](../L04-prompt-engineering-and-structured-output.md#44-validate-retry-feed-back) · Objective: [4.4](../objectives/objective-4.4.md)

**Exam wording:** `Task Statement 4.4: Implement validation, retry, and feedback loops for extraction quality` [Guide]

### Core idea

After the schema guarantees shape, your code checks meaning. When a check fails, send Claude the
exact error and let it try again. But know when a retry is pointless: **retries fix format, not
missing facts.**

### Under the hood

- **Retry with error feedback.** The follow-up request carries three things: "the original document,
  the failed extraction, and specific validation errors" [Guide 4.4]. "Specific" means the real
  message: `line_items sum to 1,240.00 but stated_total is 1,420.00`. Not "please try again".
- **Cap the retries** (one or two), then route to a person (practice, not doc).
- **When a retry works:** "format mismatches, structural output errors" [Guide 4.4]. A date in the
  wrong format, a misread digit, a value in the wrong field.
- **When a retry can't work:** "the required information is simply absent from the source
  document", for example it "exists only in an external document not provided" [Guide 4.4]. Retrying
  only invites a made-up value. Return `null` and route.
- **Self-correction fields.** Extract both `"calculated_total"` and `"stated_total"`, and add a
  `"conflict_detected"` boolean for inconsistent source data [Guide 4.4]. Add the line items in
  **code** too. Never ask the model to "make them match", and never overwrite the stated total.
- **Semantic vs syntax errors.** Syntax errors are "eliminated by tool use"; semantic errors ("values
  don't sum, wrong field placement") need validation [Guide 4.4].
- **Feedback loop.** Add a `detected_pattern` field to each finding to track "which code constructs
  trigger findings", so when people dismiss findings you can see which patterns cause false
  positives [Guide 4.4]. In extraction, log error type, field and document type the same way.

### Look-alikes

- **"Retry up to five times until the field is filled."** If the fact isn't in the document, five
  retries give you five guesses.
- **"Retry with 'that was wrong, try again'."** No specific error, so no direction. Include the
  validator's exact message.
- **"Ask the model to adjust the line items so they sum to the total."** That hides a real
  discrepancy. Flag it with both values.
- **"Use strict mode instead of validation."** Strict mode is syntax. Totals are semantics.

### Worked example (scenario: structured data extraction)

The model reads the stated total as `1,420.00`; the line items add to `1,240.00` in code.

1. Retry once with the document, the first extraction and the message "line items sum to 1,240.00;
   stated_total is 1,420.00; recheck both".
2. Second result: still `1,420.00` stated, items `1,240.00`. The source really is inconsistent.
3. Set `conflict_detected: true`, keep both numbers, route to a reviewer with the field marked.

A twist: the contract number is "per the master agreement", which isn't attached. No retry. Return
`null` and route.

**Exam reflex:** *Retry with the exact error, at most once or twice. Missing from the source = no
retry. Keep both totals and flag the conflict.*

---

## 4.5 Batch processing strategy

Lesson: [L04 section 4.5](../L04-prompt-engineering-and-structured-output.md#45-batch-processing) · Objective: [4.5](../objectives/objective-4.5.md)

**Exam wording:** `Task Statement 4.5: Design efficient batch processing strategies` [Guide]

### Core idea

If nobody is waiting, use the Message Batches API: half the price, but results can take up to a
day. If someone or something is waiting (a merge check), use the normal API.

### Under the hood

Batch facts [Batch] (exam wording where noted [Guide 4.5]):

- **Price:** "charged at 50% of the standard API prices". Exam: "50% cost savings".
- **Time:** most batches finish in under 1 hour, but results come when all are done **or after 24
  hours**. Exam: "up to 24-hour processing window, no guaranteed latency SLA".
- **Size:** "100,000 Message requests or 256 MB in size, whichever is reached first".
- **Order:** "Batch results can be returned in any order". Match by `custom_id` (1 to 64 chars,
  letters, digits, `-`, `_`).
- **Result types:** `succeeded`, `errored`, `canceled`, `expired`. For `errored`, `canceled` and
  `expired`: "You will not be billed for these requests". `expired` = "reached its 24-hour expiration
  before this request could be sent".
- **Retention:** results "available for 29 days after creation".
- **Tools:** exam wording: the batch API "does not support multi-turn tool calling within a single
  request (cannot execute tools mid-request and return results)" [Guide 4.5]. An agent loop that
  needs *your* tool results doesn't fit in one batch request. **On the exam: pick "not Batch" for
  any flow that must run your tools mid-request.**
  - Docs detail (Extra, beyond the guide): this is true for **client tools** (tools your code runs). A batch
    request can still contain tool definitions and multi-turn history, and **server tools** (web
    search, web fetch, code execution, MCP connectors and others) run on Anthropic's side inside the
    request [Batch].

**Deadline math (exam skill).** Exam wording: "4-hour windows to guarantee 30-hour SLA with 24-hour
batch processing" [Guide 4.5]. Worst case for one document: it arrives just after a submission,
waits up to one cycle (4 h), then takes up to 24 h. 4 + 24 = 28 h, which leaves 2 h to collect
results and handle failures inside 30 h. **The one rule: cycle + 24 h + buffer ≤ deadline, so 4 h,
not 6 h.** A 6-hour cycle hits exactly 30 h with no room to handle failures. (Some notes say
"30 − 24 = 6"; that forgets the buffer. Use 4 h.)

**Handling failures.** Resubmit "only failed documents (identified by custom_id) with appropriate
modifications (e.g., chunking documents that exceeded context limits)" [Guide 4.5]. Not the whole
batch.

**Test the prompt first.** "Using prompt refinement on a sample set before batch-processing large
volumes" [Guide 4.5]. A bad prompt across 50,000 documents is 50,000 bad results.

**Prompt caching (one line).** Prompt caching exists, reuses a stable prefix of your prompt (put the
unchanging parts first), and can stack with the Batch discount [Cache]. The details are out of scope:
the guide's out-of-scope list says "Prompt caching implementation details (beyond knowing it exists)".

### Look-alikes

- **"Use Batch for the pre-merge review to save 50%."** Blocking work. Someone waits up to 24 h. Use
  the synchronous API.
- **"Submit one batch a day for a 30-hour deadline."** 24 h wait + 24 h processing = 48 h. Too slow.
- **"Resubmit the whole batch when 300 of 10,000 fail."** Pays twice for the 9,700 that worked.
- **"Match results by their position in the output file."** Order is not guaranteed. Use `custom_id`.

### Worked example (scenario: structured data extraction)

A finance team needs 40,000 receipts processed each week, with each receipt done within 30 hours of
upload. Uploads trickle in all day.

- Submit a batch every 4 hours, each request's `custom_id` = the receipt ID. Worst case 28 h.
- After each batch: `succeeded` → store; `errored` with a context error → split the receipt and
  resubmit just that `custom_id`; `expired` → resubmit (no charge for the expired one).
**Exam reflex:** *Someone waiting → normal API. No one waiting → Batch. Cycle + 24 h + buffer ≤
deadline. Match and resubmit by `custom_id` only.*

---

## 4.6 Multi-instance and multi-pass review

Lesson: [L04 section 4.6](../L04-prompt-engineering-and-structured-output.md#46-multi-instance-and-multi-pass-review) · Objective: [4.6](../objectives/objective-4.6.md)

**Exam wording:** `Task Statement 4.6: Design multi-instance and multi-pass review architectures` [Guide]

### Core idea

A writer is a poor judge of their own work. Use a fresh reviewer. And split a big review into small
per-file passes plus one pass that looks across files.

### Under the hood

- **Self-review is weak:** the model "retains reasoning context from generation, making it less
  likely to question its own decisions in the same session" [Guide 4.6].
- **Independent instance** without the generator's reasoning catches more than "self-review
  instructions or extended thinking" [Guide 4.6]. In Claude Code CI: a separate `claude -p` run
  for review, not the session that wrote the code (see deep practice 3, TS 3.6).
- **Multi-pass:** "per-file local analysis passes plus cross-file integration passes to avoid
  attention dilution and contradictory findings" [Guide 4.6].
- **Verification pass with confidence:** the model reports confidence per finding, which feeds
  calibrated routing (TS 5.5) [Guide 4.6].

### Look-alikes

- **"Ask the same session to 'review your work critically'."** Still has its own reasoning in context.
- **"Turn on extended thinking for the review."** The guide names this as weaker than an independent
  instance.
- **"Review all 40 files in one pass with a bigger context window."** Attention dilution; split it.

### Worked example (scenario: code generation with Claude Code)

A 30-file refactor PR. Plan: one independent review instance per file for local bugs, then one
integration pass given short summaries of each file's changes to check cross-file data flow. Each
finding carries a confidence; low ones go to a human.

**Exam reflex:** *Fresh instance reviews. Per-file passes, then one cross-file pass.*

---

## 2.3 Tool choice and tool order (the rest of 2.3 is in deep practice 2)

Lesson: [L02 section 2.3](../L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones) · Objective: [2.3](../objectives/objective-2.3.md)

**Exam wording:** `Task Statement 2.3: Distribute tools appropriately across agents and configure tool choice` [Guide]

This page covers the `tool_choice` half. The "how many tools per agent" half is taught in deep practice 2, with a
short recap here because the exam mixes them.

### Core idea

`tool_choice` answers one question: **may Claude answer in plain text, or must it call a tool,
and which one?** Pick the loosest setting that still guarantees what your code needs.

### Under the hood

The four options [Tools]; the first three are the exam's [Guide 2.3, 4.3]:

| Setting | What it forces | Exam wording |
|---|---|---|
| `{"type": "auto"}` (default) | Nothing. Claude may call a tool **or** reply with text. | "model may return text instead of calling a tool" |
| `{"type": "any"}` | Must call **a** tool; Claude picks which. | "model must call a tool but can choose which" |
| `{"type": "tool", "name": "extract_metadata"}` | Must call **that** tool. | "forced tool selection (model must call a specific named tool)" |
| `{"type": "none"}` | No tool calls. | (not in the guide) |

- **`any`** is the exam answer when there are **several extraction schemas and the document type is
  unknown**: "Setting tool_choice: "any" to guarantee structured output when multiple extraction
  schemas exist and the document type is unknown" [Guide 4.3]. Each document type has its own tool
  (`extract_invoice`, `extract_receipt`); Claude picks the matching one, but can't chat instead.
- **Forced named tool** is the answer for **order**: "Forcing a specific tool ... to ensure a
  particular extraction runs before enrichment steps" [Guide 4.3], and "then processing subsequent
  steps in follow-up turns" [Guide 2.3]. An *enrichment step* adds extra data on top of what you
  extracted, for example looking up the vendor's address from the vendor name, so it needs the
  extracted data first. Turn 1: force `extract_metadata`. Turn 2 onward: switch to
  `auto` so Claude can use the enrichment tools. A forced tool forces *every* turn it is set on, so
  you change it between turns.
- **`disable_parallel_tool_use: true`** goes **inside** the `tool_choice` object, not at the top
  level of the request [Tools].
- **Caching side effect:** changing `tool_choice` invalidates cached *message* blocks; tools and
  system stay cached [Tools].
- **What changed since:** forced `any`/`tool` returns `400` on Opus 5.5, Sonnet 5.5, Fable 5.1 and
  Mythos 5.1; the docs say use `auto` + `strict: true`, or `output_config.format` [Tools], [Errors].
  **On the exam: pick forced `tool_choice` (`any` or the named tool).**

**Tool distribution recap (deep practice 2 has the depth).** Exam wording: giving an agent "too many tools
(e.g., 18 instead of 4-5) degrades tool selection reliability" [Guide 2.3]. Scope each agent's tools
to its role. Swap generic tools for constrained ones (`fetch_url` → `load_document`). Give a narrow
cross-role tool (`verify_fact`) for high-frequency needs and route the hard cases through the
coordinator [Guide 2.3].

**Fix tool descriptions before adding few-shot examples.** When Claude picks the wrong tool, the
first fix is the tool's description: what it does, when to use it, and when to use the look-alike
tool instead. The docs call detailed descriptions "by far the most important factor in tool
performance" and say "Aim for at least 3–4 sentences" [Tools]. Few-shot examples come after that, for cases that are still ambiguous
(TS 4.2). "Add few-shot examples" as the *first* move is a common distractor (practice, not doc;
Tier 3 candidate reports, see SOURCES.md).

### Look-alikes

- **"Set `tool_choice: auto` and tell the model in the prompt to always call the tool."** Prompt-based,
  so it can fail. `any` or forced removes the text path entirely.
- **"Force `extract_invoice` for every document."** Breaks on receipts: Claude must fill the invoice
  form for a receipt. Unknown type → `any`.
- **"Use `any` to make sure metadata is extracted first."** `any` doesn't control *which* tool. Order
  needs the named tool.
- **"Give the extraction agent all 18 tools so it never lacks one."** Fewer, role-scoped tools pick
  better.

### Worked example (scenario: structured data extraction)

The pipeline gets a mixed folder: invoices, receipts and contracts, unlabeled. Each has its own
extraction tool. One in twenty replies comes back as text ("This looks like a receipt...") and the
parser crashes. Later, an enrichment step (`lookup_vendor`) sometimes runs before metadata exists.

- Fix 1: `tool_choice: {"type": "any"}` on the extraction call. No more text replies; Claude still
  picks the right schema.
- Fix 2: on the first call of the enrichment flow, force `{"type": "tool", "name": "extract_metadata"}`;
  then send the next turn with `auto`.
- Not: "retry when the reply isn't JSON". That treats the symptom; `any` removes the cause.

**Exam reflex:** *Text sneaking in → `any`. Order matters → force the named tool on the first turn,
then `auto`. Wrong tool picked → fix descriptions before adding examples.*

---

## 5.5 Human review and confidence calibration

Lesson: [L05 section 5.5](../L05-context-management-and-reliability.md#55-human-review-and-confidence) · Objective: [5.5](../objectives/objective-5.5.md)

**Exam wording:** `Task Statement 5.5: Design human review workflows and confidence calibration` [Guide]

### Core idea

Reviewers are few. Send them the items most likely to be wrong, and prove the "auto" items really
are right. Two dangers: one big accuracy number that hides a bad corner, and a model's raw
confidence that nobody has checked against real answers.

### Under the hood

The guide's moving parts [Guide 5.5], in the order you'd build them:

1. **Field-level confidence**, not one score per document. The model outputs a confidence next to
   each field (add a `confidence` number per field to the schema). One document can have a sure
   total and an unsure date.
2. **Calibrate with a labeled validation set.** Raw model confidence is just a number until you
   compare it to truth. Run the pipeline on documents where you know the right answers. Find the
   threshold per field where, say, 0.9 confidence really means about 90% correct. Exam wording:
   "calibrating review thresholds using labeled validation sets".
3. **Segment the accuracy.** Exam wording: "aggregate accuracy metrics (e.g., 97% overall) may mask
   poor performance on specific document types or fields". Check accuracy by document type **and**
   by field before you cut review. 97% overall can be 99% on invoices and 70% on handwritten receipts.
4. **Route.** Send to people: low confidence, ambiguous or contradictory sources, `"unclear"` enum
   values, `null` in a field that should usually exist, failed meaning checks (TS 4.4). Exam wording:
   "Routing extractions with low model confidence or ambiguous/contradictory source documents to
   human review, prioritizing limited reviewer capacity".
5. **Keep sampling the "sure" ones.** Exam wording: "stratified random sampling of high-confidence
   extractions for ongoing error rate measurement and novel pattern detection". *Stratified* means
   you sample from each document type and field group, so small groups aren't missed. This is how you
   catch new error types the thresholds don't know about.

Note: the exam wants **stratified random sampling of high-confidence items** as the *audit*. What it
rejects is **random sampling as the main routing method** (reviewing a random 10% instead of the
risky ones). Both use the word "random"; read which job it is doing.

**Don't carry this into TS 5.2.** For escalating support cases, raw self-reported confidence is the
*distractor*: the guide says "self-reported confidence scores are unreliable proxies" there. Explicit
escalation criteria with few-shot examples win [Guide 5.2]. Confidence works in TS 5.5 only because
it is *field-level* and *calibrated on labeled data*.

Confidence routing and calibration are practice patterns the guide tests; there is no API field for
"confidence" (practice, not doc).

### Look-alikes

- **"Overall accuracy is 97%, so turn off human review."** Exactly what the guide warns against.
  Check by type and field first.
- **"Review a random 10% of all extractions."** Wastes scarce reviewers on easy items, and still
  misses the risky ones. Route by risk; sample only to audit.
- **"Ask the model to only output fields it is confident about."** A vague instruction. It hides
  uncertainty instead of measuring it.
- **"Use the model's confidence score directly as the threshold."** Uncalibrated. Calibrate on a
  labeled set first.

### Worked example (scenario: structured data extraction)

Leadership wants to cut human review because accuracy is 97%. You split the number: invoices 99.2%,
typed receipts 98%, handwritten receipts 81%, and the `tax_amount` field is 88% across all types.

- Plan: keep review for handwritten receipts and for `tax_amount` below its calibrated threshold.
  Auto-approve the rest. Each week, sample a stratified random set of auto-approved items from every
  type to measure the error rate and catch new patterns.
- Not: "keep reviewing everything until it's 99%". Wastes reviewers on segments already proven.

**Exam reflex:** *Split the accuracy by type and field. Calibrate confidence on labeled data. Route
the risky items; audit the sure ones with stratified sampling.*

---

## Quick sheet: exact values

| Fact | Value | Source |
|---|---|---|
| Force any tool | `{"type": "any"}` | [Tools], [Guide] |
| Force one tool | `{"type": "tool", "name": "..."}` | [Tools], [Guide] |
| Parallel off | `disable_parallel_tool_use` inside `tool_choice` | [Tools] |
| JSON outputs | `output_config.format`, `type: "json_schema"` | [SO] |
| Strict tool use | `strict: true` on the tool | [SO] |
| Schema can still miss on | `refusal`, `max_tokens`, enum casing | [SO] |
| Not supported in schema | `minimum`, `maximum`, `minLength`, `maxLength`, recursion | [SO] |
| Objects need | `additionalProperties: false` | [SO] |
| Batch price / size | 50% / 100,000 requests or 256 MB | [Batch] |
| Batch window / retention | 24 h / 29 days | [Batch] |
| Batch unbilled results | `errored`, `canceled`, `expired` | [Batch] |
| Batch cadence for a 30 h deadline | every 4 h (cycle + 24 h + buffer ≤ deadline) | [Guide 4.5] |
| Prefill on Claude 4.6+ | `400` `invalid_request_error` | [Prompting], [Errors] |
| Nullable field | `"type": ["string", "null"]` or `anyOf` with `null` | [SO] |
| CI JSON | `claude -p ... --output-format json` (+ `--json-schema`) | [Headless] |

## Sources (citation keys, Tier 1 unless marked, checked 2026-10-06)

- `[Guide]`, `[Guide x.y]` the official CCAR-F exam guide v1.0 (July 2026, Anthropic); x.y is the task statement.
- `[SO]` [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- `[Strict]` [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- `[Tools]` [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  (the old "Implement tool use" URL redirects here)
- `[Errors]` [API errors](https://platform.claude.com/docs/en/api/errors) ("Prefill not supported";
  "Forced tool use not supported")
- `[Prompting]` [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
  ("Migrating away from prefilled responses"; "Include 3–5 examples")
- `[Batch]` [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- `[Cache]` [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- `[Headless]` [Claude Code headless mode](https://code.claude.com/docs/en/headless)

## Practice, not doc

These are patterns the guide tests but no API page defines: confidence routing, calibration
thresholds, "other" + detail fields, "retry at most once or twice", and "fix tool descriptions before
adding few-shot examples".

**Next:** [Lesson 3, Claude Code configuration and workflows](../L03-claude-code-configuration-and-workflows.md), the next lesson in the study order, or back to the [CCAR-F lessons page](../README.md).