# Conditions and errors: the exact signals

**Picture the application:** An order lookup returns a timeout, while another query succeeds with no matching records. Both leave the assistant without an order to display, but they require different explanations and recovery. Use the exact signals below to trace an observed outcome before deciding whether to retry, correct input or escalate.

**How to read each table.** *Signal* is what you see in the code, config or message. *Exact value* is the word-for-word field, code or flag (doc wording, in code format). *What happens next* is what the system does by itself. *Right design response* is what your code or config should do. *Source* is the official page; a link key is at the bottom.

Bracketed tags like `[err]` are sources; the list is at the end.

**Marks.** `(unconfirmed)` = not found on an official page. `(practice, not doc)` = good practice the exam guide tests, but no Anthropic doc states it as a rule.

**Scope boundary.** The saved July 2026 guide defines this study baseline. Its terminology is preserved below; it does not establish a universal answer independent of the question constraints or prove the latest official revision. Current implementation notes are separate and version-sensitive.

---

## Exam answer vs today

This table contrasts saved guide wording with implementation notes. It is not an exhaustive drift audit or an answer key. Read the whole scenario and constraints. Existing guide quotations remain attributed to their task statements. Tool-selection, strict-shape and hook-boundary notes were rechecked 2026-10-17; other rows retain their earlier review status.

