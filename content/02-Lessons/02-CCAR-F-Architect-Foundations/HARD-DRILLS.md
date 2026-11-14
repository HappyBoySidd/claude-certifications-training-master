# CCAR-F hard drills (45 scenario questions)

> **Project-authored, not official.** Written by this project from Anthropic's public CCAR-F exam guide. These are not real exam questions and are not paraphrased from any exam.

**Built from:** [exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications) section 6 (Tier 1). Scenarios are written by this project in its own words. They test the same task statements as the guide's 12 sample questions, but they are written to avoid reusing those questions' scenarios, numbers and answer options.

**How these are harder.** Some wrong options are a setting or a prompt request ("be careful", "always do X"), which is the trap in your diagnostic. But in most drills the strongest wrong option is a *real design change* that is wrong for this case: a routing classifier, retries with backoff, a stricter schema, a review instance used in the wrong place. So "pick the design change" is not enough. Ask two questions: *does this option change what the system can do, or only ask it nicely?* and then *of the design changes, which one fixes the cause named in the stem, at the lowest cost?*

Answers are in a collapsed block under each question. Cover them and commit to a letter first.

**Drills by domain.** Drill numbers are not in order inside a domain, because later batches were added at the end. These are every drill for each domain:

- **Domain 1, Agentic Architecture & Orchestration:** drills 1–8, 31–35, 42
- **Domain 2, Tool Design & MCP Integration:** drills 9–13, 36
- **Domain 3, Claude Code Configuration & Workflows:** drills 14–19, 37–38
- **Domain 4, Prompt Engineering & Structured Output:** drills 20–25, 39–40
- **Domain 5, Context Management & Reliability:** drills 26–30, 41, 43–45

## Domain 1: Agentic Architecture & Orchestration (27%, 14 drills)

### Drill 1 (task statement 1.1)

An insurance-claims agent sometimes stops halfway: it writes "I'll now check the policy database" and the loop ends without the call being made. Your loop exits whenever the response contains any text block. What is the best change?

- **A.** Loop while the reply text mentions a tool by name, and stop as soon as a reply no longer names any tool.
- **B.** Run the requested tools and continue while stop_reason is "tool_use"; stop on "end_turn".
- **C.** Keep looping until a fixed cap of 15 iterations is reached, so a pending tool call is never skipped.
- **D.** Tell Claude in the system prompt never to write any text before it makes a tool call.

<details><summary>Answer and why</summary>

**Answer: B.** stop_reason is the structured signal of whether Claude wants a tool. Checking for text content as a completion signal is a named anti-pattern.

- **A is wrong (design):** Parsing the reply's natural-language text to decide whether to loop is a named anti-pattern: the text can name a tool without calling it (as in this stem) or call one without naming it. The guide's loop is driven by stop_reason.
- **C is wrong (design):** An arbitrary iteration cap as the primary stopping rule is a named anti-pattern; it wastes turns on finished tasks and still cuts off long ones.
- **D is wrong (prompt):** A prompt request leaves the faulty exit check in place, and text before a tool call is normal behaviour.

Objective: 1.1 Design and implement agentic loops for autonomous task execution. Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1).

</details>

### Drill 2 (task statement 1.2)

A market-research system has a coordinator and four subagents (news, filings, social, synthesis). For simple questions like "what is Acme's ticker?" every subagent still runs, taking minutes. What is the best design change?

- **A.** Have the coordinator assess what each query needs and invoke only those subagents.
- **B.** Put a separate classifier in front that labels each query simple or complex, and run all four subagents for every complex one.
- **C.** Give every subagent a much shorter max_tokens so each one finishes sooner.
- **D.** Tell each subagent to reply "N/A" at once when a question is outside its area.

<details><summary>Answer and why</summary>

**Answer: A.** The guide's skill: a coordinator that analyses query requirements and dynamically selects subagents rather than always running the full pipeline.

- **B is wrong (design):** A real routing design, but too coarse: a complex query that needs only filings still runs all four. Choosing subagents per query is the coordinator's job.
- **C is wrong (setting):** Truncating output harms complex queries and still runs the whole pipeline for simple ones.
- **D is wrong (prompt):** Every subagent is still invoked and billed; the routing decision sits in the wrong place.

Objective: 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns. Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1).

</details>

### Drill 3 (task statement 1.3)

A due-diligence coordinator runs a contracts subagent, then a financials subagent, then a summary subagent. The summary often contradicts the contracts findings. Logs show the summary prompt contains only "Summarize the due-diligence findings." What is the fix?

- **A.** Give the summary subagent the contracts and financials tools so it can re-gather the findings itself.
- **B.** Turn on shared memory so the summary subagent inherits the coordinator's conversation history.
- **C.** Pass both prior outputs in full, with source metadata, in the summary prompt.
- **D.** Add "stay consistent with the earlier findings" to the summary subagent's system prompt.

<details><summary>Answer and why</summary>

**Answer: C.** Subagents see only their prompt. Including prior agents' complete findings, structured with metadata, is the guide's skill.

- **A is wrong (design):** A real design change, but it duplicates work and hands a synthesis agent tools outside its role, which invites misuse.
- **B is wrong (design):** Subagents don't inherit parent context; it must be passed explicitly. This mechanism isn't part of the design.
- **D is wrong (prompt):** It can't stay consistent with findings it never received.

Objective: 1.3 Configure subagent invocation, context passing, and spawning. Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1).

</details>

### Drill 4 (task statement 1.3)

A coordinator must query three independent data vendors through three subagents, and users wait for the answer live. Runs take about three times as long as any single vendor call. How do you cut the latency?

- **A.** Merge the three subagents into one agent that holds all three vendors' tools.
- **B.** Tell the coordinator in its prompt to "work quickly and in parallel where possible".
- **C.** Move the vendor queries into a nightly batch job so their latency no longer matters.
- **D.** Have the coordinator emit all three Task calls in one response.

<details><summary>Answer and why</summary>

**Answer: D.** Several Task tool calls in one coordinator response spawn parallel subagents; spreading them across turns makes them sequential. (Exam guide name: Task. Claude Code renamed it Agent in v2.1.63; existing `Task(...)` references in settings and agent definitions still work as aliases [code.claude.com/docs/en/sub-agents]. See [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

- **A is wrong (design):** This loses specialization and makes tool selection less reliable, and the calls may still run one after another.
- **B is wrong (prompt):** A vague request doesn't change how the calls are emitted. Parallelism comes from several Task calls in one response.
- **C is wrong (design):** A real cost design, but users need the answer live, so overnight results don't meet the need.

Objective: 1.3 Configure subagent invocation, context passing, and spawning. Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1); code.claude.com/docs/en/sub-agents (Tier 1).

</details>

### Drill 5 (task statement 1.4)

A telecom support agent escalates billing disputes to a human team. The humans can't see the bot conversation, and they complain that they have to re-ask customers everything. What is the best change?

- **A.** Hand over a structured summary: account ID, disputed charges, root cause, recommended action.
- **B.** Give the human team read access to the full raw transcript and tool logs for each escalated case.
- **C.** Have the agent ask the customer to restate the whole problem, from the start, just before the transfer.
- **D.** Stop escalating billing disputes, and let the agent resolve all of them itself, whatever the amount.

<details><summary>Answer and why</summary>

**Answer: A.** The guide's handoff skill: a structured summary (customer ID, root cause, amounts, recommended action) for humans who lack the transcript.

- **B is wrong (design):** A real design change, but raw logs make each human dig for the facts. The guide calls for a compiled, structured summary.
- **C is wrong (prompt):** This repeats the customer's pain instead of passing what the agent already knows.
- **D is wrong (design):** Some disputes need a human; removing escalation trades one problem for a worse one.

Objective: 1.4 Implement multi-step workflows with enforcement and handoff patterns. Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1).

