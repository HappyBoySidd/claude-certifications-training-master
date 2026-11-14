# Deep practice 3: Claude Code configuration and workflows

**Picture the application:** A new teammate opens a repository and expects the same coding conventions and review workflow that work on its author’s machine. Start with that shared-work requirement and a small requested code change. The configuration mechanisms below determine which guidance and reusable procedures reach the task.

This page covers Domain 3 of CCAR-F, Claude Code configuration and workflows, one task statement at a time. It goes
deeper than [Lesson 3](../L03-claude-code-configuration-and-workflows.md): each section gives the core idea, how it works under the hood,
the look-alike wrong answers, a worked example and a one-line exam reflex. Read the lesson first.
Objective lessons for this page: [1.4](../objectives/objective-1.4.md) · [1.5](../objectives/objective-1.5.md) · [3.1](../objectives/objective-3.1.md) · [3.2](../objectives/objective-3.2.md) · [3.3](../objectives/objective-3.3.md) · [3.4](../objectives/objective-3.4.md) · [3.5](../objectives/objective-3.5.md) · [3.6](../objectives/objective-3.6.md).

Domain 3 is 20% of the exam. Sections 3.1 to 3.6 come first, in number order. Two hook skills from
Domain 1 (1.4 and 1.5) come last, because they are Claude Code configuration choices; the business-rule
half of 1.4 and 1.5 is in [deep practice 1](01-agentic-architecture-and-orchestration.md). Builds on
[L03](../L03-claude-code-configuration-and-workflows.md).
Citation keys like `[Hooks]` are listed at the bottom.

## Exam answer vs today's docs

| Topic | Exam's expected answer | What changed since (one line) |
|---|---|---|
| Commands | `.claude/commands/` (project) vs `~/.claude/commands/` (personal) [Guide 3.2] | Commands are merged into skills; old command files still work [Skills]. **On the exam: pick `.claude/commands/` for team commands.** |
| `allowed-tools` | "restrict tool access during skill execution" [Guide 3.2] | Today it only pre-approves tools; removing tools is `disallowed-tools` [Skills]. **On the exam: pick `allowed-tools` to restrict.** |
| `argument-hint` | "prompt developers for required parameters" [Guide 3.2] | Today it is an autocomplete hint such as `[issue-number]` [Skills]. **On the exam: pick `argument-hint` for missing parameters.** |
| Subagent tool name | `Task` [Guide 1.3] | Renamed `Agent` in Claude Code 2.1.63; `Task(...)` still works as an alias [Subagents]. **On the exam: pick `Task`.** |
| `/memory` | "verify which memory files are loaded" [Guide 3.1] | Lists locations; `/context` lists, under Memory files, the CLAUDE.md files loaded at launch. Path-scoped rules and subfolder CLAUDE.md files load later, with a "Loaded …" line in the terminal [Memory]. **On the exam: pick `/memory`.** |
| `@import` depth | not tested | "a maximum depth of four hops" [Memory]. **On the exam: not asked; ignore.** |

