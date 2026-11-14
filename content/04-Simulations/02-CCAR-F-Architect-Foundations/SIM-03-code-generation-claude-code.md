# CCAR-F SIM-03 — Scenario 2: Code Generation with Claude Code

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

### Stage 1 — A small request crosses several hidden boundaries

A request says “rename customer status.” The developer discovers the field in storage, API responses, validation and tests. Editing the first match alone breaks a downstream caller.

**Original exam-style practice — choose ONE.** Which workflow is most appropriate before implementing an unfamiliar cross-cutting repository change?

A. Inspect affected paths and dependencies, create a bounded plan, then implement and validate in increments.

B. Run a global text replacement immediately.

C. Require a full architecture plan for every spelling correction too.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice A.** The risk comes from connected behavior, so discover and sequence the changes first. B confuses identical text with identical meaning; C ignores task size. A tiny well-understood edit can use direct execution.

**Follow the changed path:**

```text
request → targeted repository exploration → impact plan → small edit → focused verification
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** List producer, consumer and tests before editing. A passing unit test alone is insufficient if the changed API contract breaks the consumer.

</details>

**Changed-constraint decision — choose ONE before revealing:** The implementation fails a regression test. A: say “try harder”; B: give the failing input, expected behavior and observed output, then repair and rerun the relevant check.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Specific feedback reduces ambiguity and keeps refinement tied to evidence rather than repeated broad rewrites.

</details>

**Objective connections:** [3.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.4.md), [3.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.5.md).

### Stage 2 — A useful rule spreads into the wrong files

A code assistant follows a team’s Python test convention. Later the same rule is applied while editing a Markdown guide. The convention is useful, but its reach is wrong.

**Original exam-style practice — choose ONE.** Which Claude Code instruction design best supports shared conventions without loading irrelevant path-specific rules everywhere?

A. Place all conventions in a global user instruction file.

B. Use project guidance for shared behavior and appropriately scoped path rules for file-specific conventions.

C. Repeat conflicting conventions in every prompt.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** Put common instructions where the team can find them; narrow rules should apply to the files they describe. A exports one project’s habits everywhere; C makes behavior depend on accidental prompt repetition. Read the effective instructions before assuming which rule won.

**Follow the changed path:**

```text
working directory + instruction hierarchy → applicable project guidance
matching file path → relevant scoped rule → reviewable change
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Compare a Python change with a documentation-only change. Record which rule applies and check that unrelated conventions do not shape the latter.

</details>

**Changed-constraint decision — choose ONE before revealing:** The repeated task is a user-invoked review workflow. A: express it as a reusable command/skill with clear inputs; B: treat a path-specific convention as an execution trigger.

<details><summary>Reveal changed-constraint reasoning</summary>

A. A workflow tells the assistant how to perform a task; a scoped rule supplies conventions when relevant files are involved.

</details>

**Objective connections:** [3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.1.md), [3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.2.md), [3.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.3.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** A development team asks an assistant to change code, investigate defects and maintain documentation within its existing repository. Inputs are the requested change, project files and team conventions; the expected output is reviewable work that fits the project. This simulation explores the workflow choices behind those tasks.

**Build the application picture first:** [AS 05 code change](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-05-code-change.md)

**Primary domains:** 3 Claude Code, 5 Context and Reliability · **Decisions:** 10 · **Time:** 20 min for the decisions, plus about 10 for the twists and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 2, Tier 1)

You're using Claude Code to speed up software development. Your team uses it for code generation,
refactoring, debugging and documentation. You need to fit it into the team's workflow with custom
slash commands and CLAUDE.md configuration, and know **when to use plan mode vs direct
execution**.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. A new hire isn't getting the team's coding standards. Where are they probably kept, and where
   should they be?
2. The project CLAUDE.md is 900 lines and covers everything. What do you do with it?
3. SQL migration files live in 12 places (`db/migrations/`, `services/*/migrations/`,
   `legacy/sql/`). The team's migration rules (every change reversible, no `DROP` without a backup
   step) keep getting ignored. A teammate proposes a CLAUDE.md in each of the 12 folders. What do
   you do instead?
4. Last week Claude, running straight into edits, changed the auth middleware across 19 files.
   Half of it was reverted because it chose cookie sessions, and the mobile app needs tokens. A
   similar change to the payments middleware is next. How do you run it?
5. A codebase-analysis skill floods the main chat with output. How do you contain it?
6. A skill should be able to write files but never run Bash. Answering the way the exam guide
   describes it, how do you set that up?