</details>

### Drill 6 (task statement 1.5)

An HR agent may call update_salary. Policy: any raise over 10% needs human approval. It must hold every time, even when a user argues persuasively. What do you implement?

- **A.** A clear system-prompt rule plus three few-shot examples of refusing raises over 10%.
- **B.** A PreToolUse hook that blocks update_salary calls over 10% and routes them to human approval.
- **C.** Remove update_salary from the agent and have HR staff enter every raise by hand.
- **D.** Check the raise in a PostToolUse hook and roll it back if it is over 10%.

<details><summary>Answer and why</summary>

**Answer: B.** A hook that intercepts the outgoing call gives a deterministic guarantee and redirects to an alternative workflow (human approval).

- **A is wrong (prompt):** Strong prompting is still probabilistic; a persuasive user can push the model past it.
- **C is wrong (design):** It's safe, but it throws away the allowed automation for the many raises under 10%.
- **D is wrong (design):** A real hook, but at the wrong point: PostToolUse runs after the salary has already changed, so the rule is broken before the rollback.

Objective: 1.5 Apply Agent SDK hooks for tool call interception and data normalization. Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1).

</details>

### Drill 7 (task statement 1.6)

Each quarter you review the same five aspects (security, licensing, performance, docs, tests) of a known set of 12 services. Results vary a lot between runs. Which decomposition fits best?

- **A.** A fixed prompt chain: each aspect per service in turn, then a cross-service integration pass.
- **B.** A dynamic plan where the agent generates new subtasks each run from whatever it notices first.
- **C.** One subagent per service, each free to decide which aspects it checks this quarter.
- **D.** Keep the current single prompt, adding "be thorough and consistent".

<details><summary>Answer and why</summary>

**Answer: A.** Predictable multi-aspect reviews suit prompt chaining; the separate integration pass catches cross-cutting issues.

- **B is wrong (design):** Dynamic decomposition suits open-ended investigation. Here the work is known, and adaptivity adds the variance you want to remove.
- **C is wrong (design):** Letting each subagent choose its aspects makes coverage differ between services and between runs.
- **D is wrong (prompt):** A vague instruction doesn't fix a decomposition problem.

Objective: 1.6 Design task decomposition strategies for complex workflows. Source: CCAR-F exam guide v1.0, section 6, task statement 1.6 (Tier 1).

</details>

### Drill 8 (task statement 1.7)

Yesterday a Claude Code session named 'payments-audit' spent three hours analysing a 30-file payments module. The analysis is still valid and costly to redo. Overnight a teammate rewrote two of the files. How do you continue today?

- **A.** Start a new session and inject a structured summary of yesterday's findings.
- **B.** Resume the session as it is; the analysis is mostly correct, so no extra step is needed.
- **C.** Fork the session with fork_session and have the fork re-analyse all 30 files.
- **D.** Resume with --resume payments-audit and tell Claude which two files changed.

<details><summary>Answer and why</summary>

**Answer: D.** Resume when prior context is mostly valid, and tell the agent about specific file changes for targeted re-analysis.

- **A is wrong (design):** A real option, and the right one when prior tool results are mostly stale. Here they are mostly valid, so resuming keeps more.
- **B is wrong (design):** The session doesn't know about the edits and will reason from stale results for those two files.
- **C is wrong (design):** Forking is for exploring divergent approaches from a shared baseline. Re-analysing everything wastes the valid work.

Objective: 1.7 Manage session state, resumption, and forking. Source: CCAR-F exam guide v1.0, section 6, task statement 1.7 (Tier 1).

</details>

### Drill 31 (task statement 1.3, 1.3K3)

A pharma safety team's Agent SDK coordinator spawns a literature-search subagent and a case-narrative subagent from one generic definition. Search requests keep going to the narrative subagent, which has also called web search, a tool policy forbids for it. The team already tried a prompt line naming each subagent's role. What should you change?

- **A.** Force tool_choice on the coordinator so any request mentioning a study or journal goes to the search subagent.
- **B.** Give each subagent its own AgentDefinition: a when-to-use description, its own prompt, and a tools list that leaves web search out of the narrative role.
- **C.** Merge the two subagents into a single agent that holds every search and writing tool, so the coordinator never has to choose between them.
- **D.** Keep the one shared generic definition, and add a PreToolUse hook that denies any web-search call made while the subagent is working on a case narrative.

<details><summary>Answer and why</summary>

**Answer: B.** AgentDefinition carries a description (which the coordinator uses to choose), a prompt and a tools restriction. Distinct definitions fix both the misrouting and the forbidden tool.

- **A is wrong (setting):** Keyword routing misses requests that don't use those words, and web search stays available to the narrative subagent.
- **C is wrong (design):** This removes the choice by removing specialization, and it hands web search to the narrative work the policy forbids.
- **D is wrong (design):** A real control for the forbidden tool, but it patches one symptom: with one generic definition the coordinator still has no per-role description to route by, so search requests keep going to the narrative subagent.

Objective: 1.3 Configure subagent invocation, context passing, and spawning. Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1); code.claude.com/docs/en/agent-sdk/subagents (Tier 1).

</details>

### Drill 32 (task statement 1.4, 1.4S2)

A bank's KYC assistant gets one live message raising three issues: a rejected passport upload, a frozen debit card and a disputed onboarding fee. Each needs a different backend lookup, and all three share the same verified customer. Today the agent resolves the first issue and drops the other two. What is the best design?

- **A.** Handle the three issues one after another in the same turn, re-fetching the customer's context from the backend before each one.
- **B.** Add a system-prompt line telling the agent to always address every issue the customer mentions.
- **C.** Split it into three items, check each in parallel on the shared context, then send one reply.
- **D.** Send any message that raises more than one issue straight to a human KYC analyst, with a note listing each issue.

<details><summary>Answer and why</summary>

**Answer: C.** The guide's skill: decompose a multi-concern request into distinct items, investigate each in parallel using shared context, then synthesize a unified resolution.

- **A is wrong (design):** Serial handling keeps a live customer waiting, and re-fetching throws away the shared verified context instead of reusing it.
- **B is wrong (prompt):** A request to be thorough doesn't give the agent a decomposition step; the drop-off continues.
- **D is wrong (design):** Escalation is for policy gaps, explicit requests or no progress, not for routine multi-part requests the agent can handle.

Objective: 1.4 Implement multi-step workflows with enforcement and handoff patterns. Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1).

</details>

### Drill 33 (task statement 1.2, 1.2S3)

A legal-discovery coordinator sends custodians' email sets to search and analysis subagents, then a synthesis subagent drafts a privilege-risk memo. Partners say memos often skip whole custodians, though each subagent works correctly when asked. The deadline allows extra passes but not a human check of every memo. What should the coordinator do?

- **A.** Run the full pipeline three separate times on every matter and keep whichever memo lists the most custodians.
- **B.** Tell the synthesis subagent in its prompt to make sure every custodian is covered in the memo.
- **C.** Give the synthesis subagent the search and analysis tools so it can fill any gaps it notices by itself.
- **D.** Check each memo for missing custodians, re-delegate targeted searches for them, and re-run synthesis.

