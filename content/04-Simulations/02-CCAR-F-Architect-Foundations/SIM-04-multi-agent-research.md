# CCAR-F SIM-04 — Scenario 3: Multi-Agent Research System

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

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

**Objective connections:** [5.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.2.md), [5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.3.md), [5.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.6.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** A team asks for a researched report on a topic whose evidence may come from both websites and documents. The input is a broad question; the expected output is a comprehensive report readers can check against its sources. This simulation examines how investigation and report writing are coordinated.

**Build the application picture first:** [AS 03 grounded assistant](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-03-grounded-assistant.md) · [AS 04 research system](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-04-research-system.md)

**Primary domains:** 1 Agentic Architecture, 2 Tools and MCP, 5 Context and Reliability ·
**Decisions:** 10 · **Time:** 20 min for the decisions, plus about 25 for the twists and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 3, Tier 1)

You're building a multi-agent research system with the Claude Agent SDK. A coordinator agent
delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes
findings and one writes reports. The system researches topics and produces **comprehensive, cited
reports**. The coordinator is the boss agent; the subagents are the helpers it hands work to.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. Each of the four subagents has a full definition: a description, a system prompt and its own
   tools. Yet the coordinator can't spawn any of them. Answering the way the exam guide describes
   it, what's missing?
2. The synthesis agent writes as if it never saw the search results. Why, and what's the fix?
3. For one topic, the search agent looks on the web while the analysis agent reads documents the
   user already uploaded. Neither job needs the other's output. How does the coordinator get them
   running at the same time?
4. Two search agents keep returning the same sources. What do you change?
5. The research phase for a topic took 40 minutes. Now the editor wants to compare two report
   structures (by region, and by product line) built from that same analysis, without redoing the
   research. How?
6. The search subagent has one tool for everything it does with sources: `manage_sources`,
   which searches, fetches, summarizes or deletes depending on a free-text `action` argument.
   In the logs it sends `action: "find"` with a URL, passes a search query where a URL belongs,
   and once deleted a saved source it meant to summarize. What's the fix?
7. The search subagent covers four subtopics. For one, every query ran fine and found nothing.
   For another, the paid market-data site refused access. It reports "No sources found" for both.
   What should it return instead?
