# CCAO-F SIM-06 — Support reply prompts

**Domains:** 1 Prompting (4), 7 Troubleshooting (2), 4 Workflow (2), 5 Configuration (1), 2 Output Evaluation (1) ·
**Decisions:** 10 · **Pass:** 8 of 10 · **Time:** 20 min

Last reviewed: 2026-09-29

## Scene (read it yourself, or have Claude read it)

You're the team lead for a 12-person customer-support team at a company that sells home fitness
equipment. Your agents already use Claude to draft replies to tickets, but everyone writes their
own prompts. The replies come out in different tones and lengths, some quote the wrong return
window, and a few refund amounts have been wrong. Your manager wants one shared, reusable setup
that gives consistent replies within a month, with agents still sending every reply themselves.
You'll pilot it on real tickets for two weeks before anyone reports on it.


---

## The decisions (answer these before you open the key)

1. **Setup:** Where the shared prompts should live
2. **Brief:** The current prompt is "Write a reply to this customer."
3. **Tone:** Replies swing between stiff and chatty across agents
4. **Long threads:** Some tickets have 20 back-and-forth messages and Claude misses the actual question
5. **Refunds:** A partial refund depends on the purchase date, the item's condition and a restocking fee
6. **Wrong window:** Two weeks in, some replies still promise a 60-day return window. The only policy file in knowledge is the current 30-day one.
7. **Feedback:** Agents say replies are too long and they keep cutting the last paragraph
8. **Reporting:** Your manager wants to tell the director the new setup "will halve handle time and end refund errors"
9. **Spot check:** A draft to an angry customer whose treadmill arrived broken has the right facts and the right refund, but reads like an internal note: policy codes, bullet points, no acknowledgement of the problem
10. **Next team:** The warranty-claims team wants "the same setup" next week

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Stage | Decision | Correct move | Why | Traps to use as distractors | Domain · objective | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Setup | Where the shared prompts should live | **A Project** for the team: instructions with the tone, format and what to flag, and the current return policy and approved reply templates as knowledge | One shared place everyone gets, without re-pasting or drift between agents | Each agent keeps their own prompt in a doc · one long shared chat · put the rules in each agent's account custom instructions | 5 · Configure Claude Projects with instructions and knowledge sources | [Lesson 5, section 3](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 5, section 9](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 2 | Brief | The current prompt is "Write a reply to this customer." | **Rebuild it with the professional parts:** role, goal, context (who reads it and why), constraints, the ticket inside tags, output format, an "if unsure, say so" rule and success criteria | Claude needs the missing parts; adjectives, pasted policy and bigger models don't supply them | Add "be professional and friendly" · paste the whole return policy into every prompt · switch to a bigger model | 1 · Create effective prompts for business and technical tasks | [Lesson 1, section 2](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md) |
| 3 | Tone | Replies swing between stiff and chatty across agents | **Add a few (3–5) clean, varied example replies** in the team's voice, and describe the tone in the Project instructions | Examples show tone better than rules; Anthropic's guide says 3–5 | Tell agents to add "IMPORTANT: use a warm tone" · let each agent pick their own tone · regenerate until one looks right | 1 · Iterate prompts to improve output quality | [Lesson 1, section 2](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md), [Lesson 7, section 3](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 4 | Long threads | Some tickets have 20 back-and-forth messages and Claude misses the actual question | **Put the thread first and the request last, and ask Claude to quote the customer's key lines before it drafts** | Question last plus quote-first keeps Claude on what the customer asked | Summarize the thread yourself first every time · paste only the last message · turn on Research | 1 · Create effective prompts for business and technical tasks | [Lesson 1, section 2](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md) |
| 5 | Refunds | A partial refund depends on the purchase date, the item's condition and a restocking fee | **Break it into steps:** pull the relevant policy passage, calculate the amount with **Code Execution**, draft the reply, then the agent checks the amount before sending | Separate steps can each be checked; math needs code, not a reread | One prompt that does it all · ask Claude to "double-check the math" · let Claude send refunds automatically | 1 · Apply task decomposition techniques to structure complex requests | [Lesson 1, section 3](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md), [Lesson 7, section 2](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 6 | Wrong window | Two weeks in, some replies still promise a 60-day return window. The only policy file in knowledge is the current 30-day one. | **Check every layer that states the rule:** the reply templates and example replies in knowledge, and the Project instructions. Fix whichever still says 60 days, then tell the team what changed | The file is current, so another layer still carries the old rule | Replace the policy file again · tell agents to type "30 days" in every prompt · switch to Opus | 7 · Identify, diagnose, and resolve issues with underperforming prompts or poor outputs | [Lesson 7, section 2](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md), [Lesson 5, section 4](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 5, section 6](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 7 | Feedback | Agents say replies are too long and they keep cutting the last paragraph | **Name the failure, change one thing** (a length limit plus a shorter example), test it on the same tickets, **then write the fix into the Project instructions** so it sticks for everyone | One change shows what worked; the Project makes the fix last | Rewrite the whole prompt at once · tell agents to keep trimming by hand · add the length rule in each agent's chat only | 7 · Adjust approach based on feedback and results | [Lesson 1, section 4](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md), [Lesson 7, section 5](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md), [Lesson 7, section 7](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |
| 8 | Reporting | Your manager wants to tell the director the new setup "will halve handle time and end refund errors" | **State the value and the limits.** Report what the pilot measured (draft time and rework rate on real tickets), say what Claude doesn't do (agents still check amounts and send every reply; drafts can still be wrong), and commit only to what the pilot shows | Overclaiming is always wrong; measured value with stated limits holds up | Promise both numbers, because the Project prevents errors · leave the limits out so the pitch lands · refuse to state any benefit until the setup is perfect | 4 · Communicate Claude's value and limitations to stakeholders | [Lesson 4, section 4](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 4, section 6](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md) |
| 9 | Spot check | A draft to an angry customer whose treadmill arrived broken has the right facts and the right refund, but reads like an internal note: policy codes, bullet points, no acknowledgement of the problem | **Revise, don't regenerate.** Keep the checked facts and amount, and edit for this reader: acknowledge the problem, plain words instead of codes, short paragraphs, one clear next step | Accurate but wrong fit is a revise; a targeted edit keeps verified facts | Regenerate from scratch until one sounds right · send it, since the facts are right · paste it into a fresh chat outside the Project and ask Claude to "make it nicer" | 2 · Edit, adapt, refine, and compare outputs for the intended audience | [Lesson 2, section 2](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md), [Lesson 2, section 3](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md), [Lesson 2, section 3.1](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 10 | Next team | The warranty-claims team wants "the same setup" next week | **Analyze their requirements first:** their trigger, inputs, outputs, constraints, risk and owner. Ask Claude to list the goals, assumptions and open questions from their process notes, then take the open questions to their lead | A different job has different inputs and risks; copying skips that | Copy your Project and share it as-is · add their warranty rules to your team's Project so both teams share one · let Claude answer the open questions and design the rollout itself | 4 · Apply Claude to analyze requirements and use cases | [Lesson 4, section 3](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md), [Lesson 4, section 8](../../02-Lessons/01-CCAO-F-Associate/L04-workflow-integration-and-solution-design.md) |

**Scoring:** 8 or more is a pass. If you miss 2, 3, 4 or 5, go back over the parts of a
professional prompt and decomposition in L01. If you miss 6 or 7, go back over the diagnostic
ladder in L07. If you miss 8 or 10, reread stakeholders and requirements in L04. If you miss 9,
reread pass, revise or fail in L02.

</details>