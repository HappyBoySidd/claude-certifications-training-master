# CCAO-F Lesson 2 — Output Evaluation and Validation (21%, about 12–13 questions, the biggest domain)

**Time:** 90 min · **AI Fluency:** *Discernment* · **Practice:** [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Last reviewed: 2026-09-29

**Exam wording (exam guide v1.0, Domain 2):**

- Evaluate Claude-generated outputs for accuracy and completeness
- Identify hallucinations, inconsistencies, and biases in responses
- Apply fact-checking and validation techniques
- Determine when human review or additional verification is required
- Edit, adapt, refine, and compare outputs for the intended audience
- Organize and curate information and select appropriate output formats (artifacts, inline, structured data)

## 1. The big idea

**Smooth writing is not evidence.** A polished draft can still be wrong. Community study notes
(Tier 2) report that people who use Artifacts get better at *directing* Claude and worse at
*checking* it. This domain exists to catch that.

### 1.1 The whole lesson in one look

1. **Three lenses:** complete, accurate, fit (section 2).
2. **Three verdicts:** pass, revise, fail (section 3).
3. **Fact-check** what matters: sources, numbers, recency (sections 4–5).
4. **Know when a human must review,** and pick the right format (sections 6–7).

## 2. Three separate lenses

| Lens | Question | Example of a fail |
| --- | --- | --- |
| **Complete** | Did it cover the whole brief? | A beautiful summary that leaves out the risk section you asked for |
| **Accurate** | Are the facts and numbers true, and supported by the sources? | A believable statistic cited to a report that doesn't contain it |
| **Fit** | Right audience, tone, length and format? | A correct 12-page memo when the VP asked for 8 bullets |

An answer can pass one lens and fail another, and the exam mixes them up.

## 3. Pass, revise or fail

| Verdict | Meaning | Next step |
| --- | --- | --- |
| Pass | Meets the criteria, and claims are sourced or marked as Claude's own conclusion (an inference) | Ship it, with a disclosure if needed |
| Revise | The right shape, with fixable gaps | **Targeted edit.** Don't regenerate from scratch and lose the good 80%. |
| Fail | Wrong task, invented facts, a policy issue, or unverifiable numbers | Change the approach: a source, Code Execution, a human, or no AI |

### 3.1 Revising well: edit, adapt and compare

An accurate draft still isn't finished. The official objectives ask you to "edit, adapt, refine and
compare outputs for the intended audience". The course breaks the editing pass into three steps:

1. **Clarity.** Cut hedging and padding. Claude tends toward thoroughness; your edit adds
   precision.
2. **Tone.** Match the reader. The same content reads differently to a teammate, a client and a
   regulator.
3. **Formatting.** Shape it for how it will be read: scannable for an executive, detailed for the
   working team, clean for an outside reader.

**One analysis, several versions.** The facts stay fixed; the selection, depth and tone change.
An executive version leads with the decision and the impact. A team version keeps the method and
adds owners and next steps. An external version controls what's disclosed. Sending the same raw
draft to everyone serves no one.

**Compare before you edit.** When quality matters, get two or three drafts (separate runs, or a
second model) and pick the strongest base. Comparing is cheaper than rescuing a weak first
draft.

## 4. Spotting problems

- **Hallucinations:** numbers, quotes, URLs or section numbers that aren't in the source. "According
  to the attached policy…" when the policy doesn't say it. Recent dates without a search. Confident
  gap-filling instead of "Not in the notes".
- **Inconsistencies:** it contradicts an earlier paragraph or a file, totals don't add up, or it
  ignores a constraint from the prompt. Drift after a long chat is a *context* problem (L03, L07).
- **Bias:** whose view is missing? Was a stereotype treated as fact? Would the path disadvantage a
  group? Does it sound certain on a contested topic?

## 5. How to fact-check

1. Separate the kinds of claim: quoted fact, calculation, inference, recommendation.
2. Tie each fact to a file, connector or URL. **If you can't point to a source, it's unverified.**
3. **Recalculate numbers** with Code Execution or the original spreadsheet.
4. Check how recent it is: prices, regulations and news need search or Research.
5. Spot-check the claims that matter most: numbers, legal or medical statements, named people,
   "always" and "never".
6. For high-stakes work, compare two runs. If they keep disagreeing, verify outside Claude.
7. **Citations aren't proof.** You have to open them.

### 5.1 Build the check into the prompt

The cheapest fact-check happens before the output exists. Three prompt habits from the course cut
hallucinations at the source and make the rest easier to audit:

- **Allow "I don't know".** Without that permission, Claude is more likely to fill a gap with
  something invented.
- **Restrict it to your sources.** "Answer only from the attached files, and flag anything they
  don't cover."
- **Ask for citations you can trace:** the file and the section or page behind each claim. A
  citation you can't trace isn't a citation.

These habits reduce the checking you have to do; they don't replace it.

## 6. When a human must review

**Good practice:** review anything that goes out under your name. That's a professional habit,
not a Usage Policy rule.

**What the Usage Policy requires** is narrower. It applies to its "High-Risk Use Cases", and only
when the output directly affects individuals or consumers. Usage Policy wording (Anthropic Usage
Policy, effective September 15, 2025):

- **Human-in-the-loop:** "When using our products or services to provide advice,
  recommendations, or in subjective decision-making directly affecting individuals or consumers,
  a qualified professional in that field must review the content or decision prior to
  dissemination or finalization."
- **Disclosure:** "If model outputs are presented directly to individuals or consumers, you must
  disclose to them that you are using AI to help produce your advice, decisions, or
  recommendations."

The seven High-Risk Use Cases, Usage Policy wording:

**Legal · Healthcare · Insurance · Finance · Employment and housing · Academic testing,
accreditation and admissions · Media or professional journalistic content**

In plain words: advice or decisions about a person's legal matters, health, insurance, money,
job or home, or exam and admission results, plus content that's generated and published
automatically. For these, a qualified person checks it first, even when the people affected
never see the output. If the output is shown to them directly, they're also told AI helped. (Plain wellness advice, like sleep or exercise tips, is not in the Healthcare
category, per the policy.)

