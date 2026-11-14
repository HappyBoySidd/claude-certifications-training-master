# Lab 04 — Same task, three API modes: real time, cached and batch (CCDV-F, CCAR-P)

**Supports:** CCDV-F L01, L02 · CCAR-P L06 · **Time:** 2 hours · **Needs:** Python 3.10+,
`pip install anthropic`, an API key (see the laptop note in [lab 02](../02-CCAR-F-coordinator-extraction/README.md)).

**Done when:** you have a small table of latency, input tokens, cached tokens and relative cost for
the same 20 requests run three ways, and you can say in one sentence when each mode wins.

## Setup

- Choose one task, such as "classify this support email into 1 of 6 categories and give a reason".
- Write a long, **fixed** system prompt of several thousand tokens: the policy, category
  definitions and examples. Keep it the same on every request.
- Make 20 short emails as the varying input.

## Run A — real time, no caching

- Call `client.messages.create(...)` 20 times.
- Record wall-clock time and `response.usage.input_tokens` / `output_tokens`.
- Try `stream=True` once and note the time to the first token versus the full response.

## Run B — real time with prompt caching

- Put the fixed system prompt **first**, with `cache_control: {"type": "ephemeral"}` on its last
  block.
- Rerun the 20 requests. From the second request on, check `usage.cache_read_input_tokens`
  against `cache_creation_input_tokens`.
- The cache matches only an **identical prefix**. Change one word in the system prompt and watch
  the reads drop to zero.
- Minimum cacheable length and cache lifetime vary. Check the
  [prompt caching docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching).

## Run C — Message Batches API

- Submit all 20 requests as one batch with `client.messages.batches.create(requests=[...])`,
  giving each one a `custom_id`.
- Poll until the batch ends, then read the results by `custom_id`. Results can come back in any
  order.
- Note that batch trades speed for cost: results arrive asynchronously, within a window of up to
  24 hours. See the [batch processing docs](https://docs.claude.com/en/docs/build-with-claude/batch-processing).

## Compare

| Mode | Time to results | Input tokens billed at full price | Best when |
| --- | --- | --- | --- |
| A real time | | | a user is waiting, and every prompt is different |
| B cached | | | a large prompt prefix repeats across calls |
| C batch | | | nobody is waiting, and cost matters most |

Use the current [pricing page](https://docs.claude.com/en/docs/about-claude/pricing) to turn tokens
into cost. Don't use remembered numbers.

## Bonus

- Add simple retry with backoff for `429` (rate limited) and overloaded errors.
- Rerun A on a smaller and a larger model tier, and compare quality on 5 emails.

Sources: CCDV-F official exam guide v1.0, Domain 2 "Claude API Mechanics" and Domain 5 "Cost and
Token Management"; the docs linked above; [streaming](https://docs.claude.com/en/docs/build-with-claude/streaming);
[rate limits](https://docs.claude.com/en/api/rate-limits).

## What I learned

-