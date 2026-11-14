# CCAR-P Lesson 6 — Models, Prompting and Context (13%, about 8 questions)

**Time:** 2 hours plus lab 04 (caching part) · **Practice:** [Lesson 6 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Already covered:** explicit criteria, few-shot, tool-based structured output and batches are in
[CCAR-F L04](../02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md);
context degradation is in [CCAR-F L05](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).
Here the focus is on choosing and justifying at production scale.

## 2.0 The big idea

Pick the smallest model and simplest prompt that pass your tests, and spend more only where the tests show a gap. Treat the context window like a small desk: put only the right things on it, in the right order, and reuse the fixed parts with caching.

## 2.1 Model selection by trade-off

Weigh **capabilities, speed and cost**, then prove it with evals on your own data. The saved
"choosing a model" page (September 2026) lists these starting points. Model names change often, so
**check the current docs** before quoting a version.

| Tier | Starting point in the saved docs | Use when |
| --- | --- | --- |
| Highest capability | Claude Fable 5.1 | Hours-long agent sessions, deep multistep research |
| Opus | Claude Opus 5.5 | Complex agentic coding and enterprise work; the docs say most workloads start here |
| Sonnet | Claude Sonnet 5 | Speed plus capability for everyday coding, agents and analysis |
| Haiku | Claude Haiku 4.5 | Lowest latency and price: real-time, high volume, sub-agents, classifiers |

- **Two ways to start:** *efficiency-first* (start small, upgrade only for a proven gap) or
  *capability-first* (start strong, then lower effort or downgrade as the workflow is optimized).
- **Effort is often a better lever than switching models.** The `effort` setting trades intelligence
  for latency and cost within one model (levels such as `low`, `medium`, `high`; some models add
  `xhigh` and `max`). Defaults differ by model, so check the effort page.
- **Combine models:** an orchestrator on a frontier model delegating bulk work to cheaper workers, or
  a cheap executor escalating hard calls to a stronger advisor.
- **The deciding step is a benchmark on your own prompts and data.** Brand preference isn't a reason.

## 2.2 System prompts, templates and guardrails

- **Role** in the system prompt, even one sentence, focuses behavior.
- **XML tags** (`<instructions>`, `<context>`, `<documents>`) separate parts so nothing is misread.
- **Templates** with variables (`{{CONTRACT}}`) keep the fixed part fixed, which is good for caching
  and for review.
- **Guardrails in the prompt:** permission to say "I don't know", "use only the provided documents",
  and an untrusted-content policy. They help, but real enforcement is in code ([L04](L04-governance-safety-and-risk-management.md)).
- **Version prompts like code.** A prompt change is a production change: regression suite, then roll out.

## 2.3 Techniques: zero-shot, few-shot, chain-of-thought, thinking

Start with the simplest technique and add more only when results drift:

| Technique | Use when | Note |
| --- | --- | --- |
| **Zero-shot** | Clear task, clear format | Cheapest; start here |
| **Few-shot** | Format or judgment drifts | The prompting guide suggests 3–5 relevant, diverse examples in `<example>` tags |
| **Chain-of-thought** | Multistep reasoning, and you want to see the logic | Also a verification tool for hallucinations |
| **Extended / adaptive thinking** | Hard reasoning, agentic tool loops | Thinking tokens count toward context and cost; tune with `effort`, cap with `max_tokens` |

- **Lower cost or latency on a thinking workload:** lower `effort` first. **Need a hard spend
  ceiling:** use `max_tokens`, because effort is soft guidance.
- Some newer models think adaptively by default, and some combinations (such as forced tool use with
  certain thinking modes) aren't supported. Check the thinking page for your model.

## 2.4 Context windows and token management

- **More context isn't automatically better.** As tokens grow, accuracy and recall degrade (the docs
  call it *context rot*). Curate what goes in.
- **Everything counts:** system prompt, messages, tool results, images, tool definitions and the
  output, including thinking. The `usage` field shows what a request used.
- Context sizes vary by model (up to 1M tokens on some; 200k on others). Check the table.
- **Long documents at the top, question at the end.** The prompting guide says this can improve
  quality by up to 30% on complex multidocument inputs.
- **Estimate before sending** with the token counting API.
- **Long-running work:** server-side compaction summarizes earlier turns; retrieval and progressive
  discovery keep only what's needed in context (see [L01](L01-integration.md)).

## 2.5 Prompt reuse: caching, modular prompts, Skills

**Prompt caching** reuses a prompt *prefix*. The cache covers `tools`, then `system`, then `messages`,
up to the block marked with `cache_control`.

| Fact | Value (saved pricing and caching docs) |
| --- | --- |
| Order | **Static content first, dynamic last**; any change before the breakpoint misses the cache |
| Default lifetime | 5 minutes, refreshed free on each hit; 1 hour available at extra cost |
| Cache write | 1.25× base input (5-minute) or 2× (1-hour) |
| Cache read | 0.1× base input (per-model exceptions exist) |
| Breakpoints | Up to 4 explicit; or one top-level automatic `cache_control` for growing conversations |

- Caching cuts **both** latency and cost, which is why it's the answer when both are named (exam
  guide, sample 2). Truncating the prompt or downsizing the model blindly isn't.
- **Modular prompts:** shared blocks (policy, style, tool guidance) assembled per use case and
  versioned, so one fix reaches every prompt.
- **Skills** package a reusable procedure that loads **on demand**, instead of bloating every prompt.

## Worked example

A travel company's support assistant sends a 12,000-token policy manual plus tool definitions on
every turn, uses the top model for every query, and is slow and expensive. **Response:** reorder so
tools, system prompt and manual come first, then enable caching. Route simple itinerary lookups to a
Haiku-tier model and keep complex rebooking on a stronger model, or try lower effort first. Move
rarely used procedures into Skills. Prove each change against the eval set before rollout.

## Traps

- "Use the biggest model to be safe." Pick by evals and trade-off.
- Putting the timestamp or user ID at the top of the prompt, which breaks the cache every time.
- "Paste the whole knowledge base; the window is big enough." Context rot.
- Using `effort` as a hard cost cap. That's `max_tokens`.
- Quoting a model version from memory on a design doc.

## Try it (30 min): lab 04, caching part

In [lab 04](../../06-Labs/04-CCDV-F-api-modes/README.md), send the same long system prompt five
times with the dynamic question last and `cache_control` on the static block. Record
`cache_creation_input_tokens` and `cache_read_input_tokens` for each call. Then move a changing value
above the breakpoint and watch the reads drop to zero.

## Done when

- [ ] You can justify a model tier with capability, speed, cost and an eval, and name effort as a lever
- [ ] You can choose zero-shot, few-shot, chain-of-thought or thinking for a scenario
- [ ] You can state the cache order, lifetime and read/write multipliers
- [ ] You can explain context rot and three ways to manage tokens
- [ ] You scored 80% or more on [Lesson 6 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L07 Developer Productivity and Enablement](L07-developer-productivity-and-enablement.md)

Source: official exam guide v1.0, Domain 2 objectives and sample 2;
https://platform.claude.com/docs/en/about-claude/models/choosing-a-model;
https://platform.claude.com/docs/en/build-with-claude/effort;
https://platform.claude.com/docs/en/build-with-claude/thinking;
https://platform.claude.com/docs/en/build-with-claude/context-windows;
https://platform.claude.com/docs/en/build-with-claude/prompt-caching;
https://platform.claude.com/docs/en/about-claude/pricing;
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.