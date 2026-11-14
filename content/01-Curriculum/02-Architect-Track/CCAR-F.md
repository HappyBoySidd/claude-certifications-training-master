# Architect track, level 1 · CCAR-F Claude Certified Architect: Foundations

**Exam:** 60 questions in 120 minutes · multiple-choice and multiple-response ("each item states how many responses to select", exam guide wording) · 4 of 6 scenarios drawn at random · pass mark "Scaled score of 720 on a scale of 100–1,000" (exam guide wording) · $125 list · 5 domains. Source: [official exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications) and the [Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) (Tier 1, checked 2026-10-07). The older FAQ PDF is out of date on price ($99) and the practice exam.
**Study time:** the earlier 20–25-hour estimate covers the core summary route, not the expanded apprenticeship/objective/deep-practice route. The eight application cases suggest 45–75 minutes each plus primer and labs; total time depends on prior experience and repair needs.
**Already build with the Claude API and Claude Code?** Use the [fast path](../../02-Lessons/02-CCAR-F-Architect-Foundations/README.md) (about 12–15 hours) instead of the checklist order.
**What others learned:** [Insights](../../11-Lessons-Learned/INSIGHTS.md#ccar-f-architect-foundations)

**Who it's for:** people who design Claude solutions end to end. It's the first level of the
Architect track, followed by [CCAR-P](CCAR-P.md). Internal Slack calls it CCA-F (tier F).

## Choose your starting route

**Recommended concept-first route:** [Six connected coaching lessons](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/README.md). Start with an application, follow its data and compare technical choices before the linked objective depth and practice.


**New to application architecture:** [Full learning journey](../../02-Lessons/02-CCAR-F-Architect-Foundations/learning-journey.md) → primer → coached application cases → related objectives/diagrams → paper/local exercises → formative checks → delayed transfer. No diagnostic is required before teaching. **Experienced:** use a diagnostic to target gaps, then return to explanation and transfer practice.

The checklist below retains the legacy core items; row order is not a requirement to book before learning. Its percent targets are optional project study heuristics, not validated readiness thresholds, official scaled scores or a schedule to sit the exam. Add the apprenticeship and Lab08 through the full journey before treating the route as complete.

## Choose official courses by the decision you need to learn

**Keep this page as your home base.** Our [concept coaching](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/README.md) teaches the picture first. Use an official companion when its explanation or hands-on work helps a specific gap, then return to the linked local lesson. You do not need to finish the whole Academy catalog before practising here.

The priorities below are this project's learning recommendations, **not official course prerequisites, exam percentages or a newly verified required-prep list**. Course titles and descriptions were checked against the linked official pages on 2026-10-20. The older prep-list citation below remains dated evidence; confirm current certification guidance at the [official certification page](https://anthropic-partners.skilljar.com/page/partner-certifications). Catalogs, durations and access requirements change, so use each course's current page rather than a video's catalog total or time estimate.

<div class="course-companion">

| Take this when… | Official companion and setup boundary | Bring this decision back here |
|---|---|---|
| You understand the refund story but cannot trace what the model and application send each other. | **Core companion:** [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api). Follow its setup instructions before running API exercises; reading our explanations needs no key. | Trace request → proposed tool call → runtime check → tool result → answer in [concept 1](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/01-application-and-agent-loop.md). Explain why a completed model turn does not prove a refund. |
| MCP still feels like a product name rather than a connection and message flow. | **Core companion:** [Introduction to Model Context Protocol](https://academy.claude.com/courses/introduction-to-model-context-protocol). Its implementation work expects basic Python, async/await and API concepts; use our reading trace first if those are unfamiliar. | Draw host/client/server and trace discovery, call, result and model context in [concept 2's before/after example](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/02-tools-and-mcp.md#mcp-before-after). Then choose direct API or MCP and defend the tradeoff. |
| You can use Claude Code for one task but cannot explain team configuration or unattended verification. | **Core companion:** [Claude Code in action](https://academy.claude.com/courses/claude-code-in-action). It expects prior single-prompt use and Git/command-line familiarity. Use the beginner course below first when needed. | Separate guidance, permissions, hooks and observed test evidence in [concept 3](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/03-code-workflows-and-ci.md). Apply them to the [CI review packet](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.6.md#supplied-ci-review-packet-and-worked-output). |
| Product vocabulary or the coding environment interrupts your learning. | **Optional on-ramp:** [Claude 101](https://academy.claude.com/courses/claude-101) for the application; [Claude Code 101](https://academy.claude.com/courses/claude-code-101) for coding workflow. The latter's hands-on work requires CLI/editor familiarity and supported Claude Code access or an API key. Check plan and administrator restrictions on the actual lesson. | Explain the screen, backend, model and tools in [the application primer](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/00-foundations.md), then return to the concept that was unclear. Skip repeated introductory material you can already explain. |
| You need a framework for deciding what to delegate and how to check it. | **Optional foundation:** [AI Fluency: Framework and foundations](https://academy.claude.com/courses/ai-fluency-framework-foundations); [AI capabilities and limitations](https://academy.claude.com/courses/ai-capabilities-and-limitations) for model limitations. These support understanding; neither adds a new exam domain. | Apply the [four delegation checks](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/01-application-and-agent-loop.md#four-checks-before-delegating) to C17. Name what the model may propose and what application code or a human must own. |
| You already understand basic MCP and need deeper implementation patterns. | **Optional depth:** [Model Context Protocol: Advanced Topics](https://academy.claude.com/courses/model-context-protocol-advanced-topics). Start after basic MCP and async concepts. Its sampling, notification, filesystem and transport material is enrichment unless matched to a specific exam-guide requirement. | Start with [objective 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md). Explain which actor initiates a request, which capability is available, where permission is checked and how the result reaches the model. Do not infer exam frequency from course depth. |
| Your actual deployment uses a particular cloud platform. | **Optional deployment depth:** use the [official course catalog](https://academy.claude.com/courses) to find the relevant Bedrock or Google Cloud course. Shared API concepts can overlap; identity, permissions, endpoints and operations need platform-specific study. This is not an additional CCAR-F requirement asserted by this site. | Revisit [the bank architecture capstone](../../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/06-putting-it-together.md). State which integration boundary changes and which business authorization/evidence requirements remain. |

</div>

### Turn a completed course into usable preparation

1. **Trace:** close the lesson and reconstruct one request, its data, owners and failure path.
2. **Choose:** explain a mechanism, reject its closest alternative, then change one constraint and decide again.
3. **Show evidence:** use a paper trace for understanding; an actual API/MCP/CLI lab transcript for execution. Check its prerequisites first. API usage, product access and cloud resources may have separate costs even when learning material is freely accessible.
4. **Return and repair:** try the linked [simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) or [targeted practice](site:practice/index.html?exam=CCAR-F), open the exact missed objective, then recall the decision later with [flashcards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md).

A course-completion badge or certificate records course completion. It is distinct from the proctored certification credential and from evidence that you can solve an unfamiliar scenario. Use the [full learning journey and readiness limits](../../02-Lessons/02-CCAR-F-Architect-Foundations/learning-journey.md#what-is-still-a-gap) to judge remaining work. No catalog sweep or fixed number of study hours guarantees a pass.

## Checklist

| ✓ | Step | Link | Pass bar |
| --- | --- | --- | --- |
| [ ] | When readiness evidence supports it (not a first learning step), book the exam on the Anthropic Partner Academy with your Salesforce email and legal name (route: exam guide v1.0 section 11 and FAQ, Tier 1; Salesforce email and legal name: [Insights](../../11-Lessons-Learned/INSIGHTS.md), tier F) | [Certification page](https://anthropic.skilljar.com/claude-certified-architect-foundations-certification) (standard login) or [Partner Academy SSO](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) | booked |
| [ ] | L00 orientation; choose coached teaching or an optional diagnostic | [L00](../../02-Lessons/02-CCAR-F-Architect-Foundations/L00-orientation.md) | done |
| [ ] | L01 Agentic Architecture (**27%**) → practice drill | [L01](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) · [CCAR-F practice — choose Domain 1](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) | 80% |
| [ ] | L04 Prompting and Structured Output (20%) → practice drill | [L04](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) · [CCAR-F practice — choose Domain 4](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) | 80% |
| [ ] | Lab 02: coordinator plus extraction | [Lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) | runs |
| [ ] | L03 Claude Code (20%) → practice drill | [L03](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) · [CCAR-F practice — choose Domain 3](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) | 80% |
| [ ] | L02 Tools and MCP (18%) → practice drill, plus drills on task statements 2.1–2.5 | [L02](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) · [CCAR-F practice — choose Domain 2](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) | 80% |
| [ ] | Lab 03: MCP server plus Claude Code setup | [Lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) | runs |
| [ ] | L05 Context and Reliability (15%) → practice drill | [L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) · [CCAR-F practice — choose Domain 5](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F) | 80% |
| [ ] | SIM-02 to SIM-07, six saved-guide scenario families; add unseen application transfer | [Simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) | 80% each |
| [ ] | SIM-01 full mocks | [SIM-01](../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-01-full-mock.md) | fresh attempts + domain repair |
| [ ] | Exam guide sample questions (the official practice exam was retired in the move to Pearson: [Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1, checked 2026-10-07) | [Exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications) section 9 | all correct, with the reason each wrong option is wrong |
| [ ] | Sit the exam, then share what you learned | [What others learned](../../11-Lessons-Learned/INSIGHTS.md) | 720 |

## Week plan

| Week | Focus | Do |
| --- | --- | --- |
| 1 | Domain 1 (27%) and Domain 4 (20%) | L00, concept coaching and the application primer; then L01 and L04. A diagnostic is optional after teaching, or first for experienced learners. Courses: Building with the Claude API (the tool-use and structured-output parts), Introduction to subagents (not on the official prep list). Lab 02. |
| 2 | Domain 3 (20%) and Domain 2 (18%) | L03, L02. Courses: Claude Code 101 (not on the official prep list), Claude Code in Action, Introduction to MCP. Lab 03. Audit one of your own Claude Code setups against Domain 3. |
| 3 | Domain 5 (15%), then rehearsal | L05. SIM-02 to SIM-07. Mocks, then the exam guide's 12 sample questions (section 9), all correct with reasons (the official practice exam is retired: [Partner Academy FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1, checked 2026-10-07). **Review readiness evidence and remaining objective gaps before choosing an exam date.** |

## Hard-mode track

For people who want more practice than the week plan above. Candidates report scenario judgment (field reports, F: emphasis only). Diagnose the failure before selecting a mechanism: unclear criteria can need better prompting; mandatory authorization needs executable controls; a valid but wrong extracted value needs evidence and semantic validation. No mechanism wins just because it is structural. Hard mode applies that distinction:

1. Official courses first, from the [prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
   (Tier 1, checked 2026-10-02): Building with the Claude API, Introduction to MCP, Claude Code in
   Action. These courses share API concepts, but cloud-platform identity, permissions, endpoints and operational behavior can differ. Use the [course companion](#choose-official-courses-by-the-decision-you-need-to-learn) to choose optional deployment depth; this is not a claim that the courses are interchangeable.
2. Daily [flashcards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)
   ([Anki import](../../02-Lessons/02-CCAR-F-Architect-Foundations/flashcards-anki.csv)), tagged by
   task statement.
3. The 45 [hard drills](../../02-Lessons/02-CCAR-F-Architect-Foundations/HARD-DRILLS.md), Domain 1
   first. For every wrong option, say why it's wrong.
4. Decision charts and sequence diagrams: [deep-practice](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/README.md).
5. Before booking: review fresh timed attempts, objective gaps and delayed transfer. Earlier 850+/70% targets were project study heuristics, not official scaled-score predictions;
   plus the exam guide's sample questions.

Every task statement has its own page: [exam objectives](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/README.md).


## What people who passed say (tier F)

Field reports from colleagues. They change what to emphasize, never the facts.

- "Get really good on **MCP and structured output**. Those two areas carried serious weight":
  server scoping, auth, tool discovery, JSON-schema extraction and `tool_choice`. (A colleague,
  2026-07-10)
- "The only certification exam I've ever needed the **full two hours** for", and "take lots of
  practice exams". (A colleague, 2026-07-10)
- Take the diagnostic first, then study only your weak topics. (a passer, high-800s)
- Register with your **legal name**. A preferred name cost a colleague a second fee.


## Complete objective learning path

The [objective lessons](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/README.md) cover all 30 official task statements and their 240 knowledge and skills bullets, one page per task, plus production-transfer cases. This route takes longer than the legacy core estimate, because it adds extended practice.