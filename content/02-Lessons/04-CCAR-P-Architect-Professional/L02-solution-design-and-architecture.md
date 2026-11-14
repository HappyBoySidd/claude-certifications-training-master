# CCAR-P Lesson 2 — Solution Design and Architecture (17%, about 11 questions)

**Time:** 2 hours plus the paper exercise · **Practice:** [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Already covered in CCAR-F:** the agent loop, coordinator and subagents, the Task tool, and
hooks are in [CCAR-F L01](../02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md).
Here the question is *which* structure to build, and how to defend it to the business.

## 1.0 The big idea

Start from the business problem, not the model. Use the simplest pattern that works (one call, then a fixed workflow, and an agent only when the steps really can't be scripted), and tie every design to a result the business can measure.

## 1.1 From business problem to Claude solution

Start with the problem, not the model. Before drawing any boxes, write down:

- **The outcome and how it's measured:** "cut average handling time by X", not "use AI".
- **The users and the volume:** how many requests, how fast they must be answered, and what the
  peaks look like.
- **The constraints:** data sensitivity, regulation, latency SLA, budget, the systems of record.
- **The cost of a wrong answer.** This decides how much human review and verification you need.
- **Whether an LLM is even needed.** A fixed rule or a lookup table is cheaper and exact. Put
  Claude where language, judgment or unstructured input are involved.

## 1.2 End-to-end architecture: five boxes

```text
input → processing → output → (action) → feedback loop ─┐
  ↑                                                      │
  └──────── evals, prompt fixes, retrieval fixes ←───────┘
```

Every Claude solution has these same five parts. For each one, here is the decision you have to make:

| Box | Decide |
| --- | --- |
| **Input** | Channels, validation, redaction of personal data, identity of the caller |
| **Processing** | The pattern (1.3), the model per step, retrieval, tools |
| **Output** | Format (structured or prose), guardrails, confidence, citations |
| **Action** | What it writes to downstream, and where a human approves first |
| **Feedback loop** | Human overrides, user ratings and traces → the eval set → the next change |

A design with **no feedback loop** can't get better and can't prove it's working. On the exam
that's usually the missing piece.

## 1.3 Patterns: workflow, agent, augmented LLM

Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
separates **workflows**, where LLMs and tools follow predefined code paths, from **agents**, where
the LLM directs its own process and tool use. Its advice: find the simplest solution, and add
complexity only when it clearly improves results.

| Pattern | What it is | Use when |
| --- | --- | --- |
| **Augmented LLM** | One call with retrieval, tools and memory | The building block. Often enough on its own |
| **Prompt chaining** | Fixed steps, each using the output of the last, with checks in between | The task splits cleanly into steps you know ahead |
| **Routing** | Classify the input, send it to a specialized path or model | Distinct categories that need different handling, e.g. easy ones to a smaller model |
| **Parallelization** | Split into independent parts (sectioning), or run the same task several times (voting) | Speed, or more confidence from several views |
| **Orchestrator-workers** | A central LLM breaks the task down on the fly and delegates | You can't predict the subtasks in advance |
| **Evaluator-optimizer** | One call drafts, another critiques, and it loops | Clear evaluation criteria exist, and iterating measurably helps |
| **Agent** | The model runs a loop with tools until it's done | Open-ended problems where the number of steps can't be predicted |

**The ladder:** single call → augmented LLM → workflow → agent → multi-agent. Agents trade
latency and cost for flexibility, so each step up needs a reason you can name.

## 1.4 Multi-agent systems and orchestration

- Use several agents when the subtasks are **truly independent** (parallel research), need
  **isolated context** (so one doesn't flood another), or need **different tool permissions**.
- Don't use them just because the problem is big. Every agent adds tokens, latency, handoffs and
  new ways to fail.
- **The orchestrator owns** decomposition, routing, error handling and the final synthesis. Pass
  context between agents **explicitly and in structured form**.
- **Mix models:** a capable orchestrator with lower-cost workers is a documented pattern
  ([choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model),
  "Combine models").

## 1.5 Decomposition

- **By step:** a pipeline such as extract → validate → decide → draft.
- **By item:** the same step over each document or file, in parallel.
- **By expertise or permission:** a billing specialist and a technical specialist, each with its
  own tools.
- Hand anything that **must be exact** (maths, policy limits, access checks) to code, not to the
  model.
- **Watch for gaps:** if the pieces are too narrow, nothing covers the space between them.

## 1.6 Business value pillars

Executives buy results, not models, so for each kind of value bring the evidence they will accept:

| Pillar | Evidence the business will accept |
| --- | --- |
| **Efficiency** | Handling time, throughput, less manual touch |
| **Productivity** | Work done per person, time given back to experts |
| **Transformation** | A new capability or service that wasn't possible before |
| **Cost** | Cost per case, including tokens, infrastructure and human review |
| **Performance SLAs** | Latency, availability, and accuracy targets written into the agreement |

Tie each design choice to a pillar and a number. If a choice doesn't move any pillar, it's
probably extra complexity.

## Worked example

A retailer gets thousands of return requests a day by email. It wants each one classified,
checked against the return policy, answered, and refunds over a threshold sent to a person, with
replies inside an SLA. The team proposes five autonomous agents that talk freely to each other.
**Answer:** the steps are known ahead, so use a workflow. Route by request type (a smaller model
can classify). Chain extract → policy check → draft reply. Put the policy check and the refund
threshold **in code**. Add human approval above the threshold, and feed reviewer corrections back
into the eval set. The pillars are efficiency and cost, and it's measured by cost per return and
time to reply. The multi-agent version costs more, is harder to test and adds nothing the brief
asks for.

## Traps

- "Use a multi-agent system, because the process has many steps." Known steps call for a workflow.
- "Let the model apply the refund limit." Exact rules go in code.
- A design with no feedback loop or eval set.
- "Show value by the number of AI features shipped." Show it with a pillar and a metric.
- "Use Claude to look up the order status." A fixed lookup is a plain API call, which is cheaper and exact.

## Try it (30 min): a paper exercise

**The brief:** an insurer wants to triage incoming claims. Each claim has a form, photos and a
free-text description. Simple claims under a set amount should be approved the same day. Anything
suspicious goes to an investigator. Draw the **five boxes** (input, processing, output, action,
feedback loop). Name the pattern for each step, the model tier, where code enforces a rule, where
a human approves, and the one metric per value pillar you'd report. Then write two sentences on
why you didn't pick a fully autonomous agent.

## Done when

- [ ] You can draw the five boxes, feedback loop included, for any brief
- [ ] You can name the five workflow patterns from "Building effective agents" and when each fits
- [ ] You can defend workflow vs agent vs multi-agent in one sentence each
- [ ] You can link a design choice to a value pillar and a metric
- [ ] You scored 80% or more on [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L03 Evaluation, Testing and Optimization](L03-evaluation-testing-and-optimization.md)

Source: official CCAR-P exam guide v1.0, Domain 1 objectives; Anthropic, Building effective agents; docs linked above.