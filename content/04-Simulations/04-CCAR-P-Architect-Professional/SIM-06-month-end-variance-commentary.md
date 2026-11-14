# CCAR-P SIM-06 — Month-End Variance Commentary

**Primary domains:** 2 Claude Models, Prompting & Context Engineering, 4 Evaluation, Testing &
Optimization · **Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

An accounting firm closes the books for 3,000 client accounts every month. For each account an
analyst writes a short commentary explaining why this month's numbers moved against last month's.
The firm wants Claude to draft those commentaries from the account's ledger (often 100–180k tokens),
a 20,000-token internal accounting policy, and a few lookup tools. Partners care about two things:
**every number and every cause in the commentary must be traceable to the ledger**, and the monthly
bill must stay predictable.


---

## The decisions (answer these before you open the key)

1. Which model to start with
2. Drafts are good, but thinking tokens make the bill too high
3. Commentaries drift in tone and structure between accounts
4. The prompt puts the question first, then the ledger, then the policy; answers on big ledgers get worse
5. The same policy and tool definitions go out on every call, and a timestamp sits at the very top
6. The monthly run happens overnight and nobody waits on a single draft
7. Deciding what "good" means before tuning
8. A model-graded rubric scores "causes are supported"; nobody knows if the grader is right
9. A draft blames a variance on a "one-off supplier refund" that isn't in the ledger
10. A new model version is released and the team wants to switch next month

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | Which model to start with | **Pick a starting strategy and prove it on the firm's own ledgers**: efficiency-first (start small, upgrade for a proven gap) or capability-first (start strong, then lower effort or downgrade), with the choice confirmed by an eval on real accounts | The newest model because it's newest; the cheapest model because volume is high; the model a partner likes | D2 Model selection by trade-off | [Lesson 6, section 2.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 2 | Drafts are good, but thinking tokens make the bill too high | **Lower `effort` first**, then re-run the eval; use `max_tokens` only where a hard ceiling is needed, because effort is soft guidance | Switch off thinking everywhere; cap `max_tokens` so low answers get cut off; move to a smaller model without testing | D2 Techniques (thinking, effort); D4 Cost-performance trade-offs | [Lesson 6, section 2.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md), [Lesson 6, section 2.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 3 | Commentaries drift in tone and structure between accounts | **Few-shot**: 3–5 diverse, relevant example commentaries in `<example>` tags, plus an explicit output structure | "Be consistent" in the prompt; one example repeated five times; let analysts rewrite every draft | D2 Prompting techniques (few-shot) | [Lesson 6, section 2.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 4 | The prompt puts the question first, then the ledger, then the policy; answers on big ledgers get worse | **Long documents first, question last**, check size with token counting, and pass only the ledger sections the commentary needs; more context brings context rot | "The window is big enough"; paste last year's ledger too "for context"; split every ledger into ten separate calls with no plan | D2 Context windows and token management | [Lesson 6, section 2.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 5 | The same policy and tool definitions go out on every call, and a timestamp sits at the very top | **Static content first, dynamic last, then prompt caching** on the policy and tools; move the timestamp and account ID below the breakpoint | Cache the ledger that changes every call; shorten the policy until quality drops; keep the timestamp on top "for traceability" | D2 Prompt reuse (caching); D4 Optimize token usage | [Lesson 6, section 2.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md); [Lesson 3, section 4.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 6 | The monthly run happens overnight and nobody waits on a single draft | **Message Batches** for the overnight run, stacked with caching; keep real-time calls only for an analyst's ad-hoc redo | Real-time calls for everything; batch the analyst's live redo too; run it by hand in a notebook | D4 Optimize latency and cost | [Lesson 3, section 4.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 7 | Deciding what "good" means before tuning | **Metrics set in advance**: numbers match the ledger (code-checked), every cause backed by a ledger line (groundedness), structure followed, plus cost and latency per account | Partner thumbs-up; average length; "sounds professional" | D4 Define evaluation metrics | [Lesson 3, section 4.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 8 | A model-graded rubric scores "causes are supported"; nobody knows if the grader is right | **Check the grader against human labels first**: partners score a sample, compare, fix the rubric, keep a held-out set you don't tune on | Trust the grader because it's a strong model; drop the rubric and read everything by hand; have the drafting model grade itself | D4 Evaluation datasets, mixed methodologies | [Lesson 3, section 4.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 9 | A draft blames a variance on a "one-off supplier refund" that isn't in the ledger | **Diagnose the layer**: was the needed data in the context? Then allow "cause not found in the ledger" and require every cause to cite a ledger line | Raise the temperature; a bigger model; "never make things up" in the prompt | D4 Diagnose system issues (hallucination); D2 Guardrails in prompts | [Lesson 3, section 4.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md); [Lesson 6, section 2.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 10 | A new model version is released and the team wants to switch next month | **Run the eval suite on the new version**, compare metric by metric, roll out to a slice of accounts first, and keep the current version pinned until it wins | Switch everything on release day; follow the newest alias automatically; judge by three sample drafts | D4 A/B testing and iterative improvement | [Lesson 3, section 4.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |

**Scoring:** 8 or more is a pass. The two principles: *spend more model power only where the eval
shows a gap (and try effort before switching models)*, and *put the right context in the right order,
reuse the fixed part, and prove every change on a fixed test set*.

Sources: [CCAR-P exam guide, Section 6 (community mirror of the official guide)](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1 content),
[choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model),
[effort](https://platform.claude.com/docs/en/build-with-claude/effort),
[prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
[batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing),
[develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) (all Tier 1).

</details>