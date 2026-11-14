# Deep practice 2: tool design and MCP integration

**Picture the application:** A document researcher has several search and analysis functions, but similar names send requests to the wrong source. Start with the document or question received and the evidence needed back. The sections below connect that practical routing problem to tool descriptions, scopes, errors and MCP connections.

This page covers Domain 2 of CCAR-F, tool design and MCP integration, one task statement at a time. It goes
deeper than [Lesson 2](../L02-tool-design-and-mcp-integration.md): each section gives the core idea, how it works under the hood,
the look-alike wrong answers, a worked example and a one-line exam reflex. Read the lesson first.
Objective lessons for this page: [2.1](../objectives/objective-2.1.md) · [2.2](../objectives/objective-2.2.md) · [2.3](../objectives/objective-2.3.md) · [2.4](../objectives/objective-2.4.md) · [2.5](../objectives/objective-2.5.md).

The `tool_choice` half of 2.3 (`auto` / `any` / forced tool) is in
[04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md).
Error propagation between agents (5.3) builds on 2.2 and is in
[05-context-management-and-reliability.md](05-context-management-and-reliability.md).

---

## 2.1 Tool interfaces and descriptions

Lesson: [L02 section 2.1](../L02-tool-design-and-mcp-integration.md#21-tool-descriptions-are-how-the-model-chooses) · Objective: [2.1](../objectives/objective-2.1.md)

**Exam wording:** `Task Statement 2.1: Design effective tool interfaces with clear descriptions and boundaries`

### Core idea

Claude picks a tool mostly by reading its **description**. If two tools have fuzzy, similar descriptions,
Claude will mix them up. So the fix for "Claude picks the wrong tool" is almost always: **rewrite the names
and descriptions** so each tool's job and limits are obvious.

### How it works under the hood

- **Descriptions are the biggest lever.** Doc wording: "Provide extremely detailed descriptions. This is by
  far the most important factor in tool performance." Say what the tool does, "When it should be used (and
  when it shouldn't)", what each parameter means, and caveats. "Aim for at least 3–4 sentences for each
  tool description" [define-tools].
- **`input_examples`** is an optional field with example inputs for tools with complex or format-sensitive
  parameters; each example must match the `input_schema` [define-tools]. Descriptions come first.
- **Exam knowledge wording:** "Tool descriptions as the primary mechanism LLMs use for tool selection" and
  include "input formats, example queries, edge cases, and boundary explanations" [guide, TS 2.1].
- **Names that separate tools.** Namespace by service and resource, for example `asana_search`,
  `jira_search`, `asana_projects_search`, `asana_users_search` [writing-tools]. Exam example: rename
  `analyze_content` to `extract_web_results` with a web-specific description [Guide].
- **Split generic tools.** Exam example: split `analyze_document` into `extract_data_points`,
  `summarize_content` and `verify_claim_against_source`, each with its own input/output contract [Guide].
- **Build workflow tools, not thin wrappers.** Instead of `list_users`, `list_events` and `create_event`,
  build one `schedule_event` that finds a slot and books it; instead of `read_logs`, build `search_logs`
  that returns only relevant lines [writing-tools].
- **Return readable things.** Resolving "arbitrary alphanumeric UUIDs to more semantically meaningful and
  interpretable language" improves precision and cuts hallucination [writing-tools]. Offer a
  `response_format` enum so the agent can ask for `"concise"` or `"detailed"` output [writing-tools].
- **System prompt can override a good description.** Exam skill: review system prompts "for
  keyword-sensitive instructions that might override well-written tool descriptions" [Guide]. Example: "Always
  analyze content carefully" nudges Claude toward a tool named `analyze_content`.

**Template for a good description (practice, not doc):**

```text
search_orders: Finds a customer's orders by order number, email, or date range.
Use it when the customer mentions a specific order or a purchase date.
Do NOT use it to look up refunds; use get_refund_status for that.
Input: order_number (string like "ORD-12345") OR email + optional date_from/date_to (ISO 8601).
Returns up to 20 orders, newest first, with status names (not codes). Returns an empty list, not an error, if nothing matches.
```

### Look-alikes

1. **"Add few-shot examples of correct tool picks to the system prompt."** It helps, but the root cause is
   overlapping descriptions. Fix descriptions first. The docs call detailed descriptions "by far the most important factor in
   tool performance" [define-tools]. Fixing them before adding few-shot examples is (practice, not doc).
2. **"Add a routing classifier in front of the agent."** Over-built for a description problem.
3. **"Merge the two similar tools into one with a `mode` parameter."** Can be valid, but when the exam
   offers "rename and rewrite descriptions to remove overlap", that is the targeted fix.
4. **"Use a bigger model."** Doesn't remove the ambiguity.

### Worked example (Scenario: multi-agent research system)

The research agent has `analyze_content` ("Analyzes content") and `analyze_document` ("Analyzes a
document"). It keeps sending web pages to `analyze_document`. Fix: rename `analyze_content` to
`extract_web_results`, describe it as "for HTML pages returned by web_search; not for PDFs", and say in
`analyze_document` "for uploaded PDF or DOCX files; not for web pages". Then check the system prompt for a
line like "analyze every document" that pulls Claude the wrong way.

### Exam reflex

**Wrong tool picked means fix names and descriptions first (3 to 4+ sentences, when and when not).**

---

## 2.2 Structured error responses for MCP tools

Lesson: [L02 section 2.2](../L02-tool-design-and-mcp-integration.md#22-structured-errors) · Objective: [2.2](../objectives/objective-2.2.md)

**Exam wording:** `Task Statement 2.2: Implement structured error responses for MCP tools`

### Core idea

When a tool fails, the agent needs to know **what kind** of failure it was, so it can choose: retry, fix
the input, tell the customer, or escalate. "Operation failed" tells it nothing. A structured error tells it
what to do next.

### How it works under the hood

**Two kinds of MCP error, from the spec** [mcp-spec-tools]:

| Kind | How it's sent | Examples | Can the model fix it? |
|---|---|---|---|
| **Tool execution error** | A normal tool result with `isError: true` | API failures, input validation errors ("date in wrong format, value out of range"), business logic errors | Yes. Spec wording: "actionable feedback that language models can use to self-correct and retry" |
| **Protocol error** | A JSON-RPC error object | Unknown tool, malformed request | Less likely. Spec example: `"code": -32602`, `"message": "Unknown tool: invalid_tool_name"` |

Spec wording: "Clients **SHOULD** provide tool execution errors to language models to enable
self-correction." Protocol errors "MAY" be provided [mcp-spec-tools].

**What changed since:** since the 2025-11-25 spec (unchanged in 2026-07-28; checked 2026-10-07), **input validation errors** are tool execution errors
(`isError: true`). Older spec versions and many older servers sent bad input as a JSON-RPC protocol error
(`-32602`, invalid params). The exam's answer: put failures the agent can react to in a result with
`isError: true` [guide, TS 2.2]. If a trace shows `-32602`, read it as "the request itself was rejected at
protocol level" (unknown tool, or invalid params on older servers).

**On the exam: pick the tool result with `isError: true` and structured details for any failure the agent should react to.**

**On the Claude API side** the same idea is `"is_error": true` on a `tool_result` block [handle-tool-calls].
Note the spelling: MCP is `isError` (camelCase), the Messages API is `is_error` (snake_case).

**The four error categories** (exam knowledge wording) [Guide]: "transient errors (timeouts, service
unavailability), validation errors (invalid input), business errors (policy violations), and permission
errors".

**Structured metadata** (exam skill wording): "errorCategory (transient/validation/permission), isRetryable
boolean, and human-readable descriptions" [Guide]. These field names are **exam/practice, not MCP spec**:
the spec defines only `isError` and free content. You put the structure inside the content.

```json
{
  "isError": true,
  "content": [{"type": "text", "text": "{\"errorCategory\": \"business\", \"isRetryable\": false, \"message\": \"Refunds over $500 need manager approval.\", \"customerMessage\": \"I've passed this to a manager who can approve it.\", \"nextStep\": \"escalate_to_human\"}"}]
}
```

**Empty is not an error.** Exam skill: distinguish "access failures (needing retry decisions) and valid
empty results (representing successful queries with no matches)" [Guide]. A search that worked and found
nothing returns `isError: false` with an empty list. A search that timed out returns `isError: true`,
`errorCategory: "transient"`, `isRetryable: true`.

**Recover locally first.** A subagent retries transient errors itself and passes up only what it can't fix,
"along with partial results and what was attempted" [Guide] (more in deep practice 5, 5.3).

**Make errors actionable.** Anthropic: "prompt-engineer your error responses to clearly communicate specific
and actionable improvements, rather than opaque error codes or tracebacks" [writing-tools].

### Look-alikes

1. **Throwing an exception that crashes the MCP server or the loop.** The agent learns nothing and the
   workflow dies.
2. **Returning a protocol error for a business rule ("refund too big").** The model may never see it.
   Business errors are tool results with `isError: true` and `isRetryable: false`.
3. **Returning `[]` with `isError: false` when the database timed out.** Hides the failure; the agent will
   say "no orders found" to the customer. Silent suppression is an anti-pattern (also 5.3).
4. **Generic `"Operation failed"` for everything.** Guide: "prevent the agent from making appropriate
   recovery decisions".

### Worked example (Scenario: customer support resolution agent)

`lookup_order` sometimes times out. Today it returns `{"isError": true, "content": "failed"}`, so the agent
retries 5 times on a permission error too, and gives up on a timeout that would have cleared. Fix: return
`errorCategory` plus `isRetryable`. Timeout: `transient`, `true` (retry with backoff). Expired token:
`permission`, `false` (escalate). Wrong order-number format: `validation`, `false`, message "Order numbers look
like ORD-12345" (the agent asks the customer).

### Exam reflex

**Failures go back as `isError: true` with category, retryable and next step; empty results are success, not errors.**

---

## 2.3 Tool distribution across agents

Lesson: [L02 section 2.3](../L02-tool-design-and-mcp-integration.md#23-how-many-tools-and-which-ones) · Objective: [2.3](../objectives/objective-2.3.md)

**Exam wording:** `Task Statement 2.3: Distribute tools appropriately across agents and configure tool choice`

`tool_choice` (`"auto"`, `"any"`, `{"type": "tool", "name": "..."}`) and tool order: see
[04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md). This section is the distribution half.

### Core idea

Give each agent **only** the tools its job needs. More tools means more chances to pick the wrong one, and
an agent with a tool outside its job will use it badly.

### How it works under the hood

- Exam knowledge wording: too many tools ("18 instead of 4-5") "degrades tool selection reliability"
  [guide, TS 2.3]. Doc fact: "Claude's ability to pick the right tool degrades once you exceed 30–50
  available tools"; tool search loads a focused set on demand [tool-search]. (Exam number: 4 to 5 per
  agent. Doc number: degradation past 30 to 50. Both point the same way.)
- **Scoping in the SDK:** each `AgentDefinition` has `tools` (allowed list) and `disallowedTools`; if
  `tools` is omitted the subagent inherits all subagent tools [sdk-subagents]. So set `tools` explicitly.
- **Constrained replacements.** Exam example: replace generic `fetch_url` with `load_document` "that
  validates document URLs" [Guide].
- **Scoped cross-role tools.** Exam example: give the synthesis agent a small `verify_fact` tool for a
  frequent need, and route complex cases back through the coordinator [Guide].

### Look-alikes

1. **"Give every agent every tool so none gets stuck."** The exact anti-pattern.
2. **"The synthesis agent keeps running web searches: tell it in the prompt not to."** Remove the tool;
   that's a guarantee, the prompt isn't.
3. **"Give the synthesis agent full web search for fact checks."** Too broad; the guide's answer is a
   narrow `verify_fact` tool.

### Worked example (Scenario: multi-agent research system)

The synthesis agent has 18 tools including `web_search` and `fetch_url`. It wanders off searching instead of
writing. Fix: give it `tools=["verify_fact"]` plus what it needs to write; leave search to the search agent;
send big fact gaps back to the coordinator.

### Exam reflex

**Each agent gets the 4 to 5 tools its role needs; narrow cross-role tools for frequent needs; the rest go through the coordinator.**

---

## 2.4 MCP servers in Claude Code and agent workflows

Lesson: [L02 section 2.4](../L02-tool-design-and-mcp-integration.md#24-mcp-servers-in-claude-code-and-agents) · Objective: [2.4](../objectives/objective-2.4.md)

**Exam wording:** `Task Statement 2.4: Integrate MCP servers into Claude Code and agent workflows`

### Core idea

Where you put an MCP server's config decides **who gets it**. Team tools go in the project file that's in
git. Personal or experimental tools stay in your own file. Secrets never go in git: the config says
`${GITHUB_TOKEN}` and each person's environment supplies the value.

### How it works under the hood

**Three scopes** (doc table) [cc-mcp]:

| Scope | Loads in | Shared with team | Stored in |
|---|---|---|---|
| Local (the default) | Current project only | No | `~/.claude.json` (under that project's path) |
| Project | Current project only | Yes, via version control | `.mcp.json` in project root |
| User | All your projects | No | `~/.claude.json` |

- Add with `claude mcp add ... --scope local|project|user`; no flag means local [cc-mcp].
- **Precedence** when one name is defined twice: "1. Local scope 2. Project scope 3. User scope", then
  plugin servers, then claude.ai connectors. "The entire server entry from that source is used; fields are
  not merged across scopes" [cc-mcp].
- **Approval:** Claude Code "prompts for approval in interactive sessions before using project-scoped
  servers from `.mcp.json` files". In `claude -p` and Agent SDK runs it can't prompt, so it loads them
  without asking [cc-mcp].
- **Exam version of scopes:** the guide contrasts "project-level (.mcp.json) for shared team tooling vs
  user-level (~/.claude.json) for personal/experimental servers" [guide, TS 2.4]. Local scope is also in
  `~/.claude.json` but per project. Don't let "both live in `~/.claude.json`" confuse you.
- Watch the name clash: MCP "local scope" is in `~/.claude.json`, while general local **settings** are
  `.claude/settings.local.json` [cc-mcp].

**Environment variable expansion** [cc-mcp]: `${VAR}` expands to the variable's value; `${VAR:-default}`
uses `default` if `VAR` isn't set.

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "${GITHUB_MCP_URL:-https://mcp.example.com/github}",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

**When the variable is missing** (this corrects a common belief): if `${VAR}` "names a variable that isn't
set and has no `:-default`, Claude Code warns in `claude mcp list` output and in `/mcp`, naming the
variable, and still loads the server with the `${VAR}` text unexpanded" [cc-mcp]. So the server usually
**does** start, then fails to authenticate. The symptom is "Needs authentication" or failed calls, plus a
warning naming the variable.

**What changed since: credential variables that read as empty.** Today, in a **remote** server's `url`
and `headers`, Claude Code "reads credential variables from your environment as empty rather than
expanding them", and gives **no warning** [cc-mcp]. This stops a project's `.mcp.json` from sending your
own credentials to some server. The doc names, "such as": Claude Code's own (`ANTHROPIC_API_KEY`,
`ANTHROPIC_AUTH_TOKEN`), your cloud provider's (`AWS_BEARER_TOKEN_BEDROCK`), and others like
`HTTPS_PROXY` and `NPM_TOKEN`. The list isn't complete. Doc wording: "A name outside this set, such as
`API_KEY`, expands as written." So for a team server, use a variable name of your own, like
`GITHUB_MCP_TOKEN`. Whether `GITHUB_TOKEN` is on the hidden list is not confirmed.

**On the exam: pick `.mcp.json` with a `${VAR}` reference for shared secrets.**

**Checking servers** [cc-mcp]:

- `claude mcp list` shows status per server, such as `✔ Connected`, `! Needs authentication`,
  `✘ Failed to connect`, or ``⏸ Pending approval (run `claude` to approve)`` for an unapproved `.mcp.json`
  server.
- `claude mcp get <name>` shows one server and an `Issue:` line on failure.
- `/mcp` inside a session shows servers, tool counts, and lets you reconnect, authenticate or disable.

**All tools at once.** Exam knowledge: tools from all configured servers "are discovered at connection
time and available simultaneously" [Guide].

**Output limit:** Claude Code warns when MCP tool output exceeds 10,000 tokens and "limits output to
25,000 tokens by default"; change it with `MAX_MCP_OUTPUT_TOKENS` [cc-mcp]. So big tools should paginate
and filter [writing-tools].

**Resources vs tools.** Resources expose "content catalogs (e.g., issue summaries, documentation
hierarchies, database schemas) to reduce exploratory tool calls" [Guide]. A tool **does** something; a
resource **shows** what's there.

**The Grep problem.** Exam skill: enhance MCP tool descriptions "to explain capabilities and outputs in
detail, preventing the agent from preferring built-in tools (like Grep) over more capable MCP tools"
[Guide]. If Claude keeps using Grep instead of your code-search MCP tool, the fix is **the MCP tool's
description**, not removing Grep and not a prompt rule.

**Build or reuse?** Exam skill: choose "existing community MCP servers over custom implementations for
standard integrations (e.g., Jira), reserving custom servers for team-specific workflows" [Guide].

### Look-alikes

1. **"Put the shared Jira server in `~/.claude.json` and send teammates the file."** Personal file, not
   shared via git. Team tools go in `.mcp.json`.
2. **"Paste the token into `.mcp.json`; the repo is private."** Still a secret in git. Use `${JIRA_TOKEN}`.
3. **"Teammate's tool is missing, so the `.mcp.json` must be broken."** First check `claude mcp list`:
   it may be `Pending approval`, missing an env var (warning names it), or shadowed by a same-name local
   server (local wins).
4. **"Claude prefers Grep, so deny Grep."** Treats the symptom. Improve the MCP tool's description.
5. **"Build a custom Jira MCP server for control."** Reuse the community one unless the workflow is unique.

### Worked example (Scenario: developer productivity with Claude)

The team adds a shared GitHub MCP server. Put it in `.mcp.json` with
`"Authorization": "Bearer ${GITHUB_TOKEN}"`, commit it, and each developer sets `GITHUB_TOKEN` in their
shell. Priya's tool calls fail. `claude mcp list` usually shows a warning naming `GITHUB_TOKEN` (unless that name is one of the credential variables that read as empty, which give no warning): she never set it.
Raj sees a different, older endpoint: he has a same-name server in local scope, which beats project scope.
He removes it with `claude mcp remove github --scope local`.

### Exam reflex

**Shared: `.mcp.json` plus `${VAR}`; personal: `~/.claude.json`; local beats project beats user; agent ignores your MCP tool means fix its description.**

---

## 2.5 Built-in tools: Read, Write, Edit, Bash, Grep, Glob

Lesson: [L02 section 2.5](../L02-tool-design-and-mcp-integration.md#25-built-in-tools) · Objective: [2.5](../objectives/objective-2.5.md)

**Exam wording:** `Task Statement 2.5: Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively`

### Core idea

- **Glob** finds files by **name**. (`**/*.test.tsx`)
- **Grep** finds text **inside** files. (Who calls `processRefund`?)
- **Read** opens a file. **Edit** changes one exact piece. **Write** writes a whole file.

Build understanding step by step: find, then narrow, then read only what matters.

### How it works under the hood

- **Grep output modes** [cc-tools]: `files_with_matches` ("file paths only, no line content. This is the
  default"), `content` (matching lines with file and line number), `count` (matches per file). Scope with
  the `glob` parameter (`**/*.tsx`) or `type` (`py`). It uses ripgrep regex and respects `.gitignore`.
- **Read** [cc-tools]: returns contents with line numbers. When a whole-file read is too big it returns a
  `PARTIAL view` notice and tells Claude to read more with `offset` and `limit`.
- **Edit** [cc-tools]: exact string replacement of `old_string` with `new_string`. Checks: the file was
  read first, the text matches exactly, and it is **unique**. If it appears more than once, give a longer
  `old_string` with more context, or set `replace_all: true`.
  - The "read first" check is relaxed today. Doc wording: "Claude Opus 4.6, Claude Haiku 4.5, and older
    models always require the read. Newer models can edit an unread file when reading it wouldn't need a
    permission prompt" [cc-tools]. For the exam, assume Read comes before Edit.
- **Exam fallback:** "When Edit fails due to non-unique text matches, using Read + Write as a fallback"
  [guide, TS 2.5].
  - **What changed since:** today's docs also offer a longer `old_string` with more context, or
    `replace_all: true` [cc-tools].

    **On the exam: pick Read + Write when Edit can't find unique text.**

**The search order (practice pattern, built from the doc tool behaviours):**

1. **Glob** to find candidate files by name.
2. **Grep** in `files_with_matches` mode first, to see **how many** files match without flooding context.
3. **Grep** in `content` mode, narrowed by `glob`/`type` or folder, on the files that matter.
4. **Read** with `offset`/`limit` for big files, then follow imports.

Exam skill wording: "starting with Grep to find entry points, then using Read to follow imports and trace
flows, rather than reading all files upfront" [Guide]. And for wrapper modules: "first identifying all
exported names, then searching for each name across the codebase" [Guide].

**What changed since:** today's tools reference says Glob and Grep are "Absent by default on macOS, Linux,
and WSL"; Claude searches with `find` and `grep` through Bash instead (embedded `bfs` and `ugrep`), and the
tools come back if you name them in `--tools`/`--allowedTools` or remove Bash [cc-tools]. The exam still
treats Glob and Grep as the dedicated tools.

**On the exam: pick Glob for file names and Grep for file contents.**

### Look-alikes

1. **Grep for `*.test.tsx`.** Grep searches contents. File-name patterns are Glob.
2. **Glob for "all callers of `processRefund`".** Glob can't see inside files. Grep.
3. **"Read every file in `src/` first so Claude has full context."** The named anti-pattern; floods
   context.
4. **"Use Bash `sed` when Edit fails."** The exam's fallback is Read + Write.

### Worked example (Scenario: code generation with Claude Code)

Task: find every place that uses the old `formatCurrency` helper, which is re-exported through
`utils/index.ts` as `fmt` and `money`. Steps: Read `utils/index.ts` to list exported names. Grep
`files_with_matches` for `formatCurrency|fmt\(|money\(`: 41 files. Narrow with `glob: "src/**/*.tsx"`: 12
files. Grep `content` on those 12. Read the two biggest with `offset`/`limit` around the hits. Edit each call;
where the call text repeats in a file, use more context (or the exam's Read + Write fallback).

### Exam reflex

**Names: Glob; contents: Grep (file list first); then Read only the parts you need; Edit not unique means Read + Write.**

---

## Sources (citation keys)

Tier 1 unless marked, checked 2026-10-07:
[define-tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) ·
[tool-search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) ·
[handle-tool-calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) ·
[writing-tools](https://www.anthropic.com/engineering/writing-tools-for-agents) ·
[mcp-spec-tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) ·
[cc-mcp](https://code.claude.com/docs/en/mcp) ·
[cc-tools](https://code.claude.com/docs/en/tools-reference) ·
[sdk-subagents](https://code.claude.com/docs/en/agent-sdk/subagents) ·
[Guide] = the official CCAR-F exam guide v1.0 (July 2026, Anthropic).

## Not confirmed

- Whether `GITHUB_TOKEN` is one of the credential variables that read as empty in a remote server's `url` or `headers` (2.4). The doc's list says "such as" and isn't complete.
- The error fields `errorCategory`, `isRetryable` and `nextStep` (2.2) are exam and practice wording. The MCP spec defines only `isError`.
- The tool-description template (2.1) and the Glob, then Grep file list, then Read order (2.5) are practice patterns built from the doc tool behaviours.
- "Fix tool descriptions before adding few-shot examples" (2.1) is practice, not doc. It fits the doc's "by far the most important factor" [define-tools].

**Next:** [Lesson 5, context management and reliability](../L05-context-management-and-reliability.md), the next lesson in the study order, or back to the [CCAR-F lessons page](../README.md).