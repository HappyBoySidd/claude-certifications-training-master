# CCAR-P Lesson 0 — Orientation: how the Professional exam thinks

**Time:** 45 min · **Do first:** the baseline mock (step 3)

## What you're preparing for

- **63 questions in 120 minutes**, a little under 2 minutes each. The pass mark is a **scaled 720**
  on a range of 100–1,000. The fee is **$175 USD**, before any partner discount shown at checkout.
- Two item types: **multiple-choice** (pick one) and **multiple-response** (pick several). Every
  item tells you how many to pick. Count before you click.
- Your score report shows pass or fail, the scaled score, and your **percent correct per domain**.
  Only the total decides the result.
- **No mandatory prerequisite.** CCAR-F is recommended, not required. Anthropic said this to the
  Salesforce accelerated cohort (relayed by a colleague, September 2026): CCAR-F and CCAR-P "can be
  pursued independently; neither is a prerequisite for the other". Another colleague got the same
  answer earlier by email from Anthropic.
- The credential lasts **12 months**. Renewing on time is a **free, non-proctored assessment** on
  the Anthropic Partner Academy. If it lapses, you retake the full exam at full price.
- Retakes wait 14, then 30, then 90 days, with at most 4 attempts in a rolling 12 months.

## The seven domains, and the lessons that cover them

| Domain | Weight | About | Lesson |
| --- | --- | --- | --- |
| 3 Integration | **19%** | 12 questions | [L01](L01-integration.md) |
| 1 Solution Design & Architecture | 17% | 11 | [L02](L02-solution-design-and-architecture.md) |
| 4 Evaluation, Testing & Optimization | 16% | 10 | [L03](L03-evaluation-testing-and-optimization.md) |
| 5 Governance, Safety & Risk Management | 14% | 9 | [L04](L04-governance-safety-and-risk-management.md) |
| 6 Stakeholder Communication & Lifecycle Management | 14% | 9 | [L05](L05-stakeholder-communication-and-lifecycle.md) |
| 2 Claude Models, Prompting & Context Engineering | 13% | 8 | [L06](L06-models-prompting-and-context.md) |
| 7 Developer Productivity & Operational Enablement | 7% | 4 | [L07](L07-developer-productivity-and-enablement.md) |

The question counts are the weights times 63, rounded. The guide calls the weights "approximate",
so treat the counts as a guide, not a promise. Domains 5 and 6 together are 28%: governance and
stakeholder questions feel softer than the technical ones, but they aren't easier.

## How this exam differs from CCAR-F

CCAR-F asks "how do you wire this up?" (agent loops, hooks, `tool_choice`, CLAUDE.md). CCAR-P asks
"which design would you defend in a review, and why?" Most options are reasonable. Only one fits
the constraint the scenario states. The scenarios come from industries such as finance,
healthcare, retail and government.

## The rules that decide most Professional questions

1. **Remove privilege, don't monitor it.** If a role doesn't need a tool or permission, take it
   away. Logging, confirmation prompts and audits are compensating controls. They come second.
2. **Fix retrieval before blaming the model.** Wrong answers straight after a data change point to
   chunking, embeddings or the index. They don't point to the model weights or the temperature.
3. **Measure before optimizing.** Set the metrics and build the eval set first. Then change the
   prompt, the model or the architecture, and compare against that baseline.
4. **Use the least complex pattern that meets the requirement.** A single call, then an augmented
   LLM, then a workflow, then an agent, then several agents. Each step up has to earn its place.
5. **Name the trade-off.** Every choice costs something: accuracy, latency, money, safety or the
   effort to maintain it. The best answer says what you give up and why that's acceptable here.
6. **Put static content first and cache it.** It's the one change that cuts both latency and cost.

## Steps

1. [ ] Skim the [official exam guide v1.0 (community mirror of the official guide)](https://anthropic-partners.skilljar.com/page/partner-certifications)
       ([text version](https://anthropic-partners.skilljar.com/page/partner-certifications)).
       Read sections 5 and 6 closely: the format, and the objectives for each domain.
2. [ ] Work the **3 official samples** in section 8 and read their rationales. Their topics:
       a support agent with more tools than its staff need (Integration), a large static prompt
       sent on every request (Models and context), and a RAG system that gives confident wrong
       answers after a document refresh (Evaluation). Each one teaches a rule above: 1, 6 and 2.
3. [ ] **Baseline:** a timed CCAR-P mock in the [practice tool](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html).
       Log the score, and your weakest two domains, in your own notes.
4. [ ] Start **lab 05** early: a test set, graded scoring and a regression check. It supports L01
       and L03. See [`06-Labs/`](../../06-Labs/README.md).

## Self-check

- Which domain is the biggest? *(Integration, 19%, about 12 questions)*
- Why does "log every refund" lose to "remove the refund tool" when staff never issue refunds?
  *(Logging only detects misuse. Removing the tool means there's nothing left to misuse.)*
- A RAG bot starts giving wrong answers after a re-index, and nothing else changed. Where do you
  look first? *(Retrieval and the index)*
- What must you check on every multiple-response item? *(How many answers it asks for)*

## What people who passed say

- **It isn't harder than CCAR-F, and for some it was the easiest of the four.** Confirmed by three
  colleagues who passed (one scored 944).
- **About half is standard system design with Claude wording** (one colleague who passed, single report).
  Your general architecture experience counts. Spend your study time on the Claude-specific parts.
- **You don't need CCAR-F first** (confirmed). Anthropic's two-day Partner Base Camp for architects
  does strongly recommend it first (single report, relayed by a colleague).
- Across all exams: **full, timed mocks beat reading**, and some items ask for 2 or more answers
  (both confirmed). See [Insights](../../11-Lessons-Learned/INSIGHTS.md).

**Next:** [L01 Integration](L01-integration.md)

Source: official CCAR-P exam guide v1.0, sections 3, 5, 6, 8, 9, 11 and 14; colleague reports in `11-Lessons-Learned/INSIGHTS.md`.