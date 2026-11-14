# CCAO-F Lesson 0 — Orientation: how this exam thinks

Last reviewed: 2026-09-29

**Time:** 30 min · **Do first:** the cold baseline mock (step 4 in Try it)

## 1. The big idea

**The exam tests judgment in workplace stories, not features.** Almost every question is a
colleague with a job to do. You pick the move a careful professional would make.

## 2. What you're preparing for

- 60 questions in 120 minutes. The pass mark is 720 on a 100–1,000 scale, and the fee is $99.
- Most questions have one answer. Some ask for more than one, for example "select two". Exam
  wording (exam guide v1.0, section 5, Item format): each item "states how many responses to select".
- It's all **workplace stories**. There's no code and no API. A colleague who passed (field
  report, F) said to expect "lots of sequencing questions and scenario-based questions focused on
  non-technical personas".

### 2.1 Words you'll see

| Word | Plain meaning | Taught in |
| --- | --- | --- |
| Project | A workspace in Claude with standing instructions and files you upload once | L03, L05 |
| Artifact | A separate panel for a longer piece of work you edit, reuse or share | L02, L03 |
| Research | A mode where Claude runs many web searches and writes a cited report | L03 |
| Code Execution | Claude runs real code, so numbers are calculated, not guessed | L02, L07 |
| Skill | A saved, reusable set of instructions for one task | L03, L05 |
| Connector | A link that lets Claude read a tool like Google Drive or Gmail | L05 |
| Memory | Claude remembering facts about you across chats | L03, L05 |
| AI Fluency / 4D | Anthropic's course framework: four skills for working with AI (below) | this lesson |
| "The course" | The CCAO-F prep path on the Partner Academy | all lessons |
| Cold mock | A full timed practice exam taken before you study | this lesson |
| Blueprint | The exam guide's table of the seven domains and their weights | this lesson |

## 3. The four decisions behind almost every question

Before you choose an answer, name these four. Course wording (Module 1): "Four decisions determine
the quality ceiling for every Claude session."

1. **Entry point:** Chat, Project, Artifact or Research?
2. **Capability:** web search, thinking, Code Execution, a Skill, a connector, Memory?
3. **Model:** Haiku, Sonnet or Opus?
4. **Context:** carry on, summarize, restart, or save the fact?

Then add a fifth: **what's the check?** That could be verifying the facts, a human review, or Code
Execution for numbers.

## 4. The 4D frame (from AI Fluency)

| D | Question | Main lessons |
| --- | --- | --- |
| Delegation | Should AI do this step at all? | L04, L06 |
| Description | Did I brief it clearly? | L01, L05 |
| Discernment | Is the output good, and would I sign it? | L02 |
| Diligence | Who owns it? Was AI disclosed? Is there sensitive data? | L06 |

## 5. Five facts that are true on every question

Our summary of the course:

1. The same prompt can give different answers.
2. A confident tone doesn't mean it's right.
3. Context is a budget, and long chats drift.
4. Knowledge has a cutoff date, so current facts need search, Research or a file.
5. Skills reduce variation but don't remove the need to review.

## 6. Worked example

A marketing lead asks Claude to "write this quarter's competitor summary for the leadership team".
Run the four decisions and the check:

- **Entry point:** Research, because it needs current facts from many sources.
- **Capability:** web search is on (Research uses it).
- **Model:** Sonnet is enough for a summary. Save Opus for hard reasoning.
- **Context:** start a fresh chat; this has nothing to do with last week's work.
- **Check:** open the key citations, and have the lead read it before it goes to leadership.

An answer that only says "write a more detailed prompt" misses four of these five. That's why it's
usually wrong.

## 7. Traps

- "A longer prompt fixes it." Often the real gap is the wrong entry point, a missing file or no check.
- "The bigger model is always safer." Opus costs more and is slower; a clear, simple task doesn't need it.
- "It sounds confident, so it's right." Confidence isn't evidence (L02).
- "Skip the policy question; it's just a productivity tool." Governance is 15% of the exam (L06).

## 8. Try it (30 min)

1. [ ] Download the CCAO-F exam guide from the Partner Academy (sign in first). A copy is in the
       [exam guide PDF](https://anthropic-partners.skilljar.com/page/partner-certifications).
       Read the blueprint table (section 6). There's also a summary in the
       guide notes.
2. [ ] In the same PDF, read the three official sample questions *and their explanations*
       (section 8). Notice why each wrong answer is wrong.
3. [ ] Do the self-check below.
4. [ ] **Cold baseline:** take Amey Thakur's CCAO-F
       [mock 1](https://github.com/Amey-Thakur/CLAUDE-CERTIFICATIONS/blob/main/associate-foundations/mock-exam-1.md)
       (Tier 2) first, timed, without studying. Its questions are fresh to you now; later most
       of them turn up in the practice tool too. Practice-tool mocks come after this.
       To open the [practice tool](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html): (1) open `index.html`,
       (2) if you're on the website, choose **Download raw file**, (3) open the downloaded file in
       your browser and pick CCAO-F. Write the score and your two weakest domains in
       your own notes.
5. [ ] Plan your lessons: skip any domain where you scored over 85%, **except L02**. Always do
       L02, because it's the biggest domain.

## 9. Self-check (answer out loud)

- Why is "write a more detailed prompt" usually *not* the best answer?
- Name the five facts from memory.
- Which domain is the biggest? *(Output Evaluation, 21%)*

## Done when

- [ ] You took the cold baseline mock and logged the score
- [ ] You wrote down your two weakest domains
- [ ] You chose your lesson order (L02 always in it)

**Next:** [L01 Prompting](L01-prompting-and-task-execution.md), or start with your weakest domain.

Sources: CCAO-F exam guide v1.0, section 5 "Exam Details at a Glance" (Item format row), section 6 blueprint and
section 8 samples (Tier 1); course Module 1 for the four decisions (Tier 1, copy); course Module 8 for the
4D frame, which names the "AI Fluency Framework: Description, Discernment, Diligence, Delegation"
(Tier 1, copy); the "five facts" are our summary of the course; Amey Thakur's mocks (Tier 2,
MIT licence); a colleague's debrief (F: changes emphasis, not facts).