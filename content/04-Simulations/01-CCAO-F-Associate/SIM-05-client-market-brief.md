# CCAO-F SIM-05 — Client market brief

**Domains:** 6 Governance (3), 2 Output Evaluation (3), 3 Product and Model Selection (1), 5 Configuration (1) ·
**Decisions:** 8 · **Pass:** 7 of 8 · **Time:** 16 min

Last reviewed: 2026-09-29

## Scene (read it yourself, or have Claude read it)

You're a consultant. A client, a mid-size insurer, wants a brief on how competitors use AI in
claims handling, with current numbers, before their board meeting in five days. The partner wants
two versions from the same analysis: a 1-page version for the board and a detailed version for the
client's claims team. You have:

- the client's internal claims-volume spreadsheet, which contains policyholder names
- last quarter's brief for a different client in the same industry
- a team Claude account with Research, which you've already used to gather competitor material

Your firm's policy says no client data goes into any AI tool without the client's written consent.
The brief will be sent to the client under your firm's name.


---

## The decisions (answer these before you open the key)

1. **Model for volume:** Research has turned up 1,200 short public news items and press releases on competitors' AI claims tools. You want each one tagged into 5 fixed categories so you can count them.
2. **Setup:** Where the work lives
3. **Client data:** You want to use the claims spreadsheet
4. **Old brief:** Reusing last quarter's brief for the other client
5. **Two versions:** The board version and the claims-team version, from the same analysis
6. **A number:** The draft says "competitor X cut claims time by 60%". The citation is real and says that, but it's from 2023, and the client asked for current numbers.
7. **Disclosure:** Should the brief say AI helped?
8. **Release:** Sending to the client

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Stage | Decision | Correct move | Why | Traps to use as distractors | Domain · objective | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Model for volume | Research has turned up 1,200 short public news items and press releases on competitors' AI claims tools. You want each one tagged into 5 fixed categories so you can count them. | **A faster, lower-cost model (Haiku, or Sonnet)** with the rubric in the prompt, then spot-check a sample of the tags | Many short items and a fixed rubric suit a faster, cheaper model. | Opus, because the brief is for an insurer's board · run Research again on each item · Opus for the first half, then compare | 3 · Differentiate between Claude model types (Haiku, Sonnet, Opus) | [Lesson 3, section 5](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md) (questions 1 and 2) |
| 2 | Setup | Where the work lives | **A new Project for this client only**, on the team account | One client per Project keeps files and context apart. | Reuse the other client's Project · a personal Pro account · an Incognito chat as the "safe" option | 5 · Configure Claude Projects with instructions and knowledge sources | [Lesson 5, section 8](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 6, section 3](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 3 | Client data | You want to use the claims spreadsheet | **Check the firm's policy first: get the client's written consent, or leave their data out.** With consent, share only the columns the brief needs, without policyholder names. | Ask "is this allowed here?" before "how do I handle it here?" | The Project is private, so upload it all · remove the names and upload, since anonymized data doesn't need consent · upload it in an Incognito chat so it isn't kept | 6 · Follow organizational AI policies and governance standards | [Lesson 6, section 4](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md), [Lesson 6, section 3.1](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 4 | Old brief | Reusing last quarter's brief for the other client | **Use its structure only, as a template stripped of that client's content** | Another client's content is confidential; reuse only the empty structure. | Upload it as-is for style · ask Claude to "ignore the other client's details" · upload it with only the client's name blacked out | 6 · Apply data sensitivity, regulatory, and privacy considerations | [Lesson 5, section 8](../../02-Lessons/01-CCAO-F-Associate/L05-configuration-and-knowledge-management.md), [Lesson 6, section 3](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 5 | Two versions | The board version and the claims-team version, from the same analysis | **Keep the facts fixed, then adapt:** the board version leads with the decision and impact; the team version keeps the method, owners and next steps | Same facts, different selection, depth and tone for each reader. | Send the detailed version to both; the board can skim · write the board version from scratch in a new chat · cut every other paragraph of the detailed version | 2 · Edit, adapt, refine, and compare outputs for the intended audience | [Lesson 2, section 3.1](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 6 | A number | The draft says "competitor X cut claims time by 60%". The citation is real and says that, but it's from 2023, and the client asked for current numbers. | **Check the date: refresh the number with Research, or keep it and label its date clearly** | A real source can still be stale; checking the date is part of fact-checking. | The citation is real, so use it · switch to a bigger model · remove every number from the brief | 2 · Apply fact-checking and validation techniques | [Lesson 2, section 5](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |
| 7 | Disclosure | Should the brief say AI helped? | **Follow the firm's disclosure rule. If there isn't one, say briefly that AI helped with research and drafting and that your team checked it.** | Good practice; the Usage Policy also bars AI-assisted work without proper attribution. | No, it's the firm's work once you've reviewed it · only if the client asks · add a line that the firm isn't responsible for AI-generated content | 6 · Understand the ethical implications of AI usage | [Lesson 6, section 5](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) |
| 8 | Release | Sending to the client | **You review it, every number and citation included, before it goes out under your name**, then send | It carries your firm's name, so you own every claim. | Send it now, since Research cited everything · let the client check it · ask Claude for a final review and send if it finds nothing | 2 · Determine when human review or additional verification is required | [Lesson 2, section 6](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) |

**Scoring:** 7 or more is a pass. If you miss 1, go back over the three questions that pick the
model in [Lesson 3, section 5](../../02-Lessons/01-CCAO-F-Associate/L03-product-and-model-selection.md). If you miss 3 or 4, go back over [Lesson 6, section 3](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md) and [Lesson 6, section 4](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md). If you miss 5 or 6, go back over
[Lesson 2, section 3.1](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md) and [Lesson 2, section 5](../../02-Lessons/01-CCAO-F-Associate/L02-output-evaluation-and-validation.md). If you miss 7, go back over [Lesson 6, section 5](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md).

**Decision 7, in more detail:** the Usage Policy's High-Risk disclosure rule doesn't strictly apply
here. This is a business brief for a client, not high-risk advice shown to individuals. The rule
that does apply is general. Usage Policy wording: "Plagiarize or submit AI-assisted work without
proper permission or attribution" is on its list of things not to do (Usage Policy, saved
2026-09-29, Tier 1; public copy: https://www.anthropic.com/legal/aup). Disclosing is also good
practice ([Lesson 6, section 5](../../02-Lessons/01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md)).

</details>