# CCAO-F Lesson 4 — Workflow Integration and Solution Design (16%, about 9–10 questions)

**Time:** 60 min · **AI Fluency:** *Delegation* · **Practice:** [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Last reviewed: 2026-09-29

**Exam wording (exam guide v1.0, Domain 4):**

- Apply Claude to analyze requirements and use cases
- Leverage Claude for research, planning, and process optimization
- Use Claude to support solution design, development, and iteration
- Integrate Claude into existing workflows to augment or redesign them
- Communicate Claude's value and limitations to stakeholders

## 1. The big idea

Move from "I use Claude" to "**our workflow** uses Claude". Decide which steps Claude does, which a
human does, where the check happens and who owns the result.

## 2. Three ways to work with AI

| Mode | Who thinks | Example |
| --- | --- | --- |
| Automation | AI does a specified task | Pull fields from 200 invoices into a table |
| Augmentation | You and AI think together | Stress-test a project plan, then the PM decides |
| Agency | You configure AI to run tasks later | A Skill plus a Project that produces the weekly status pack |

**Exam tell:** if the stakes are high or a person is affected, the answer is **augmentation with a
named human owner**, not full automation.

## 3. Understand the work before choosing features

Write down the **trigger**, **inputs** (and how fresh they must be), **outputs** (who gets them and
what good looks like), **constraints** (policy, personal data, brand), **risk** (what happens if
Claude is wrong), **cadence** and **owner**. Then map them:

| Signal | Design choice |
| --- | --- |
| Recurring, with stable context and format | A Project, plus a Skill for the procedure |
| Live data in Drive, Gmail or Slack | A connector, not a stale upload |
| Current outside facts | Web search or Research |
| Numbers that must be right | Code Execution plus a human spot-check |
| High-risk use | A qualified human reviews before it's sent, and AI use is disclosed |
| A one-off | Chat. Don't pay the setup cost of a Project. |

A good move the exam likes: paste the current process document into Claude, ask it to mark each
step *automate*, *augment* or *keep human*, then **challenge that split yourself**.

## 4. Improving a process

1. Write down the current steps, with times and pain points.
2. Mark each step as Claude, a human, or the system of record (the official tool where the data
   lives, like the company's CRM or finance system).
3. Put review gates where mistakes are expensive.
4. **Pilot it for a week on real work.**
5. **Measure** time taken and rework rate, not "it felt faster".
6. Redesign: move stable context into the Project and procedures into Skills, and keep
   accountability with a human.

**Augment** (Claude drafts, a human sends) changes little and carries little risk. **Redesign**
(remove steps) pays off more but needs the owner's buy-in and a fallback plan. **Match the change to
how ready the organization is.** A team with no AI policy shouldn't jump to unattended automation
on customer data.

## 5. Human checkpoints that belong in the design

- Before anything reaches a customer or regulator.
- After any calculation that affects money, inventory or compliance.
- When sources conflict or Claude says it's unsure.
- Before anything is sent, filed or changed through a connector.

Every workflow needs **an accountable owner**, **an escalation path** and **a clean handoff**: a
finished file with its caveats, not a chat transcript.

## 6. Talking to stakeholders

- **Value you can claim:** setup done once, faster first drafts, consistency, and output that's
  easier to review.
- **Limits you must state:** answers vary, fluency isn't accuracy, knowledge has a cutoff, context
  fills up, usage limits exist, and high-risk areas need a human and disclosure. **Claude doesn't
  make the decision** on hiring, credit, medical or legal questions.
- **Overclaiming is always wrong:** "It'll replace the analyst" and "it doesn't hallucinate in a
  Project" are both false.

A one-pager for stakeholders covers: the job and how success is measured · what Claude does and
what people do · what data goes in and what doesn't · the review gate and owner · what isn't
automated in version 1 · how you'll know it's working in 30 days.

**Know where your job ends:** API, agent and tool building goes to a **Developer**. Enterprise
architecture and governance at scale go to an **Architect**.

## 7. Worked example

"Have Claude just handle vendor onboarding: read contracts, set a risk rating and email the
vendor."

**The sound design:**

- A Project with the onboarding playbook as knowledge
- A Skill that builds the risk report the same way every time
- Code Execution for the financial exposure numbers
- **A human legal or ops review before any email goes out**
- No automatic sending in version 1

**The unsound design:**

- Pasting each contract into a new chat every time
- Using Opus "because it's legal", with no review
- Letting Claude set the final risk rating
- Emailing the vendor automatically

## 8. Claude as a design partner: research, plan, iterate

The official objectives also ask you to use Claude *while you design*, not only inside the
finished workflow. Three moves cover it:

- **Analyze the requirements.** Paste the request, the meeting notes or the current process and
  ask Claude to list the goals, the unstated assumptions and the open questions. Then take the
  open questions back to the people who own the work. Claude can find gaps; it can't answer
  them for the business.
- **Research and plan.** Use Research (or web search for one fact) to see how others handle the
  same process, then ask Claude for two or three options with the trade-offs of each. You pick.
  Ask it to mark which parts of its plan come from your sources and which are its own suggestions.
- **Iterate the design.** Ask Claude to attack its own draft: "What would go wrong in week one?
  Where would a reviewer miss an error?" Pilot the design, bring the real results back, and
  change one thing at a time ([Lesson 7, section 5](L07-troubleshooting-and-optimization.md)).

At every step, the human stays accountable for the decision. Claude speeds up the thinking; it
doesn't own the answer.

## 9. Traps

- **Automating before mapping.** Picking features before you've written down the trigger, inputs,
  outputs, risk and owner (section 3) means you're guessing.
- **Full automation for anything customer-facing in version 1.** Start with Claude drafting and a
  human sending. Remove the check only after a record of accuracy.
- **"It felt faster" as proof.** Measure time taken and rework rate during the pilot.
- **Overselling to stakeholders.** "It won't hallucinate in our Project" or "it replaces the
  analyst" is always wrong. State the limits along with the value.
- **Handing off a chat transcript.** The handoff is a finished file with its caveats and an owner.
- **Doing Developer or Architect work yourself.** If the design needs the API, custom agents or
  enterprise-scale governance, the right move is to escalate to that role.

## Try it (15 min)

Take one recurring process from your engagements. Mark each step automate, augment or human, name
the owner and the review gate, and write the 6-line stakeholder one-pager.

## Done when

- [ ] You can split a process into automate, augment and human, with a reason for each
- [ ] Every design you draw has an owner, a review gate and an escalation path
- [ ] You scored 80% or more on [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Sources: official exam guide v1.0, Domain 4 objectives (Tier 1); course Module 4 (Tier 1, copy);
`…/public-docs-fetch/04-workflow-integration-and-solution-design.ocr.txt` (Tier 2).