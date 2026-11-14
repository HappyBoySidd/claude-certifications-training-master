# Lab 02 — An agent loop, two subagents and schema-checked extraction (CCAR-F, CCDV-F)

<!-- layered-scenario-migration -->
## Read the experiment before building

**Two ways to use this lab:** read and predict with no setup, or run the separately identified fixtures/build steps after completing their prerequisites below. These layers are paper experiments until you execute an implementation. An expected trace is not a captured run. Use fictional records in a disposable folder; do not connect real customer data or business effects. Keep input, expected result, observed result and recovery evidence separately.

### Stage 1 — Another investigator joins, but receives the wrong brief

The support case now needs both an order check and a policy check. Each specialist works in a separate conversation. The coordinator tells the policy specialist “use what the other agent found,” but sends neither the order nor its evidence. The reply confidently discusses a different product.

**Original exam-style practice — choose ONE.** Which coordinator-subagent design best preserves context isolation while enabling evidence-grounded synthesis?

A. Assume all subagents inherit the coordinator conversation automatically.

B. Broadcast all transcripts to every specialist indefinitely.

C. Pass a bounded brief containing the task, relevant facts, source references and expected return contract; validate the returned evidence before synthesis.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice C.** A separate conversation needs an explicit briefing packet. C supplies what this job requires and lets the receiver check it. A assumes memory that may not exist; B carries unrelated history, extra cost and potentially unnecessary sensitive data.

**Follow the changed path:**

