# CCAR-F scenario walkthroughs

**Your learning route:** Start with [one application you can picture](../architecture-studio/00-foundations.md), then [choose a complete situation](../architecture-studio/README.md). Each taught layer shows a failure, asks a technical original exam-style question first, then explains the repair simply after you choose. Use this directory for its particular depth, not as another mandatory course. [Return to the complete learning journey](../learning-journey.md).


The saved July 2026 exam guide v1.0 describes selection of 4 of these 6 scenario families (Tier 1). This is the saved blueprint baseline, not an exhaustive inventory of possible application problems. Each page
walks one scenario from start to finish, the way you would design it for real:

- **The whole job in one chart:** the order of steps, the decisions and the failure paths.
- **Step by step:** what you decide at each step, the design rule (exam wording where it matters),
  and what can go wrong, with the exact signal or error code and what the design does about it.
- **Try the paper decisions:** 10 what-if questions with answers, written for this site. They are practice,
  not real exam questions.

**How to study one scenario (about 45 minutes the first time):** read the walkthrough (20 min), try
its 10 what-ifs with the answers closed (10 min), then run the matching simulation (15 min).

**Reading the charts.** Each box is a step. Each diamond is a decision. A green **PICK** box is the
right move. A pink dashed **NOT** box is the tempting trap.

| # | Scenario | Page | Then practise with |
|---|---|---|---|
| 1 | Customer Support Resolution Agent | [Walkthrough 1](WT-01-customer-support-agent.md) | [Simulation 2](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-02-customer-support-agent.md) |
| 2 | Code Generation with Claude Code | [Walkthrough 2](WT-02-code-generation-claude-code.md) | [Simulation 3](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-03-code-generation-claude-code.md) |
| 3 | Multi-Agent Research System | [Walkthrough 3](WT-03-multi-agent-research.md) | [Simulation 4](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-04-multi-agent-research.md) |
| 4 | Developer Productivity with Claude | [Walkthrough 4](WT-04-developer-productivity.md) | [Simulation 5](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-05-developer-productivity.md) |
| 5 | Claude Code for Continuous Integration | [Walkthrough 5](WT-05-claude-code-ci-cd.md) | [Simulation 6](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-06-claude-code-ci-cd.md) |
| 6 | Structured Data Extraction | [Walkthrough 6](WT-06-structured-data-extraction.md) | [Simulation 7](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-07-structured-data-extraction.md) |

**In real life (beyond the exam).** Each page ends with where this design shows up at work, what
production adds, an architect's checklist and two real-life what-ifs. Read it after the exam part.
Keep saved-blueprint terminology distinct from current runtime support. Do not infer an official answer for an unseen item or use obsolete runtime behavior in production.

**You're done with a scenario when** you can say, for each what-if, the decision and the failure move
with the answer still closed. Then open each one and fix any miss.

**One rule for every scenario.** The exam guide is from July 2026. Where today's product differs, each
page distinguishes the saved-guide teaching baseline from current runtime behavior. Verify the applicable exam guide before relying on that baseline. The full list is in
[exam answer vs today](../deep-practice/conditions-and-errors.md#exam-answer-vs-today).

## Sources

- Claude Certified Architect – Foundations exam guide v1.0 (Anthropic, July 2026): the six scenarios,
  the task statements each page cites, and the 12 sample questions that every practice question here
  was checked against so none repeats one (Tier 1).
- Anthropic docs (Tier 1): API errors, stop reasons, tool use, structured outputs, Message Batches, PDF
  support, Agent SDK, Claude Code hooks, settings, skills, CLI and MCP. Each is listed in the
  [conditions and errors link key](../deep-practice/conditions-and-errors.md#link-key). Checked 2026-10-07.

## Read these decisions conditionally

Batch requires independent eligible Messages requests, no dependent local iterative state, and an explicit deadline/expiry/recovery contract. Waiting overnight alone is insufficient; the 24-hour processing window does not guarantee successful completion. Tool choice selects a supported invocation mode; strict/schema enforcement constrains structure; application evidence checks establish meaning. A declared optional null need not trigger human review; required missing, ambiguous or conflicting evidence follows the stated review policy. These qualifications apply to gallery previews as well as full walkthroughs.