# CCAR-F SIM-02 — Scenario 1: Customer Support Resolution Agent

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

### Stage 1 — Two tools sound equally useful

A service assistant handles a balance question and an address change. Both tools are named `manage_account` and described as “manage customer data.” A balance request sometimes triggers the write operation. The working one-tool demo hid this ambiguity.

**Original exam-style practice — choose ONE.** Which tool-interface change most directly improves selection reliability while preserving the read/write boundary?

A. Use one generic tool and explain all differences in a long system prompt.

B. Give each capability a distinct purpose, precise description, input schema and side-effect boundary.

C. Add more overlapping aliases so the model has more options.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** Name the actual job, such as read balance versus propose address change, and state when each is appropriate. A hides the distinction inside one broad interface; C increases confusion. A schema describes accepted arguments; authorization is a separate check.

**Follow the changed path:**

```text
customer need → distinct tool purpose → typed arguments → runtime authorization → service result
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Use a balance request and an address request. Record the selected capability and arguments separately from permission and execution outcome. A selected write tool does not authorize the write.

</details>

**Changed-constraint decision — choose ONE before revealing:** The model chooses the correct tool but supplies an invalid account ID. A: redesign names alone; B: validate arguments and return a specific correctable error without executing.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Correct selection and valid arguments are different requirements. Repair the failing layer.

</details>

**Objective connections:** [2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md), [2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.3.md).

### Stage 2 — A proposal becomes a money movement

The customer now requests a refund. A person approves USD 80 for ORD4, but a later proposal changes to USD 90. The old design remembers only “approved: yes.” That broad flag would let a changed action through.

**Original exam-style practice — choose ONE.** Which control best enforces approval scope before execution of a side-effecting tool?

A. Instruct Claude to remember the approved amount.

B. Validate the current principal, order, amount and approval validity against the bound proposal in the runtime/backend before submitting the action.

C. Execute first and inspect the model explanation afterward.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The program compares this exact action with what was approved. A model reminder can help behavior but cannot replace that gate. C finds the problem after money may already move. A hook can intercept an attempted call; business authorization still belongs at the authoritative service boundary.

**Follow the changed path:**

```text
proposal → approval bound to exact action → runtime/backend gate → business API
changed target, amount or expired approval → deny or request new approval
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Keep the approval record and action fields. Changing one field must block submission; a matching permitted action still needs a real business receipt before being called settled.

</details>

**Changed-constraint decision — choose ONE before revealing:** The write timed out after submission. A: blindly resubmit; B: inspect the business operation status with the operation key before deciding whether retry is safe.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Timeout means the caller lacks a result, not that the operation failed. Reconciliation prevents a duplicate effect.

</details>

**Objective connections:** [1.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.4.md), [1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md), [1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.7.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** A customer contacts support about a return, a billing dispute or an account problem. The service receives their request and relevant account information; its output should be a useful resolution or an honest handoff. This simulation asks you to choose the architecture behind that familiar interaction.

**Build the application picture first:** [AS 01 action service](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-01-action-service.md) · [AS 08 resumable case](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-08-resumable-case.md)

**Primary domains:** 1 Agentic Architecture, 2 Tools and MCP, 5 Context and Reliability ·
**Decisions:** 10 · **Time:** 20 min for the decisions, plus about 5 for the twist and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 1, Tier 1)

You're building a customer support resolution agent with the Claude Agent SDK. It handles
high-ambiguity requests such as returns, billing disputes and account issues. It reaches your
backend through custom MCP tools: `get_customer`, `lookup_order`, `process_refund` and
`escalate_to_human`. The target is **80% or more first-contact resolution, while knowing when to
escalate**.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. The loop keeps running after the answer is complete. What should decide when it stops?
2. In testing, the agent calls `lookup_order` four times in a row for the same order and never
   answers. Your loop code logs each tool's output and then sends the next request. What's wrong?
3. Refunds over $500 must never go through automatically. How do you guarantee that?
4. One tool returns order dates as Unix time and another as ISO 8601. How do you make them
   consistent for the model?
5. `lookup_order` times out. What should the tool send back?
6. `get_customer` returns 3 customers named "J. Smith". What does the agent do?
7. A customer's first message is "I want a human." What does the agent do?
8. A customer wants their shipping fee back because a courier strike delayed the parcel. The
   policy covers damage and late delivery by your own carrier, and says nothing about strikes at a
   third-party courier. What does the agent do?
