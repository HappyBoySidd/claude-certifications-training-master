# CCAR-P Lesson 3 — Evaluation, Testing and Optimization (16%, about 10 questions)

**Time:** 2 hours plus lab 05 · **Practice:** [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Already covered in CCAR-F:** per-field confidence, stratified sampling and "97% overall can hide
a weak document type" are in [CCAR-F L05](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).
This lesson is about building the eval system, reading its results, and spending less without
losing quality.

## 4.0 The big idea

If you can't measure it, you can't improve it. Decide what "good" means before you build, rerun the same test set every time anything changes, and fix the layer that actually broke instead of guessing.

## 4.1 Metrics: decide them before you build

Write the marking scheme before the exam: decide what a good result looks like before you write a single prompt.

| Metric | Example measures |
| --- | --- |
| **Accuracy and quality** | Exact match, F1 on extracted fields, rubric score, groundedness (claims backed by a source) |
| **Latency** | Time to first token, total time, p95 against the SLA |
| **Cost** | Tokens and dollars per request or per resolved case, cache hit rate |
| **Safety** | Harmful-output rate, correct refusals, over-refusals |
| **Security** | Prompt-injection resistance, data leaks, unauthorized tool calls |

- Make success criteria **specific and measurable**, and judge on **several dimensions at once**
  ([define success criteria](https://platform.claude.com/docs/en/test-and-evaluate/define-success)).
- **Break results down** by case type, language, customer group. One average hides the failures.

## 4.2 Eval datasets and mixed methods

- Build the set from **real traffic**, and add edge cases, adversarial inputs and past incidents.
  Label the expected answer, or the expected properties, for each case.
- Keep a **held-out set** you don't tune against, so you aren't grading your own homework.
- The docs favor **more test cases with automated grading** over a few hand-graded ones
  ([develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)).

No single way of grading covers everything, so mix them:

| Method | Best for | Watch out for |
| --- | --- | --- |
| **Code-graded** | Crisp truth: a label, a JSON field, a number, a valid schema | Can't judge tone or reasoning |
| **Model-graded** (LLM-as-judge) | Subjective quality, with a **clear rubric** and a reason before the score | The judge can be wrong. Check it against human labels first |
| **Human review** | High stakes, new failure types, calibrating the judge | Slow and costly, so sample it |

Mix all three: code where you can, a rubric-guided model where you must, and humans to audit both.

## 4.3 A/B testing and iterating

1. **Baseline:** run the current version on the eval set and save the scores.
2. **Change one thing** (the prompt, the model, the retrieval setting or the effort level).
3. **Offline:** rerun the whole set. The **regression suite must pass**. No old case may break.
4. **Online:** A/B test on live traffic with metrics you **fixed in advance**, and let it run
   long enough to mean something.
5. **Roll out gradually,** keep a rollback path, and add the new failures to the eval set.

A prompt change is a production change. Version prompts like code.

## 4.4 Diagnosing: which layer broke?

When something goes wrong, check the most likely broken layer first, the way you check the plug before the wiring:

| Symptom | Most likely cause | First check |
| --- | --- | --- |
| Wrong right after a data refresh; model and latency unchanged | **Retrieval or index** | Are the retrieved chunks relevant and current? Same embedding model on both sides? |
| Right facts in context, but the answer ignores them or has the wrong format | **Prompt** | Instructions, examples, output format |
| Confident claims that no source supports | **Hallucination** | Allow "I don't know", quote first, cite each claim |
| Fine on easy cases, fails on the hard reasoning ones | **Model mismatch** | Try a higher effort level or a more capable model, on the eval set |
| Slow, or expensive, but correct | **Configuration** | Caching, model tier, batch, effort (4.5) |

Look at the **trace**. The retrieved context tells you if the problem is upstream of the model.
The docs' hallucination tactics: let Claude say it doesn't know, ground answers in direct quotes
from long documents, and retract any claim it can't back with a quote
([reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)).

## 4.5 Optimizing tokens, latency and cost

Each lever below cuts cost or waiting time. Pull it only when its "use when" is true:

| Lever | What it does | Use when |
| --- | --- | --- |
| **[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)** | Reuses a stable prefix (tools, system, then messages). Cache reads cost a fraction of normal input. The default lifetime is 5 minutes, and 1 hour costs more | The same long instructions or documents on many requests. Put static content first |
| **[Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing)** | 50% of standard prices. Most batches finish within 1 hour, and results come within 24 hours at most | Nobody's waiting: overnight scoring, backfills, eval runs |
| **Model tiering** | A smaller model for simple steps, a larger one for hard ones | Routing or orchestrator-worker designs ([choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)) |
| **[Effort](https://platform.claude.com/docs/en/build-with-claude/effort)** | Trades thoroughness for fewer tokens within one model | Often a better first lever than switching models |
| **Trim context** | Fewer, better chunks. Trim tool output | Long prompts that are slow and suffer context rot |

The caching and batch discounts **stack** (see [pricing](https://platform.claude.com/docs/en/about-claude/pricing)).
Check that caching works with the usage fields: if both `cache_creation_input_tokens` and
`cache_read_input_tokens` are 0, nothing was cached. The prompt may be under the minimum
cacheable length, which varies by model, so check the current docs.

## 4.6 Monitoring in production

- Log per request: prompt and model version, the retrieved chunk IDs, tool calls, tokens, cache
  usage, latency, and the outcome (including human overrides).
- Put the eval metrics on a dashboard, and run a **sample of live traffic** through the graders.
- **Alert on drift:** quality score, refusal rate, the rate of escalations to a human, cost per
  case, and p95 latency.

## Worked example

A bank summarizes loan files for its underwriters. After a prompt update, the underwriters say
the summaries "feel worse", and the monthly bill has doubled. **Answer:** first, measure. Rerun
the frozen eval set on the old and new prompts. Grade the figures with code (amounts and dates
must match the file) and completeness with a rubric-guided model judge, checked against a
human-labeled sample. The new prompt drops the covenant section, so roll it back and add those
cases to the regression suite. For the cost: move the long, fixed instructions to the front and
cache them. Send the overnight backlog through the Batch API. Use a smaller model for the
document-type classification step. "Switch to the biggest model" and "ask the underwriters to
rate more" skip measurement.

## Traps

- "Judge quality by answer length or exact match on prose." Use a rubric.
- "Ship it, it looked good on five examples." Use an eval set and a regression suite.
- "Wrong answers after a re-index, so change the model." Check retrieval first.
- "Use Batch for the live chat." Batch is for work nobody's waiting on.
- "Trust the LLM judge without checking it against humans."

## Try it (2–3 hours): lab 05

Build a small eval harness for the lab 02 extractor: 20–30 labeled cases, code grading for the
fields, one rubric-graded check, a saved baseline, and a regression check that fails the run if
any old case breaks. See [`06-Labs/05-CCAR-P-eval-harness/`](../../06-Labs/05-CCAR-P-eval-harness/README.md).

## Done when

- [ ] You can name a measure for each of the 5 metric families
- [ ] You can say when to use code-graded, model-graded and human review
- [ ] You can walk the diagnosis table from symptom to first check
- [ ] You can pick caching, batch, tiering or effort for a given cost or latency problem
- [ ] You scored 80% or more on [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L04 Governance, Safety and Risk Management](L04-governance-safety-and-risk-management.md)

Source: official CCAR-P exam guide v1.0, Domain 4 objectives and samples 2–3; Anthropic docs linked above.