# CCAR-P SIM-04 — Multi-Agent Operations Platform

**Primary domains:** 1 Solution Design & Architecture, 2 Claude Models, Prompting & Context
Engineering, 4 Evaluation, Testing & Optimization, 3 Integration · **Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

A logistics company wants Claude across operations. There are three needs: sort inbound
shipment-exception emails into fixed categories within five minutes, investigate complex delayed
shipments across tracking, warehouse and carrier systems, and produce a weekly operations summary.
Leadership's first idea is "one big autonomous agent with access to everything". The CFO wants to
know what the business gets for the spend.


---

## The decisions (answer these before you open the key)

1. One big agent, or something else?
2. Structure of the delay investigation
3. Each worker has a hand-written prompt; a fix to the output rules has to be copied into six places and they keep drifting apart
4. Workers duplicate each other and return rambling prose
5. The CFO asks what the platform is worth
6. Email sorting must meet its SLA at peak; investigations can take longer
7. Thousands of runs a day, occasional wrong routing, no idea why
8. A new routing prompt looks better on ten examples
9. The top model runs every worker and the bill is high
10. Ops staff fix misrouted emails by hand every day

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | One big agent, or something else? | **Pick a pattern per need**: an augmented LLM call with structured output for email sorting, a fixed workflow for the weekly summary, an agent only for open-ended investigations | One agent for everything; agents for all three "for consistency"; no AI for the investigations | D1 Select architectural patterns | [Lesson 2, section 1.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L02-solution-design-and-architecture.md) |
| 2 | Structure of the delay investigation | **Orchestrator-workers**: an orchestrator plans and delegates to one worker per system, in parallel, each holding only its own system's tools, then combines the findings | One agent holding every tool; a fixed chain that always runs every system in order; every worker gets all tools "for flexibility" | D1 Multi-agent systems and orchestration; D3 Capability bloat | [Lesson 2, section 1.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L02-solution-design-and-architecture.md); [Lesson 1, section 3.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |
| 3 | Each worker has a hand-written prompt; a fix to the output rules has to be copied into six places and they keep drifting apart | **One versioned prompt template**: shared blocks (role, output rules, untrusted-content policy) in XML-tagged sections, per-worker variables, and a regression run before any change ships | Keep separate prompts and review them monthly; one giant prompt for all workers; let each worker rewrite its own prompt | D2 System prompts and templates | [Lesson 6, section 2.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md) |
| 4 | Workers duplicate each other and return rambling prose | **Explicit task specs**: objective, scope boundary, output format and when to stop | A longer orchestrator prompt; more workers; a bigger model for the orchestrator | D1 Decomposition techniques | [Lesson 2, section 1.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L02-solution-design-and-architecture.md) |
| 5 | The CFO asks what the platform is worth | **Tie each use case to a value pillar with a baseline measured before launch**: handling time (efficiency), cost per case (cost), five-minute routing (performance SLA) | A "transformation" story with no numbers; token spend alone; count of agents deployed | D1 Align to business value pillars | [Lesson 2, section 1.6](../../02-Lessons/04-CCAR-P-Architect-Professional/L02-solution-design-and-architecture.md) |
| 6 | Email sorting must meet its SLA at peak; investigations can take longer | **Set SLAs per path**, and choose model and settings per path using eval results on accuracy against latency | The most capable model everywhere; one SLA for the whole platform; drop accuracy checks to hit latency | D3 Accuracy-latency trade-offs | [Lesson 1, section 3.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md) |
| 7 | Thousands of runs a day, occasional wrong routing, no idea why | **Tracing per run**: every step, tool call, token count, latency and error tied to one trace ID, with dashboards, alerts and sampled quality review | Log only final outputs; read transcripts by hand; wait for complaints | D3 Observability at scale; D4 Monitor with logging | [Lesson 1, section 3.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L01-integration.md); [Lesson 3, section 4.6](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 8 | A new routing prompt looks better on ten examples | **Offline eval first, then an A/B test**: split traffic, success metrics set in advance, one change at a time, a rollback plan | Ship to everyone because it looked good; change the prompt and the model together; judge by anecdotes | D4 A/B testing and iterative improvement | [Lesson 3, section 4.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 9 | The top model runs every worker and the bill is high | **Match the model to the role**: lighter models or lower effort for extraction workers, stronger ones where reasoning matters, confirmed by eval | Downgrade everything at once; keep the top model everywhere; cap tokens until answers truncate | D2 Model selection; D4 Cost-performance trade-offs | [Lesson 6, section 2.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L06-models-prompting-and-context.md); [Lesson 3, section 4.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 10 | Ops staff fix misrouted emails by hand every day | **Close the feedback loop**: capture corrections into the eval set and use them to drive the next prompt iteration | Ignore corrections; retrain nothing; ask staff to email the team occasionally | D1 End-to-end architecture with feedback loops | [Lesson 2, section 1.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L02-solution-design-and-architecture.md) |

**Scoring:** 8 or more is a pass. The two principles: *use the simplest pattern that meets each
need, with agents only for open-ended work*, and *change one thing at a time and measure it (eval,
then A/B) with traces you can read*.

Sources: [CCAR-P exam guide, Section 6 (community mirror of the official guide)](https://anthropic-partners.skilljar.com/page/partner-certifications),
choosing a model,
[prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

</details>