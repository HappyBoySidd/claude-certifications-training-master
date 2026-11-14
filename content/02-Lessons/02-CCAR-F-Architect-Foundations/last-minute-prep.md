# CCAR-F last-minute preparation checklist

**Updated: 2026-10-20.** [CCAR-F home](site:exams/ccar-f.html) · [Download the ready-made PDF](site:assets/downloads/ccar-f-last-minute-prep.pdf). For a fresh export of this HTML page, use your browser's Print → Save as PDF. Links in the downloadable PDF open the study site; download it before going offline.

## How to use this last-minute guide

- [ ] This is a project-authored recall aid mapped to all 30 saved CCAR-F task statements, not a replacement for the official guide, all 240 skill bullets or full study. No checklist score predicts an exam result.
- [ ] If you have 10 minutes: read the decision loop, 4Ds and traps. If you have 30-45 minutes: explain every objective check aloud and open any weak lesson. These are optional study suggestions, not official timing.
- [ ] Mark a check only when you can explain it without notes, choose between two plausible alternatives and handle one changed constraint. Uncertain? Open the linked objective, trace an example, then recall it again later.

## Decision loop and whole-system picture

- [ ] Outcome -> constraint -> mechanism -> evidence. What must happen? What condition decides the design? Which smallest sufficient supported mechanism meets it? What observation proves success?
- [ ] Trace: user interface -> authenticated backend -> Claude proposes a tool call -> runtime checks scope/arguments/prerequisites -> business API acts -> result with identity returns -> Claude explains observed evidence.
- [ ] Name each owner: identity provider authenticates; backend/services authorize; model interprets; runtime executes; business records prove outcome. MCP connects capabilities. A session store preserves context, not the truth of a payment.
- [ ] Add specialists, MCP, durable state, redaction, evaluation and monitoring because a requirement needs them. For a rising bill inspect request count, tokens, repeated context, fan-out and retries; compare latency and quality before simplifying. Caching and batch processing fit different constraints.
- [ ] Observe safely: correlate model/tool requests and downstream outcomes; track latency, errors and resource/cost usage without putting credentials or unrestricted sensitive data into logs. Evaluate representative failures and consequential errors, not aggregate accuracy alone.

## The 4Ds: supporting framework, not an extra exam domain

- [ ] Delegation: what should AI do, and what should a person or deterministic system own? Refund example: interpret the request; keep mandatory authorization in code.
- [ ] Description: specify intent, constraints, inputs and success. Refund example: order, currency, amount, policy and required receipt; vague wording leaves room for error.
- [ ] Discernment: check the output, process and evidence. Refund example: a timeout is not a receipt; a plausible explanation does not prove payment.
- [ ] Diligence: use AI responsibly with appropriate data handling, oversight and accountability. Refund example: scoped access, necessary data, review owner and appropriate records.
- [ ] These are the AI Fluency framework terms: Delegation, Description, Discernment, Diligence. Use them to support reasoning, not to infer exam weight or a new certification requirement.

## Agentic Architecture and Orchestration - 27%

- [ ] **[1.1: Design and implement agentic loops for autonomous task execution](objectives/objective-1.1.md)** — Agent loop: recognize tool_use versus completion; execute permitted calls in the runtime, return matching tool results and continue. A model message is not proof of business completion.
- [ ] **[1.2: Orchestrate multi-agent systems with coordinator-subagent patterns](objectives/objective-1.2.md)** — Coordinator: partition responsibilities, collect evidence and integrate partial outcomes. Prefer one agent with tools when that is sufficient.
- [ ] **[1.3: Configure subagent invocation, context passing, and spawning](objectives/objective-1.3.md)** — Subagent brief: supply the question, scope, relevant evidence, permissions and expected return. Isolated context does not automatically contain the parent conversation.
- [ ] **[1.4: Implement multi-step workflows with enforcement and handoff patterns](objectives/objective-1.4.md)** — Enforcement: put mandatory authorization, ordering and approval checks in executable controls; identify the handoff owner. A prompt reminder alone cannot enforce a prerequisite.
- [ ] **[1.5: Apply Agent SDK hooks for tool call interception and data normalization](objectives/objective-1.5.md)** — Hooks: distinguish tool interception/normalization from natural-language guidance. Check the applicable SDK hook contract and failure behavior; hooks do not replace downstream authorization.
- [ ] **[1.6: Design task decomposition strategies for complex workflows](objectives/objective-1.6.md)** — Decomposition: parallelize independent work; sequence dependencies. Explain why each boundary exists and how results are reconciled.
- [ ] **[1.7: Manage session state, resumption, and forking](objectives/objective-1.7.md)** — Session: distinguish resume from a fork and working conversation from durable business state. Re-authorize access and reconcile unresolved actions after interruption.

