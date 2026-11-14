# Lab 01 — A Claude Project that does one job well (CCAO-F)

Last reviewed: 2026-09-29

**Supports:** CCAO-F L01, L02, L05, L06 · **Time:** 60–90 minutes · **Needs:** a Claude account
with Projects (claude.ai). No code.

**Coming from a lesson?** L05's "Try it" is steps 1–4 (build the Project). L02's "Try it" is
steps 5–7 (grade 5 outputs). Doing the whole lab in one sitting is fine too.

**Done when:** a Project with written instructions and two knowledge files has produced 5 outputs,
you've graded each one pass, revise or fail against a checklist you wrote first (including a bias
check), at least one Revise or Fail has been fixed by changing one thing, and you've written down
what changed.

## Steps

1. **Pick one repeat task** you do at work, with no customer data in it. For example: "turn my
   meeting notes into a status update for my manager".
2. **Create a Project.** Write the instructions in four short parts:
   - who Claude is helping, and who reads the result
   - the task, in one sentence
   - the output format: headings, length, tone
   - what to do when information is missing (ask, or mark it `[missing]`, but never invent it)
3. **Add knowledge.** Upload two files: one good past example, and a one-page style guide. Name
   them with a version, such as `style-guide-v1.md`. When you change one, upload `v2` and delete
   `v1`, so old guidance doesn't linger.
4. **Write the review checklist before you run anything.** Keep it to 5 or 6 lines, for example:
   facts match the notes · no invented dates or names · under 200 words · the ask is in the first
   line · the tone suits the reader · **fair and balanced: no group's view is missing or
   stereotyped, and it doesn't sound certain where things are contested**.
5. **Run it on 5 inputs:** two normal ones, one with missing information, one that's messy, and one
   that mentions several teams or people (to test the bias line).
6. **Grade all 5 outputs.** For each, note whether it's complete, accurate and fit for the reader,
   then mark it Pass, Revise or Fail against your checklist. For every Revise or Fail, change *one
   thing*: the instructions, an example or the knowledge. Then rerun that input.
7. **Write the lesson learned** in 3 lines in your own notes: what you changed, and what it fixed.

## What this teaches

- Clear instructions, context and examples beat "be careful" (L01).
- You judge output against criteria you wrote first, not against a gut feel, and that includes
  bias (L02).
- Knowledge needs versions and cleanup (L05).
- Nothing sensitive goes in (L06).

**Next:** [SIM-02 Marketing launch brief](../../04-Simulations/01-CCAO-F-Associate/SIM-02-marketing-launch.md),
in session 6 of the [CCAO-F week plan](../../01-Curriculum/01-Associate-Track/CCAO-F.md#week-plan-about-18-hours-about-2-weeks).

**Sources:** CCAO-F exam guide v1.0, domains 1, 2, 5 and 6, and section 7, which says to "configure a
Project with instructions and knowledge sources, and evaluate outputs for accuracy and bias"
(official wording; Tier 1) · [Anthropic's prompting best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices) (Tier 1).