<details><summary>Answer and why</summary>

**Answer: D.** The guide's iterative refinement loop: the coordinator evaluates synthesis for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient.

- **A is wrong (design):** Blind repetition costs three times as much and never targets the specific gap.
- **B is wrong (prompt):** Synthesis can't cover custodians whose material it never received.
- **C is wrong (design):** Tools outside a role invite misuse, and routing around the coordinator loses observability and control.

Objective: 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns. Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1).

</details>

### Drill 34 (task statement 1.3, 1.3S4)

A public-sector benefits agency's coordinator briefs research subagents with a fixed twelve-step prompt: search site A, then site B, then summarize. When a question needs a source not on the list, subagents follow the steps anyway and return thin answers. Approved sources change monthly. What is the best rewrite of the briefs?

- **A.** State the research goal and quality criteria (source types, recency, coverage) and let subagents choose how to search.
- **B.** Add more steps that cover every source the agency might ever need, and have someone update the step list by hand each month.
- **C.** Raise max_tokens for each research subagent so it has room to go beyond the twelve listed steps.
- **D.** Add 'use your judgment if the steps don't fit' to the end of the twelve steps.

<details><summary>Answer and why</summary>

**Answer: A.** The guide: coordinator prompts should specify goals and quality criteria rather than step-by-step procedures, so subagents can adapt.

- **B is wrong (design):** A longer procedure is still a procedure; it breaks the next time a source changes.
- **C is wrong (setting):** Output length isn't the limit; the fixed steps are.
- **D is wrong (prompt):** A vague escape hatch without criteria gives the subagent nothing to judge against.

Objective: 1.3 Configure subagent invocation, context passing, and spawning. Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1).

</details>

### Drill 35 (task statement 1.5)

An insurer's Agent SDK agent pulls policy records from three MCP servers that return dates as Unix timestamps, ISO 8601 strings and US-format text. It sometimes miscalculates coverage periods. Denying calls would stall live claims, and an earlier prompt fix didn't hold. Which hook fits best?

- **A.** A PreToolUse hook that denies any call to a server whose dates are not already in ISO 8601 format.
- **B.** A PostToolUse hook that converts every returned date to ISO 8601 before the model reads the result.
- **C.** A UserPromptSubmit hook that adds the three date formats and conversion steps to each user message.
- **D.** A Stop hook that re-checks every coverage period after the agent has finished writing its answer.

<details><summary>Answer and why</summary>

**Answer: B.** PostToolUse runs after the tool and can replace what the model sees (in the Agent SDK, through updatedToolOutput), which is the guide's normalization pattern. It blocks nothing.

- **A is wrong (design):** PreToolUse is the right event for blocking, but denying calls would stall live claims and the data would never arrive.
- **C is wrong (prompt):** It's a hook, but what it adds is still prompt guidance, which already failed once; the tool results stay unconverted.
- **D is wrong (design):** It fires too late: the wrong reasoning has already happened, and Stop doesn't change tool results.

Objective: 1.5 Apply Agent SDK hooks for tool call interception and data normalization. Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1); code.claude.com/docs/en/hooks and code.claude.com/docs/en/agent-sdk/hooks, hooks reference for Claude Code and the Agent SDK (Tier 1). Hook event names can change: check the current docs.

</details>

### Drill 42 (task statement 1.1, stop_reason full handling)

A public-sector records agent's loop continues on stop_reason "tool_use" and treats anything else as done. Some long answers are cut off mid-sentence, and auditors require the stop reasons these turns produce to be handled explicitly. Some server web-search turns end with pause_turn, and a few requests end with refusal. Which handling is right?

- **A.** Continue on tool_use; treat end_turn, max_tokens, pause_turn and refusal alike as finished, and log the text that came back.
- **B.** Continue on tool_use; on max_tokens continue or raise the limit; on pause_turn send the reply back; on refusal read stop_details and fall back.
- **C.** Add a cap of 20 iterations, and keep looping until the model's text contains the word DONE, then return that text.
- **D.** Tell Claude in the system prompt to keep answers short, never pause during a web search, and never refuse a request.

<details><summary>Answer and why</summary>

**Answer: B.** Stretch: beyond the guide. Task statement 1.1 names tool_use and end_turn; the other values come from the current API docs. Each stop_reason needs its own branch: max_tokens means truncated (raise the limit or continue), pause_turn means a server-tool loop paused and you send the assistant content back to continue, and on refusal you read stop_details (the policy category) and retry on another Claude model rather than resend the same request unchanged.

- **A is wrong (design):** This is today's bug: truncated and paused turns are reported as complete answers.
- **C is wrong (design):** An iteration cap as the main stop and parsing text for completion are both named anti-patterns, and neither handles each stop explicitly.
- **D is wrong (prompt):** The model can't promise not to pause or refuse; the loop must handle each signal.

Objective: 1.1 Design and implement agentic loops for autonomous task execution. Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1); platform.claude.com/docs/en/build-with-claude/handling-stop-reasons and /refusals-and-fallback (Tier 1). stop_reason values can change: check the current docs.

</details>

## Domain 2: Tool Design & MCP Integration (18%, 6 drills)

### Drill 9 (task statement 2.1)

A shopping agent has get_order_status and search_catalog, each with a detailed description, input formats and examples. Since a system-prompt update, questions like "is my order of running shoes on its way?" trigger catalog searches. The update added: "Whenever the user mentions a product name, call search_catalog." What is the best fix?

- **A.** Remove the keyword rule from the system prompt, and let the detailed tool descriptions drive selection.
- **B.** Add a second rule: "If the user mentions an order, call get_order_status instead."
- **C.** Lower the temperature so the agent applies its rules more consistently.
- **D.** Add a PreToolUse hook that blocks search_catalog whenever the message mentions an order.

<details><summary>Answer and why</summary>

**Answer: A.** The descriptions are already good. Keyword-sensitive system-prompt instructions create unintended tool associations that override them, so the fix is to remove the rule.

- **B is wrong (prompt):** Stacking keyword rules makes the conflict worse: a message with a product name and an order now matches both.
- **C is wrong (setting):** The agent is already following the rule consistently; the rule is the cause.
- **D is wrong (design):** A real code control, but it patches one symptom with brittle keyword matching and leaves the faulty rule in place for every other case.

Objective: 2.1 Design effective tool interfaces with clear descriptions and boundaries. Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1).

</details>

### Drill 10 (task statement 2.2)

A ticketing MCP tool returns {"error": "failed"} for every failure. The agent retries rejected priority changes (a policy violation) five times, then tells the customer the system is down. What should you change?

- **A.** Return isError with errorCategory "business", isRetryable false and a plain explanation.
- **B.** Add retry with exponential backoff inside the tool before any error reaches the agent.
- **C.** Add to the agent's prompt: "If a tool fails, retry at most twice."
- **D.** Cap retries at one in the agent loop so rejected changes fail fast.

<details><summary>Answer and why</summary>

**Answer: A.** Structured error metadata lets the agent see a non-retryable business error and explain it properly.

- **B is wrong (design):** Backoff is the right design for transient errors, but a policy rejection will never succeed, so it only adds delay.
- **C is wrong (prompt):** The agent still can't tell a policy rejection from an outage.
- **D is wrong (design):** Fewer retries still treats every failure the same, and transient errors that deserve a retry lose it.