## Tool Design and MCP Integration - 18%

- [ ] **[2.1: Design effective tool interfaces with clear descriptions and boundaries](objectives/objective-2.1.md)** — Tool contract: name the operation precisely; define inputs, units, required fields, scope and outputs. Separate a read lookup from a consequential write.
- [ ] **[2.2: Implement structured error responses for MCP tools](objectives/objective-2.2.md)** — Tool error: return a structured category and recoverability signal with enough context to act. Separate invalid input, denied access, transient failure and not-found evidence.
- [ ] **[2.3: Distribute tools appropriately across agents and configure tool choice](objectives/objective-2.3.md)** — Tool allocation/choice: expose only relevant capabilities to each actor. Distinguish automatic selection from required/specific tool selection; forced selection does not validate arguments or authorize execution.
- [ ] **[2.4: Integrate MCP servers into Claude Code and agent workflows](objectives/objective-2.4.md)** — MCP: trace host, client, server, discovery, call and result. Protocol authentication does not grant access to every business record; server configuration and tool permissions remain explicit.
- [ ] **[2.5: Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively](objectives/objective-2.5.md)** — Built-in tools: choose Glob for paths, Grep for content, Read for inspection and Edit/Write for intended changes. Scope searches and verify mutations; use Bash when its execution is appropriate and permitted.

## Claude Code Configuration and Workflows - 20%

- [ ] **[3.1: Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization](objectives/objective-3.1.md)** — CLAUDE.md: distinguish shared project guidance from personal/local instructions and directory scope. Instructions are context, not an access-control mechanism.
- [ ] **[3.2: Create and configure custom slash commands and skills](objectives/objective-3.2.md)** — Commands/skills: choose reusable instructions and task-specific guidance rather than repeating a large prompt. State trigger, inputs and expected output; a skill is not a security boundary.
- [ ] **[3.3: Apply path-specific rules for conditional convention loading](objectives/objective-3.3.md)** — Path rules: attach conventions to the files they govern; avoid loading irrelevant rules everywhere. Verify which rule applies to the actual target path.
- [ ] **[3.4: Determine when to use plan mode vs direct execution](objectives/objective-3.4.md)** — Plan or execute: inspect and plan when scope, dependencies or risks are uncertain. Use a bounded direct edit for a clear task; planning itself proves no code was changed.
- [ ] **[3.5: Apply iterative refinement techniques for progressive improvement](objectives/objective-3.5.md)** — Iterate: use a concrete failure and acceptance criterion, make a bounded correction, then inspect/test the result. Repeated vague requests provide weak feedback.
- [ ] **[3.6: Integrate Claude Code into CI/CD pipelines](objectives/objective-3.6.md)** — CI/CD: use an explicit noninteractive task, scoped permissions, defined inputs/output and executable checks. Treat repository/PR text as untrusted input; a generated review does not prove tests passed.

## Prompt Engineering and Structured Output - 20%