| Topic | Saved-guide concept and scope | Guide wording (Tier 1) | Current implementation note (Tier 1) | Source |
|---|---|---|---|---|
| Output must match a JSON schema | Schema-based extraction is the saved guide concept; ordinary and strict tool use are not interchangeable current implementations. | "Tool use (tool_use) with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output, eliminating JSON syntax errors" (TS 4.3) | Supported strict tool inputs use `strict: true`; structured final output uses the documented output format. Ordinary schemas guide inputs without the same enforcement. Shape does not establish source truth, authorization or business validity; handle schema limits and abnormal termination. | [Guide], [strict], [so] |
| Forced `tool_choice` | In the guide capability model, `any` requires some tool and named selection requests the named first tool. Execute and validate its result before dependent actions. | `"any"` "to guarantee the model calls a tool rather than returning conversational text"; a named tool "to ensure a specific tool is called first" (TS 2.3, 4.3) | Support varies by model and thinking setting. Some configurations reject forced choices; others accept them. `auto` permits no-tool replies. Selection is not prerequisite completion or action authorization; enforce those in application state. Check the current compatibility table before deployment. | [Guide], [impl] |
| Prefill to force JSON | Tool use with a JSON schema over prefill. | Not in the guide. The guide calls tool use "the most reliable approach for guaranteed schema-compliant structured output" (TS 4.3), so a prompt-side trick like prefill loses to it. | Claude 4.6 and later reject a prefilled last assistant turn with `400` (prefill = writing the first words of Claude's reply yourself, so it carries on from there). | [Guide], [prompt], [err] |
| Spawning subagents | `Task`. | "The Task tool as the mechanism for spawning subagents" (TS 1.3) | The tool is `Agent` (renamed in Claude Code v2.1.63; `Task` still works as an alias). | [Guide], [cc-subagents] |
| Agent SDK `allowedTools` | `Task` in `allowedTools`. | "allowedTools must include "Task" for a coordinator to invoke subagents" (TS 1.3) | `allowedTools` only pre-approves tools: a listed tool runs without asking for permission. It does not limit which tools exist. `Agent` needs no approval, so it runs even when unlisted. Take spawning away with `disallowedTools`, or leave `Agent` out of a restricted `tools` list (the coordinator's `tools` option, or a subagent definition's `tools`). | [Guide], [sdk-perm], [cc-subagents] |
| Skill `allowed-tools` | `allowed-tools`. | "Configuring allowed-tools in skill frontmatter to restrict tool access during skill execution" (TS 3.2) | `allowed-tools` only pre-approves; it "does not restrict which tools are available". `disallowed-tools` blocks (for example `disallowed-tools: Bash`). | [Guide], [skills] |
| Skill `argument-hint` | `argument-hint`. | "Using argument-hint frontmatter to prompt developers for required parameters" (TS 3.2) | A hint shown during autocomplete, Claude Code only. | [Guide], [skills] |
| Custom slash commands | `.claude/commands/` for shared team commands. | "Project-scoped commands in .claude/commands/ (shared via version control) vs user-scoped commands in ~/.claude/commands/ (personal)" (TS 3.2) | Custom commands are now part of skills, but `.claude/commands/` still works. | [Guide], [skills] |
| Project context in CI | `-p` with `CLAUDE.md`. | `-p`, with "CLAUDE.md as the mechanism for providing project context" (TS 3.6) | Docs say add `--bare` in CI. It skips `CLAUDE.md`, hooks, skills, MCP servers and more, so you pass standards in explicitly. | [Guide], [headless], [cli] |
| PreToolUse decisions | Use a correctly scoped pre-action guard for mandatory restrictions; instructions alone do not enforce them. | "Implementing tool call interception hooks that block policy-violating actions" (TS 1.5). The guide names no decision values; `allow`, `deny` and `ask` are from the hooks doc. | Hook decisions apply only to matching event/tool paths and correct policy inputs. Test bypass paths and failure behavior. PostToolUse runs after the side effect. Decision fields depend on runtime; verify hooks documentation. | [Guide], [hooks] |
| Which memory files loaded | `/memory`. | "Using the /memory command to verify which memory files are loaded" (TS 3.1) | `/memory` lists memory file locations; `/context` lists, under Memory files, the `CLAUDE.md` files loaded at launch. A path-scoped rule or a subfolder `CLAUDE.md` loads later, and the terminal shows a "Loaded …" line when it does. | [Guide], [mem] |
| Path-scoped rules | "When editing matching files". Either way, not every session. | "load only when editing matching files" (TS 3.3) | A path-scoped rule loads when Claude reads, writes or edits a matching file. | [Guide], [mem] |
| Personal MCP server | User-level `~/.claude.json`. | "Configuring personal/experimental MCP servers in user-scoped ~/.claude.json" (TS 2.4) | `claude mcp add` defaults to local scope (also in `~/.claude.json`, this project only); `--scope user` covers all your projects. | [Guide], [cc-mcp] |
| MCP tool loading | All tools available at once. | "That tools from all configured MCP servers are discovered at connection time and available simultaneously to the agent" (TS 2.4) | Tool search is on by default: only tool names and server instructions load at session start, and definitions load on demand (fallbacks in the note under the table). | [Guide], [cc-mcp] |
| Edit with repeated text | Read + Write. | "When Edit fails due to non-unique text matches, using Read + Write as a fallback" (TS 2.5) | Edit can also take `replace_all: true` when every match should change. | [Guide], [cc-tools] |

**Note on MCP tool loading:** Claude Code falls back to loading every tool definition up front with `ENABLE_TOOL_SEARCH=false` or a non-first-party `ANTHROPIC_BASE_URL`, and `alwaysLoad: true` exempts one server [cc-mcp].

---

## 1. Agent loop signals (`stop_reason`)

For model-turn control, read `stop_reason` rather than parsing prose. The application also owns validation, execution, resource limits and business completion evidence.

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Claude wants a tool | `stop_reason: "tool_use"` | Reply holds one or more `tool_use` blocks, each with `id`, `name`, `input`. Nothing runs until you act. | Validate each client-tool request, execute authorized calls or return errors, then send linked `tool_result` blocks. Continue with the results; a request itself is not execution. | [stop], [calls] |
| Claude is finished | `stop_reason: "end_turn"` | Normal model-turn finish, not proof of business settlement. | Exit normal turn control; report actual receipts and unresolved work. | [stop] |
| Reply cut off by your limit | `stop_reason: "max_tokens"` | Reply stops mid-sentence, or mid-tool-call. | Raise `max_tokens` or continue. If the last block is an incomplete `tool_use`, **do not run it**; retry with a higher `max_tokens`. | [stop] |
| Your stop string fired | `stop_reason: "stop_sequence"` | The `stop_sequence` field says which one. | Read it; treat as a planned stop. | [stop] |
| Server-tool loop hit its limit | `stop_reason: "pause_turn"` | A server tool (for example web search) hit the iteration limit (default 10). | Send the assistant content back as-is to let it continue. Only happens with server tools, never while a client tool waits on you. | [stop] |
| Claude declined | `stop_reason: "refusal"` | `stop_details` names the policy category. | Exam answer: handle it (log, tell the user, route); never blind-retry the same request. Today's docs add: read `stop_details`, retry on a fallback model. **On the exam: pick "handle or route it", not "retry the same request".** | [stop] |
| Context window full | `stop_reason: "model_context_window_exceeded"` | Reply filled the model's whole context window. | Treat as truncated. Trim or summarise history. | [stop] |
| Empty reply after tool results | `end_turn` with 2 to 3 tokens, no content | Claude thinks the turn is done. | Common cause: you put text right after the `tool_result` blocks, or re-sent its finished reply unchanged. Send results alone. | [stop] |
| Loop ends when reply says "done" | text check like `"done" in reply` | Fragile: wording changes, loop stops early or never. | Branch on `stop_reason` only ("Always check stop_reason" is a doc heading). Add a max-iterations counter and a time or cost cap with a safe hand-off to a person. A cap is an explicit control safeguard also discussed in Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) article; reaching it means halt/handoff, not normal completion or business settlement. | [stop] |
| API "forgets" earlier turns | each call uses supplied context | Necessary prior evidence must be supplied or deliberately summarized. | Maintain coherent relevant history and matching tool-call/result pairs; for long work use validated summaries, persistent exact facts and retrieval. Do not replay every raw message forever. | [calls], [context-engineering] |

---