Objective: 2.2 Implement structured error responses for MCP tools. Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1).

</details>

### Drill 11 (task statement 2.3)

A document-classification agent has 22 tools, including web fetch, email and calendar. It sometimes emails partial summaries when it should only classify documents. What is the best design change?

- **A.** Warn it firmly in the system prompt: "Never send email while you are classifying documents, under any circumstances."
- **B.** Keep all 22 tools, but put a human approval step in front of every email the agent tries to send out.
- **C.** Give it only its few classification tools, and move email to the agent that owns notifications.
- **D.** Set tool_choice to "any" so it must pick a tool on every turn.

<details><summary>Answer and why</summary>

**Answer: C.** Scoped tool access (4-5 role tools, not 20+) improves selection and removes the chance of misuse.

- **A is wrong (prompt):** The tool stays in reach. Agents with tools outside their role tend to misuse them.
- **B is wrong (design):** A real control, but it treats the symptom. The crowded toolset still degrades selection, and humans now review emails that should never exist.
- **D is wrong (setting):** It forces a tool call but says nothing about which; email is still possible.

Objective: 2.3 Distribute tools appropriately across agents and configure tool choice. Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1).

</details>

### Drill 12 (task statement 2.3)

A contract-intake flow must call classify_document before any enrichment tool runs. In 6% of runs Claude goes straight to enrichment. What should you do?

- **A.** Put "always call classify_document first" at the top of the system prompt in bold.
- **B.** On the first request set tool_choice to {"type": "tool", "name": "classify_document"}.
- **C.** On the first request set tool_choice to "any" so that some tool is always called before any text.
- **D.** Split classification and enrichment into two agents linked by a message queue.

<details><summary>Answer and why</summary>

**Answer: B.** Forced tool selection guarantees that tool is called first; enrichment then runs in follow-up turns. What changed since: on the models listed in the forced-tool-use table in Define tools (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, checked 2026-10-21), tool_choice any and tool return a 400 whatever the thinking setting, and with manual extended thinking they error on any model. Current docs say to use auto with strict tool use, or structured outputs [platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]. The exam answer is unchanged.

- **A is wrong (prompt):** Position and emphasis are still prompt guidance and will fail sometimes.
- **C is wrong (setting):** "any" guarantees a tool call but not which one; enrichment can still go first.
- **D is wrong (design):** A real architecture change, but far heavier than needed; one forced tool_choice solves the ordering.

Objective: 2.3 Distribute tools appropriately across agents and configure tool choice. Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1); platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools (Tier 1).

</details>

### Drill 13 (task statement 2.4)

Your team wants a shared database MCP server in Claude Code. One developer also tests an experimental scraping server. Credentials must not reach git. What setup is right?

- **A.** Put both servers in the project .mcp.json with their tokens written inline, and add .mcp.json to .gitignore.
- **B.** Put both servers in each developer's own ~/.claude.json, and document the setup steps in the project README.
- **C.** Put both servers in the project .mcp.json, with the experimental one commented out until it is ready to share.
- **D.** Shared server in project .mcp.json via ${DB_TOKEN}; experimental one in that developer's ~/.claude.json.

<details><summary>Answer and why</summary>

**Answer: D.** This is a config-scope question: project scope for shared tooling, environment-variable expansion for secrets, user scope for personal experiments. That is the guide's split.

- **A is wrong (design):** Ignoring the file stops it being shared, which defeats the purpose, and inline secrets are a risk.
- **B is wrong (design):** Shared team tooling belongs in project scope so everyone gets it on clone; manual setup drifts.
- **C is wrong (design):** Experimental servers are personal; committing them, even disabled, puts them in the wrong scope.

Objective: 2.4 Integrate MCP servers into Claude Code and agent workflows. Source: CCAR-F exam guide v1.0, section 6, task statement 2.4 (Tier 1).

</details>

### Drill 36 (task statement 2.5, 2.5S5 · multiple response)

In a manufacturing-quality codebase of 1,400 files, sensor calls go through a wrapper package, qc/sensors, that re-exports eight vendor functions under new names. Before a vendor change you must find every real caller without reading every file. Grepping for the vendor library finds only the wrapper. What should Claude Code do? Select 2.

- **A.** Grep for qc/sensors import statements and treat each importing file as a caller.
- **B.** Glob for the wrapper package's files, then Read them to list every exported name.
- **C.** Use Glob with the pattern **/*sensor* to find every calling module by its file name across the codebase.
- **D.** Grep for each exported name across the codebase to find the real modules that call it.

<details><summary>Answer and why</summary>

**Answer: B and D.** Step one of the guide's wrapper-tracing skill: identify all exported names first. Glob finds files by path; Read loads them. Step two: search for each exported name. Grep searches file contents, which is what finding callers needs.

- **A is wrong (design):** Importing the package isn't calling the eight functions, and imports via aliases or other modules slip through; search for the exported names.
- **C is wrong (design):** Glob matches paths, not contents; callers don't have to have 'sensor' in their file names.

Objective: 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively. Source: CCAR-F exam guide v1.0, section 6, task statement 2.5 (Tier 1); code.claude.com/docs/en/tools-reference, Claude Code tools reference (Tier 1).

</details>

## Domain 3: Claude Code Configuration & Workflows (20%, 8 drills)

### Drill 14 (task statement 3.1)

Half your team's Claude Code sessions follow the API error-handling convention; the other half don't. The convention lives in the tech lead's ~/.claude/CLAUDE.md. What is the fix?

- **A.** Move it into the project CLAUDE.md (or .claude/rules/) in the repo, then check with /memory.
- **B.** Ask every developer to paste the convention into their first prompt of each session.
- **C.** Turn it into a path-scoped rule file in the tech lead's ~/.claude/rules/ folder.
- **D.** Have everyone raise the effort setting so that Claude looks harder for team conventions in the repo.

<details><summary>Answer and why</summary>

**Answer: A.** User-level files are personal and not shared through version control. Project-level files are, and /memory shows what is loaded. (Exam answer. Today `/memory` lists memory file locations; `/context` lists, under Memory files, the CLAUDE.md files loaded at launch. A subfolder CLAUDE.md loads later, when Claude reads a file there, and a "Loaded …" line with its path appears in the terminal; path-scoped rules also load later, and the InstructionsLoaded hook can log them.)

- **B is wrong (prompt):** Manual pasting is unreliable and doesn't fix where the convention lives.
- **C is wrong (design):** A real modular design, but still in the user's home folder, so teammates still don't get it.
- **D is wrong (setting):** No setting can surface instructions that were never loaded.

Objective: 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization. Source: CCAR-F exam guide v1.0, section 6, task statement 3.1 (Tier 1).

</details>

### Drill 15 (task statement 3.2)

A codebase-audit skill dumps thousands of lines of analysis, and afterwards the main session loses track of the task. The skill should also never edit files. Which configuration is best?

- **A.** Add "keep your output short, and never modify any files" to the instructions in the skill body.
- **B.** Move the audit steps into CLAUDE.md so they are always loaded.
- **C.** In SKILL.md frontmatter, set context: fork and limit allowed-tools to read-only tools.
- **D.** Run /compact after each audit, and ask Claude in the prompt not to edit files while auditing.

<details><summary>Answer and why</summary>

**Answer: C.** context: fork isolates verbose output in a sub-agent context, and allowed-tools restricts what the skill can use. (Exam guide wording. In current Claude Code, allowed-tools pre-approves tools and disallowed-tools removes them. To block edits today, list Edit and Write under disallowed-tools. See [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

- **A is wrong (prompt):** Prompt requests may be ignored, and verbose analysis is the skill's job anyway.
- **B is wrong (design):** CLAUDE.md is for always-loaded universal standards; this would bloat every session.
- **D is wrong (design):** /compact cleans up after the damage, and the no-edit rule is still only a request.

Objective: 3.2 Create and configure custom slash commands and skills. Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1).

</details>

### Drill 16 (task statement 3.3)

Your file .claude/rules/migrations.md has frontmatter paths: ["db/*.sql"]. Migrations live in db/migrations/2026/ and in services/*/db/. When Claude edits them, the rule never loads. What is the fix?

