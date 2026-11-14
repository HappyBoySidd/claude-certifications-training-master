# CCAO-F SIM-04 — Monthly ops report Project

**Domains:** 4 Workflow (3), 5 Configuration (3), 7 Troubleshooting (2) · **Decisions:** 8 ·
**Pass:** 7 of 8 · **Time:** 16 min

Last reviewed: 2026-09-29

## Scene (read it yourself, or have Claude read it)

You're an operations analyst. Every month you build a vendor performance report: pull the latest
export from Drive, compute on-time delivery and cost variance for each vendor, flag anything over
10% variance, write a narrative using the standard template, and send it to the COO. Three
colleagues want to use the same setup. The company's vendor policy was updated last month.


---

## The decisions (answer these before you open the key)

1. **Design:** How to set it up
2. **Monthly data:** Where the monthly export goes
3. **Old policy:** Claude quotes last year's vendor policy
4. **Conflict:** The instructions say bullets, the template is a table, and a colleague asks for a memo
5. **Wrong total:** The variance total doesn't match finance's number
6. **Slow and hitting limits:** By month 3 the report takes 3 hours. You paste the template and last month's narrative into one long chat, ask Claude to add up the variances by reading the table, and hit usage limits before the narrative.
7. **Split the work:** Before the three colleagues adopt it, the COO asks which steps Claude should do
8. **Send:** Automatically emailing the COO

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Stage | Decision | Correct move | Why | Traps to use as distractors | Domain · objective | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Design | How to set it up | **A Project** (template and policy as knowledge, instructions with the 10% rule) **plus a Skill for the steps, plus Code Execution** for the math | Stable context in a Project, repeat steps in a Skill, math in code. | A new chat every month · one giant prompt saved in a doc · a Project alone, with Claude reading the numbers off the export | 4 · Use Claude to support solution design, development, and iteration | [Lesson 3, section 7](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md), [Lesson 4, section 3](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 5, section 3](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 2 | Monthly data | Where the monthly export goes | **Bring it in through the Drive connector, or attach it in the chat.** Not in Project knowledge. | Knowledge is for stable files; fresh data comes in with each run. | Upload every month's export to Project knowledge · attach a screenshot of the sheet · paste the numbers into the Project instructions | 5 · Manage uploaded knowledge and connectors (e.g., Google Drive, Gmail) | [Lesson 5, section 2](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 3 | Old policy | Claude quotes last year's vendor policy | **Remove or replace the old file**, and point the instructions at the new version by name | Two versions in knowledge means Claude may quote either one. | Type "use the latest policy" in every prompt · switch to Opus · add the new file and keep the old one | 5 · Inform, maintain, and update Claude configurations, knowledge sources, and instructions | [Lesson 5, section 5](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 4 | Conflict | The instructions say bullets, the template is a table, and a colleague asks for a memo | **Reconcile the layers** so the instructions and template agree; use the prompt only for one-off exceptions | Layers that disagree give inconsistent output; make them agree once. | Keep adding "IMPORTANT" to the prompt · let each person override it in their own chat · delete the template so only the instructions remain | 5 · Create effective system-level instructions | [Lesson 5, section 6](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 5, section 9](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 5 | Wrong total | The variance total doesn't match finance's number | **Check which export and columns were used, then recompute with Code Execution** and compare | Find the cause, input or arithmetic, before trusting any total. | Ask Claude to double-check its math in the chat · switch to Opus · use finance's number and edit the total by hand | 7 · Identify, diagnose, and resolve issues with underperforming prompts or poor outputs | [Lesson 2, section 5](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md), [Lesson 7, section 2](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md), [Lesson 7, section 3](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 6 | Slow and hitting limits | By month 3 the report takes 3 hours. You paste the template and last month's narrative into one long chat, ask Claude to add up the variances by reading the table, and hit usage limits before the narrative. | **Fix the workflow, not the prompt:** a fresh chat in the Project each month, the knowledge and Skill carry the template and steps, and Code Execution does the math once | Time and limits go on repeated context and manual steps, not wording. | Shorten the prompt's wording · switch to Opus so it needs fewer turns · finish on a colleague's account when you hit the limit | 7 · Optimize workflows for efficiency and effectiveness | [Lesson 7, section 4](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md), [Lesson 7, section 6](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 7 | Split the work | Before the three colleagues adopt it, the COO asks which steps Claude should do | **Paste the process steps into Claude, have it mark each one automate, augment or keep human, then challenge the split yourself** (for example, sign-off on the COO narrative stays human) | Claude drafts the split; you own it and test it against the risk. | Automate every step, since the Project is set up · accept Claude's split as written · keep every step human until the tool is proven | 4 · Apply Claude to analyze requirements and use cases | [Lesson 4, section 2](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 4, section 3](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md) |
| 8 | Send | Automatically emailing the COO | **Keep a human review before sending** in version 1. Automate only once it's been measured as accurate for a while. | The COO acts on it; a named person checks it until accuracy is proven. | Fully automatic sending from day one · skip review because it's internal · review only the first month, then automate | 4 · Integrate Claude into existing workflows to augment or redesign them | [Lesson 4, section 4](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 4, section 5](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md) |

**Scoring:** 7 or more is a pass. If you miss 5 or 6, go back over the diagnostic ladder and
"Optimizing" in L07 (section 2, section 4).

</details>