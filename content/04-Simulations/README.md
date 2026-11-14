# 04 — Simulations

Simulations are the **exam rehearsal**. They come after the lessons and practice sessions. There
are two kinds:

| Kind | What it is | Where |
| --- | --- | --- |
| **Full mock** | 60 questions, 120 minutes, weighted like the real exam, no help | Practice tool, Amey's held-back mocks, official and online mocks |
| **Scenario simulation** | Claude plays out one realistic work situation in stages. At each stage you choose the next move. It's scored against an answer key written from the official guide. | The files below |

| Folder | Exam | Simulations |
| --- | --- | --- |
| [01-CCAO-F-Associate](01-CCAO-F-Associate/README.md) | Associate | 1 full mock, 5 scenarios |
| [02-CCAR-F-Architect-Foundations](02-CCAR-F-Architect-Foundations/README.md) | Architect: Foundations | 1 full mock, all 6 official scenarios |
| [03-CCDV-F-Developer](03-CCDV-F-Developer/README.md) | Developer | 1 full mock, 6 scenarios |
| [04-CCAR-P-Architect-Professional](04-CCAR-P-Architect-Professional/README.md) | Architect: Professional | 1 full mock, 4 scenarios |

## Exam-day conditions (for every full mock)

- One sitting. Set a 120-minute timer. No notes, no lessons, no Claude.
- Answer every question, because there's no penalty for guessing. Flag the hard ones and come back.
- Read how many answers each question asks for.
- Score it, then **review every question you got wrong and every one you guessed**. The review is
  where the learning happens.

## How Claude runs a scenario simulation

When you say *"Run simulation CCAR-F SIM-03"*, Claude follows these rules:

1. It reads the simulation file, **including the coach key, which you shouldn't open**.
2. It sets the scene in 3–5 sentences, as an exam scenario would.
3. It asks **one decision at a time**, as a multiple-choice question with 4 options (sometimes
   "choose 2"). Every distractor is a plausible wrong move from the key's list of traps.
4. It gives **no hints, and no feedback until the end**. Time budget: about 2 minutes per decision.
5. At the end:
   - a score by decision
   - for each wrong answer, the correct move, why it's right, and the official task statement or
     lesson section it comes from
   - the two weakest concepts, with the lesson to reread
6. It adds a row to the exam's progress log.
7. **Replays:** asking for the same simulation again changes the wording and the order of the
   options, but tests the same decisions.

**Decisions per scenario:** CCAR-F, CCDV-F and CCAR-P scenarios have 10 decisions each (pass 8 of
10), except CCAR-F SIM-07, which has 11 (pass 9 of 11). CCAO-F SIM-02 to SIM-05 have 8 decisions
(pass 7 of 8), and CCAO-F SIM-06 has 10 (pass 8 of 10).

**Pass bar:** 80% or more on each simulation. For each exam, the bar before booking is in the
[curriculum](../01-Curriculum/00-Overview.md): two mocks at 850 or more and no domain below 70%.
Anthropic's official practice exam for CCAR-F "was retired in the move to Pearson" (official
wording; Pearson is the company that now runs the exam), per the
[Partner Academy certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications)
(Tier 1). The official practice items now are the exam guide's 12 sample questions in section 9
(run E in [CCAR-F SIM-01](02-CCAR-F-Architect-Foundations/SIM-01-full-mock.md)) and the quizzes in
the [Anthropic Academy prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
(Tier 1).