# CCDV-F Lesson 1 — Applications and Integration (33.1%, about 18 questions)

**Time:** 3 hours plus lab 04 · **Practice:** [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Biggest domain on the exam.** Its two largest skills are Application Design (8.6%) and
Software Engineering Foundations (7.4%), then API Mechanics (6.8%).

## 2.0 The big idea

Almost every question here asks two things: *who is waiting*, and *what does the rest of the
system need back?* A person waiting means real-time and streamed; nobody waiting means batch; the
same long prefix every call means caching. Then build it like normal software: retry what's
temporary, fix what's wrong, and pin what must not change.

## 2.1 Understanding requirements (3.4%)

- **Functional** = what the app must do (summarize tickets, extract fields). **Infrastructure**
  (non-functional) = how it must run: latency, volume, cost, availability, data location.
- Turn business words into design choices before you pick anything:

| Requirement says | Design implication |
| --- | --- |
| "A user is waiting", "live chat" | Real-time Messages API, streamed |
| "Overnight", "by tomorrow", "bulk" | Message Batches API |
| "Same long instructions every call" | Prompt caching on a stable prefix |
| "Data must stay in the US" | `inference_geo: "us"` (Claude 4.6+, 1.1× price) or a regional Bedrock/Google Cloud endpoint (+10%) |
| "Must output fields our system reads" | Structured outputs (JSON schema) |

## 2.2 Systems life cycle (2.8%)

- Plan → design → build → **test (evals)** → deploy → **operate (monitor)** → maintain → retire.
- Claude twists: tests include **evals**; "maintain" includes **model deprecations** (plan the
  migration, re-run evals, switch). Roll out new models and prompts in stages, with a way back.

## 2.3 Claude API mechanics (6.8%)

- **The Messages API is stateless.** You resend the full history every call. Long chats cost more
  per turn. `system` is a top-level field; `messages` alternate `user` and `assistant`.
- Content comes as **blocks**: text, image, document, `tool_use`, `tool_result`, thinking.
- **`stop_reason`** tells you what to do next: `end_turn` (done), `tool_use` (run the tool, send
  back a `tool_result`), `max_tokens` (cut off: raise the limit or split the task), `refusal`.
- **Tools:** *client tools* run in your code (you return `tool_result`); *server tools* such as
  web search, web fetch and code execution run on Anthropic's side.
- **Streaming** (server-sent events): `message_start` → per block `content_block_start` /
  `content_block_delta` / `content_block_stop` → `message_delta` → `message_stop`, plus `ping`.
  It cuts **perceived** latency, not cost. The SDKs need streaming for large `max_tokens` to avoid
  HTTP timeouts. Errors (for example `overloaded_error`) can arrive **mid-stream**.
- **Vision:** send images as base64, URL, or a Files API `file_id`. Put **images before text**.
  On Bedrock and Google Cloud, only base64 is available.
- **Thinking:** thinking tokens are billed as output and count toward `max_tokens`. With tool use,
  pass the thinking block back **unmodified** with the tool result, or the API errors.
- **Prefill** (starting Claude's reply yourself) returns a 400 on Claude 4.6 and later. Use
  structured outputs or system instructions instead.
- **Third-party vendors:** Claude runs on Amazon Bedrock, Google Cloud, Microsoft Foundry and
  Claude Platform on AWS. Features can differ by platform (fast mode is first-party only), so
  check the platform's page before you rely on one.
- **Data access patterns** (our reading of this objective): put data inline in the message,
  upload once and reference by `file_id`, or let Claude fetch it through a tool or MCP.

Picking one is like choosing between a phone call (answered now), a letter (cheaper, arrives
later) and a saved template (the part you'd otherwise rewrite every time).

**Real-time vs batch vs caching** (these combine; they're not either/or):

| | Real-time | Message Batches API | Prompt caching |
| --- | --- | --- | --- |
| Use when | Someone is waiting | Nobody is waiting, high volume | The same prefix repeats |
| Price | Standard | **50% of standard** | Reads ~0.1× input; writes 1.25× (5 min) or 2× (1 h) |
| Latency | Seconds | Most done in under 1 hour; expires at 24 hours | Faster on a hit |
| Limits | Rate limits (RPM, ITPM, OTPM) | 100,000 requests or 256 MB per batch; results kept 29 days | Min prefix length per model; up to 4 breakpoints |
| Gotcha | — | No `stream: true`; match results by `custom_id`, not order | Anything that changes early in the prompt breaks the prefix |

## 2.4 Software engineering foundations (7.4%)

- **REST:** `POST https://api.anthropic.com/v1/messages` with `x-api-key`, `anthropic-version`
  and `content-type: application/json` headers. The SDKs wrap this.
- **Errors, and what to do.** In everyday terms, some errors mean "you asked wrong" (fix it) and
  some mean "too busy, try again later" (wait, then retry):

| Code / type | Meaning | Action |
| --- | --- | --- |
| 400 `invalid_request_error` | Your request is wrong (also: prompt too long) | Fix it. **Don't retry.** |
| 429 `rate_limit_error` | Over RPM/ITPM/OTPM | Wait for `retry-after`, back off |
| 429 with **no** `retry-after` | Monthly spend cap reached | Retrying won't help; raise the limit |
| 529 / `overloaded_error` | Anthropic is busy | Retry with exponential backoff and jitter |

- **Async:** fire many real-time calls concurrently (`asyncio.gather`, `Promise.all`) but **cap
  concurrency** to your rate limit. Limits refill continuously (token bucket), so short bursts
  can trip them.
- **Version control and SDLC:** prompts, schemas and config live in git, get code review, and run
  evals in CI like tests.
- **Refactoring:** small = one change, tests stay green. Large = plan first, split into steps,
  keep tests as the safety net, and review each step.

## 2.5 Claude application design (8.6%)

- **Each interface wraps Claude differently.** claude.ai and Desktop add their own system prompt,
  Projects and memory. Claude Code loads CLAUDE.md files as context. On the API, **you own the
  whole prompt**. The SDKs are thin wrappers over the API.
- **Content boundaries:** keep instructions apart from data. Wrap inputs in XML tags
  (`<document>`, `<user_input>`) and treat retrieved or user content as untrusted.
- **Schema design:** use structured outputs (`output_config.format` with `json_schema`) or
  `strict: true` on tools, which guarantee schema-valid output via constrained decoding. Keep
  schemas small, use enums and required fields, and allow `null`/"unknown" so Claude isn't forced
  to invent a value.
- **Session hygiene:** one task per session; start fresh (or summarize, then restart) when
  context gets stale, rather than piling on corrections.
- **Plugins** (Claude Code) bundle commands, Skills, subagents, hooks and MCP servers. Install
  only what you trust, and review what a plugin can run.

## 2.6 Configuration management (4.1%)

- **CLAUDE.md hierarchy:** user (`~/.claude/CLAUDE.md`, only you), project (root or
  `.claude/CLAUDE.md`, committed, whole team), directory (subfolder CLAUDE.md). Use `@import`
  for modular files and `.claude/rules/` files with `paths:` globs for area-specific rules.
- **settings.json:** permissions, hooks, environment and model settings for Claude Code. Shared
  project settings are committed; personal overrides stay local (check the current docs for
  exact file names and precedence).
- **Model version pinning:** production should call a **specific model version**, so behavior
  doesn't shift under you. Upgrading is a deliberate change: run evals, then switch.
- **Prompt versioning:** give each prompt a version, log it with every request, and roll back
  like code.
- **Plugin dependencies:** pin versions of plugins and MCP servers; an update can change tools.

## What people who passed say

More Claude Code than its 3.1% weight (much of it lives in 2.6): *Confirmed*, two colleagues
who passed (INSIGHTS, 2026-09-26). Streaming and protocols in scenarios: *single report*,
one colleague who passed.

## Worked example

A help-desk app has three jobs. (1) Agents chat with Claude live about an open ticket.
(2) Every night, 40,000 closed tickets get re-tagged. (3) Both jobs start with the same
6,000-token policy manual. **Design:** job 1 is real-time and streamed, with the manual cached at
the front of the prompt. Job 2 goes to the Message Batches API (50% off), with the manual cached
using the **1-hour TTL**, because batches can outlast a 5-minute cache. Each request gets a
`custom_id` equal to the ticket ID. "Run job 2 as 40,000 parallel real-time calls" is wrong:
it's full price and trips rate limits.

## Traps

- "Streaming makes it cheaper." It only makes it *feel* faster.
- "Retry every error." A 400 fails the same way every time.
- "Batch results come back in order." Match on `custom_id`.
- "Use the model alias in production." Pin a version.
- "Cached tokens don't count toward the context window." They do; you just pay less.

## Try it, lab 04 (90 min)

[Lab 04](../../06-Labs/04-CCDV-F-api-modes/README.md): run one task real-time, then with
prompt caching, then through the Message Batches API. Record cost (from `usage`) and latency.

## Done when

- [ ] You can map any requirement sentence to real-time, batch, caching or structured outputs
- [ ] You can name each `stop_reason` and what your code does next
- [ ] You know which errors to retry, and how
- [ ] You can explain the CLAUDE.md hierarchy and why production pins a model version
- [ ] You scored 80% or more on [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Source: official CCDV-F exam guide v1.0, Domain 2 objectives and sample 1; CCAR-F exam guide
v1.0, task statement 3.1 (CLAUDE.md). Docs: platform.claude.com/docs/en/build-with-claude/working-with-messages,
…/streaming, …/vision, …/thinking, …/context-windows, …/prompt-caching, …/batch-processing,
…/structured-outputs; …/agents-and-tools/tool-use/overview; …/api/rate-limits;
…/about-claude/pricing. Settings.json and plugin details: check current Claude Code docs.