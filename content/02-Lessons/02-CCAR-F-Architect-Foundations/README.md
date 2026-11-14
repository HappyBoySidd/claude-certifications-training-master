# CCAR-F lessons (Claude Certified Architect: Foundations)

**Your learning route:** Start with [one application you can picture](architecture-studio/00-foundations.md), then [choose a complete situation](architecture-studio/README.md). Each taught layer shows a failure, asks a technical original exam-style question first, then explains the repair simply after you choose. Use this directory for its particular depth, not as another mandatory course. [Return to the complete learning journey](learning-journey.md).


**Build the concepts in order:** [Six connected coaching lessons](concept-course/README.md) explain the application, data flow and technical alternatives before deeper lessons and practice. Reading mode needs no setup.

**New to building applications?** Start with the [architecture apprenticeship](architecture-studio/README.md): eight complete original application cases, beginning with a plain-language primer, then decisions, diagrams, lab experiments, simulations, questions and conversation prompts. These are additional teaching scenarios, not additional official exam families.

One lesson per official domain, organized by the official task statements (1.1–5.6) in the
[v1.0 exam guide](https://anthropic-partners.skilljar.com/page/partner-certifications).

| Step | # | Lesson | Weight | Time | Targeted practice |
| --- | --- | --- | --- | --- | --- |
| 1 | L00 | [Orientation, a five-minute Claude API primer, the 6 scenarios and the 5 rules](L00-orientation.md) | none | 50 min | diagnostic |
| 2 | L01 | [Agentic Architecture and Orchestration](L01-agentic-architecture-and-orchestration.md) | **27%** | 2–3 h | [CCAR-F practice — choose Domain 1](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) |
| 3 | L04 | [Prompt Engineering and Structured Output](L04-prompt-engineering-and-structured-output.md) | 20% | 2 h | [CCAR-F practice — choose Domain 4](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) |
| 4 | L03 | [Claude Code Configuration and Workflows](L03-claude-code-configuration-and-workflows.md) | 20% | 2 h | [CCAR-F practice — choose Domain 3](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) |
| 5 | L02 | [Tool Design and MCP Integration](L02-tool-design-and-mcp-integration.md) | 18% | 2 h | [CCAR-F practice — choose Domain 2](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) |
| 6 | L05 | [Context Management and Reliability](L05-context-management-and-reliability.md) | 15% | 90 min | [CCAR-F practice — choose Domain 5](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) |

**Default path:** L00 plus the five domain lessons, in the Step order; objective lessons to fill gaps; audio for review.

> **Already build with the Claude API and Claude Code? (about 12–15 hours over 2 weeks, by the page time estimates.)** Do the
> [diagnostic in Lesson 0](L00-orientation.md#steps) →
> read the [tie-breaker rules](deep-practice/tie-breaker-rules.md) and the
> [conditions sheet](deep-practice/conditions-and-errors.md) → do the [hard drills](HARD-DRILLS.md) cold →
> run SIM-02 to SIM-07 → open lessons and deep practice only for the task statements you missed →
> SIM-01 mocks. Watch the "What changed since" boxes: they flag where the exam answer and today's
> product differ ([exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today)).

**Order:** L00 → L01 → L04 → L03 → L02 → L05, with
[lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) after L04 and
[lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) after L02. Read each lesson's
[deep practice page](deep-practice/README.md) right after the lesson. Then do the
[simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md): 6 scenarios plus the
full mocks ([SIM-01](../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-01-full-mock.md)).

Anthropic no longer offers an official practice exam: it "was retired in the move to Pearson"
([Partner Academy certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1).
The only official practice questions are the 12 sample questions in section 9 of the CCAR-F exam
guide v1.0 (Anthropic, Tier 1) and the quizzes in the Anthropic Academy courses on the
[CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
(Tier 1). SIM-01 run E walks you through the sample questions.

**Build as you learn.** [Lab 02: agent loop and extraction](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md), [Lab 03: MCP and Claude Code](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) and [Lab 08: local architecture decisions](../../06-Labs/08-CCAR-F-architecture-decisions/README.md) provide complementary exercises. Use the [objective lessons](objectives/README.md) and [full learning journey](learning-journey.md) to identify and study remaining coverage.

## Learn through scenarios and decisions

Open the [Scenario learning studio](scenario-studio.md) for all 30 worked decision variants, matching questions, drawings, recall and five industry transfer exercises. Keep the six blueprint scenarios as your foundation, then change constraints rather than memorizing their wording.

## Learn by objective

Use the [30-objective curriculum](../../01-Curriculum/02-Architect-Track/CCAR-F-objective-curriculum.md) and [objective lessons](objectives/README.md) for full knowledge-and-skills coverage, then the [industry transfer cases](objectives/INDUSTRY-CASES.md).




## Practice changed constraints

Use the [decision atlas](decision-atlas.md) to compare the base choice, changed constraint and failure path. Finance changes approval, monetary consistency and source-age risk; Legal changes evidence attribution, privilege/access and ambiguity; Marketing changes consent, segment criteria and false-positive cost. These are synthetic transfer contexts, not official industry weightings. Keep the underlying Claude mechanism explicit.