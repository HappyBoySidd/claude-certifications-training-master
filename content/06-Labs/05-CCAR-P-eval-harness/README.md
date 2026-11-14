# Lab 05 — An evaluation harness with a regression check (CCAR-P, CCDV-F)

**Supports:** CCAR-P L01 (step 7), L03 · CCDV-F L07 · **Time:** 3 hours, plus 1 hour for step 7 ·
**Needs:** the extractor from [lab 02](../02-CCAR-F-coordinator-extraction/README.md), or any small
Claude task you already have; for step 7, a small document set.

**Done when:**

- one command runs a 30-case test set and prints a score by metric
- a prompt change that makes things worse **fails** the run
- you can say which failures are prompt problems, retrieval or context problems, or model-fit
  problems
- you have recall@5 for keyword, vector and hybrid retrieval, and can say which question types
  each one wins

## Steps

### 1. A test set before any tuning

Write 30 cases in a `cases.jsonl` file, each with an input, the expected output or key facts, and
a tag:

| Tag | Share | Example |
| --- | --- | --- |
| normal | 60% | a clean invoice |
| edge | 25% | a missing date, two currencies, a handwritten total |
| adversarial | 15% | text inside the document saying "ignore your instructions" |

### 2. Three kinds of grader

- **Code-graded**, for anything exact: the JSON is valid, the total matches, the date is ISO.
- **Model-graded**, for judgment: a second Claude call with a short **rubric** that returns a
  1–5 score *and a reason*. Check the grader itself on 5 cases you've scored by hand.
- **Human review**, only for the cases the other two disagree on.

### 3. Metrics that match the goal

Report accuracy (per field), cost (tokens per case), latency (p50 and p95) and a safety pass rate
(the adversarial cases). Averages hide failures, so also print the **worst 3 cases**.

### 4. The regression gate

- Save today's scores as `baseline.json`.
- The harness exits with a failure if any metric drops by more than your threshold, for example
  2 points of accuracy, or if any adversarial case fails.
- Now make the prompt worse on purpose, for example by deleting the examples, and confirm the
  gate catches it.

### 5. A/B a real change

- Change one thing: add two examples, switch model tier, or raise the effort level.
- Run both versions on the same 30 cases and compare them metric by metric.
- Decide with the numbers, and write the trade-off in one line, for example "+4 accuracy,
  +30% cost".

### 6. Diagnose the failures

For each failure, ask in this order:

1. Was the needed information in the context at all? If not, it's a retrieval or context
   problem.
2. Was the instruction clear and in the right place? If not, it's a prompt problem.
3. Did it fail anyway? Then it may be a model-fit problem.

Log the answer next to the case.

### 7. Retrieval comparison

This step is for CCAR-P L01. It checks whether the *search* part finds the right text before
Claude ever sees it. About 1 hour.

- Take a small document set, for example 10–15 policy pages or README files, and split it into
  chunks along its headings.
- Write about 20 question and right-chunk pairs in `retrieval.jsonl`: the question, the ID of the
  chunk that answers it, and a tag:

| Tag | Example |
| --- | --- |
| exact | "What is error code E-2207?" (a code, a name, a part number) |
| paraphrase | "Can I bring my partner on a work trip?" when the doc says "companion travel" |
| mixed | a concept plus an exact term, for example "refund rules for plan P-40" |

- Run the same questions three ways: **keyword-only** (BM25 or plain keyword search),
  **vector-only** (embeddings), and **hybrid** (both, results merged).
- Score **recall@5**: the share of questions where the right chunk is in the top 5 results.
  Print it per method and per tag.
- Write one line per tag saying which method won, for example "exact: keyword 95%, vector 60%".
  Expect keyword to win on exact terms, vector on paraphrases, and hybrid to be the safest overall.

Sources: CCAR-P official exam guide, Domain 4 "Evaluation, Testing & Optimization" and Domain 3
retrieval objectives; [contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
(Tier 1, for keyword plus embeddings); [define success criteria and build evaluations](https://docs.claude.com/en/docs/test-and-evaluate/develop-tests);
[reduce hallucinations](https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations).

## What I learned

-