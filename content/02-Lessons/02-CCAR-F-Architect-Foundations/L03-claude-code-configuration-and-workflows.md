# CCAR-F Lesson 3 — Claude Code Configuration and Workflows (20%, about 12 questions)

**Picture the application:** A teammate tries to run the same review command that works on its author’s machine, but cannot find it. The team needs a repeatable review workflow available with the project. Claude Code configuration is the technical layer that determines which instructions and reusable activities each working context receives.

**Time:** 2 hours plus [lab 03, the MCP server wired into Claude Code with a guardrail hook](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) · **Practice:** [CCAR-F practice — choose Domain 3](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)
**Scenarios:** 2 Code generation, 4 Dev productivity, 5 CI/CD


<!-- layered-scenario-migration -->
## Learn this domain through connected case studies

Read and predict; no account, code execution or setup is required for these teaching scenes. Each stage names its application and the requirement that fails. Some stages transfer the same decision to a different application; follow the named people and data rather than assuming every stage belongs to one system. The original reference sections remain below for detail. These are original teaching questions, not claimed live exam items. Write your choice before revealing the repair. Diagrams below show AI reasoning and ordinary software checks explicitly in their labels.

### Stage 1 — A useful rule spreads into the wrong files

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

**Objective connections:** [3.1](objectives/objective-3.1.md), [3.2](objectives/objective-3.2.md), [3.3](objectives/objective-3.3.md).

### Stage 2 — A small request crosses several hidden boundaries

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

**Objective connections:** [3.4](objectives/objective-3.4.md), [3.5](objectives/objective-3.5.md).

### Stage 3 — The interactive review hangs in CI

The same review works on a developer’s laptop. In CI, nobody can answer a permission prompt, the log contains prose instead of a usable report, and the job waits until timeout.

**Original exam-style practice — choose ONE.** Which CI integration best supports unattended, auditable Claude Code review?

A. Copy the interactive command unchanged and disable all checks.

B. Provide a supported non-interactive invocation, scoped permissions, explicit input/output contract and exit/error handling.

C. Interpret any process exit as proof the repository is safe.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** A pipeline needs a complete job contract: input revision, allowed work, machine-readable output and failure handling. Non-interactive mode does not itself grant authority. A widens risk without fixing the consumer; C confuses command completion with review quality.

**Follow the changed path:**

```text
commit/diff → constrained headless review → parse and validate report
valid report for current revision → review decision; invalid/error → visible job failure
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Test an unavailable credential, malformed report and stale commit identifier. Each must remain distinguishable from a valid report containing zero findings.

</details>

**Changed-constraint decision — choose ONE before revealing:** A large diff includes a caller/callee mismatch. A: review each file independently only; B: add a bounded cross-file pass after local checks.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Local review finds individual defects; an integration pass checks relationships. Neither a larger token window nor more reviewers automatically creates that coverage.

</details>

**Objective connections:** [3.6](objectives/objective-3.6.md), [4.6](objectives/objective-4.6.md).

<!-- /layered-scenario-migration -->

## Connect plain reasoning to technical choices

Start with the business constraint, then learn the documentation term and the option it rules out. These worked application bridges show both levels: [AS-05-code-change](architecture-studio/AS-05-code-change.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-06-ci-review](architecture-studio/AS-06-ci-review.md#connect-the-simple-explanation-to-technical-design-choices). Read [artifact types and study mode](architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course) before interpreting examples as build instructions. Reading needs no API setup; runnable activities retain their own prerequisites.


## 3.0 The big idea

Most Claude Code questions are really "where does this file live, and who sees it?" Team rules go
in project files that are committed; personal ones stay in your home folder; things only needed
sometimes load on demand. The same setup then runs non-interactively in CI with `-p` and JSON output, once you also set auth, permissions (`--allowedTools`, `--permission-mode`) and limits.

## 3.1 The CLAUDE.md hierarchy

CLAUDE.md supplies project guidance through ordinary Claude Code discovery, and it can live at several levels. Current bare-mode and isolated Explore/fork contexts have distinct discovery rules; verify the actual runtime instead of assuming every session loads every file. Each row is one level; read across for where the file goes and whether teammates get it.

| Level | Location | Shared with the team? |
| --- | --- | --- |
| User | `~/.claude/CLAUDE.md` | **No**, it's only yours |
| Project | `.claude/CLAUDE.md` or root `CLAUDE.md` | Yes, through version control |
| Directory | `sub/dir/CLAUDE.md` | Yes |

- **Current implementation context: settings are separate from CLAUDE.md.** Ordinary precedence
  is managed, command-line settings, project-local, shared-project, then user. Check the specific
  key: restrictive security values, model policy/defaults and some merge rules have documented
  exceptions. `permissions.allow` lists ordinarily merge; this does not override matching denies
  or applicable managed restrictions.
  ([settings precedence and exceptions](https://code.claude.com/docs/en/settings), checked 2026-10-21.)
- **Distribute shared hooks** through committed `.claude/settings.json`. A runtime must actually
  load the applicable settings sources; CLI bare-mode and SDK configuration can change loading.
  ([hooks](https://code.claude.com/docs/en/hooks), checked 2026-10-21.)
- **Classic diagnosis:** a new teammate isn't getting the instructions because they're in *user*
  level, not project level.
- **`@import`** keeps things modular, for example importing only the standards files each package
  needs.
- **`.claude/rules/`** holds topic files (`testing.md`, `api-conventions.md`, `deployment.md`)
  instead of one huge CLAUDE.md.
- **`/memory`** shows which memory files are loaded, which helps explain inconsistent behavior
  (exam answer, task 3.1). Today `/memory` lists memory file locations; `/context` lists, under
  Memory files, the CLAUDE.md files loaded at launch. A path-scoped rule or a subfolder CLAUDE.md
  loads later, and the terminal shows a "Loaded …" line when it does.

## 3.2 Slash commands and skills

Commands and skills are saved instructions you run by name; where you save them decides who has them. Each row is one kind; the columns give the shared (project) folder and the personal (user) folder.

| Kind | Project (shared) | User (personal) |
| --- | --- | --- |
| Commands | `.claude/commands/` | `~/.claude/commands/` |
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/`. **Give personal variants a different name** so teammates aren't affected. |

