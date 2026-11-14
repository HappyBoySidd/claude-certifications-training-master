# CCAO-F Lesson 7 — Troubleshooting and Optimization (10%, about 6 questions)

Last reviewed: 2026-09-29

**Time:** 45 min · **Practice:** [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Exam wording (exam guide v1.0, Domain 7):**

- Identify, diagnose, and resolve issues with underperforming prompts or poor outputs
- Adjust approach based on feedback and results
- Optimize workflows for efficiency and effectiveness

## 1. The big idea

The exam rewards **finding the real cause**. Most distractors are "switch to Opus" or "write a
longer prompt". Those only help when the real cause is the model or the prompt.

## 2. The diagnostic ladder (always in this order)

| Step | Ask | Fix |
| --- | --- | --- |
| 1 | Is this the wrong task for AI, or a policy problem? | Stop or escalate |
| 2 | Wrong place, or missing knowledge? | Fix the Project, source or connector, or turn on web search or Research |
| 3 | Is the prompt missing information? | Add the role, constraints, examples, format and success criteria (L01) |
| 4 | Has context drifted, or do instructions conflict? | Summarize and restart; reconcile the layers (L03, L05) |
| 5 | Is it a calculation? | **Code Execution.** A better adjective won't fix math. |
| 6 | Wrong model? **Only after steps 2–5.** | Haiku for volume, Opus for judgment |

The model comes last on purpose. Switching models is the fix people reach for first, and it's
usually the wrong one.

## 3. Symptom to cause

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Quotes an outdated policy | An old file is still in knowledge | Replace the file |
| Wrong totals in a summary | Mental math | Code Execution |
| Ignores the template after 40 turns | Context drift | Summarize and restart |
| "I don't have information about last week's launch" | Knowledge cutoff | Web search or Research |
| Output changes every run | No examples or format spec | Add 3–5 relevant, varied examples (Anthropic's prompting guide, Tier 1) and a format; use a Skill |
| Can't see the shared Drive folder | Connector off, or you lack permission | Check the connector and access |
| Research never starts | Web search is off, or it wasn't asked for directly | Turn on web search; say "use the research tool" |
| Hit usage limits on a batch job | An expensive model on simple work | Haiku, and a Project instead of re-pasting |

## 4. Optimizing

- **Cost and speed:** a cheaper model for volume, a Project instead of retyping context, a Skill
  instead of repeating steps, Research only when you need many sources.
- **Quality:** examples, success criteria, quote first, and splitting the task.
- **Know when to stop:** if three targeted fixes fail, or the work needs judgment AI shouldn't make,
  change the approach or hand it to a person.

## 5. Adjusting from feedback and results

The official objectives include "adjust approach based on feedback and results". In practice that
means treating each disappointing output as evidence, not bad luck:

1. **Name what was wrong** against your success criteria ([Lesson 1, section 2](L01-prompting-and-task-execution.md)): missing a section, a wrong
   number, the wrong tone. "It's not good" can't be fixed.
2. **Change one thing**, run it again on the same input, and compare. If you change the prompt,
   the model and the file at once, you won't know which fix worked.
3. **Make the fix stick.** If the same correction keeps coming up, move it out of your chat and
   into the setup: a rule in the Project instructions, a better example in knowledge, or a step
   in the Skill. Otherwise every colleague rediscovers the same problem.
4. **Listen to the people who use the output.** If reviewers keep editing the same thing, that
   edit belongs in the instructions or the template.
5. **Know when the answer is "not AI".** If three targeted fixes fail, or the work needs judgment
   that must stay with a person, change the approach (section 4).

## 6. Worked example

"After a 2-hour chat, Claude has stopped applying the scoring framework." Walk the ladder:

1. Is it a policy problem? No.
2. Is knowledge missing? No.
3. Is the prompt missing information? The framework was given earlier.
4. **Has context drifted? Yes.** Summarize the framework and the progress so far, then start a new
   chat in the Project.

Switching to Opus is wrong. So is repeating the framework in the same long thread.

**A second example, on optimizing.** A team runs 400 short product descriptions a week through Opus
and keeps hitting usage limits. Nothing is wrong with the quality. Walk the ladder: the task suits
AI, the knowledge is there, the prompt is fine and there's no math, so the step that applies is 6,
the model. The
work is structured and high-volume, so **move it to Haiku or Sonnet**, put the style guide in a
Project so nobody re-pastes it, and spot-check a sample each week. Keep Opus for the few
descriptions that need real judgment.

## 7. Traps

- **Jumping to "switch to Opus".** The model is step 6, the last on the ladder. Most bad outputs
  come from the place, the knowledge, the prompt, the context or the math first.
- **"Make the prompt longer."** More words don't help if the real cause is an old file, drift, a
  connector that's off, or math done in Claude's head.
- **Changing several things at once.** You fix the output but learn nothing, and it breaks again
  next month.
- **Fixing it in the chat only.** A correction typed into one conversation is gone next time. Put
  repeat fixes into the Project or Skill.
- **Asking Claude to "double-check its math".** For numbers, use Code Execution or the source
  spreadsheet.
- **Never stopping.** Some tasks shouldn't be done by AI. After three targeted fixes fail, change
  the approach or hand it to a person.

## Try it (10 min)

Remember a time Claude disappointed you. Walk the ladder out loud and name the step where the real
cause was.

## Done when

- [ ] You can recite the ladder in order
- [ ] You answer "wrong model" only after ruling out steps 2–5
- [ ] You scored 80% or more on [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**After this lesson:** the CCAO-F workplace scenarios, starting with
[SIM-02](../../04-Simulations/01-CCAO-F-Associate/SIM-02-marketing-launch.md), then the full mock.

Sources: official exam guide v1.0, Domain 7 objectives (Tier 1); course Modules 3 and 7 (Tier 1,
copy); Anthropic's prompting best-practices page, saved at
the reference library (in the study workspace)
(Tier 1, for "3–5 examples"; public copy:
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices); `…/public-docs-fetch/07-troubleshooting-and-optimization.ocr.txt` (Tier 2).