## 2. Tool use rules

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| A `tool_use` with no answer | error text `tool_use ids were found without tool_result blocks immediately after` | `400` | Every `tool_use` `id` needs a matching `tool_result` with that `tool_use_id`, in the very next user message. | [calls] |
| Text before results | user `content` starts with a `text` block, then `tool_result` | `400` | `tool_result` blocks go **first**. Any text goes after all of them. | [calls] |
| Anything between call and result | a message inserted between the assistant `tool_use` and the user `tool_result` | Rejected | Results must immediately follow the call. Nothing in between. | [calls] |
| Parallel calls | several `tool_use` blocks in one reply | All wait for you. | Return **all** results in **one** user message. | [parallel] |
| Tool failed (network, bad data) | `tool_result` with `"is_error": true` | Claude reads the message and adapts or tells the user. | Return `is_error: true` with an instructive message ("Rate limit exceeded. Retry after 60 seconds."), not `"failed"`. Don't crash the loop or throw. | [calls] |
| Claude sent a bad call (missing param) | `is_error: true`, `"Error: Missing required 'location' parameter"` | Claude retries 2 to 3 times with corrections, then apologises. | During development, improve the tool `description`. To remove the whole class of failure, use `strict: true`. | [calls] |
| Schema check fails in your code | your validator's error | Nothing automatic. | Retry once or twice with the **exact** validator error in the feedback, then stop and route to a person. Bounded retries are `(practice, not doc)`. | [calls] |
| Retry for data that isn't in the source | field truly absent | Retries can't invent real data; they push the model to make it up. | Make the field nullable or optional; route `null` to review. `(practice, not doc)` | — |
| `tool_choice` | `{"type": "auto"}` | Claude decides to call a tool or not. Default when `tools` are given. | Normal agent loops. | [impl] |
| `tool_choice` | `{"type": "any"}` | On supported configurations, requires **some** provided tool. | Use when any provided tool is acceptable and support is verified (guide TS 4.3). It does not enforce a particular first operation. | [impl] |
| `tool_choice` | `{"type": "tool", "name": "..."}` | On supported configurations, requests **that** tool. | For the guide first-tool scenario, select metadata extraction, execute and validate its result, then allow enrichment in later steps. Enforce authorization and prerequisite state separately (TS 2.3, 4.3). | [impl] |
| `tool_choice` | `{"type": "none"}` | No tools. Default when no `tools` are given. | Pure text answer. | [impl] |
| Forced choice and text | `any` or `tool` | The API prefills the reply, so Claude writes **no** text before the `tool_use`, even if asked. | Want an explanation too? Use `auto` plus "Use the X tool" in the user message. | [impl] |
| Forced choice with manual thinking | `thinking: {type: "enabled"}` plus `any`/`tool` | Error. | Use `auto` or `none`. | [impl] |
| *Beyond the exam:* change `tool_choice` mid-conversation | different `tool_choice` | Invalidates cached message blocks. | Keep it stable if you rely on caching. | [impl] |
| Parallel off switch | `disable_parallel_tool_use: true` | One tool call at a time. | Goes **inside** the `tool_choice` object; it is not a top-level parameter. | [parallel] |
| Strict schema limits | `strict: true` or supported structured-output format | Constrains supported schema shape; not source truth or arbitrary business rules. | Check the current supported schema subset and handle errors/refusals/truncation before consuming output. Validate ranges and totals against the source in application code. | [so], [strict] |

> **Tool choice versus ordering.** Saved-guide `any`/named selection describes a supported selection mechanism. Current compatibility is configuration-specific [impl]. Selecting `extract_metadata` does not mean it executed successfully. Return its linked result, validate the trusted extraction state, and gate dependent enrichment. Ordinary `auto` plus a prompt may guide selection, but does not guarantee it; structured final output addresses response shape, not whether a tool ran.


