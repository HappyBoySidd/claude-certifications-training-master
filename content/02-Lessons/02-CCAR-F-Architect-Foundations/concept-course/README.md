# Architecture concept coaching — understand before choosing

**Your learning route:** Start with [one application you can picture](../architecture-studio/00-foundations.md), then [choose a complete situation](../architecture-studio/README.md). Each taught layer shows a failure, asks a technical original exam-style question first, then explains the repair simply after you choose. Use this directory for its particular depth, not as another mandatory course. [Return to the complete learning journey](../learning-journey.md).


Start with a familiar screen and follow its data. Then learn the technical names for the choices you make. This course is an original teaching bridge to the existing CCAR-F objectives, not a new exam blueprint or a promise of every possible exam scenario.

**Reading setup:** none. No account, API key, installation or paid credits are required. Read the traces and answer aloud or on paper. Any runnable lab linked below has its own prerequisites; a teaching contract here is not executable SDK code.

## Your first pass

| Lesson | Recognizable application | Decision you will learn to explain |
|---|---|---|
| [1. Application, loop and boundaries](01-application-and-agent-loop.md) | Refund request on a support case | Who interprets, who authorizes, who executes, and when the loop stops |
| [2. Tool contracts and MCP](02-tools-and-mcp.md) | Find an order and propose its refund | Which tool fits; what it promises; how failures travel |
| [3. Claude Code and CI](03-code-workflows-and-ci.md) | Change a refund rule in a code repository | How to investigate, scope instructions, implement and independently review |
| [4. Prompts, extraction and batches](04-prompts-extraction-and-batch.md) | Read supplier invoices into an accounts-payable queue | How to specify, validate, repair and schedule work |
| [5. Context, reliability and evidence](05-context-reliability-and-evaluation.md) | Resume a disputed-refund investigation | What must survive, what can fail, and what proves a claim |
| [6. Put it together](06-putting-it-together.md) | Bank balance and transaction assistant | Why each architecture component earns its place, and how to diagnose wrong answers |

Each lesson follows **scene → trace → choices → changed constraint → recall → application**. Read one lesson, close it, explain its trace aloud, then reveal the decision answers. If you cannot explain why the alternative loses, use the linked objective before attempting timed practice.

## Keep the learning arc connected

Use [application anatomy](../architecture-studio/00-foundations.md) when a component is unfamiliar. Use the [objective map](../objectives/README.md) for precise task coverage and the [decision atlas](../decision-atlas.md) for more changed constraints. The [architecture cases](../architecture-studio/README.md) combine concepts into complete applications. The [SIM collection](../../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) tests larger decisions; [Lab 08](../../../06-Labs/08-CCAR-F-architecture-decisions/README.md) offers paper-first practice and an optional local exercise. Finish a study session with [flashcards](../FLASHCARDS.md), then return to the concept behind any missed answer.

The examples use fictional records. Finance, Legal and Marketing are transfer contexts, not asserted official industry weightings. Reading this course does not replace the 30 objective lessons or validate an exam-readiness score by itself.

## Pair a local lesson with an official course

