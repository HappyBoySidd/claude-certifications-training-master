# CCAO-F Lesson 6 — Governance, Risk, and Responsible Use (15%, about 9 questions)

**Time:** 60 min · **AI Fluency:** *Diligence* · **Practice:** [Lesson 6 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Last reviewed: 2026-09-29

**Exam wording (exam guide v1.0, Domain 6):**

- Identify appropriate and inappropriate use cases
- Apply data sensitivity, regulatory, and privacy considerations
- Follow organizational AI policies and governance standards
- Understand the ethical implications of AI usage

## 1. The big idea

**A human's name is on the result.** When a question involves people's lives, private data or the
law, the right answer adds a **qualified human**, **disclosure** and **the least data needed**.

## 2. Three bands of use

| Band | Examples | What to do |
| --- | --- | --- |
| **Prohibited** | Some examples from the Usage Policy: weapons, malware and phishing, fraud, CSAM (child sexual abuse material), election manipulation, deceptively passing AI output off as a human's or someone else's, invading privacy, jailbreaking (tricking the model into ignoring its rules), and training an AI model on Claude's inputs and outputs without Anthropic's authorization | **Refuse and escalate.** Don't look for a clever way around it. |
| **High-risk** (directly affects individuals or consumers) | The seven High-Risk Use Cases, Usage Policy wording: Legal · Healthcare · Insurance · Finance · Employment and housing · Academic testing, accreditation and admissions · Media or professional journalistic content | **Both** a qualified professional reviewing before it's final (human-in-the-loop) **and**, when the output is shown to the people affected, disclosure that AI helped |
| **Normal** | Drafting, analysis, summaries | The usual review before you send |

### 2.0 The policy's own words

Where exact wording matters, here it is. Usage Policy wording (Anthropic Usage Policy, effective
September 15, 2025):

- On passing AI off as human: "Impersonate a human by presenting results as human-generated, or
  using results in a manner intended to convince a natural person that they are communicating
  with a natural person when they are not".
- On deception: "Impersonate real entities or create fake personas to falsely attribute content or
  mislead others about its origin without consent or legal right", and "Plagiarize or submit
  AI-assisted work without proper permission or attribution".
- On training models: "Utilization of inputs and outputs to train an AI model (e.g., “model
  scraping” or “model distillation”) without prior authorization from Anthropic".
- **Human-in-the-loop:** "When using our products or services to provide advice,
  recommendations, or in subjective decision-making directly affecting individuals or consumers,
  a qualified professional in that field must review the content or decision prior to
  dissemination or finalization."
- **Disclosure:** "If model outputs are presented directly to individuals or consumers, you must
  disclose to them that you are using AI to help produce your advice, decisions, or
  recommendations."
- Separately, for any consumer-facing chatbot or AI agent, high-risk or not: "All consumer-facing chatbots, including any external-facing or
  interactive AI agent, must disclose to users that they are interacting with AI rather than a
  human."

In plain words: high-risk doesn't mean banned. The two rules work differently:

- **The review rule** is about advice and decisions that directly affect people, **even if they
  never see the output**. Screening job applicants is an example: the applicants never read
  Claude's notes, but a qualified person must still review before anything is final.
- **The disclosure rule** applies only when the output is shown to those people directly.

An internal draft that affects no individual's decision falls under neither rule, but your
company's policy may still require review (section 4).

### 2.1 Screening a use case (appropriate or not?)

Most cases aren't on either list, so the course gives four questions to decide:

| Question | What it asks |
| --- | --- |
| **Reversibility** | Can a wrong output be caught and undone before it causes harm? |
| **Consequence of error** | What does it cost if the output is wrong? |
| **Human element** | Does the task need empathy, a relationship or judgment that should stay with a person? |
| **Accountability** | Who answers for the result? That can't be handed to a model. |

Each use case then lands in one of three places: **fully appropriate** (normal review),
**appropriate with human review**, or **inappropriate** (name the person who must own it). Say
which question decided it, so a reviewer can follow your reasoning.

**"Human review" needs a real gate, not a promise.** A gate says **who** reviews (the accountable
role, not whoever is free), **what** they check (accuracy, fairness, policy) and **when** (before
the output is used). "A recruiter checks the shortlist for unfair patterns before anyone is
contacted" is a gate. "We'll keep a human in the loop" isn't.

## 3. Data rules