> **What changed since (prefill).** Exam logic (the guide doesn't mention prefill; this follows from TS 4.3): prefill (starting the assistant reply with `{`) is a weak way to force JSON. Today: Claude 4.6 and later models (and Mythos Preview) reject a prefilled last assistant turn with `400` `invalid_request_error`, message "This model does not support assistant message prefill. The conversation must end with a user message." [prompt], [err] **On the exam: pick tool use with a JSON schema over prefill; treat prefill as the weakest option.**

**Separate output shape, tool selection and business validation.** Strict tool inputs constrain tool arguments; structured final outputs constrain the answer format. Ordinary tool use and prompt-only JSON do not provide the same shape enforcement. A strict schema does not require a tool call, prove factual correctness or authorize execution. The saved guide's schema-based extraction objective remains relevant, but current code must select a supported mechanism and handle its failure states. [Guide], [so], [strict], [impl]


---

## 3. API errors

**Must know (the retry rule only):** **429, 500, 529 = wait and retry. 400, 401, 403, 404, 413 = a retry gets the same error; fix the request or the setup.**

Everything else in this section is background. The exam guide's "Out-of-Scope Topics" list includes "Claude API authentication, billing, or account management", "Rate limiting, quotas, or API pricing calculations" and "Streaming API implementation or server-sent events" (exam wording) [Guide]. So rows marked *background, not tested* or *Extra, beyond the guide* help you read a trace, but no question should hinge on them.

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Bad request (must know) | `400` `invalid_request_error` | Same request fails every time. | Fix the request (format, ordering of `tool_result`, schema, unsupported forced `tool_choice` for the selected model/settings, prefill on 4.6+). No retry. | [err] |
| Bad API key (*background, not tested*) | `401` `authentication_error` | Fails every time. | Stop and alert a person. Key comes from an env var or secret store, never code. | [err] |
| No permission (*background, not tested*) | `403` `permission_error` | Key can't use that resource. | Fix access or workspace settings. No retry. | [err] |
| Not found (must know) | `404` `not_found_error` | Wrong path or ID (for example a model name). | Fix the endpoint or ID. | [err] |
| Too big (must know) | `413` `request_too_large` | Over the byte limit: Messages API 32 MB, Batch API 256 MB. | Shrink: split files, fewer pages, use the Files API. No retry. | [err] |
| Rate limit (must know: retry rule only) | `429` `rate_limit_error` with a `retry-after` header | Temporary. | Retry with exponential backoff; honour `retry-after`. | [err] |
| Server error (must know) | `500` `api_error` | Temporary. | Retry with exponential backoff; if it persists, contact support with the `request_id`. | [err] |
| Overloaded (must know) | `529` `overloaded_error` | High traffic across all users. | Retry with backoff; consider a fallback model. | [err] |
| SDK behaviour (must know) | default `max_retries` = 2 | The official SDK retries connection errors, 429 and 5xx **twice** with backoff, honouring `retry-after`. | Don't stack your own big retry loop on top without thinking. Set `max_retries` to change it. | [err] |
| Usage-tier spend cap (*Extra, beyond the guide*) | `429` with **no** `retry-after` | Keeps failing until access resumes. | Don't loop on retries. Alert a person. | [err] |
| Your own spend limit (*Extra, beyond the guide*) | `400` `invalid_request_error` | An org or workspace spend limit **you set** was reached (a Claude Code workspace limit can give `429` instead). | Raise the limit; retrying won't help. | [err] |
| Timeout (*Extra, beyond the guide*) | `504` `timeout_error` | Long request timed out. | Use streaming for long requests. | [err] |
| Too big, before the API (*Extra, beyond the guide*) | `413` from Cloudflare | On the direct API, Cloudflare (the network layer in front of the API) rejects an oversized request before it reaches the API servers. | Same fix: shrink the request. | [err] |
| Error after a 200 (*Extra, beyond the guide*) | error event mid-stream | With streaming, the reply arrives over SSE (server-sent events: one open connection that sends the answer in pieces). An error can arrive after the `200`, so normal HTTP error handling doesn't catch it. | Handle the stream's error events. | [err] |

> **What changed since (spend limits; Extra, beyond the guide).** Today's errors page splits spend limits: a usage-tier monthly spend cap gives `429` with no `retry-after` and keeps failing; an org or workspace spend limit you set gives `400`. **On the exam: pick "fix or escalate, don't retry" for any limit that won't clear by itself; pick "retry with backoff" only for a normal `429`, `500` or `529`.** [err]

Every error body has `type: "error"`, an `error` object with `type` and `message`, and a `request_id`. Catch the SDK's typed exceptions; don't string-match messages. [err]

---

## 4. Message Batches API

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Batch created | `processing_status: "in_progress"` | Processing runs async. Most batches finish in under 1 hour. | Poll until `processing_status: "ended"`. | [batch] |
| Processing window | 24 hours | Requests not done by 24 hours **expire**. | Only use Batch where waiting up to 24 hours is fine. Plan submit times so the deadline holds even if the batch takes the full 24 hours. | [batch] |
| Result OK | `succeeded` | Holds the message. | Use it. | [batch] |
| Result error | `errored` | No message created (invalid request or server error). **Not billed.** | Fix invalid ones; resubmit only the failed `custom_id`s. | [batch] |
| Result canceled | `canceled` | You canceled before it was sent. Not billed. | Resubmit if still needed. | [batch] |
| Result expired | `expired` | Hit the 24-hour limit before it was sent. Not billed. | Resubmit only those `custom_id`s in a new batch. | [batch] |
| Results out of order | results file (`.jsonl`) | Results can come back in any order. | Match by `custom_id`, never by position. | [batch] |
| `custom_id` rules | `^[a-zA-Z0-9_-]{1,64}$` | Must be unique per request in the batch. | Use a meaningful ID (for example the file name). | [batch] |
| Size limits | 100,000 requests or 256 MB | Whichever comes first. | Split bigger jobs. | [batch] |
| Validation timing | `params` checked async | Bad requests show up only when the whole batch has ended. | Test one request on the Messages API first. | [batch] |
| Price and retention | 50% of standard price; results kept 29 days | Download after 29 days fails. | Save results promptly. Batch stacks with prompt caching (cache hits are best-effort). | [batch] |
| Tool loop inside a batch | a result ends with a client `tool_use` | The request is finished; nothing runs **your** (client) tool mid-request. **Server** tools (web search, web fetch, code execution, MCP connectors) do run server-side inside the request. | Batch can carry multi-turn **history**, but a client tool round trip needs a **new** request, so agent loops with your own tools use the normal API. Exam wording (TS 4.5): "does not support multi-turn tool calling within a single request (cannot execute tools mid-request and return results)". | [Guide], [batch] |

---

## 5. MCP errors

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Tool ran but failed (API down, business rule) | result with `"isError": true` | Client SHOULD pass it to the model so it can self-correct. | Return a clear message: what went wrong, whether a retry helps, what to try next. | [mcp-latest] |
| Unknown tool / malformed request | JSON-RPC `error`, for example `"code": -32602`, `"Unknown tool: ..."` | Protocol error; the model is less likely to recover. | Fix the client or server; not something the model can fix. | [mcp-latest] |
| Bad input (wrong date format, out of range) | result with `"isError": true` | Model sees it and retries with fixed arguments. | Say exactly what was wrong ("must be in the future; today is ..."). | [mcp-latest] |
| Error body that says only "failed" | `"text": "failed"` | Model can't tell retry from give-up. | Add error type, a retryable flag and a suggested next step. Field names like `retryable` are `(practice, not doc)`; "write instructive error messages" is doc. | [calls] |
| Expired or unknown handle | tool execution error | Model can recover by creating a new one. | Say it expired; state lifetimes in the creation tool's description. | [mcp-latest] |
| Server won't connect | `claude mcp list` shows `✘ Failed to connect` | Its tools are missing. | Check the command, URL and the `Issue:` line (`claude mcp get <name>`). | [cc-mcp] |
| Project server not approved | `⏸ Pending approval (run claude to approve)` | `.mcp.json` server not loaded. | Run `claude` interactively and approve. A cloned repo can't approve its own servers. | [cc-mcp] |
| Needs login | `! Needs authentication` | Tools unavailable until OAuth. | Authenticate from `/mcp`. | [cc-mcp] |
| Missing env var | `${VAR}` with no `:-default` and not set | Claude Code **warns** in `claude mcp list` and `/mcp`, and still loads the server with the literal `${VAR}` text, so auth calls fail. | Set the variable or use `${VAR:-default}`. Never paste secrets into `.mcp.json`. | [cc-mcp] |
| Big tool output | over 10,000 tokens | Warning; output capped at 25,000 tokens by default. | Page, filter, return fewer fields. `MAX_MCP_OUTPUT_TOKENS` raises the cap. | [cc-mcp] |
| Slow tool | `MCP_TOOL_TIMEOUT` env var, or per-server `"timeout"` (ms) in `.mcp.json` | Call is cut off at the timeout. | Set a per-server timeout for slow tools. | [cc-mcp] |

> **Spec history (MCP bad input). No exam-vs-docs conflict here.** The older spec, 2025-06-18, listed "Invalid arguments" as a **protocol error** (JSON-RPC). From spec 2025-11-25 on, input validation errors are **tool execution errors** with `isError: true`, so the model can fix and retry. That change came before the July 2026 guide, and the guide tests "the MCP `isError` flag pattern for communicating tool failures". The exam and the current spec agree. [mcp-2025], [mcp-2025-11], [mcp-latest] **On the exam: pick "return it in the result with `isError: true` and a clear message" for any failure the model can act on; protocol errors are for unknown tools and malformed requests.**

---

## 6. Claude Code hooks: exit codes

A hook script reads JSON on stdin. Its exit code, or the JSON it prints, decides what happens.

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Success | exit `0` | Action goes ahead. stdout is parsed as JSON if it looks like JSON. | Use exit `0` plus JSON when you need fine control. | [hooks] |
| Block | exit `2` | Blocks (on events that can block). stderr, or the JSON `reason`, is the message. | **The** way to enforce a policy by exit code. | [hooks] |
| Unix-style failure | exit `1` (or any code other than 0 and 2) | **Non-blocking** error: the action proceeds; transcript shows `Failed with non-blocking status code:`. | A "block" script that exits `1` does **not** block. Change it to `exit 2`. | [hooks] |
| Script missing or not executable | shell exits `127` | Same non-blocking notice; the gate is silently off. | Check for the notice on first run. | [hooks] |
| Exit 2 with bad JSON | exit `2` + invalid JSON | Still blocks; stderr is the reason. | Pick one style per hook: exit codes, or exit 0 plus JSON. | [hooks] |
| Stop everything | JSON `"continue": false`, `"stopReason": "..."` | Claude stops processing entirely. Beats event-specific decisions. | Use for "build failed, stop". | [hooks] |
| Worktree events | any non-zero from `WorktreeCreate` | Creation fails. | Exception to the exit-2 rule. | [hooks] |

---

## 7. Claude Code hooks: JSON fields and what each event can block

**JSON decision fields.**

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Block via JSON (most events) | top-level `"decision": "block"`, `"reason": "..."` | Used by `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `PreCompact`, `ConfigChange`. `"block"` is the only value; omit it to allow. | Feedback that Claude must act on. | [hooks] |
| PreToolUse decision | `hookSpecificOutput.permissionDecision`: `"allow"`, `"deny"`, `"ask"` (today also `"defer"`, only in -p and Agent SDK runs) plus `permissionDecisionReason` | `allow` skips the prompt; `deny` stops the call (reason goes to Claude); `ask` prompts the user. | Business rules (refund limit, protected files) go here. What changed since: `"defer"` is newer and works only in -p and Agent SDK runs (it pauses the call for the calling app). **On the exam: pick from `allow`, `deny`, `ask`.** | [hooks] |
| Several PreToolUse hooks disagree | precedence `deny` > `defer` > `ask` > `allow` (`defer` only in -p and Agent SDK runs) | Strictest wins. | — | [hooks] |
| Rewrite the input | `hookSpecificOutput.updatedInput` | Replaces the **whole** input object. | Normalise data before the tool runs (include unchanged fields). | [hooks] |
| PostToolUse block | `"decision": "block"` + `reason` | Adds the reason next to the tool result. Claude still sees the original output. | Quality hook: run lint or tests after `Edit`, feed failures back. | [hooks] |
| Replace a tool's output | `hookSpecificOutput.updatedToolOutput` | Claude sees your value instead. | Redact or normalise results. | [hooks] |
| Add facts | `hookSpecificOutput.additionalContext` | Added as a system reminder (cap 10,000 characters). | Dynamic state (branch, flags). Static rules belong in `CLAUDE.md`. | [hooks] |
| Hook allow vs a deny rule | hook returns `"allow"`, settings has a matching `deny` | **Still denied.** Hooks don't bypass deny or ask rules. | Need a hard block? A deny rule or an exit-2 hook. | [perm] |
| Exit-2 hook vs an allow rule | `exit 2` + matching `allow` | **Blocked.** The hook runs before rules are checked. | "Allow all Bash, block a few commands" = allow `Bash` + PreToolUse hook. | [perm] |

**What each event can and cannot block** (exit `2`).

| Event | Can block? | What exit `2` does | Source |
|---|---|---|---|
| `PreToolUse` | Yes | Blocks the tool call | [hooks] |
| `PostToolUse` | **No** | Shows stderr to Claude; the tool **already ran** | [hooks] |
| `PostToolUseFailure` | No | Shows stderr to Claude; the tool already failed | [hooks] |
| `UserPromptSubmit` | Yes | Blocks the prompt; it never reaches Claude | [hooks] |
| `Stop` | Yes | Prevents Claude from stopping; conversation continues | [hooks] |
| `SubagentStop` | Yes | Prevents the subagent from stopping | [hooks] |
| `SessionStart` | **No** | stderr shown to the user only; Claude doesn't see it | [hooks] |
| `SessionEnd` | No | stderr to the user only | [hooks] |
| `Notification` | No | Ignored | [hooks] |
| `PermissionRequest` | No (by exit code) | Ignored; deny through the `decision` object instead | [hooks] |
| `PreCompact` | Yes | Blocks compaction | [hooks] |
| `PostToolBatch` | Yes | Stops the loop before the next model call | [hooks] |

The trap: "use a PostToolUse hook to **prevent** a bad write." It can't; the write already happened. Prevent with `PreToolUse`. Use `PostToolUse` to check and report.

---

## 8. Hook `matcher`

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Match all | `"*"`, `""`, or no `matcher` | Fires on every occurrence. | — | [hooks] |
| Exact name(s) | `"Bash"`, `"Edit\|Write"`, `"Edit, Write"` | Only letters, digits, `_`, `-`, spaces, `,` and the pipe sign → exact strings (pipe or comma separates names). | Quality hook after edits: `PostToolUse` + `"Edit\|Write"`. | [hooks] |
| Regex | any other character, for example `"mcp__memory__.*"` | JavaScript regex, **unanchored**: `Edit.*` also matches `NotebookEdit`. | Use `^Edit$` for a whole-name match. | [hooks] |
| MCP tool names | `mcp__<server>__<tool>` | Match one server with `mcp__memory__.*`. | — | [hooks] |
| What the matcher tests | tool events → `tool_name`; `SessionStart` → `startup`, `resume`, `clear`, `compact`, `fork` | Different field per event. | — | [hooks] |
| Matcher on an event without matchers | `matcher` on `UserPromptSubmit` or `Stop` | **Silently ignored**; hook always fires. | Filter inside the script. | [hooks] |
| Finer filter | handler `"if": "Bash(git *)"` | Permission-rule syntax on name plus arguments. | — | [hooks] |

---

## 9. Settings precedence and permission rules

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Same key in several places | order, highest first: **managed** > **command line** > **local** (`.claude/settings.local.json`) > **project** (`.claude/settings.json`) > **user** (`~/.claude/settings.json`) | Highest level that sets the key wins. | Company policy that nobody can override → managed settings. | [set] |
| `--settings '{...}'` | command line | Beats local, project, user; never managed. | One-off session change. | [set] |
| Allow vs deny on the same call | rules checked **deny → ask → allow**; first match wins | A broad `deny` like `Bash(aws *)` beats a narrow `allow` like `Bash(aws s3 ls)`. Specificity doesn't change the order. | An allow can't carve a hole in a deny. Narrow the deny instead. | [perm] |
| Ask vs allow | matching `ask` + matching `allow` | Prompts. | — | [perm] |
| "Yes, don't ask again" still prompts | local `allow` vs project or managed `ask` | Still prompts; a local allow doesn't outrank an ask. | Change the shared rule, if that's right for the team. | [set] |
| Permissions merge | `permissions.allow` across scopes | Merged, unless managed sets `allowManagedPermissionRulesOnly`. | — | [set] |
| Untrusted folder | project `allow` rules | Wait until the user trusts the folder. `deny` and `ask` apply right away. | — | [set] |
| Bypass mode from repo | `permissions.defaultMode: "bypassPermissions"` in project or local | Doesn't take effect. | Set in user or managed, or pass `--permission-mode`. | [set] |
| Env var vs setting | `ANTHROPIC_MODEL` vs `model` key | Decided per pair, not by level (`ANTHROPIC_MODEL` wins over `model`). | — | [set] |

---

## 10. `settings.json` vs `settings.local.json`, and MCP scopes

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Team rules | `.claude/settings.json` | Committed; everyone who clones gets the same permissions, hooks, plugins. CI uses it too. | Team-wide hooks and permissions live here. | [set] |
| Just me, this project | `.claude/settings.local.json` | Applied over the shared file. Claude Code adds it to global git excludes when **it** creates the file; hand-made ones you must gitignore yourself. "Don't ask again" approvals land here. | Personal overrides. Not on the CI machine. | [set] |
| Just me, all projects | `~/.claude/settings.json` | Lowest level. | Personal defaults. | [set] |
| MCP local scope (default) | stored in `~/.claude.json` under the project path | Private, this project only. | Personal servers, secrets you don't commit. Not the same as `settings.local.json`. | [cc-mcp] |
| MCP project scope | `.mcp.json` at project root (`--scope project`) | Shared via git; **approval prompt** before use. | Team servers, with secrets as `${VAR}`. | [cc-mcp] |
| MCP user scope | `~/.claude.json` (`--scope user`) | All your projects, private. | Personal tools you use everywhere. | [cc-mcp] |
| Same server name in two scopes | precedence **local > project > user > plugin > claude.ai connectors** | Whole entry from the winner; fields **not** merged. Warning shown. | Remove the extra definition with `claude mcp remove --scope <scope>`. | [cc-mcp] |
| Check what loaded | `claude mcp list`, `claude mcp get <name>`, `/mcp` | Status per server. | First step when "the tool doesn't show up." | [cc-mcp] |

---

## 11. `CLAUDE.md` load order, `@` imports, `.claude/rules/`

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Where files live | managed policy file (for example `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS) · `~/.claude/CLAUDE.md` (user) · `./CLAUDE.md` or `./.claude/CLAUDE.md` (project) · `./CLAUDE.local.md` (personal, gitignore it) | Loaded broad to specific. | Team standards → project file (committed). Personal → user or `CLAUDE.local.md`. | [mem] |
| Launch | `CLAUDE.md` + `CLAUDE.local.md` in the working dir **and every dir above** | **Concatenated**, not overridden. Order root → working dir, so the closest file is read last. In each dir, `CLAUDE.local.md` comes after `CLAUDE.md`. | — | [mem] |
| Subdirectory file | `src/api/CLAUDE.md` below the working dir | Loads **on demand**, when Claude uses Read, Write or Edit on a file there. | — | [mem] |
| Import | `@path/to/file` | Expanded and loaded **at launch**. Relative to the file that contains it. Max depth **four hops**. | Organises a long file but does **not** cut context cost. | [mem] |
| Mention without importing | `` `@README` `` in backticks | Not imported (code spans are skipped). | — | [mem] |
| External import | path outside the working dir in a project file | One-time approval dialog. | — | [mem] |
| Rules folder | `.claude/rules/*.md` (found recursively) | No `paths` → always loaded. | One topic per file. | [mem] |
| Path-scoped rule | frontmatter `paths:` with globs, for example `"src/api/**/*.ts"`, `"src/**/*.{ts,tsx}"` | Loads only when Claude Reads, Writes or Edits a matching file. | Conventions for one file type, wherever the files live (better than a subdirectory `CLAUDE.md` when files are spread across folders). | [mem] |
| User rules | `~/.claude/rules/` | Every project on your machine. | — | [mem] |
| Skip a file | `claudeMdExcludes` | Skips matching files. Managed `CLAUDE.md` can't be excluded. | Monorepo noise. | [mem] |
| Size | target under 200 lines per file | Longer files cost context and lower adherence. | Move part-of-repo rules into path-scoped rules. | [mem] |
| Advice vs enforcement | a rule in `CLAUDE.md` | Instructional context guides model behavior; it is not an execution boundary. | Mandatory restrictions require a correctly scoped hook, permission setting or action-service guard, tested across equivalent paths and policy failures. No mechanism repairs incorrect trusted inputs by itself. | [hooks], [perm] |

