# CCAO-F Lesson 3 — Product and Model Selection (12%, about 7 questions)

**Time:** 60 min · **Practice:** [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Last reviewed: 2026-09-29

**Exam wording (exam guide v1.0, Domain 3):**

- Select appropriate Claude product features (Projects, research mode, chat, artifacts)
- Differentiate between Claude model types (Haiku, Sonnet, Opus)
- Align model selection with task requirements (cost, speed, quality)
- Understand and manage context limitations and memory considerations (when to restart, summarize, or persist)

## 1. The big idea

Every task needs three picks: **where** to work, **which tool** to switch on and **which model** to
run. The right answer is the simplest, cheapest setup whose output you'd actually ship. A bigger
model never makes up for the wrong place or a worn-out conversation.

## 2. Where to work

| Entry point | What it is | Choose when |
| --- | --- | --- |
| **Chat** | A single thread | A one-off, with no plan to reuse the setup |
| **Project** | Standing instructions plus knowledge, with its own chat list | Recurring work with stable background and a consistent format. **If 2 of those 3 are true, build a Project.** |
| **Artifact** | A window for a standalone deliverable | Something you'll edit, reuse or share |
| **Research** | Multi-step search over the web and your connected sources, with citations | Deep, multi-source work. It runs many searches and usually takes a few minutes. Rule of thumb: 5 or more lookups. Needs web search turned on; paid plans only (Tier 2; per the Help Center as of mid-2026, check the current docs). |

Project facts:

- Chats in a Project share its instructions and knowledge, but **not** each other's thread.
- The Free plan allows up to 5 Projects (Tier 2; per the Help Center as of mid-2026, check the
  current docs).
- On paid plans, when the knowledge gets large, Claude searches the files for the relevant parts
  instead of reading them all at once. This is called **retrieval**, and it gives about 10 times
  the capacity (Tier 2; per the Help Center as of mid-2026, check the current docs).

**Chat or Artifact?** Short answers and lists you'll paste somewhere stay inline in the chat.
Something substantial that stands on its own (a rule of thumb is more than about 15 lines) and
that you'll edit or share goes in an Artifact. If you need a real spreadsheet, slide deck or
document file, that's Code Execution (section 4), not an Artifact.

## 3. Web search, thinking or Research

| Need | Pick |
| --- | --- |
| One current fact ("who won last night") | **Web search** |
| Hard reasoning on material already in front of Claude | **Extended thinking** |
| A multi-source report with citations | **Research** |
| A proposal on a new technology from many papers plus the web | Research **and** thinking |

If Research sits idle, say "use the research tool". If it ignores Drive, say "pull the relevant
context from Google Drive".

The quick test: **is the answer outside Claude, or inside the material you already gave it?**
Outside and small means web search. Outside and big means Research. Inside means thinking. None of
the three fixes a missing file; you have to supply that.

**Check the current docs on the name.** The course calls it "extended thinking". Anthropic's
models page now says current models use *adaptive thinking*, so the toggle in claude.ai may have
a different name. The idea is the same: Claude reasons harder over what it already has.

## 4. The capability layer

| Layer | Its job |
| --- | --- |
| Project knowledge | Stable reference files |
| Project instructions | How to behave every time in this space |
| **Skill** | A repeatable procedure that loads only when relevant. It **needs Code Execution** (Tier 2; per the Help Center as of mid-2026, check the current docs). |
| **Code Execution** | Real formulas, files, charts and correct calculations |
| Memory | Who you are, your preferences, ongoing work. Project memory is kept separate for each Project. |
| Connectors | Live data from Drive, Gmail, Slack and so on. Claude sees **only what you can see.** |

The difference: Projects hold background that's always loaded, and Skills hold procedures loaded on
demand. Connectors give Claude *access* to tools and data; Skills teach it *how* to do a task.

## 5. Models: the exam uses three tiers

| | Haiku | Sonnet | Opus |
| --- | --- | --- | --- |
| Character | Fastest and cheapest | Balanced; the course treats it as the default | The most capable of the three, and usually slower |
| Fit | Structured, high-volume work where a mistake costs little | Most professional work | Complex, ambiguous, high-stakes judgment |
| Example | Classify 500 contracts on a clear rubric | A weekly narrative status | A 15-page board paper from conflicting reports |

- **Efficiency first:** start with Haiku or Sonnet and move up only if quality fails.
- **The right model is the cheapest one whose output you'd actually ship.**
- **Trap:** "It's legal, so use Opus." If the rubric is clear and the volume is high, Haiku is the
  right choice.
- **"Sonnet as the default" is the course and exam framing.** Anthropic's API models page now
  says to start with Opus 5.5 for most workloads. That's version-sensitive developer advice; for
  this exam, use the guide's rule: faster, cheaper model for high volume, most capable model for
  complex reasoning.
- **Fable:** a course note (as of June 2026) says a fourth tier, Claude Fable, sits *above* Opus.
  Anthropic's models page also lists it. The exam uses only Haiku, Sonnet and Opus.

**Three questions that pick the model** (the cost, speed and quality trade-off in the official
objectives):

1. **How many?** Hundreds of similar items push you toward Haiku, because cost and speed add up.
2. **How clear is the rule?** A fixed rubric or format means a smaller model can follow it. Messy,
   conflicting inputs that need weighing push you toward Opus.
3. **What does a mistake cost, and who catches it?** A human review catches mistakes whichever
   model you use. A high-stakes call with little review time justifies Opus.

The official exam guide's own sample on this domain describes exactly this pattern: lots of short,
straightforward drafts where speed and cost matter most point to the faster, cheaper model.

## 6. Context is a budget

**Signs it's degrading:** Claude stops following earlier instructions, answers only the last turn,
or gets less accurate.

| Move | When |
| --- | --- |
| **Restart** (a new chat in the Project; the instructions and knowledge carry over, the thread doesn't) | Drift you can't recover from, or a genuinely new task |
| **Summarize**, then restart | You need continuity without the degraded thread |
| **Save it** to Memory or Project knowledge | It should be true in every future session |

A 2-hour analysis that has drifted needs **summarize, then restart**. Switching to Opus doesn't fix
it, turning on Research doesn't fix it, and neither does repeating the framework in the same thread.

**Incognito** keeps a chat out of history and Memory. It doesn't override your organization's
retention rules, and it's **not** a substitute for separate Projects for separate clients. Per the
course, Incognito is for standalone chats, not chats inside a Project (check the current docs).

## 7. Combined example (this is how questions are built)

**Walk one first.** 800 survey responses; you need favorability rates by department and a flag on
anything under 60%.

1. **Entry point: a chat.** It's a one-off, so a Project's setup would be wasted.
2. **Capability: Code Execution.** It's counting and percentages. Claude's head-math can't be
   trusted for that; code actually calculates it.
3. **Model: Haiku or Sonnet.** Many items, a clear rule, and a slip is cheap because code does the
   math and you check the totals.
4. **Context: a fresh chat** with just the file. Nothing from older threads is needed.

Now the rest, quickly:

| Scenario | Answer |
| --- | --- |
| Monthly budget variance: flag anything over 10%, in the standard template | Project, Code Execution and a Skill, with Sonnet |
| Competitor moves in the last 90 days | Research or web search, with Sonnet |
| A one-off vendor reply, with the policy PDF in hand | Chat and an Artifact, with Sonnet |
| 800 survey responses: rates by department, flag anything under 60% | Code Execution, with Haiku or Sonnet |
| Two clients who must never mix | Separate Projects, each with its own memory |

## 8. Traps

- **"Important means Opus."** Importance is about review, not model size. A clear rubric at high
  volume is still Haiku or Sonnet work, with a human check where it matters.
- **A Project for a one-off.** If the task won't recur and the context won't be reused, the setup
  cost is wasted. Use a chat.
- **Research for one fact.** Research takes minutes and many lookups. One current fact is a web
  search.
- **Extended thinking to find new information.** Thinking reasons harder over what Claude already
  has; it doesn't fetch anything. For outside facts, use web search or Research. (The toggle may
  now be called adaptive thinking; check the current docs.)
- **Switching models to fix drift.** A long, drifted thread needs summarize and restart. A new
  model in the same thread inherits the same mess.
- **Incognito as client separation.** It keeps one chat out of Memory. Separate clients still need
  separate Projects.

## Try it (10 min)

Take 3 tasks from your week and fill in the four decisions for each: entry point, capability,
model and context.

## Done when

- [ ] You can justify Chat, Project, Artifact or Research in one sentence each
- [ ] Given the 5 scenarios in section 7 with the answers covered, you pick the right model for
      each and give the reason in one line
- [ ] You scored 80% or more on [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Sources: official exam guide v1.0, Domain 3 objectives and sample question 2 (Tier 1); course
Module 1 (Tier 1, copy), including the Fable note (as of June 2026) and Incognito scope;
Anthropic models overview, saved at the reference library (in the study workspace)
(Tier 1, for Fable, adaptive thinking and the API "start with Opus" advice);
`…/public-docs-fetch/03-product-and-model-selection.ocr.txt` (Tier 2: Free = 5 Projects, ~10×
retrieval, Research timing and plans, Skills needing Code Execution; check the current docs);
the Artifact 15-line rule of thumb and the Chat-or-Artifact split follow the study guide's Domain 2
notes (the reference library (in the study workspace), Tier 2).