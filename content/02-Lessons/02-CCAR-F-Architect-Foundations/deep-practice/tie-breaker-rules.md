# Tie-breaker rules for close answers

**Picture the application:** An invoice pipeline fails, and several proposed repairs sound plausible: revise instructions, adjust an output contract or redesign the workflow. Start with the actual input, failure and required result. Use the comparisons below to identify the mechanism that fits the case, rather than memorizing a universally winning answer.

**Why this exists.** Several options can look plausible. Compare them against the stated constraints, requested first step and failure mechanism. These are diagnostic heuristics, not universal answer rules or claims about undisclosed exam items. Sources: the official exam guide v1.0 (July 2026) and its task statement wording, plus Anthropic docs where named. Rules 1 and 4 also draw on Tier 3 candidate reports (blog posts by people who took the exam), which are never the only source for a fact.

**How to use it.** Read it once before a mock. When you review a wrong answer, name the rule it broke.

---

**1. Read the last sentence first.**
- *Example:* A 6-line story about an invoice pipeline ends "What should the team do **first**?" Now you know you're picking a first step, not the full redesign.
- *Trap it beats:* Answering the problem you imagined from the setup instead of the question actually asked.

**2. Pick the best *first* step.**
- *Example:* A `fetch_invoice` tool starts returning HTTP 503 and the agent gives up with "something went wrong". Before adding a queue, a fallback service or a second agent, first make the tool return `is_error: true` with "upstream unavailable, retryable, try again in 30 s" so the agent can act on it.
- *Trap it beats:* A big, correct-sounding redesign when a small step would solve it.

**3. Match the size of the fix to the size of the problem.**
- *Example:* On some invoices the PO number is genuinely absent and the model invents one. Make `po_number` nullable and route `null` to review. On other invoices the `total` is a schema-valid number that disagrees with the line items: nullable can't catch that, because the wrong value still matches the schema. Add a semantic check in code (line items sum to the printed total; on conflict, flag for review). Supported constrained-output modes enforce their schema shape, not source truth; handle refusal/truncation/error states before consumption ([Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), primary source, checked 2026-10-17). Neither problem needs a multi-agent rebuild.
- *Trap it beats:* Over-engineering. Extra agents or services need a requirement that justifies their coordination cost; a small patch is insufficient when the actual cause crosses boundaries.

