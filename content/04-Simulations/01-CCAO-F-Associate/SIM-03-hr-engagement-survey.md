# CCAO-F SIM-03 — HR engagement survey

**Domains:** 6 Governance (3), 2 Output Evaluation (3), 3 Product and Model Selection (1), 4 Workflow (1) ·
**Decisions:** 8 · **Pass:** 7 of 8 · **Time:** 16 min

Last reviewed: 2026-09-29

## Scene (read it yourself, or have Claude read it)

You're an HR business partner. The annual engagement survey closed with 800 responses in a
spreadsheet: employee name, employee ID, department, manager, a 1–5 score on 12 questions, and a
free-text comment. Half the responses come from Engineering; the Legal team has only 3 people.
The survey promised employees that answers stay confidential and are reported only in groups of 5
or more. Leadership wants a summary by department, themes from the comments, and "a list of the
people most likely to leave" by Friday. Your company's AI policy says no personal identifiers go to
external tools unless they're needed.


---

## The decisions (answer these before you open the key)

1. **Data:** You've deleted the name, ID and manager columns. Legal still shows as its own 3-person group, and one comment names a project only one person runs.
2. **Policy:** Anthropic's Usage Policy doesn't forbid this analysis, but company policy is stricter
3. **Numbers:** Favorability by department, and which ones are below 60%
4. **Themes:** Claude's top theme is "employees want more remote work". You notice most of the comments behind it are from Engineering.
5. **Check:** A theme says "most engineers mention pay"
6. **The flight-risk list:** Leadership wants names of people "likely to leave"
7. **Review:** Before it goes to leadership
8. **Next year:** Make this repeatable

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Stage | Decision | Correct move | Why | Traps to use as distractors | Domain · objective | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Data | You've deleted the name, ID and manager columns. Legal still shows as its own 3-person group, and one comment names a project only one person runs. | **Finish the redaction before upload:** fold groups under 5 into "Other" and scrub identifying details in comments | Partial redaction still identifies people; small groups and details count. | Upload now, since names and IDs are gone · upload and tell Claude not to quote identifying comments · drop the comments column entirely | 6 · Apply data sensitivity, regulatory, and privacy considerations | [Lesson 6, section 3](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md), [Lesson 6, section 3.1](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 2 | Policy | Anthropic's Usage Policy doesn't forbid this analysis, but company policy is stricter | **Follow company policy.** The stricter one wins. | Anthropic's policy is the floor; your organization's policy can go further. | Follow Anthropic's policy, because it's the vendor's own rule · IT approved the tool, so any use in it is approved · ask Claude which policy applies | 6 · Follow organizational AI policies and governance standards | [Lesson 6, section 4](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 3 | Numbers | Favorability by department, and which ones are below 60% | **Code Execution** on the spreadsheet | Exact math on data needs code that runs, not reading. | Ask Claude to estimate from reading it · switch to Opus for accuracy · ask Claude to show its working in the chat so you can trust the sums | 3 · Select appropriate Claude product features (…) | [Lesson 3, section 4](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md), [Lesson 7, section 2](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 4 | Themes | Claude's top theme is "employees want more remote work". You notice most of the comments behind it are from Engineering. | **Check whether one group dominates:** ask for themes by department with counts, and report each department's view separately | A big group can drown out smaller ones; break themes down by group. | Accept it, since it's the most common theme overall · ask Claude to "remove any bias" from the summary · delete some Engineering comments to balance it | 2 · Identify hallucinations, inconsistencies, and biases in responses | [Lesson 2, section 4](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 5 | Check | A theme says "most engineers mention pay" | **Check the count and the example quotes** (count with Code Execution, or read a sample of the source) | A "most" claim needs a count from the data, not Claude's word. | Accept it, because it matches what you expected · ask Claude whether it's sure · soften it to "many engineers" and move on | 2 · Evaluate Claude-generated outputs for accuracy and completeness | [Lesson 2, section 5](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 6 | The flight-risk list | Leadership wants names of people "likely to leave" | **Don't produce a named list.** Offer department-level retention themes instead; any follow-up with a person is HR's judgment, with a named owner. | The confidentiality promise, company policy and fairness rule it out here. | Have Claude rank people from their scores by re-joining the IDs · rank them, but share only with the CEO · rank them and add a note that AI did it | 6 · Identify appropriate and inappropriate use cases | [Lesson 6, section 2](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md), [Lesson 6, section 2.1](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md), [Lesson 6, section 5](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 7 | Review | Before it goes to leadership | **The HR partner reviews it, owns it, and says AI helped** with the analysis | A named person owns the output; checked numbers aren't checked conclusions. | Send it now, since Code Execution already checked the numbers · let Claude "finalize" it · have a colleague skim it for typos only | 2 · Determine when human review or additional verification is required | [Lesson 2, section 6](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md), [Lesson 4, section 5](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md) |
| 8 | Next year | Make this repeatable | **A Project with the rubric, plus a Skill for the analysis steps.** Identifiers are removed in the spreadsheet *before* upload; the Skill's first step checks that no name or ID column is present, and stops if one is. | Removal happens before upload; the Skill only checks it happened. | Let the Skill remove the names after upload · one saved prompt in a note · automatically email each manager their team's results | 4 · Leverage Claude for research, planning, and process optimization | [Lesson 4, section 3](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 4, section 4](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 5, section 3](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 6, section 3](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |

**Scoring:** 7 or more is a pass. Decision 6 is the one people usually get right for the wrong
reason. It isn't "high-risk, so it's banned." Anthropic's Usage Policy lists employment decisions
as a High-Risk Use Case. It frames these requirements for "specific consumer-facing use cases".
Within them, a qualified professional must review advice or decisions that directly affect
individuals, even if those people never see the output. Disclosure is needed only when outputs
are presented directly to them (Usage Policy, saved 2026-09-29, Tier 1; public copy:
https://www.anthropic.com/legal/aup). None of that is a ban. Here, the named list fails because of the
survey's confidentiality promise, your company's identifier rule, and fairness: scores alone
shouldn't flag a person. A department-level view with HR judgment is the appropriate version.

</details>