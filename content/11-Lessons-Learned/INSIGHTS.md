# Insights from people who passed

A summary of every record in [`debriefs/`](debriefs/), by exam. **The official exam guide always
wins.** These insights only change *emphasis*: hours, order, and what to practice more.

**Evidence levels**

- **Confirmed:** reported independently by 2 or more people. It goes into lessons and curriculum
  as "What people who passed say".
- **Single report:** one person. Shown with their name, and not treated as a rule.
- **Contested:** people disagree, or it conflicts with our plan or the official guide. Both views
  are shown, with our call.
- **Relayed:** a colleague passing on what Anthropic told them (tier F-relayed). It is credited to
  the colleague, never counted as Confirmed, and never shown as Anthropic's own words unless an
  Anthropic page (Tier 1) says the same and is linked.

Every row names the exam each report came from. Rows under "Across all exams" have reports from more than one exam, or apply to all of them.

Last updated 2026-10-03 · 18 debriefs from 12 people (one anonymous, by DM), plus posts in the `#claude-certified-architect-exam-prep`
channel and other Salesforce Slack channels
and one [Slackbot Research harvest](harvests/2026-09-27-slackbot-research.md) (anonymized, so its
points are single reports unless they match a named record).

## Across all exams

| Insight | Level | Who | Used in |
| --- | --- | --- | --- |
| Full, timed practice exams matter more than reading | **Confirmed** | A colleague (CCAR-F), a colleague (CCAR-F, diagnostic then mocks), a colleague (CCAO-F), a colleague (CCAR-F, full mock the day before) | [00-Overview](../01-Curriculum/00-Overview.md) rules, every SIM-01 |
| Register with your **legal name**; the profile must match your government ID | **Confirmed** | A colleague (CCAR-F, paid twice), 2 colleagues (Slack posts, exam not stated; had to request a name change) | Every curriculum's booking step |
| Renewal after 12 months is a free assessment on the Partner Academy if done on time | Official guide, section 14 | — | Proposed for [00-Overview](../01-Curriculum/00-Overview.md) renewals |

## Registration, price and paying