Use [the official-course companion on the CCAR-F hub](../../../01-Curriculum/02-Architect-Track/CCAR-F.md#choose-official-courses-by-the-decision-you-need-to-learn) when you want a second explanation or actual implementation work. It identifies core companions, optional on-ramps and enrichment, prerequisites and the concrete decision to practise afterward. Our reading route still requires no installation. A completion badge is separate from certification and scenario readiness.

## How the supplied series connects to your existing objectives

This is a topic-navigation map of the supplied learning resources, not copied course material or independent verification of each video's claims. The six coaching lessons connect these themes; use the existing objective lesson for detailed mechanisms and exercises.

| Supplied resource theme | Coaching stop | Exact depth lesson |
|---|---|---|
| 1. Agentic loop and termination | Lesson 1 | [1.1](../objectives/objective-1.1.md) |
| 2. Coordinator and specialists | Lessons 1, 5 | [1.2](../objectives/objective-1.2.md) |
| 3. Isolated context, sources and sessions | Lesson 5 | [1.3](../objectives/objective-1.3.md), [1.7](../objectives/objective-1.7.md) |
| 4. Integrated multi-agent example | Lessons 1, 5 | [1.2](../objectives/objective-1.2.md), [1.6](../objectives/objective-1.6.md) |
| 5. Hooks, gates and decomposition | Lesson 1 | [1.4](../objectives/objective-1.4.md), [1.5](../objectives/objective-1.5.md), [1.6](../objectives/objective-1.6.md) |
| 6. Tool descriptions and routing | Lesson 2 | [2.1](../objectives/objective-2.1.md) |
| 7. Errors, tool scope and choice | Lesson 2 | [2.2](../objectives/objective-2.2.md), [2.3](../objectives/objective-2.3.md) |
| 8. MCP foundations | Lesson 2 | [2.4](../objectives/objective-2.4.md) |
| 9. Built-in code tools | Lesson 3 | [2.5](../objectives/objective-2.5.md) |
| 10. Instructions and conditional rules | Lesson 3 | [3.1](../objectives/objective-3.1.md), [3.3](../objectives/objective-3.3.md) |
| 11. Commands and skills | Lesson 3 | [3.2](../objectives/objective-3.2.md) |
| 12. Planning and iterative execution | Lesson 3 | [3.4](../objectives/objective-3.4.md), [3.5](../objectives/objective-3.5.md) |
| 13. CI execution and reviews | Lesson 3 | [3.6](../objectives/objective-3.6.md) |
| 14. Review precision and extraction criteria | Lessons 3, 4 | [4.1](../objectives/objective-4.1.md) |
| 15. Few-shot boundary examples | Lesson 4 | [4.2](../objectives/objective-4.2.md) |
| 16. Schema, validation and repair | Lesson 4 | [4.3](../objectives/objective-4.3.md), [4.4](../objectives/objective-4.4.md) |
| 17. Batch and multi-pass review | Lessons 3, 4 | [4.5](../objectives/objective-4.5.md), [4.6](../objectives/objective-4.6.md) |
| 18. Context preservation and escalation | Lesson 5 | [5.1](../objectives/objective-5.1.md), [5.2](../objectives/objective-5.2.md) |
| 19. Error propagation and recovery | Lesson 5 | [5.3](../objectives/objective-5.3.md), [5.4](../objectives/objective-5.4.md) |
| 20. Evaluation and provenance | Lesson 5 | [5.5](../objectives/objective-5.5.md), [5.6](../objectives/objective-5.6.md) |
| Bonus: exam walkthrough | Coaching changed-constraint exercises | [Decision conversation](../decision-conversation.md), [full mock SIM](../../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-01-full-mock.md) |
| Bonus: certification-path comparison | Orientation context | [Orientation](../L00-orientation.md) |
| 23. Enterprise architecture: how the parts come together | [Lesson 6](06-putting-it-together.md) | [1.1](../objectives/objective-1.1.md), [1.2](../objectives/objective-1.2.md), [2.4](../objectives/objective-2.4.md), [5.1](../objectives/objective-5.1.md), [5.6](../objectives/objective-5.6.md) |
| 24. MCP before/after architecture and message lifecycle | [Lesson 2: before and after MCP](02-tools-and-mcp.md#mcp-before-after) | [2.4](../objectives/objective-2.4.md), [2.1](../objectives/objective-2.1.md), [2.2](../objectives/objective-2.2.md) |

Certification-path commentary is background, not a new technical objective. Current exam requirements and format must be read from the official guide rather than inferred from a creator's announcement. These lessons deliberately retain nuanced conditions instead of universal shortcuts.

## Compare close technical mechanisms

Use the [mechanism clinic](../mechanism-clinic.md) after concept coaching to distinguish output guarantees, permissions, tool ordering, MCP capabilities and recovery. It includes eight original checks with changed constraints and exact objective repair links.