# CCAO-F Lesson 5 — Configuration and Knowledge Management (12%, about 7 questions)

**Time:** 60 min · **Practice:** [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Last reviewed: 2026-09-29

**Exam wording (exam guide v1.0, Domain 5):**

- Configure Claude Projects with instructions and knowledge sources
- Manage uploaded knowledge and connectors (e.g., Google Drive, Gmail)
- Create effective system-level instructions
- Inform, maintain, and update Claude configurations, knowledge sources, and instructions

Memory and account custom instructions aren't Domain 5 objectives. The guide mentions Memory in
section 7, "How to Prepare", so this lesson covers them briefly as layers of setup.

## 1. The big idea

Every layer of setup has **one job**. Most wrong answers put something in the wrong layer, or leave
an old file where it is.

## 2. What goes where (learn this table cold)

| Layer | Holds | Example | Changes |
| --- | --- | --- | --- |
| Account custom instructions | Style rules for every chat | "Use UK spelling. No emojis." | Rarely |
| Memory | Who you are, preferences, ongoing work | "I'm a PM at a healthcare company." | Review monthly |
| **Project instructions** | Role, tone, rules for what to flag, output shape | "Always flag budget variance over 10%." | When the process changes |
| **Project knowledge** | **Stable** reference material | The playbook, templates, policy | Replace when it's superseded |
| Connectors | **Live** data, with **your** permissions | Drive, Gmail, Slack, Calendar | Always current |
| Skills | Repeatable procedures (need Code Execution: Tier 2, per the Help Center as of mid-2026; check the current docs) | "Build the monthly variance report." | Versioned |
| This chat | This week's file | Last week's export | Every session |

**Trap:** putting this week's changing file into Project knowledge. Knowledge is for stable
reference only.

## 3. Setting up a Project well

1. Name it for the **job**, for example "Q3 Vendor Onboarding", not "Stuff".
2. Instructions: role, audience, format, what to flag, what to refuse or escalate.
3. Knowledge: the smallest set of **stable, current, well-named** files.
   Example: `Policy_Travel_v2026-07.pdf`.
4. Connectors: turn on only the sources this job needs.
5. Skills: add them when the same steps repeat.
6. Test with 3 real requests before you share the Project with the team.

## 4. Keeping it current (the most-tested part)

- Replace superseded files **the same day**. Don't leave v1 and v2 side by side.
- Version your file names.
- Keep instructions and Skills consistent. If the template changed, update both.
- Remove people who leave the work.
- Tell other users when you change a shared Project.

## 5. The classic question

"Claude keeps quoting last year's travel policy in the Project." **Fix:** remove or replace the old
file and point the instructions at the new one.

These are **wrong**:

- Switching to Opus.
- Typing "use the latest policy" every time. That's fragile.
- Adding the new file but leaving the old one in.

## 6. When layers conflict

The Project instructions say "bullets", your prompt says "a memo" and the template is a table. The
result will be inconsistent. **Reconcile the layers** so they agree, and use the prompt only for a
genuine one-off exception.

## 7. Connectors and permissions

- Connectors **inherit your permissions**. Claude sees only what you can see.
- Use a connector for live data. An upload is a snapshot that goes stale.
- If Claude "can't find" a Drive file, check the connector is on for the chat, that you have
  access, and ask it directly: "pull the relevant context from Google Drive".

## 8. Clients and confidentiality

**Keep each client in its own Project**, with project-level memory. Don't put two clients'
playbooks in one knowledge base. Incognito isn't a replacement for this.

## 9. Writing Project instructions that work

The official objectives say "Create effective system-level instructions" (exam wording). Our
explanation: on claude.ai, the Project instructions are the Associate's version, because they
apply to every chat in the Project. Good ones are
short, specific and testable. A useful shape:

```text
Role: You help the vendor team write onboarding summaries for the ops manager.
Always use: the playbook and the risk template in this Project's knowledge.
Output: the template's five headings, under one page, plain English.
Flag: any contract term the playbook doesn't cover, and any number you couldn't check.
Never: set a final risk rating or send anything. A person decides and sends.
If a file you need is missing or out of date, say so instead of guessing.
```

What makes it work:

- **Rules, not wishes.** "Flag variance over 10%" can be checked. "Be thorough" can't.
- **Point at the knowledge by name**, so Claude uses the right file.
- **Say what to flag and what to refuse**, not just what to produce.
- **Keep one-off requests out.** This week's special format goes in the prompt, not the
  instructions.
- **Test and version it.** Run 3 real requests after any change, and tell the people who share
  the Project what changed (section 4).

Memory and account custom instructions need the same care. Review Memory about monthly and remove
anything that's stale, and keep account custom instructions to style rules you want in *every*
chat, not rules for one job.

## 10. Worked example

A recruiting coordinator runs a Project called "Interview Scheduling Emails". Last month the
company changed its interview policy from four rounds to three. Now Claude's drafts sometimes say
"four rounds" and sometimes "three", the tone varies between people and a new colleague's Claude
can't see the shared calendar folder in Drive.

Work it layer by layer (section 2):

1. **Knowledge:** both the old and new policy files are in the Project. Remove the old one, keep
   `Policy_Interview_v2026-08.pdf`, and point the instructions at it by name (section 5).
2. **Instructions:** they say "friendly tone", and people add "be formal" in their prompts. Agree
   on one tone, write it into the instructions with a few (3–5) sample emails as examples, and stop
   overriding it in prompts (section 6, section 9).
3. **Connector:** the new colleague doesn't have access to the Drive folder. Claude can't see what
   they can't see, so fix the Drive access, then check the connector is on (section 7).
4. **Tell the team** what changed in the shared Project (section 4).

Switching to Opus fixes none of these. Neither does typing "use the new policy" every time.

## 11. Traps

- **This week's file in Project knowledge.** Changing data goes in the chat or comes through a
  connector. Knowledge is for stable reference.
- **Adding v2 and leaving v1.** Claude may quote either. Replace the old file the same day.
- **Rules scattered across layers.** A style rule in account instructions, a different one in the
  Project and a third in the prompt give inconsistent output. Put each rule in one layer.
- **Assuming a connector sees everything.** It inherits each user's permissions, so two colleagues
  can get different results from the same Project.
- **Two clients in one Project.** Their files and memory can leak into each other's answers. Use
  separate Projects.
- **Editing a shared Project silently.** Colleagues see the behavior change with no explanation.
  Announce changes and keep one owner.

## Try it (20 min, in Claude)

Build a real Project for one recurring job. Use a clear name, 5–10 lines of instructions, two
stable files named with versions, and only the connectors it needs. This is steps 1–4 of
[Lab 01](../../06-Labs/01-CCAO-F-engagement-project/README.md). Then go on to lab step 5 and run
it on 5 inputs.

## Done when

- [ ] You can fill in the "what goes where" table from memory
- [ ] You can explain the old-policy fix and why the three distractors are wrong
- [ ] You scored 80% or more on [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Sources: official exam guide v1.0, Domain 5 objectives (Tier 1); course Modules 1 and 5 (Tier 1,
copy); `…/public-docs-fetch/05-configuration-and-knowledge-management.ocr.txt` (Tier 2, including
"Skills need Code Execution"; check the current docs). "Project instructions play the role of the
system prompt" (section 9) is our own explanation.