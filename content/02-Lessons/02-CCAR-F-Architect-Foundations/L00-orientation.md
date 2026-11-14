# CCAR-F Lesson 0 — Orientation: how the Architect exam thinks

**Start with a situation you can picture:** [Read the application primer](architecture-studio/00-foundations.md), then [choose one complete case](architecture-studio/README.md). Each case grows when a concrete failure requires another layer. [Concept explanations](concept-course/README.md) help at the point you need them; they are not a separate prerequisite course. Reading mode needs no setup.

**New to building applications?** Start with the [architecture apprenticeship](architecture-studio/README.md): eight complete original application cases, beginning with a plain-language primer, then decisions, diagrams, lab experiments, simulations, questions and conversation prompts. These are additional teaching scenarios, not additional official exam families.


**Time:** 50 min · **Do first:** choose the [coached learning route](learning-journey.md); a diagnostic is optional for experienced learners

New to the Claude API? Read the [five-minute primer](#five-minute-primer-how-a-claude-app-works) first.

## Eight application scenarios you can study here

These are the **eight coached teaching applications available in this course**, not eight additional official exam families. Each includes setup guidance, plain-language and technical design choices, a drawing, a worked artifact, an exercise and transfer questions. Start with the [primer](architecture-studio/00-foundations.md), then follow the cases in order or choose the application you need.

| Case | Application lesson | Decisions you will learn |
|---|---|---|
| AS-01 | [Support action service](architecture-studio/AS-01-action-service.md) | Interpret a request, verify authority, guard the action and reconcile an uncertain result |
| AS-02 | [Document-intake pipeline](architecture-studio/AS-02-document-pipeline.md) | Choose extraction structure, preserve missing values and validate evidence rather than plausible output |
| AS-03 | [Grounded knowledge assistant](architecture-studio/AS-03-grounded-assistant.md) | Retrieve permitted evidence, distinguish MCP connection from context inclusion, preserve sources |
| AS-04 | [Research system](architecture-studio/AS-04-research-system.md) | Choose fixed, routed, parallel or adaptive work; delegate context and retain coverage |
| AS-05 | [Code-change assistant](architecture-studio/AS-05-code-change.md) | Explore unfamiliar code, select file tools, scope instructions and verify a change across callers |
| AS-06 | [Unattended CI reviewer](architecture-studio/AS-06-ci-review.md) | Separate invocation, permissions, structured output, evidence and independent review |
| AS-07 | [Immediate and deferred work queue](architecture-studio/AS-07-work-queue.md) | Choose synchronous, staged or batch processing; budget deadlines and recover individual failures |
| AS-08 | [Resumable case service](architecture-studio/AS-08-resumable-case.md) | Refresh saved facts and authority, reconcile prior effects and handle human-review limits |

[Full teaching-to-exam journey](learning-journey.md) → [eight-case course](architecture-studio/README.md) → [30 objective lessons](objectives/README.md) → [targeted decision variants](scenario-studio.md). The saved-guide six-family reference table below is a separate baseline, not the total of what this course teaches.

## What you're preparing for

- 60 questions in 120 minutes: "Multiple-choice and multiple-response items; each item states how many responses to select" (exam guide wording). Pass mark "Scaled score of 720 on a scale of 100–1,000" (exam guide wording). $125 fee (official exam guide v1.0 and the [Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1, checked 2026-10-07; it was $99 before June 30, 2026).
- Coworkers say it's the one exam where they needed all the time (field reports, tier F).
- The **saved July 2026 guide describes four scenarios drawn from six families**. Treat this as that guide's format, not an exhaustive catalog of possible application contexts; verify current rules with the provider.
- Five domains: **Agentic Architecture 27%**, Tool Design and MCP 18%, Claude Code 20%,
  Prompting and Structured Output 20%, Context and Reliability 15% (exam guide v1.0, Tier 1).
- **Pacing tip:** **Flag and review inside each scenario** before moving on (field report, tier F:
  going back to an earlier scenario may be hard). Keep a few minutes at the very end only if the
  exam lets you go back. The exam guide says nothing about navigation, so this is not an official
  rule. The "120 minutes ÷ 4 scenarios, about 15 items each" split is our own arithmetic from the
  guide (exam guide, exam format section), not something the guide states, and the real split may
  be uneven. Per-question pace: the [timing rule](deep-practice/tie-breaker-rules.md#timing-rule-exam-day)
  in the tie-breaker rules.
- **The day before:** revise what you already know; if you feel solid, skim the "Building with
  the Claude API" course (seen by several passers, field reports, tier F).

## Your scenario preparation goes beyond six stories

[Follow the full teaching-to-exam route](learning-journey.md): primer → coached application → objective and diagram → exercise → practice → repair → delayed transfer. The eight application cases, six family walkthroughs and 30 decision variants overlap; do not add them into a total of unique exam scenarios.

The table below describes the **six scenario families in the saved official blueprint**. Our preparation also includes **30 original decision variants across all 30 objectives**, six extended industry cases and targeted practice. They need to be part of your lessons, not hidden extra reading.

**Start here:** [Scenario learning studio](scenario-studio.md) → choose a decision → inspect its inline flow and mechanism → answer the matching question → repair → recall. Start with the studio's Finance, Legal and Marketing cases; then transfer the same decisions to Education and Government. These industry choices are supplemental teaching, not claimed exam weightings.

<a id="the-six-scenarios-and-the-lessons-that-cover-them"></a>
## Six saved-guide scenario families, not the limit of preparation

The saved July 2026 guide describes six workplace families. They are a preparation baseline, not proof that every future story uses the same application context. Each row is one saved-guide family; "Primary domains" lists the exam domains it tests most (1 Agentic architecture and orchestration, 2 Tool design and MCP integration, 3 Claude Code configuration and workflows, 4 Prompt engineering and structured output, 5 Context management and reliability), and "Lessons" says where to study it.

| # | Scenario | Primary domains | Lessons |
| --- | --- | --- | --- |
| 1 | Customer Support Resolution Agent (get_customer, lookup_order, process_refund, escalate_to_human; 80%+ first-contact resolution) | 1, 2, 5 | [Lesson 1, Agentic architecture and orchestration](L01-agentic-architecture-and-orchestration.md), [Lesson 2, Tool design and MCP integration](L02-tool-design-and-mcp-integration.md), [Lesson 5, Context management and reliability](L05-context-management-and-reliability.md) |
| 2 | Code Generation with Claude Code (slash commands, CLAUDE.md, plan mode) | 3, 5 | [Lesson 3, Claude Code configuration and workflows](L03-claude-code-configuration-and-workflows.md), [Lesson 5, Context management and reliability](L05-context-management-and-reliability.md) |
| 3 | Multi-Agent Research System (a coordinator plus search, analysis, synthesis and report subagents) | 1, 2, 5 | [Lesson 1, Agentic architecture and orchestration](L01-agentic-architecture-and-orchestration.md), [Lesson 2, Tool design and MCP integration](L02-tool-design-and-mcp-integration.md), [Lesson 5, Context management and reliability](L05-context-management-and-reliability.md) |
| 4 | Developer Productivity (Read, Write, Bash, Grep, Glob plus MCP) | 2, 3, 1 | [Lesson 2, Tool design and MCP integration](L02-tool-design-and-mcp-integration.md), [Lesson 3, Claude Code configuration and workflows](L03-claude-code-configuration-and-workflows.md), [Lesson 1, Agentic architecture and orchestration](L01-agentic-architecture-and-orchestration.md) |
| 5 | Claude Code for Continuous Integration (reviews, tests, few false positives) | 3, 4 | [Lesson 3, Claude Code configuration and workflows](L03-claude-code-configuration-and-workflows.md), [Lesson 4, Prompt engineering and structured output](L04-prompt-engineering-and-structured-output.md) |
| 6 | Structured Data Extraction (JSON schemas, validation and retry, downstream systems) | 4, 5 | [Lesson 4, Prompt engineering and structured output](L04-prompt-engineering-and-structured-output.md), [Lesson 5, Context management and reliability](L05-context-management-and-reliability.md) |

## Five-minute primer: how a Claude app works

New to the Claude API? Read this before the five rules below. Every later page builds on these few ideas.

- **One request, one reply.** Your code sends Claude a request: a system prompt (standing
  instructions), the conversation so far, and a list of tools Claude may use. Claude sends back one
  reply. The reply says why Claude stopped, in a field called `stop_reason`: `"end_turn"` means
  it's finished; `"tool_use"` means it wants a tool run.
- **The API keeps no memory.** "The Messages API is stateless, which means that you always send
  the full conversational history to the API" (Anthropic docs wording). Your application therefore manages coherent conversation state: preserve relevant messages, matched tool requests/results and critical facts, while budgeting or compacting older context deliberately. Stateless does not mean resend every raw byte forever.
- **A tool call: Claude asks, your code runs it.** You describe each tool to Claude with a name, a
  description and an input schema (the shape its inputs must have). Claude never runs your tools;
  your code does. (Server tools such as web search are different: Anthropic runs those.) Claude replies with a `tool_use` block naming the tool and its inputs. Your code runs it and sends back a `tool_result` with the
  answer, matched by `tool_use_id`. Then Claude carries on.
- **An agent is that loop, repeated.** Send, read `stop_reason`, run any tools, add the results to
  the history, send again, until an appropriate protocol outcome. This short example uses `end_turn` for normal model completion; truncation, refusal, paused/server-tool work and limits need separate handling. Model completion is not a transaction receipt. Lesson 1 teaches the loop.
- **One turn of the loop, worked through.** A customer asks "Where's order 123?"
  1. Your code sends the question plus a `lookup_order` tool.
  2. Claude replies with `stop_reason: "tool_use"` and a `tool_use` block: `lookup_order`, input
     `{"order_id": "123"}`.
  3. Your code runs `lookup_order("123")` and sends back a `tool_result` ("shipped, arrives
     Tuesday") with the same `tool_use_id`, plus the whole history.
  4. Claude replies with `stop_reason: "end_turn"`: "Your order has shipped and arrives Tuesday."
     Your code stops.
- **Three names you'll see on every page:**
  - **Claude Agent SDK:** a library that runs the agent loop for you, with subagents, hooks and
    permissions built in.
  - **Claude Code:** Anthropic's coding agent. It works in your project, reads files such as
    `CLAUDE.md`, and can run in CI with nobody at the keyboard. Lesson 3 covers its setup.
  - **MCP (Model Context Protocol):** an open standard for plugging tools and data into Claude
    through a small server. Lesson 2 covers it.

**Saved blueprint and current implementation.** Use the saved guide to locate objectives, and current primary documentation to validate runtime behavior. Solve the conditions actually stated in a question; do not memorize “always choose X.” Where terminology has changed, consult [documented differences](deep-practice/conditions-and-errors.md#exam-answer-vs-today), checking the supported interface rather than assuming a universal exam answer.

**Words used on every page:**

- **Message:** one user or assistant entry in history. A **turn** can span several model/tool exchanges; check the protocol rather than counting visible messages.
- **Token:** a small chunk of text (a word, part of a word or a character); size limits and prices
  are counted in tokens ([glossary](https://platform.claude.com/docs/en/about-claude/glossary),
  Tier 1).

- **Agent:** Claude running in a loop, calling tools until a job is done.
- **Tool:** a function you give Claude that it can ask to run (for example `get_customer`).
- **Coordinator / subagent:** the main agent that splits up the work / a helper agent it starts for
  one piece.
- **Hook:** your own code that runs automatically before or after a tool call, and can block or
  change it.
- **Prerequisite gate:** code that blocks a tool until an earlier step has succeeded (for example,
  no refund until the customer is verified).
- **Schema:** a description of the exact shape the output must have (which fields, which types).
- **Few-shot examples:** a few sample inputs with the right outputs, put in the prompt to show
  Claude what you want.
- **Context (window):** all the text Claude can work with in one request: the instructions, the history, the tool results, and the reply it is writing. It has a size limit.
- **Synchronous:** you send a request and wait for the answer right away.
- **CI:** the automatic system that builds and tests code on every change, with nobody at the
  keyboard.

Want to see the loop in code? [Deep practice 1, section 1.1](deep-practice/01-agentic-architecture-and-orchestration.md#11-agentic-loops)
has a short Python version.

## Five decision habits — apply the stated constraint

1. **Enforce mandatory rules at the executable boundary.** A prompt can guide interpretation; a pre-effect service guard checks identity, authority and policy before a mutation. Correct code still needs trustworthy data, tested predicates and coverage of all mutation paths. Post-action normalization cannot prevent a completed effect.
2. **Make judgment criteria explicit.** Relevant examples and clear severity/evidence criteria help when the task requires model judgment. A schema or hook is not a replacement for understanding what the judgment means.
3. **Separate shape, truth and completion.** Compatible strict schema constraints govern structure; source/business validation checks meaning; a correlated result or receipt establishes the relevant outcome. None implies the others.
4. **Scope capabilities by the task.** Give a specialist the smallest sufficient set of tools and a self-contained brief. The guide's small-versus-large tool-count example is an illustration, not a universal quota.
5. **Diagnose before increasing resources or retrying.** Protocol outcomes govern normal continuation/completion. Keep turn, cost and time safety budgets; exhausting one means interruption or handoff. More context, another model or a retry may help a diagnosed bottleneck, but cannot substitute for missing authority or evidence.

## Steps

1. [ ] Skim the [official exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications): sections 3–5 (the scenarios and the task statements).
2. [ ] Read the 12 official sample questions in section 9 of the official CCAR-F exam guide v1.0 *with their explanations*. The official
       practice exam was retired, so these are the official practice that's left. They're also in the
       practice tool under CCAR-F, source "Anthropic official exam guide".
3. [ ] **Optional baseline after the primer/coached case (or first if experienced):** the [claudecertificationguide.com diagnostic](https://claudecertificationguide.com/learn/diagnostic)
       (15 minutes, Tier 2), **or** a CCAR-F mock in the [practice tool](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html).
       Write your score down; you'll compare it after L05.
4. [ ] Start the labs early. Develop executed evidence for an agent loop and Claude Code configuration; reading and local fixtures alone do not establish that experience. See [`06-Labs/`](../../06-Labs/README.md), labs 02 and 03.
5. [ ] Bookmark [chart 0, which chart do I need?](deep-practice/decision-charts.md#0-which-chart-do-i-need).
       Use it whenever a question asks "which option?".

## Self-check

- Which domain is the biggest? *(Agentic Architecture, 27%)*
- Why does "add it to the system prompt" usually lose to "add a hook"? *(Choose a tested pre-effect executable check for a mandatory predicate; prompt guidance alone cannot enforce it. Check hook timing, failure handling and bypass paths.)*
- Which two scenarios mostly test Claude Code? *(2 and 5)*
- Claude's reply has `stop_reason: "tool_use"`. What does your code do next? *(Run the tool, send a
  `tool_result` with the matching `tool_use_id` plus the full history, and call again.)*

**Next:** [L01 Agentic Architecture](L01-agentic-architecture-and-orchestration.md)

## Sources

- [Official exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications)
  (Tier 1): format, time, pass mark, fee, scenarios, domain weights, sample questions.
- [Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) (Tier 1, checked 2026-10-07): the 720 pass mark, the $125 fee, and the practice exam retired in the move to Pearson. The older FAQ PDF is out of date on price and the practice exam.
  Use the 12 sample questions in section 9 of the official CCAR-F exam guide v1.0 instead.
- Primer (Tier 1, checked 2026-10-07): [working with messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
  (the stateless quote), [tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
  and [handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
  (Anthropic docs); [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) and
  [Claude Code overview](https://code.claude.com/docs/en/overview); [MCP](https://modelcontextprotocol.io);
  [context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) (the
  "Context (window)" entry).
  The glossary extends the one in the [decision charts](deep-practice/decision-charts.md).
- [claudecertificationguide.com](https://claudecertificationguide.com/learn/diagnostic) diagnostic
  (Tier 2), a third-party study aid.
- "Coworkers say": colleague debriefs, summed up on the [Insights](../../11-Lessons-Learned/INSIGHTS.md) page (tier F). They change emphasis,
  never facts.