**4. Remove a whole class of failure, don't just make it rarer.**
- *Example:* A missing bracket or stray sentence is a syntax/shape failure. The saved guide TS 4.3–4.4 describes schema-based tool use as its reliable structured-extraction approach. Keep that assessed concept separate from current implementation: ordinary tool use with a schema alone is not strict validation. Current supported strict tool inputs use `strict: true`; structured final answers use their documented output-format mechanism. Both have supported-schema limits and error/termination cases. Wrong totals still require source and business validation. See [scope versus current implementation](conditions-and-errors.md#exam-answer-vs-today) and [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use).
- *Trap it beats:* Repeated prompting for a hard shape constraint when a supported constrained-output mechanism addresses it. Conversely, neither a schema nor a larger architecture repairs an absent source fact.

**5. Enforce mandatory action rules at an executable boundary; use instructions to explain behavior.**
- *Example:* "Never refund over $500 without approval." A correctly matched pre-action hook can deny a prohibited call before execution; the action service should also check trusted identity and policy. Test alternate tool paths, stale inputs and fail-open behavior. A line in the prompt guides behavior but does not enforce this financial limit. ([hooks](https://code.claude.com/docs/en/hooks))
- *Trap it beats:* "Add it to `CLAUDE.md` in bold" or "repeat it in the system prompt". Hooks and deny rules enforce their configured scope, not every imaginable action path or semantic policy interpretation. PostToolUse cannot undo an already performed side effect.

**6. Distinguish tool selection from execution order and authorization.**
- *Example:* Under the saved guide's supported-tool-choice model, `{"type":"any"}` requires some provided tool; `{"type":"tool","name":"extract_metadata"}` selects that named tool for the request. `auto` permits a direct answer. Named selection can establish the requested first call, but your runtime must execute it, return its result, validate prerequisite state, and only then allow enrichment. Neither `any` nor named selection authorizes the action or proves the prerequisite completed.
- *Trap it beats:* Changing a schema when the problem is non-selection, or treating selection as workflow enforcement. Current forced-choice compatibility depends on the model and thinking configuration; some reject `any`/named choice, others support it. Check [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools), not a blanket “newest models return 400” shortcut.

**7. Let the model say "unknown".**
- *Example:* Invoices sometimes have no PO number. Make `po_number` `"type": ["string", "null"]` and say "use null if not present". Enums get `"other"` plus a detail field.
- *Trap it beats:* A required, non-null field. It pushes the model to invent a value. That's a made-up fact, which is worse than a blank.

**8. Retries fix format, not missing data.**
- *Example:* Validator says "date must be YYYY-MM-DD": retry with that exact error. The total is missing from the scan: retrying won't create it; route to a person.
- *Trap it beats:* "Retry up to 5 times until all fields are filled."

**9. Check facts and maths in code, not by asking the model.**
- *Example:* Line items add to 1,240; the stated total is 1,420. Code adds them up, records both values, flags the mismatch, and retries once with the specific gap.
- *Trap it beats:* "Ask Claude to make the totals match" (it may change the real number) or "trust the stated total".

**10. Targeted routing beats random sampling.**
- *Example:* Send to review when a field's **calibrated** confidence is low (field-level scores checked against a labelled validation set; guide TS 5.5), a required field is `null`, totals differ, or the document type is new. Spot-check a small sample of the rest.
- *Careful:* this is for extraction review. For escalating support cases (TS 5.2), the guide calls "self-reported confidence scores" "unreliable proxies"; there, raw self-reported confidence is the distractor and explicit escalation criteria win.
- *Trap it beats:* "Review a random 10%." It spends review time on easy cases and misses the risky ones.

**11. Diagnose information loss or capability limits before changing model capacity.**
- *Example:* The agent forgets facts from turn 3 in a long chat. Keep a short "key facts" block (or summary) that you send every call. Preserve exact facts and provenance outside lossy summaries.
- *Trap it beats:* Paying more to hide a design problem. A larger window or more capable model is reasonable when measured context/capability limits remain after evidence and prompt defects are addressed. Compare quality, latency and cost on representative tasks; there is no blanket “bigger is wrong” answer rule.

**12. Fix tool descriptions before adding few-shot examples.**
- *Example:* Two MCP tools, `search_docs` and `search_tickets`, both say "Searches for information." The agent keeps searching tickets for product how-to questions. Rewrite both descriptions: what each searches, what it returns, and when to use the other one instead.
- *Trap it beats:* "Move to a larger model" or "rename the tools only" as the first move: neither tells the agent what each tool searches. Clear descriptions are the relevant repair for this demonstrated ambiguity; model changes can be appropriate for a measured capability gap instead. ([define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools))

**13. The smallest fix at the root cause wins.**
- *Example:* The hook "should block" but doesn't. Its script exits `1`. Change it to `exit 2`. Don't add a second hook, a prompt rule or a wrapper. ([hooks](https://code.claude.com/docs/en/hooks))
- *Trap it beats:* Patches on the symptom, stacked on top of a bug nobody fixed.

**14. Use independent review when shared assumptions are the risk.**
- *Example:* In CI, one `claude -p` run writes the fix. A second, independent run with its own review instructions checks it.
- *Trap it beats:* "Ask the same session to double-check its work." It can share blind spots. A same-session focused pass still has value for another review dimension; an independent session provides a stronger separation when that is the requirement (guide TS 4.6).

**15. Batch API only when nobody is waiting.**
- *Example:* A weekly re-tag of 40,000 product descriptions → Message Batches (50% cheaper, up to 24 hours). A support agent answering a live customer → normal API. ([batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing))
- *Trap it beats:* "Batch to save money" on a job where a person is waiting, or an agent loop that needs tool round trips.

**16. Errors should carry context. Never swallow them, never send just "failed".**
- *Example:* A `lookup_order` tool gets an order number in the wrong format. Instead of `"failed"`, it returns `is_error: true` with "order_id must look like ORD-12345; you sent 12345". The agent fixes the call on its own.
- *Trap it beats:* A bare `"failed"` (the agent can't tell retry from give-up), or catching the error and returning an empty list as if no orders exist (hides the failure). ([tool errors](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls))

---

## Timing rule (exam day)

- **60 questions in 120 minutes = about 2 minutes each.** (Official CCAR-F exam guide v1.0, "Number of items" and "Time limit".)
- **Read the last sentence first** (rule 1), then the options, then the story.
- **At about 2 minutes, flag it and move on.** Pick your best guess first, so nothing is left blank.
- **Flag and review inside each scenario** before moving on (field report, tier F: going back to an earlier scenario may be hard). Keep a few minutes at the very end only if the exam lets you go back. The exam guide doesn't say how navigation works, so treat this as advice, not an official rule. Same advice as [Lesson 0, orientation](../L00-orientation.md).
- **Multi-select questions tell you how many to pick.** The official CCAR-F exam guide v1.0, under "Item format", says each item "states how many responses to select" (exam wording). Pick exactly that many. Check the number before you submit.
- **Don't change an answer** on a second pass unless you can name the rule above that proves it wrong.

**Freshness and scope:** Targeted mechanism corrections checked against primary docs 2026-10-17. The saved July guide defines study scope; latest blueprint revision and every runtime detail on this page have not been independently recertified.