---

## 12. Sessions and headless runs

| Signal | Exact value | What happens next | Right design response | Source |
|---|---|---|---|---|
| Pick up the last chat | `--continue` / `-c` | Loads the most recent conversation in this directory. Skips `-p` and SDK sessions unless you run `claude -p --continue`. | Quick "carry on". | [cli] |
| Pick a specific chat | `--resume` / `-r` `<id or name>` | Loads that session, or opens a picker. | Return to a named investigation. | [cli] |
| Branch off | `--fork-session` (with `--resume` or `--continue`) | New session ID; the original stays as it was. | Try a different approach without spoiling the original. | [cli] |
| Fixed ID | `--session-id <uuid>` | Uses that ID. | Scripts that track sessions. | [cli] |
| Headless | `-p` / `--print` | Runs without the interactive UI. | CI jobs. | [cli] |
| Machine-readable output | `--output-format json` (or `text`, `stream-json`) | Pipeline can parse the result. | CI: `claude -p "<task>" --output-format json`. | [cli] |
| Validated output | `--json-schema '{...}'` (print mode) | JSON checked against your schema at the end. | Structured review findings. | [cli] |
| Turn cap | `--max-turns N` (print mode) | **Exits with an error** at the limit. No limit by default. | Always cap CI runs. | [cli] |
| Cost cap | `--max-budget-usd` (print mode) | Stops at the cap (client-side estimate). | — | [cli] |
| Pre-approved tools | `--allowedTools "Bash(git diff *)" "Read"` | Those run without prompts. To restrict which tools exist, use `--tools`. | Least privilege in CI. | [cli] |
| Mode | `--permission-mode` `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` | Overrides `defaultMode`. | — | [cli] |
| No saved history | `--no-session-persistence` (print mode) | Can't be resumed. | Throwaway CI runs. | [cli] |
| Resumed session: hook context | `PostToolUse` / `UserPromptSubmit` `additionalContext` | **Replayed** from the transcript, not re-run, so timestamps or SHAs go stale. `SessionStart` runs again with `source` `"resume"` or `"fork"`. | Refresh dynamic facts in a `SessionStart` hook. | [hooks] |
| Resumed session: files changed | files edited since last session | Old tool results in history show the **old** content. | Re-read only the changed files; add a short summary of earlier findings instead of replaying everything. `(practice, not doc)` | — |
| Resumed session: system prompt | recorded on the first request | Reused on resume until compaction. | — | [cli] |
| CI review independence | same session wrote and reviews the code | Self-review misses its own mistakes. | Use a separate review session. `(practice, not doc)`; matches exam guide TS 4.6 wording "multi-instance and multi-pass review". | [Guide] |

