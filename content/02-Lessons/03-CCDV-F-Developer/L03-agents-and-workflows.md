# CCDV-F Lesson 3 — Agents and Workflows (14.7%, about 8 questions)

**Time:** 2 hours plus lab 02 (reuse) · **Practice:** [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
If you passed CCAR-F, much of this is review (its Domain 1). What's new here: deployment models
(self-hosted vs Anthropic-hosted) and third-party frameworks.

## 1.0 The big idea

If you can write the steps down in advance, build a workflow; use an agent only when the path
depends on what Claude finds. Either way, a rule that must always hold goes in code (a hook),
not in the prompt.

## 1.1 Agent architecture (4.5%)

- **Workflow:** *your code* decides the steps; Claude does work inside each step. **Agent:**
  *Claude* decides the next step, in a loop, using tools.
- **Decision rule:** if you can write the steps down in advance, build a workflow. Use an agent
  only when the path depends on what Claude finds along the way. Workflows are cheaper, faster,
  and easier to test and debug.

| Signal in the scenario | Pick |
| --- | --- |
| Fixed steps (extract → validate → save) | Workflow (prompt chaining) |
| Classify first, then send to the right handler | Workflow (routing) |
| Independent parts that can run at once | Workflow (parallel calls) |
| Unknown number of steps, open-ended investigation | Agent |
| Need to inspect or gate each intermediate output | Workflow, even with a smart model |

- **Manager/supervisor hierarchies** (hub-and-spoke): a coordinator breaks the task down, picks
  which subagents to call, combines their results and handles errors. **All** traffic goes
  through the coordinator, which makes it observable and consistent.
- **Why subagents help:** each gets a **clean, isolated context** and only the tools for its
  role. The verbose middle work stays out of the coordinator's window; only a summary comes back.
- Don't over-delegate. Newer models spawn subagents readily; a direct search is often faster.
  Use subagents for parallel work, isolated context, or independent workstreams.

## 1.2 Agent construction with Claude (5.3%)

- **The loop:** send messages + tools → if `stop_reason` is `tool_use`, run the tool, append the
  `tool_result`, call again → stop at `end_turn`.
- **Anti-patterns:** stopping when the text "sounds done", stopping when any text appears, or
  using an iteration cap as the *main* stop. (A cap as a backstop is fine.)
- **Build options.** They run from building everything yourself to letting Anthropic run it:
  more control means more to build and operate.

| Option | You get | Choose when |
| --- | --- | --- |
| **Custom loop** on the Messages API | Full control; you write dispatch, retries, context handling | Unusual control flow, minimal dependencies |
| SDK **Tool Runner** | The SDK runs your tools and sends results back | Simple tool loops without the boilerplate |
| **Claude Agent SDK** | The Claude Code harness as a library: built-in tools, subagents, hooks, sessions, MCP | A production agent without rebuilding the harness |
| **Claude Managed Agents** | A pre-built, configurable harness on Anthropic's infrastructure | Long-running or async work you don't want to host |

- **Self-hosted vs Anthropic-hosted:** self-hosted (your loop or the Agent SDK in your own
  infrastructure) means you control the runtime, network and data path, and you operate it.
  Anthropic-hosted (Managed Agents) means less to run, within the harness's options.
- **Agent SDK subagents:** spawned with the **Task** tool, so the coordinator's `allowedTools`
  must include `"Task"`. Each is configured with an **AgentDefinition** (description, system
  prompt, tool restrictions). For parallel work, emit **several Task calls in one response**.
- **Hooks = deterministic actions** at fixed points in the loop:
  - **Before a tool runs:** block or redirect a call that breaks a rule (a refund over the limit
    goes to a human; `rm -rf` is denied).
  - **After a tool runs (`PostToolUse`):** clean or normalize the result before Claude sees it
    (mixed date formats become ISO 8601; secrets get redacted).
  - A prompt instruction has a non-zero failure rate. A hook runs every time.
- **Sessions:** resume a named session to continue; **fork** to try two approaches from the same
  starting point.

## 1.3 Agent patterns and frameworks (4.9%)

- **Tool-use loop:** the pattern in 1.2. Parallel tool calls in one turn cut round trips.
- **Subagents:** they **don't inherit** the parent's history. Pass everything they need in the
  prompt, with structured metadata (source, date) so attribution survives. Give goals and quality
  criteria, not step-by-step scripts.
- **Memory** outside the context window:
  - The **memory tool** (files you control).
  - Structured state files such as `progress.txt` or `tests.json`.
  - **git** as a log and checkpoint. The docs note current models are strong at recovering state
    from these when a new session starts.
- **Context-window management:**
  - **Clear old tool results** (context editing).
  - **Server-side compaction** summarizes earlier turns (beta, Claude 4.6 and later).
  - Push verbose exploration into a **subagent**.
  - Sometimes the best move is a **fresh window** that re-reads the state files.
  - A bigger window only delays the same failure.
- **Frameworks** (general knowledge; not in our saved Anthropic sources):

| Framework | Idea |
| --- | --- |
| **LangGraph** | Agents and workflows as a graph of nodes with explicit state; good for branching and checkpoints |
| **PydanticAI** | Python agents with typed inputs and outputs, validated by Pydantic models |
| **Strands Agents** | An open-source, model-driven agent SDK (from AWS): give it a model, a prompt and tools |

- **Tradeoff:** a framework gives you conventions and speed but adds a dependency and a layer of
  abstraction. A custom loop or the Agent SDK gives you control. None of them fixes a bad tool
  description or a missing guardrail.

## What people who passed say

The Agent SDK came up inside scenario questions. *Single report:* a colleague who passed (INSIGHTS,
2026-09-26). About two-thirds overlap with CCAR-F. *Single report:* another colleague who passed.

## Worked example

A finance team wants two things. (1) Every invoice PDF: extract fields → check them against the
purchase order → save. (2) When month-end totals don't match across three systems, find out why.
**Answer:** (1) is a **workflow**: the steps are fixed, and each output can be validated before
the next step. (2) is an **agent**: the path depends on what it finds. A coordinator sends one
subagent per system, each with read-only tools. Each returns a short structured summary, and the
coordinator compares them. A **pre-tool hook** blocks any payment or write tool, so a wrong guess
can't move money. "Make both of them agents for consistency" is wrong: (1) gets slower, costlier
and harder to test for no gain.

## Traps

- "Use an agent, it's more flexible." Flexibility you don't need is cost and risk.
- "The subagent can see what the coordinator saw." It can't; pass the context explicitly.
- "Tell the agent in the prompt never to exceed $500." Use a hook.
- "Stop the loop after 10 iterations." That's a backstop, not the stop condition. Use `end_turn`.
- "Switch to LangGraph to fix unreliable tool choice." Frameworks don't fix descriptions.

## Try it, reuse lab 02 (90 min)

[Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md): a coordinator agent loop
with subagents. Add one pre-tool hook that blocks a tool, and one `PostToolUse` hook that
normalizes a field. Then note which parts would be simpler as a fixed workflow.

## Done when

- [ ] You can decide workflow vs agent from a scenario in one sentence
- [ ] You can write the loop from memory, `stop_reason` included, and name the stop anti-patterns
- [ ] You can compare a custom loop, the Agent SDK and Managed Agents, and self-hosted vs Anthropic-hosted
- [ ] You can say what a pre-tool hook and a `PostToolUse` hook are each for
- [ ] You scored 80% or more on [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L04 Prompt and Context Engineering](L04-prompt-and-context-engineering.md)

Source: official CCDV-F exam guide v1.0, Domain 1 objectives; CCAR-F exam guide v1.0, task
statements 1.1–1.5 (loop, coordinator, Task tool, AgentDefinition, hooks, sessions). Docs:
platform.claude.com/docs/en/build-with-claude/working-with-messages (Messages API vs Managed
Agents), …/agents-and-tools/tool-use/overview (Tool Runner, memory tool),
…/build-with-claude/context-windows (compaction, context editing),
…/prompt-engineering/claude-prompting-best-practices (subagent orchestration, state tracking,
prompt chaining). Framework descriptions: general knowledge; check each project's docs.