# CCAR-F Lesson 2 — Tool Design and MCP Integration (18%, about 11 questions)

**Picture the application:** A researcher submits a PDF, but the assistant repeatedly sends it to an operation meant for another kind of content. The expected result is analysis from the appropriate source with an understandable outcome. Tool design and MCP integration name the technical choices that make capabilities discoverable, distinguishable and usable.

**Time:** 2 hours plus [lab 03, the MCP server wired into Claude Code with a guardrail hook](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) · **Practice:** [CCAR-F practice — choose Domain 2](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)
**Scenarios:** 1 Support, 3 Research, 4 Dev productivity · A colleague who passed said MCP questions were
"heavy" on his exam.


<!-- layered-scenario-migration -->
## Learn this domain through connected case studies

Read and predict; no account, code execution or setup is required for these teaching scenes. Each stage names its application and the requirement that fails. Some stages transfer the same decision to a different application; follow the named people and data rather than assuming every stage belongs to one system. The original reference sections remain below for detail. These are original teaching questions, not claimed live exam items. Write your choice before revealing the repair. Diagrams below show AI reasoning and ordinary software checks explicitly in their labels.

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

**Objective connections:** [2.1](objectives/objective-2.1.md), [2.3](objectives/objective-2.3.md).

### Stage 2 — An unavailable service looks like an empty account

The balance tool normally returns current funds. Today the server cannot reach the bank service. It returns an empty list and the assistant says the customer has no accounts. The error was hidden as ordinary data.

**Original exam-style practice — choose ONE.** Which MCP tool-result contract best supports correct error propagation and recovery?

A. Return an empty successful result on every failure.

B. Return an explicit failure category and useful retryability context without exposing secrets; preserve available partial data as partial.

C. Ask the model to infer the failure from response length.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The caller must distinguish “there are no accounts” from “we could not check.” A confuses those meanings; C guesses. Permission denial, invalid input, insufficient stock and transient outage need different responses.

**Follow the changed path:**

```text
business API failure → tool failure category → caller recovery policy
confirmed empty data → successful empty result → ordinary answer
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Inject a timeout, bad input and permission denial. Expect different categories; do not retry permanent invalid input as though waiting would fix it.

</details>

**Changed-constraint decision — choose ONE before revealing:** The service denies access. A: retry with higher model confidence; B: stop that action and use the approved permission/escalation route.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Confidence cannot grant access. Keep access failures separate from temporary outages.

</details>

**Objective connections:** [2.2](objectives/objective-2.2.md).

### Stage 3 — The server is configured, but the capability is absent

A developer connects a document-search MCP server. The connection appears healthy, yet the agent cannot search documents. The tool was not included in that agent’s available capability set.

**Original exam-style practice — choose ONE.** Which diagnosis correctly distinguishes MCP connectivity, tool availability and authorization?

A. Treat a successful server connection as proof every agent may execute every server tool.

B. Verify server discovery/health, the agent’s exposed tool set, and the service authorization independently.

C. Add credentials to the user-facing prompt so the model can repair access.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** A working connection is a doorway, not proof that this agent has the search tool or permission to use it. A merges three checks; C exposes secrets and does not create a legitimate control.

**Follow the changed path:**

```text
configured server → discovered tool → included in agent scope → authorized request → result
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Compare discovery output with the agent-visible tool list and an authorized synthetic test. Redact credentials from retained logs.

</details>

**Changed-constraint decision — choose ONE before revealing:** No external service is needed; a repository filename pattern is known. A: use local Glob then Read; B: introduce MCP solely because it is available.

<details><summary>Reveal changed-constraint reasoning</summary>

A. Choose the local capability that matches the job. Search content with Grep; locate matching paths with Glob; inspect selected files with Read.

</details>

**Objective connections:** [2.4](objectives/objective-2.4.md), [2.5](objectives/objective-2.5.md).

<!-- /layered-scenario-migration -->

## Connect plain reasoning to technical choices