9. After a long conversation, the summary has lost the $247.83 amount and the order number. How do
   you keep facts like these?
10. The agent hands a case to a human agent. What does the handoff contain?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | The loop keeps running after the answer is complete | **Continue on `stop_reason == "tool_use"` and stop on `"end_turn"`** | Stop when the text says "resolved"; a 10-iteration cap as the main stop; stop whenever the response contains text | D1 1.1 Agentic loops | [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 2 | `lookup_order` is called four times in a row and the agent never answers; the loop logs tool output but doesn't send it back | **Append each tool's output to the conversation as a `tool_result` (matched by `tool_use_id`) before the next request.** The model can only reason about results it can see. Keep an iteration cap, but only as a safety net. | Add "never call the same tool twice" to the system prompt; switch to a bigger model; cap the loop at 3 iterations and return whatever it has | D1 1.1 Agentic loops | [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 3 | Refunds over $500 must never be automatic | A **tool-call interception hook** that blocks them and redirects to `escalate_to_human` | "Never refund over $500" in the system prompt; ask the model to confirm the amount before each refund; let refunds through and flag the big ones in a daily monitoring report | D1 1.5 Agent SDK hooks | [Lesson 1, section 1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 4 | Order dates come back as Unix time from one tool and ISO 8601 from another | A **PostToolUse hook that normalizes them** before the model sees them | Tell the model in the prompt to convert every date; convert the dates in a PreToolUse hook, which runs before the tool is called and never sees its result; ask the backend team to change one API, which takes weeks and doesn't cover the next tool | D1 1.5 Agent SDK hooks | [Lesson 1, section 1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 5 | `lookup_order` times out | Return **`isError` with `errorCategory: transient` and `isRetryable: true`**, as distinct from "no orders found" | Return an empty list; a generic "Operation failed"; retry forever inside the tool until the backend answers | D2 2.2 Structured error responses; D5 5.3 Error propagation | [Lesson 2, section 2.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md), [Lesson 5, section 5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 6 | `get_customer` returns 3 customers named "J. Smith" | **Ask the customer for another identifier** (email, order number) | Pick the most recent account; pick the one with the most orders; tell the model to "be careful" and choose the likeliest | D5 5.2 Escalation and ambiguity | [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 7 | A customer says "I want a human" at the first turn | **Escalate right away**, without investigating first | Try to solve it first; escalate only if they sound angry; offer a discount to keep them with the agent | D5 5.2 Escalation and ambiguity | [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 8 | Shipping-fee refund after a third-party courier strike; policy covers only your own carrier's delays | **Escalate, because the policy is silent on this case.** The agent shouldn't invent policy. | Approve it, since first-contact resolution counts; refuse outright, since it isn't listed; let the agent decide from "the spirit of the policy" | D5 5.2 Escalation and ambiguity | [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 9 | After a long conversation, the summary loses the $247.83 amount and the order number | A **persistent "case facts" block** outside the summarized history; trim tool output to the relevant fields | A bigger context window; "summarize carefully" in the prompt; summarize more often | D5 5.1 Preserving conversation context | [Lesson 5, section 5.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 10 | Handing off to a human agent | A **structured handoff**: customer ID, root cause, amount, recommended action. The human can't see the transcript. | Forward the whole transcript; "customer needs help"; let the human re-ask the customer from the start | D1 1.4 Multi-step workflows and handoff | [Lesson 1, section 1.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |

**Scoring:** 8 or more is a pass. Decisions 2 and 3 are the heart of the scenario: *the loop only
works if the model sees each tool result*, and *deterministic beats probabilistic*.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 1 and task statements 1.1, 1.4, 1.5, 2.2, 5.1–5.3 (Tier 1); Claude API tool-use docs on
platform.claude.com for `tool_result` handling (Tier 1). Taught in lessons
[L01](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md),
[L02](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) and
[L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: the handoff summary keeps arriving half empty

**What changed:** human agents say some escalations reach them with a blank or half-filled case
summary, so they have to ask the customer everything again. The system prompt already says
"always fill in the case summary before escalating".

**Question:** how do you make sure every handoff is complete?

<details><summary><b>Answer and why</b></summary>

**Enforce it in code, not in the prompt.** Make the handoff fields (customer ID, root cause,
refund amount, recommended action) required in the `escalate_to_human` tool's input schema. Add a
check before the call runs (for example a `PreToolUse` hook) that rejects the call when a field is
empty and tells the agent which ones are missing. The human agent can't see the transcript, so the
summary has to be complete every time.

**Why the others lose:** giving human agents the full transcript moves the work onto people, and
long transcripts bury the facts. Adding "check your summary carefully" to the prompt is still a
request, not a guarantee. When a rule must always hold, code beats the prompt.

**Tests:** Domain 1, task statement 1.4 (multi-step workflows and handoff); also 1.5 (Agent SDK hooks).

**Lesson:** [Lesson 1, section 1.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#14-enforcement-and-handoff) · [Deep practice, Domain 1](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/01-agentic-architecture-and-orchestration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 1.4 (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: the loop keeps running after the answer is complete**

- **What's going on:** the agent is done, but the loop doesn't know it.
- **Under the hood:** every response carries a `stop_reason` (why the model stopped). `"tool_use"` means it wants a tool run; `"end_turn"` means it has finished. That field is the signal, not the words in the reply.
- **How to make the call:** if `stop_reason` is `"tool_use"`, run the tool and loop again; if it's `"end_turn"`, stop. Keep an iteration cap only as a safety net. Exam wording (task statement 1.1): "Implementing agentic loop control flow that continues when stop_reason is "tool_use" and terminates when stop_reason is "end_turn"".
- **Why the tempting answers are wrong:**
  - **Stop on "resolved":** reading the words is a guess.
  - **10-iteration cap:** cuts long cases short; a cap is a backstop, not the stop.
  - **Stop on any text:** a reply can hold text and a tool call together.
- **Go deeper:** [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#11-the-agentic-loop)

**Decision 2: the same lookup four times, and never an answer**

- **What's going on:** the agent asks a question but never hears the answer.
- **Under the hood:** the API remembers nothing between requests, so each request must carry the whole conversation. A tool's answer goes back as a `tool_result` block, tagged with the `tool_use_id` (the ID of the call it answers).
- **How to make the call:** if the model repeats the same call, check that the last result was appended as a `tool_result` before the next request. If it was, look at the tool itself. Exam wording (task statement 1.1): "Adding tool results to conversation context between iterations so the model can incorporate new information into its reasoning".
- **Why the tempting answers are wrong:**
  - **"Never call twice" rule:** hides the symptom; it still hasn't seen the order.
  - **Bigger model:** no model can read a result it was never sent.
  - **Cap at 3:** stops the loop with no answer.
- **Go deeper:** [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#11-the-agentic-loop)

**Decision 3: refunds over $500 must never be automatic**

- **What's going on:** a money rule that has to hold every single time.
- **Under the hood:** a hook is your own code that runs at set points in the agent loop. A hook on outgoing tool calls sees the call before it runs, so it can block it and tell the agent why.
- **How to make the call:** if a rule must never be broken, put it in a hook that blocks the call and sends the case to `escalate_to_human`. If it's guidance the model may sometimes miss, a prompt is enough. Exam wording (task statement 1.5): "Implementing tool call interception hooks that block policy-violating actions (e.g., refunds exceeding $500) and redirect to alternative workflows (e.g., human escalation)".
- **Why the tempting answers are wrong:**
  - **Prompt rule:** works most of the time, not every time.
  - **Model confirms the amount:** still the model deciding.
  - **Daily report:** finds the refund after the money has gone.
- **Go deeper:** [Lesson 1, section 1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#15-agent-sdk-hooks)

**Decision 4: one tool says Unix time, the other ISO 8601**

- **What's going on:** two tools write dates two different ways.
- **Under the hood:** a `PostToolUse` hook runs after a tool returns, before the model works with the result, so it's where results get reshaped. A `PreToolUse` hook runs before the call and sees only the inputs.
- **How to make the call:** if the fix is to what a tool returns, use `PostToolUse`; if it's to the call itself, use `PreToolUse`. Here, convert both formats to one in `PostToolUse`. Exam wording (task statement 1.5): "Implementing PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools before the agent processes them".
- **Why the tempting answers are wrong:**
  - **Prompt says convert:** the model converts most times, not every time.
  - **`PreToolUse` hook:** runs before the call and never sees the result.
  - **Change the backend API:** takes weeks; the next tool brings a new format.
- **Go deeper:** [Lesson 1, section 1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#15-agent-sdk-hooks)

**Decision 5: `lookup_order` times out**

- **What's going on:** the order system didn't answer in time.
- **Under the hood:** an MCP (the standard tool-plug-in protocol) tool marks a failed call with `isError` (a "call failed" marker). Fields you add, like `errorCategory` and `isRetryable`, tell the agent what kind of failure it was and whether trying again could work.
- **How to make the call:** if the call failed, return `isError` with a category and a retry flag; a timeout is `transient` and retryable. If the call worked and found nothing, return a normal empty result. Exam wording (task statement 2.2): "Returning structured error metadata including errorCategory (transient/validation/permission), isRetryable boolean, and human-readable descriptions".
- **Why the tempting answers are wrong:**
  - **Empty list:** says "no orders" when the truth is "couldn't check".
  - **"Operation failed":** the agent can't tell retry from give up.
  - **Retry forever in the tool:** the customer waits and the agent never decides.
- **Go deeper:** [Lesson 2, section 2.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#22-structured-errors), [Lesson 5, section 5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#53-passing-errors-between-agents)

**Decision 6: three customers named "J. Smith"**

- **What's going on:** three people share a name, and a guess could open the wrong account.
- **Under the hood:** the tool did its job: it returned every match. Only the customer knows which account is theirs, so any pick the agent makes on its own is a guess.
- **How to make the call:** if a lookup returns more than one match, ask for another identifier (email, order number) and look again; if exactly one matches, carry on. Exam wording (task statement 5.2): "Instructing the agent to ask for additional identifiers when tool results return multiple matches, rather than selecting based on heuristics".
- **Why the tempting answers are wrong:**
  - **Most recent account:** a guess with a rule attached.
  - **Most orders:** still a guess.
  - **"Be careful" and pick:** careful guessing is still guessing.
- **Go deeper:** [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#52-escalation-and-ambiguity)

**Decision 7: "I want a human" in the first message**

- **What's going on:** the customer has said exactly what they want.
- **Under the hood:** escalation triggers are about what's asked and what the policy covers, not mood. The exam's listed triggers are a request for a human, a policy gap, and being unable to make progress.
- **How to make the call:** if the customer clearly asks for a human, escalate now, with no investigation first. If they're only frustrated and the issue is simple, offer to help, and escalate if they ask again. Exam wording (task statement 5.2): "Honoring explicit customer requests for human agents immediately without first attempting investigation".
- **Why the tempting answers are wrong:**
  - **Solve it first:** ignores what they asked for.
  - **Only if angry:** mood is an unreliable signal.
  - **Offer a discount:** bargains instead of listening.
- **Go deeper:** [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#52-escalation-and-ambiguity)

**Decision 8: a courier strike the policy never mentions**

- **What's going on:** the rulebook doesn't cover this case.
- **Under the hood:** the agent knows only the policy it was given. When the policy is silent, any yes or no from the agent is a new rule it made up, applied to real money.
- **How to make the call:** if the policy clearly covers the case, act on it; if it's silent or unclear, escalate to a human. Exam wording (task statement 5.2): "Escalating when policy is ambiguous or silent on the customer's specific request (e.g., competitor price matching when policy only addresses own-site adjustments)".
- **Why the tempting answers are wrong:**
  - **Approve for the metric:** buys a resolution by inventing policy.
  - **Refuse outright:** "not listed" isn't the same as "not allowed".
  - **"Spirit of the policy":** the agent still invents the rule.
- **Go deeper:** [Lesson 5, section 5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#52-escalation-and-ambiguity)

**Decision 9: the summary lost $247.83 and the order number**

- **What's going on:** squeezing the chat into a summary squeezed out the numbers.
- **Under the hood:** summarizing condenses text, and exact amounts, dates and IDs blur first. Facts kept in a separate block, sent with every prompt and never summarized, stay exact.
- **How to make the call:** if a fact must stay exact (amount, order number, date), pull it into a "case facts" block sent with each prompt, outside the summarized history. If it's only background chat, the summary can carry it. Also trim tool output to the fields you need. Exam wording (task statement 5.1): "Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent "case facts" block included in each prompt, outside summarized history".
- **Why the tempting answers are wrong:**
  - **Bigger context window:** the summary still loses the numbers.
  - **"Summarize carefully":** a request, not a structure.
  - **Summarize more often:** more squeezing, more loss.
- **Go deeper:** [Lesson 5, section 5.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#51-keeping-the-facts-that-matter-in-long-conversations)

**Decision 10: what the handoff to a human contains**

- **What's going on:** a new person takes over, and they weren't there.
- **Under the hood:** the human agent can't see the transcript. Whatever the escalation passes along is all they get, so it needs fixed fields, not a vague note.
- **How to make the call:** if the person taking over can't see the conversation, send a structured summary: customer ID, root cause, refund amount, recommended action; never just a one-line note or the raw transcript. Exam wording (task statement 1.4): "Compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to human agents who lack access to the conversation transcript".
- **Why the tempting answers are wrong:**
  - **Whole transcript:** buries the facts; the human has to dig.
  - **"Customer needs help":** says nothing they can act on.
  - **Human re-asks:** the customer repeats everything.
- **Go deeper:** [Lesson 1, section 1.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#14-enforcement-and-handoff)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-03](SIM-03-code-generation-claude-code.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-01 — decision checkpoint

A settlement agent receives end_turn after a write returned status=unknown. There are no pending tool calls, but business completion has not been established. What should the application do?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** End this model loop and check operation status through the application recovery path before retrying the write. end_turn ends the model turn, while an unknown business effect still needs reconciliation.

**Base choice:** A support agent has one refund tool call pending. Return tool_result with its matching tool_use_id and continue the conversation; keep the business transaction status separately.

**Changed constraint and recovery:** The model returns end_turn, but the payment request timed out. Stop the model loop; do not describe the refund as committed.

**Failure:** A network timeout leaves operation r-17 unknown. Query r-17 status or reconcile by idempotency key before sending another refund.

**Nearest alternative:** A blind refund retry can duplicate a committed transaction. Model termination is not proof of settlement.

**Conditional cue:** Stop the loop on its signal; settle the effect from its receipt.

**Proof:** Inspect `stop_reason=tool_use; pending_id=t17; operation_id=r17; business_status=unknown` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.1.md#variant-fv-01).

</details>

### SIM-FV-04 — decision checkpoint

A bank customer explicitly requests a human while a transfer dispute is unresolved. The receiving officer cannot read the transcript. What should the agent do?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Escalate with verified identity, unresolved issue, evidence, proposal version and operation status. A complete handoff lets the human continue without guessing current state.

**Base choice:** A finance support workflow proposes a 40-unit credit for account A and proposal v2. Trusted verification, scope and current approval are checked by the action handler before the effect.

**Changed constraint and recovery:** The target changes to account B or amount changes to 80. Invalidate the prior approval and request the newly scoped authorization.

**Failure:** Verification expires between draft and execute. Reject the protected action and hand off the complete case with blocked status.

**Nearest alternative:** A prompt reminding Claude to verify cannot enforce the backend boundary. Read-only investigation follows its own access policy.

**Conditional cue:** Bind identity, scope and version; changed target means new gate.

**Proof:** Inspect `gate={account:A,proposal:v2,amount:40,verified:true,approval:current}; requested={account:B,proposal:v2}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.4.md#variant-fv-04).

</details>

### SIM-FV-05 — decision checkpoint

A records deletion must never execute when a legal hold is active. The current proposal checks only after the delete tool succeeds. Which design fixes the timing?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Check the hold in a pre-action application gate or blocking pre-tool hook before deletion. A prevention requirement must be enforced before the side effect.

**Base choice:** A fictional service normalizes a successful date result after the tool returns while retaining the original value and parse status.

**Changed constraint and recovery:** The requirement becomes preventing an irreversible account mutation. Move the authorization check before execution, in the application or supported pre-tool control.

**Failure:** A post-result check finds a bad write already happened. Record the effect and invoke reviewed compensation or escalation; result replacement does not undo it.

**Nearest alternative:** A post-action hook can change model-visible output where supported, but cannot retroactively block the completed effect.

**Conditional cue:** Before prevents; after detects; retain raw evidence.

**Proof:** Inspect `trace=proposal -> precheck -> execute -> effect -> postcheck; raw_date=03/04; locale=unknown` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md#variant-fv-05).

</details>

### SIM-FV-08 — decision checkpoint

A redesign proposes one universal execute tool that accepts arbitrary action strings. The application must enforce separate read and payment capabilities. Which choice best preserves the boundary?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Keep a separate scoped execution capability with an application authorization check. A narrow execution boundary can be enforced independently of model selection.

**Base choice:** A support catalog separates get_balance, draft_credit and execute_credit. Descriptions specify read versus proposal versus mutation, required scope and return status.

**Changed constraint and recovery:** Two tools both say “manage account.” Rename them and tighten schemas/descriptions so capability boundaries are clear.

**Failure:** Claude picks execute_credit for a lookup. Reject the call at the handler, then repair the catalog rather than merely lengthening the prompt.

**Nearest alternative:** A universal tool can conceal prohibited effects and confuse selection; splitting should follow real capability boundaries, not arbitrary tool-count ceilings.

**Conditional cue:** Name the effect; describe the boundary; validate the arguments.

**Proof:** Inspect `get_balance(account_id)->amount; draft_credit(account_id,amount)->proposal; execute_credit(proposal_id,approval)->receipt` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md#variant-fv-08).

</details>

### SIM-FV-09 — decision checkpoint

A campaign creation request times out after transmission; it may have committed and accepts an idempotency key. What should happen before creating another campaign?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Look up the existing operation by its stable key and reconcile status before deciding whether to retry. A potentially committed write needs status reconciliation to avoid duplicates.

**Base choice:** An MCP lookup succeeds with records=[]; report no matching record and clarify filters rather than retrying a supposed outage.

**Changed constraint and recovery:** A timeout is transient and read-only. Retry with a bounded policy. A permission refusal instead requires changed authorization or escalation.

**Failure:** A write times out after submission. Query operation status before retrying; a transient category alone does not establish safe re-execution.

**Nearest alternative:** MCP protocol errors and the application payload are different layers; error strings alone do not define a safe recovery policy.

**Conditional cue:** Empty is evidence; timeout is uncertainty; denied needs authority.

**Proof:** Inspect `application_result={status:success,records:[]}; failure={category:permission,retryable:false}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md#variant-fv-09).

</details>

### SIM-FV-26 — decision checkpoint

A customer says the report is confusing but does not request a human; policy calls for clarification of the disputed metric first. What should happen?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Ask a targeted clarification under the support policy while keeping escalation available. Ambiguity without the trigger should follow the applicable clarification route.

**Base choice:** A customer explicitly asks for a human. Route promptly with verified identity status, issues, evidence, attempted and blocked actions, and next owner.

**Changed constraint and recovery:** The customer says “this is frustrating” without requesting a person. Clarify or continue according to the fictional support policy; do not invent an escalation mandate.

**Failure:** The handoff says credit issued, but only a proposal exists. Correct status and include the operation ledger before transferring.

**Nearest alternative:** A transcript dump does not ensure an actionable handoff; a vague complaint is not identical to an explicit human request.

**Conditional cue:** Hear the trigger; hand over facts, status and next action.

**Proof:** Inspect `handoff={identity_status,issues,confirmed,proposed,blocked,reason,next_owner}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.2.md#variant-fv-26).

</details>


<span data-assessment-exposure="cct-fv-01-base-v1,cct-fv-01-retry-v1,cct-fv-04-base-v1,cct-fv-04-retry-v1,cct-fv-05-base-v1,cct-fv-05-retry-v1,cct-fv-08-base-v1,cct-fv-08-retry-v1,cct-fv-09-base-v1,cct-fv-09-retry-v1,cct-fv-26-base-v1,cct-fv-26-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-01 — Confirm the effect before retrying](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.1.md#variant-fv-01) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.1&variant=FV-01)
- [FV-04 — Bind approval to this action](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.4.md#variant-fv-04) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.4&variant=FV-04)
- [FV-05 — Separate prevention from detection](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md#variant-fv-05) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.5&variant=FV-05)
- [FV-08 — Make capabilities distinguishable](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md#variant-fv-08) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.1&variant=FV-08)
- [FV-09 — Route the actual error category](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md#variant-fv-09) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.2&variant=FV-09)
- [FV-26 — Honor explicit escalation with context](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.2.md#variant-fv-26) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.2&variant=FV-26)

**Build the mechanism:** [Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.