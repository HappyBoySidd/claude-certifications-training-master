# CCAR-P SIM-02 — Enterprise Knowledge Assistant (RAG)

**Primary domains:** 3 Integration, 2 Claude Models, Prompting & Context Engineering,
4 Evaluation, Testing & Optimization · **Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

You're the architect for an internal knowledge assistant at a global engineering firm. It answers
employee questions from a large mix of policy PDFs, project specs, wiki pages and rate-card
spreadsheets, and it must cite its sources. Some people ask broad policy questions; others paste
exact part codes. The index refreshes weekly, and some HR documents are confidential. The sponsor
wants answers that are **accurate, current and permission-aware**.


---

## The decisions (answer these before you open the key)

1. Fixed-size chunks cut policy clauses in half
2. The sponsor wants the most capable model at maximum effort for every question, but most questions are simple lookups
3. Exact part codes like "PX-4471" return the wrong documents
4. A developer proposes pasting every policy into one huge prompt on each request, "because the context window is big enough"
5. After the weekly refresh the assistant cites a superseded travel policy
6. How to measure quality
7. Building the eval set
8. When nothing relevant is retrieved the assistant makes up an answer
9. The long system prompt and tool definitions are paid for on every question
10. Confidential HR documents

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | Fixed-size chunks cut policy clauses in half | **Structure-aware chunking** on headings and sections, with some overlap and metadata (title, section, effective date, owner) | One chunk per whole document; make every chunk smaller; a bigger model to "fill the gaps" | D3 Design a RAG pipeline (chunking and indexing) | [Lesson 1, section 3.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |
| 2 | The sponsor wants the most capable model at maximum effort for every question, but most questions are simple lookups | **Choose by trade-off, proven on the eval set**: benchmark two tiers and effort levels on real questions, then route simple lookups to a lighter model or lower effort and keep the stronger setting for hard synthesis | The top model everywhere "to be safe"; the cheapest model everywhere; pick the model the team used last time | D2 Model selection by trade-off | [Lesson 6, section 2.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 3 | Exact part codes like "PX-4471" return the wrong documents | **Hybrid retrieval**: keyword search plus semantic search, then rerank | Semantic search only with a better embedding model; ask users to rephrase; raise top-k to 100 | D3 Retrieval matched to query pattern | [Lesson 1, section 3.6](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |
| 4 | A developer proposes pasting every policy into one huge prompt on each request, "because the context window is big enough" | **Curate the context**: retrieve only the relevant passages, put documents first and the question last, and check size with token counting; more context brings context rot and cost | "The window is big enough"; truncate the corpus to fit; summarize all policies into one page | D2 Context windows and token management; D3 Progressive discovery | [Lesson 6, section 2.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md); [Lesson 1, section 3.8](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |
| 5 | After the weekly refresh the assistant cites a superseded travel policy | **Fix the index**: version documents, remove superseded chunks, filter on effective date, and monitor index freshness | Tell the model to "prefer newer documents"; re-index by hand monthly; switch models | D3 RAG indexing; D4 Diagnose system issues | [Lesson 1, section 3.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md); [Lesson 3, section 4.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 6 | How to measure quality | **Measure retrieval and answers separately**: did the right passage come back, and is the answer faithful to it with correct citations; plus latency and cost | One thumbs-up rate; average answer length; how confident the answers sound | D4 Define evaluation metrics | [Lesson 3, section 4.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 7 | Building the eval set | **Mixed methods**: an expert-written golden set that includes hard cases (exact codes, superseded docs, questions with no answer), automated grading, plus a human-reviewed sample | Only model-generated questions; only easy questions; a one-time demo with the sponsor | D4 Evaluation datasets, mixed methodologies | [Lesson 3, section 4.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 8 | When nothing relevant is retrieved the assistant makes up an answer | **Allow and instruct "not found in the sources"**, and require every claim to cite a retrieved passage | Raise the temperature; a bigger model; "never be wrong" in the prompt | D2 System prompts and guardrails; D4 Diagnose hallucinations | [Lesson 6, section 2.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md); [Lesson 3, section 4.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 9 | The long system prompt and tool definitions are paid for on every question | **Prompt caching** on the stable prefix; retrieved passages go after the breakpoint | Shorten the instructions until quality drops; cache the retrieved passages; move instructions into each user turn | D2 Prompt reuse (caching); D4 Optimize token usage | [Lesson 6, section 2.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md); [Lesson 3, section 4.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 10 | Confidential HR documents | **Filter by the user's permissions at retrieval**, before any content reaches the model | Tell the model not to reveal HR content; trust users not to ask; a separate assistant nobody governs | D3 Authentication and authorization gaps | [Lesson 1, section 3.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |

**Scoring:** 8 or more is a pass. The two principles: *match retrieval to the data's shape and the
query's pattern, and put only what's needed in context*, and *measure retrieval and answer quality separately, and fix freshness and
access in the index, not the prompt*.

Sources: [CCAR-P exam guide, Section 6 (community mirror of the official guide)](https://anthropic-partners.skilljar.com/page/partner-certifications),
prompt caching,
reduce hallucinations.

</details>