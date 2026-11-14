# Curriculum overview: three tracks, four exams

Anthropic's certifications fall into **three tracks**. Each exam has **its own curriculum file**,
so plans, lessons and progress never mix. This page covers only what applies across exams: the
order, the shared method and the shared courses.

| Track | Level | Exam | Curriculum | Lessons | Progress log |
| --- | --- | --- | --- | --- | --- |
| **Associate** | Foundations | CCAO-F | [CCAO-F.md](01-Associate-Track/CCAO-F.md) | [02-Lessons/01-CCAO-F-Associate](../02-Lessons/01-CCAO-F-Associate/README.md) | CCAO-F |
| **Architect** | Foundations | CCAR-F | [CCAR-F.md](02-Architect-Track/CCAR-F.md) | [02-Lessons/02-CCAR-F-Architect-Foundations](../02-Lessons/02-CCAR-F-Architect-Foundations/README.md) | CCAR-F |
| **Architect** | Professional | CCAR-P | [CCAR-P.md](02-Architect-Track/CCAR-P.md) | [02-Lessons/04-CCAR-P-Architect-Professional](../02-Lessons/04-CCAR-P-Architect-Professional/README.md) | CCAR-P |
| **Developer** | Foundations | CCDV-F | [CCDV-F.md](03-Developer-Track/CCDV-F.md) | [02-Lessons/03-CCDV-F-Developer](../02-Lessons/03-CCDV-F-Developer/README.md) | CCDV-F |

Only the Architect track has a second level (Professional) today. Anthropic's pages list no
Associate or Developer Professional exam as of 2026-09-25.

## 1. Recommended order: it depends on who you are

Decided on 2026-09-27. Pick the path that fits your job.

**Path A: you don't write code** (consultants, analysts, project and business roles).

| # | Exam | Study hours | Why in this slot |
| --- | --- | --- | --- |
| 1 | CCAO-F | 8–12 | A quick, cheap win ($99) that teaches Anthropic's question style |
| 2 | CCAR-F | 20–25 | The core technical exam; the others build on it |
| 3 | CCAR-P | 15–20 | Recommended after CCAR-F, not required |
| 4 | CCDV-F | 10–15 more | Optional for this path; about two-thirds overlaps with CCAR-F |

**Path B: you design solutions** (architects, technical consultants, engagement leads).

| # | Exam | Study hours | Why in this slot |
| --- | --- | --- | --- |
| 1 | CCAR-F | 20–25 | Anthropic's advice to architects, relayed by a colleague, is "preferably CCAR-F", and a colleague who passed all four says everything else builds on it. It also counts toward partner tiers. |
| 2 | CCAR-P | 15–20 | Same track, next level, while the architecture is fresh. Its governance, rollout and stakeholder domains (28%) are the day job. |
| 3 | CCDV-F | 10–15 more | The most hands-on exam (API mechanics are 33%). About two-thirds overlaps with CCAR-F, and the labs from steps 1–2 cover much of the rest. |
| 4 | CCAO-F | 8–12 | Colleagues call it the easiest of the four. After three technical exams it's mostly review. |

**Path C: you write code** (developers, forward-deployed engineers)

| # | Exam | Study hours | Why in this slot |
| --- | --- | --- | --- |
| 1 | CCAR-F | 20–25 | Anthropic's advice, relayed by a colleague, is "preferably CCAR-F" for a Foundations exam |
| 2 | CCDV-F | 10–15 more | Anthropic's advice for developers, relayed by a colleague, is the Developer track. It overlaps about two-thirds with CCAR-F, so take it **within 2 weeks** |
| 3 | CCAR-P | 15–20 | Optional; colleagues found it no harder than CCAR-F |
| 4 | CCAO-F | 8–12 | Optional; by now it's quick |

**Why CCAR-F comes before CCAR-P:** Anthropic's advice to the cohort, relayed by a colleague, is that neither is a prerequisite for the other. Our call: CCAR-P covers the same agent, tool and MCP
topics at a harder level, so CCAR-F is the natural first step.

**About 55–70 hours for all four.** That's 8 weeks at about 10 hours a week, or about 14 weeks at 5.
If you only need Claude Partner Network tier credit, skip CCAO-F: Associate doesn't count toward
tiers. Background is in [lessons learned](../11-Lessons-Learned/INSIGHTS.md#order-of-exams).

## 2. The same six steps for every exam

1. **Book first,** at the end of the planned window. Rescheduling is free up to 24 hours before.
   Use the legal name on your photo ID.
2. **Cold baseline:** one timed mock before studying. Skip any domain above 85%.
3. **Blueprint self-check:** mark every objective yes, shaky or no.
4. **Lessons** for the shaky and no domains, each followed by its practice session.
5. **One hands-on lab** from [`06-Labs/`](../06-Labs/README.md).
6. **Simulations, then mocks.**

**Ready to book when:** two timed mocks in a row at **850 or more**, and no domain under **70%**.
Anthropic's official practice exam was retired in the move to Pearson
([Partner Academy certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications), Tier 1).
The only official practice items now are the exam guide's sample questions and the Anthropic Academy
course quizzes, so use them as a final check, not a score bar.

## 3. Courses shared across exams (take each once)

| Course | Hours | Serves |
| --- | --- | --- |
| AI Fluency: Framework & Foundations | 4 | CCAO-F, and the review ideas in CCAR-P |
| Claude 101 | 2.5 | CCAO-F |
| Associate prep path (8 modules) | about 6 | CCAO-F |
| Introduction to subagents | 0.75 | CCAR-F, CCDV-F |
| Claude Code 101, then Claude Code in Action | 2.5 | CCAR-F, CCDV-F |
| Introduction to MCP | 1 | CCAR-F, CCDV-F, CCAR-P |
| Introduction to agent skills | 1 | CCAR-F, CCDV-F |
| Building with the Claude API | 9 (tool use and structured output for CCAR-F; the rest for CCDV-F) | CCAR-F, CCDV-F |
| MCP Advanced Topics | 1.5 | CCAR-P |
| One cloud course (Bedrock *or* Vertex) | about 8 | CCDV-F, CCAR-P |

**Skip:** a colleague who passed says Building with the Claude API, Claude in Amazon Bedrock and Claude with
Google Vertex are almost identical, so take only the first. Also skip the role-specific AI Fluency
editions and Deploying Claude Enterprise.

## 4. Rules that save time

- **Study by weight.** A 27% domain deserves about 3 times the hours of a 10% one.
- **Mocks beat reading.** Four colleagues who passed all said so.
- **Pace yourself:** 2 minutes a question. Flag the hard ones; guessing isn't penalized.
- **If you fail:** you wait 14 days. Use them on your weakest domains from the score report.
- **Renewals:** each credential lasts 12 months. Finishing all four in about 8 weeks keeps the
  renewals together.