Custom commands are now part of skills, but `.claude/commands/` still works
([skills docs](https://code.claude.com/docs/en/skills), Tier 1). On the exam, use the two kinds
as the guide names them.

SKILL.md frontmatter:

- **`context: fork`** runs the skill in an isolated subagent, so verbose output (codebase analysis,
  brainstorming) doesn't pollute the main session.
- **`allowed-tools`** limits the tools a skill can use, for example file writes only, to prevent
  destructive actions. On the exam, `allowed-tools` restricts tools; today it only pre-approves
  them (they run without asking), and `disallowed-tools` blocks
  ([exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
- **`argument-hint`** prompts for parameters that are missing. In the current docs it's an
  autocomplete hint: text shown after the command name so you know what arguments to type. On
  the exam, the answer is the guide's: "to prompt developers for required parameters" (exam
  wording, task 3.2).

A **skill is loaded on demand** for task-specific workflows. **CLAUDE.md supplies persistent discovered guidance** for standards in its scope during ordinary operation; bare-mode and isolated-agent exceptions require explicit context.

## 3.3 Path-specific rules

```yaml
---
paths: ["terraform/**/*"]
---
Terraform conventions...
```

- These load only when editing matching files (exam wording, task 3.3). Today's docs say a
  path-scoped rule loads when Claude reads, writes or edits a matching file. Either way, it doesn't
  load every session, which saves context.
- A glob such as `**/*.test.tsx` beats subdirectory CLAUDE.md files when the convention covers files
  **spread across the codebase**.

## 3.4 Plan mode or direct execution

- **Plan mode:** big changes, several valid approaches, architecture decisions, many files (a
  microservice split, a migration touching 45+ files).
- **Direct execution:** a simple, well-scoped change (one validation check, a single-file fix with
  a clear stack trace).
- **Why:** plan mode lets Claude explore the codebase and design before it changes anything, which
  prevents costly rework; a small, clear fix doesn't need that step (task 3.4).

- You can combine them: **plan the migration, then carry it out directly**.
- The **Explore subagent** isolates verbose discovery and returns a summary, so the main context
  isn't used up.

## 3.5 Refining step by step

- **2–3 concrete input/output examples** when prose instructions get read inconsistently.
- **Test-driven iteration:** write the tests first (expected behavior, edge cases, performance),
  then share the failures.
- **The interview pattern:** have Claude ask questions first (cache invalidation, failure modes)
  when the domain is unfamiliar.
- Put **interacting** issues in **one** message. Fix **independent** issues **one at a time**.

## 3.6 Claude Code in CI/CD

- **`-p` / `--print`** runs non-interactively, so CI doesn't hang waiting for input.
- **`--output-format json` plus `--json-schema`** give machine-parseable findings you can post as
  inline PR comments.
- **CLAUDE.md** gives CI the project context: testing standards, fixtures and review criteria.
- **What changed since:** today's docs say "In CI or other scripted environments, add `--bare`".
  `--bare` skips hooks, skills, MCP servers **and `CLAUDE.md`**, so with it you pass standards in
  explicitly ([headless docs](https://code.claude.com/docs/en/headless), Tier 1; see
  [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
  **On the exam: pick `-p` with `CLAUDE.md` in the repo as the way CI gets project context.**
- **Independent review instance:** the session that wrote the code is worse at reviewing it.
- On re-runs, **include the earlier findings** and report only new or unaddressed issues, so there
  are no duplicate comments.
- Give it the **existing test files** so it doesn't suggest tests you already have.

> **Watch out:** the flag is lowercase `-p` (long form `--print`). CI/CD is task 3.6 inside
> Domain 3, and Domain 3 as a whole is 20% of the exam; CI/CD is not 20% on its own (exam guide
> v1.0, task 3.6, Tier 1).

## Worked example

The team's `/review` command works for you but not for your new teammate. **Cause:** it lives in
`~/.claude/commands/`. **Fix:** move it to `.claude/commands/` and commit it.

## Traps

- Putting team standards in `~/.claude/CLAUDE.md`.
- **Watch out:** the folder is `.claude/`, not ".cloud". And the guide never says "the most specific
  file always wins, like CSS." It tests where a file lives and who sees it, so answer from that
  (exam guide task 3.1, Tier 1).
- Using plan mode for a one-line fix, or direct execution for a 45-file migration.
- Having the generating session review its own pull request.
- A CI job without `-p`, which hangs.

## Try it (60 min): Claude Code setup (you can do this now in any small repo; it becomes part 2 of lab 03, which you run after L02)

In a small repo, set up a root CLAUDE.md with one `@import`, one `.claude/rules/tests.md` with
`paths`, one project command, and one skill using `context: fork`, `allowed-tools` and
`argument-hint`. Run `/memory` (exam wording) to see the memory locations, then `/context` to see
what loaded at launch. Then run `claude -p "review" --output-format json`.

Done when `/context` lists the root CLAUDE.md under Memory files, the terminal shows
"Loaded .claude/rules/tests.md" after you ask Claude to read a matching test file, and `-p`
returns JSON that parses.

## Done when

- [ ] You can place every file in the hierarchy and say who sees it
- [ ] You can explain `context: fork`, `allowed-tools` and `argument-hint` without notes
- [ ] You can make plan-or-direct calls with a reason
- [ ] You scored 80% or more on [CCAR-F practice — choose Domain 3](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)

**Go deeper:**

- **Deep practice:** [Deep practice 3](deep-practice/03-claude-code-configuration-and-workflows.md), which takes every section of this lesson further.
- **Official course:** *Claude Code in Action* from the [CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) (Anthropic, Tier 1, checked 2026-10-02).
- **Flashcards and drills:** the Domain 3 section of the [flashcards](FLASHCARDS.md) and the 8 Domain 3 drills (14–19, 37, 38) in [HARD-DRILLS.md](HARD-DRILLS.md).
- **Charts:** decision charts [8b Where a team rule lives](deep-practice/decision-charts.md#8b-where-does-a-team-rule-live), [9 Plan mode or direct](deep-practice/decision-charts.md#9-plan-mode-or-just-make-the-change), [10 A Claude Code run in CI](deep-practice/decision-charts.md#10-what-does-a-claude-code-run-in-ci-need) and [10b Who reviews in CI](deep-practice/decision-charts.md#10b-who-reviews-the-code-in-ci); sequence diagram [6 A CI review](deep-practice/sequence-diagrams.md#6-a-ci-review-how-does-claude-code-run-with-nobody-at-the-keyboard).

**Next:** [Deep practice 3](deep-practice/03-claude-code-configuration-and-workflows.md), then [Lesson 2](L02-tool-design-and-mcp-integration.md).

## Sources

- Official exam guide v1.0, task statements 3.1–3.6 (Tier 1).
- Claude Code docs: [memory](https://code.claude.com/docs/en/memory) (`/memory` lists locations,
  `/context` lists the CLAUDE.md files loaded at launch, path-scoped rules load on Read, Write or
  Edit) and
  [headless](https://code.claude.com/docs/en/headless) (`--bare`), checked 2026-10-07 (Tier 1).
- Claude Code docs: [skills](https://code.claude.com/docs/en/skills) for `allowed-tools`,
  `disallowed-tools` and `argument-hint`, and the [CLI reference](https://code.claude.com/docs/en/cli-reference)
  for `-p` and `--output-format` (Tier 1).

## Objective modules

For deeper learning and a separate practice/completion check for each objective:

- [Objective 3.1](objectives/objective-3.1.md)
- [Objective 3.2](objectives/objective-3.2.md)
- [Objective 3.3](objectives/objective-3.3.md)
- [Objective 3.4](objectives/objective-3.4.md)
- [Objective 3.5](objectives/objective-3.5.md)
- [Objective 3.6](objectives/objective-3.6.md)

## Decisions in this domain

| Objective | Decision variant and exact repair |
| --- | --- |
| 3.1 | [FV-13 — Put instructions at their real scope](objectives/objective-3.1.md#variant-fv-13) |
| 3.2 | [FV-14 — Give reusable skills a contract](objectives/objective-3.2.md#variant-fv-14) |
| 3.3 | [FV-15 — Load rules for the affected paths](objectives/objective-3.3.md#variant-fv-15) |
| 3.4 | [FV-16 — Plan when uncertainty crosses boundaries](objectives/objective-3.4.md#variant-fv-16) |
| 3.5 | [FV-17 — Change the hypothesis after repeated failure](objectives/objective-3.5.md#variant-fv-17) |
| 3.6 | [FV-18 — Run CI with observable failure](objectives/objective-3.6.md#variant-fv-18) |

**Interpret local practice targets:** any 80% target above is an optional project study heuristic, not a validated mastery threshold or conversion to the official scaled score. Use fresh decisions, explanations and delayed transfer alongside remaining objective gaps.