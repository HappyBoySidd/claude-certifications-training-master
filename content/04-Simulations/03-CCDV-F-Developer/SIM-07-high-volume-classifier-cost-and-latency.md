# CCDV-F SIM-07 — Cutting Cost and Latency on a High-Volume Classifier

**Primary domains:** 5 Model Selection and Optimization, 6 Prompt and Context Engineering ·
**Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

An online marketplace uses Claude to sort every new listing into one of 40 categories and flag
prohibited items. Sellers see the result a few seconds after they post, and hundreds of thousands
of listings arrive each day. The classifier runs on the most capable model at a high effort level,
with a long instruction block of category definitions and 30 examples, and each answer explains
its reasoning in a paragraph. Accuracy is good, but the bill doubled this quarter and sellers
complain about the wait. You're asked to cut both **without losing accuracy**.


---

## The decisions (answer these before you open the key)

1. What to do before changing anything
2. The first lever to try on the current model
3. Most listings are easy; a few (possible weapons, medicines) are hard calls
4. Output tokens are most of the bill, and nobody reads the reasoning paragraph
5. The long instruction block is identical on every call and paid for at full price
6. After a clean-up trims the instructions to a few hundred tokens, both cache fields in `usage` read 0, and no error appears
7. The 30 examples are all easy categories, and edge cases are still misclassified
8. Category definitions are pasted after the listing text, mixed in with it
9. A taxonomy change means re-labeling millions of existing listings by next Monday
10. After the switch, a few answers use a different capitalization of a category, or come back with `stop_reason: "refusal"`

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | What to do before changing anything | **Build an eval set** of real listings with correct labels (edge cases and past mistakes included), grade by code, and record the current accuracy, cost and latency as the baseline | Switch to the cheapest model and watch complaints; ask the model to rate its own accuracy; test on five hand-picked listings | D5 Model Selection and Tradeoffs; D4 (simple evals) | [Lesson 7, section 4.3](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md), [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 2 | The first lever to try on the current model | **Lower the effort level** and re-run the eval. The docs call tuning effort often the better lever before switching models | Switch models first; raise `max_tokens`; lower temperature (a 400 on newer models) | D5 Model Selection and Tradeoffs (effort) | [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md), [Lesson 2, section 5.1](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 3 | Most listings are easy; a few (possible weapons, medicines) are hard calls | **Route by difficulty**: a small, fast tier (such as Haiku) for routine listings, and escalate prohibited-item doubts to a stronger tier. Prove it on the eval before rollout | The top model for everything "to be safe"; the cheapest model for everything; pick one model by price alone | D5 Model Selection and Tradeoffs (combining models) | [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 4 | Output tokens are most of the bill, and nobody reads the reasoning paragraph | **Return only what the system needs**: a category from an enum and a yes/no flag through structured outputs. Drop the explanation | Keep the paragraph "for audit"; set a tiny `max_tokens` and let answers cut off; ask for a "short" paragraph | D5 Cost and Token Management; D6 Output Handling | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md), [Lesson 4, section 6.5](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 5 | The long instruction block is identical on every call and paid for at full price | **Prompt caching**: stable content first (tools, system instructions, examples), a `cache_control` breakpoint at the end of it, and the listing text after | Put the listing first so it's "seen first"; resend the definitions inside each user message; delete half the definitions and lose accuracy | D5 Cost and Token Management (prompt caching) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 6 | After a clean-up trims the instructions to a few hundred tokens, both cache fields in `usage` read 0, and no error appears | **Below the model's minimum cacheable length, nothing is cached and no error is returned.** Check `usage`; decide whether caching still pays at this size | Report a caching bug; add more breakpoints; switch to the 1-hour cache | D5 Cost and Token Management (cache check-pointing) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 7 | The 30 examples are all easy categories, and edge cases are still misclassified | **Use 3–5 relevant, diverse examples** that cover the hard cases, wrapped in `<example>` tags, and say *why* each tricky one gets its label | Add 100 more easy examples; write the rules in capitals; remove examples entirely | D6 Prompt Engineering (few-shot) | [Lesson 4, section 6.4](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 8 | Category definitions are pasted after the listing text, mixed in with it | **Put the stable definitions in the system prompt** (which also keeps the cached prefix stable) and wrap the listing in `<listing>` tags in the user turn | Mix everything into one paragraph; put the definitions inside the listing; repeat them at the top and the bottom of every message | D6 Prompt Engineering (placement, XML tags) | [Lesson 4, section 6.4](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 9 | A taxonomy change means re-labeling millions of existing listings by next Monday | **Message Batches API** (50% of standard price), with the shared prefix cached using the **1-hour** duration, because batches can outlast a 5-minute cache | Run them all as parallel real-time calls; stream each one; re-label only when sellers complain | D5 Cost and Token Management; D2 Claude API Mechanics (batch) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md), [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 10 | After the switch, a few answers use a different capitalization of a category, or come back with `stop_reason: "refusal"` | **Check `stop_reason` before parsing, normalize and validate the value in code**, and send anything that fails to a fallback path or a person | Trust anything that matches the schema; drop failures silently; default every failure to "Other" | D6 Output Handling | [Lesson 4, section 6.5](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |

**Scoring:** 8 or more is a pass. Decisions 1 and 2 are the heart of the scenario: *measure before
you switch (an eval set and a baseline)*, and *pull the cheap levers first: effort, prompt
structure, caching and shorter output, then a smaller model only if the eval holds*.

Sources (Tier 1): [CCDV-F exam guide, Domains 5 and 6](https://anthropic-partners.skilljar.com/page/partner-certifications),
choosing a model,
effort,
prompt caching,
batch processing,
structured outputs,
prompting best practices.

</details>