8. Final reports lose track of which source said what. How do you keep it?
9. Two credible sources give different market-size numbers. What goes in the report?
10. The synthesis agent gets all subagent output as one long input. It fits well inside the
    context window, yet findings from the middle get dropped. What do you change?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | All four subagents are fully defined, but the coordinator can't spawn any | **The coordinator's `allowedTools` must include `"Task"`** (the exam says Task; today it's `Agent` in Claude Code and the Agent SDK, and `allowedTools` only pre-approves tools; see [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today)). Also accept "`Agent` is blocked: it's in `disallowedTools`, or left out of a restricted `tools` list" as right for today's product; on the exam, pick `"Task"` in `allowedTools`. The Task tool is how a coordinator spawns subagents; without it, the definitions have nothing to call them. | Sharpen each subagent's description so the coordinator knows when to use it: descriptions steer *which* subagent gets picked, not *whether* the coordinator can spawn one; list the subagents and their jobs in the coordinator's system prompt: the prompt can't grant a tool the coordinator doesn't have; give the coordinator every tool available: spawning would start working, but only by accident, because the full list happens to include `"Task"`. It breaks scoped tool access: the coordinator now holds search, fetch and delete tools it should hand to subagents, and too many tools make its tool choice worse. Add the one tool it needs, not all of them | D1 1.3 Subagent invocation and context passing; D2 2.3 Tool distribution and scoped access | [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context), [Lesson 2, section 2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones) |
| 2 | The synthesis agent writes as if it never saw the search results | **Pass the complete findings in its prompt.** Subagents don't inherit context. | Assume shared memory; have synthesis search again; a longer system prompt telling it that search already happened | D1 1.2 Coordinator-subagent orchestration; D1 1.3 Subagent invocation and context passing | [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke), [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context) |
| 3 | Search and analysis are independent and should run at the same time | **Several Task calls in a single coordinator response** | One Task call per turn; a background thread outside the SDK; have the search subagent spawn the analysis subagent itself, which chains the two, so analysis waits on search instead of running beside it | D1 1.3 Subagent invocation and context passing | [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context) |
| 4 | Two search agents return the same sources | **Partition the scope** by subtopic or source type | Deduplicate afterwards and pay for the overlap; add a third agent; tell both to "avoid overlap" in their prompts | D1 1.2 Coordinator-subagent orchestration | [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke) |
| 5 | Compare two report structures from the same 40-minute analysis without redoing the research | **Fork the session from the finished analysis**, one branch per structure: `fork_session` in the Agent SDK (`forkSession` in TypeScript), or `--fork-session` with `--resume`/`--continue` on the CLI. Each branch starts from the same baseline and the original stays untouched. | Rerun the whole research twice; build both structures one after the other in one session, so the second is shaped by the first; resume the same session and overwrite the first draft | D1 1.7 Session state, resumption and forking | [Lesson 1, section 1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#17-sessions-resume-and-fork) |
| 6 | One overloaded `manage_sources` tool (search, fetch, summarize or delete, picked by a free-text `action`) gets wrong actions and wrong arguments | **Split it into narrow, single-purpose tools**, such as `search_sources(query)`, `fetch_source(url)` and `summarize_source(source_id)`, each with a clear name, a description of what it does and returns, and its own input schema with typed, required fields. **Drop delete from the research agent entirely**; a researcher has no need to destroy sources. | Add few-shot examples of each action, which still leaves one free-text argument to get wrong and delete one typo away; add a system-prompt rule listing the valid actions, which the model can still misread and nothing enforces; raise the iteration cap so it can retry, which only pays for more wrong calls and doesn't undo a delete | D2 2.1 Tool interfaces and descriptions | [Lesson 2, section 2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#21-tool-descriptions-are-how-the-model-chooses) |
| 7 | One subtopic found nothing, another was refused access, and both come back as "No sources found" | Return a **structured result per subtopic that tells the two apart**: the empty one is a *valid empty result* (queries tried, no matches); the refused one is an *access failure* (which source, what error, what was tried, any partial results). The coordinator can then try another source for the refused subtopic, accept the true gap, and have synthesis mark coverage in the report. | One overall `status: "partial"` flag: the coordinator learns something went wrong but not where or what, so it has nothing to act on; log the refusal to a file and return the results as normal: the coordinator decides blind and the gap never reaches the report; tell the subagent in its prompt to "mention any problems in your summary": free text the coordinator can't reliably act on, and the two cases can still blur together | D5 5.3 Error propagation; D2 2.2 Structured error responses | [Lesson 5, section 5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#53-passing-errors-between-agents), [Lesson 2, section 2.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#22-structured-errors) |
| 8 | Final reports lose which source said what | **Structured claim-source mappings** (URL, document, excerpt, date) preserved through synthesis | Ask synthesis to "cite carefully"; append all URLs at the end; have a final agent search again and attach citations to the finished report, matching claims to sources after the fact (Anthropic's own research system runs a final CitationAgent (the last agent, which matches claims to the sources already collected) over the documents it already collected, as an extra check on top of claims that kept their sources, not instead of them; on the exam, pick the mappings) | D5 5.6 Provenance and uncertainty | [Lesson 5, section 5.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#56-provenance-and-uncertainty) |
| 9 | Two credible sources give different market-size numbers | **Include both, noting the conflict and crediting each source** (plus dates) | Pick the newer one; average them; let the model pick the one it finds more credible and drop the other | D5 5.6 Provenance and uncertainty | [Lesson 5, section 5.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#56-provenance-and-uncertainty) |
| 10 | The aggregated input fits, but findings from the middle are dropped | **A key-findings summary first, plus section headers.** Upstream agents return structured facts, not long prose. This is the "lost in the middle" effect: models handle the start and end of long input well and may miss the middle. | Switch to a model with a larger context window so the input takes up a smaller share of it: the input already fits, and the problem is *where* findings sit, not how much room there is, so a bigger window leaves the middle just as easy to miss; a longer prompt telling it to "read everything carefully": adds more text and doesn't change the position effect; cut the number of subagents so there's less input: shrinks the middle by losing coverage | D5 5.1 Preserving conversation context | [Lesson 5, section 5.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#51-keeping-the-facts-that-matter-in-long-conversations) |

**Scoring:** 8 or more is a pass. Decisions 2, 6 and 7 are where people usually go wrong:
*subagents see only what you pass them, the model picks tools by their descriptions, and an access
failure that looks like "no results" can't be recovered*.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 3 and task statements 1.2, 1.3, 1.7, 2.1, 2.2, 2.3, 5.1, 5.3, 5.6 (Tier 1); Claude Code docs on
[subagents](https://code.claude.com/docs/en/sub-agents) (Task renamed Agent in v2.1.63), the Agent SDK
[permissions](https://code.claude.com/docs/en/agent-sdk/permissions) (`allowedTools` pre-approves; checked 2026-10-07) and the
[CLI reference](https://code.claude.com/docs/en/cli-reference) (`--fork-session`) (Tier 1). Taught in
lessons [L01](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md),
[L02](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) and
[L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: one timeout, two broken files

**What changed:** the document-analysis subagent gets 9 sources. Reading one of them times out
once, then works on the next try. Two others are corrupt PDFs that can't be read at all.

**Question:** which problems does the subagent handle itself, and which does it pass up to the
coordinator?

<details><summary><b>Answer and why</b></summary>

**Handle the one-off timeout locally; report only what it can't fix.** The timeout is transient,
so the subagent retries it and moves on. Retrying can't repair a corrupt file, so it finishes the
other 7 and tells the coordinator which 2 failed, why, and that they aren't retryable. The
coordinator can then look for other sources or mark the gap.

**Why the others lose:** passing every hiccup up floods the coordinator with noise it can't fix
any better. Retrying the corrupt PDFs again and again wastes time, because a retry can't fix a
broken file.

**Tests:** Domain 5, task statement 5.3 (error propagation); also 2.2 (structured error responses).

**Lesson:** [Lesson 5, section 5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#53-passing-errors-between-agents) · [Deep practice, Domain 5](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/05-context-management-and-reliability.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 5.3 (Tier 1).

</details>

### Twist 2: the report writer holds tools it never needs

**What changed:** the report-writing subagent was defined with the same tools list as the search
agent: web search, fetch, and delete a saved source. The logs show it fetching new pages halfway
through a report and adding sources nobody checked. Once, it deleted a saved source.

**Question:** what do you change?

<details><summary><b>Answer and why</b></summary>

**Cut its tools list in its agent definition down to what writing needs** (reading the findings
it was given and writing the report). If it spots a gap, it says so in its output, and the
coordinator sends the search agent back out. Exam guide wording: "Restricting each subagent's
tool set to those relevant to its role, preventing cross-specialization misuse".

**Why the others lose:** a prompt line saying "don't search or delete" leaves the tools there to
misuse. A hook that logs every call tells you about a deleted source only after it's gone.
Merging the search and writing agents into one agent gives it even more tools, and more tools
mean worse tool choices.

**Tests:** Domain 2, task statement 2.3 (tool distribution and scoped access).

**Lesson:** [Lesson 2, section 2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones) · [Deep practice, Domain 2](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/02-tool-design-and-mcp-integration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 2.3 (Tier 1).

</details>

### Twist 3: a simple question goes through the whole pipeline

**What changed:** a user asks a quick factual question that one web search could answer. The
coordinator still runs search, document analysis, synthesis and report writing every time.

**Question:** how should the coordinator handle it?

<details><summary><b>Answer and why</b></summary>

**Let the coordinator choose which subagents to call based on how complex the query is.** A
simple question needs only the search subagent; a full research topic needs the whole team.

**Why the others lose:** always running the full pipeline costs time and money for no gain. A
separate pipeline built just for simple questions adds a second system to maintain when the
coordinator can already decide.

**Tests:** Domain 1, task statement 1.2 (coordinator-subagent orchestration).

**Lesson:** [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke) · [Deep practice, Domain 1](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/01-agentic-architecture-and-orchestration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 1.2 (Tier 1).

</details>

### Twist 4: one section of the draft rests on a single source

**What changed:** the synthesis draft is done, but one section rests on a single source, and
another subtopic barely appears.

**Question:** what does the coordinator do before the report is written?

<details><summary><b>Answer and why</b></summary>

**Check the synthesis for gaps, send targeted queries back to search and analysis, then run
synthesis again** until coverage is good enough. The coordinator owns that loop.

**Why the others lose:** shipping the report with a note that coverage is thin skips a fix that
was easy to make. Re-running the whole research from scratch throws away the good parts. Asking
the synthesis agent to "fill the gaps" makes it guess, because it has no search tools.

**Tests:** Domain 1, task statement 1.2 (coordinator-subagent orchestration).

**Lesson:** [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke) · [Deep practice, Domain 1](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/01-agentic-architecture-and-orchestration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 1.2 (Tier 1).

</details>

### Twist 5: two tools with names that sound the same

**What changed:** the system has two tools, `process_text` and `process_file`. One is meant for web
pages, the other for uploaded documents. The logs show the model calls the wrong one about a
third of the time.

**Question:** what's the fix?

<details><summary><b>Answer and why</b></summary>

**Rename them and sharpen their descriptions so they no longer overlap**, for example
`extract_web_page_facts` and `summarize_uploaded_document`. Each name and description should say
exactly what the tool takes in and returns. The model picks tools by their names and descriptions.

**Why the others lose:** a system-prompt rule saying which one to use is easy to misread and
nothing enforces it. Adding a router agent in front of the tools is a big fix for a naming
problem. Deleting one tool and making the other do both jobs loses a capability and leaves one
vaguer tool.

**Tests:** Domain 2, task statement 2.1 (tool interfaces and descriptions).

**Lesson:** [Lesson 2, section 2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#21-tool-descriptions-are-how-the-model-chooses) · [Deep practice, Domain 2](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/02-tool-design-and-mcp-integration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 2.1 (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: the subagents are defined, but the coordinator can't spawn any**

- **What's going on:** four job descriptions exist, but the boss can't hand out work.
- **Under the hood:** each subagent is an `AgentDefinition` (one subagent's prompt, tools, description). The coordinator spawns one with the `Task` tool. On the exam, choose Task in `allowedTools`. Today it's called `Agent`, and `allowedTools` only pre-approves tools (they run without asking); see [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today).
- **How to make the call:** if it never spawns *any* subagent, check `allowedTools` for `Task`; if it spawns the *wrong* one, fix descriptions. Exam wording (task statement 1.3): "the requirement that allowedTools must include "Task" for a coordinator to invoke subagents".
- **Why the tempting answers are wrong:**
  - **Sharper subagent descriptions:** they steer which one gets picked, not whether any can be spawned.
  - **List subagents in the prompt:** a prompt can't grant a tool.
  - **Give it every tool:** works by accident; breaks scoped access and tool choice.
- **Go deeper:** [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context), [Lesson 2, section 2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones)

**Decision 2: the synthesis agent acts like it never saw the search results**

- **What's going on:** the summary writer was never handed the notes.
- **Under the hood:** a subagent starts with a fresh context. It sees its own system prompt, its tools and the `prompt` text in the coordinator's `Task` call (plus project CLAUDE.md if loaded). The coordinator's history and other subagents' results aren't copied over.
- **How to make the call:** if the findings aren't in the synthesis agent's `Task` prompt, pass them there in full; if they are, look elsewhere. Exam wording (task statement 1.3): "subagents do not automatically inherit parent context or share memory between invocations".
- **Why the tempting answers are wrong:**
  - **Assume shared memory:** there is none between subagents.
  - **Synthesis searches again:** pays twice and still skips the analysis.
  - **Longer system prompt:** says search happened, but hands over no results.
- **Go deeper:** [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke), [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context)

**Decision 3: search and analysis should run at the same time**

- **What's going on:** two jobs don't depend on each other, so neither should wait.
- **Under the hood:** one coordinator response can hold several tool calls; the SDK runs them and returns each result. So two `Task` calls in one response let two subagents run side by side.
- **How to make the call:** does job B need job A's output? If not, put both Task calls in one response. If yes, run them one after the other. Exam wording (task statement 1.3): "emitting multiple Task tool calls in a single coordinator response rather than across separate turns".
- **Why the tempting answers are wrong:**
  - **One Task call per turn:** the jobs queue up, one per turn.
  - **Background thread outside the SDK:** the coordinator never gets the results back as tool results, and the SDK already runs both calls.
  - **Search spawns analysis:** chains the two, so analysis waits on search.
- **Go deeper:** [Lesson 1, section 1.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#13-spawning-subagents-and-passing-context)

**Decision 4: two search agents keep finding the same sources**

- **What's going on:** two people were sent to search the same shelf.
- **Under the hood:** subagents can't see each other; each knows only its own prompt. So only the coordinator can prevent overlap, when it writes each `Task` prompt.
- **How to make the call:** if two agents' prompts cover the same ground, partition by subtopic or source type; if scopes are already distinct, look elsewhere. Exam wording (task statement 1.2): "Partitioning research scope across subagents to minimize duplication (e.g., assigning distinct subtopics or source types to each agent)".
- **Why the tempting answers are wrong:**
  - **Deduplicate afterwards:** you still pay for the overlap.
  - **Add a third agent:** more searchers, not less overlap.
  - **"Avoid overlap" in prompts:** neither agent can see what the other found.
- **Go deeper:** [Lesson 1, section 1.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#12-coordinator-and-subagents-hub-and-spoke)

**Decision 5: compare two report structures without redoing 40 minutes of research**

- **What's going on:** you want two drafts from one finished pile of research.
- **Under the hood:** a session is the saved conversation. Forking copies it into a new session with its own unique session ID. Each branch starts from the same baseline; the original stays untouched.
- **How to make the call:** if you need two independent versions from one shared start, fork once per structure: `fork_session` in the Agent SDK (`forkSession` in TypeScript), or `--fork-session` with `--resume`/`--continue` on the CLI. If you're continuing one line of work, resume. Exam wording (task statement 1.7): "fork_session for creating independent branches from a shared analysis baseline to explore divergent approaches".
- **Why the tempting answers are wrong:**
  - **Rerun the research twice:** pays the 40 minutes twice.
  - **Both structures, one session:** the first draft shapes the second.
  - **Resume and overwrite:** loses the first draft.
- **Go deeper:** [Lesson 1, section 1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#17-sessions-resume-and-fork), [Agent SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions) (Tier 1)

**Decision 6: one overloaded `manage_sources` tool**

- **What's going on:** a free-text switch is easy to flip the wrong way.
- **Under the hood:** the model fills arguments from the tool's name, description and `input_schema` (rules for the tool's inputs). A free-text `action` has nothing checking it; typed, `required` (must be filled in) fields do.
- **How to make the call:** does each tool do exactly one job, with typed inputs? If one tool does several jobs picked by a free-text argument, split it into one tool per job with typed fields, then remove any job this agent never needs. Exam wording (task statement 2.1): "Splitting generic tools into purpose-specific tools with defined input/output contracts".
- **For this question:** `search_sources(query)`, `fetch_source(url)`, `summarize_source(source_id)`. Drop delete; researchers never need it.
- **Why the tempting answers are wrong:**
  - **Few-shot examples (sample calls in the prompt):** the free-text argument stays; delete is one typo away.
  - **Prompt rule:** nothing enforces it.
  - **Higher iteration cap (a limit on loop turns):** more wrong calls; deletes can't be undone.
- **Go deeper:** [Lesson 2, section 2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#21-tool-descriptions-are-how-the-model-chooses)

**Decision 7: "found nothing" and "refused access" look the same**

- **What's going on:** an empty room and a locked door got the same label.
- **Under the hood:** an empty search succeeded with zero matches; a refusal failed. MCP (the standard tool-plug-in protocol) tools flag failures with `isError` (a "call failed" marker).
- **How to make the call:** if queries ran and matched nothing, return a valid empty result listing them; if a source refused, return an access failure: which source, the error, what was tried, any partial results. The coordinator can then try another source, accept the true gap, and have synthesis mark the gap in the report. Exam wording (task statement 5.3): "Distinguishing access failures from valid empty results in error reporting so the coordinator can make appropriate decisions".
- **Why the tempting answers are wrong:**
  - **One `status: "partial"` flag:** not where or what.
  - **Log refusal to a file:** the coordinator decides blind.
  - **"Mention problems" rule:** free text, hard to act on.
- **Go deeper:** [Lesson 5, section 5.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#53-passing-errors-between-agents), [Lesson 2, section 2.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#22-structured-errors)

**Decision 8: reports lose which source said what**

- **What's going on:** facts got separated from where they came from.
- **Under the hood:** each handoff is text in a prompt or a returned result. Whenever a step rewrites findings as prose, the claim-to-source link can drop. Claims that travel as records (URL, document, excerpt, date) survive synthesis.
- **How to make the call:** follow one claim from the search agent to the final report. Is its source attached as data at every handoff? If any step rewrites it as prose, the link can break there; make that step pass claim-source records instead. Exam wording (task statement 5.6): "Requiring subagents to output structured claim-source mappings (source URLs, document names, relevant excerpts) that downstream agents preserve through synthesis".
- **Why the tempting answers are wrong:**
  - **"Cite carefully" instruction:** a request, not a structure.
  - **URL list at the end:** doesn't link claims to sources.
  - **Re-search, then attach citations:** matches claims to sources after the fact. (Anthropic's CitationAgent, a final agent, matches claims to collected sources, on top of kept mappings.)
- **Go deeper:** [Lesson 5, section 5.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#56-provenance-and-uncertainty)

**Decision 9: two credible sources give different market-size numbers**

- **What's going on:** two good sources disagree, and the reader deserves to know.
- **Under the hood:** the model has no hidden truth to check against, so any single number it picks is a guess that looks like a fact. Keeping both values with source and date also shows when they measured different years.
- **How to make the call:** if both sources are credible and disagree, include both, note the conflict, credit each with its date; if one isn't credible, there's no real conflict. Exam wording (task statement 5.6): "annotating conflicts with source attribution rather than arbitrarily selecting one value".
- **Why the tempting answers are wrong:**
  - **Pick the newer one:** newer isn't always right.
  - **Average them:** gives a number neither source reported.
  - **Let the model pick:** drops a credible source on a guess.
- **Go deeper:** [Lesson 5, section 5.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#56-provenance-and-uncertainty)

**Decision 10: it fits, but the middle gets dropped**

- **What's going on:** the reader skims the start and end, missing the middle.
- **Under the hood:** fitting in the context window (how much text the model can see at once) means it can see everything, not that it weighs it equally. Models handle the start and end of long input reliably and may miss the middle: the "lost in the middle" effect.
- **How to make the call:** if it fits but middle findings vanish, fix the layout: key-findings summary first, section headers, and structured facts, not prose, from upstream agents. If it doesn't fit, it's a size problem. Exam wording (task statement 5.1): "Placing key findings summaries at the beginning of aggregated inputs and organizing detailed results with explicit section headers to mitigate position effects".
- **Why the tempting answers are wrong:**
  - **Bigger context window:** it already fits; the middle stays easy to miss.
  - **"Read everything carefully":** doesn't change the position effect.
  - **Fewer subagents:** shrinks the middle by losing coverage.
- **Go deeper:** [Lesson 5, section 5.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#51-keeping-the-facts-that-matter-in-long-conversations)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-05](SIM-05-developer-productivity.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-02 — decision checkpoint

A lawyer asks for the current retention period of one named policy. One read-only lookup returns the authoritative clause and date. What is the best orchestration choice?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Use the bounded single-agent lookup and return the supported answer. The bounded question is already supported without specialist coordination overhead.

**Base choice:** A legal team compares three vendors on evidence retention, integration cost and deployment permissions. Assign dimensions, require source-tagged findings and let the coordinator integrate the comparison.

**Changed constraint and recovery:** The task becomes one known price lookup from an authorized source. One scoped agent is sufficient; decomposition overhead adds no evidence.

**Failure:** Cost returns, but retention is missing. Re-delegate retention with an explicit gap; do not publish a complete comparison.

**Nearest alternative:** Assigning one vendor to each specialist can hide inconsistent criteria unless the return contracts enforce the same dimensions.

**Conditional cue:** Split by evidence need; count coverage before conclusion.

**Proof:** Inspect `coverage={retention:pending,cost:complete,permissions:complete}; owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.2.md#variant-fv-02).

</details>

### SIM-FV-03 — decision checkpoint

Two independent channel audits must finish before synthesis; neither needs the other’s output. What should the coordinator do at dispatch?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Dispatch both independent investigations together with bounded scopes and quality criteria. Independent investigations can run in parallel without inventing a dependency.

**Base choice:** A marketing specialist checks audience evidence. Send the precise question, permitted data, exclusions, cited upstream findings and output contract, not a reference to another unseen chat.

**Changed constraint and recovery:** New consent evidence invalidates the audience assumption. Send the changed evidence and require a revised conclusion.

**Failure:** The specialist claims it used a result never included in its brief. Reject that claim and resend the bounded evidence packet.

**Nearest alternative:** Shared task naming is not shared conversation context; a bare “use the earlier findings” instruction is insufficient.

**Conditional cue:** Send scope, source and shape; never assume shared memory.

**Proof:** Inspect `brief={question:segment_fit,scope:consented_records,evidence:[source:CRM42],return:[finding,source,limits]}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.3.md#variant-fv-03).

</details>

### SIM-FV-06 — decision checkpoint

A campaign launch failure has an unknown cause; each log finding may expose a new dependency. Which decomposition fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Start an adaptive investigation that expands tasks as evidence reveals relevant dependencies. Unknown causes require investigation that responds to discoveries.

**Base choice:** A government intake follows a known sequence: validate, classify, route. Use an explicit workflow with defined outputs and stop states.

**Changed constraint and recovery:** The task becomes an open-ended investigation with unknown evidence paths. Use bounded adaptive decomposition and review discovered gaps.

**Failure:** After ten iterations the agent has activity but no evidence for one requirement. Stop or re-plan using the coverage ledger, not iteration count alone.

**Nearest alternative:** Multiple agents do not cure an unclear completion contract. Fixed steps are easier to test when the process is known.

**Conditional cue:** Known path: workflow; unknown path: bounded discovery.

**Proof:** Inspect `steps=[validate,classify,route]; done={valid:true,route_assigned:true}; missing=[]` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.6.md#variant-fv-06).

</details>

### SIM-FV-10 — decision checkpoint

A schema-constrained tool call returns an account identifier that is outside the requester’s authorization. What should the application do?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Reject the unauthorized operation even if invocation and schema validation succeeded. Invocation control and shape validation do not confer business authorization.

**Base choice:** Research specialists get only their relevant read tools. A separate authorized executor handles accepted mutations; the coordinator tracks ownership.

**Changed constraint and recovery:** One bounded read-only lookup fits a single agent with two relevant tools. Do not add agents merely to satisfy a tool-count slogan.

**Failure:** Forced tool choice invokes the named tool with invalid semantics. Authorization and application validation still reject it.

**Nearest alternative:** tool_choice governs invocation; it does not prove business permission, factual truth or a sound result.

**Conditional cue:** Choose the call; separately prove permission and meaning.

**Proof:** Inspect `tools={research:[search,read],executor:[approved_write]}; proposal_owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.3.md#variant-fv-10).

</details>

### SIM-FV-25 — decision checkpoint

After compaction, a referenced policy document is revised and the summary no longer establishes the applicable exception. What should happen?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Reacquire the revised source and revalidate the affected decision instead of reconstructing missing details. A changed source requires fresh evidence even when conversation state persists.

**Base choice:** A long marketing investigation stores the current question, accepted constraints, unresolved issues, source pointers and next bounded action before compaction.

**Changed constraint and recovery:** Source consent or policy changes. Refresh the relevant evidence and revise the stored decision state.

**Failure:** A summary drops the “do not contact” exception. Restore it from the source before proceeding; never infer that omitted means revoked.

**Nearest alternative:** Keeping every transcript token can overwhelm context. A compact record must retain decisive exceptions and reacquisition paths.

**Conditional cue:** Keep decisions and exceptions; reacquire the detail.

**Proof:** Inspect `state={question,constraints:[no_contact],sources:[CRM42],unresolved:[consent_age],next:verify}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.1.md#variant-fv-25).

</details>

### SIM-FV-27 — decision checkpoint

A different brief explicitly permits a partial overview; an optional source is unavailable and cannot be recovered now. Which output fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Return the permitted partial overview with attributed findings and an explicit unavailable-source limitation. Explicit permission for partial coverage changes whether a bounded output is acceptable.

**Base choice:** Specialists return findings and structured failures to the coordinator. Preserve successful evidence and decide which missing dimensions block the final claim.

**Changed constraint and recovery:** The unavailable source is explicitly optional. Publish a bounded partial answer with the omission and limitations visible.

**Failure:** A mandatory permissions source fails. Target that recovery or stop the affected conclusion; do not replace its facts with another specialist’s guess.

**Nearest alternative:** Discarding all successes wastes evidence; silently dropping a failed mandatory dimension fabricates completeness.

**Conditional cue:** Keep the successes; name the gap; block dependent claims.

**Proof:** Inspect `result={dimension:permissions,status:failed,reason:access_denied,retryable:false}; aggregate=partial` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.3.md#variant-fv-27).

</details>

### SIM-FV-30 — decision checkpoint

A supported federation now provides one query interface over both sources, but their records still conflict. What changes?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Return a structured claim-to-source mapping with document locators, relevant evidence and timestamps, retaining the conflict for the coordinator. A unified query interface does not replace structured claim-source mappings. Downstream synthesis needs attributable claims and explicit conflict, not inferred source identity.

**Base choice:** Separate finance and CRM interfaces return revenue and customer records with timestamps and field-level provenance. Join only under a declared identifier rule.

**Changed constraint and recovery:** The host offers supported federation. It may simplify retrieval, but still retain origin, time and conflict checks.

**Failure:** CRM says customer active while finance reports suspended at a different date. Preserve both assertions and their scope; ask for policy or current authoritative evidence.

**Nearest alternative:** A joined table can erase provenance and make mismatched-age sources look consistent. Federation does not establish truth by itself.

**Conditional cue:** Join identifiers; retain origins; expose disagreement.

**Proof:** Inspect `row={customer_id:C7,revenue:{value:120,source:FIN9,as_of:d1},status:{value:active,source:CRM4,as_of:d2}}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.6.md#variant-fv-30).

</details>


<span data-assessment-exposure="cct-fv-02-base-v1,cct-fv-02-retry-v1,cct-fv-03-base-v1,cct-fv-03-retry-v1,cct-fv-06-base-v1,cct-fv-06-retry-v1,cct-fv-10-base-v1,cct-fv-10-retry-v1,cct-fv-25-base-v1,cct-fv-25-retry-v1,cct-fv-27-base-v1,cct-fv-27-retry-v1,cct-fv-30-base-v1,cct-fv-30-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-02 — Cover dimensions before synthesizing](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.2.md#variant-fv-02) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.2&variant=FV-02)
- [FV-03 — Send an attributable handoff](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.3.md#variant-fv-03) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.3&variant=FV-03)
- [FV-06 — Choose decomposition by uncertainty](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.6.md#variant-fv-06) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.6&variant=FV-06)
- [FV-10 — Scope tools to the assigned role](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.3.md#variant-fv-10) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.3&variant=FV-10)
- [FV-25 — Compact the decision state, not just prose](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.1.md#variant-fv-25) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.1&variant=FV-25)
- [FV-27 — Propagate partial success without hiding failure](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.3.md#variant-fv-27) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.3&variant=FV-27)
- [FV-30 — Keep sources through a join](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.6.md#variant-fv-30) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.6&variant=FV-30)

**Build the mechanism:** [Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.