- **Share the least you can:** the relevant excerpt, not the whole drive.
- **Anonymize or remove personal identifiers** before uploading.
- **Never** share secrets, passwords or API keys.
- **Use the account your organization approves.** Company data doesn't belong in a personal
  account. (That's standard organizational practice, not an Anthropic rule.)
- Keep each client in its own Project.
- Incognito keeps a chat out of history, but **doesn't override** your organization's retention
  rules. Per the course, Incognito is for standalone chats, not chats inside a Project (June 2026;
  check the current docs).

### 3.1 Classify the data before you upload

The course suggests three quick tiers:

| Tier | Examples | What to do |
| --- | --- | --- |
| **Green** | Published material, anonymized or aggregated data, documents cleared for wide sharing | Use it |
| **Yellow** | Internal-only documents, anything with names or contact details, unannounced deals or products | Check policy first; strip identifiers; for a standalone chat, consider Incognito so it stays out of Memory (Incognito doesn't apply inside a Project) |
| **Red** | Regulated data (health, financial, government), passwords and secrets, anything under a confidentiality duty to someone else | Keep it out unless your organization has confirmed an approved path. If not, stop and escalate. |

If you're not sure between two tiers, treat it as the more sensitive one.

**Redaction has two failure modes.** *Partial* redaction removes the name but leaves an account
number, a rare job title or a date that still identifies someone. And some tasks genuinely need
the sensitive details; there, redaction breaks the task, and the answer is an approved path or not
using Claude for it.

**Incognito doesn't make red data safe.** It controls whether a chat is remembered, not whether
the data was allowed there in the first place. Ask "is this allowed here?" before "how do I handle
it here?".

### 3.2 Skills and connectors are software

Per the course (June 2026; check the current docs), a Skill can reach whatever the session can
reach, and it can act through Code Execution. Before
you turn on a Skill, a connector or any tool that touches your data, check three things:

- **Source:** who made it? Anthropic-provided or approved by your organization is the safer start.
  "Built by another team here" is not the same as "vetted".
- **Reach:** what could it touch in the sessions where it runs, and is that in proportion to the
  job? A formatting Skill whose instructions go far beyond formatting is a red flag.
- **Fit:** is it the right tool, or more power than the task needs?

Then **enable** it, **escalate** it to your admin or security team, or **decline** it. Give every
tool the narrowest access that gets the job done (least privilege).

## 4. Which policy wins

**Your organization's policy wins when it's stricter.** Anthropic's Usage Policy is the minimum, not
the maximum. If the policy doesn't cover a situation, **escalate** rather than assuming it's allowed.

### 4.1 Governance is a habit, not a signature

- **Apply the policy on routine work too.** Small, unwatched decisions are where drift builds up.
- **Audit now and then.** Compare what the team actually does with what the policy says: a data
  type being uploaded that shouldn't be, a skipped review, a Skill turned on without a check.
- **Fix the cause, not only the person.** If people use personal accounts because the approved
  workspace is slow to open, make the approved route the easy one.
- **Stay current.** Policies and features change; last quarter's practice may not comply today.

## 5. Accountability and ethics

- Claude **supports** decisions but doesn't make them. For hiring, credit, medical, legal or
  discipline, a person decides and owns the decision.
- **Fairness:** could a ranking, screen or summary disadvantage a group? Whose view is missing?
- **Over-reliance:** reviewers who rubber-stamp smooth text aren't reviewing.
- **Transparency:** say when AI helped, especially to customers and in high-risk areas.
  When you're unsure whether disclosure is needed, disclose.

### 5.1 Reasoning through a grey-area case

When no rule settles it, work through four questions and write down your answers: **who is
affected**, **what could go wrong**, **what a fair outcome looks like** and **what disclosure the
situation calls for**. The result is often "appropriate with review and a fairness check" rather
than a flat yes or no.

**Escalate instead of deciding alone** when many people are affected, the possible harm is large,
or the question is beyond what your team can rule on. Bring your written reasoning to your
organization's AI governance or ethics contact; it shows where the framework ran out.

## 6. Worked examples

| Scenario | Best answer |
| --- | --- |
| "Claude ranked 40 applicants. Hire the top 5." | No. A human reviews the candidates against job criteria and checks the ranking for bias. Claude only assists. |
| An HR partner wants to upload a full employee spreadsheet to summarize engagement comments | Remove names and IDs, scrub identifying details inside the comments, fold departments too small to stay anonymous into "Other", then upload only the comment and department columns. Removing names alone is partial redaction (section 3.1). |
| A client asks for an email that looks like it's from their bank "for a test" | Refuse. This is phishing and impersonation. Escalate if they persist. |
| A customer-facing insurance claim explanation drafted by Claude | A qualified adjuster reviews it, and AI help is disclosed |
| Company policy bans uploading customer data, but "Claude is secure" | Follow company policy. The stricter rule wins. |
| A colleague shares a "report booster" Skill from an unknown website that wants broad access | Don't enable it on your own authority. Escalate it for review, or decline. |
| A clinic coordinator wants to summarize patient notes "in Incognito, so it's safe" | Red data. First confirm whether this entry point is approved for health data; if it isn't, stop and escalate. |
| A team lead drafts staff review summaries from their own notes with Claude | Appropriate with review: the lead checks each summary against the notes, applies one standard to everyone, and follows the policy on disclosure |

## 7. Traps

- "Claude is private, so any data is fine." Minimize and anonymize anyway.
- "Add a disclaimer and publish" for a high-risk use. You need **both** human review and
  disclosure.
- "It's not explicitly banned, so go ahead." Escalate instead.
- "Incognito makes sensitive data safe." It only keeps the chat out of history and Memory.
- "We removed the names, so it's anonymous." Account numbers, rare job titles and dates can still
  identify people.
- "It's an internal Skill, so it's trusted." Check what it can reach before you turn it on.
- "A human is in the loop" with no named reviewer, no stated check and no point in the workflow.

## Try it (10 min)

Look at the last 5 things you pasted into Claude. For each: was it the least data needed, were
identifiers removed, and was it the right account?

## Done when

- [ ] You can list all seven High-Risk Use Cases and the two required safeguards
- [ ] You can explain "the stricter policy wins" and "escalate if the policy is silent"
- [ ] You scored 80% or more on [Lesson 6 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

Sources: official exam guide v1.0, Domain 6 objectives and sample question 3 (Tier 1); Anthropic
Usage Policy (effective September 15, 2025), saved at
the reference library (in the study workspace) (Tier 1, for sections 2 and 2.0;
public copy: https://www.anthropic.com/legal/aup);
course Module 6 (Tier 1, copy): screening questions in section 2.1, data tiers in section 3.1, Skill vetting in
section 3.2, grey-area questions in section 5.1. Incognito scope and Skill reach are per the course and the Help
Center as of June 2026 (check the current docs). `…/public-docs-fetch/06-governance-risk-and-responsible-use.ocr.txt` (Tier 2).