# CCDV-F Lesson 2 — Model Selection and Optimization (16.8%, about 9 questions)

**Time:** 2 hours plus lab 04 · **Practice:** [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
Technical Fundamentals (6.1%) and LLM Fundamentals (5.2%) are most of this domain. Prices and
model names below are from the saved docs (September 2026); **check the current docs** before
you rely on a number.

## 5.0 The big idea

Everything is counted in tokens, and you pay for what goes in and what comes out. Pick the
smallest model that passes your evals, tune effort before switching models, and when the bill
is too high, fix prompt structure and caching before anything else.

## 5.1 LLM fundamentals (5.2%)

- **Tokens** are chunks of text (often part of a word). Everything is priced, limited and
  budgeted in tokens. Claude 4.7 and later use a newer tokenizer that makes **about 30% more
  tokens** for the same text, so re-check budgets when you migrate.
- **Context window** = everything Claude can see in one request: system prompt, all messages,
  tool definitions, images, **plus the output, including thinking**. Many current models have 1M
  tokens; others 200k. More isn't automatically better: recall drops as context grows
  (**context rot**).
- **Next-token generation:** Claude writes one token at a time, each chosen from a probability
  spread. **Sampling** picks from that spread, so the **same prompt can give different answers**
  (non-determinism). Design for it: validate outputs, and judge prompts over many runs.
- `temperature`, `top_p` and `top_k` are the classic sampling knobs, but on Claude 4.7 and later
  a non-default value returns a **400**. Steer with the prompt instead.
- **Model options.** Think of these as how long Claude may think, how hard it tries, and whether
  it rushes: each one trades quality against time and cost.

| Option | What it does | Remember |
| --- | --- | --- |
| **Extended thinking** | `thinking: {type: "enabled", budget_tokens: N}` | Older models; you set the budget |
| **Adaptive thinking** | `thinking: {type: "adaptive"}`: Claude decides when and how much to think | Always on for the newest models (e.g. Opus 5.5, Sonnet 5); opt-in on Opus 4.6–4.8 and Sonnet 4.6 |
| **Effort** | `output_config.effort`: `low` / `medium` / `high` / `xhigh` / `max` | Affects **all** output tokens, not only thinking. Default `high` (Opus 5.5: `medium`). A behavior signal, not a hard budget |
| **Fast mode** | `speed: "fast"`: up to 2.5× output speed at premium price | Research preview, some Opus models, first-party API only, **not in batches** |

- Thinking tokens are billed as **output** and come out of `max_tokens`. The thinking text you
  see is a summary; on the newest models `display` defaults to `"omitted"` (hidden).
- **Prompting basics:** zero-shot (instructions only), one-shot (one example), multi-shot
  (several). The docs recommend **3–5 examples** in `<example>` tags for format and edge cases.

## 5.2 Technical fundamentals (6.1%)

- **SDKs wrap the REST API.** They handle auth (API key from an environment variable), typed
  requests, automatic retries on transient errors, and streaming helpers. Know what's underneath:
  one `POST /v1/messages` with JSON in and JSON out.
- **Streaming uses server-sent events (SSE):** one-way, server to client, over HTTP. SDK helpers
  can stream internally and still hand you the final message, which avoids HTTP timeouts on long
  outputs.
- **WebSockets** are two-way and stay open. A common pattern: your backend streams from Claude
  over SSE and relays tokens to the browser over a WebSocket. (Check current docs for any
  WebSocket-based Anthropic endpoints; none are in our saved sources.)
- **Measure before you send:** the token counting API estimates a request's size. Every response
  reports actual use in `usage`.
- **Rate limits** are per model class: requests (RPM), input tokens (ITPM), output tokens (OTPM).
  `max_tokens` does **not** count against OTPM; only tokens actually generated do.

## 5.3 Model selection and tradeoffs (2.7%)

Think of the three tiers as a quick assistant, a strong all-rounder and a senior expert: you
don't send every small job to the most expensive person.

| | Haiku | Sonnet | Opus |
| --- | --- | --- | --- |
| Strength | Lowest latency and price | Speed plus capability, everyday default | Complex agentic coding, hard reasoning |
| Fits | High volume, real time, **subagent tasks**, classification | Code generation, data analysis, tool use | Multi-hour agents, large refactors, high stakes |
| Thinking | Extended thinking (no interleaved thinking) | Adaptive | Adaptive |

- Two ways to start: **efficiency-first** (start with Haiku, upgrade only for a real gap) or
  **capability-first** (start strong, then lower effort or downgrade as evals allow).
- **Tune effort before switching models.** The docs call it often the better lever.
- **Combine models:** a cheap executor that escalates hard calls to a strong advisor, or a strong
  orchestrator that hands bulk work to cheap workers.
- The docs also list a tier above Opus (Claude Fable 5.1). Exam items frame the choice as
  Haiku vs Sonnet vs Opus.
- **Breaking changes between releases** are why you pin versions and re-run evals:
  - Prefill returns 400 on 4.6 and later.
  - Non-default sampling parameters return 400 on 4.7 and later.
  - Opus 5.5 can't turn thinking off (400), and changed the default effort to `medium`.
  - Forced tool use (`tool_choice` `any`/`tool`) is flagged in Opus 5.5's breaking changes.
  - The new tokenizer changes token counts.

## 5.4 Cost and token management (2.8%)

- **Track usage per request:** `input_tokens`, `output_tokens`, `cache_creation_input_tokens`,
  `cache_read_input_tokens`. Total input = the three input fields added up. Log them with the
  prompt version and model so you can model cost.
- **Cost model:** (uncached input × input price) + (cache writes × write price) + (cache reads ×
  read price) + (output × output price), then × 0.5 if batched.
- **Prompt caching:** the cache matches a **prefix** in the order `tools` → `system` →
  `messages`. Put stable content first and variable content last.
  - Default lifetime is 5 minutes, refreshed free on each hit. The 1-hour option costs 2× to write.
  - A 5-minute write costs 1.25×, so it **pays off after one read**; 1-hour pays off after two.
  - **Cache checkpointing:** up to **4 breakpoints**. Put them where content changes at different
    rates (tools, then system, then conversation). The lookback checks only **20 blocks**, so long
    conversations need an extra breakpoint.
  - Below the model's minimum length (512–4,096 tokens, by model) nothing is cached and **no error
    is returned**. If both cache fields in `usage` are 0, it didn't cache.
  - Cache reads don't count toward ITPM on most models: caching also raises throughput.
- **Lever order when the bill is too high:** fix prompt structure and caching → lower effort →
  batch what isn't urgent → smaller model (only if evals hold).

## Worked example

10,000 requests share a 5,000-token instruction prefix, plus 500 variable tokens and 300 output
tokens each. Using Sonnet 5's saved prices ($2 input, $0.20 cache read, $10 output per million):

- **No caching:** 55M input × $2 = $110, plus 3M output × $10 = $30. **About $140.**
- **Prefix cached** (requests close enough to keep hitting): 50M reads × $0.20 = $10, plus 5M
  uncached × $2 = $10, plus $30 output. **About $50.** The one-time write is pennies.
- **Also batched** (not urgent): the 50% discount stacks, **about $25** if the cache keeps hitting.

Output is now the biggest cost, so trimming verbose output is the next lever, not a smaller model.

## Traps

- "Use Opus to be safe." Pick the cheapest model that passes your evals.
- "Raise temperature for variety." On current models that's a 400.
- "Set `max_tokens` low to save money." You pay for tokens generated, not the cap, and a low cap
  truncates answers (`stop_reason: max_tokens`).
- "Caching failed with an error." Below the minimum it fails **silently**. Check `usage`.
- "A timestamp at the top of the system prompt is fine." It breaks the cached prefix every call.

## Try it, lab 04 (90 min)

[Lab 04](../../06-Labs/04-CCDV-F-api-modes/README.md): run the same task real-time, with caching
and batched. Compute cost from `usage` with the formula above and compare it to your estimate.

## Done when

- [ ] You can explain tokens, context rot, sampling and why outputs vary
- [ ] You can tell thinking, adaptive thinking, effort and fast mode apart
- [ ] You can pick Haiku, Sonnet or Opus for a scenario and justify it in one line
- [ ] You can compute a request's cost from `usage` and say where caching pays off
- [ ] You scored 80% or more on [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Source: official CCDV-F exam guide v1.0, Domain 5 objectives. Docs:
platform.claude.com/docs/en/about-claude/models/choosing-a-model, …/about-claude/pricing,
…/build-with-claude/context-windows, …/thinking, …/effort, …/prompt-caching, …/streaming,
…/batch-processing, …/working-with-messages, …/prompt-engineering/claude-prompting-best-practices;
…/api/rate-limits.