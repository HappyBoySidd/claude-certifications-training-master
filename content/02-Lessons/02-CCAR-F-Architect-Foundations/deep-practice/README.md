# CCAR-F deep practice

**Your learning route:** Start with [one application you can picture](../architecture-studio/00-foundations.md), then [choose a complete situation](../architecture-studio/README.md). Each taught layer shows a failure, asks a technical original exam-style question first, then explains the repair simply after you choose. Use this directory for its particular depth, not as another mandatory course. [Return to the complete learning journey](../learning-journey.md).


**Picture the application:** You have an assistant that receives a customer request, calls a service and returns an explanation, but one step behaves incorrectly. Use this reference area to trace that specific input and expected outcome into the relevant mechanism. Choose a page for the problem instead of memorizing every table at once.

This section goes deeper than the five CCAR-F lessons. There is one page per exam domain. Each page
takes the domain one task statement (TS) at a time, in number order: the core idea, how it works under
the hood, the look-alike wrong answers, a worked example and a one-line exam reflex. Five extra pages
cut across all domains: the exact signals and error codes, rules for picking between close answers,
step-by-step code walk-throughs of the systems the exam scenarios describe, decision charts for the
"which option?" moments, and sequence diagrams that show who talks to whom, in order.

| Page | What it covers | Goes with | Time |
| --- | --- | --- | --- |
| [Deep practice 1](01-agentic-architecture-and-orchestration.md) | Agentic architecture and orchestration (1.1–1.7), plus escalation (5.2) | [Lesson 1](../L01-agentic-architecture-and-orchestration.md) | about 90 min |
| [Deep practice 2](02-tool-design-and-mcp-integration.md) | Tool design and MCP integration (2.1–2.5) | [Lesson 2](../L02-tool-design-and-mcp-integration.md) | about 60 min |
| [Deep practice 3](03-claude-code-configuration-and-workflows.md) | Claude Code configuration and workflows (3.1–3.6), plus the hook halves of 1.4 and 1.5 | [Lesson 3](../L03-claude-code-configuration-and-workflows.md) | about 90 min |
| [Deep practice 4](04-prompt-engineering-and-structured-output.md) | Prompt engineering and structured output (4.1–4.6), plus `tool_choice` (2.3) and human review (5.5) | [Lesson 4](../L04-prompt-engineering-and-structured-output.md) | about 90 min |
| [Deep practice 5](05-context-management-and-reliability.md) | Context management and reliability (5.1, 5.3, 5.4, 5.6), plus what a resumed session knows (1.7) | [Lesson 5](../L05-context-management-and-reliability.md) | about 45 min |
| [Conditions and errors](conditions-and-errors.md) | The exact signals: `stop_reason`, API errors, Batch limits, MCP errors, hook exit codes, settings and `CLAUDE.md` rules | All domains | about 60 min |
| [Tie-breaker rules](tie-breaker-rules.md) | How to pick the best answer when three of four options would work, plus a timing rule | All domains | about 15 min |
| [Code-level flows](code-level-flows.md) | Eight systems walked through step by step in code, from an extraction pipeline to CI/CD | All domains | about 2 hours |
| [Decision charts](decision-charts.md) | Decision charts: which option fits? One-look charts for the "which option?" moments, with a map that sends you to the right one | All domains | about 45 min |
| [Sequence diagrams](sequence-diagrams.md) | Six systems drawn as who talks to whom, in order, plus two decision trees (built-in tools, noisy review comments) | All domains | about 30 min |

Times are estimates for a first careful read.

**Study order:** L00 → L01 → L04 → L03 → L02 → L05, and read each lesson's deep practice page right
after it. Use the five cross-domain pages alongside, and read the tie-breaker rules before your first
mock. Then move on to the [scenario simulations](../../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md).
When a page shows both an exam answer and a today answer, the
[exam answer vs today](conditions-and-errors.md#exam-answer-vs-today) table says which one to give
on exam day.

**Already build with the Claude API and Claude Code?** Start with the tie-breaker rules and the
conditions sheet, then open the domain pages only for the task statements you miss; the full fast
path is on the [lessons page](../README.md).