7. You're asked to add rate limiting to a payment-webhook service, a domain nobody on the team has
   built before. Claude's first draft ignored the provider's automatic retries and clock drift.
   What do you do before the next attempt?
8. A one-line fix with a clear stack trace. Which mode?
9. Your prose description of a data transformation keeps being read differently. What do you
   give Claude instead?
10. After a long exploration, answers start mentioning "typical patterns" instead of the classes
    you found earlier. What do you do?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | A new hire isn't getting the team's coding standards | They're in `~/.claude/CLAUDE.md`. **Move them to the project CLAUDE.md** and commit it. | Tell the new hire to copy the file; paste the standards into every prompt; put them in the new hire's `CLAUDE.local.md` | D3 3.1 CLAUDE.md hierarchy | [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 2 | CLAUDE.md is 900 lines and covers everything | **Split it into `.claude/rules/` topic files**, with `@import` where a package needs them | Trim it to 100 lines and lose rules; one file per developer; move to a model with a bigger context window | D3 3.1 CLAUDE.md hierarchy | [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 3 | Migration rules for SQL files in 12 folders keep getting ignored | **One path-scoped rule file**, for example `.claude/rules/migrations.md` with `paths: ["**/migrations/**/*.sql", "legacy/sql/**/*.sql"]`. It loads only when Claude touches a matching file, wherever it lives. | Put the rules in a `/migration-rules` skill that developers run when they remember, so they're skipped whenever nobody does; a longer, all-caps section in the root CLAUDE.md, loaded every session; a CLAUDE.md in each of the 12 folders, which drift apart | D3 3.3 Path-specific rules | [Lesson 3, section 3.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 4 | A 19-file auth change was half reverted because Claude chose the wrong session design; a similar payments change is next | **Plan mode first:** explore the callers, compare the design options, and agree the approach, **then direct execution** of the agreed plan | Direct execution again, with "be careful" in the prompt; a bigger model; direct execution file by file, reverting whatever breaks | D3 3.4 Plan mode vs direct execution | [Lesson 3, section 3.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 5 | A codebase-analysis skill floods the main chat | **`context: fork`** in SKILL.md | Tell it to "be brief"; turn off the skill; run `/clear` after every use and lose the thread | D3 3.2 Slash commands and skills | [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 6 | A skill should be able to write files but never run Bash | **`allowed-tools`** in the frontmatter (exam guide wording). Also accept `disallowed-tools: Bash` as right for today's Claude Code, where `allowed-tools` only pre-approves tools; on the exam, pick `allowed-tools`. See [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | A line in SKILL.md saying "don't use Bash"; ask it to be careful with the shell; let it run and monitor the logs for Bash calls afterwards | D3 3.2 Slash commands and skills | [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 7 | Rate limiting in an unfamiliar domain; the first draft missed provider retries and clock drift | **The interview pattern:** ask Claude to question you first (failure modes, how the provider retries, limits per merchant, what happens on clock drift), then implement from the answers | A longer first prompt listing everything you can think of; let Claude implement straight away and catch the missed cases in code review; "think about edge cases carefully" added to the same request | D3 3.5 Iterative refinement | [Lesson 3, section 3.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 8 | A one-line fix with a clear stack trace | **Direct execution** | Plan mode with an Explore subagent; write a design doc first; hand it to a bigger model "to be safe" | D3 3.4 Plan mode vs direct execution | [Lesson 3, section 3.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 9 | Prose descriptions of a transformation keep being read differently | **2–3 concrete input/output examples**, or tests first, then share the failures | Rewrite the prose more strongly; move the same prose into CLAUDE.md so it's loaded every session; ask it to "follow the description exactly" | D3 3.5 Iterative refinement | [Lesson 3, section 3.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 10 | After a long exploration, answers start mentioning "typical patterns" | **A scratchpad file of findings**, `/compact`, or an Explore subagent for discovery | Keep going; restart with no summary; switch to a bigger context window and carry on | D5 5.4 Large-codebase exploration | [Lesson 5, section 5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |

**Scoring:** 8 or more is a pass. Decisions 3, 4 and 7 are where people usually go wrong: *match
the rule to the files, plan before a change with design choices, and let Claude ask before it
builds in unfamiliar territory*.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 2 and task statements 3.1–3.5, 5.4 (Tier 1); Claude Code docs on skills and memory at
code.claude.com (Tier 1; check the current `allowed-tools` wording). Taught in lessons
[L03](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md)
and [L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: one developer wants their own version of a team skill

**What changed:** the team shares a `release-notes` skill in the repo. One developer wants it to
write in a different style, just for themselves.

**Question:** where do they make that change?

<details><summary><b>Answer and why</b></summary>

**Make a personal copy with a different name** (for example `my-release-notes`) in
`~/.claude/skills/`. Their version lives in their own home folder, and the team's skill stays the
same for everyone else. Exam guide wording: "creating personal variants in ~/.claude/skills/ with
different names to avoid affecting teammates".

**Why the others lose:** editing the shared skill in the repo changes it for the whole team. A
personal copy with the *same* name is a quiet trap: a personal skill wins over a project skill with
the same name, so that developer's copy runs and silently hides the team skill, including every
later update the team makes to it. Asking Claude each time to "write it differently" gives a
different result every run.

**Tests:** Domain 3, task statement 3.2 (slash commands and skills).

**Lesson:** [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#32-slash-commands-and-skills) · [Deep practice, Domain 3](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/03-claude-code-configuration-and-workflows.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 3.2 (Tier 1); Claude Code [skills docs](https://code.claude.com/docs/en/skills) (Tier 1).

</details>

### Twist 2: people keep running a skill without the input it needs

**What changed:** the release-notes skill needs a version number. Developers often run it without
one, and the notes come out with the wrong version.

**Question:** how do you get people to supply the version?

<details><summary><b>Answer and why</b></summary>

**Add `argument-hint: [version]` to the skill's `SKILL.md` frontmatter.** The hint shows the
developer what to type when they run the skill. It's a hint, not a rule: it doesn't stop a run
with no version, and it works in Claude Code only.

Exam guide wording: "Using argument-hint frontmatter to prompt developers for required
parameters". Today it is an autocomplete hint; on the exam, pick `argument-hint`.

**Why the others lose:** a line in the skill's instructions saying "ask for the version" depends
on the model remembering to ask. A note in the README depends on people reading it. Hard-coding a
version means editing the skill every release.

**Tests:** Domain 3, task statement 3.2 (slash commands and skills).

**Lesson:** [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#32-slash-commands-and-skills) · [Deep practice, Domain 3](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/03-claude-code-configuration-and-workflows.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 3.2 (Tier 1); Claude Code [skills docs](https://code.claude.com/docs/en/skills) (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: a new hire isn't getting the team's coding standards**

- **What's going on:** the rules live on one person's laptop, not in the repo.
- **Under the hood:** Claude Code loads CLAUDE.md files (instruction files it reads at the start of a session) at several levels. `~/.claude/CLAUDE.md` (user level) applies only to you and isn't in version control. The project CLAUDE.md is committed, so every teammate gets it.
- **How to make the call:** if a rule should reach the whole team, put it in the project CLAUDE.md and commit it; if it's only your own taste, keep it at user level. Exam wording (task statement 3.1): "Diagnosing configuration hierarchy issues (e.g., a new team member not receiving instructions because they're in user-level rather than project-level configuration)".
- **Why the tempting answers are wrong:**
  - **New hire copies the file:** the copies drift apart.
  - **Paste into every prompt:** manual and easy to forget.
  - **New hire's `CLAUDE.local.md`:** personal and not shared, the same problem again.
- **Go deeper:** [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#31-the-claudemd-hierarchy)

**Decision 2: a 900-line CLAUDE.md that covers everything**

- **What's going on:** one giant rulebook where nothing is easy to find or update.
- **Under the hood:** `.claude/rules/` holds topic files, such as testing or API conventions. `@import` (a line like `@path/to/file`) pulls a chosen file into a CLAUDE.md, so each package can include only the standards it needs.
- **How to make the call:** if CLAUDE.md mixes many topics, split it into topic files in `.claude/rules/`, and use `@import` where a package needs specific standards. If it's short and focused, leave it. Exam wording (task statement 3.1): "Splitting large CLAUDE.md files into focused topic-specific files in .claude/rules/ (e.g., testing.md, api-conventions.md, deployment.md)".
- **Why the tempting answers are wrong:**
  - **Trim to 100 lines:** loses rules.
  - **One file per developer:** team rules split apart and drift.
  - **Bigger context window:** still one tangled file to follow and maintain.
- **Go deeper:** [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#31-the-claudemd-hierarchy)

**Decision 3: migration rules for SQL files in 12 folders**

- **What's going on:** one rule applies to files scattered across the repo.
- **Under the hood:** a file in `.claude/rules/` can start with YAML frontmatter (settings at the top of the file) holding a `paths` field of glob patterns (wildcards like `**/*.sql`). The rule loads only when Claude works on a matching file.
- **How to make the call:** if a convention follows a file type across many folders, write one path-scoped rule with glob patterns; if it belongs to one folder only, a CLAUDE.md there can work. Exam wording (task statement 3.3): "Choosing path-specific rules over subdirectory CLAUDE.md files when conventions must apply to files spread across the codebase".
- **Why the tempting answers are wrong:**
  - **A `/migration-rules` skill:** runs only when someone remembers.
  - **All-caps root section:** loaded every session, still ignored.
  - **12 folder CLAUDE.md files:** twelve copies that drift apart.
- **Go deeper:** [Lesson 3, section 3.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#33-path-specific-rules)

**Decision 4: a 19-file change half reverted; a similar one is next**

- **What's going on:** a big change with a design choice got built before anyone chose.
- **Under the hood:** plan mode lets Claude read and explore the code and propose a plan without editing files. You agree the approach, then switch to normal execution to carry it out.
- **How to make the call:** if a change spans many files or has more than one valid design, plan first, agree the approach, then execute it directly. If it's small and the fix is clear, go straight to execution. Exam wording (task statement 3.4): "Combining plan mode for investigation with direct execution for implementation (e.g., planning a library migration, then executing the planned approach)".
- **Why the tempting answers are wrong:**
  - **Direct again, "be careful":** the design choice still gets made blind.
  - **Bigger model:** skips the same exploration step.
  - **File by file, revert breaks:** rework instead of a plan.
- **Go deeper:** [Lesson 3, section 3.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#34-plan-mode-or-direct-execution)

**Decision 5: a codebase-analysis skill floods the main chat**

- **What's going on:** a noisy skill is filling up the main conversation.
- **Under the hood:** `context: fork` in a skill's SKILL.md frontmatter runs the skill in a separate subagent (a helper with its own context). Its working output stays there; only the result comes back to the main chat.
- **How to make the call:** if a skill makes lots of output you don't need to keep (analysis, brainstorming), add `context: fork`; if its output is short and is the point, leave it in the main chat. Exam wording (task statement 3.2): "Using context: fork to isolate skills that produce verbose output (e.g., codebase analysis) or exploratory context (e.g., brainstorming alternatives) from the main session".
- **Why the tempting answers are wrong:**
  - **"Be brief":** a thinner analysis, and the noise problem stays.
  - **Turn off the skill:** loses the tool.
  - **`/clear` after each use:** wipes the thread too.
- **Go deeper:** [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#32-slash-commands-and-skills)

**Decision 6: a skill may write files but never run Bash**

- **What's going on:** the skill may write files but must stay away from the shell.
- **Under the hood:** a skill's frontmatter can set its tools. Today's docs say `allowed-tools` only pre-approves the listed tools for that turn (they run without asking) and "does not restrict which tools are available". Blocking a tool is `disallowed-tools` (here `disallowed-tools: Bash`); see [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today).
- **How to make the call:** if a skill must be kept from a tool, set that in its frontmatter, not in its instructions. On the exam, pick `allowed-tools`. Exam wording (task statement 3.2): "Configuring allowed-tools in skill frontmatter to restrict tool access during skill execution (e.g., limiting to file write operations to prevent destructive actions)".
- **Why the tempting answers are wrong:**
  - **"Don't use Bash" line:** text the model can miss.
  - **Be careful with the shell:** a request, not a limit.
  - **Monitor logs afterwards:** finds the damage after it happened.
- **Go deeper:** [Lesson 3, section 3.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#32-slash-commands-and-skills)

**Decision 7: rate limiting in a domain nobody has built before**

- **What's going on:** new territory, and you don't know what you don't know.
- **Under the hood:** asking Claude to question you first brings up likely issues before any code exists. You answer with your system's facts (how the provider retries, limits per merchant, clock drift), and it builds from those.
- **How to make the call:** if the domain is new to you and a first draft missed things, have Claude interview you before it builds, then implement from your answers. If you know the domain well, give clear requirements and go. Exam wording (task statement 3.5): "Using the interview pattern to surface design considerations (e.g., cache invalidation strategies, failure modes) before implementing solutions in unfamiliar domains".
- **Why the tempting answers are wrong:**
  - **Longer first prompt:** you can only list what you already know.
  - **Catch it in review:** pays for rework later.
  - **"Think about edge cases":** same request, no new facts.
- **Go deeper:** [Lesson 3, section 3.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#35-refining-step-by-step)

**Decision 8: a one-line fix with a clear stack trace**

- **What's going on:** the bug, the file and the fix are all clear.
- **Under the hood:** planning pays when there's something to decide. With one file, one cause and a stack trace pointing at it, there's no design choice left, so planning only adds steps.
- **How to make the call:** if the change is small, in one place, and the cause is known, use direct execution; if it spans files or has design choices, plan first. Exam wording (task statement 3.4): "Selecting direct execution for well-understood changes with clear scope (e.g., a single-file bug fix with a clear stack trace, adding a date validation conditional)".
- **Why the tempting answers are wrong:**
  - **Plan mode plus Explore:** heavy setup for a known fix.
  - **Design doc first:** paperwork for one line.
  - **Bigger model:** there's nothing hard left to solve.
- **Go deeper:** [Lesson 3, section 3.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#34-plan-mode-or-direct-execution)

**Decision 9: a prose description keeps being read differently**

- **What's going on:** the words leave room for more than one reading.
- **Under the hood:** a prose description can fit many transformations. A real input with its exact expected output fits far fewer. Tests make the target checkable: a failing test shows exactly where the result went wrong.
- **How to make the call:** if prose keeps being read differently, give 2–3 input/output examples, or write tests first and share the failures. If it's being read correctly, prose is fine. Exam wording (task statement 3.5): "Providing 2-3 concrete input/output examples to clarify transformation requirements when natural language descriptions produce inconsistent results".
- **Why the tempting answers are wrong:**
  - **Stronger prose:** still words, still open to readings.
  - **Same prose in CLAUDE.md:** loaded every session, misread the same way.
  - **"Follow it exactly":** it follows its own reading exactly.
- **Go deeper:** [Lesson 3, section 3.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#35-refining-step-by-step)

**Decision 10: answers drift to "typical patterns" after a long exploration**

- **What's going on:** a long session is getting fuzzy about what it actually found.
- **Under the hood:** long sessions fill the context with search output, and answers lose hold of earlier specifics. A scratchpad file keeps findings outside the chat. `/compact` condenses the history. An Explore subagent searches in its own context and returns a summary.
- **How to make the call:** if answers turn generic instead of naming the classes you found, save findings to a scratchpad file, then `/compact` or hand further discovery to an Explore subagent; if answers still name the classes you found, keep going. Exam wording (task statement 5.4): "Context degradation in extended sessions: models start giving inconsistent answers and referencing "typical patterns" rather than specific classes discovered earlier".
- **Why the tempting answers are wrong:**
  - **Keep going:** it only gets fuzzier.
  - **Restart, no summary:** throws away the findings.
  - **Bigger context window:** more room for the same noise.
- **Go deeper:** [Lesson 5, section 5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#54-exploring-a-large-codebase)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-04](SIM-04-multi-agent-research.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-12 — decision checkpoint

The requested artifact is a brand-new standalone CSV with an explicit schema; no existing file needs modification. Which operation fits after inspecting the target location?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Write the new artifact at the agreed path and validate its schema. Creating a new artifact is different from patching an existing region.

**Base choice:** An unfamiliar education repository needs a one-function fix. Glob relevant paths, Grep the symbol, Read callers and tests, then Edit the precise existing region.

**Changed constraint and recovery:** A genuinely new standalone artifact has no existing file to patch. Write the new file after verifying its placement and contract.

**Failure:** A broad replacement changes unrelated handlers. Restore the unintended changes and inspect the focused diff and targeted behavior.

**Nearest alternative:** Dumping or rewriting the repository risks losing context and unrelated code. Tool selection follows the task, not a fixed ritual for every edit.

**Conditional cue:** Locate, inspect, change, prove; create only when new.

**Proof:** Inspect `evidence=[paths,symbol_hits,caller_read,test_read]; change={file:handler.py,region:retry_condition}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.5.md#variant-fv-12).

</details>

### SIM-FV-15 — decision checkpoint

The same repository has a policy requiring evidence attribution in every generated artifact, regardless of path. What rule scope fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Use an applicable broader instruction for the cross-cutting attribution policy. A genuinely cross-cutting requirement needs correspondingly broad applicability.

**Base choice:** Backend and test conventions are scoped to their respective path patterns. Predict applicable rules for a change touching both areas and verify actual loading.

**Changed constraint and recovery:** A security policy genuinely applies across the repository. Move that requirement to an appropriate broader scope.

**Failure:** A test file moved outside the expected glob, so its rule was not loaded. Correct the scope and check a matching and nonmatching path.

**Nearest alternative:** Duplicating every rule into the main prompt can hide mismatches and flood context; path scope must match actual files.

**Conditional cue:** Match the path; verify the rule; broaden only when shared.

**Proof:** Inspect `paths=[services/api.py,tests/test_api.py]; rules={backend:services/**,testing:tests/**}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.3.md#variant-fv-15).

</details>

### SIM-FV-16 — decision checkpoint

A reviewed typo fix touches one documented label, has an exact replacement and no behavior change. Which starting mode fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Perform the clear bounded edit directly and verify the rendered label. A small unambiguous low-impact change can be executed and checked directly.

**Base choice:** A cross-service authentication change has unclear callers and migration impact. Inspect evidence, produce a plan and review dependencies before editing.

**Changed constraint and recovery:** The task becomes a precise typo in an isolated documented comment. Direct execution and a focused check are proportionate.

**Failure:** An apparently small edit reveals a shared API dependency. Pause to revise the plan rather than continuing under the old assumption.

**Nearest alternative:** Always planning adds overhead to bounded simple work; always executing can miss uncertain dependencies.

**Conditional cue:** Plan the unknown boundaries; execute the bounded known edit.

**Proof:** Inspect `plan={affected:[client,server,tests],unknown:[migration],acceptance:[old_client_works]}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.4.md#variant-fv-16).

</details>

### SIM-FV-17 — decision checkpoint

The same precise failing fixture still fails after two different implementations. The team is repeating its initial diagnosis without inspecting new evidence. What should change?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Revisit the failure hypothesis and inspect the implementation or dependency evidence before another change. Repeated failure can signal a wrong hypothesis rather than insufficient repetition.

**Base choice:** A date parser fails on one fixture. Supply actual input, expected result, failing assertion and relevant code; make a targeted change and re-run the fixture plus nearby cases.

**Changed constraint and recovery:** Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign.

**Failure:** The same failure survives two identical retries. Investigate a new cause, such as locale interpretation or preprocessing, instead of repeating the same prompt.

**Nearest alternative:** More iterations do not imply learning. Narrow evidence and hypothesis changes matter more than request length.

**Conditional cue:** Example, expectation, evidence; failed hypothesis must change.

**Proof:** Inspect `feedback={input:03/04,locale:en_GB,expected:2026-04-03,actual:2026-03-04,check:date_locale}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.5.md#variant-fv-17).

</details>

### SIM-FV-28 — decision checkpoint

A targeted read shows that the URL builder depends on a shared encoding helper used by three services. What should exploration do next?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Expand into the demonstrated dependency chain and inspect affected callers before choosing the repair. Newly evidenced cross-cutting dependencies require appropriately expanded investigation.

**Base choice:** A large codebase bug starts with targeted symbol search, relevant caller reads and a file/dependency ledger. Expand only the evidence path needed for the defect.

**Changed constraint and recovery:** The failure crosses the API boundary. Add the adjacent client/server dependencies and contract tests rather than preserving an artificially narrow scope.

**Failure:** Compaction loses a function’s exception condition. Re-read the actual file at the current commit before editing.

**Nearest alternative:** A guessed summary cannot replace current code evidence. Reading the whole repository also makes the decisive detail harder to retain.

**Conditional cue:** Map the path; read the dependency; refresh before edit.

**Proof:** Inspect `ledger={commit,files:[handler,caller],symbols:[retry],unresolved:[ownership],next:test_contract}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.4.md#variant-fv-28).

</details>


<span data-assessment-exposure="cct-fv-12-base-v1,cct-fv-12-retry-v1,cct-fv-15-base-v1,cct-fv-15-retry-v1,cct-fv-16-base-v1,cct-fv-16-retry-v1,cct-fv-17-base-v1,cct-fv-17-retry-v1,cct-fv-28-base-v1,cct-fv-28-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-12 — Search before making a scoped edit](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.5.md#variant-fv-12) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.5&variant=FV-12)
- [FV-15 — Load rules for the affected paths](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.3.md#variant-fv-15) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.3&variant=FV-15)
- [FV-16 — Plan when uncertainty crosses boundaries](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.4.md#variant-fv-16) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.4&variant=FV-16)
- [FV-17 — Change the hypothesis after repeated failure](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.5.md#variant-fv-17) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.5&variant=FV-17)
- [FV-28 — Build a minimal code evidence ledger](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.4.md#variant-fv-28) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.4&variant=FV-28)

**Build the mechanism:** [Lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.