| Insight | Level | Who |
| --- | --- | --- |
| Register on the Partner Academy with your **Salesforce email** | **Confirmed** | 3 colleagues |
| Sign in with your Salesforce email directly, **not "Sign in with Google"**, or you may be charged | Single report | A colleague (2026-09-25) |
| List prices are CCAO-F $99, CCAR-F $125, CCDV-F $125, CCAR-P $175 (USD) | **Official** ([Anthropic's certification pages](https://anthropic.skilljar.com/claude-certified-architect-foundations-certification), checked 2026-09-28) | — |
| Is it free, or full price? | **Contested.** Some got it free (Bangalore drive, partner discount, Partner Academy sign-up with a Salesforce email, a $125 credit from the Architect registration link). Others were charged in full at checkout in September; one reply said "it's what they charge us now" | Free: 3 colleagues. Charged: 6 colleagues |
| **New 2026-09-29:** a post said all four can now be registered free by signing in at `partner-sso.anthropic.com`. Register first and schedule later; the Pearson login arrives by email. In the same thread one person still saw a charge and was told to sign in through that link with a Salesforce email. Not yet confirmed on an Anthropic page. | **Contested** | Free: a colleague. Charged: a colleague |
| **Our call:** sign in at `partner-sso.anthropic.com` with your Salesforce email first, and check the price at checkout. If you're charged, get Forma and manager pre-approval **before** paying, then claim through the Global Education Reimbursement Program | **Confirmed** (reimbursement routes; the partner-sso step is a single report) | posts by 4 colleagues |
| Reimbursement rules: claim within 6 months of finishing; pay with your own card, not a company AMEX; exam, renewal and prep-course fees count; yearly limit $5,250 USD or your country's limit | **Internal policy** (BaseCamp, Global Education Reimbursement Program, via Slackbot 2026-09-28); can change | — |
| An internal "Wave 1" CCAR-F cohort started in late September 2026: 4 weeks, a 1:1 coach, 5-person study groups, a prep pack, and exam costs paid through Forma. Waves 2 and 3 are planned for Q4 | Single report (internal announcement, via the Slackbot harvest; start date given as both 09-24 and 09-28) | unnamed |
| PS cohort members can book up to 40 hours of AI enablement, including Foundations prep, to "Internal AI Training – Credited (FY27)" | Single report (cohort channel) | A colleague |

## Exam day

| Insight | Level | Who |
| --- | --- | --- |
| Time pressure and long scenario reading are real; agent and multi-agent questions run long | **Confirmed** | 2 colleagues |
| Run the system test at least a day ahead; join 30 minutes early; keep your phone for ID and room photos | Single report | A colleague |
| Online check-in takes about 30 minutes or more (room photos, ID); be ready 30 minutes early | **Confirmed** | 2 colleagues, the project's author (CCAO-F, more than 30 minutes) |
| For online exams, pick a plain room you won't have to rearrange. A desk with external monitors meant moving them for the room check | Single report (matches a colleague clearing her desk and room for an earlier online exam) | The project's author (CCAO-F) |
| Stamina matters: it got tiring after about 20 questions. Practice in timed blocks, building up to a full sitting | Single report | The project's author (CCAO-F) |
| Online proctoring (OnVUE) on a **Salesforce-managed Mac** | **Contested.** #help-techforce has many reports that the Mac firewall can't be changed for OnVUE, and some people missed exams. A colleague passed online on her office laptop | A colleague's summary and 5+ reports in #help-techforce vs a colleague |
| **Our call:** run the OnVUE system test on the exact machine a few days ahead. If it fails, book a test center | — | — |
| Test centers give you a notepad, pen and earplugs; the result shows at the end | Single report | 2 colleagues |

## Hands-on practice

| Insight | Level | Who |
| --- | --- | --- |
| Salesforce laptops block direct calls to the Anthropic API needed for course exercises | **Confirmed** | 2 colleagues |
| Two ways around it: a personal Anthropic account on a personal laptop, or an internal route your team supports (ask in the channel) | Two single reports | 2 colleagues |

## Order of exams

**Contested.**

- **Our default:** CCAO-F first, as a cheap way to learn the question style.
- A colleague, who passed all four: start with CCAR-F, because "everything else builds on
  it".
- **Relayed: Anthropic's advice to the Salesforce accelerated cohort** (relayed by a colleague,
  2026-09-24): architects should take CCAR-F and CCAR-P, and developers (FDEs) the Developer track.
  "Pursue a Foundations certification where possible, preferably CCAR-F." CCAR-F and CCAR-P "can be
  pursued independently; neither is a prerequisite for the other."
- **A colleague:** CCAO-F is "the easiest to crack out of all 4".
- **Decided 2026-09-27:** CCAO-F first only for people who don't write code. Architects and
  developers start with CCAR-F; architects take CCAR-P next and developers CCDV-F. The full paths
  are in the [curriculum overview](../01-Curriculum/00-Overview.md#1-recommended-order-it-depends-on-who-you-are).

## CCAO-F Associate

Every row here is Tier F (field report) unless marked Official.

| Insight | Level | Who |
| --- | --- | --- |
| CCAO-F has some items with more than one correct answer, and each item says how many to choose. Official guide wording: "Multiple-choice and multiple-response items; each item states how many responses to select" | **Confirmed**, and in the official guide's Item format | A colleague (CCAO-F); the project's author (CCAO-F, 2026-10-01) |
| Scenario questions about non-technical personas and practical AI decisions, not technical detail | **Confirmed** | 2 colleagues |
| Many **sequencing** questions. One form: the stem gives a process of about 5 steps, and each option lists those steps in a different order; pick the option with the right order | **Confirmed** that sequencing items appear; "many" and the 5-step format are a single report (the project's author) | A colleague; the project's author (2026-10-01, described the ordering format) |
| "Pick 2" items are common on CCAO-F, mostly 2 out of 5 options. How common is **Contested**: "a few" (A colleague) vs "many" (the project's author). Our practice bank has 15 two-answer items out of 500 and no 5-option items (checked 2026-10-02) | **Confirmed** that they appear; amount Contested; "2 out of 5" is a single report (the project's author) | A colleague; the project's author |
| The score report gave percent-correct for 27 of the 30 guide objectives, each named in the guide's own wording, not just the 7 domains. With about 2 questions per objective, one objective's percentage means little; the guide says these percentages aren't used for pass or fail. The official guide describes only a per-domain report (exam wording: "percent-correct by domain on the score report"), so the per-objective breakdown may not appear for everyone. Used in the `01-Curriculum/*/CCxx-objectives.md` intros | Single report (2026-10-01, no score shared) | The project's author |
| The 4D framework and AI Fluency feature heavily | **Confirmed** | 2 colleagues (AI Fluency in her short list) |
| Short prep is enough: the prep path, AI Fluency and Claude 101, in under a week | Single report | A colleague |
| Prep took under 5 hours (recorded 2026-10-02) | Single report | The project's author (CCAO-F) |
| One colleague found output evaluation (spotting hallucinations, inconsistencies and bias) harder than everyday prompting | Single report | Slackbot harvest, Colleague E |

## CCAR-F Architect Foundations

| Insight | Level | Who |
| --- | --- | --- |
| One CCAR-F sitting had only single-answer items, no choose-two. Not a conflict with anyone's CCAR-F report; the multi-answer sightings were on CCAO-F. The Tier 1 CCAR-F guide (lines 61–62) still allows "multiple-choice and multiple-response items". **Our call:** keep a small choose-N share in CCAR-F practice, and read the count on each item | Single report, first-hand (received directly, 2026-10-03) | Anonymous colleague (CCAR-F, 2026-10-03) |
| Use Claude as a study partner: ask it to explain *why* an answer is right (proposed for [00-Overview](../01-Curriculum/00-Overview.md) rules) | **Confirmed** | A colleague (CCAR-F, "helped a LOT"), a colleague (CCAR-F) |
| Community practice questions can have wrong or ambiguous answers; understand the reasoning, don't memorize (proposed for [00-Overview](../01-Curriculum/00-Overview.md) rules) | Single report (matches our tier-3 caution) | A colleague (CCAR-F) |
| MCP (scoping, auth, discovery) and structured output (JSON schema, `tool_choice`) carry a lot of weight | Single report | A colleague |
| Take a diagnostic or mock first, then study only weak topics | **Confirmed** | 2 colleagues |
| Of the near-identical prep courses, take Building with the Claude API; skip Bedrock and Vertex. **Project interpretation (2026-10-20):** this is exam-prep prioritization advice, not a claim that platform-specific deployment, identity and operations are interchangeable; see the [course companion](../01-Curriculum/02-Architect-Track/CCAR-F.md#choose-official-courses-by-the-decision-you-need-to-learn) | **Confirmed** | 2 colleagues, anonymous colleague (CCAR-F, 2026-10-03, "most useful learning") |
| Claude Code in Action matters for the orchestration and architecture domains | Single report | A colleague |
| About 20–30 hours of prep (10 days × 2 h; 2 weeks × 2–3 h) | **Confirmed** | 2 colleagues |
| Alex Kaziuka's Udemy course covered what was needed | Single report | A colleague |
| Udemy practice tests run easier than the real exam | Single report | A colleague |
| Words like "guarantee", "enforce" or "every time" in a question point to a deterministic mechanism (a hook, or a forced tool choice), not a prompt instruction | Single report (internal cheat sheet, via the Slackbot harvest) | unnamed |
| Answer in three passes: the ones you know, then the flagged ones, then a confidence check | Single report (same cheat sheet) | unnamed |
| Forced tool use vs structured outputs was a common point of confusion | Single report | Slackbot harvest, unnamed |
| Topics felt evenly spread across domains (compare a colleague: MCP and structured output weighed heavily) | Single report, first-hand (received directly, 2026-10-03) | Anonymous colleague (CCAR-F, 2026-10-03) |
| Questions felt close to the exam guide's sample questions and common sample sets; no surprises | Single report, first-hand (received directly, 2026-10-03) | Anonymous colleague (CCAR-F, 2026-10-03) |
| Pace by scenario: give each one 30 minutes, review its marked items inside that window, then move on. End-of-exam review was hard because re-entering an old scenario is hard. The guide gives 60 items, 4 scenarios, 120 minutes (Tier 1, CCAR-F guide lines 59–66); about 15 items and 30 minutes each is our arithmetic, and the split may be uneven | Single report, first-hand (received directly, 2026-10-03) (differs from the three-pass cheat sheet above) | Anonymous colleague (CCAR-F, 2026-10-03, finished with about 10 minutes left) |
| Day before: revise what you've learned; if solid, revisit Building with the Claude API | Single report, first-hand (received directly, 2026-10-03) (A colleague did a full mock instead) | Anonymous colleague (CCAR-F, 2026-10-03) |

## CCAR-F supplemental course reviews

**Added 2026-10-20.** The [Academy course-review video](https://www.youtube.com/watch?v=OYyYlH6Un0Y&t=118s) is a **single third-party course review (Tier 2)**, not a verified first-hand CCAR-F exam debrief. It does not increase the passer/debrief counts above or change official objective weights. Its course rankings and time estimates are the creator's opinion. The supplied summary was checked against current official course pages before adopting advice.

| Preparation lesson | What we changed or retained | Evidence boundary |
|---|---|---|
| Choose a course for a learning gap, rather than collect every completion badge. | Added a [course-to-decision companion](../01-Curriculum/02-Architect-Track/CCAR-F.md#choose-official-courses-by-the-decision-you-need-to-learn) to the existing exam hub, with local return links and mastery outputs. | Project learning recommendation, not an official required sequence or validated readiness threshold. |
| Establish the prerequisite picture before advanced implementation work. | Keep the no-setup concept route; distinguish optional Python/API/CLI exercises and their access requirements. Take basic MCP before optional advanced patterns. | Check each official course's current prerequisites; the video's catalog counts and durations are not treated as current facts. |
| Learn what to delegate and how to evaluate the result. | Added the [four checks applied to a refund](../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/01-application-and-agent-loop.md#four-checks-before-delegating): Delegation, Description, Discernment and **Diligence**. | Names verified against the [official AI Fluency framework course](https://academy.claude.com/courses/ai-fluency-framework-foundations); our refund mapping is an original teaching application. |
| Distinguish course progress from architecture readiness. | After a course, reconstruct a trace, compare alternatives, change a constraint, attempt targeted practice and repair the exact objective. | A course-completion badge/certificate is distinct from the certification exam and from demonstrated transfer. |
| Keep deployment learning conditional on the intended platform. | Qualify the historical “skip Bedrock/Vertex” advice; platform-specific learning can matter for real deployments. Advanced MCP remains optional depth unless tied to an actual guide requirement. | No inferred exam weight, requirement to finish all courses, or claim that platform choices are interchangeable. |

[Return to the CCAR-F study hub](../01-Curriculum/02-Architect-Track/CCAR-F.md) · [Concept coaching](../02-Lessons/02-CCAR-F-Architect-Foundations/concept-course/README.md) · [Full teaching-to-exam journey](../02-Lessons/02-CCAR-F-Architect-Foundations/learning-journey.md)

## CCDV-F Developer Foundations

| Insight | Level | Who |
| --- | --- | --- |
| About two-thirds overlap with CCAR-F, so take it soon after | Single report | A colleague |
| More Claude Code than the 3% blueprint weight suggests: CLI, CLAUDE.md, Skills, settings.json, subagents | **Confirmed** | 2 colleagues |
| Also: Agent SDK, streaming and protocols, all in scenario questions | Single report | A colleague |
| On one score report, building agents was the weak area while agent architecture and agent patterns were strong. The report's label "Agent Construction" is the guide's skill area 1.2 | Single report | A colleague, via the Slackbot harvest |
| Harder than CCAR-P, with many development-specific questions | Single report | A colleague |
| Time and pass mark | **Contested.** a colleague reported 135 minutes and 772. The official guide says 120 minutes and a scaled 720. **The guide wins** | A colleague vs official guide |

## CCAR-P Architect Professional

| Insight | Level | Who |
| --- | --- | --- |
| Not harder than CCAR-F; for some people the easiest exam | **Confirmed** | 3 colleagues |
| About half is standard system design with Claude wording | Single report | A colleague |
| CCAR-F isn't required first | **Relayed** (Anthropic, passed on by 2 colleagues; not in the official FAQ) | A colleague (Anthropic email), Anthropic via a colleague (2026-09-24) |
| Anthropic's two-day Partner Base Camp for architects strongly recommends CCAR-F first | **Relayed** (single report) | A colleague |