- **A.** Replace the rule with a CLAUDE.md in each migrations folder.
- **B.** Change the glob to "**/db/**/*.sql" to match .sql files under any db folder.
- **C.** Remind Claude in every migration prompt to follow the team's migration conventions.
- **D.** Move the migration conventions into the root CLAUDE.md so they always load, everywhere.

<details><summary>Answer and why</summary>

**Answer: B.** "db/*.sql" matches only files directly under a top-level db/. A recursive glob matches the files where they really live.

- **A is wrong (design):** A directory CLAUDE.md loads for everything in its folder, duplicates the rules in many places and misses new folders. Path globs are the guide's answer for files spread across the codebase.
- **C is wrong (prompt):** Per-prompt reminders are unreliable and easy to forget.
- **D is wrong (design):** It works, but loads migration rules into every task, which is what path-scoped rules exist to avoid.

Objective: 3.3 Apply path-specific rules for conditional convention loading. Source: CCAR-F exam guide v1.0, section 6, task statement 3.3 (Tier 1).

</details>

### Drill 17 (task statement 3.4)

A two-phase task: first find every use of a deprecated logger (hundreds of hits across the repo), then design its replacement. After the search, the main session is nearly full and starts forgetting earlier decisions. What should you have done?

- **A.** Used direct execution and replaced each logger call as soon as the search found it.
- **B.** Run the whole search in plan mode in the main session so nothing gets edited while searching.
- **C.** Run the discovery in the Explore subagent, which returns a summary to the main session.
- **D.** Asked Claude to keep its search output short.

<details><summary>Answer and why</summary>

**Answer: C.** The Explore subagent isolates verbose discovery and returns a summary, preserving the main session for design.

- **A is wrong (design):** Skipping the design phase on a repo-wide change invites rework, and the hits still flood the context.
- **B is wrong (design):** Plan mode makes exploration safe from edits, but the verbose output still fills the main context.
- **D is wrong (prompt):** Hundreds of hits are hundreds of hits; a request doesn't isolate them.

Objective: 3.4 Determine when to use plan mode vs direct execution. Source: CCAR-F exam guide v1.0, section 6, task statement 3.4 (Tier 1).

</details>

### Drill 18 (task statement 3.5)

You ask Claude Code to convert legacy address strings into a structured format. Prose descriptions keep giving inconsistent results on edge cases such as PO boxes. What is the most effective next step?

- **A.** Give 2-3 concrete input/output examples, including a PO box.
- **B.** Rewrite the prose description in more detail, with a paragraph on PO boxes.
- **C.** Add a second Claude instance that reviews each converted address and corrects mistakes.
- **D.** Ask Claude to "double-check edge cases" before finishing.

<details><summary>Answer and why</summary>

**Answer: A.** Concrete input/output examples communicate a transformation best when prose is read inconsistently.

- **B is wrong (prompt):** More prose is the approach that is already failing.
- **C is wrong (design):** Independent review is a real pattern, but the reviewer has the same unclear spec. Examples fix the spec itself.
- **D is wrong (prompt):** A vague self-check doesn't show what correct output looks like.

Objective: 3.5 Apply iterative refinement techniques for progressive improvement. Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1).

</details>

### Drill 19 (task statement 3.6)

A nightly CI job runs Claude Code to write tests for changed modules. Many suggested tests duplicate ones that already exist, and they ignore the team's fixtures. What do you change?

- **A.** Add a Claude review step that deletes duplicate tests after generation, and name the fixtures in the CI prompt.
- **B.** Add "don't write tests that already exist" and "use the team's fixtures" to the CI prompt text.
- **C.** Switch to --output-format json with a JSON schema for the tests, so every test comes back in one fixed shape.
- **D.** Include the existing test files in context, and document test standards and fixtures in the project CLAUDE.md.

<details><summary>Answer and why</summary>

**Answer: D.** The guide's CI skills: provide existing tests in context, and give CI-invoked Claude Code the testing standards and fixtures through CLAUDE.md. What changed since: `claude -p --bare` (recommended for scripted calls and planned as the `-p` default) skips CLAUDE.md, so in bare mode pass the standards another way, for example with `--append-system-prompt` or by putting the file in the prompt [code.claude.com/docs/en/headless]. The exam answer is unchanged.

- **A is wrong (design):** A real pattern used for the wrong job: Claude still never sees the existing tests, so it generates duplicates that are then thrown away, and fixture names alone don't give it the team's testing standards.
- **B is wrong (prompt):** Claude can't avoid duplicating tests it hasn't seen.
- **C is wrong (setting):** Structured output helps parsing, not test quality or duplication.

Objective: 3.6 Integrate Claude Code into CI/CD pipelines. Source: CCAR-F exam guide v1.0, section 6, task statement 3.6 (Tier 1); code.claude.com/docs/en/headless (Tier 1).

</details>

### Drill 37 (task statement 3.2 · multiple response)

A healthcare-claims engineering team keeps a 400-line release checklist in the project CLAUDE.md, so every session loads it, though it's used about twice a month. When developers do run it, they often forget to give the release number. The checklist must stay shared through git. Which changes fix both problems? Select 2.

- **A.** Move the checklist into each developer's ~/.claude/CLAUDE.md to keep it out of the project file.
- **B.** Add 'always ask for the release number first' near the top of the project CLAUDE.md.
- **C.** Move the checklist into a project skill in .claude/skills/ so it loads only when invoked.
- **D.** Add argument-hint: [release-number] to that skill's frontmatter, so developers are prompted for the release number.

<details><summary>Answer and why</summary>

**Answer: C and D.** Skills are on-demand for task-specific workflows; CLAUDE.md is for always-loaded universal standards. A project skill stays in git. Builds on C: argument-hint in the skill frontmatter prompts for required parameters when the skill is invoked without them.

- **A is wrong (design):** It's still loaded in every session, and user-level files aren't shared through git.
- **B is wrong (prompt):** A request in an always-loaded file fixes neither the load cost nor reliably the missing argument.

Objective: 3.2 Create and configure custom slash commands and skills. Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1); code.claude.com/docs/en/skills and code.claude.com/docs/en/memory, Claude Code skills and memory docs (Tier 1). Frontmatter fields can change: check the current docs.

</details>

### Drill 38 (task statement 3.5)

Claude Code is refactoring a bank's KYC risk-scoring module. You found three problems: score rounding is wrong, a threshold check that reads the rounded score is off by one, and an unrelated log message has a typo. Fixing the rounding alone changes which threshold cases fail. How should you send the fixes?

- **A.** Send all three problems in one long message so Claude has everything in front of it at once.
- **B.** Fix each of the three problems in its own message, one after another, in the order you found them.
- **C.** Send the rounding and threshold problems together in one detailed message, and fix the typo separately.
- **D.** Ask Claude to be extra careful about side effects between changes, then send the three problems in whatever order is convenient.