Start with the business constraint, then learn the documentation term and the option it rules out. These worked application bridges show both levels: [AS-01-action-service](architecture-studio/AS-01-action-service.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-03-grounded-assistant](architecture-studio/AS-03-grounded-assistant.md#connect-the-simple-explanation-to-technical-design-choices). Read [artifact types and study mode](architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course) before interpreting examples as build instructions. Reading needs no API setup; runnable activities retain their own prerequisites.


## 2.0 The big idea

Claude picks a tool by reading its name and description, so clear, non-overlapping descriptions
matter more than anything you add to the prompt. Give each agent a few tools that fit its job, and
make failures say what went wrong and whether a retry could help. MCP is how you plug those tools
into Claude Code and agents, with the right scope for who should share them.

## 2.1 Tool descriptions are how the model chooses

- A **description is the main thing** the model uses to pick a tool. Thin descriptions mean
  unreliable choices between similar tools.
- Include **input formats, example queries, edge cases and boundaries**: when to use this tool and
  when to use its neighbor instead.
- Overlapping tools (`analyze_content` vs `analyze_document`) get misrouted. **Rename them and
  sharpen the descriptions**, for example `extract_web_results` with a web-specific description.
- **Split a generic tool** into purpose-specific ones: `extract_data_points`,
  `summarize_content`, `verify_claim_against_source`.
- Check the **system prompt for keyword-sensitive wording** that overrides good descriptions.

## 2.2 Structured errors

- The MCP **`isError`** flag tells the agent a tool call failed.
- On the Messages API the `tool_result` field is `is_error`; in MCP it is `isError`. Same idea, two
  layers.
- Error types: **transient** (timeout, service unavailable), **validation** (bad input),
  **business** (policy), **permission**.
- Return `errorCategory`, **`isRetryable`** and a readable description. For business-rule
  violations, set `retriable: false` and include a customer-friendly explanation.
- Only **`isError`** is an MCP field. `errorCategory` and `isRetryable`/`retriable` are fields
  **you** design into your own error payload; the guide spells the retry flag both ways, so don't
  read anything into the spelling.
- A uniform "Operation failed" stops the agent recovering well.
- **An access failure is not a valid empty result.** A timeout needs a retry decision. "No matches"
  is a successful query.
- Subagents **recover locally** from transient errors and pass up to the coordinator only what they
  can't fix, along with partial results and what they tried.

## 2.3 How many tools, and which ones

- **Smallest sufficient role-relevant tool set.** The saved guide contrasts 4–5 relevant tools with 18 indiscriminate tools; that is an example, not a quota. Scope by the work, relevant cross-role needs and discovery costs.
- Irrelevant capabilities increase the risk of mistaken tool selection; legitimate narrow cross-role needs can still be appropriate. For example, a synthesis worker should not start unrelated broad web searches merely because a search tool is available.
- Give **scoped** access, plus narrow cross-role tools for frequent needs (for example `verify_fact`
  for synthesis). Route complex cases through the coordinator.
- Replace generic tools with constrained ones: `fetch_url` becomes `load_document`, which checks
  URLs.
- **`tool_choice`:** the request setting that says whether Claude may answer in text or must call a tool. Each row is one value; read across for what Claude does and when to pick it.

| Value | Behavior | Use |
| --- | --- | --- |
| `"auto"` | Model may reply in text | Normal chat |
| `"any"` | Must call *some* tool | Guarantee structured output when the document type is unknown |
| `{"type":"tool","name":"X"}` | Must call **X** | Force `extract_metadata` to run first, then handle the rest in later turns |

These are the three options the exam tests (exam guide, task 2.3). Today the API also has a fourth,
`{"type": "none"}`, which turns tools off; see
[exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).

## 2.4 MCP servers in Claude Code and agents

An MCP server's scope is who gets it: the whole team or only you. Each row is one scope; read across for the file it lives in and who it is for.

| Scope | File | For |
| --- | --- | --- |
| **Project** | `.mcp.json` (committed) | Shared team tooling. Use **`${GITHUB_TOKEN}`** expansion so secrets aren't committed. |
| **User** | `~/.claude.json` | Personal or experimental servers |
| **Local** (the default) | `~/.claude.json`, under the project's path | Just you, in just this project. It loads only in that project. |

- Tools from **all** configured servers are discovered when the connection starts and are all
  available at once. Exam wording (task 2.4): "That tools from all configured MCP servers are
  discovered at connection time and available simultaneously to the agent". Today Claude Code's
  tool search is on by default: only tool names and server instructions load at the start, and
  full definitions load when Claude needs them; see
  [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).
  On supported current models/platforms, the default is tool search. To turn it off, set `ENABLE_TOOL_SEARCH=false` (every tool loads upfront). On Google Cloud's
  Agent Platform, models older than the 4.5 generation also load every tool upfront. The "10% of
  the context window" figure you may see in course videos belongs to the **opt-in** `auto`
  threshold mode, not the default
  ([MCP docs](https://code.claude.com/docs/en/mcp), checked 2026-10-21, Tier 1).
- **Transport and discovery:** common connections use local stdio or remote HTTP; host support
  can differ. Protocol tool discovery and calls use `tools/list` and `tools/call`; SDK helper
  names can differ. ([MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).)
- **The three server primitives differ by who controls them** ([MCP server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server),
  checked 2026-10-21):

| Primitive | Controlled by | Example use |
| --- | --- | --- |
| **Tool** | The model (Claude decides when to call it) | Create a ticket in the tracker |
| **Resource** | The app (your code decides when to fetch it) | Inject a document's text when the user @-mentions it |
| **Prompt** | The user (a click, menu pick or slash command) | A ready-made "review this PR" workflow |

- **MCP resources** expose *content catalogs* (issue summaries, doc trees, database schemas) so the
  agent doesn't need exploratory calls. A **direct** resource has a fixed URI; a **templated**
  one has parameters in the URI, such as a document ID ([resource contracts](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)).
- **Choose the boundary:** tools expose capabilities, skills package reusable instructions/work,
  and MCP standardizes access to tools and context from your own **or** external services.
  Primitive control categories are interaction patterns, not permission grants. Apply authorization
  and least privilege separately. ([MCP primitives](https://modelcontextprotocol.io/specification/2025-06-18/server).)
- If the agent prefers Grep over a more capable MCP tool, **improve the MCP tool's description**.
- Use a **community server** for standard integrations such as Jira. Build custom servers only for
  team-specific workflows.

## Server tools vs client tools (who runs the loop)

| Kind | Execution and continuation responsibility |
| --- | --- |
| **Server tool** | Anthropic executes the handler; your application still checks results, errors and stop reasons. |
| **Client tool** | Your application or chosen host/SDK executes the handler and supplies correlated `tool_result` messages. |

A raw Messages API client implements dispatch/continuation; a suitable runner may manage it.
Server tools can return `pause_turn`, requiring continuation, and mixed server/client calls can
wait for client results. Tool selection alone does not prove execution or business completion.
Check support for the selected model, platform and feature combination.

Sources: [tool overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools),
checked 2026-10-21.

## 2.5 Built-in tools

| Tool | For |
| --- | --- |
| **Grep** | Searching **content**: function callers, error messages, imports |
| **Glob** | Matching **file paths**, such as `**/*.test.tsx` |
| Read / Write | Whole-file operations |
| **Edit** | A targeted change anchored on **unique** text. If the text isn't unique, fall back to **Read, then Write**. |
| Bash | Commands |

Build understanding **step by step**: Grep for entry points, then Read to follow imports. Don't read
everything up front. For wrapper modules, list the exported names first, then Grep for each one.

## Worked example

The research agent keeps calling `analyze_content` for PDFs, which are meant for
`analyze_document`. **Answer:** rename and re-describe the tools so they don't overlap, adding
input formats and when to use each. Adding "prefer analyze_document for PDFs" to the prompt, or a
routing classifier, doesn't fix the root cause.

## Traps

- "Give every agent every tool, just in case."
- "Return an empty list when the search times out." That's silent error suppression.
- "Put the API token directly in `.mcp.json`." Use `${ENV}` expansion.
- Mixing up Grep (content) and Glob (paths).
- **Watch out:** some videos say "Bash is always wrong." The guide doesn't say that. The guide picks
  Grep, Glob, Read and Edit for file work; Bash is for running commands (exam guide task 2.5,
  Tier 1).
- **Watch out:** some videos get three details wrong. The user file is `~/.claude.json`, not
  "cloud.json". The guide gives only "18 instead of 4-5"; bands such as "6–10 is acceptable" aren't
  in it. And the guide spells the flags `isRetryable` and `retriable`, never snake_case
  "is_retriable" (exam guide tasks 2.2–2.4, Tier 1).

## Try it, lab 03: the MCP server and guardrail hook lab (2 hours)

Write a small MCP server with 2 tools and structured `isError` errors. Register it in a project
`.mcp.json` with `${TOKEN}`, and call it from Claude Code.

Done when a forced error returns `isError` with its category and Claude Code shows it.

## Done when

- [ ] You can write a tool description with inputs, examples, edge cases and "use X instead when…"
- [ ] You can list the 4 error categories and the fields that go with them
- [ ] You can place the right `tool_choice` value in any scenario
- [ ] You scored 80% or more on [CCAR-F practice — choose Domain 2](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)

**Go deeper:**

- **Deep practice:** [Deep practice 2](deep-practice/02-tool-design-and-mcp-integration.md), which takes every section of this lesson further (the `tool_choice` half of 2.3 is in [deep practice 4](deep-practice/04-prompt-engineering-and-structured-output.md#23-tool-choice-and-tool-order-the-rest-of-23-is-in-deep-practice-2)).
- **Official course:** *Introduction to MCP* from the [CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) (Anthropic, Tier 1, checked 2026-10-02).
- **Flashcards and drills:** the Domain 2 section of the [flashcards](FLASHCARDS.md) and the 6 Domain 2 drills (9–13, 36) in [HARD-DRILLS.md](HARD-DRILLS.md).
- **Charts:** decision charts [7 Wrong tool picked](deep-practice/decision-charts.md#7-claude-keeps-picking-the-wrong-tool-what-do-i-fix-first), [8a Where MCP config lives](deep-practice/decision-charts.md#8a-where-does-an-mcp-servers-config-live) and [11 What a failed tool sends back](deep-practice/decision-charts.md#11-a-tool-or-subagent-failed-what-should-it-send-back); sequence diagrams [4 MCP tool errors](deep-practice/sequence-diagrams.md#4-mcp-how-does-a-tool-error-get-back-to-claude) and [Tree A, which built-in tool](deep-practice/sequence-diagrams.md#tree-a-which-built-in-tool-for-this-file-job).

**Next:** [Deep practice 2](deep-practice/02-tool-design-and-mcp-integration.md), then [Lesson 5](L05-context-management-and-reliability.md).

## Sources

- Official exam guide v1.0, task statements 2.1–2.5 (Tier 1).
- Claude API [define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  (`tool_choice` `none`; `is_error` on `tool_result`) and the
  [MCP tools spec](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  (`isError`), checked 2026-10-07 (Tier 1).
- Claude Code docs: [MCP](https://code.claude.com/docs/en/mcp) for the local, project and user
  scopes, and [MCP tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search)
  (deferred tool definitions, the default), checked 2026-10-07 (Tier 1).
- A colleague's debrief (tier F): emphasis only.

## Objective modules

For deeper learning and a separate practice/completion check for each objective:

- [Objective 2.1](objectives/objective-2.1.md)
- [Objective 2.2](objectives/objective-2.2.md)
- [Objective 2.3](objectives/objective-2.3.md)
- [Objective 2.4](objectives/objective-2.4.md)
- [Objective 2.5](objectives/objective-2.5.md)

## Decisions in this domain

| Objective | Decision variant and exact repair |
| --- | --- |
| 2.1 | [FV-08 — Make capabilities distinguishable](objectives/objective-2.1.md#variant-fv-08) |
| 2.2 | [FV-09 — Route the actual error category](objectives/objective-2.2.md#variant-fv-09) |
| 2.3 | [FV-10 — Scope tools to the assigned role](objectives/objective-2.3.md#variant-fv-10) |
| 2.4 | [FV-11 — Separate connection from inclusion](objectives/objective-2.4.md#variant-fv-11) |
| 2.5 | [FV-12 — Search before making a scoped edit](objectives/objective-2.5.md#variant-fv-12) |

**Interpret local practice targets:** any 80% target above is an optional project study heuristic, not a validated mastery threshold or conversion to the official scaled score. Use fresh decisions, explanations and delayed transfer alongside remaining objective gaps.