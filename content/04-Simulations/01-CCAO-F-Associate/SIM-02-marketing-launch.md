# CCAO-F SIM-02 — Marketing launch brief

**Domains:** 3 Product and Model Selection (4), 2 Output Evaluation (2), 1 Prompting (2) ·
**Decisions:** 8 · **Pass:** 7 of 8 · **Time:** 16 min

Last reviewed: 2026-09-29

## Scene (read it yourself, or have Claude read it)

You're a marketing manager at a mid-size software company. In 3 weeks you launch a new analytics
add-on. You have to produce a competitive landscape, a launch messaging brief, 20 short
social-post variants, and a one-page summary for the VP of Marketing. The VP will act on that
summary directly, and it has to weigh three analyst reports on the market that disagree with each
other. The team uses Claude on a Team plan with web search, Research, Projects, Artifacts, Code
Execution and a Google Drive connector. The brand voice guide and last year's launch brief are in
Drive.


---

## The decisions (answer these before you open the key)

1. **Setup:** Where to do 3 weeks of launch work
2. **Competitors:** Competitor moves in the last 90 days, with sources
3. **Check:** The report says a competitor "cut prices 30% in August". You open the source: it says 30% off one plan, in one region, for a limited time.
4. **Brief:** Weak prompt: "write launch messaging"
5. **Social posts:** 20 short, varied posts
6. **Model:** The VP summary must weigh three analyst reports that disagree, and the VP acts on it directly
7. **Format:** A standalone brief you'll revise several times and share for comment
8. **Drift:** After 50 turns, the posts ignore the voice guide

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Stage | Decision | Correct move | Why | Traps to use as distractors | Domain · objective | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Setup | Where to do 3 weeks of launch work | **A Project** with the voice guide and last year's brief as knowledge, plus instructions for audience and tone | Recurring work with stable context belongs in a Project. | A new chat each time, pasting the voice guide in · one long chat for all 3 weeks · the voice guide in account-level custom instructions | 3 · Select appropriate Claude product features (Projects, research mode, chat, artifacts) | [Lesson 3, section 2](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md), [Lesson 5, section 2](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md) |
| 2 | Competitors | Competitor moves in the last 90 days, with sources | **Research** (web search on), asking for citations and dates | Many recent sources with citations is Research's job. | A thinking mode on what Claude already knows · relying on the model's own knowledge · uploading last year's analysis and asking for an update | 3 · Select appropriate Claude product features (Projects, research mode, chat, artifacts) | [Lesson 3, section 3](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md) |
| 3 | Check | The report says a competitor "cut prices 30% in August". You open the source: it says 30% off one plan, in one region, for a limited time. | **Narrow the claim to what the source says**, or mark it unverified | A citation supports only what it actually says. | Keep it, because the source exists · delete the whole competitor section · ask Claude to find a second source that says 30% | 2 · Apply fact-checking and validation techniques | [Lesson 2, section 4](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md), [Lesson 2, section 5](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 4 | Brief | Weak prompt: "write launch messaging" | Add **the audience, the goal, the voice guide's constraints, the output headings and success criteria** | Claude can't guess the reader or what good looks like. | Make it longer and more polite · add "be creative and on-brand" · ask Claude to write the prompt and use it unread | 1 · Create effective prompts for business and technical tasks | [Lesson 1, section 2](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md) |
| 5 | Social posts | 20 short, varied posts | **Say how many and ask for variety** (brainstorm mode), with **a few (3–5) clean, varied on-brand example posts**; judge them in a second pass | A count plus varied examples steers range; judging separately keeps quality. | Ask for one post at a time, 20 times · ask for "some posts" with no variety instruction and pick the best · give one example post and ask for 20 like it | 1 · Adapt prompting strategies based on task type (analysis, research, drafting, brainstorming) | [Lesson 1, section 2](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md), [Lesson 1, section 5](../../02-Lessons/01-CCAO-F-Associate/L01-prompting-and-task-execution.md) |
| 6 | Model | The VP summary must weigh three analyst reports that disagree, and the VP acts on it directly | **Opus** | Conflicting inputs and a high-stakes reader need the most capable of the three. | Haiku, since it's only one page · the same model as the posts, for consistency · turn on Research, because the inputs conflict | 3 · Align model selection with task requirements (cost, speed, quality) | [Lesson 3, section 5](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md) (question 2) |
| 7 | Format | A standalone brief you'll revise several times and share for comment | **An Artifact** (versions are kept, and it's shareable) | Standalone content you'll revise and share fits an Artifact. | Inline chat text · paste it into the Project instructions · start a new chat for each revision | 2 · Organize and curate information and select appropriate output formats (artifacts, inline, structured data) | [Lesson 2, section 7](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 8 | Drift | After 50 turns, the posts ignore the voice guide | **Summarize the decisions so far, then start a new chat in the Project** (the instructions and knowledge carry over) | Long threads drift; a fresh chat reloads the instructions and knowledge. | Paste the voice guide again in the same thread · switch to Opus · add "IMPORTANT: follow the voice guide" to every message | 3 · Understand and manage context limitations and memory considerations (when to restart, summarize, or persist) | [Lesson 3, section 6](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md), [Lesson 7, section 2](../../02-Lessons/01-CCAO-F-Associate/L07-troubleshooting-and-optimization.md) |

**Runner note (decision 2):** don't offer plain web search as a wrong option; L03 treats it as a
fair pick for recent news. Use "one web search for competitor news" only if it's framed as a single
lookup.

**Scoring:** one point per decision. 7 or more is a pass. For each miss, name the lesson section.

</details>