---

## Practice, not doc (no official page states these as rules)

- Error-body fields like `retryable` or `suggested_action`: `(practice, not doc)`.
- Loop caps, bounded retries, separate review session, re-reading changed files: `(practice, not doc)`.

## Link key

- [err]: https://platform.claude.com/docs/en/api/errors
- [stop]: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- [calls]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- [impl]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools ("Define tools"; the old implement-tool-use URL redirects here)
- [parallel]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- [so]: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- [prompt]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (section "Migrating away from prefilled responses")
- [batch]: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- [mcp-latest]: https://modelcontextprotocol.io/specification/latest/server/tools (section "Error Handling")
- [mcp-2025]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools (section "Error Handling")
- [mcp-2025-11]: https://modelcontextprotocol.io/specification/2025-11-25/server/tools (section "Error Handling")
- [cc-mcp]: https://code.claude.com/docs/en/mcp
- [hooks]: https://code.claude.com/docs/en/hooks
- [set]: https://code.claude.com/docs/en/settings
- [perm]: https://code.claude.com/docs/en/permissions
- [mem]: https://code.claude.com/docs/en/memory
- [cli]: https://code.claude.com/docs/en/cli-reference
- [strict]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
- [cc-subagents]: https://code.claude.com/docs/en/sub-agents ("In version 2.1.63, the Task tool was renamed to Agent")
- [sdk-perm]: https://code.claude.com/docs/en/agent-sdk/permissions
- [skills]: https://code.claude.com/docs/en/skills
- [headless]: https://code.claude.com/docs/en/headless
- [cc-tools]: https://code.claude.com/docs/en/tools-reference
- [messages]: https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- [Guide]: the official CCAR-F exam guide v1.0 (July 2026, Anthropic)

[err]: https://platform.claude.com/docs/en/api/errors
[stop]: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
[calls]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
[impl]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
[parallel]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
[so]: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
[prompt]: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[batch]: https://platform.claude.com/docs/en/build-with-claude/batch-processing
[mcp-latest]: https://modelcontextprotocol.io/specification/latest/server/tools
[mcp-2025]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
[mcp-2025-11]: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
[cc-mcp]: https://code.claude.com/docs/en/mcp
[hooks]: https://code.claude.com/docs/en/hooks
[set]: https://code.claude.com/docs/en/settings
[perm]: https://code.claude.com/docs/en/permissions
[mem]: https://code.claude.com/docs/en/memory
[cli]: https://code.claude.com/docs/en/cli-reference
[strict]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use
[cc-subagents]: https://code.claude.com/docs/en/sub-agents
[sdk-perm]: https://code.claude.com/docs/en/agent-sdk/permissions
[skills]: https://code.claude.com/docs/en/skills
[headless]: https://code.claude.com/docs/en/headless
[cc-tools]: https://code.claude.com/docs/en/tools-reference
[messages]: https://platform.claude.com/docs/en/build-with-claude/working-with-messages

[context-engineering]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents