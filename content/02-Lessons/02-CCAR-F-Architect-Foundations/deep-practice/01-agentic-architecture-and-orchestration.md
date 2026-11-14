# Deep practice 1: agentic architecture and orchestration

**Picture the application:** A customer asks an assistant to investigate an order and explain what can happen next. Start with that request, follow the evidence returned by each lookup, and identify who owns any proposed action. The mechanisms below explain how an agent loop, delegation and handoff support that ordinary service task.

This page covers Domain 1 of CCAR-F, agentic architecture and orchestration, one task statement at a time. It goes
deeper than [Lesson 1](../L01-agentic-architecture-and-orchestration.md): each section gives the core idea, how it works under the hood,
the look-alike wrong answers, a worked example and a one-line exam reflex. Read the lesson first.
Objective lessons for this page: [1.1](../objectives/objective-1.1.md) · [1.2](../objectives/objective-1.2.md) · [1.3](../objectives/objective-1.3.md) · [1.4](../objectives/objective-1.4.md) · [1.5](../objectives/objective-1.5.md) · [1.6](../objectives/objective-1.6.md) · [1.7](../objectives/objective-1.7.md) · [5.2](../objectives/objective-5.2.md).

Two hook skills are in [03-claude-code-configuration-and-workflows.md](03-claude-code-configuration-and-workflows.md), not here:
"hooks or settings vs `CLAUDE.md`" and "PostToolUse quality hooks". `tool_choice` modes are in
[04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md).

Bracketed tags like `[stop-reasons]` are sources; the list is at the end.

---

## 1.1 Agentic loops

Lesson: [L01 section 1.1](../L01-agentic-architecture-and-orchestration.md#11-the-agentic-loop) · Objective: [1.1](../objectives/objective-1.1.md)

**Exam wording (task statement):** `Task Statement 1.1: Design and implement agentic loops for autonomous task execution`

### Core idea

An agent is a loop. You call Claude. Claude answers. You look at **one field**, `stop_reason`, to decide
what to do next. If Claude asked for a tool, you run it, send the result back, and call again. If Claude
is finished, you stop. That is the whole engine.

The exam tests one thing hard: **the loop is driven by `stop_reason`, nothing else.** Not the text. Not a
counter. Not the word "done".

### How it works under the hood

Every Messages API response carries `stop_reason`. The table lists the doc values [stop-reasons] and
what your loop does:

| `stop_reason` (doc wording) | What it means | What the loop does |
|---|---|---|
| `tool_use` | Claude is calling a tool. | Run every `tool_use` block, send back a `tool_result` for each, call again. |
| `end_turn` | Claude finished its response naturally. | Use the answer. Exit the loop. |
| `max_tokens` | The response hit your `max_tokens` limit. | Raise `max_tokens` or continue the response. If the cut-off reply holds a half-written tool call, **do not run it**; retry with a higher `max_tokens` [stop-reasons]. |
| `stop_sequence` | Claude emitted one of your `stop_sequences`. | Read the `stop_sequence` field to see which one fired, then act on it. |
| `pause_turn` | A **server-tool** loop reached its iteration limit (default 10). | Send the assistant content back as-is to let Claude continue [stop-reasons]. |
| `refusal` | Claude declined to respond. | Read `stop_details` (category of the refusal); handle it or retry on a fallback model. Do not blindly retry the same call [stop-reasons]. |
| `model_context_window_exceeded` | The response filled the model's context window. | Treat the response as truncated [stop-reasons]. |

Exam focus: the guide's knowledge line names only `"tool_use"` vs `"end_turn"` [guide, TS 1.1]. The other
five are doc facts that make good trace-reading distractors.

**One detail that trips people:** `pause_turn` is **only** for server tools (tools Anthropic runs, such as
web search). When Claude stops to call **your** tool, `stop_reason` is `tool_use`, never `pause_turn`
[stop-reasons].

**How a tool result goes back** [handle-tool-calls]:

- The result is a block `{"type": "tool_result", "tool_use_id": "<id from the tool_use block>", "content": ...}`.
  Optional `"is_error": true` when the tool failed.
- Every `tool_use` block needs a matching `tool_result` (same id).
- Doc wording: "Tool result blocks must immediately follow their corresponding tool use blocks in the
  message history." No message may sit in between.
- Doc wording: "the tool_result blocks must come FIRST in the content array. Any text must come AFTER all
  tool results." Text first gives a `400` error [handle-tool-calls].
  - Edge case: if the same turn also called a **server tool** that has no result yet, the user message
    must hold **only** `tool_result` blocks. Text after them ends the turn early, and the request fails
    with a `400` that names the unfinished server tool [handle-tool-calls].
- If Claude called several tools in parallel, **all** results go back in **one** user message, with no
  text before them. This is a doc rule: "every tool result returns in a single user message, and no
  text content appears before the tool results in that message" [parallel-tools].

**The API keeps no memory.** Doc wording: "The Messages API is stateless, which means that you always send
the full conversational history to the API" [messages]. So each loop turn appends Claude's assistant
message **and** your tool results to the list, then sends the whole list again. (Deeper in deep practice 5, 5.1.)

```python
messages = [{"role": "user", "content": task}]
for turn in range(SAFETY_CAP):                     # safety net, NOT the stop signal
    resp = client.messages.create(model=M, tools=TOOLS, messages=messages, max_tokens=4096)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason == "end_turn":
        return final_text(resp)
    if resp.stop_reason == "tool_use":
        results = [run(b) for b in resp.content if b.type == "tool_use"]   # all of them
        messages.append({"role": "user", "content": results})           # results first, one message
        continue
    if resp.stop_reason == "max_tokens":
        raise_limit_or_continue()                  # never run a half-written tool call
    elif resp.stop_reason == "pause_turn":
        continue                                   # assistant content already appended; call again
    else:                                          # refusal, model_context_window_exceeded, stop_sequence
        handle_or_escalate(resp)
escalate_to_human("hit safety cap")
```

**Model-driven vs pre-set.** The guide's knowledge line: Claude "reasons about which tool to call next based
on context", unlike "pre-configured decision trees or tool sequences" [guide, TS 1.1]. You give tools and a
goal; Claude picks the order.

### Look-alikes (sound right, are wrong)

1. **"Stop when the reply contains 'done' / 'task complete'."** Exam wording calls this an anti-pattern:
   "parsing natural language signals to determine loop termination" [Guide]. Text can say "done" while
   Claude still wants a tool, or never say it.
2. **"Stop after N iterations."** Also named in the guide: "setting arbitrary iteration caps as the primary
   stopping mechanism". A cap is fine as a **safety net** with a handoff. It must not be the **main** stop.
3. **"Stop when the response has text in it."** The guide: "checking for assistant text content as a
   completion indicator". A `tool_use` response often has text too ("Let me look that up").
4. (Trace items) **Putting a "Here are the results:" text block before the `tool_result` blocks** gives a
   `400`. **Sending parallel results as two separate user messages** breaks the parallel pattern.

### Worked example (Scenario: customer support resolution agent)

The agent calls `get_customer` and `lookup_order` in parallel. The response has two `tool_use` blocks and
`stop_reason: "tool_use"`. A teammate's code runs only the first block, appends one `tool_result`, and adds
a text line "Order lookup still running" before it.

What breaks? Two things. The second `tool_use` id has no `tool_result`, and text comes before the results.
The fix: run both tools, put both `tool_result` blocks (each with its own `tool_use_id`) first in one user
message, then call again. Keep looping until `stop_reason` is `end_turn`.

### Exam reflex

**Loop on `tool_use`, stop on `end_turn`; text, keywords and counters never decide.**

---

## 1.2 Coordinator-subagent orchestration

Lesson: [L01 section 1.2](../L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke) · Objective: [1.2](../objectives/objective-1.2.md)

**Exam wording:** `Task Statement 1.2: Orchestrate multi-agent systems with coordinator-subagent patterns`

### Core idea

One boss agent (the **coordinator**) splits the job, hands pieces to helper agents (**subagents**),
collects what they find, and checks the result for holes. Helpers never talk to each other. Everything goes
through the boss. The guide calls this "Hub-and-spoke" [guide, TS 1.2].

### How it works under the hood

- **Isolated context.** A subagent "starts fresh, with no parent conversation". Its only input from the
  parent is the prompt string the parent writes [sdk-subagents]. (Details in 1.3.)
- **Only the final message comes back.** Doc wording: "intermediate tool calls and results stay inside the
  subagent; only its final message returns to the parent" [sdk-subagents].
- **Scale the team to the question.** Anthropic's research system embeds rules like: "Simple fact-finding
  requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls
  each, and complex research might use more than 10 subagents" [research-system]. Exam skill wording:
  "dynamically select which subagents to invoke rather than always routing through the full pipeline"
  [Guide].
- **Partition the scope** so helpers do not overlap: distinct subtopics or source types [Guide]. Anthropic
  found that vague delegation makes agents "duplicate work, leave gaps, or fail to find necessary
  information"; each subagent needs "an objective, an output format, guidance on the tools and sources to
  use, and clear task boundaries" [research-system].
- **Gap-check loop.** The coordinator reads the synthesis, finds gaps, sends targeted follow-up queries to
  search/analysis helpers, and re-runs synthesis "until coverage is sufficient" [Guide].
- **Why route all traffic through the coordinator?** Exam wording: "for observability, consistent error
  handling, and controlled information flow" [Guide].

### Look-alikes

1. **"Let subagents message each other directly to save time."** Breaks hub-and-spoke: you lose one place
   for error handling and tracing.
2. **"Always run the full pipeline for every query."** Wastes effort on simple questions; the guide wants
   dynamic selection.
3. **"Whole areas are missing from the report, so give the synthesis agent a bigger context window."**
   The synthesis agent can only combine what it was handed. If no subagent was ever assigned an area,
   no window size brings it back. Look at how the coordinator divided the work.

### Worked example (Scenario: multi-agent research system)

Question: "Where is EU renewable energy policy heading?" The coordinator sends one subagent per country:
Germany, France, Spain. Each returns a solid summary of that country's subsidies. The final report has
nothing on grid storage or on permitting rules, which cut across countries.

Each subagent did its own job well. The gap comes from the way the coordinator cut up the question: only
by country. Fix: make the coordinator split by theme as well (subsidies, grid storage, permitting, EU-wide
rules). Then add the gap-check loop: after synthesis, the coordinator compares the report with the
question's main themes and sends targeted follow-up queries for anything missing.

### Exam reflex

**Good subagents but missing areas: fix how the coordinator divides the work, then add a gap check.**

---

## 1.3 Subagent invocation, context passing, and spawning

Lesson: [L01 section 1.3](../L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context) · Objective: [1.3](../objectives/objective-1.3.md)

**Exam wording:** `Task Statement 1.3: Configure subagent invocation, context passing, and spawning`

### Core idea

A subagent knows **nothing** you did not put in its prompt. So the coordinator must paste in everything the
helper needs: the findings so far, the sources, the goal. To run helpers at the same time, ask for them all
in **one** coordinator turn.

### How it works under the hood

- **The spawning tool.** Exam answer: the **`Task`** tool, and "allowedTools must include "Task"" for a
  coordinator to spawn subagents [guide, TS 1.3].
  - **What changed since:** today's Agent SDK calls it the **`Agent`** tool. The examples use
    `allowed_tools=["Read", "Grep", "Glob", "Agent"]`. The doc says it "appears as "Agent" in tool_use
    blocks but as "Task" in the system:init tools list", and before Claude Code v2.1.63 `tool_use` blocks
    also named it `"Task"` [sdk-subagents]. Doc wording: "In version 2.1.63, the Task tool was renamed
    to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases"
    [cc-subagents]. The `Task` alias still works, but today `allowedTools` only pre-approves tools;
    `Agent` needs no approval, so leaving it out doesn't stop spawning. Use `disallowedTools` for that
    [sdk-permissions]. See [exam answer vs today](conditions-and-errors.md#exam-answer-vs-today).

    **On the exam: pick `Task`.**
- **`AgentDefinition` fields** [sdk-subagents]: `description` (required; "when to use this agent"),
  `prompt` (required; its system prompt), `tools` (allowed tools; if omitted, it inherits all subagent tools),
  `disallowedTools`, `model` (`'inherit'` or an alias or full id), plus others. Claude picks a subagent
  from its `description`.
- **What a subagent gets** (doc table) [sdk-subagents]: its own system prompt plus the Agent tool's prompt;
  the project `CLAUDE.md` (via `settingSources`); tool definitions. **What it does not get:** "The parent's
  conversation history or tool results" and "The parent's system prompt". Doc wording: "The only content you
  pass from parent to subagent is the Agent tool's prompt string".
- **Parallel spawning.** Exam skill: emit "multiple Task tool calls in a single coordinator response rather
  than across separate turns" [Guide]. Doc support: "multiple subagents can run concurrently"
  [sdk-subagents].
- **Structured hand-over.** Keep content separate from metadata (URL, document name, page) so citations
  survive [Guide]. Example:
  `{"claim": "...", "source_url": "...", "doc": "...", "page": 14, "date": "2026-03"}`.
- **Goals, not steps.** Coordinator prompts should state "research goals and quality criteria rather than
  step-by-step procedural instructions" [Guide].
- **Fork.** A fork starts with a copy of the parent's history instead of a fresh context
  [sdk-subagents] [sdk-sessions]. Used to try two approaches from one shared analysis (see 1.7). (Not the
  same as `context: fork` in a Claude Code skill, which runs the skill away from your main chat; see
  [deep practice 3](03-claude-code-configuration-and-workflows.md).)

**What changed since (also):** the doc now says "Subagents can also spawn subagents of their own" and
subagents run in the background by default [sdk-subagents]. Older guidance said subagents could not nest.
The exam may still assume subagents can't start their own; if an option depends on it, don't rule it out
just because today's docs differ. Which
version the exam assumes is not stated (see "Not confirmed" at the bottom).

**On the exam: pick the option that doesn't depend on whether subagents can nest.**

### Look-alikes

1. **"The synthesis subagent can see the search agent's results because they share a session."** No.
   Nothing is inherited. Pass the findings in the prompt.
2. **"Spawn the three researchers one per turn, so each sees the last one's output."** That is sequential;
   the guide wants several `Task` calls in one response for parallel work (unless one truly depends on
   another).
3. **"Write the subagent a 12-step procedure."** Over-specifies; the guide prefers goals plus quality
   criteria so the helper can adapt.
4. **"Coordinator can't spawn anything. Fix: rewrite the prompt."** If `Task` is missing from
   `allowedTools`, no prompt fixes it. Add `Task`.

### Worked example (Scenario: multi-agent research system)

The synthesis agent writes a report with no citations. The search agent did return URLs. Cause: the
coordinator passed the synthesis agent a prose summary ("findings show X and Y") and dropped the metadata.
Fix: pass the full findings as structured records (claim, source URL, document, page, date). The synthesis
agent can only cite what it was handed.

### Exam reflex

**A subagent knows only its prompt: pass complete findings with metadata, and spawn parallel helpers in one turn.**

---

## 1.4 Enforcement and handoff

Lesson: [L01 section 1.4](../L01-agentic-architecture-and-orchestration.md#14-enforcement-and-handoff) · Objective: [1.4](../objectives/objective-1.4.md)

**Exam wording:** `Task Statement 1.4: Implement multi-step workflows with enforcement and handoff patterns`

**This task statement is split across two pages.** The Claude Code half, "hooks or settings vs `CLAUDE.md`
(enforced vs advice)", is in [deep practice 3, section 1.4](03-claude-code-configuration-and-workflows.md#14-enforced-vs-advice-claude-code-half).
This section covers handoff packages, session safeguards and the headline skill, the **prerequisite gate**.

### Core idea

If a step **must** happen first (verify the customer before a refund), don't ask nicely in the prompt.
Block the later tool in code until the first one has succeeded. And when a case goes to a person, hand them
a complete package, because they can't read the chat.

### How it works under the hood

- Exam wording: "prompt instructions alone have a non-zero failure rate" when "deterministic compliance is
  required" [guide, TS 1.4].
- **Prerequisite gate.** Exam skill: "blocking process_refund until get_customer has returned a verified
  customer ID" [Guide]. In code: your tool layer (or a `PreToolUse` hook, see 1.5) keeps a flag such as
  `verified_customer_id`. A call to `process_refund` without it returns an error result telling Claude to
  verify first.
- **Multi-concern requests.** Split them into separate items, investigate each (in parallel, with shared
  context), then give one combined answer [Guide].
- **Handoff package.** Exam skill: "customer ID, root cause, refund amount, recommended action" for human
  agents "who lack access to the conversation transcript" [Guide].
- **Session safeguards** (practice, not doc): every session ends in a resolution or an escalation, even
  when the loop hits its cap or a tool keeps failing.

```python
def issue_store_credit(args, state):
    if state.get("return_window_ok", {}).get(args["order_id"]) is not True:
        return {"is_error": True,
                "content": "Blocked: call check_return_window for this order first."}
    ...
```

### Look-alikes

1. **"Add 'ALWAYS verify identity first' in capitals to the system prompt."** Still a prompt. Still
   non-zero failure. The guide wants a programmatic gate.
2. **"Add few-shot examples showing verification first."** Better behaviour, same problem: not guaranteed.
3. **"Hand the human the full transcript."** The guide's answer is a structured summary; the human may not
   have the transcript, and a summary is faster to act on.

### Worked example (Scenario: customer support resolution agent)

A store's returns agent has two tools: `check_return_window` and `issue_store_credit`. After someone
shortens the system prompt, a weekly audit finds store credit issued on orders that were past the 30-day
return window. The rule "check the window first" was only in the prompt.

The fix is a code gate. `issue_store_credit` refuses unless `check_return_window` has set
`return_window_ok[order_id] = True` for that same order in this session. The flag is kept per order, so a
check on one order can't unlock credit on another. Now the order of the steps doesn't depend on
the prompt at all. When an order is out of window and the customer pushes back, the agent escalates with
`{customer_id, order_id, issue, what_was_checked, credit_requested, recommended_action}`.

### Exam reflex

**"Must always happen first" means a code gate, not a prompt; a human handoff means a structured summary.**

---

## 1.5 Agent SDK hooks

Lesson: [L01 section 1.5](../L01-agentic-architecture-and-orchestration.md#15-agent-sdk-hooks) · Objective: [1.5](../objectives/objective-1.5.md)

**Exam wording:** `Task Statement 1.5: Apply Agent SDK hooks for tool call interception and data normalization`

**This task statement is split across two pages.** The quality-hook half, "PostToolUse quality hooks", is in
[deep practice 3, section 1.5](03-claude-code-configuration-and-workflows.md#15-posttooluse-quality-hooks-quality-hook-half). Here: the business-rule hook
and the data-normalization idea.

### Core idea

A hook is your code that runs **around** a tool call. Before the call (`PreToolUse`), it can block or
change it. After the call (`PostToolUse`), it can clean up the result before Claude reads it. Hooks are
**deterministic**. Prompts are **probabilistic**.

### How it works under the hood

- **Block a call.** A `PreToolUse` hook callback returns `hookSpecificOutput` holding
  `permissionDecision: "deny"` and a `permissionDecisionReason`. Allowed values: `"allow"`, `"deny"`, `"ask"`, or `"defer"`; it can also
  return `updatedInput` [sdk-hooks]. The reason "tells the model why, so it avoids retrying" [sdk-hooks].
- **Change a result.** A `PostToolUse` hook can add `additionalContext` to the tool result, or replace the
  output with `updatedToolOutput` (any tool). The older `updatedMCPToolOutput` (MCP tools only) still
  works; the docs say to prefer `updatedToolOutput` [sdk-hooks].
- **Normalization use.** Exam skill: normalize "Unix timestamps, ISO 8601, numeric status codes" from
  different MCP tools before the agent processes them [Guide].
- **Policy use.** Exam skill: block "refunds exceeding $500" and "redirect to alternative workflows (e.g.,
  human escalation)" [Guide].

### Look-alikes

1. **"Tell Claude in the system prompt that refunds over $500 need a manager."** Advice, not a guarantee.
2. **"Ask Claude to convert all dates to ISO 8601 itself."** Works most of the time; a `PostToolUse` hook
   works every time and costs no tokens of reasoning.
3. **"Use a PostToolUse hook to stop a $900 refund."** Too late: the refund already ran. Blocking needs
   `PreToolUse`.

### Worked example (Scenario: customer support resolution agent)

Three MCP tools return dates as `1727740800`, `2024-10-01T00:00:00Z` and `10/01/2024`. The agent sometimes
misreads which order is older. Fix: one `PostToolUse` hook rewrites all dates to ISO 8601 before Claude sees
them. Separately, a `PreToolUse` hook on `process_refund` denies `amount > 500` with the reason "Over limit:
escalate to a human" and the agent hands off.

### Exam reflex

**Block before (`PreToolUse` deny), clean up after (`PostToolUse`); guaranteed rules live in hooks.**

---

## 1.6 Task decomposition

Lesson: [L01 section 1.6](../L01-agentic-architecture-and-orchestration.md#16-breaking-the-task-down) · Objective: [1.6](../objectives/objective-1.6.md)

**Exam wording:** `Task Statement 1.6: Design task decomposition strategies for complex workflows`

### Core idea

There are two ways to break up a big job.

- **Fixed chain** ("prompt chaining"): the steps are known up front. Step 1, then step 2, then step 3.
  Good when the work is predictable.
- **Adaptive plan** ("dynamic decomposition"): you don't know the steps yet. You look, learn, and make the
  next steps from what you found. Good when the work is open-ended.

This section focuses on the second one: "steps that change as new facts come in".

### How it works under the hood

Exam knowledge wording [guide, TS 1.6]:

- "When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on
  intermediate findings"
- "Prompt chaining patterns that break reviews into sequential steps (e.g., analyze each file individually,
  then run a cross-file integration pass)"
- "The value of adaptive investigation plans that generate subtasks based on what is discovered at each
  step"

Exam skill wording for the adaptive case: decompose "add comprehensive tests to a legacy codebase" "by
first mapping structure, identifying high-impact areas, then creating a prioritized plan that adapts as
dependencies are discovered" [Guide].

**The adaptive pattern, as steps:**

1. **Map.** Find the structure first (folders, entry points, what calls what).
2. **Rank.** Pick the high-impact areas (most used, most risky, least tested).
3. **Plan.** Write a prioritized list of subtasks.
4. **Do one, learn, re-plan.** When a subtask finds something new (a hidden dependency, a shared helper),
   add, drop or reorder subtasks. The plan is a living list, not a contract.

**The fixed-chain pattern for big reviews:** per-file passes (each file on its own, so attention is not
diluted), then **one separate cross-file pass** to catch problems between files (a changed function
signature that breaks a caller elsewhere). The guide: "to avoid attention dilution" [Guide].

**How to pick (quick test):** Can you write all the steps before you start, and will they stay the same
for every input? Fixed chain. Do the next steps depend on what you find? Adaptive.

### Look-alikes

1. **"Write the full test plan for all 400 files up front, then execute it."** Looks organized. Fails
   because you can't know dependencies before mapping. That's a fixed plan for an open-ended task.
2. **"Review all 30 changed files in one pass with a bigger context window."** Attention dilution; the
   guide wants per-file passes plus a cross-file pass.
3. **"Use dynamic decomposition for a standard 3-check compliance review of every invoice."** Over-built.
   The steps are known and identical: chain them.
4. **"Only per-file passes, no integration pass."** Misses cross-file bugs.

### Worked example (Scenario: developer productivity with Claude)

Task: "add comprehensive tests to this legacy payments service". Step 1, map: Claude finds 3 modules and
that `ledger.py` is imported by everything. Step 2, rank: `ledger.py` first. Step 3, plan: tests for
`ledger.post()`, then `refunds`, then `reports`. Step 4, learn: while testing `ledger.post()`, Claude finds
it calls a currency helper with no tests and odd rounding. The plan changes: add "test currency helper"
**before** continuing, because the ledger tests depend on it. That re-plan is exactly the skill.

Twist: same team, but now "check every PR for the same 4 style rules". Known steps, same each time: fixed
chain.

### Exam reflex

**Open-ended work: map, rank, plan, re-plan as you learn; predictable multi-part work: fixed chain, per-file then cross-file.**

---

## 1.7 Session state, resumption, and forking

Lesson: [L01 section 1.7](../L01-agentic-architecture-and-orchestration.md#17-sessions-resume-and-fork) · Objective: [1.7](../objectives/objective-1.7.md)

**Exam wording:** `Task Statement 1.7: Manage session state, resumption, and forking`

The full deep version (stale tool results, file changes, summaries) is in
[05-context-management-and-reliability.md, section "Session resumption"](05-context-management-and-reliability.md). Here are the
mechanics and the choice.

### Core idea

Three moves. **Resume**: keep going in the same old session. **Fork**: copy the session into a new branch
and try something different; the original stays as it was. **Start fresh with a summary**: when the old
session's tool results are out of date.

### How it works under the hood

- **CLI** [cli]:
  - `--continue`, `-c`: "Load the most recent conversation in the current directory". Plain
    `claude --continue` "Skips sessions created with `claude -p` or the Agent SDK". But
    "`claude -p --continue` includes `-p`, SDK, and `/loop` sessions", so a CI job can pick up the last
    headless run [cli].
  - `--resume`, `-r`: "Resume a specific session by ID or name, or show an interactive picker".
  - `--name`, `-n`: sets a display name; "You can resume a named session with `claude --resume <name>`".
  - `--fork-session`: "When resuming, create a new session ID instead of reusing the original (use with
    `--resume` or `--continue`)".
- **Agent SDK** [sdk-sessions]: options `continue` / `continue_conversation=True` (most recent session in
  the directory), `resume` (a specific session ID, read from `session_id` on the result message), and
  fork: `fork_session=True` (Python) / `forkSession: true` (TypeScript). Doc wording: fork "creates a new
  session that starts with a copy of the original's history. The original stays unchanged."
- **Exam wording** uses `--resume <session-name>` and `fork_session` [guide, TS 1.7].

### Look-alikes

1. **`--continue` when you need a specific older session.** It only takes the most recent one in this
   directory. Use `--resume <name>`.
2. **`--resume` to compare two approaches.** Both experiments would pile into one history. Fork instead.
3. **Resume a session after big code changes and hope it notices.** Its old tool results are stale. Tell it
   which files changed, or start fresh with a summary (deep practice 5).

### Worked example (Scenario: developer productivity with Claude)

Yesterday you ran a long analysis session named `auth-audit`. Today you want to compare two refactoring
plans from that same analysis. Run `claude --resume auth-audit --fork-session` twice (or `fork_session=True`
in the SDK), one branch per plan. The original `auth-audit` stays clean.

### Exam reflex

**Same line of work: `--resume <name>`; two different directions from one baseline: fork; stale results: fresh session plus summary.**

---

## 5.2 Escalation and ambiguity resolution

Lesson: [L05 section 5.2](../L05-context-management-and-reliability.md#52-escalation-and-ambiguity) · Objective: [5.2](../objectives/objective-5.2.md)

**Exam wording:** `Task Statement 5.2: Design effective escalation and ambiguity resolution patterns`

### Core idea

Hand the case to a person for **the right reasons**, and ask a question instead of guessing.

### How it works under the hood

Exam wording for the triggers: "customer requests for a human, policy exceptions/gaps (not just complex
cases), and inability to make meaningful progress" [guide, TS 5.2].

| Situation | Right move (exam skill wording, paraphrased where marked) |
|---|---|
| Customer explicitly asks for a human | "Honoring explicit customer requests for human agents immediately without first attempting investigation" |
| Customer is frustrated, issue is easy | "Acknowledging frustration while offering resolution", escalate "only if the customer reiterates their preference" |
| Policy is silent or unclear | Escalate. Example in the guide: "competitor price matching when policy only addresses own-site adjustments" |
| Tool returns several matching customers | "ask for additional identifiers", not pick by heuristic |
| Agent escalates inconsistently | "Adding explicit escalation criteria with few-shot examples to the system prompt" |

Exam knowledge wording: "sentiment-based escalation and self-reported confidence scores are unreliable
proxies for actual case complexity" [Guide].

Note: escalation **criteria** are a prompt fix (judgment calls). A **hard money limit** (refund over $500)
is a hook (1.5). Don't mix them up.

### Look-alikes

1. **"Escalate when sentiment analysis says the customer is angry."** Named unreliable.
2. **"Escalate when Claude's self-reported confidence is below 0.7."** Also named unreliable.
3. **"Two customers named J. Smith: pick the one with the most recent order."** Heuristic guess. Ask for
   another identifier.
4. **"Investigate first, then transfer, so the human has context."** Not when the customer asked for a
   human. Transfer now (with the handoff package from 1.4).

### Worked example (Scenario: customer support resolution agent)

A customer says: "This is the third time. I want a real person." Right move: transfer now with a structured
handoff. Twist: the customer says "This is so annoying, my order is late". The issue is a simple tracking
lookup. Right move: acknowledge, offer to fix it now, and escalate only if they ask again.

### Exam reflex

**Escalate on: asked for a human, policy gap, no progress; never on mood or self-rated confidence; multiple matches means ask.**

---

## Not covered here on purpose

- Hooks or settings vs `CLAUDE.md`, and PostToolUse quality hooks: [03-claude-code-configuration-and-workflows.md](03-claude-code-configuration-and-workflows.md).
- `tool_choice` modes (`auto`, `any`, forced tool, `none`): [04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md).
- Error propagation between agents (5.3), scratchpads (5.4), provenance (5.6), and what a resumed
  session still knows: [05-context-management-and-reliability.md](05-context-management-and-reliability.md).

---

## Sources (citation keys)

All Tier 1, checked 2026-10-06:
[stop-reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons) ·
[handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) ·
[parallel-tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use) ·
[messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) ·
[sdk-subagents](https://code.claude.com/docs/en/agent-sdk/subagents) ·
[cc-subagents](https://code.claude.com/docs/en/sub-agents) ·
[sdk-permissions](https://code.claude.com/docs/en/agent-sdk/permissions) ·
[sdk-sessions](https://code.claude.com/docs/en/agent-sdk/sessions) ·
[sdk-hooks](https://code.claude.com/docs/en/agent-sdk/hooks) ·
[cli](https://code.claude.com/docs/en/cli-reference) ·
[research-system](https://www.anthropic.com/engineering/multi-agent-research-system) ·
[Guide] = the official CCAR-F exam guide v1.0 (July 2026, Anthropic).

## Not confirmed

- Whether the exam assumes subagents can or can't start their own subagents (1.3). Today's docs say they can.
- Session safeguards (1.4): "every session ends in a resolution or an escalation" is practice, not a doc rule.

**Next:** [Lesson 4, prompt engineering and structured output](../L04-prompt-engineering-and-structured-output.md), the next lesson in the study order, or back to the [CCAR-F lessons page](../README.md).