```text
coordinator → bounded brief → specialist → result + sources + status
receiver checks required fields and evidence → integrated answer
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Remove the order reference from the brief: the specialist must flag missing evidence rather than supply a made-up answer. Restore it and trace the returned claim back to that order.

</details>

**Changed-constraint decision — choose ONE before revealing:** Both checks can be completed reliably with one agent and two tools. A: always add specialists; B: keep the simpler design unless specialization solves a demonstrated requirement.

<details><summary>Reveal changed-constraint reasoning</summary>

B. More agents are not a quality guarantee. Split work when independent expertise, context or work boundaries justify the coordination cost.

</details>

**Objective connections:** [1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.2.md), [1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.3.md), [1.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.6.md).

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

**Objective connections:** [4.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md), [4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md).

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

**Objective connections:** [4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.5.md), [4.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.6.md).

<!-- /layered-scenario-migration -->


**Supports:** CCAR-F L01, L04, L05 · CCDV-F L03 (Agents and workflows) and L04 (Prompt and context engineering) · **Time:** 3–4 hours · **Needs:** Python 3.10+,
`pip install anthropic jsonschema`, and an API key.

> **Salesforce laptops block direct calls to the Anthropic API.** People who passed used either a
> personal account on a personal laptop, or the internal LLM gateway; ask in
> #claude-certified-architect-exam-prep. (This comes from colleague debrief notes, on the Insights page under "Hands-on practice".) Never paste company or
> customer data into a personal account.

## Understand the design before setup

Before executing this lab, read the [action-service loop](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-01-action-service.md) and its plain-language/technical choices. Reading requires no credentials; **running this lab does require the setup, account, environment and permission prerequisites below**. Keep its real execution evidence separate from the paper case and local Lab08 fixture. Use the [full learning journey](../../02-Lessons/02-CCAR-F-Architect-Foundations/learning-journey.md) to return to objectives, practice and repair.

## Connect this build to scenario decisions

**Before building:** [Choose a case in the scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md). Predict the result before running each failure injection.

Inject a tool failure, a schema-valid wrong amount and conflicting totals. Retain successes, send the exact validation error, stop retries at the declared budget and preserve the contradictory source values.

**Evidence to keep:** synthetic input, observed tool/result or hook outcome, expectation, actual failure category, recovery and a changed-condition retest. Do not mark this lab complete from reading alone.

- [FV-01 — Confirm the effect before retrying](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.1.md#variant-fv-01) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.1&variant=FV-01)
- [FV-02 — Cover dimensions before synthesizing](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.2.md#variant-fv-02) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.2&variant=FV-02)
- [FV-21 — Validate shape and truth separately](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md#variant-fv-21) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.3&variant=FV-21)
- [FV-22 — Repair the failed check within a budget](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md#variant-fv-22) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.4&variant=FV-22)
- [FV-27 — Propagate partial success without hiding failure](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.3.md#variant-fv-27) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.3&variant=FV-27)

**After building:** explain which constraint changes the answer, then use [drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md), [recall](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md) and [simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) to transfer the mechanism.

## What you'll build and why

You'll write one small "coordinator" agent that hands work to two helper agents: one that
searches notes, one that pulls invoice fields into a checked JSON shape. Doing it by hand shows
you what an agent loop really is, why helpers get narrow tools, and how retries with a precise
error fix bad extractions.

```text
you ──> coordinator loop
          ├── research(topic) ──> researcher loop ──> search_notes ──> notes/*.txt
          └── extract(doc)    ──> extractor loop  ──> record_invoice ──> jsonschema + your rules
                                                            │ fails? retry with the error (max 2)
                                                            └── still fails? needs-human-review list
```

Words you'll meet, in plain terms:

- **Agent loop:** call the model, run any tools it asks for, send the results back, repeat until
  it says it's done.
- **`stop_reason`:** the field on each reply that says why the model stopped. `tool_use` means
  "run my tools"; `end_turn` means "I'm finished".
- **`tool_use` / `tool_result` blocks:** the model's tool request, and your answer to it, linked
  by the same `tool_use_id`.
- **Coordinator:** the top agent that decides what to do and calls helpers.
- **Subagent:** a helper agent, here just a fresh loop with its own system prompt and tools.
- **JSON schema:** a description of the exact fields and types a JSON object must have.
- **`tool_choice`:** a request setting that can force the model to call one named tool.
- **`is_error`:** a flag on a `tool_result` that tells the model "that call failed".

Task numbers refer to the task statements in the official exam guide.

## Why this matters on the exam

- The loop ends when the model says so (`end_turn`), not when a counter runs out.
- Subagents get only the tools and context their job needs; more tools means more wandering.
- Tool calls with a schema (forced where the model allows it, otherwise `auto` + `strict: true`),
  plus validation and a retry that quotes the error, are the reliable way to get structured data
  out.
- A failure must look like a failure. An empty "success" hides it from the coordinator.

**Done when:**

- the coordinator loop and the researcher loop each stop because `stop_reason == "end_turn"`
  (print the stop reason on the last turn and see `end_turn`), not because a turn counter ran out
- the extractor returns as soon as it gets a `record_invoice` call that passes validation, not on
  `end_turn`. On a model that supports forcing, you force the tool with `tool_choice`; on a model
  that rejects forcing (see Step 3), you use `auto` plus `strict: true` and a prompt that says to
  call the tool, and either way the exit is the valid `record_invoice` call
- for each subagent call you print its `tools` list and its first user message, and see: the
  researcher has only `search_notes` and gets only the topic; the extractor has only
  `record_invoice` and gets only one document
- `inv_bad_math.txt` fails once if the model copies 100.00 into `calculated_total`, is retried
  with the exact error message, and passes within 2 retries with `calculated_total` 90.00,
  `stated_total` 100.00 and `totals_conflict` true
- `inv_no_vendor.txt` ends up on the needs-human-review list after 2 retries, and is not retried
  a third time
- a failing `search_notes` call reaches the coordinator as
  `{"status": "error", ...}`, not as an empty success

## Build it in five steps

### 0. Set up (about 20 minutes)

Make this folder layout:

```text
lab02/
  agent.py
  notes/       5 short .txt files
  invoices/    5 short .txt files
```

Sample notes (one or two lines each is enough):

- `notes/returns.txt`: "Returns are accepted within 30 days with a receipt."
- `notes/shipping.txt`: "Standard shipping takes 3 to 5 business days."
- three more on any topic you like.

Sample invoices (make 3 clean, plus these 2 broken on purpose):

- `invoices/inv_ok_1.txt`: "Acme Ltd. Date 2026-09-01. Widgets 2 x 25.00 = 50.00. Bolts
  1 x 50.00 = 50.00. Total 100.00 USD."
- `invoices/inv_bad_math.txt`: same, but the line items are 40.00 and 50.00 while the total
  still says 100.00.
- `invoices/inv_no_vendor.txt`: line items and total, but no vendor name anywhere.

**How you know it worked:** `ls notes invoices` shows 5 files in each.

### 1. The loop (about 45 minutes, about 30 lines)

*Practises: task 1.1.*

- Call `client.messages.create(model=MODEL, max_tokens=..., tools=TOOLS, messages=history)`.
  Pick `MODEL` from the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
  (Tier 1, check the current docs).
- If `response.stop_reason == "tool_use"`:
  1. run each `tool_use` block
  2. append the whole assistant turn (`{"role": "assistant", "content": response.content}`,
     including its `tool_use` blocks), then **one** user turn holding every `tool_result`
     block, each with the matching `tool_use_id`
  3. loop again
- If it's `"end_turn"`, stop and return the text.
- Any other `stop_reason`, such as `max_tokens`, is not success: log it and handle it on
  purpose (raise `max_tokens`, or fail loudly). The full list of stop reasons can change, so
  check the current docs.
- Keep a high safety cap, for example 25 turns, and log it if the cap is ever hit. A cap is a
  seatbelt, not the way the loop is meant to end.

Skeleton (the marked lines are yours to fill in):

```python
def run_loop(system, tools, history, tool_impls, cap=25, tool_choice=None):
    for turn in range(cap):
        extra = {"tool_choice": tool_choice} if tool_choice else {}
        response = client.messages.create(model=MODEL, max_tokens=2048, system=system,
                                          tools=tools, messages=history, **extra)
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")
        if response.stop_reason != "tool_use":
            raise RuntimeError(f"Unexpected stop_reason: {response.stop_reason}")  # YOUR CHOICE
        history.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = tool_impls[block.name](**block.input)        # YOUR TOOLS
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": json.dumps(output)})
        history.append({"role": "user", "content": results})          # ONE user turn
    raise RuntimeError("Safety cap hit")  # log it: this should never be the normal ending
```

The extractor uses the same loop but exits differently: on a valid `record_invoice` call, not on
`end_turn`. Replace the inner tool step with this variant:

```python
if block.type == "tool_use" and block.name == "record_invoice":
    problem = validate(block.input)            # jsonschema + your rules; None if fine
    if problem is None: return block.input     # pass: done
    results.append({"type": "tool_result", "tool_use_id": block.id,
                    "is_error": True, "content": problem}); retries += 1  # fail: one retry
    if retries > 2: return {"status": "needs_review", "document": doc, "error": problem}  # 2 retries used
```

What `history` looks like after one tool round (simplified):

```python
[
  {"role": "user", "content": "What is our returns policy?"},
  {"role": "assistant", "content": [
      {"type": "tool_use", "id": "toolu_01", "name": "search_notes",
       "input": {"query": "returns"}}]},
  {"role": "user", "content": [
      {"type": "tool_result", "tool_use_id": "toolu_01",
       "content": "[\"Returns are accepted within 30 days with a receipt.\"]"}]},
]
```

**How you know it worked:** the loop runs without errors on a plain question with no tools
needed and ends on `end_turn`. The full tool round is checked at the end of Step 2, once
`search_notes` exists.

### 2. Two subagents with narrow tools (about 45 minutes)

*Practises: tasks 1.2, 1.3 and 2.3.*

Make the coordinator's tools `research(topic)` and `extract(document)`. Each one calls a fresh
loop, which is the subagent, with its own system prompt and its own tool list:

| Subagent | Tools | Gets |
| --- | --- | --- |
| researcher | `search_notes(query)`, a fake search over 5 local text files | the topic only |
| extractor | `record_invoice(...)`, whose input schema is your JSON schema | one document only |

Return a **short, structured result** to the coordinator, not the subagent's whole transcript.
If a subagent's tool fails, it returns a structured failure, for example
`{"status": "error", "error": "search_notes timed out", "partial_results": [...]}`, so the
coordinator can decide what to do. An empty "success" hides the failure.

The subagent call, in pseudo-code:

```python
def research(topic):
    history = [{"role": "user", "content": topic}]          # the topic only, nothing else
    print([t["name"] for t in RESEARCH_TOOLS], history[0])  # the Done-when check
    try:
        answer = run_loop(RESEARCHER_SYSTEM, RESEARCH_TOOLS, history, {"search_notes": search_notes})
        return {"status": "ok", "answer": answer}
    except ToolFailure as e:                                 # YOUR exception type
        return {"status": "error", "error": str(e), "partial_results": e.partial}
```

**How you know it worked:** the printout shows `['search_notes']` and only the topic text. Then
ask the researcher "What is our returns policy?": it prints one `tool_use` turn, then
`end_turn`, and answers "30 days with a receipt".

### 3. Extraction through a tool schema (about 45 minutes)

*Practises: task 4.3.*

*Practises: tasks 4.1–4.3.*

- Define `record_invoice` with an `input_schema`: `vendor`, `date` (ISO 8601), `stated_total`
  and `calculated_total` (numbers, so a mismatch can be flagged), `line_items` (array), and
  `confidence` (`high`, `medium` or `low`). `vendor` is **required** and not nullable, so an
  invoice with no vendor can only end on the review list.
- `calculated_total` must be the sum of `line_items`; `stated_total` is what the document says.
  Add a required boolean `totals_conflict`: true when they differ. That's a flagged conflict,
  not a failure.
- Make `date` nullable (`"type": ["string", "null"]`) and tell the model to return null when
  the document has no date. A required, non-nullable field pushes the model to invent a value.
- Add `currency` as an enum that includes `"other"`, plus a `currency_detail` string for when
  `"other"` is chosen.
- Force it with `tool_choice={"type": "tool", "name": "record_invoice"}`. **Check your model
  first:** the [define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  page (Tier 1, check the current docs) says forced `tool_choice` (`any` or `tool`) returns a 400
  error on Opus 5.5, Sonnet 5.5, Fable 5.1 and Mythos 5.1. Either use a model that supports
  forcing (the docs example uses `claude-opus-5`), or on those models use `tool_choice` `auto`,
  set `strict: true` on the tool, and tell the model in the prompt to call `record_invoice`.
- Validate the tool input with `jsonschema.validate`, then add your own rule: `calculated_total`
  equals the sum of `line_items` (compare in cents, or with `decimal.Decimal`, not raw floats).

**How you know it worked:** `inv_ok_1.txt` comes back as a `record_invoice` input with vendor
"Acme Ltd", date "2026-09-01" and both totals 100.00, and `jsonschema.validate` raises nothing.

### 4. Validate and retry (about 45 minutes)

*Practises: tasks 4.4, 5.2 and 5.5.*

On failure, send back a `tool_result` with `is_error: true` and the exact validation message:

```python
{"type": "tool_result", "tool_use_id": block.id, "is_error": True,
 "content": "line items sum to 90.00 but total is 100.00"}
```

Put the `tool_result` blocks first in that user turn, before any text. Because the document and the
failed `tool_use` are already in the history, the `is_error` result completes the trio the
guide names: the original document, the failed extraction and the specific error.

Allow up to 2 retries, then route the document to a "needs human review" list. Retries fix
format and arithmetic slips; they don't help when the information isn't in the document.

Test it with 5 documents, two of which you've broken on purpose: one with an arithmetic error
(should pass after a retry) and one with the required vendor genuinely missing (should end up
on the review list).

**How you know it worked:** if the first attempt copies 100.00 into `calculated_total`,
`inv_bad_math.txt` prints a failed attempt with "line items sum to 90.00 but total is 100.00",
then a passing one with `calculated_total` 90.00, `stated_total` 100.00 and
`totals_conflict` true. (If the first attempt already gets 90.00, it passes straight away;
`totals_conflict` is what you check.) `inv_no_vendor.txt` prints two failed retries and
then appears on the review list.

## Checks (about 30 minutes)

*Practises: tasks 1.3 and 5.1–5.3.* Expected results are in brackets.

- Remove the retry and run all 5 invoices. [`inv_bad_math.txt` now ends as a failure or goes
  straight to review.] Then put the retry back.
- Give the extractor the search tool too. [It may call `search_notes` instead of, or before,
  `record_invoice`, or try to look up the missing vendor.] Then take the tool away.
- Make `search_notes` raise an error. [The coordinator receives `{"status": "error", "error":
  ..., "partial_results": [...]}` and says it couldn't search, rather than answering as if the
  notes were empty.]

## Common traps

| Trap | Symptom you'll see |
| --- | --- |
| Stopping on a turn counter | Answers get cut off, or the loop keeps going after the answer |
| Sending each `tool_result` as its own user turn, or putting text before them | A 400 error such as "tool_use ids were found without tool_result blocks immediately after"; all `tool_result` blocks go first in one user turn ([parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use), Tier 1) |
| Forcing `tool_choice` on a model that rejects it | A 400 error on the first extractor call; switch model or use `auto` + `strict: true` |
| Dropping the assistant turn before the results | A 400 error: `tool_result` with no matching `tool_use` |
| Treating `max_tokens` as success | Half-finished answers or cut-off JSON |
| Required, non-nullable `date` | The model invents a date for an undated invoice |
| Retrying without the exact error | The same wrong total comes back each time |
| Retrying missing data forever | `inv_no_vendor.txt` burns turns and never finishes |
| Comparing totals as raw floats | A correct invoice fails on 0.1 + 0.2 style rounding |
| Passing the whole transcript back to the coordinator | The coordinator's context fills up fast |
| Empty "success" on a failed search | The coordinator says "no notes found" when the search actually broke |

Sources: CCAR-F official exam guide v1.0 (Tier 1), task statements 1.1–1.3, 2.3, 4.1–4.4,
5.1–5.3 and 5.5, and Exercises 3 and 4;
[tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools),
[parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use) and
[handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
(Tier 1, check the current docs);
[structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
(Tier 1; a separate feature from tool-based extraction; check the current docs).

## Next

Next: [SIM-04](../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-04-multi-agent-research.md).

## What I learned

-

## Decision-variant failure acceptance

Use the existing synthetic fixture and a disposable local state. Retain input, trace, failed check and recovery evidence; these tests do not authorize production effects.

- **FV-03:** Omit the upstream evidence from one specialist brief. The reviewer must identify the unsupported finding; send a complete bounded packet and recheck. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.3.md#variant-fv-03).
- **FV-21:** Supply schema-valid amount 900 against source 90. Source/semantic validation must fail even when shape passes. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md#variant-fv-21).
- **FV-22:** Use a contradictory source total. Preserve the discrepancy and stop at the declared retry budget instead of inventing a reconciled number. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md#variant-fv-22).
- **FV-27:** Fail a mandatory specialist source. Preserve successful findings while blocking its dependent conclusion. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.3.md#variant-fv-27).


**Runnable pilot fixtures:** Run `python3 decision_variant_fixtures.py` from this lab directory. The synthetic script injects target/amount/expiry changes (FV-04), a schema-valid wrong amount (FV-21), and malformed/error/stale-commit CI reports (FV-18). No network or production effects occur. Its declared envelope is a teaching fixture; inspect the actual installed CLI contract before adapting it.

[Download the complete synthetic decision-variant fixture](../../downloads/decision_variant_fixtures.py). Save it in a disposable folder and run `python3 decision_variant_fixtures.py`. This validates fictional application contracts, not authenticated SDK/API behavior.


<a id="benchmark-evidence-tasks"></a>
## Objective evidence tasks — predict, inspect, explain

**Optional offline files:** [Python inspector](site:downloads/benchmark_exercises.py) and [synthetic fixture data](site:downloads/benchmark-fixtures.json). Save both beside each other; run the script with Python 3. The output validates only the controlled example, not Claude runtime behavior.

These original tasks extend this existing LAB without replacing its integration setup. Each contains its own input, failure and checkable result. You can read them without installation. Optional Python replay is offline; live tool routing, permissions, rule loading and third-party services remain unverified until you run those integration steps.

- [1.1: Objective 1.1 — Build an agentic loop that knows when to continue](#benchmark-exercise-1-1)
- [1.2: Objective 1.2 — Coordinate specialists without losing the whole question](#benchmark-exercise-1-2)
- [1.3: Objective 1.3 — Spawn agents with complete, attributable context](#benchmark-exercise-1-3)
- [4.2: Objective 4.2 — Apply few-shot prompting to improve output consistency and quality](#benchmark-exercise-4-2)
- [4.3: Objective 4.3 — Enforce structured output using tool use and JSON schemas](#benchmark-exercise-4-3)
- [4.4: Objective 4.4 — Implement validation, retry, and feedback loops for extraction quality](#benchmark-exercise-4-4)
- [4.5: Objective 4.5 — Design efficient batch processing strategies](#benchmark-exercise-4-5)


<a id="benchmark-exercise-1-1"></a>
### Worked evidence task — 1.1: test the boundary

**Original technical decision.** A response contains text, a tool-use request, then a timeout and a truncated continuation. Which lifecycle policy preserves correlation without treating generation interruption as business completion?

**In everyday terms:** A readable sentence is not a transaction receipt. A timeout still belongs to the requested tool; do not lose its identity.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "responses": [
    {
      "text": "I will check",
      "stop_reason": "tool_use",
      "id": "t17"
    },
    {
      "tool_result_for": "t17",
      "status": "timeout"
    },
    {
      "stop_reason": "max_tokens"
    }
  ],
  "task_complete": false
}
```

#### Break, choose, repair, prove

1. **Break:** Replay mixed text and tool requests, correlated tool results and interrupted generation. Name the exact failed assumption before proposing another component.
2. **Choose:** Keep assistant tool requests and matching results together; classify interruption separately from a finished model turn. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** In this fixture end_turn ends the normal model turn. Define separate policies for paused continuation, truncation, refusal, stop sequence and budget/cancellation exits; none alone proves business task completion. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.1.md#lifecycle) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.1 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.1` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "tool_request_ids": [
    "t17"
  ],
  "failed_result_ids": [
    "t17"
  ],
  "last_stop": "max_tokens",
  "business_complete": false,
  "next_policy": "bounded continuation or documented partial stop; not success"
}
```

**Why this matters:** A readable sentence is not a transaction receipt. A timeout still belongs to the requested tool; do not lose its identity. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview) · [Messages API Reference](https://platform.claude.com/docs/en/api/messages). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-1-2"></a>
### Worked evidence task — 1.2: test the boundary

**Original technical decision.** A coordinator receives security and cost findings for a comparison that also requires migration analysis. Which completion condition should govern synthesis?

**In everyday terms:** Two useful reports can still leave one part of the question unanswered.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "required": [
    "security",
    "cost",
    "migration"
  ],
  "returned": [
    "security",
    "cost"
  ],
  "deadline_minutes": 15
}
```

#### Break, choose, repair, prove

1. **Break:** Give three requested dimensions but only two specialist reports. Name the exact failed assumption before proposing another component.
2. **Choose:** Compare returned dimensions with the required coverage set, and request only the missing investigation. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Coordinator identifies the missing dimension before claiming a complete comparison. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.2.md#scope) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.2 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.2` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "missing": [
    "migration"
  ],
  "complete": false
}
```

**Why this matters:** Two useful reports can still leave one part of the question unanswered. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-1-3"></a>
### Worked evidence task — 1.3: test the boundary

**Original technical decision.** A fresh synthesis specialist receives a claim without a source locator. Which handoff contract makes its output attributable under isolated context?

**In everyday terms:** The next specialist cannot read a conversation it never received.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "specialist": "synthesizer",
  "prior_context": null,
  "finding": {
    "claim": "unit cost 8",
    "locator": null
  },
  "allowed_tools": [
    "merge"
  ]
}
```

#### Break, choose, repair, prove

1. **Break:** Pass a finding first without, then with, its source locator and explicit tool boundary. Name the exact failed assumption before proposing another component.
2. **Choose:** Send the bounded task, source locator and capability boundary explicitly; flag unsupported claims. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Fresh specialist can identify the source and task without inheriting parent conversation. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.3.md#packet) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.3 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.3` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "source_attributable": false,
  "parent_context_available": false,
  "allowed_tools": [
    "merge"
  ],
  "repair_required": [
    "task",
    "source locator",
    "tool boundary"
  ]
}
```

**Why this matters:** The next specialist cannot read a conversation it never received. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [sessions guide](https://code.claude.com/docs/en/agent-sdk/sessions) · [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-4-2"></a>
### Worked evidence task — 4.2: test the boundary

**Original technical decision.** An extraction prompt has table and prose examples, but a field is split across two paragraphs. Which evaluation establishes transfer beyond memorized formatting?

**In everyday terms:** The new layout checks whether the rule was learned rather than one example copied.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "source_examples": [
    "amount in table",
    "amount in prose"
  ],
  "unseen": "same field split across two paragraphs",
  "format": "fixed record; missing evidence nullable"
}
```

#### Break, choose, repair, prove

1. **Break:** Teach one extraction boundary with varied examples and test an unseen arrangement. Name the exact failed assumption before proposing another component.
2. **Choose:** Use the unseen arrangement as a separate test and require supporting text for the fixed record. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Improve consistency without treating examples as proof of truth or a universal remedy. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.2.md#worked-example) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.2 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.2` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "source_layouts": 2,
  "unseen_layout": "same field split across two paragraphs",
  "record_rule": "fixed record; missing evidence nullable",
  "unseen_accuracy_observed": false
}
```

**Why this matters:** The new layout checks whether the rule was learned rather than one example copied. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-4-3"></a>
### Worked evidence task — 4.3: test the boundary

**Original technical decision.** An extraction object passes schema validation but reports 12000 minor units where the source supports 1200 and no reference. Which validator must still fail?

**In everyday terms:** The JSON can be well formed and still say the wrong amount.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "schema_valid": true,
  "output": {
    "amount_minor": 12000,
    "reference": null
  },
  "source_supported_amount_minor": 1200,
  "source_reference_absent": true
}
```

#### Break, choose, repair, prove

1. **Break:** Return schema-valid data with an unsupported amount and an absent optional field. Name the exact failed assumption before proposing another component.
2. **Choose:** Validate evidence and units after shape validation; retain a nullable absent reference. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Shape validation passes while evidence validation fails; unknown remains representable. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.3.md#illustrative-output-contract) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.3 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.3` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "shape_pass": true,
  "amount_supported": false,
  "reference_unknown_preserved": true,
  "accept": false
}
```

**Why this matters:** The JSON can be well formed and still say the wrong amount. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [define-tools page](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use) · [Tool Use (Function Calling)](https://platform.claude.com/docs/en/build-with-claude/tool-use). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-4-4"></a>
### Worked evidence task — 4.4: test the boundary

**Original technical decision.** Two line items total 50 while the output claims 60, and one retry is allowed. Which correction request stays grounded when no missing item exists?

**In everyday terms:** Tell it exactly what disagrees; do not ask it to make the numbers look right.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "line_items": [
    20,
    30
  ],
  "stated_total": 60,
  "retry_budget": 1,
  "source_has_missing_item": false
}
```

#### Break, choose, repair, prove

1. **Break:** Provide failed output, precise validation error and source, then remove the supporting fact. Name the exact failed assumption before proposing another component.
2. **Choose:** Send the exact arithmetic mismatch and source, bound the correction attempt, and never invent a balancing item. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Bound correction attempts; stop inventing values when evidence is absent; preserve failed result for diagnosis. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.4.md#foundation) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.4 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.4` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "computed_sum": 50,
  "stated_total": 60,
  "mismatch": true,
  "retry_budget": 1,
  "invent_missing_item": false,
  "preserve_failed_output": true
}
```

**Why this matters:** Tell it exactly what disagrees; do not ask it to make the numbers look right. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) · [Tool Use (Function Calling)](https://platform.claude.com/docs/en/build-with-claude/tool-use). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-4-5"></a>
### Worked evidence task — 4.5: test the boundary

**Original technical decision.** Batch results arrive `D3`,`D1`,`D2` with success, denial and timeout outcomes. Which retry strategy preserves completed work and item identity?

**In everyday terms:** Do not match results by their arrival position or rerun everything.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "input_ids": [
    "D1",
    "D2",
    "D3"
  ],
  "output_order": [
    "D3",
    "D1",
    "D2"
  ],
  "outcomes": {
    "D1": "success",
    "D2": "permission_denied",
    "D3": "timeout"
  },
  "retry_budget": 1,
  "deadline": "next-day review"
}
```

#### Break, choose, repair, prove

1. **Break:** Process an out-of-order mixed result stream with success, permanent error and retryable error. Name the exact failed assumption before proposing another component.
2. **Choose:** Join by document ID, retain success, route denial to authorization and retry only the transient item within budget. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Join by request identity, preserve successes and resubmit only justified failures; report partial completion. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.5.md#supplied-batch-pilot-and-result-fixtures) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.5 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 4.5` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "joined": {
    "D1": "success",
    "D2": "permission_denied",
    "D3": "timeout"
  },
  "preserve": [
    "D1"
  ],
  "authorization_queue": [
    "D2"
  ],
  "retry": [
    "D3"
  ],
  "rerun_successes": false,
  "completion": "partial"
}
```

**Why this matters:** Do not match results by their arrival position or rerun everything. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [batch processing docs](https://platform.claude.com/docs/en/build-with-claude/batch-processing) · [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>