<details><summary>Answer and why</summary>

**Answer: C.** The guide: give interacting issues in one message, because their fixes affect each other; fix independent ones sequentially.

- **A is wrong (design):** Bundling the unrelated typo adds noise; only the interacting problems belong together.
- **B is wrong (design):** Sequential fixes suit independent problems; here the rounding fix shifts the threshold failures, so they must be solved together.
- **D is wrong (prompt):** Care doesn't supply the information that the two fixes interact.

Objective: 3.5 Apply iterative refinement techniques for progressive improvement. Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1).

</details>

## Domain 4: Prompt Engineering & Structured Output (20%, 8 drills)

### Drill 20 (task statement 4.1)

Your review bot flags many "possible performance issues" that developers dismiss, and they've started ignoring its security findings too. What is the best fix?

- **A.** Add "only report issues you are highly confident about" to the review prompt for every category.
- **B.** Turn off the performance category for now; write explicit report/skip criteria before turning it back on.
- **C.** Send every performance finding to a second Claude instance to confirm before posting.
- **D.** Have the bot attach a confidence score to each finding, and post only findings scored above 0.8.

<details><summary>Answer and why</summary>

**Answer: B.** Temporarily disabling a high false-positive category restores trust; explicit categorical criteria fix precision.

- **A is wrong (prompt):** The guide: confidence-based instructions don't improve precision.
- **C is wrong (design):** A real review design, but the confirmer works from the same vague criteria, and trust keeps falling meanwhile.
- **D is wrong (design):** Self-reported confidence isn't calibrated, so a 0.8 cut-off filters on a number nobody has checked; explicit criteria fix precision.

Objective: 4.1 Design prompts with explicit criteria to improve precision and reduce false positives. Source: CCAR-F exam guide v1.0, section 6, task statement 4.1 (Tier 1).

</details>

### Drill 21 (task statement 4.2)

A support-triage prompt has detailed routing rules, yet borderline tickets (a billing question that mentions a bug) are routed inconsistently. What is most effective?

- **A.** Add more rules covering each borderline combination seen so far.
- **B.** Add a code rule that sends every ticket matching more than one category to a fixed default queue.
- **C.** Ask Claude to list every category that applies to each ticket, and let the agents receiving them sort it out.
- **D.** Add 2-4 few-shot examples of borderline tickets showing why one route wins.

<details><summary>Answer and why</summary>

**Answer: D.** Few-shot examples with reasoning show how to handle ambiguous cases and generalize to new patterns.

- **A is wrong (prompt):** Rules cover only listed cases; the next new combination breaks again.
- **B is wrong (design):** A real code rule, but it hides the problem: borderline tickets pile up in one queue and are still not routed correctly.
- **C is wrong (design):** This pushes the routing decision onto people downstream; the inconsistent judgment is never fixed.

Objective: 4.2 Apply few-shot prompting to improve output consistency and quality. Source: CCAR-F exam guide v1.0, section 6, task statement 4.2 (Tier 1).

</details>

### Drill 22 (task statement 4.3)

You extract fields from shipping manifests. 'Hazard class' is missing from about a third of them, and the output contains invented hazard classes. The schema marks the field required. What do you change?

- **A.** Make the field nullable, and add an "unclear" enum value for ambiguous entries.
- **B.** Add "never guess the hazard class; leave it out if you can't find it" to the extraction prompt.
- **C.** Keep the field required, and restrict it to an enum of the official list of hazard classes.
- **D.** Retry each manifest extraction until a valid hazard class comes back from the model.

<details><summary>Answer and why</summary>

**Answer: A.** Required fields push the model to fabricate; nullable fields and an "unclear" value let it report absence honestly.

- **B is wrong (prompt):** The schema still demands a value, so the prompt and the schema conflict.
- **C is wrong (design):** A stricter schema makes the invented values look valid; it does nothing about absence.
- **D is wrong (design):** Retries can't produce information that isn't in the document.

Objective: 4.3 Enforce structured output using tool use and JSON schemas. Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1).

</details>

### Drill 23 (task statement 4.4)

Extracted purchase orders sometimes have line items that don't add up to the stated total. Tool use already guarantees valid JSON. What is the best design?

- **A.** Add "make sure the line items always sum to the stated total" to the extraction prompt, with a worked example of the arithmetic.
- **B.** Extract calculated_total and stated_total; compare in code; on mismatch, retry with the document, output and error.
- **C.** Tighten the JSON schema so that any purchase order whose line items don't add up to its total fails schema validation.
- **D.** Have a second Claude instance re-extract every purchase order independently, and keep whichever of the two totals it prefers.

<details><summary>Answer and why</summary>

**Answer: B.** Semantic validation in code plus retry with error feedback is the guide's pattern; schemas only stop syntax errors.

- **A is wrong (prompt):** A request doesn't detect or fix the error when it happens.
- **C is wrong (design):** JSON schemas can't express arithmetic consistency; this is a semantic error.
- **D is wrong (design):** Another extraction is not a check; nothing compares the numbers.

Objective: 4.4 Implement validation, retry, and feedback loops for extraction quality. Source: CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1).

</details>

### Drill 24 (task statement 4.5)

A compliance team needs results within 36 hours of each document arriving. Batch processing can take up to 24 hours, and documents arrive around the clock. How do you meet the deadline at batch prices, with margin?

- **A.** Submit one batch at midnight; batches usually finish in a few hours.
- **B.** Use the synchronous API for every document, to be safe.
- **C.** Submit batches no more than 8 hours apart, since 8 + 24 = 32.
- **D.** Submit batches no more than 12 hours apart, since 12 + 24 = 36.

<details><summary>Answer and why</summary>

**Answer: C.** Worst case is 8h waiting plus 24h processing, 32h, leaving 4 hours of margin inside 36h.

- **A is wrong (design):** A document arriving just after midnight waits about 24h, then up to 24h of processing: 48h. "Usually" isn't a guarantee.
- **B is wrong (design):** Not at batch prices: it meets the deadline but gives up the batch saving when a schedule can do both.
- **D is wrong (design):** This hits 36h exactly in the worst case, with no margin for any delay in submission or retries.

Objective: 4.5 Design efficient batch processing strategies. Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1).

</details>

### Drill 25 (task statement 4.6)

Claude generates a data-migration script and is then asked, in the same conversation, to review it. The review rarely finds anything, but production runs reveal bugs. What is the best change?

- **A.** Turn on extended thinking for the review step so the model reflects more deeply.
- **B.** Add "be highly critical of your own work" to the review instruction.
- **C.** Run the review twice in the same conversation and merge the findings.
- **D.** Review with a separate Claude instance that lacks the generator's reasoning.

<details><summary>Answer and why</summary>

**Answer: D.** An independent review instance without prior reasoning context catches more subtle issues.

- **A is wrong (setting):** The guide: independent instances beat extended thinking for catching subtle issues.
- **B is wrong (prompt):** Self-review instructions don't remove the retained reasoning that makes self-review weak.
- **C is wrong (design):** Both passes share the generator's reasoning, so both inherit its blind spots.

Objective: 4.6 Design multi-instance and multi-pass review architectures. Source: CCAR-F exam guide v1.0, section 6, task statement 4.6 (Tier 1).

</details>