- [ ] **[4.1: Design prompts with explicit criteria to improve precision and reduce false positives](objectives/objective-4.1.md)** — Prompt criteria: define what counts as a finding, required evidence and exclusions. Reduce false positives through precise criteria rather than simply asking for confidence.
- [ ] **[4.2: Apply few-shot prompting to improve output consistency and quality](objectives/objective-4.2.md)** — Few-shot examples: select representative cases and boundary failures; keep examples consistent with the desired task. Examples improve behavior but do not enforce authorization or guarantee truth.
- [ ] **[4.3: Enforce structured output using tool use and JSON schemas](objectives/objective-4.3.md)** — Structured output: distinguish a valid shape from correct facts and successful business action. Use the supported schema/tool mechanism for the workflow; validate semantic constraints separately.
- [ ] **[4.4: Implement validation, retry, and feedback loops for extraction quality](objectives/objective-4.4.md)** — Validation/retry: report exact failed fields and evidence, bound retries and preserve successful items. Retrying a write after timeout requires reconciling outcome/duplicate risk first.
- [ ] **[4.5: Design efficient batch processing strategies](objectives/objective-4.5.md)** — Batch: choose deferred processing for independent work without an interactive deadline. Correlate results by request identifier, not return order; account for partial failures.
- [ ] **[4.6: Design multi-instance and multi-pass review architectures](objectives/objective-4.6.md)** — Multi-pass review: separate generation and critique where useful; reconcile disagreements against evidence. Two agreeing model responses are not independent proof.

## Context Management and Reliability - 15%

- [ ] **[5.1: Manage conversation context to preserve critical information across long interactions](objectives/objective-5.1.md)** — Context: retain exact identifiers, amounts, decisions, sources and unresolved work. Summaries can lose critical details; durable records remain separate from model context.
- [ ] **[5.2: Design effective escalation and ambiguity resolution patterns](objectives/objective-5.2.md)** — Ambiguity/escalation: ask a focused question when missing information changes the action. Escalate consequential uncertainty with evidence and a named next owner.
- [ ] **[5.3: Implement error propagation strategies across multi-agent systems](objectives/objective-5.3.md)** — Failure propagation: preserve valid partial results, identify missing branches and report unresolved outcomes. Do not silently substitute guesses for a failed specialist.
- [ ] **[5.4: Manage context effectively in large codebase exploration](objectives/objective-5.4.md)** — Large codebase: narrow by paths/content, inspect relevant dependencies and preserve a compact evidence trail. Dumping the whole repository wastes context and obscures the deciding code.
- [ ] **[5.5: Design human review workflows and confidence calibration](objectives/objective-5.5.md)** — Human review: calibrate against labeled outcomes and consequence severity. A model confidence score alone is not a validated probability or sufficient permission to act.
- [ ] **[5.6: Preserve information provenance and handle uncertainty in multi-source synthesis](objectives/objective-5.6.md)** — Provenance: keep source identity, time, scope and conflicts through synthesis. Distinguish observed fact, inference and missing evidence; a fluent answer does not settle contradictory sources.

## Final traps and exam approach

- [ ] Authorization is not authentication. Schema validity is not factual correctness. A proposed action is not an executed action. Execution is not proven success without the right evidence.
- [ ] Do not assume more agents, larger context, retries, MCP or a stronger model always improve the design. Identify the actual failure before choosing a mechanism.
- [ ] Read how many answers the item requests. Identify the requested outcome and hard constraint, reject options that violate them, and avoid adding requirements that are not in the scenario.
- [ ] For a stalled decision, name why the closest alternative fails. Mark and revisit if the exam interface permits. Manage time using the actual exam instructions; do not infer readiness from memorized mock answers.
- [ ] Before exam day: check current official registration, identification, delivery and system-test instructions. Course completion is not the proctored credential. Do not experiment with a new technical setup immediately before the exam.

## Sources, repair links and readiness limits

- [ ] Task labels and domain weights use the project's saved official CCAR-F guide mapping. Check current official guidance for changes. This short guide does not reproduce all knowledge/skill bullets.
- [ ] Known coverage limit: 196 of 240 mapped skill bullets still lack a dedicated reviewed diagnostic. This guide does not close that gap or guarantee a pass.
- [ ] Return to concept coaching, full objective lessons, simulations, labs, targeted practice and flashcards through the CCAR-F home page. HTML checklist ticks stay in this browser independently of existing objective and practice progress.

[Worked 4Ds refund exercise](concept-course/01-application-and-agent-loop.md#four-checks-before-delegating) · [Whole-bank synthesis](concept-course/06-putting-it-together.md) · [Full learning journey](learning-journey.md) · [Official certification](https://anthropic-partners.skilljar.com/page/partner-certifications) · [Official AI Fluency framework](https://academy.claude.com/courses/ai-fluency-framework-foundations)