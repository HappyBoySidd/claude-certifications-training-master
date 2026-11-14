# CCAR-F SIM-05 — Scenario 4: Developer Productivity with Claude

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

### Stage 1 — The server is configured, but the capability is absent

A developer connects a document-search MCP server. The connection appears healthy, yet the agent cannot search documents. The tool was not included in that agent’s available capability set.

**Original exam-style practice — choose ONE.** Which diagnosis correctly distinguishes MCP connectivity, tool availability and authorization?

A. Treat a successful server connection as proof every agent may execute every server tool.

B. Verify server discovery/health, the agent’s exposed tool set, and the service authorization independently.

C. Add credentials to the user-facing prompt so the model can repair access.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** A working connection is a doorway, not proof that this agent has the search tool or permission to use it. A merges three checks; C exposes secrets and does not create a legitimate control.

**Follow the changed path:**

```text
configured server → discovered tool → included in agent scope → authorized request → result
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Compare discovery output with the agent-visible tool list and an authorized synthetic test. Redact credentials from retained logs.

</details>

**Changed-constraint decision — choose ONE before revealing:** No external service is needed; a repository filename pattern is known. A: use local Glob then Read; B: introduce MCP solely because it is available.

<details><summary>Reveal changed-constraint reasoning</summary>

A. Choose the local capability that matches the job. Search content with Grep; locate matching paths with Glob; inspect selected files with Read.

</details>

**Objective connections:** [2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md), [2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.5.md).

### Stage 2 — A resumed case remembers the old approval

A support case continues tomorrow. A summary remembers the customer’s goal and yesterday’s approved proposal, but the amount has changed. The application needs continuity without treating remembered state as fresh permission.

**Original exam-style practice — choose ONE.** Which resumption strategy best preserves useful context while respecting changing external facts?

A. Restore a bounded state packet containing goal, decisions, sources and unresolved work, then refresh volatile facts and revalidate approvals before effects.

B. Paste the entire transcript and assume every old fact remains current.

C. Start from nothing and discard the case identifier.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice A.** A summary is a handover note, not a live bank record. A retains useful work and rechecks time-sensitive facts. B keeps old errors and stale authority; C loses continuity. Session resumption and business authorization are different layers.

**Follow the changed path:**

```text
case checkpoint → restored task/state → refreshed evidence and authority → next permitted step
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Change the amount or expire approval between sessions. The restored case must request the necessary fresh check instead of submitting based on the old summary.

</details>

**Changed-constraint decision — choose ONE before revealing:** Only a small repository area matters. A: read every file into context; B: retain the map and search/read relevant paths as needed.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Keep the route to evidence and fetch what matters. Context size alone does not guarantee relevant understanding.

</details>

**Objective connections:** [5.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.1.md), [5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-5.4.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** An engineer opens an unfamiliar codebase and asks for help understanding it, finding relevant files and automating repetitive work. The input is a practical development request; the output should be useful findings or a reviewable change grounded in that repository. This simulation explores the tools and working context involved.

**Build the application picture first:** [AS 05 code change](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-05-code-change.md) · [AS 03 grounded assistant](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-03-grounded-assistant.md)

**Primary domains:** 2 Tools and MCP, 3 Claude Code, 1 Agentic Architecture · **Decisions:** 10 ·
**Time:** 20 min for the decisions, plus about 15 for the twists and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 4, Tier 1)

You're building developer productivity tools with the Claude Agent SDK. The agent helps engineers
explore unfamiliar codebases, understand legacy systems, generate boilerplate and automate
repetitive tasks. It uses the **built-in tools (Read, Write, Bash, Grep, Glob)** and connects to MCP
servers.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. Find every caller of `calculateTax()`. Which tool?
2. Find all `**/*.test.tsx` files. Which tool?
3. An Edit fails because its anchor text appears 4 times in the file. What next?
4. An engineer needs to understand an unfamiliar legacy module. How does the agent explore it?
5. The team wants a Jira integration. How do you set it up?
6. You want to try an experimental MCP server just for yourself. Answering the way the exam guide
   describes it, where does it go?