### Drill 39 (task statement 4.3, 4.3S6 + 4.4 · multiple response)

A healthcare-claims extractor uses tool use with a strict JSON schema, so output is always valid JSON. But service dates arrive as '03/04/26', 'March 4' and '2026-03-04', amounts sometimes carry currency symbols, and the payment system rejects them. You need fewer rejects without adding human review. Which changes help most? Select 2.

- **A.** Add format normalization rules to the prompt, such as YYYY-MM-DD dates and plain-decimal amounts.
- **B.** Switch tool_choice to auto so that Claude can explain any unusual date or amount formats to the payment team in plain text.
- **C.** Validate each result with a Pydantic model and, on failure, retry with the specific validation errors appended.
- **D.** Make every date and amount field optional so the schema never rejects a claim on formatting grounds.

<details><summary>Answer and why</summary>

**Answer: A and C.** The guide's skill: format normalization rules in the prompt alongside strict schemas handle inconsistent source formatting. Retry-with-error-feedback works for format errors, because the information is present in the source.

- **B is wrong (setting):** Explaining odd formats in plain text doesn't make them acceptable to the payment system, and `auto` lets Claude skip the tool, so the reply may not be structured at all.
- **D is wrong (design):** Optional fields are for information that may be absent. These values are present but badly formatted; nulls would hide them.

Objective: 4.3 Enforce structured output using tool use and JSON schemas. Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1); CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1); platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use and platform.claude.com/docs/en/build-with-claude/structured-outputs, tool use and structured outputs (Tier 1).

</details>

### Drill 40 (task statement 4.5, 4.5K3)

A legal-discovery team wants to move 40,000 nightly document reviews to the Message Batches API. Each review now calls lookup_privilege_log, a client-side tool your code executes, mid-conversation. The team must match every result to its document and resubmit only failures. What is the right design?

- **A.** Submit each review as one batch request and let Claude call lookup_privilege_log inside it, as it does today.
- **B.** Run the tool calls inside the batch, and set a longer expiry so they have time to finish.
- **C.** Set custom_id to a random UUID per request, and keep a local lookup file mapping each UUID to its document.
- **D.** Fetch privilege-log data first and put it in each request, set custom_id to the document ID, and resubmit only errored or expired results.

<details><summary>Answer and why</summary>

**Answer: D.** A batch request can't pause while your code runs a client-side tool and returns its result, so the data is supplied upfront. custom_id correlates results, and results come back as succeeded, errored, canceled or expired.

- **A is wrong (design):** Your code can't return a client-side tool's result inside a batch request. (Server tools, which Anthropic runs, are a different case.)
- **B is wrong (setting):** Time isn't the problem: no expiry setting lets your code return a client-side tool result mid-request.
- **C is wrong (design):** It works only while the lookup file survives. Using the document ID as custom_id makes resubmitting failures direct, with nothing extra to lose.

