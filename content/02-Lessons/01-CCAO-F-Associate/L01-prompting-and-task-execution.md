# CCAO-F Lesson 1 — Prompting and Task Execution (14%, about 8–9 questions)

Last reviewed: 2026-09-29

**Time:** 60 min · **AI Fluency:** *Description* · **Practice:** [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Exam wording (exam guide v1.0, Domain 1):**

- Create effective prompts for business and technical tasks
- Apply task decomposition techniques to structure complex requests
- Iterate prompts to improve output quality
- Adapt prompting strategies based on task type (analysis, research, drafting, brainstorming)

## 1. The big idea

Brief Claude the way you'd brief a **brilliant new colleague who knows nothing about your
situation**. The test: if a coworker with no background couldn't do the job from your prompt,
Claude can't either.

## 2. The parts of a professional prompt

| Part | What it does | Example |
| --- | --- | --- |
| Role | Sets the expertise and what "good" means | "You are a skeptical financial controller…" |
| Goal / task | An action verb plus the object | Write, Analyze, Extract, Compare |
| Context / why | Lets Claude make good choices you didn't spell out | "This goes to the board, who have 8 minutes." |
| Constraints | Length, must and must-not, allowed sources, tone | Say what *to do* ("write in flowing prose"), not only what not to do |
| Inputs | Documents and data, kept separate from instructions | `<documents>…</documents>` tags |
| Examples | Show the format and tone. **3–5 relevant, varied examples** (Anthropic's prompting guide, Tier 1: "Include 3–5 examples for best results"). | Claude copies the details of your examples, so make them clean |
| Process | Steps, when order matters | "1. Quote the relevant passages. 2. Then analyze." |
| Output format | The shape of the result | "A table with columns X, Y, Z", or "an Artifact" |
| Uncertainty rule | Permission to say "I don't know" | Cuts down on made-up facts |
| **Success criteria** | How you'll accept the work | **An exam favorite** |

**Long documents:** put the document **first** and the question **last**, and ask Claude to
**quote first, then analyze**.

**Say it directly when you want action:** "Change this", "create the Artifact", "search the
web". "Can you suggest…" may only get suggestions.

## 3. Breaking work into steps (decomposition)

Split the job when there are several deliverables, mixed modes (research, then draft), a quality
step that depends on an intermediate result, or a human checkpoint in the middle.

| Pattern | Use when |
| --- | --- |
| Outline, then draft | Long documents |
| Quote, then analyze | Analysis grounded in a source |
| Rubric, then score | Classification and review |
| Generate, then critique | Writing where quality matters |
| Research, then synthesize | Current information |
| Plan on a stronger model, execute on a faster one | Heavy workflows |

**Exam tell:** "Break it into steps with a review gate" beats "one longer prompt that does
everything".

## 4. Iterating like a professional

1. Run it against success criteria you wrote in advance.
2. **Name the failure:** wrong format, missing section, invented fact, wrong tone, ignored
   constraint.
3. **Change one thing:** add an example, move the question to the end, add "quote first", add
   permission to be uncertain, or split the task.
4. Test again on the same input plus one edge case.

If three edits don't help, the problem probably isn't the prompt (see [L07](L07-troubleshooting-and-optimization.md)).

## 5. Adapting to the task type

| Type | Emphasize | Extras |
| --- | --- | --- |
| Analysis | Role, rubric, quote first | "Separate facts, inferences and recommendations. What would change the conclusion?" |
| Research | Scope, sources, recency, citations | Turn on web search or Research, and allow "not enough sources" as an answer |
| Drafting | Audience, tone, length, a sample of the voice | Use an Artifact and edit in place |
| Brainstorming | Quantity, variety, don't judge yet | Ask for N distinct options, then evaluate them in a second pass |

## 6. Worked example

**Weak:** "Summarize these notes."

**Strong:** "You are a program manager writing for a busy VP. Goal: a one-page status they can read
in 3 minutes. They care about schedule, budget and the decisions they need to make.
`<notes>…</notes>`. 1) Pull out only the items that affect the timeline or budget, or that need a
decision. 2) If the notes don't cover one of those, write 'Not in notes'; don't invent anything.
3) Flag any ambiguous date or number. Use these headings: status (Red/Amber/Green and why),
progress, risks, decisions needed (with owner and date), open questions. Success means there are no
facts that weren't in the notes."

### 6.1 Why the strong prompt wins

Map it back to the table in section 2:

- "program manager writing for a busy VP" = **role** and audience (context)
- "one page … in 3 minutes" = **constraint**
- the numbered steps = **process**
- "write 'Not in notes'; don't invent anything" = **uncertainty rule**
- the list of headings = **output format**
- "no facts that weren't in the notes" = **success criteria**

The weak prompt has none of these, so Claude has to guess all of them.

## 7. Traps

- "Make the prompt longer or more polite" when the real issue is a missing success criterion.
- Choosing *zero-shot vs few-shot* jargon over what actually fixes the problem. (Zero-shot = no
  examples; few-shot = with a few examples.) The exam asks what fixes the problem, not what it's
  called.
- You **don't** need API system prompts (standing instructions a developer sets in code) or
  "prefill" (starting Claude's answer for it). Those are developer tools, and this exam has no
  code or API. On claude.ai, the Project instructions play the role of the system prompt (our
  explanation).

## Try it (15 min, in Claude)

Take one prompt you really used this week and rewrite it using the table in section 2. Run both
versions and write one line on what changed.

## Done when

- [ ] You can list the prompt parts from memory, including **success criteria**
- [ ] For each of the 6 patterns in section 3, you can give one work task it fits
- [ ] You scored 80% or more on a [practice-tool drill](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) for this domain

Sources: CCAO-F exam guide v1.0, Domain 1 objectives (Tier 1); course Module 2 (Tier 1, copy);
Anthropic's prompting best-practices page, saved at
the reference library (in the study workspace)
(Tier 1; "Include 3–5 examples", long documents first, quote first; public copy:
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices);
`…/public-docs-fetch/01-prompting-and-task-execution.ocr.txt` (Tier 2).