7. The internal-docs MCP server has a tool that searches the docs by topic and returns the
   matching sections with links. The agent keeps running Grep over the raw doc files instead, and
   misses those sections. What's the fix?
8. The agent makes many exploratory calls just to find out which database schemas exist. What do
   you offer it instead?
9. "Add comprehensive tests to this legacy codebase." How should the agent approach it?
10. Yesterday's investigation is saved as a named session, `tax-audit`. Since then, teammates have
    changed 3 of the files it read. How do you continue it?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | Find every caller of `calculateTax()` | **Grep** | Glob; Read every file; Bash `find` then Read each result | D2 2.5 Built-in tools | [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 2 | Find all `**/*.test.tsx` files | **Glob** | Grep; Bash `ls` in each folder; Read the directory tree folder by folder | D2 2.5 Built-in tools | [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 3 | Edit fails because the anchor text appears 4 times | **Read, then Write** the whole file (or a more unique anchor) | Retry the same Edit; ask the model to "be careful" choosing the anchor and retry; switch to a bigger model | D2 2.5 Built-in tools | [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 4 | Understanding an unfamiliar legacy module | **Step by step:** Grep for entry points, then Read to follow imports | Read the whole repo up front; a bigger context window and load every file; ask the model to describe "typical" legacy patterns from memory | D2 2.5 Built-in tools | [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 5 | Team Jira integration | A **community MCP server** in the project's `.mcp.json` with `${JIRA_TOKEN}` | Build a custom server from scratch; commit the token in `.mcp.json`; have each developer add it to their own `~/.claude.json`, so setups drift | D2 2.4 MCP server integration | [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 6 | A personal experimental server | **`~/.claude.json`** (user scope). Also accept local scope (the default for `claude mcp add`, also stored in `~/.claude.json` but for this project only) as right for today's Claude Code; on the exam, pick user-level `~/.claude.json`. See [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | The project's `.mcp.json`, which pushes it on the whole team; the team's shared settings file; paste the server's URL into CLAUDE.md | D2 2.4 MCP server integration | [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 7 | The agent greps raw docs instead of using the internal-docs MCP search tool | **Improve the MCP tool's description** (what it can do, what it returns, when to use it) | Remove Grep; tell the prompt "always use MCP"; list the MCP server first in the config, which changes nothing about what the model knows the tool can do | D2 2.4 MCP server integration; D2 2.1 Tool interfaces and descriptions | [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md), [Lesson 2, section 2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 8 | The agent makes many exploratory calls to find which DB schemas exist | Expose the schema catalog as **MCP resources** | A bigger context window; more tools; a prompt that lists the schema names by hand and goes stale | D2 2.4 MCP server integration | [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| 9 | "Add comprehensive tests to this legacy codebase" | **Dynamic decomposition:** map the structure, find high-impact areas, plan by priority, adapt | A fixed prompt chain over every file alphabetically; one giant "add tests everywhere" prompt; raise the iteration cap so it keeps going | D1 1.6 Task decomposition | [Lesson 1, section 1.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 10 | Continue the named session `tax-audit` after teammates changed 3 of its files | **`--resume tax-audit` and tell it which files changed.** If most results are stale, start fresh with a summary. | Resume and say nothing; re-explore everything; resume and ask it to "double-check everything" | D1 1.7 Session state, resumption and forking | [Lesson 1, section 1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |

**Scoring:** 8 or more is a pass.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 4 and task statements 1.6, 1.7, 2.1, 2.4, 2.5 (Tier 1); Claude Code docs on MCP and the
CLI at code.claude.com (Tier 1). Taught in lessons
[L01](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md)
and [L02](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: an hour in, the agent forgets what it found

**What changed:** an hour into exploring a legacy system, the agent starts describing the payment
module as if it calls the bank directly. Earlier it found that every payment goes through a queue
service. Its answers no longer match what it read.

**Question:** what do you do?

<details><summary><b>Answer and why</b></summary>

**Keep the key findings outside the chat and keep the main context clean.** Have the agent write a
scratchpad file of findings and re-read it, hand narrow questions to subagents that return short
summaries, and use `/compact` when discovery output piles up.

**Why the others lose:** a model with a bigger context window still fills up with search output.
Restarting and exploring everything again throws away an hour of work.

**Tests:** Domain 5, task statement 5.4 (large-codebase exploration).

**Lesson:** [Lesson 5, section 5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#54-exploring-a-large-codebase) · [Deep practice, Domain 5](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/05-context-management-and-reliability.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 5.4 (Tier 1).

</details>

### Twist 2: the function is re-exported under a wrapper

**What changed:** you need every use of the billing helpers, but a wrapper module re-exports them,
and other code imports them from the wrapper.

**Question:** how does the agent find every caller?

<details><summary><b>Answer and why</b></summary>

**First list the names the wrapper exports, then Grep for each name across the codebase.** That
catches callers that import through the wrapper as well as those that import directly.

**Why the others lose:** Grepping only for the original module path misses everyone who imports
through the wrapper. Reading every file that might be involved is slow and fills the context.

**Tests:** Domain 2, task statement 2.5 (built-in tools).

**Lesson:** [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#25-built-in-tools) · [Deep practice, Domain 2](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/02-tool-design-and-mcp-integration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 2.5 (Tier 1).

</details>

### Twist 3: thirty endpoints, the same steps every time

**What changed:** the team wants boilerplate for 30 new API endpoints. Every endpoint needs the
same steps in the same order: the route, request validation, a handler stub and a unit-test stub.

**Question:** how should the agent structure the job?

<details><summary><b>Answer and why</b></summary>

**A fixed sequential pipeline (prompt chaining):** the same focused steps for each endpoint, in
the same order. The work is predictable, so a fixed chain is cheaper, easier to check and gives
the same shape every time. Save dynamic decomposition for open-ended work, like the legacy test
job in decision 9. Exam guide wording: "When to use fixed sequential pipelines (prompt chaining)
versus dynamic adaptive decomposition based on intermediate findings".

**Why the others lose:** dynamic decomposition, where the agent re-plans after each endpoint, adds
cost and variation to work that never changes. One giant prompt for all 30 endpoints mixes every
step into one pass and is hard to check. Letting each engineer prompt it by hand gives 30 slightly
different endpoints.

**Tests:** Domain 1, task statement 1.6 (task decomposition).

**Lesson:** [Lesson 1, section 1.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#16-breaking-the-task-down) · [Deep practice, Domain 1](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/01-agentic-architecture-and-orchestration.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 1.6 (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: find every caller of `calculateTax()`**

- **What's going on:** you're looking for text written inside files.
- **Under the hood:** Grep searches file *contents* for a pattern, like a function name. Glob matches file *names and paths*, like `*.ts`. A call to a function is text inside a file.
- **How to make the call:** if you're searching for what's written inside files (a call, an error message, an import), use Grep; if you're searching by file name or extension, use Glob. Exam wording (task statement 2.5): "Selecting Grep for searching code content across a codebase (e.g., finding all callers of a function, locating error messages)".
- **Why the tempting answers are wrong:**
  - **Use Glob instead:** matches file names, not what's inside them.
  - **Read every file:** slow, and fills the context.
  - **Bash `find`, then Read:** a file-name search plus reading everything.
- **Go deeper:** [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#25-built-in-tools)

**Decision 2: find all `**/*.test.tsx` files**

- **What's going on:** you're looking for files by their name pattern.
- **Under the hood:** `**/*.test.tsx` is a glob pattern: `**` means "any folder, any depth" and `*` means "any name". Glob returns the matching file paths without opening any file.
- **How to make the call:** if you're searching by file name or extension, use Glob; if you're searching for text inside files, use Grep. Exam wording (task statement 2.5): "Selecting Glob for finding files matching naming patterns (e.g., `**/*.test.tsx`)".
- **Why the tempting answers are wrong:**
  - **Use Grep instead:** searches inside files, not their names.
  - **Bash `ls` in each folder:** manual, and easy to miss deep folders.
  - **Read folder by folder:** slow and noisy.
- **Go deeper:** [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#25-built-in-tools)

**Decision 3: an Edit fails because its anchor text appears 4 times**

- **What's going on:** the edit tool can't tell which of four matching spots you mean.
- **Under the hood:** Edit replaces one exact piece of text (the anchor), and that text must appear only once in the file (unless `replace_all: true` is set, which changes every copy). When it appears four times, Edit can't choose, so it fails.
- **How to make the call:** if Edit fails on a match that isn't unique, Read the whole file and Write it back with the change; a longer anchor that appears only once also works. Exam wording (task statement 2.5): "When Edit fails due to non-unique text matches, using Read + Write as a fallback for reliable file modifications".
- **Why the tempting answers are wrong:**
  - **Retry the same Edit:** same text, same failure.
  - **"Be careful" and retry:** care doesn't make the text unique.
  - **Bigger model:** the anchor still appears four times.
- **Go deeper:** [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#25-built-in-tools)

**Decision 4: exploring an unfamiliar legacy module**

- **What's going on:** a big unknown module, and limited room to read it all.
- **Under the hood:** every file the agent reads takes up room in its context window (how much text it can see at once). Grep finds the entry points cheaply; Read then follows imports only along the paths that matter.
- **How to make the call:** if the code is large and unfamiliar, start with Grep for entry points, then Read to follow imports outward; don't load everything up front. Exam wording (task statement 2.5): "Building codebase understanding incrementally: starting with Grep to find entry points, then using Read to follow imports and trace flows, rather than reading all files upfront".
- **Why the tempting answers are wrong:**
  - **Read the whole repo:** fills the context with noise.
  - **Bigger window, load everything:** the same noise, with more room.
  - **"Typical" patterns from memory:** guesses, not this code.
- **Go deeper:** [Lesson 2, section 2.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#25-built-in-tools)

**Decision 5: the team wants a Jira integration**

- **What's going on:** the whole team needs the same standard integration.
- **Under the hood:** a project's `.mcp.json` (the team's list of MCP servers, the plug-ins that give the agent tools) is committed to the repo, so everyone gets it. `${JIRA_TOKEN}` is filled in from each person's environment, so no secret is committed.
- **How to make the call:** if it's a standard tool many teams use, pick an existing community MCP server; if the workflow is specific to your team, build your own. Share it in `.mcp.json` with `${...}` tokens. Exam wording (task statement 2.4): "Choosing existing community MCP servers over custom implementations for standard integrations (e.g., Jira), reserving custom servers for team-specific workflows".
- **Why the tempting answers are wrong:**
  - **Build a custom server:** rebuilds an integration that already exists.
  - **Commit the token:** a leaked secret.
  - **Each developer's `~/.claude.json`:** setups drift apart.
- **Go deeper:** [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#24-mcp-servers-in-claude-code-and-agents)

**Decision 6: an experimental MCP server just for you**

- **What's going on:** you want to try something without pushing it on the team.
- **Under the hood:** MCP servers have scopes (who they apply to). `.mcp.json` in the repo is shared; `~/.claude.json` (user scope) applies only to you. Today `claude mcp add` defaults to local scope: same file, this project only, suggested for "experimental configurations". On the exam, pick user level.
- **How to make the call:** if only you need the server, put it in `~/.claude.json`; if the team needs it, put it in `.mcp.json`. Exam wording (task statement 2.4): "MCP server scoping: project-level (.mcp.json) for shared team tooling vs user-level (~/.claude.json) for personal/experimental servers".
- **Why the tempting answers are wrong:**
  - **Project `.mcp.json`:** pushes it on the whole team.
  - **Team shared settings:** still shared with everyone.
  - **URL in CLAUDE.md:** text, not a connected server.
- **Go deeper:** [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#24-mcp-servers-in-claude-code-and-agents)

**Decision 7: Grep instead of the docs MCP tool**

- **What's going on:** it grabs the familiar tool; it can't tell the other is better.
- **Under the hood:** the model picks a tool by its name and description. Today Claude Code's tool search (on by default) loads only MCP tool names at start, so a clear description matters even more.
- **How to make the call:** if the agent skips a better tool, improve that tool's description: what it does, what it returns, and when to use it instead of Grep. If it's clear, check the prompt for steering wording. Exam wording (task statement 2.4): "Enhancing MCP tool descriptions to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools (like Grep) over more capable MCP tools".
- **Why the tempting answers are wrong:**
  - **Remove Grep:** loses a needed tool.
  - **"Always use MCP":** blunt; wrong for plain text search.
  - **List the MCP server first:** the guide's fix is the description; reordering doesn't tell the model what the tool can do.
- **Go deeper:** [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#24-mcp-servers-in-claude-code-and-agents), [Lesson 2, section 2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#21-tool-descriptions-are-how-the-model-chooses)

**Decision 8: many calls just to learn which schemas exist**

- **What's going on:** the agent keeps knocking on doors to see what's behind them.
- **Under the hood:** MCP resources are content a server offers for reading, like a catalog. They let the agent see what data exists without calling tools to probe for it. Tools do things; resources show what's there.
- **How to make the call:** if the agent spends many calls just finding out what exists, expose that catalog (schemas, a docs index) as MCP resources; if it needs to act on the data, that's a tool. Exam wording (task statement 2.4): "MCP resources as a mechanism for exposing content catalogs (e.g., issue summaries, documentation hierarchies, database schemas) to reduce exploratory tool calls".
- **Why the tempting answers are wrong:**
  - **Bigger context window:** the same calls, with more room.
  - **More tools:** more choices, more probing.
  - **Schema names in the prompt:** goes stale.
- **Go deeper:** [Lesson 2, section 2.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md#24-mcp-servers-in-claude-code-and-agents)

**Decision 9: "add comprehensive tests to this legacy codebase"**

- **What's going on:** a huge, open job with no obvious first step.
- **Under the hood:** a fixed chain runs the same steps in the same order every time. Dynamic decomposition lets the agent plan subtasks from what it finds, and change the plan as dependencies show up.
- **How to make the call:** if you can't know the steps until you look, map the structure, find the high-impact areas, plan by priority, and adapt. If every item needs the same steps, use a fixed chain. Exam wording (task statement 1.6): "Decomposing open-ended tasks (e.g., "add comprehensive tests to a legacy codebase") by first mapping structure, identifying high-impact areas, then creating a prioritized plan that adapts as dependencies are discovered".
- **Why the tempting answers are wrong:**
  - **Fixed chain, alphabetical:** treats a trivial file like a critical one.
  - **One giant prompt:** no plan, no priorities.
  - **Higher iteration cap:** more turns, still no plan.
- **Go deeper:** [Lesson 1, section 1.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#16-breaking-the-task-down)

**Decision 10: continue yesterday's work after 3 files changed**

- **What's going on:** yesterday's notes are mostly right, but three files changed.
- **Under the hood:** `--resume <name>` (here `--resume tax-audit`) reopens a saved session with its history, including old tool results. Those results show the files as they were, so the agent has to be told which ones changed.
- **How to make the call:** if most of the old context is still valid, resume and name the changed files so it re-checks just those; if most is stale, start fresh with a structured summary. Exam wording (task statement 1.7): "Informing a resumed session about specific file changes for targeted re-analysis rather than requiring full re-exploration".
- **Why the tempting answers are wrong:**
  - **Resume, say nothing:** works from old file contents.
  - **Re-explore everything:** throws away valid work.
  - **"Double-check everything":** a full re-exploration by another name.
- **Go deeper:** [Lesson 1, section 1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#17-sessions-resume-and-fork)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-06](SIM-06-claude-code-ci-cd.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-07 — decision checkpoint

An analyst wants to compare two independent interpretations from the same verified baseline without overwriting the original investigation. Which session approach fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Fork from the baseline and keep branch conclusions separately attributable. Forking supports alternative exploration while retaining the shared starting point.

**Base choice:** An interrupted legal repository investigation resumes with source pointers and a checkpoint. Re-read changed files and revalidate permissions before continuing.

**Changed constraint and recovery:** The learner wants an alternative investigation without replacing the existing trajectory. Fork the session, but revalidate the same mutable assumptions.

**Failure:** A stored path was renamed and prior access revoked. Reacquire current evidence; do not trust an old tool result just because the session resumed.

**Nearest alternative:** Resume and fork preserve or branch state; neither renews authorization nor makes stale evidence current.

**Conditional cue:** Resume the reasoning; refresh the mutable evidence.

**Proof:** Inspect `checkpoint={commit:abc,paths:[policy.md],permissions_checked:old}; current_commit:def` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.7.md#variant-fv-07).

</details>

### SIM-FV-11 — decision checkpoint

A connected MCP server advertises a resource. The host has not discovered or included that resource in the agent’s context. What should the architect verify?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Verify host resource discovery, permissions and explicit inclusion rather than assume connection supplied content. Server availability does not establish host inclusion or model-visible evidence.

**Base choice:** A shared marketing repository uses safe project MCP configuration with secrets provided outside committed files. Inspect the actual host’s tool/resource discovery behavior.

**Changed constraint and recovery:** A developer tests a personal server. Keep its configuration in the appropriate personal/local scope instead of committing credentials to the team project.

**Failure:** The server connects but the expected resource is not in model context. Check listing, host support and explicit inclusion; do not claim automatic availability.

**Nearest alternative:** Connectivity is not proof that every resource was discovered or supplied. Resource behavior depends on host support and invocation.

**Conditional cue:** Connect, discover, include: prove each stage.

**Proof:** Inspect `project_config={server:crm,secret:environment}; trace=[connected,listed,included]` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md#variant-fv-11).

</details>

### SIM-FV-13 — decision checkpoint

A child directory’s instructions conflict with applicable project policy on retaining evidence. The conflict changes the requested output. What should the agent do?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Identify the applicable instruction files and resolve the conflict according to authority before editing. An identified instruction conflict needs explicit resolution rather than accidental behavior.

**Base choice:** A shared repository convention belongs in project instructions; personal preferences stay in personal configuration. Trace which nested instructions apply to the current path.

**Changed constraint and recovery:** A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file.

**Failure:** Two applicable files disagree on test behavior. Surface and resolve the conflict using the runtime’s documented loading/scope rules.

**Nearest alternative:** More copies increase drift. Instruction files guide model behavior; they do not replace enforced permission checks.

**Conditional cue:** Shared at project; specific at path; resolve conflicts.

**Proof:** Inspect `instructions={shared:CLAUDE.md,package:services/CLAUDE.md,personal:user}; target=services/api.py` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.1.md#variant-fv-13).

</details>

### SIM-FV-14 — decision checkpoint

A user gives one short task with complete inputs that is unlikely to recur. What should the agent create?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Use the task brief directly without introducing a reusable workflow solely for this one case. A one-off complete brief does not automatically justify maintaining a reusable abstraction.

**Base choice:** A repeated reviewed-release brief becomes a scoped skill with required commit, evidence paths and output expectations. Check discovery and allowed dependencies.

**Changed constraint and recovery:** A single ad hoc explanation is needed. Use a brief rather than creating a reusable asset without repeated need.

**Failure:** The skill is invoked without the reviewed commit. Stop with a missing-input message instead of inventing a build identity.

**Nearest alternative:** A reusable skill is not permission to publish. Invocation and downstream authorization remain separate.

**Conditional cue:** Reuse the workflow; require its inputs; preserve permission.

**Proof:** Inspect `skill_input={reviewed_commit,tests,evidence}; output={changes,limits,next_action}` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.2.md#variant-fv-14).

</details>


<span data-assessment-exposure="cct-fv-07-base-v1,cct-fv-07-retry-v1,cct-fv-11-base-v1,cct-fv-11-retry-v1,cct-fv-13-base-v1,cct-fv-13-retry-v1,cct-fv-14-base-v1,cct-fv-14-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-07 — Resume with fresh permissions](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.7.md#variant-fv-07) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.7&variant=FV-07)
- [FV-11 — Separate connection from inclusion](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md#variant-fv-11) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.4&variant=FV-11)
- [FV-13 — Put instructions at their real scope](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.1.md#variant-fv-13) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.1&variant=FV-13)
- [FV-14 — Give reusable skills a contract](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.2.md#variant-fv-14) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.2&variant=FV-14)

**Build the mechanism:** [Lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.