Also bring in a human when the output goes to a customer, regulator or board, when you can't
verify a key claim, when sensitive personal data is involved, or when sources conflict.

### 6.1 Four questions that set the review bar

| Ask | Raises the bar when… |
| --- | --- |
| **Stakes:** what does a mistake cost? | Money, reputation or a person's outcome is on the line |
| **Reversibility:** can it be undone? | It gets sent, filed or presented and can't be pulled back |
| **Audience:** who sees it? | It goes outside the team, to executives or to a regulator |
| **Regulation:** does a rule or contract govern it? | Law, contract or policy applies. AI help doesn't remove the obligation. |

An internal meeting agenda trips none of these; ship it after a quick read. A board summary with
figures trips three; it goes to a human reviewer and the numbers get recomputed, however clean it
looks.

**Know when to stop prompting.** If each new round barely changes the draft, more prompts won't
add the judgment that's missing. Hand it to a person for a fresh read. The signal is the flat
improvement, not a visible error.

## 7. Picking the format

| Format | Use for |
| --- | --- |
| Inline chat | Short answers, decisions, lists you'll paste into Slack |
| **Artifact** | Substantial, standalone content you'll edit, reuse or share. Rule of thumb: more than about 15 lines (Tier 2 notes, not an Anthropic limit). Versions are kept. |
| **Code Execution file** | Real .xlsx with formulas, .pptx, .docx or .pdf, or charts. Files up to 30 MB (Tier 2; per the Help Center as of mid-2026, check the current docs). |

### 7.1 Structured data and curated inputs

- **Structured output** means a table or a fixed set of fields that someone, or another tool, will
  use directly. Say the columns you want and what to put when a value is missing.
- **Format is a reliability choice.** A number written in prose is Claude's best guess. A number
  from Code Execution was actually calculated from the file, so you can trace and re-run it. The
  code can still have a bug, so check that totals match their line items.
- **Curate what goes in.** Organized inputs give organized outputs. Remove duplicate copies of the
  same file, label each input's role ("this is the approved policy; these are the draft
  replies"), and leave out material that isn't relevant. Noise in the input becomes noise in the
  output.

## 8. Worked example

Claude drafts a customer email saying "on-time delivery was 98.6% this quarter" from a messy
export. **Complete:** yes. **Accurate:** no, because 98.6% isn't in the data; it averaged the wrong
column. **Verdict:** fail on that number. Recompute it with Code Execution, revise the email, and
have the owner review it before sending. The **worst** answer is "it reads professionally, so send
it".

### 8.1 Second worked example

An office manager asks Claude, inside a Project holding the staff handbook, for a one-page FAQ on
the new hybrid-work rules for all 200 employees. The draft is friendly and well organized. Run the
three lenses:

- **Complete:** it covers office days and equipment, but skips the expense rules the manager asked
  for. That's a gap to fill.
- **Accurate:** it says "per section 4.2, staff may work abroad for up to 30 days". The handbook
  has no section 4.2 and says nothing about working abroad. That's a hallucination, and it's the
  claim that could cost the most.
- **Fit:** it's written for managers ("remind your team…"), but the readers are all staff.

**Verdict: revise, not fail.** The structure is good. Delete the invented claim, add the expense
section from the handbook, and rewrite it for staff. Then, because it goes to everyone and states
policy, have HR check it against the handbook before it's sent. Regenerating from scratch would
throw away the good parts, and "it came from our Project, so it's accurate" is wrong: a Project
reduces invented facts but doesn't prevent them.

## 9. Traps

- "Claude was very confident, so skip review." That's always wrong.
- "Ask Claude to rate its own confidence." Self-rating isn't a reliable check.
- "Reword it to sound more formal." That doesn't fix whether it's correct.
- Regenerating from scratch when a targeted edit would do.
- "It has citations, so it's checked." A citation you haven't opened proves nothing.
- "It's accurate, so it's done." Accurate but written for the wrong reader still fails the fit
  lens.
- Sending one raw draft to every audience instead of adapting it.
- Trusting a total in a table without checking it matches the line items.

## Try it (20 min)

Take 5 real Claude outputs from your work. For each, write *complete, accurate and fit* verdicts
plus pass, revise or fail, and say what you'd do next. This is the grading step of
[Lab 01](../../06-Labs/01-CCAO-F-engagement-project/README.md), which also uses 5 outputs.

## Done when

- [ ] You can list all seven High-Risk Use Cases and the two safeguards (human-in-the-loop, disclosure) from memory
- [ ] You can name the three lenses and the three verdicts
- [ ] You scored 80% or more on [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html). **Do this one twice**, because it's the biggest domain.

Sources: official exam guide v1.0, Domain 2 objectives and sample question 1 (Tier 1); course
Module 3, screens 4–7 (Tier 1, copy); Anthropic Usage Policy, "High-Risk Use Case Requirements",
saved at the reference library (in the study workspace) (Tier 1; public copy:
https://www.anthropic.com/legal/aup);
`…/public-docs-fetch/02-output-evaluation-and-validation.ocr.txt` (Tier 2, including the Artifacts
note in section 1, the 15-line rule of thumb and the 30 MB limit).