Objective: 4.5 Design efficient batch processing strategies. Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1); platform.claude.com/docs/en/build-with-claude/batch-processing, Message Batches API (Tier 1). Result types and limits can change: see [Message Batches API signals](deep-practice/conditions-and-errors.md#4-message-batches-api).

</details>

## Domain 5: Context Management & Reliability (15%, 9 drills)

### Drill 26 (task statement 5.1)

In 40-turn support chats your agent summarizes earlier turns to save tokens. Customers complain it forgets their refund amount and the delivery date it promised. What is the best fix?

- **A.** Summarize less often, every 20 turns instead of every 5, so fewer exact details get condensed.
- **B.** Ask the summarizer to "preserve important details".
- **C.** Keep a case-facts block (amounts, dates, order IDs) in every prompt, outside the summary.
- **D.** Move to a model with a larger context window, and stop summarizing the conversation at all.

<details><summary>Answer and why</summary>

**Answer: C.** Transactional facts in a separate persistent block, outside the summarized history, is the guide's skill.

- **A is wrong (design):** Fewer summaries still condense exact values, just later.
- **B is wrong (prompt):** Progressive summarization condenses exact values; a vague instruction doesn't make it lossless.
- **D is wrong (design):** This defers the problem and raises cost, and long inputs suffer the lost-in-the-middle effect.

Objective: 5.1 Manage conversation context to preserve critical information across long interactions. Source: CCAR-F exam guide v1.0, section 6, task statement 5.1 (Tier 1).

</details>

### Drill 27 (task statement 5.2)

A customer writes: "I don't want the bot. Put me through to a person." The issue is a simple address change the agent could finish in one step. What should the agent do?

- **A.** Make the quick address change first, then offer the transfer.
- **B.** Transfer to a human at once, with a structured handoff summary.
- **C.** Check a sentiment score and transfer only if it is strongly negative.
- **D.** Acknowledge the request and explain that it can fix this faster than a person.

<details><summary>Answer and why</summary>

**Answer: B.** The guide: honour explicit requests for human agents immediately. A handoff summary helps the person who picks it up.

- **A is wrong (design):** Explicit requests for a human are honoured immediately, without first attempting the work.
- **C is wrong (design):** Sentiment is an unreliable proxy, and the customer has already said what they want.
- **D is wrong (prompt):** Offering to resolve fits frustration without an explicit request, not a clear demand for a person.

Objective: 5.2 Design effective escalation and ambiguity resolution patterns. Source: CCAR-F exam guide v1.0, section 6, task statement 5.2 (Tier 1).

</details>

### Drill 28 (task statement 5.3)

A research coordinator merges three subagents' findings. One subagent couldn't reach a regulatory database even after local retries. It reported that clearly, but the final report presents all topics with the same certainty. What should change?

- **A.** Drop the topics that relied on the unreachable database, so everything the report shows is well supported.
- **B.** Have that subagent keep retrying with backoff until the database responds.
- **C.** Have the synthesis mark each section as well-supported or as having gaps from unavailable sources.
- **D.** Tell the synthesis agent to sound less certain throughout.

<details><summary>Answer and why</summary>

**Answer: C.** Coverage annotations show which findings are well-supported and which topics have gaps, so readers aren't misled.

- **A is wrong (design):** It hides the gap instead of reporting it: readers lose those topics and never learn that coverage was incomplete. Gaps from unavailable sources should be annotated, not silently removed.
- **B is wrong (design):** Local retries already ran; retrying without limit stalls the report and the outage may last.
- **D is wrong (prompt):** Uniform hedging hides which parts are actually weak.

Objective: 5.3 Implement error propagation strategies across multi-agent systems. Source: CCAR-F exam guide v1.0, section 6, task statement 5.3 (Tier 1).

</details>

### Drill 29 (task statement 5.4)

Three hours into exploring a large monorepo, Claude Code starts describing "typical service patterns" instead of the specific classes it found earlier. What is the best response?

- **A.** Keep a scratchpad file of key findings, send new searches to subagents, and use /compact.
- **B.** Fork the session with fork_session and keep exploring in the fork, so the original stays safe.
- **C.** Remind Claude in each prompt to cite the specific classes found earlier.
- **D.** Restart from scratch in a fresh session and re-explore the whole repo without any notes.

<details><summary>Answer and why</summary>

**Answer: A.** Scratchpad files, subagent delegation and /compact are the guide's counters to context degradation.

- **B is wrong (design):** A fork copies the degraded context; it doesn't clean it.
- **C is wrong (prompt):** The details may already have dropped out of usable context; reminders can't restore them.
- **D is wrong (design):** Starting over without notes throws away the findings.

Objective: 5.4 Manage context effectively in large codebase exploration. Source: CCAR-F exam guide v1.0, section 6, task statement 5.4 (Tier 1).

</details>

### Drill 30 (task statement 5.5)

Invoice extraction is 96% accurate overall, and the team wants to remove human review. A breakdown shows handwritten invoices are only 70% accurate. What is the best plan?

- **A.** Remove human review for all invoices, since 96% is high, and spot-check customer complaints as they arrive.
- **B.** Check accuracy per document type and field, keep review where a segment falls short, and stratified-sample the rest.
- **C.** Have the model self-report a confidence score per invoice and auto-approve anything above 90% without review.
- **D.** Have a second Claude instance re-check handwritten invoices, and drop human review for everything.

<details><summary>Answer and why</summary>

**Answer: B.** Segment-level validation before automating, and stratified sampling of high-confidence output, are the guide's skills.

- **A is wrong (design):** Aggregate metrics can mask poor segments, which is exactly the case here.
- **C is wrong (design):** Uncalibrated self-reported confidence is unreliable; thresholds need a labeled validation set.
- **D is wrong (design):** Re-checking is unmeasured and removes the humans before anyone knows its error rate.

Objective: 5.5 Design human review workflows and confidence calibration. Source: CCAR-F exam guide v1.0, section 6, task statement 5.5 (Tier 1).

</details>

### Drill 41 (task statement 5.5, 5.5 + 4.6S3)

A manufacturing-quality reviewer flags defects in inspection reports. It produces about 300 flags a day, but two engineers can check only 50. You have 2,000 past reports labeled with confirmed defects. Missed critical defects are costly, and false alarms waste the engineers' time. How should you route flags?

- **A.** Have it report confidence per finding, calibrate thresholds on the labeled set, and route low-confidence or critical flags to the engineers.
- **B.** Route only the flags the model tags as critical to the two engineers, at any confidence level, and auto-accept every other flag without any review.
- **C.** Tell the model to flag only the defects it is really sure about.
- **D.** Set temperature to 0 so that the model produces fewer, steadier flags that the two engineers can realistically get through in a normal working day.

<details><summary>Answer and why</summary>

**Answer: A.** The guide: verification passes with self-reported confidence enable calibrated routing, and thresholds are calibrated on a labeled validation set.

- **B is wrong (design):** Low-confidence non-critical flags go unchecked, and confident critical flags still use up the limited review time.
- **C is wrong (prompt):** Uncalibrated 'be sure' instructions cut flags unpredictably, including critical ones.
- **D is wrong (setting):** Determinism doesn't make flags more accurate or prioritize review capacity.

Objective: 5.5 Design human review workflows and confidence calibration. Source: CCAR-F exam guide v1.0, section 6, task statements 5.5 and 4.6 (Tier 1).

</details>

### Drill 43 (task statement 5.1, 5.1S2)

An insurer's support agent handles long chats in which one policyholder raises several claims. Amounts must stay exact to the cent, but older turns are summarized to keep token cost down. By turn 30 the agent mixes up which claim has which amount and status. What is the best fix?

- **A.** Stop summarizing and send the entire raw transcript on every turn, however large it grows over time.
- **B.** Ask the summarizer, in its prompt, to take extra care to keep every claim amount, claim status and claim ID accurate in each summary.
- **C.** Move the summarizer to a larger model with a longer context window so fewer details get dropped.
- **D.** Keep a structured claims list (claim ID, exact amount, current status) in its own context layer outside the summary, and send it with every prompt.

<details><summary>Answer and why</summary>

**Answer: D.** The guide: persist structured issue data in a separate context layer for multi-issue sessions, outside summarized history.

- **A is wrong (design):** It ignores the token constraint, and long inputs bring their own lost-in-the-middle risk.
- **B is wrong (prompt):** Progressive summarization compresses numbers into vague text regardless of the request.
- **C is wrong (design):** A costlier model still summarizes; exact values need to live outside the summary.

Objective: 5.1 Manage conversation context to preserve critical information across long interactions. Source: CCAR-F exam guide v1.0, section 6, task statement 5.1 (Tier 1).

</details>

### Drill 44 (task statement 5.4)

A pharma trial-data coordinator runs six subagents over a ten-hour reconciliation job. When the host crashed at hour seven last week, the restart re-ran everything from scratch. Compute is costly, and the finished subagents' work was still valid. How should you design recovery?

- **A.** Restart the coordinator's session with --resume so it remembers which of the six subagents had already finished their work.
- **B.** Rerun the full ten-hour job from scratch after any crash, because partial state left behind by the crash may be inconsistent.
- **C.** Have each subagent export state to a known location; on resume the coordinator loads a manifest and injects it.
- **D.** Use fork_session from the hour-seven session to branch a copy and carry on the reconciliation from there.

<details><summary>Answer and why</summary>

**Answer: C.** The guide's crash-recovery design: structured state exports per agent, plus a manifest the coordinator loads on resume.

- **A is wrong (design):** Session history isn't a durable record of each subagent's outputs, and its tool results may be stale.
- **B is wrong (design):** This is the costly behaviour the team wants to end, and valid work is thrown away.
- **D is wrong (design):** A fork copies the conversation, not the subagents' saved outputs, and the crashed session may not hold their results.

Objective: 5.4 Manage context effectively in large codebase exploration. Source: CCAR-F exam guide v1.0, section 6, task statement 5.4 (Tier 1).

</details>

### Drill 45 (task statement 5.6, 5.6S2 + 5.6S5 · multiple response)

A public-sector analytics team synthesizes reports on regional unemployment. One subagent cites 6.1% from a 2024 survey, another 4.8% from a 2026 release, and the draft calls this a contradiction and keeps one figure. Officials need to see each figure's source and which findings are settled. What should change? Select 2.

- **A.** Keep the most recent figure in the report and add a footnote that mentions the other one.
- **B.** Require subagents to output claim-source mappings with publication or collection dates, and preserve them through synthesis.
- **C.** Tell the synthesis agent, in its prompt, to always prefer whichever source was published most recently.
- **D.** Separate well-established from contested findings, keeping each source's figure and context.

<details><summary>Answer and why</summary>

**Answer: B and D.** The guide: structured claim-source mappings preserved through synthesis, with dates so temporal differences aren't read as contradictions. The guide: distinguish established from contested findings and preserve source characterizations and methodological context.

- **A is wrong (design):** A footnote still treats a date difference as an error and hides which findings are settled versus contested.
- **C is wrong (prompt):** It silently discards a credible figure instead of annotating it with its source and date.

Objective: 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis. Source: CCAR-F exam guide v1.0, section 6, task statement 5.6 (Tier 1).

</details>

## Drill set checks

- Answer letters: A 12, B 13, C 12, D 12
- Correct answer is the strictly longest option: 10 of 45 (22%)
- Length rank of the correct answer, single-answer drills (1 shortest to 4 longest; tie = shares its length): rank 1 7, rank 2 12, rank 3 11, rank 4 8, rank tie 3
- Length rank of each pick in Select 2 drills: rank 1 1, rank 2 3, rank 3 2, rank 4 2
- Correct answer is the shortest option: 9 of 45 drills
- Strongest-distractor types (drills with at least one): design-change distractor 45, mentions temperature 2, mentions max_tokens 3, prompt-request distractor 36
- Drills per domain: D1 14, D2 6, D3 8, D4 8, D5 9