The same rows, with the other domains, are in one place: [exam answer vs today](conditions-and-errors.md#exam-answer-vs-today).

---

## 3.1 CLAUDE.md hierarchy, scope and modules

Lesson: [L03 section 3.1](../L03-claude-code-configuration-and-workflows.md#31-the-claudemd-hierarchy) · Objective: [3.1](../objectives/objective-3.1.md)

**Exam wording:** `Task Statement 3.1: Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization` [Guide]

### Core idea

Every piece of context has a right home. Ask two questions: **who needs it** (just me, the team,
one package) and **when** (every session, only when touching some files, only for this task).

### Under the hood

**Where files live** [Memory] (the exam names the first three [Guide 3.1]):

| Level | Path | Who gets it |
|---|---|---|
| Managed policy | e.g. macOS `/Library/Application Support/ClaudeCode/CLAUDE.md` | Everyone in the org; "cannot be excluded" |
| User | `~/.claude/CLAUDE.md` | Only you, every project. Not in version control. |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | The team, through git |
| Local | `./CLAUDE.local.md` | Only you, this project; add it to `.gitignore` |
| Directory | `sub/dir/CLAUDE.md` | The team; loads when Claude works in that folder |

**How they load** [Memory]:

- Files in the working directory and every folder **above** it load at launch.
- Files in **subfolders** load on demand, "when Claude uses the Read, Write, or Edit tool on a file
  in those subdirectories".
- They are "concatenated into context rather than overriding each other", root first. So it's not
  CSS: there's no "most specific wins". Conflicting lines make Claude "pick one arbitrarily".
- Target under 200 lines per file; longer files "reduce adherence".

**`@` imports** [Memory]: `@path/to/import` inside a `CLAUDE.md`. Relative paths resolve from the
importing file. Imported files load at launch with it. Max "four hops". Exam use: each package's
`CLAUDE.md` imports only the standards it needs, e.g. `@../../standards/api.md` [Guide 3.1].

**`.claude/rules/`**: topic files (`testing.md`, `api-conventions.md`) instead of one giant
`CLAUDE.md` [Guide 3.1]. Without `paths` frontmatter they load always; with it, see TS 3.3.

**`/memory`** "lists your CLAUDE.md, CLAUDE.local.md, and other memory file locations across user
and project scopes" [Memory]. Exam use: "verify which memory files are loaded and diagnose
inconsistent behavior across sessions" [Guide 3.1].

### The context-placement decision

| The info is... | Put it in | Why |
|---|---|---|
| Needed in every session by the whole team | project `CLAUDE.md` | Always loaded, shared through git |
| A big standards doc that only some packages need | `@import` from those packages' `CLAUDE.md` (exam answer [Guide 3.1]) | Modular and easy to maintain. The context saving comes from the *package* `CLAUDE.md` being a subfolder file that loads only when Claude works there. The import itself saves nothing: imports "don't reduce its context cost, because imported files also load at launch" [Memory] |
| Only relevant for some file types anywhere in the repo | `.claude/rules/x.md` with `paths:` | Loads only when matching files are touched |
| Needed for **this task** only, in a known file | `@file` mention in the prompt (check current docs for prompt `@` mentions) | No lasting cost; precise |
| A one-off fact ("the bug is in the retry loop") | type it in the prompt | It's about this task, not the project |
| A repeatable workflow you run sometimes | a skill or command | On demand, not always loaded |
| A rule that must never be broken | settings or a hook (TS 1.4) | Enforced |
| Your own preference | `~/.claude/CLAUDE.md` or `CLAUDE.local.md` | Doesn't affect teammates |

### Look-alikes

- **"Put the team's API conventions in `~/.claude/CLAUDE.md`."** Only you get them. The classic
  diagnosis: "a new team member not receiving instructions because they're in user-level rather
  than project-level configuration" [Guide 3.1].
- **"Paste the whole 900-line standards doc into the root `CLAUDE.md`."** Loads everywhere, lowers
  adherence. Split into `.claude/rules/` or `@import` per package.
- **"Add this one-off bug detail to `CLAUDE.md` so Claude remembers it."** Pollutes every future
  session. Say it in the prompt.
- **"The subfolder `CLAUDE.md` overrides the root one."** They're combined, not overridden.

### Worked example (scenario: developer productivity with Claude)

A monorepo has `payments/` and `web/`. The payments team's PCI rules are in the root `CLAUDE.md`, so
web developers' sessions carry 300 irrelevant lines and Claude sometimes applies PCI rules to UI
code. A new hire on payments says Claude ignores the team's test rules, which live in a senior's
`~/.claude/CLAUDE.md`.

- Move PCI rules to `standards/pci.md`, imported with `@` from `payments/CLAUDE.md`.
- Move the test rules into the repo (project `CLAUDE.md` or `.claude/rules/testing.md`), commit.
- Ask both developers to run `/memory` to confirm what loads. (Exam answer. Today `/memory` lists memory
  file locations; `/context` lists, under Memory files, the CLAUDE.md files loaded at launch. A path-scoped
  rule or a subfolder CLAUDE.md loads later, and the terminal shows a "Loaded …" line when it does.)

**Exam reflex:** *Who needs it and when? Team + always → project `CLAUDE.md`. Some packages →
`@import`. Some file types → `.claude/rules/` with `paths`. This task → the prompt. Must hold →
settings/hook. Check with `/memory` (exam answer; today `/context` lists the CLAUDE.md files loaded at launch, and later loads show a "Loaded …" line).*

---

## 3.2 Custom slash commands and skills

Lesson: [L03 section 3.2](../L03-claude-code-configuration-and-workflows.md#32-slash-commands-and-skills) · Objective: [3.2](../objectives/objective-3.2.md)

**Exam wording:** `Task Statement 3.2: Create and configure custom slash commands and skills` [Guide]

### Core idea

A command or skill is a saved prompt you run by name. The folder decides who has it. A skill is
loaded **on demand**; `CLAUDE.md` is **always** loaded.

### Under the hood

- Project (shared through git): `.claude/commands/` and `.claude/skills/<name>/SKILL.md`.
  Personal: `~/.claude/commands/` and `~/.claude/skills/` [Guide 3.2].
- Personal variants of a team skill get a **different name**, "to avoid affecting teammates"
  [Guide 3.2]. Why a new name matters today: when a personal and a project skill share a name,
  "Enterprise over personal, and personal over project" applies [Skills]. Your copy would silently
  replace the team's skill for you, and you'd stop seeing the team's updates. **On the exam: pick
  "personal copy with a different name".**
- SKILL.md frontmatter the exam names [Guide 3.2]; current definitions [Skills]:
  - `context: fork`: "run in a forked subagent context". Exam use: keep verbose output (codebase
    analysis) or exploration (brainstorming) out of the main conversation. `agent` picks the subagent
    type.
  - `allowed-tools`: exam = restrict tools (e.g. file writes only). Today = pre-approve; restricting
    is `disallowed-tools` (see the changes table).
  - `argument-hint`: e.g. `[issue-number]`, shown when you type the command.
  - `disable-model-invocation: true` (not in the guide): only you can start it with `/name`.
- Choosing: skills for "on-demand invocation for task-specific workflows", `CLAUDE.md` for
  "always-loaded universal standards" [Guide 3.2].

### Look-alikes

- **"Put the team's `/review` command in `~/.claude/commands/`."** Only you get it. Move to
  `.claude/commands/` and commit.
- **"Put the 400-line release checklist in `CLAUDE.md`."** Used twice a month; loads every session.
  Make it a skill.
- **"Edit the team skill to suit you."** Changes it for everyone. Make a differently-named personal copy.

### Worked example

A `/analyze-deps` skill dumps 2,000 lines of dependency output and the main session runs out of
room. Add `context: fork` so it runs in a subagent and returns a summary; add `argument-hint:
[package-name]`.

**Exam reflex:** *Team → `.claude/...` and commit. Personal → `~/.claude/...` with a new name.
Noisy → `context: fork`. Sometimes → skill; always → `CLAUDE.md`.*

---

## 3.3 Path-specific rules

Lesson: [L03 section 3.3](../L03-claude-code-configuration-and-workflows.md#33-path-specific-rules) · Objective: [3.3](../objectives/objective-3.3.md)

**Exam wording:** `Task Statement 3.3: Apply path-specific rules for conditional convention loading` [Guide]

### Core idea

Some rules only matter for some files: test files, Terraform files. Tie the rule to a file pattern so
it loads only when Claude touches those files, wherever they live.

### Under the hood [Memory]

```markdown
---
paths:
  - "**/*.test.tsx"
  - "terraform/**/*"
---
# Test and Terraform conventions
...
```

- File lives in `.claude/rules/` (subfolders are fine; found recursively).
- `paths` takes glob patterns. Brace expansion works: `"src/**/*.{ts,tsx}"`.
- "Path-scoped rules trigger when Claude uses the Read, Write, or Edit tool on a file matching the
  pattern, not on every tool use."
- Rules **without** `paths` load every session.
- Exam: rules beat subfolder `CLAUDE.md` "when conventions must apply to files spread across the
  codebase" (e.g. `**/*.test.tsx`) [Guide 3.3].

### Look-alikes

- **"Add a `CLAUDE.md` to each of the 40 folders that contain tests."** Duplicated, drifts, misses
  new folders. One rule with `**/*.test.tsx`.
- **"Put the test rules in the root `CLAUDE.md`."** Loads for every task, wasting context.
- **"Use `.claude/rules/` without `paths`."** Then it's always loaded, not conditional.

### Worked example (scenario: code generation with Claude Code)

Test files sit next to source files in 60 folders. Testing conventions are ignored half the time.
Create `.claude/rules/testing.md` with `paths: ["**/*.test.tsx", "**/*.test.ts"]`.

**Exam reflex:** *Files of one type spread everywhere → `.claude/rules/` with a `paths` glob.*

---

## 3.4 Plan mode vs direct execution

Lesson: [L03 section 3.4](../L03-claude-code-configuration-and-workflows.md#34-plan-mode-or-direct-execution) · Objective: [3.4](../objectives/objective-3.4.md)

**Exam wording:** `Task Statement 3.4: Determine when to use plan mode vs direct execution` [Guide]

### Core idea

Big, risky or open-ended change → look and plan first. Small, clear change → just do it.

### Under the hood

- Plan mode: Claude "reads files and runs read-only shell commands to explore but doesn't edit your
  source files" [Perms]. Start in it with `--permission-mode plan` [CLI], or switch modes with
  `Shift+Tab` during a session [CLI].
- Use plan mode for "large-scale changes, multiple valid approaches, architectural decisions, and
  multi-file modifications" (e.g. a microservice split, a library migration across 45+ files)
  [Guide 3.4].
- Direct execution for "simple, well-scoped changes" (one validation check; a single-file bug fix
  with a clear stack trace) [Guide 3.4].
- Combine: plan the migration, then execute the plan directly [Guide 3.4].
- **Explore subagent:** isolates verbose discovery and returns a summary, so the main context isn't
  used up [Guide 3.4]. It's a built-in agent; a `deny` rule `Agent(Explore)` turns it off [Perms].
  What changed since: the subagent tool the exam calls `Task` was renamed `Agent` in Claude Code
  2.1.63, and `Task(...)` still works as an alias [Subagents]. **On the exam: pick `Task`.**

### Look-alikes

- **"Plan mode for a typo fix."** Overhead for no gain.
- **"Direct execution for the 45-file migration because the team is in a hurry."** Rework risk.
- **"Read the whole codebase in the main session before planning."** Floods context. Use Explore.

### Worked example

Move from one HTTP client library to another across 52 files, with two possible adapter designs.
Plan mode first; Explore subagent maps the call sites and returns a summary; pick the design; then
execute directly, folder by folder.

**Exam reflex:** *Many files or many valid approaches → plan mode (+ Explore). Clear and small →
direct.*

---

## 3.5 Iterative refinement

Lesson: [L03 section 3.5](../L03-claude-code-configuration-and-workflows.md#35-refining-step-by-step) · Objective: [3.5](../objectives/objective-3.5.md)

**Exam wording:** `Task Statement 3.5: Apply iterative refinement techniques for progressive improvement` [Guide]

### Core idea

When Claude's code isn't right, don't just say "try again". Give it something concrete to aim at:
examples, failing tests, or answers to its own questions. And group your feedback the right way.

### Under the hood (the four techniques) [Guide 3.5]

1. **2 to 3 concrete input/output examples** when "natural language descriptions produce
   inconsistent results". Examples are "the most effective way to communicate expected
   transformations when prose descriptions are interpreted inconsistently".
2. **Test-driven iteration:** write tests "covering expected behavior, edge cases, and performance
   requirements before implementation, then iterating by sharing test failures". For one edge case,
   give "specific test cases with example input and expected output (e.g., null values in migration
   scripts)".
3. **The interview pattern:** have Claude ask you questions first, "to surface design considerations
   (e.g., cache invalidation strategies, failure modes) before implementing solutions in unfamiliar
   domains".
4. **Group feedback by how the issues relate:**
   - Issues that **interact** (fixing one changes another) → "a single detailed message".
   - **Independent** issues → "sequential iteration", one at a time.

### Look-alikes

- **"Rewrite the instructions more clearly and in more detail."** Prose has already been read
  inconsistently. Switch to examples.
- **"Send all 6 review comments at once to save time."** Right only if they interact. If they're
  independent, one at a time keeps each fix clean and checkable.
- **"Fix the three interacting issues one per message."** Each fix can break the others; send them
  together with how they connect.
- **"Let Claude start coding the caching layer and correct it as you go."** In an unfamiliar domain,
  interview first.
- **"Tell Claude 'it still fails on nulls'."** Give the exact input and expected output.

### Worked example (scenario: code generation with Claude Code)

A date-normalizer keeps getting edge cases wrong. "Handle all common formats" gave three different
results. Do this:

1. Give 3 input/output pairs: `"03/04/2026" → "2026-03-04"` (US), `"4 Mar 2026" → "2026-03-04"`,
   `"" → null`.
2. Ask Claude to write tests for those plus time zones first, then implement until they pass.
3. Two review issues remain: the time-zone handling and the DST offset interact (send them together);
   a log message typo is independent (send it later on its own).

### Second worked example: interview first, then tests first (scenario: developer productivity with Claude)

Nobody on the team has built a cache before. You ask Claude to add one to a pricing service.

1. **Interview.** "Before writing any code, ask me the questions you need answered." Claude asks:
   how stale may a price be? What clears an entry: a time limit, or a "price changed" event? If the
   cache is down, do we read from the database or fail?
2. **Tests first.** "Write tests for: a hit returns the cached price; a price-change event clears
   that key; cache down means read from the database; 1,000 reads in under 50 ms. Don't implement
   yet."
3. **Implement, then share the exact failure.** Claude implements and runs the tests. One fails:

```text
FAILED test_invalidation_on_price_change
  expected 19.99, got 24.99 (old entry served after the price-change event)
```

   Paste that output and say "fix only this failure".

Trace look-alikes for this example:

- **After step 3 you write "tests are failing, please fix".** No failure output, so Claude guesses.
  Paste the real failure.
- **You write a detailed spec yourself and skip the interview.** Fine in a domain you know. Here
  you don't know what to ask (failure modes, invalidation), which is exactly when the guide wants the
  interview pattern.
- **You let Claude write the tests after the code.** Tests written after the code tend to match
  the code, bugs included. Tests first define "done".

**Exam reflex:** *Prose not working → 2 to 3 examples. Write tests first and share failures.
Unfamiliar domain → interview. Interacting issues together; independent ones one by one.*

---

## 3.6 Claude Code in CI/CD

Lesson: [L03 section 3.6](../L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd) · Objective: [3.6](../objectives/objective-3.6.md)

**Exam wording:** `Task Statement 3.6: Integrate Claude Code into CI/CD pipelines` [Guide]

### Core idea

In CI, nobody is there to answer a prompt. Run Claude Code non-interactively, get JSON a script can
read, give it the project's rules through committed files, and never let the session that wrote the
code be the one that reviews it.

### Under the hood

- **`-p` / `--print`**: non-interactive, prints and exits. Exam: "to prevent interactive input hangs"
  [Guide 3.6].
- **`--output-format`**: `text` (default), `json`, or `stream-json` [Headless]. With `json` the payload
  includes the answer in `.result` plus session ID, usage and `total_cost_usd` [Headless].
- **`--json-schema`**: "validated JSON output matching a JSON Schema after the agent completes its
  workflow (print mode only)" [CLI]. The structured answer arrives in `structured_output` [Headless].
  Exam: findings you can post "as inline PR comments" [Guide 3.6].
- Guard rails (print mode): `--max-turns` ("Exits with an error when the limit is reached"),
  `--max-budget-usd`, `--permission-mode`, and `--tools` to limit which tools exist [CLI].
  Careful: `--allowedTools` only **pre-approves** tools so they run without a prompt; it doesn't
  remove the others. "To restrict which tools are available, use `--tools` instead" [CLI].
- **Context in CI:** the committed `CLAUDE.md` and `.claude/settings.json` come with the repo.
  Personal files (`~/.claude/...`, `settings.local.json`, `CLAUDE.local.md`) are not on the CI
  machine. Exam: document "testing standards, valuable test criteria, and available fixtures in
  CLAUDE.md" [Guide 3.6].
- **Independent reviewer:** "the same Claude session that generated code is less effective at
  reviewing its own changes compared to an independent review instance" [Guide 3.6]. A separate
  `claude -p` run with its own prompt.
- **Re-runs on new commits:** include prior findings, report "only new or still-unaddressed issues
  to avoid duplicate comments" [Guide 3.6].
- **Test generation:** give it the existing test files so it doesn't suggest duplicates [Guide 3.6].
- `--continue` skips sessions created with `claude -p` [CLI]. To pick one up again, take
  `session_id` from the JSON output and pass it to `--resume`: `claude -p "Continue that review"
  --resume "$session_id"` [Headless].
- A blocking pre-merge check uses this synchronous run, never the Batch API (deep practice 4, TS 4.5).

```bash
git diff origin/main...HEAD | claude -p "Review this diff against the CLAUDE.md review criteria. Prior findings: $(cat prior.json). Report only new or unaddressed issues." \
  --output-format json --json-schema "$(cat findings.schema.json)" \
  --max-turns 15 --tools "Read,Grep,Glob" \
  | jq '.structured_output'
```

### Look-alikes

- **"Run `claude "review"` in the pipeline."** No `-p`: it waits for input and the job hangs.
- **"Parse the text output with a regex."** Use `--output-format json` + `--json-schema`.
- **"Have the generating session also approve the PR to save tokens."** Self-review is weaker.
- **"Re-run the full review on every commit and post everything."** Duplicate comments. Pass prior
  findings in.
- **"Put the review criteria in the CI runner's `~/.claude/CLAUDE.md`."** Not versioned with the
  repo; drifts. Use the project `CLAUDE.md`.

### Worked example (scenario: Claude Code for continuous integration)

Every push to a PR triggers review. Developers complain about repeat comments and generic test
suggestions that duplicate existing tests. Fix: store each run's JSON findings as an artifact; on
the next push pass them in with "report only new or unaddressed"; give the generator the existing
test files; put fixture names and "what makes a valuable test" in the project `CLAUDE.md`. Generation
and review are two separate `claude -p` runs.

**Exam reflex:** *CI → `-p` + `--output-format json` + `--json-schema`. Context from committed
`CLAUDE.md`. Separate review run. Feed prior findings back in.*

---

## 1.4 Enforced vs advice (Claude Code half)

Lesson: [L01 section 1.4](../L01-agentic-architecture-and-orchestration.md#14-enforcement-and-handoff) · Objective: [1.4](../objectives/objective-1.4.md)

**Exam wording:** `Task Statement 1.4: Implement multi-step workflows with enforcement and handoff patterns` [Guide]

### Core idea

`CLAUDE.md` is **advice**. Claude reads it and usually follows it. Usually is not always. Hooks and
permission settings are **enforced**: code runs, or a rule blocks the action, whatever Claude
"decides". If a rule must hold every single time, it can't live only in `CLAUDE.md`.

Exam wording: know "The difference between programmatic enforcement (hooks, prerequisite gates)
and prompt-based guidance", and that when "deterministic compliance is required ... prompt
instructions alone have a non-zero failure rate" [Guide 1.4].

The official docs say the same thing in a table: "Use settings for technical enforcement and
CLAUDE.md for behavioral guidance" [Memory]. Their examples: "Block specific tools, commands, or
file paths" → `permissions.deny`; "Code style and quality guidelines" → `CLAUDE.md` [Memory].

### Under the hood: the three tools and what each guarantees

| Mechanism | Where | Guarantee | Use for |
|---|---|---|---|
| `CLAUDE.md` | `CLAUDE.md`, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md` | None. It's context. | Style, conventions, "how we work" |
| Permission rules | `permissions.allow` / `ask` / `deny` in a settings file | Enforced by Claude Code | "Never read `.env`", "never run `git push`" |
| Hooks | `hooks` key in a settings file | Enforced; your script runs every time the event fires | "Lint after every edit", "block edits to `migrations/`" |

**Permission order.** "Rules are evaluated in order: deny, then ask, then allow. The first match in
that order determines the outcome, and rule specificity doesn't change the order" [Perms]. So a
broad `deny` beats a narrow `allow`. Exam shorthand: **deny > ask > allow.**

**Settings precedence** (highest first) [Settings]:

1. Managed settings (`managed-settings.json`, MDM, or server-managed). Nothing overrides them.
2. Command-line arguments (this session only).
3. Project local: `.claude/settings.local.json` (just you, this project; not committed).
4. Shared project: `.claude/settings.json` (committed; the whole team).
5. User: `~/.claude/settings.json` (just you, every project).

Two traps: list keys such as `permissions.allow` **merge** across files instead of replacing each
other [Settings], and `deny` still wins at evaluation time. Check what loaded with `/status`
("Setting sources" line) [Settings].

### Look-alikes

- **"Add 'ALWAYS run the linter after editing' in capitals to `CLAUDE.md`."** Stronger wording is
  still advice. Use a PostToolUse hook.
- **"Put the rule in `~/.claude/CLAUDE.md` so it applies everywhere."** User-level, so teammates don't
  get it, and it's still advice.
- **"Add an `allow` rule for `Bash(npm test)` to override the `deny` on `Bash`."** Deny is checked
  first.
- **"Write a skill that runs the linter."** Skills load on demand. Nothing makes them run every time.

### Worked example (scenario: code generation with Claude Code)

The team's `CLAUDE.md` says "Never edit files in `db/migrations/`". Twice this month Claude edited one
while fixing a test. Smallest guaranteed fix: in the committed `.claude/settings.json`, add
`"deny": ["Edit(./db/migrations/**)"]`. If you need a custom message or logic, use a PreToolUse hook
with matcher `Edit|Write` that exits `2` for those paths. Keep the `CLAUDE.md` line as context.

**Exam reflex:** *Must always happen → hook or settings. Nice to have → `CLAUDE.md`. Deny beats
ask beats allow.*

---

## 1.5 PostToolUse quality hooks (quality-hook half)

Lesson: [L01 section 1.5](../L01-agentic-architecture-and-orchestration.md#15-agent-sdk-hooks) · Objective: [1.5](../objectives/objective-1.5.md)

**Exam wording:** `Task Statement 1.5: Apply Agent SDK hooks for tool call interception and data normalization` [Guide]

### Core idea

A `PostToolUse` hook runs **after** a tool finishes. It can't undo the tool call. What it can do:
check the result (run the formatter, linter, tests) and tell Claude what's wrong so Claude fixes it
in the next step. Or, in the Agent SDK, clean up the tool result before Claude reads it.

Exam wording: "Hook patterns (e.g., PostToolUse) that intercept tool results for transformation
before the model processes them", and "Implementing PostToolUse hooks to normalize heterogeneous
data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools" [Guide 1.5].

### Under the hood

**Config shape (Claude Code, in a settings file)** [Hooks]:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/lint.sh" }
        ]
      }
    ]
  }
}
```

- `matcher` is tested against the tool name; `"Edit|Write"` means either. No matcher = every event
  of that type [SDK-Hooks].
- The script reads the event as JSON on stdin [Hooks].

**Exit codes (memorize)** [Hooks]:

| Exit code | Meaning | Trap |
|---|---|---|
| `0` | Success. With no output, "the tool call continues through the normal permission flow". JSON on stdout is read. | — |
| `2` | "a blocking error". On events that can block, it blocks "whether or not you print JSON: even a JSON `permissionDecision` of `"allow"` can't override it". stderr becomes the message. | — |
| any other (e.g. `1`) | Non-blocking error. "Claude Code treats exit code 1 as a non-blocking error and proceeds with the action, even though 1 is the conventional Unix failure code." | A guard script that `exit 1`s **does not block**. |

**What exit 2 does per event** (the ones the exam cares about) [Hooks]:

| Event | Can block? | On exit 2 |
|---|---|---|
| `PreToolUse` | Yes | "Blocks the tool call" |
| `PostToolUse` | **No** | "Shows stderr to Claude; the tool already ran" |
| `UserPromptSubmit` | Yes | Blocks the prompt |
| `Stop` / `SubagentStop` | Yes | Prevents stopping; the conversation continues |
| `SessionStart` | No | Shows stderr to the user only |

**JSON decision fields** [Hooks]:

- `PreToolUse`: `hookSpecificOutput.permissionDecision` = `allow` / `deny` / `ask` / `defer`, plus
  `permissionDecisionReason`. (Extra, beyond the guide: `defer`, only in `-p` and Agent SDK runs; and `updatedInput`, which rewrites
  the tool's arguments before it runs.)
- `PostToolUse`, `Stop`, `UserPromptSubmit`: top-level `"decision": "block"` with a `reason`.
  For `PostToolUse` this feeds the reason back to Claude; the tool has still already run.
- `additionalContext` (inside `hookSpecificOutput`) adds a note to Claude's context.
- Pick one style per hook: exit codes alone, or exit `0` and print JSON [Hooks].

**Agent SDK version (the exam's "Agent SDK hooks")** [SDK-Hooks]: hooks are callbacks registered
by event with a matcher, e.g. `"PostToolUse": [HookMatcher(matcher="...", hooks=[callback])]`. A
`PostToolUse` callback can set `additionalContext` "to append information to the tool result", or
`updatedToolOutput` "to replace the tool's output before Claude sees it". That replacement is how
you normalize timestamps or status codes from different MCP tools.

### The quality-hook pattern, step by step

1. Claude calls `Edit` on `src/cart.ts`.
2. The edit happens. `PostToolUse` fires; matcher `Edit|Write` matches.
3. `lint.sh` reads `tool_input.file_path` from stdin, runs the formatter and linter on that file.
4. Clean → `exit 0`. Errors → print them to stderr and `exit 2` (or print `{"decision": "block",
   "reason": "<lint output>"}`).
5. Claude sees the errors and fixes them in its next step.

Keep the hook fast and scoped to the changed file. Running the whole test suite on every edit slows
every step. Many teams run the full suite in a `Stop` hook (blocks stopping until tests pass) or in
CI (practice, not doc).

### Look-alikes

- **"Use a PostToolUse hook to stop Claude from editing the file."** Too late; the edit already
  happened. Blocking is `PreToolUse`.
- **"The hook exits 1 when lint fails, so Claude will fix it."** Exit 1 is non-blocking; Claude may
  never see it. Use `2` or a JSON `decision`.
- **"Ask Claude in `CLAUDE.md` to normalize dates from every MCP tool."** Advice, and it costs
  tokens each time. A PostToolUse hook normalizes in code, every time.
- **"Normalize in a PreToolUse hook."** PreToolUse sees the *call*, not the *result*.

### Worked example (scenario: developer productivity with Claude)

An agent uses three MCP tools. One returns Unix timestamps, one ISO 8601, one `"status": 3`. The agent
misorders events. Fix: an SDK `PostToolUse` hook with a matcher for those tools converts every time
to ISO 8601 and maps status codes to names, returned through `updatedToolOutput`. Claude only ever
sees one format.

**Exam reflex:** *PostToolUse = after; it checks and reports, it can't block. Block = PreToolUse.
Only exit `2` blocks; `1` doesn't. Normalize results in PostToolUse, not in the prompt.*

---

## Quick sheet: exact values

| Fact | Value | Source |
|---|---|---|
| User / project / local memory | `~/.claude/CLAUDE.md` / `./CLAUDE.md` or `./.claude/CLAUDE.md` / `./CLAUDE.local.md` | [Memory] |
| Import syntax / depth | `@path/to/file` / four hops | [Memory] |
| Path rule | `.claude/rules/*.md` with `paths:` globs | [Memory] |
| See loaded memory | `/memory` (exam answer); today `/memory` lists locations, `/context` lists CLAUDE.md files loaded at launch, and later loads show a "Loaded …" line | [Memory] |
| Settings order | managed > CLI > local > project > user | [Settings] |
| Rule order | deny, then ask, then allow | [Perms] |
| Hook exits | `0` ok · `2` block (stderr to Claude) · other = non-blocking | [Hooks] |
| PostToolUse exit 2 | can't block; stderr shown to Claude | [Hooks] |
| PreToolUse JSON | `permissionDecision`: allow / deny / ask / defer (`defer` only in `-p` and Agent SDK runs) | [Hooks] |
| PostToolUse JSON | `"decision": "block"`, `reason` | [Hooks] |
| SDK result rewrite | `updatedToolOutput` (PostToolUse) | [SDK-Hooks] |
| Skill fields | `context: fork`, `agent`, `allowed-tools`, `disallowed-tools`, `argument-hint` | [Skills] |
| Plan mode | `--permission-mode plan`; `Shift+Tab` cycles modes | [CLI], [Perms] |
| CI | `-p`, `--output-format json`, `--json-schema`, `--max-turns`; `--tools` restricts, `--allowedTools` only pre-approves | [CLI], [Headless] |
| Resume a `-p` run | `--resume "$session_id"` (from the JSON output) | [Headless] |
| Subagent tool | exam `Task`; today `Agent` (alias kept) | [Guide], [Subagents] |

## Sources (citation keys, all Tier 1, checked 2026-10-06)

- `[Guide]`, `[Guide x.y]` the official CCAR-F exam guide v1.0 (July 2026, Anthropic); x.y is the task statement.
- `[Memory]` [Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory)
- `[Settings]` [Settings](https://code.claude.com/docs/en/settings)
- `[Perms]` [Permissions](https://code.claude.com/docs/en/permissions)
- `[Hooks]` [Hooks reference](https://code.claude.com/docs/en/hooks)
- `[SDK-Hooks]` [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- `[Skills]` [Skills](https://code.claude.com/docs/en/skills)
- `[Subagents]` [Subagents](https://code.claude.com/docs/en/sub-agents)
- `[CLI]` [CLI reference](https://code.claude.com/docs/en/cli-reference)
- `[Headless]` [Headless mode](https://code.claude.com/docs/en/headless)

## Not confirmed on an official page today

- `@file` mentions inside a prompt (as opposed to `@import` inside `CLAUDE.md`): standard Claude Code
  use, but the page that documents it was not re-read in this pass.
- Exact `Shift+Tab` cycle order for entering plan mode: the CLI page confirms `Shift+Tab` cycles
  permission modes; the order wasn't checked.
- "Run the full suite in a `Stop` hook or CI, not on every edit": practice, not doc.

**Next:** [Lesson 2, tool design and MCP integration](../L02-tool-design-and-mcp-integration.md), the next lesson in the study order, or back to the [CCAR-F lessons page](../README.md).