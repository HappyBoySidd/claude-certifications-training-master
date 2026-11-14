# CCAR-F flashcards (about 120 cards, weighted by domain)

> **Project-authored, not official.** Written by this project from Anthropic's public CCAR-F exam guide. These are not real exam questions and are not paraphrased from any exam.

**Built from:** [exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications) section 6 (Tier 1) and [CCAR-F objectives](../../01-Curriculum/02-Architect-Track/CCAR-F-objectives.md) · **Import:** [flashcards-anki.csv](flashcards-anki.csv) (front, back, tags) for Anki or Quizlet.

**How to use.** Say the answer out loud before you look. Cards marked **TRAP** show a tempting wrong answer: name why it is wrong and what the design fix is. Most traps are a *setting or a prompt request* standing in for a *design fix*, the pattern from your diagnostic. Anything marked "check the current docs" can change between product releases.

## Domain 1: Agentic Architecture & Orchestration (27%, 32 cards)

### 1.1 Design and implement agentic loops for autonomous task execution

**1.**

Q: In an agentic loop, which field tells your code whether to run a tool or stop?

A: stop_reason: keep looping on "tool_use", stop on "end_turn". It is the model's own structured signal, so no guessing is needed.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1)

**2.**

Q: After your code runs a tool Claude asked for, what must happen before the next request?

A: Append the tool result to the conversation history. Claude can only reason about the next step from what is in its context.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1)

**3.** **TRAP**

Q: Tempting wrong answer: "Stop the loop when Claude's reply contains words like 'done' or 'finished'."

A: Parsing natural language to end the loop is a named anti-pattern. Use stop_reason, which is structured and reliable.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1)

**4.** **TRAP**

Q: Tempting wrong answer: "Set max iterations to 10 as the way the loop ends."

A: An arbitrary cap as the primary stopping rule cuts off real work or wastes turns. stop_reason ends the loop; a cap is only a safety net.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1)

**5.**

Q: Model-driven decision-making vs a pre-configured decision tree: what is the difference?

A: In an agent, Claude picks the next tool from context; a decision tree fixes the sequence in code. Agents fit open tasks; fixed trees fit predictable ones.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.1 (Tier 1)

### 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

**6.**

Q: What is hub-and-spoke in a multi-agent system?

A: A coordinator manages all communication, error handling and routing between subagents. Subagents never talk to each other directly, which keeps flow observable.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1)

**7.**

Q: Do subagents inherit the coordinator's conversation history?

A: No. Each subagent has isolated context and sees only what the coordinator passes it. Missing facts in its output usually mean missing facts in its prompt.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1)

**8.** **TRAP**

Q: Tempting wrong answer: "A competitor analysis covered only pricing and skipped product and support, so give the web-search subagent a longer timeout."

A: If every subagent did what it was asked, the gap is upstream: the coordinator split the topic too narrowly. Fix the decomposition, not a subagent setting.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1)

**9.**

Q: Should a coordinator always route every query through the full subagent pipeline?

A: No. It should analyse the query and invoke only the subagents its complexity needs. Running the full pipeline every time wastes time and cost.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1)

**10.**

Q: How does a coordinator make sure a synthesized report has no coverage gaps?

A: An iterative refinement loop: evaluate the synthesis for gaps, re-delegate targeted queries to search and analysis subagents, re-run synthesis until coverage is enough.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.2 (Tier 1)

### 1.3 Configure subagent invocation, context passing, and spawning

**11.**

Q: Which tool does a coordinator use to spawn a subagent, and what config must allow it?

A: Saved-guide wording: the coordinator uses the Task tool with "Task" in allowedTools for delegation. (Current runtime: the tool is `Agent` (renamed in Claude Code v2.1.63; `Task` still works as an alias), and `allowedTools` only pre-approves tools; see [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1)

**12.** **TRAP**

Q: Tempting wrong answer: "The synthesis subagent ignores earlier findings, so raise its max_tokens."

A: The subagent never received those findings. Pass the complete prior outputs in its prompt; a token limit cannot supply context that was never sent.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1)

**13.**

Q: How do you pass findings between agents without losing which source said what?

A: Use a structured format that separates content from metadata (URL, document name, page). Attribution then survives each hand-off.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1)

**14.**

Q: How do you run three subagents in parallel?

A: Emit three Task tool calls in one coordinator response. Spreading them across separate turns makes them sequential.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1)

**15.**

Q: Should a coordinator's prompt to a subagent give step-by-step procedure or goals?

A: Goals and quality criteria. Procedural scripts stop the subagent adapting to what it finds.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.3 (Tier 1)

### 1.4 Implement multi-step workflows with enforcement and handoff patterns

**16.**

Q: Why can't a system prompt alone guarantee an account-ownership check happens before a SIM swap?

A: Prompt instructions have a non-zero failure rate. When compliance must be deterministic, enforce the order in code with a prerequisite gate.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1)

**17.** **TRAP**

Q: Tempting wrong answer: "Add 'ALWAYS verify identity first' in capitals to the system prompt."

A: Louder wording is still a request the model can skip. A programmatic prerequisite that blocks the downstream tool until verification returns is a guarantee.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1)

**18.**

Q: What does a programmatic prerequisite gate do?

A: It blocks a downstream tool call (e.g. close_account) until the prerequisite step has returned the needed value (e.g. a verified account-holder ID).

Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1)

**19.**

Q: What goes in a handoff summary when an agent escalates to a human?

A: Customer ID, root cause, amounts, and the recommended action, in a structured summary. The human usually cannot see the transcript.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1)

**20.**

Q: A customer raises three separate problems in one message. What is the pattern?

A: Split them into distinct items, investigate each (in parallel where possible) with shared context, then synthesize one unified resolution.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.4 (Tier 1)

### 1.5 Apply Agent SDK hooks for tool call interception and data normalization

**21.**

Q: What does a PostToolUse hook let you do?

A: Intercept a tool result and transform it (e.g. normalize timestamps or status codes) before the model processes it.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1)

**22.**

Q: Which kind of hook blocks a credit-limit increase above a set amount?

A: A PreToolUse hook: it intercepts the outgoing tool call before it runs and blocks or redirects it, e.g. to human approval. It runs in code every time.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1)

**23.** **TRAP**

Q: Tempting wrong answer: "MCP tools return dates in three formats, so tell Claude in the prompt to convert them all to ISO 8601."

A: That relies on the model getting it right every time. A PostToolUse hook normalizes the data deterministically before Claude sees it.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1)

**24.**

Q: Hooks vs prompt instructions: which gives deterministic guarantees?

A: Hooks. Prompt instructions are probabilistic compliance. Choose hooks when a business rule must always hold.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.5 (Tier 1)

### 1.6 Design task decomposition strategies for complex workflows

**25.**

Q: When do you pick prompt chaining over dynamic decomposition?

A: Prompt chaining (fixed sequential steps) for predictable multi-aspect work; dynamic decomposition when later subtasks depend on what you discover.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.6 (Tier 1)

**26.**

Q: How should a large multi-file code review be decomposed?

A: Per-file local analysis passes, then a separate cross-file integration pass. One pass over everything dilutes attention.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.6 (Tier 1)

**27.**

Q: How do you decompose an open task like "add comprehensive tests to a legacy codebase"?

A: Map the structure first, find high-impact areas, then build a prioritized plan that adapts as dependencies are discovered.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.6 (Tier 1)

**28.** **TRAP**

Q: Tempting wrong answer: "For an open-ended investigation, write the full list of subtasks up front so the run is predictable."

A: Open-ended work needs an adaptive plan that generates subtasks from findings. A fixed list misses what you only learn mid-investigation.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.6 (Tier 1)

### 1.7 Manage session state, resumption, and forking

**29.**

Q: How do you continue a specific earlier Claude Code investigation?

A: --resume <session-name> continues that named session with its prior context (name a session with -n or /rename).

Source: CCAR-F exam guide v1.0, section 6, task statement 1.7 (Tier 1)

**30.**

Q: What is fork_session for?

A: Creating independent branches from a shared analysis baseline, e.g. to compare two refactoring approaches without re-doing the analysis. fork_session is an Agent SDK option (Python fork_session=True, TypeScript forkSession: true); the CLI equivalent is --fork-session with --resume or --continue.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.7 (Tier 1)

**31.**

Q: Resume or start fresh? When is a new session with a summary better?

A: When the earlier tool results are stale (files changed a lot). A fresh session with an injected structured summary beats resuming on outdated context.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.7 (Tier 1)

**32.** **TRAP**

Q: Tempting wrong answer: "After editing two files, resume the session and ask Claude to re-explore the whole repo."

A: Wasteful. Resume and tell the agent exactly which files changed so it re-analyses only those.

Source: CCAR-F exam guide v1.0, section 6, task statement 1.7 (Tier 1)

## Domain 2: Tool Design & MCP Integration (18%, 23 cards)

### 2.1 Design effective tool interfaces with clear descriptions and boundaries

**33.**

Q: What is the main thing Claude uses to choose between tools?

A: The tool descriptions. Minimal or overlapping descriptions cause unreliable selection among similar tools.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

**34.** **TRAP**

Q: Tempting wrong answer: "Claude keeps picking the wrong one of two similar tools, so lower the temperature."

A: Sampling settings do not fix ambiguous descriptions. Rewrite the descriptions (purpose, inputs, outputs, when to use vs the other tool) or rename them.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

**35.**

Q: What belongs in a good tool description?

A: Purpose, input formats, example queries, edge cases, outputs and boundaries: when to use it versus similar tools.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

**36.**

Q: Two tools, analyze_content and analyze_document, are misrouted because their names overlap. What is the rename fix?

A: Rename to remove the overlap (e.g. analyze_content becomes extract_web_results) and give it a web-specific description.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

**37.**

Q: One generic tool does several jobs and Claude uses it for the wrong one. What is the split fix?

A: Split it into purpose-specific tools, each with a clear input/output contract and its own description.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

**38.**

Q: How can a system prompt break good tool descriptions?

A: Keyword-sensitive instructions ("whenever the user says 'order', check the customer") create unintended tool associations. Review the prompt for them.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.1 (Tier 1)

### 2.2 Implement structured error responses for MCP tools

**39.**

Q: What is the MCP isError flag for?

A: Telling the agent a tool call failed, so it can decide how to recover instead of treating the output as data.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1)

**40.**

Q: Name the four error categories the guide distinguishes.

A: Transient (timeout, unavailable), validation (bad input), business (policy violation) and permission. Each needs a different recovery.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1)

**41.** **TRAP**

Q: Tempting wrong answer: "Return a simple 'Operation failed' for every error to keep the tool interface clean."

A: Uniform errors stop the agent choosing a sensible recovery. Return errorCategory, isRetryable and a readable description.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1)

**42.**

Q: Why include isRetryable: false on a business-rule error?

A: It prevents wasted retries and, with a customer-friendly explanation, lets the agent tell the user what is going on.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1)

**43.**

Q: A search returns zero results. Is that an error?

A: No, if the query succeeded: it is a valid empty result. An access failure (timeout) is different and needs a retry decision. Report them differently.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.2 (Tier 1)

### 2.3 Distribute tools appropriately across agents and configure tool choice

**44.**

Q: What happens to tool selection when an agent has 18 tools instead of 4-5?

A: Reliability drops because the decision gets harder. Give each agent only the tools its role needs.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1)

**45.** **TRAP**

Q: Tempting wrong answer: "The synthesis agent keeps running web searches, so tell it in the prompt not to search."

A: Remove the search tool from that agent. Tools outside an agent's specialization get misused; scoping tool access is the design fix.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1)

**46.**

Q: What are the tool_choice options?

A: "auto" (may answer in text), "any" (must call some tool), and forced {"type": "tool", "name": "..."} (must call that tool). (Exam wording. Today `any` and forced `tool` return 400 on the models listed in the forced-tool-use table in Define tools (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, checked 2026-10-21): see [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1)

**47.** **TRAP**

Q: Tempting wrong answer: "To make sure extract_metadata runs first, write 'call extract_metadata first' in the prompt."

A: That is a request, not a guarantee. Force it with tool_choice {"type":"tool","name":"extract_metadata"}, then handle later steps in follow-up turns. (Exam wording. Today forced `tool` returns 400 on the models listed in the forced-tool-use table in Define tools (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, checked 2026-10-21): see [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1)

**48.**

Q: A synthesis agent often needs quick fact checks. Give it the full search agent's tools?

A: No. Give a scoped cross-role tool (e.g. verify_fact) for the frequent simple case and route complex cases through the coordinator.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.3 (Tier 1)

### 2.4 Integrate MCP servers into Claude Code and agent workflows

**49.**

Q: Where do you configure an MCP server the whole team should get?

A: Project-level .mcp.json in the repo (shared via version control). Personal or experimental servers go in user-level ~/.claude.json.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.4 (Tier 1)

**50.** **TRAP**

Q: Tempting wrong answer: "Paste the GitHub token into .mcp.json so teammates' servers work."

A: Never commit secrets. Use environment variable expansion such as ${GITHUB_TOKEN} in .mcp.json.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.4 (Tier 1)

**51.**

Q: What are MCP resources good for?

A: Exposing content catalogs (issue summaries, doc trees, schemas) so the agent sees what exists without exploratory tool calls.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.4 (Tier 1)

**52.**

Q: Claude prefers built-in Grep over your more capable MCP search tool. Fix?

A: Improve the MCP tool's description to explain its capabilities and outputs in detail. Selection follows descriptions.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.4 (Tier 1)

### 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

**53.**

Q: Grep or Glob: which finds all callers of a function?

A: Grep, because it searches file contents. Glob matches file paths by name pattern (e.g. **/*.test.tsx).

Source: CCAR-F exam guide v1.0, section 6, task statement 2.5 (Tier 1)

**54.**

Q: Edit fails because the anchor text is not unique. What now?

A: Read the full file, then Write the corrected version. Read + Write is the reliable fallback. (Today Edit can also take `replace_all: true` when every match should change. On the exam, the fallback is Read + Write.)

Source: CCAR-F exam guide v1.0, section 6, task statement 2.5 (Tier 1)

**55.** **TRAP**

Q: Tempting wrong answer: "To understand a new codebase, Read every file first."

A: Build understanding incrementally: Grep for entry points, then Read to follow imports and trace flows. Reading everything floods context.

Source: CCAR-F exam guide v1.0, section 6, task statement 2.5 (Tier 1)

## Domain 3: Claude Code Configuration & Workflows (20%, 24 cards)

### 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

**56.**

Q: Name the three CLAUDE.md levels.

A: User (~/.claude/CLAUDE.md), project (.claude/CLAUDE.md or root CLAUDE.md), and directory (subdirectory CLAUDE.md).

Source: CCAR-F exam guide v1.0, section 6, task statement 3.1 (Tier 1)

**57.** **TRAP**

Q: Tempting wrong answer: "A new teammate isn't getting our conventions, so tell them to run with a higher-effort setting."

A: The conventions are probably in someone's user-level ~/.claude/CLAUDE.md, which is not shared. Move them to project-level CLAUDE.md in the repo.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.1 (Tier 1)

**58.**

Q: How do you keep CLAUDE.md modular?

A: Use @import to pull in specific standards files, or split topics into files under .claude/rules/ (testing.md, api-conventions.md...).

Source: CCAR-F exam guide v1.0, section 6, task statement 3.1 (Tier 1)

**59.**

Q: Which command shows which memory files are actually loaded?

A: /memory. Use it to diagnose inconsistent behaviour across sessions. (Exam answer. Today `/memory` lists memory file locations; `/context` lists, under Memory files, the CLAUDE.md files loaded at launch. A path-scoped rule or a subfolder CLAUDE.md loads later, and the terminal shows a "Loaded …" line when it does.)

Source: CCAR-F exam guide v1.0, section 6, task statement 3.1 (Tier 1)

### 3.2 Create and configure custom slash commands and skills

**60.**

Q: Where does a slash command go so every developer gets it on clone?

A: Project .claude/commands/ (in version control). ~/.claude/commands/ is personal only.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1)

**61.**

Q: What does context: fork do in a skill's SKILL.md frontmatter?

A: Runs the skill in an isolated sub-agent context so verbose or exploratory output does not pollute the main conversation.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1)

**62.**

Q: Name two other skill frontmatter fields from the guide and their jobs.

A: allowed-tools restricts which tools the skill may use; argument-hint prompts the developer for required parameters. (Exam guide wording. In current Claude Code, allowed-tools pre-approves tools and disallowed-tools removes them. See [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1)

**63.** **TRAP**

Q: Tempting wrong answer: "Put a rarely used 200-line release workflow into CLAUDE.md so it's always available."

A: CLAUDE.md is always loaded and meant for universal standards. Task-specific workflows belong in a skill, invoked on demand.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.2 (Tier 1)

### 3.3 Apply path-specific rules for conditional convention loading

**64.**

Q: How do you make a rule load only when Claude edits Terraform files?

A: A file in .claude/rules/ with YAML frontmatter paths: ["terraform/**/*"]. It loads only for matching files.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.3 (Tier 1)

**65.** **TRAP**

Q: Tempting wrong answer: "Test files live next to source everywhere, so add a CLAUDE.md to every directory with test rules."

A: A path-scoped rule with a glob like **/*.test.tsx applies to matching files wherever they live. Directory CLAUDE.md files can't follow files across folders.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.3 (Tier 1)

**66.**

Q: Why do path-scoped rules save tokens?

A: They load only when matching files are edited, so irrelevant conventions stay out of context.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.3 (Tier 1)

**67.**

Q: Rules in .claude/rules/ vs subdirectory CLAUDE.md: which for conventions spread across the codebase?

A: Path-specific rules with glob patterns. Subdirectory CLAUDE.md suits conventions tied to one directory.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.3 (Tier 1)

### 3.4 Determine when to use plan mode vs direct execution

**68.**

Q: When should you use plan mode?

A: Large-scale or multi-file changes, several valid approaches, architectural decisions (e.g. a library migration touching 45+ files).

Source: CCAR-F exam guide v1.0, section 6, task statement 3.4 (Tier 1)

**69.**

Q: When is direct execution right?

A: Simple, well-scoped changes: a single-file bug fix with a clear stack trace, adding one validation check.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.4 (Tier 1)

**70.**

Q: What is the Explore subagent for?

A: Isolating verbose discovery output and returning a summary, so the main conversation's context is preserved.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.4 (Tier 1)

**71.** **TRAP**

Q: Tempting wrong answer: "A big migration keeps running out of context, so switch to a model with a bigger window."

A: Fix the design: plan mode for investigation, the Explore subagent for verbose discovery, then direct execution of the planned approach.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.4 (Tier 1)

### 3.5 Apply iterative refinement techniques for progressive improvement

**72.**

Q: Prose instructions for a transformation give inconsistent results. Best fix?

A: Give 2-3 concrete input/output examples. Examples communicate the transformation better than prose.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1)

**73.**

Q: What is the interview pattern?

A: Have Claude ask you questions before implementing, to surface considerations (cache invalidation, failure modes) you had not anticipated.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1)

**74.**

Q: Several bugs to fix. One message or one at a time?

A: One detailed message when the fixes interact; sequential iteration when they are independent.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1)

**75.** **TRAP**

Q: Tempting wrong answer: "The migration script mishandles nulls, so tell Claude to 'be more careful with edge cases'."

A: Give a specific test case with example input and expected output. Test-driven iteration with shared failures is the reliable fix.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.5 (Tier 1)

### 3.6 Integrate Claude Code into CI/CD pipelines

**76.**

Q: Your CI job hangs waiting for input. What flag fixes it?

A: -p (--print) runs Claude Code non-interactively.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.6 (Tier 1)

**77.**

Q: How do you get machine-parseable findings from Claude Code in CI?

A: --output-format json with --json-schema, so results can be posted as inline PR comments. --json-schema works only in print mode (-p). (Flags: check the current docs.)

Source: CCAR-F exam guide v1.0, section 6, task statement 3.6 (Tier 1)

**78.** **TRAP**

Q: Tempting wrong answer: "In the same session that wrote the code, ask Claude to review its own changes critically."

A: The generating session keeps its reasoning and is less likely to question itself. Use an independent review instance.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.6 (Tier 1)

**79.**

Q: Re-running a CI review after new commits produces duplicate comments. Fix?

A: Include the prior findings in context and instruct Claude to report only new or still-unaddressed issues.

Source: CCAR-F exam guide v1.0, section 6, task statement 3.6 (Tier 1)

## Domain 4: Prompt Engineering & Structured Output (20%, 24 cards)

### 4.1 Design prompts with explicit criteria to improve precision and reduce false positives

**80.**

Q: Why do explicit criteria beat "be conservative"?

A: Vague confidence instructions do not improve precision. Specific categorical criteria (report X, skip Y) do.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.1 (Tier 1)

**81.** **TRAP**

Q: Tempting wrong answer: "Too many false positives, so add 'only report high-confidence findings'."

A: Confidence-based filtering fails. Define which issue types to report and which to skip, with concrete examples per severity.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.1 (Tier 1)

**82.**

Q: One review category has a very high false-positive rate. What do you do while you fix it?

A: Temporarily disable that category to restore developer trust, then improve its prompt. Bad categories undermine trust in good ones.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.1 (Tier 1)

**83.**

Q: How do you get consistent severity labels?

A: Define explicit severity criteria with concrete code examples for each level.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.1 (Tier 1)

### 4.2 Apply few-shot prompting to improve output consistency and quality

**84.**

Q: Detailed instructions still give inconsistent output format. Most effective fix?

A: Few-shot examples showing the exact format (location, issue, severity, fix).

Source: CCAR-F exam guide v1.0, section 6, task statement 4.2 (Tier 1)

**85.**

Q: How many few-shot examples, and of what?

A: 2-4 targeted examples of ambiguous cases, showing the reasoning for why one action beats plausible alternatives.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.2 (Tier 1)

**86.**

Q: Can few-shot examples help Claude handle cases you did not list?

A: Yes. Good examples let the model generalize the judgment to novel patterns, not just match listed cases.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.2 (Tier 1)

**87.** **TRAP**

Q: Tempting wrong answer: "Extraction returns null for fields that exist in odd layouts, so make the fields required."

A: Required fields push the model to invent values. Add few-shot examples showing correct extraction from the varied formats.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.2 (Tier 1)

### 4.3 Enforce structured output using tool use and JSON schemas

**88.**

Q: Most reliable way to get schema-compliant JSON from Claude?

A: Tool use with a JSON schema as the tool's input; read the tool_use block. This removes JSON syntax errors.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1)

**89.**

Q: Several extraction schemas exist and the document type is unknown. tool_choice?

A: "any": Claude must call one of the extraction tools, and picks which. (Exam wording. Today `any` returns 400 on the models listed in the forced-tool-use table in Define tools (https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools, checked 2026-10-21): see [exam answer vs today](deep-practice/conditions-and-errors.md#exam-answer-vs-today).)

Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1)

**90.** **TRAP**

Q: Tempting wrong answer: "Strict schemas via tool use mean the extracted numbers are correct."

A: Schemas stop syntax errors, not semantic ones (line items not summing, values in the wrong field). You still validate in code.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1)

**91.**

Q: A field may be missing from the source document. Required or optional?

A: Optional (nullable), so the model is not pushed to fabricate a value. Add "unclear" and "other" + detail for categories.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.3 (Tier 1)

### 4.4 Implement validation, retry, and feedback loops for extraction quality

**92.**

Q: What should a retry request contain?

A: The original document, the failed extraction, and the specific validation errors, so the model can correct itself.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1)

**93.** **TRAP**

Q: Tempting wrong answer: "Retry the extraction three more times; the missing contract date will turn up."

A: If the fact is not in the document (e.g. it is in an external file not provided), retries cannot help. Retries fix format and structure errors.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1)

**94.**

Q: How do you catch invoices whose line items don't add up?

A: Extract calculated_total alongside stated_total and flag differences; add a conflict_detected boolean for inconsistent sources.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1)

**95.**

Q: What is a detected_pattern field for?

A: Recording which code construct triggered a finding, so you can analyse which patterns developers keep dismissing.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.4 (Tier 1)

### 4.5 Design efficient batch processing strategies

**96.**

Q: Message Batches API: three facts the guide gives.

A: 50% cost savings, up to a 24-hour processing window, no guaranteed latency SLA. (Pricing: check the current docs.)

Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1)

**97.** **TRAP**

Q: Tempting wrong answer: "Move the blocking pre-merge check to batches to save 50%."

A: Batches suit latency-tolerant work (overnight, weekly). Blocking workflows stay on the synchronous API.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1)

**98.**

Q: Can a batch request do multi-turn tool calling?

A: Not a client-side loop: a batch request cannot pause for your code to run a tool and return its result, so those loops need the synchronous API. Batches do support tools, including server tools (tools Anthropic runs for you, such as web search) (Anthropic docs, Message Batches, Tier 1, checked 2026-10-12).

Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1)

**99.**

Q: Some documents in a batch failed. What do you resubmit?

A: Only the failed ones, found by custom_id, with fixes (e.g. chunk documents that were too long).

Source: CCAR-F exam guide v1.0, section 6, task statement 4.5 (Tier 1)

### 4.6 Design multi-instance and multi-pass review architectures

**100.**

Q: Why is self-review in the same session weak?

A: The model keeps its generation reasoning and is less likely to question its own decisions.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.6 (Tier 1)

**101.** **TRAP**

Q: Tempting wrong answer: "Turn on extended thinking so the generator reviews its own code more deeply."

A: An independent instance without the generator's reasoning context catches more than self-review or extended thinking.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.6 (Tier 1)

**102.**

Q: A single review pass over many files gives shallow and contradictory feedback. Design fix?

A: Per-file local passes plus a separate cross-file integration pass for data flow.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.6 (Tier 1)

**103.**

Q: What does a verification pass with per-finding confidence enable?

A: Calibrated review routing: low-confidence findings go to closer review.

Source: CCAR-F exam guide v1.0, section 6, task statement 4.6 (Tier 1)

## Domain 5: Context Management & Reliability (15%, 18 cards)

### 5.1 Manage conversation context to preserve critical information across long interactions

**104.**

Q: What is the risk of progressive summarization in long support chats?

A: Exact numbers, dates, percentages and customer expectations get condensed into vague text. Keep them in a persistent "case facts" block outside the summary.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.1 (Tier 1)

**105.**

Q: What is the "lost in the middle" effect and one mitigation?

A: Models handle the start and end of long inputs best. Put a key-findings summary at the start and use clear section headers.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.1 (Tier 1)

**106.** **TRAP**

Q: Tempting wrong answer: "Order lookups return 40 fields and context fills up, so raise max_tokens."

A: max_tokens limits output, not input bloat. Trim tool outputs to the relevant fields before they accumulate in context.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.1 (Tier 1)

### 5.2 Design effective escalation and ambiguity resolution patterns

**107.**

Q: Name the three appropriate escalation triggers.

A: The customer asks for a human; policy has an exception or gap; the agent cannot make meaningful progress.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.2 (Tier 1)

**108.** **TRAP**

Q: Tempting wrong answer: "Escalate when sentiment analysis shows the customer is angry."

A: Sentiment and self-reported confidence are unreliable proxies for complexity. Use explicit criteria, and always honour an explicit request for a human.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.2 (Tier 1)

**109.**

Q: A customer says "I want a human" on a simple issue. What does the agent do?

A: Hand off immediately, without investigating first. Only if they are frustrated but did not ask does the agent offer to resolve, escalating if they repeat the request.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.2 (Tier 1)

**110.**

Q: A lookup returns three customers named Lee. What does the agent do?

A: Ask for another identifier. Never pick one by heuristic.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.2 (Tier 1)

### 5.3 Implement error propagation strategies across multi-agent systems

**111.**

Q: What should a subagent's error report to the coordinator include?

A: Failure type, what was attempted, partial results and possible alternatives.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.3 (Tier 1)

**112.** **TRAP**

Q: Tempting wrong answer: "If a source times out, return an empty list so the workflow keeps going."

A: Silently turning failures into empty success hides them. Report the access failure with context; empty means the query worked and found nothing.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.3 (Tier 1)

**113.**

Q: Should a subagent pass every transient failure up to the coordinator?

A: No. Retry transient failures locally; propagate only what it cannot resolve, with what was tried and partial results.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.3 (Tier 1)

### 5.4 Manage context effectively in large codebase exploration

**114.**

Q: In a long exploration Claude starts citing "typical patterns" instead of the classes it found. What is happening?

A: Context degradation. Counter it with scratchpad files of key findings, subagents for verbose searches, and /compact.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.4 (Tier 1)

**115.**

Q: How do you design crash recovery for a multi-agent exploration?

A: Each agent exports structured state to a known location; the coordinator loads a manifest on resume and injects it into agent prompts.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.4 (Tier 1)

**116.** **TRAP**

Q: Tempting wrong answer: "Keep all exploration in one main session so nothing is lost."

A: Verbose output degrades the main context. Delegate specific questions to subagents and keep the main agent on coordination.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.4 (Tier 1)

### 5.5 Design human review workflows and confidence calibration

**117.** **TRAP**

Q: Tempting wrong answer: "Overall extraction accuracy is 97%, so remove human review."

A: An aggregate can hide poor results on specific document types or fields. Measure accuracy per type and field first.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.5 (Tier 1)

**118.**

Q: How do you keep measuring errors in high-confidence extractions after automating?

A: Stratified random sampling of those extractions, which also surfaces new error patterns.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.5 (Tier 1)

**119.**

Q: How do you make field-level confidence scores useful for routing?

A: Calibrate the review thresholds against a labeled validation set; route low-confidence or contradictory items to humans.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.5 (Tier 1)

### 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis

**120.**

Q: Two credible sources give different figures. What should the synthesis do?

A: Include both, annotated with their sources. Do not pick one arbitrarily.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.6 (Tier 1)

**121.** **TRAP**

Q: Tempting wrong answer: "A 2021 and a 2025 figure disagree, so flag a contradiction."

A: They may just be different periods. Require publication or collection dates in subagent outputs so time differences are read correctly.

Source: CCAR-F exam guide v1.0, section 6, task statement 5.6 (Tier 1)

## Deck totals

| Domain | Weight | Cards | Share of deck |
| --- | --- | --- | --- |
| 1 Agentic Architecture & Orchestration | 27% | 32 | 26% |
| 2 Tool Design & MCP Integration | 18% | 23 | 19% |
| 3 Claude Code Configuration & Workflows | 20% | 24 | 20% |
| 4 Prompt Engineering & Structured Output | 20% | 24 | 20% |
| 5 Context Management & Reliability | 15% | 18 | 15% |
| **Total** | 100% | 121 | 32 of them TRAP cards |

## Decision-variant recall — closed answer practice

These 30 original free-response cards supplement the existing 121-card set; they are not included in its unchanged Anki export. The fronts reuse the original local decision items, so an exposed scene is not an unseen diagnostic. Answers begin closed.

### FV-01 — recall

A claims agent receives stop_reason=tool_use with two read-only calls, IDs u1 and u2. Both calls finish. What should its Messages orchestration loop do next? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>



**Answer to the front:** Return each result with its matching tool_use_id and send the next model request. The protocol requires results for the requested calls before the next model iteration.

**Paired changed-constraint scene:** A settlement agent receives end_turn after a write returned status=unknown. There are no pending tool calls, but business completion has not been established. What should the application do?

**Answer to the paired scene:** End this model loop and check operation status through the application recovery path before retrying the write. end_turn ends the model turn, while an unknown business effect still needs reconciliation.

**Base choice:** A support agent has one refund tool call pending. Return tool_result with its matching tool_use_id and continue the conversation; keep the business transaction status separately.

**Changed constraint and recovery:** The model returns end_turn, but the payment request timed out. Stop the model loop; do not describe the refund as committed.

**Failure:** A network timeout leaves operation r-17 unknown. Query r-17 status or reconcile by idempotency key before sending another refund.

**Nearest alternative:** A blind refund retry can duplicate a committed transaction. Model termination is not proof of settlement.

**Conditional cue:** Stop the loop on its signal; settle the effect from its receipt.

**Proof:** Inspect `stop_reason=tool_use; pending_id=t17; operation_id=r17; business_status=unknown` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.1.md#variant-fv-01).

</details>

### FV-02 — recall

A law firm requests a vendor comparison covering retention, jurisdiction and operational recovery. Its draft decomposition investigates only three vendors’ prices. What is the best correction? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Have a coordinator allocate the missing comparison dimensions, collect attributed findings and check coverage. Dimension-based coverage repairs the omitted requirements.

**Paired changed-constraint scene:** A lawyer asks for the current retention period of one named policy. One read-only lookup returns the authoritative clause and date. What is the best orchestration choice?

**Answer to the paired scene:** Use the bounded single-agent lookup and return the supported answer. The bounded question is already supported without specialist coordination overhead.

**Base choice:** A legal team compares three vendors on evidence retention, integration cost and deployment permissions. Assign dimensions, require source-tagged findings and let the coordinator integrate the comparison.

**Changed constraint and recovery:** The task becomes one known price lookup from an authorized source. One scoped agent is sufficient; decomposition overhead adds no evidence.

**Failure:** Cost returns, but retention is missing. Re-delegate retention with an explicit gap; do not publish a complete comparison.

**Nearest alternative:** Assigning one vendor to each specialist can hide inconsistent criteria unless the return contracts enforce the same dimensions.

**Conditional cue:** Split by evidence need; count coverage before conclusion.

**Proof:** Inspect `coverage={retention:pending,cost:complete,permissions:complete}; owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.2.md#variant-fv-02).

</details>

### FV-03 — recall

A synthesis specialist is isolated from its parent. Earlier agents found campaign claims and conflicting source dates. Which handoff should the coordinator provide? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Supply the question, scoped findings, source locators, dates and expected output contract explicitly. Explicit context and attribution enable an isolated specialist to reason from prior evidence.

**Paired changed-constraint scene:** Two independent channel audits must finish before synthesis; neither needs the other’s output. What should the coordinator do at dispatch?

**Answer to the paired scene:** Dispatch both independent investigations together with bounded scopes and quality criteria. Independent investigations can run in parallel without inventing a dependency.

**Base choice:** A marketing specialist checks audience evidence. Send the precise question, permitted data, exclusions, cited upstream findings and output contract, not a reference to another unseen chat.

**Changed constraint and recovery:** New consent evidence invalidates the audience assumption. Send the changed evidence and require a revised conclusion.

**Failure:** The specialist claims it used a result never included in its brief. Reject that claim and resend the bounded evidence packet.

**Nearest alternative:** Shared task naming is not shared conversation context; a bare “use the earlier findings” instruction is insufficient.

**Conditional cue:** Send scope, source and shape; never assume shared memory.

**Proof:** Inspect `brief={question:segment_fit,scope:consented_records,evidence:[source:CRM42],return:[finding,source,limits]}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.3.md#variant-fv-03).

</details>

### FV-04 — recall

A transfer approval is bound to account A, amount 800 and proposal version 3. The agent changes the destination and produces version 4. What should the execution gate do? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Reject execution until the changed proposal receives current scoped authorization. Authorization for a different proposal cannot justify the new effect.

**Paired changed-constraint scene:** A bank customer explicitly requests a human while a transfer dispute is unresolved. The receiving officer cannot read the transcript. What should the agent do?

**Answer to the paired scene:** Escalate with verified identity, unresolved issue, evidence, proposal version and operation status. A complete handoff lets the human continue without guessing current state.

**Base choice:** A finance support workflow proposes a 40-unit credit for account A and proposal v2. Trusted verification, scope and current approval are checked by the action handler before the effect.

**Changed constraint and recovery:** The target changes to account B or amount changes to 80. Invalidate the prior approval and request the newly scoped authorization.

**Failure:** Verification expires between draft and execute. Reject the protected action and hand off the complete case with blocked status.

**Nearest alternative:** A prompt reminding Claude to verify cannot enforce the backend boundary. Read-only investigation follows its own access policy.

**Conditional cue:** Bind identity, scope and version; changed target means new gate.

**Proof:** Inspect `gate={account:A,proposal:v2,amount:40,verified:true,approval:current}; requested={account:B,proposal:v2}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.4.md#variant-fv-04).

</details>

### FV-05 — recall

Two document tools return ISO dates and epoch timestamps. Raw evidence must remain auditable, and no external write is involved. Which mechanism best normalizes what the model receives? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Normalize returned data in a post-tool transformation while preserving raw values and provenance. Post-tool normalization is appropriate for already returned read data.

**Paired changed-constraint scene:** A records deletion must never execute when a legal hold is active. The current proposal checks only after the delete tool succeeds. Which design fixes the timing?

**Answer to the paired scene:** Check the hold in a pre-action application gate or blocking pre-tool hook before deletion. A prevention requirement must be enforced before the side effect.

**Base choice:** A fictional service normalizes a successful date result after the tool returns while retaining the original value and parse status.

**Changed constraint and recovery:** The requirement becomes preventing an irreversible account mutation. Move the authorization check before execution, in the application or supported pre-tool control.

**Failure:** A post-result check finds a bad write already happened. Record the effect and invoke reviewed compensation or escalation; result replacement does not undo it.

**Nearest alternative:** A post-action hook can change model-visible output where supported, but cannot retroactively block the completed effect.

**Conditional cue:** Before prevents; after detects; retain raw evidence.

**Proof:** Inspect `trace=proposal -> precheck -> execute -> effect -> postcheck; raw_date=03/04; locale=unknown` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.5.md#variant-fv-05).

</details>

### FV-06 — recall

A campaign compliance review always checks each file against three known criteria and then checks cross-file consistency. Which decomposition fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Use predictable per-file review stages followed by a cross-file integration pass. Known stages support a fixed review chain plus integration.

**Paired changed-constraint scene:** A campaign launch failure has an unknown cause; each log finding may expose a new dependency. Which decomposition fits?

**Answer to the paired scene:** Start an adaptive investigation that expands tasks as evidence reveals relevant dependencies. Unknown causes require investigation that responds to discoveries.

**Base choice:** A government intake follows a known sequence: validate, classify, route. Use an explicit workflow with defined outputs and stop states.

**Changed constraint and recovery:** The task becomes an open-ended investigation with unknown evidence paths. Use bounded adaptive decomposition and review discovered gaps.

**Failure:** After ten iterations the agent has activity but no evidence for one requirement. Stop or re-plan using the coverage ledger, not iteration count alone.

**Nearest alternative:** Multiple agents do not cure an unclear completion contract. Fixed steps are easier to test when the process is known.

**Conditional cue:** Known path: workflow; unknown path: bounded discovery.

**Proof:** Inspect `steps=[validate,classify,route]; done={valid:true,route_assigned:true}; missing=[]` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.6.md#variant-fv-06).

</details>

### FV-07 — recall

A resumed contract session points to an older file revision; the repository revision and user permissions changed overnight. What must happen before relying on its findings? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Reacquire changed files and permissions, retaining only still-valid evidence. Resumption preserves conversation state, not the freshness of external evidence.

**Paired changed-constraint scene:** An analyst wants to compare two independent interpretations from the same verified baseline without overwriting the original investigation. Which session approach fits?

**Answer to the paired scene:** Fork from the baseline and keep branch conclusions separately attributable. Forking supports alternative exploration while retaining the shared starting point.

**Base choice:** An interrupted legal repository investigation resumes with source pointers and a checkpoint. Re-read changed files and revalidate permissions before continuing.

**Changed constraint and recovery:** The learner wants an alternative investigation without replacing the existing trajectory. Fork the session, but revalidate the same mutable assumptions.

**Failure:** A stored path was renamed and prior access revoked. Reacquire current evidence; do not trust an old tool result just because the session resumed.

**Nearest alternative:** Resume and fork preserve or branch state; neither renews authorization nor makes stale evidence current.

**Conditional cue:** Resume the reasoning; refresh the mutable evidence.

**Proof:** Inspect `checkpoint={commit:abc,paths:[policy.md],permissions_checked:old}; current_commit:def` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.7.md#variant-fv-07).

</details>

### FV-08 — recall

A payment catalog has tools named payment_action1 and payment_action2; one drafts, one executes. Their descriptions omit side effects. What change best reduces confusion? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Give draft and execute distinct names, inputs, side-effect descriptions and prerequisite contracts. Distinct tool contracts make operational purpose and requirements explicit.

**Paired changed-constraint scene:** A redesign proposes one universal execute tool that accepts arbitrary action strings. The application must enforce separate read and payment capabilities. Which choice best preserves the boundary?

**Answer to the paired scene:** Keep a separate scoped execution capability with an application authorization check. A narrow execution boundary can be enforced independently of model selection.

**Base choice:** A support catalog separates get_balance, draft_credit and execute_credit. Descriptions specify read versus proposal versus mutation, required scope and return status.

**Changed constraint and recovery:** Two tools both say “manage account.” Rename them and tighten schemas/descriptions so capability boundaries are clear.

**Failure:** Claude picks execute_credit for a lookup. Reject the call at the handler, then repair the catalog rather than merely lengthening the prompt.

**Nearest alternative:** A universal tool can conceal prohibited effects and confuse selection; splitting should follow real capability boundaries, not arbitrary tool-count ceilings.

**Conditional cue:** Name the effect; describe the boundary; validate the arguments.

**Proof:** Inspect `get_balance(account_id)->amount; draft_credit(account_id,amount)->proposal; execute_credit(proposal_id,approval)->receipt` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.1.md#variant-fv-08).

</details>

### FV-09 — recall

A CRM campaign lookup returns success=true and records=[]. What is the appropriate recovery? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Treat this as an empty successful lookup and clarify or widen the query if the task requires records. An empty result is not evidence of transport failure.

**Paired changed-constraint scene:** A campaign creation request times out after transmission; it may have committed and accepts an idempotency key. What should happen before creating another campaign?

**Answer to the paired scene:** Look up the existing operation by its stable key and reconcile status before deciding whether to retry. A potentially committed write needs status reconciliation to avoid duplicates.

**Base choice:** An MCP lookup succeeds with records=[]; report no matching record and clarify filters rather than retrying a supposed outage.

**Changed constraint and recovery:** A timeout is transient and read-only. Retry with a bounded policy. A permission refusal instead requires changed authorization or escalation.

**Failure:** A write times out after submission. Query operation status before retrying; a transient category alone does not establish safe re-execution.

**Nearest alternative:** MCP protocol errors and the application payload are different layers; error strings alone do not define a safe recovery policy.

**Conditional cue:** Empty is evidence; timeout is uncertainty; denied needs authority.

**Proof:** Inspect `application_result={status:success,records:[]}; failure={category:permission,retryable:false}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.2.md#variant-fv-09).

</details>

### FV-10 — recall

A clause research specialist only needs read access to a policy corpus. The coordinator also has a deletion tool. Which tool allocation fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Give the specialist the relevant read tools without the unrelated deletion capability. Minimum relevant capabilities reduce accidental exposure without assuming multi-agent structure alone is safe.

**Paired changed-constraint scene:** A schema-constrained tool call returns an account identifier that is outside the requester’s authorization. What should the application do?

**Answer to the paired scene:** Reject the unauthorized operation even if invocation and schema validation succeeded. Invocation control and shape validation do not confer business authorization.

**Base choice:** Research specialists get only their relevant read tools. A separate authorized executor handles accepted mutations; the coordinator tracks ownership.

**Changed constraint and recovery:** One bounded read-only lookup fits a single agent with two relevant tools. Do not add agents merely to satisfy a tool-count slogan.

**Failure:** Forced tool choice invokes the named tool with invalid semantics. Authorization and application validation still reject it.

**Nearest alternative:** tool_choice governs invocation; it does not prove business permission, factual truth or a sound result.

**Conditional cue:** Choose the call; separately prove permission and meaning.

**Proof:** Inspect `tools={research:[search,read],executor:[approved_write]}; proposal_owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.3.md#variant-fv-10).

</details>

### FV-11 — recall

A team needs a reviewed MCP server configuration shared with its repository, but each developer has a separate credential. What should be committed? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Commit safe project-scoped configuration with credentials supplied externally through the supported mechanism. Configuration sharing and secret handling are separate responsibilities.

**Paired changed-constraint scene:** A connected MCP server advertises a resource. The host has not discovered or included that resource in the agent’s context. What should the architect verify?

**Answer to the paired scene:** Verify host resource discovery, permissions and explicit inclusion rather than assume connection supplied content. Server availability does not establish host inclusion or model-visible evidence.

**Base choice:** A shared marketing repository uses safe project MCP configuration with secrets provided outside committed files. Inspect the actual host’s tool/resource discovery behavior.

**Changed constraint and recovery:** A developer tests a personal server. Keep its configuration in the appropriate personal/local scope instead of committing credentials to the team project.

**Failure:** The server connects but the expected resource is not in model context. Check listing, host support and explicit inclusion; do not claim automatic availability.

**Nearest alternative:** Connectivity is not proof that every resource was discovered or supplied. Resource behavior depends on host support and invocation.

**Conditional cue:** Connect, discover, include: prove each stage.

**Proof:** Inspect `project_config={server:crm,secret:environment}; trace=[connected,listed,included]` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.4.md#variant-fv-11).

</details>

### FV-12 — recall

A campaign repository has hundreds of templates. You must find the code emitting an incorrect unsubscribe URL and make a small repair. Which sequence fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Find relevant paths and text, read the matching code, then edit the smallest supported region and inspect its diff. Search and read establish evidence for a scoped edit.

**Paired changed-constraint scene:** The requested artifact is a brand-new standalone CSV with an explicit schema; no existing file needs modification. Which operation fits after inspecting the target location?

**Answer to the paired scene:** Write the new artifact at the agreed path and validate its schema. Creating a new artifact is different from patching an existing region.

**Base choice:** An unfamiliar education repository needs a one-function fix. Glob relevant paths, Grep the symbol, Read callers and tests, then Edit the precise existing region.

**Changed constraint and recovery:** A genuinely new standalone artifact has no existing file to patch. Write the new file after verifying its placement and contract.

**Failure:** A broad replacement changes unrelated handlers. Restore the unintended changes and inspect the focused diff and targeted behavior.

**Nearest alternative:** Dumping or rewriting the repository risks losing context and unrelated code. Tool selection follows the task, not a fixed ritual for every edit.

**Conditional cue:** Locate, inspect, change, prove; create only when new.

**Proof:** Inspect `evidence=[paths,symbol_hits,caller_read,test_read]; change={file:handler.py,region:retry_condition}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.5.md#variant-fv-12).

</details>

### FV-13 — recall

Repository conventions must apply to all contributors, while one analyst’s preferred response tone is personal. What instruction placement fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Keep shared conventions in project instructions and personal preferences in the personal scope. Scope should match who owns and needs the instruction.

**Paired changed-constraint scene:** A child directory’s instructions conflict with applicable project policy on retaining evidence. The conflict changes the requested output. What should the agent do?

**Answer to the paired scene:** Identify the applicable instruction files and resolve the conflict according to authority before editing. An identified instruction conflict needs explicit resolution rather than accidental behavior.

**Base choice:** A shared repository convention belongs in project instructions; personal preferences stay in personal configuration. Trace which nested instructions apply to the current path.

**Changed constraint and recovery:** A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file.

**Failure:** Two applicable files disagree on test behavior. Surface and resolve the conflict using the runtime’s documented loading/scope rules.

**Nearest alternative:** More copies increase drift. Instruction files guide model behavior; they do not replace enforced permission checks.

**Conditional cue:** Shared at project; specific at path; resolve conflicts.

**Proof:** Inspect `instructions={shared:CLAUDE.md,package:services/CLAUDE.md,personal:user}; target=services/api.py` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.1.md#variant-fv-13).

</details>

### FV-14 — recall

The team repeatedly produces campaign evidence packets from a supplied brief, source list and output directory. What reusable artifact fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Create a scoped command or skill with documented inputs, dependencies, output contract and explicit missing-input behavior. A repeatable workflow benefits from explicit invocation and failure contracts.

**Paired changed-constraint scene:** A user gives one short task with complete inputs that is unlikely to recur. What should the agent create?

**Answer to the paired scene:** Use the task brief directly without introducing a reusable workflow solely for this one case. A one-off complete brief does not automatically justify maintaining a reusable abstraction.

**Base choice:** A repeated reviewed-release brief becomes a scoped skill with required commit, evidence paths and output expectations. Check discovery and allowed dependencies.

**Changed constraint and recovery:** A single ad hoc explanation is needed. Use a brief rather than creating a reusable asset without repeated need.

**Failure:** The skill is invoked without the reviewed commit. Stop with a missing-input message instead of inventing a build identity.

**Nearest alternative:** A reusable skill is not permission to publish. Invocation and downstream authorization remain separate.

**Conditional cue:** Reuse the workflow; require its inputs; preserve permission.

**Proof:** Inspect `skill_input={reviewed_commit,tests,evidence}; output={changes,limits,next_action}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.2.md#variant-fv-14).

</details>

### FV-15 — recall

Only files in backend/payments require the payment-specific test convention. What configuration is appropriate? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Use a path-scoped rule whose pattern matches the payment files and verify it is actually loaded for the change. Conditional conventions should load for their relevant paths.

**Paired changed-constraint scene:** The same repository has a policy requiring evidence attribution in every generated artifact, regardless of path. What rule scope fits?

**Answer to the paired scene:** Use an applicable broader instruction for the cross-cutting attribution policy. A genuinely cross-cutting requirement needs correspondingly broad applicability.

**Base choice:** Backend and test conventions are scoped to their respective path patterns. Predict applicable rules for a change touching both areas and verify actual loading.

**Changed constraint and recovery:** A security policy genuinely applies across the repository. Move that requirement to an appropriate broader scope.

**Failure:** A test file moved outside the expected glob, so its rule was not loaded. Correct the scope and check a matching and nonmatching path.

**Nearest alternative:** Duplicating every rule into the main prompt can hide mismatches and flood context; path scope must match actual files.

**Conditional cue:** Match the path; verify the rule; broaden only when shared.

**Proof:** Inspect `paths=[services/api.py,tests/test_api.py]; rules={backend:services/**,testing:tests/**}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.3.md#variant-fv-15).

</details>

### FV-16 — recall

A change spans authentication, ingestion and retention behavior; dependencies and acceptance boundaries are still unclear. Which starting mode fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Inspect dependencies and develop a reviewed plan before making the broad change. Uncertainty and cross-file impact justify planning and evidence gathering.

**Paired changed-constraint scene:** A reviewed typo fix touches one documented label, has an exact replacement and no behavior change. Which starting mode fits?

**Answer to the paired scene:** Perform the clear bounded edit directly and verify the rendered label. A small unambiguous low-impact change can be executed and checked directly.

**Base choice:** A cross-service authentication change has unclear callers and migration impact. Inspect evidence, produce a plan and review dependencies before editing.

**Changed constraint and recovery:** The task becomes a precise typo in an isolated documented comment. Direct execution and a focused check are proportionate.

**Failure:** An apparently small edit reveals a shared API dependency. Pause to revise the plan rather than continuing under the old assumption.

**Nearest alternative:** Always planning adds overhead to bounded simple work; always executing can miss uncertain dependencies.

**Conditional cue:** Plan the unknown boundaries; execute the bounded known edit.

**Proof:** Inspect `plan={affected:[client,server,tests],unknown:[migration],acceptance:[old_client_works]}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.4.md#variant-fv-16).

</details>

### FV-17 — recall

An agent has twice returned a campaign report with a broken date parser. The feedback only said improve it. What feedback should be supplied next? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Provide the failing input, observed output, expected result and relevant diagnostic so refinement targets a reproducible defect. Concrete fixtures and diagnostics define measurable refinement.

**Paired changed-constraint scene:** The same precise failing fixture still fails after two different implementations. The team is repeating its initial diagnosis without inspecting new evidence. What should change?

**Answer to the paired scene:** Revisit the failure hypothesis and inspect the implementation or dependency evidence before another change. Repeated failure can signal a wrong hypothesis rather than insufficient repetition.

**Base choice:** A date parser fails on one fixture. Supply actual input, expected result, failing assertion and relevant code; make a targeted change and re-run the fixture plus nearby cases.

**Changed constraint and recovery:** Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign.

**Failure:** The same failure survives two identical retries. Investigate a new cause, such as locale interpretation or preprocessing, instead of repeating the same prompt.

**Nearest alternative:** More iterations do not imply learning. Narrow evidence and hypothesis changes matter more than request length.

**Conditional cue:** Example, expectation, evidence; failed hypothesis must change.

**Proof:** Inspect `feedback={input:03/04,locale:en_GB,expected:2026-04-03,actual:2026-03-04,check:date_locale}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.5.md#variant-fv-17).

</details>

### FV-18 — recall

A nightly repository audit must inspect local files, run tests and emit a machine-readable findings artifact. It must run without a user at the terminal. Which runtime fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Use a configured headless Claude Code job with scoped credentials, exit handling and validated findings extraction. The audit depends on the Code runtime and repository environment.

**Paired changed-constraint scene:** A separate job summarizes 2,000 independent supplied texts, needs no local filesystem or dependent tool loop and tolerates asynchronous completion. Which runtime is eligible for consideration?

**Answer to the paired scene:** Consider Messages Batch for independent supported API requests and recover individual failed or expired items. Independent eligible requests can be processed asynchronously; this is not a completion-time guarantee.

**Base choice:** A scheduled repository-dependent Code review runs headless with available credentials, scoped permissions, project context, exit handling and retained artifacts. Parse its CLI envelope before validating the findings payload.

**Changed constraint and recovery:** The work becomes independent eligible Messages requests with no local iterative state and a tolerant deadline. Consider batch; an urgent dependent tool loop remains a different runtime.

**Failure:** Missing credentials or malformed findings must produce an observable failure or bounded repair, never an empty “passed” report.

**Nearest alternative:** Nonblocking alone does not justify Messages Batch. JSON CLI output alone does not prove the findings schema or source accuracy.

**Conditional cue:** Runtime by dependency; gate by validated evidence.

**Proof:** Inspect `ci_packet={commit,permissions,environment,prompt,exit_code,envelope,findings}; accept=all_required_checks_pass` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.6.md#variant-fv-18).

</details>

### FV-19 — recall

A contract scanner flags any occurrence of fee as an unexpected charge, causing false positives on clauses that expressly prohibit fees. What prompt change best addresses the defect? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Define the prohibited-charge criterion, exclusions, evidence citation and examples of negated versus operative clauses. Explicit operational criteria and exclusions reduce this known classification ambiguity.

**Paired changed-constraint scene:** The policy owner cannot say whether conditional pass-through costs count as prohibited fees. Which next step fits?

**Answer to the paired scene:** Request the missing policy interpretation or label those cases unresolved before classifying them. An unresolved business definition cannot be repaired by confident model wording.

**Base choice:** A legal clause review flags only an explicit unilateral termination right without the fictional required notice. Provide threshold, exclusions and source locator expectations.

**Changed constraint and recovery:** The policy wording is ambiguous about mutual termination. Ask for clarification or label the case uncertain instead of treating every termination mention as a violation.

**Failure:** False positives cluster around historical examples. Add the exclusion and test borderline cases against actual text.

**Nearest alternative:** “Be careful” does not operationalize the criterion. A longer prompt without measurable boundaries can preserve the same errors.

**Conditional cue:** Name trigger, exclusion and evidence before flagging.

**Proof:** Inspect `finding_rule={trigger:unilateral_right,required:notice,evidence:clause_locator,exclude:historical_example}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.1.md#variant-fv-19).

</details>

### FV-20 — recall

A campaign classifier sees regular examples but fails on disclaimers and conditional promotions. Which few-shot set best addresses the observed distribution? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Add representative contrastive examples for the failing edge cases with the intended labels and evidence. Representative edge cases teach the distinction the current set omits.

**Paired changed-constraint scene:** A new market introduces a promotion structure absent from the original examples; held-out results show systematic mistakes. What should the team do?

**Answer to the paired scene:** Revise or add examples for the changed distribution and evaluate on a separate held-out set. Distribution change needs evidence-driven example revision and independent measurement.

**Base choice:** A finance extraction prompt includes ordinary invoices, absent tax IDs and source conflicts, with explanations of allowed nulls and unresolved values.

**Changed constraint and recovery:** A new document population uses credit notes and negative amounts. Revise the example distribution and validate on unseen cases.

**Failure:** All examples are clean positive invoices; the model invents rare fields. Add realistic counterexamples rather than simply adding more clean examples.

**Nearest alternative:** Few-shot consistency is not a factual guarantee. Examples should represent the relevant error modes, not leak held-out answers.

**Conditional cue:** Examples teach boundaries; holdouts test transfer.

**Proof:** Inspect `examples=[ordinary,missing_field,conflict,credit_note]; holdout=unseen_edge_cases` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.2.md#variant-fv-20).

</details>

### FV-21 — recall

A source invoice omits a purchase-order number; the approved schema permits null for that field. What should the extractor return? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Return null for the unsupported field and preserve the source locator. The approved nullable contract supports absence without invention.

**Paired changed-constraint scene:** Another invoice explicitly states PO-782, but the schema-valid output says PO-728. What validation fixes this defect?

**Answer to the paired scene:** Compare the field against source evidence and correct the non-null value through semantic validation. The wrong value has valid shape but conflicts with the source.

**Base choice:** Use supported strict schema enforcement for an extraction tool, then independently validate source evidence and arithmetic. Tool selection, structural conformance and semantic validity are separate checks.

**Changed constraint and recovery:** A field truly absent from the source may be null only when the declared contract allows it. A wrong non-null amount does not call for a nullable-only repair.

**Failure:** The JSON is well typed but says 900 where the source says 90. Reject the semantic mismatch and return the exact failed check.

**Nearest alternative:** Forcing a tool call does not prove schema adherence unless the applicable mechanism enforces it; even conforming output can be wrong.

**Conditional cue:** Call, shape, truth: three proofs, not one.

**Proof:** Inspect `candidate={amount:900,currency:USD}; source={amount:90}; shape=pass; source_match=fail` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.3.md#variant-fv-21).

</details>

### FV-22 — recall

An extracted invoice has line totals summing to 980 but reports 890; the source clearly shows 980. What recovery fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Send the exact failed arithmetic and source checks with the previous output for a bounded targeted correction. A clear check payload targets the evidenced error and bounds recovery.

**Paired changed-constraint scene:** After the allowed correction attempts, two source pages still disagree about the invoice total. What should happen?

**Answer to the paired scene:** Keep the discrepancy unresolved and escalate with source evidence and attempt history. Persistent source conflict cannot be resolved by inventing agreement.

**Base choice:** An invoice candidate’s subtotal plus tax differs from total. Return the precise values, source locators and failed arithmetic check for a bounded correction.

**Changed constraint and recovery:** The source itself contains contradictory totals. Preserve both values and route review instead of asking Claude to manufacture reconciliation.

**Failure:** The retry budget is exhausted. Escalate with source, previous outputs, failed checks and unresolved discrepancy.

**Nearest alternative:** Retrying the whole document without diagnostic feedback can repeat the error or mutate correct fields.

**Conditional cue:** Repair the named failure; stop when evidence cannot resolve it.

**Proof:** Inspect `failed_check={subtotal:80,tax:8,total:100,expected:88}; retry_budget=2; status=unresolved` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.4.md#variant-fv-22).

</details>

### FV-23 — recall

An overnight job classifies independent supplied campaign snippets with no local runtime requirement; each can finish asynchronously. Which design fits? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Use eligible independent batch requests with stable item IDs and per-item result reconciliation. Independence and asynchronous tolerance make batch a candidate.

**Paired changed-constraint scene:** A launch approval now requires one result before constructing the next prompt, with a five-minute deadline and human clarification. What design fits?

**Answer to the paired scene:** Use an appropriate interactive or synchronous dependent workflow with deadline and escalation handling. Dependent, time-sensitive human interaction changes the runtime requirements.

**Base choice:** Independent eligible document requests tolerate delayed completion and have per-item recovery. Messages Batch is a candidate; retain custom IDs and item states.

**Changed constraint and recovery:** A result is needed before the next dependent local tool step or a tight user deadline. Use the appropriate immediate/interactive runtime instead.

**Failure:** Some items expire or fail. Recover those items with their recorded inputs; do not treat a submission as completed work.

**Nearest alternative:** A 24-hour processing window is not a guaranteed finish time. Batch does not substitute for a local Code agent loop with filesystem state.

**Conditional cue:** Independent plus tolerant plus recoverable; otherwise another lane.

**Proof:** Inspect `items={i1:succeeded,i2:expired,i3:errored}; recovery=[i2,i3]; deadline_policy=explicit` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.5.md#variant-fv-23).

</details>

### FV-24 — recall

A consequential contract finding needs review against the source. The producer and reviewer currently share only the producer’s conclusion. What architecture best improves review? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Give an independent reviewer the source, producer artifact and explicit criteria; preserve and resolve disagreements. Independent source-based critique can identify producer omissions.

**Paired changed-constraint scene:** A low-risk internal formatting task has an exact deterministic validator; no substantive conclusion is produced. What review approach is proportionate?

**Answer to the paired scene:** Use the deterministic validator and bounded human or automated spot checks appropriate to the low risk. Additional model passes need to justify their cost and failure exposure for this bounded task.

**Base choice:** A producer proposes extracted claims; a separate critic checks source locators, omissions and contradictions under explicit criteria. Resolve disagreement by evidence.

**Changed constraint and recovery:** A simple low-risk formatting task has deterministic validation. Extra model passes may not justify their cost.

**Failure:** Both instances share a misleading summary and agree. Give the critic original sources or a different check; agreement alone is not validation.

**Nearest alternative:** Repeated identical prompts can amplify the same blind spot. Independence needs evidence and criteria, not just another instance.

**Conditional cue:** Separate the reviewer’s evidence; resolve with the source.

**Proof:** Inspect `producer={claims,sources}; critic={criteria,original_sources,failed_checks}; dispute={claim,source,verdict}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.6.md#variant-fv-24).

</details>

### FV-25 — recall

A long investigation is approaching its context limit. A rare jurisdiction exception determines the final action. What should the compact state preserve? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Preserve the exception, decisions, unresolved issues and precise source pointers in the compact state. Critical constraints and pointers must survive compaction to support later decisions.

**Paired changed-constraint scene:** After compaction, a referenced policy document is revised and the summary no longer establishes the applicable exception. What should happen?

**Answer to the paired scene:** Reacquire the revised source and revalidate the affected decision instead of reconstructing missing details. A changed source requires fresh evidence even when conversation state persists.

**Base choice:** A long marketing investigation stores the current question, accepted constraints, unresolved issues, source pointers and next bounded action before compaction.

**Changed constraint and recovery:** Source consent or policy changes. Refresh the relevant evidence and revise the stored decision state.

**Failure:** A summary drops the “do not contact” exception. Restore it from the source before proceeding; never infer that omitted means revoked.

**Nearest alternative:** Keeping every transcript token can overwhelm context. A compact record must retain decisive exceptions and reacquisition paths.

**Conditional cue:** Keep decisions and exceptions; reacquire the detail.

**Proof:** Inspect `state={question,constraints:[no_contact],sources:[CRM42],unresolved:[consent_age],next:verify}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.1.md#variant-fv-25).

</details>

### FV-26 — recall

A customer explicitly asks to speak to a human about disputed campaign billing. Policy permits that escalation. What should the assistant do? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Escalate promptly with the issue, verified identifiers, evidence and unresolved status. The explicit request is a defined escalation trigger.

**Paired changed-constraint scene:** A customer says the report is confusing but does not request a human; policy calls for clarification of the disputed metric first. What should happen?

**Answer to the paired scene:** Ask a targeted clarification under the support policy while keeping escalation available. Ambiguity without the trigger should follow the applicable clarification route.

**Base choice:** A customer explicitly asks for a human. Route promptly with verified identity status, issues, evidence, attempted and blocked actions, and next owner.

**Changed constraint and recovery:** The customer says “this is frustrating” without requesting a person. Clarify or continue according to the fictional support policy; do not invent an escalation mandate.

**Failure:** The handoff says credit issued, but only a proposal exists. Correct status and include the operation ledger before transferring.

**Nearest alternative:** A transcript dump does not ensure an actionable handoff; a vague complaint is not identical to an explicit human request.

**Conditional cue:** Hear the trigger; hand over facts, status and next action.

**Proof:** Inspect `handoff={identity_status,issues,confirmed,proposed,blocked,reason,next_owner}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.2.md#variant-fv-26).

</details>

### FV-27 — recall

A coordinator receives valid findings from two specialists and a retryable source timeout from a third. The missing source is mandatory for the final conclusion. What should it do? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Preserve successful findings, report the missing mandatory evidence and dispatch targeted recovery before a final supported conclusion. Targeted recovery retains valid work while respecting the mandatory evidence requirement.

**Paired changed-constraint scene:** A different brief explicitly permits a partial overview; an optional source is unavailable and cannot be recovered now. Which output fits?

**Answer to the paired scene:** Return the permitted partial overview with attributed findings and an explicit unavailable-source limitation. Explicit permission for partial coverage changes whether a bounded output is acceptable.

**Base choice:** Specialists return findings and structured failures to the coordinator. Preserve successful evidence and decide which missing dimensions block the final claim.

**Changed constraint and recovery:** The unavailable source is explicitly optional. Publish a bounded partial answer with the omission and limitations visible.

**Failure:** A mandatory permissions source fails. Target that recovery or stop the affected conclusion; do not replace its facts with another specialist’s guess.

**Nearest alternative:** Discarding all successes wastes evidence; silently dropping a failed mandatory dimension fabricates completeness.

**Conditional cue:** Keep the successes; name the gap; block dependent claims.

**Proof:** Inspect `result={dimension:permissions,status:failed,reason:access_denied,retryable:false}; aggregate=partial` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.3.md#variant-fv-27).

</details>

### FV-28 — recall

A defect appears in one generated campaign URL among a large codebase. What exploration strategy fits before editing? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Search narrowly, read relevant files and keep a compact evidence ledger of paths, dependencies and findings. Targeted evidence reduces context noise and supports a justified local diagnosis.

**Paired changed-constraint scene:** A targeted read shows that the URL builder depends on a shared encoding helper used by three services. What should exploration do next?

**Answer to the paired scene:** Expand into the demonstrated dependency chain and inspect affected callers before choosing the repair. Newly evidenced cross-cutting dependencies require appropriately expanded investigation.

**Base choice:** A large codebase bug starts with targeted symbol search, relevant caller reads and a file/dependency ledger. Expand only the evidence path needed for the defect.

**Changed constraint and recovery:** The failure crosses the API boundary. Add the adjacent client/server dependencies and contract tests rather than preserving an artificially narrow scope.

**Failure:** Compaction loses a function’s exception condition. Re-read the actual file at the current commit before editing.

**Nearest alternative:** A guessed summary cannot replace current code evidence. Reading the whole repository also makes the decisive detail harder to retain.

**Conditional cue:** Map the path; read the dependency; refresh before edit.

**Proof:** Inspect `ledger={commit,files:[handler,caller],symbols:[retry],unresolved:[ownership],next:test_contract}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.4.md#variant-fv-28).

</details>

### FV-29 — recall

A routing model is 98% accurate overall but only 65% accurate on a rare high-loss claim category. What should review routing use? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Use stratified error and loss evidence to route the high-risk category rather than rely on the overall average. Aggregate accuracy can hide consequential subgroup failure.

**Paired changed-constraint scene:** The routing team has calibrated scores but reviewer demand exceeds daily capacity; a published policy forbids silently dropping flagged claims. What is required?

**Answer to the paired scene:** Define and test a capacity and overflow policy with observable escalation for unresolved review demand. A review design must specify what happens when its required human queue exceeds capacity.

**Base choice:** A finance extractor has high overall accuracy but weaker rare-currency performance. Evaluate severity-weighted slices on independent holdout and calibrate review thresholds with actual human capacity.

**Changed constraint and recovery:** A review queue exceeds available capacity. Apply a declared overflow policy or reduce scope; do not silently accept low-confidence items.

**Failure:** Distribution drift breaks calibration. Recalibrate on suitable data and evaluate on a separate holdout; do not tune against the final test set.

**Nearest alternative:** The average can hide dangerous categories; confidence scores alone are not calibrated correctness probabilities.

**Conditional cue:** Average, slice, severity, capacity: check all four.

**Proof:** Inspect `metrics={overall:0.98,rare_currency:0.70}; capacity=20; queued=35; overflow=hold` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.5.md#variant-fv-29).

</details>

### FV-30 — recall

Two systems disagree about a contract’s termination date and have different update timestamps. What should the synthesis preserve? State the mechanism, nearest alternative, exception and proof.

<details>
<summary>Reveal conditional answer and repair</summary>


**Answer to the front:** Keep field-level source locators, timestamps and the explicit discrepancy without inventing a merged date. Attribution and explicit uncertainty preserve the actual evidence state.

**Paired changed-constraint scene:** A supported federation provides one query interface. The coordinator receives conflicting termination dates with source locators removed. What return contract must the research subagent provide before synthesis?

**Answer to the paired scene:** Return a structured claim-to-source mapping with document locators, relevant evidence and timestamps, retaining the conflict for the coordinator. A unified query interface does not replace structured claim-source mappings. Downstream synthesis needs attributable claims and explicit conflict, not inferred source identity.

**Base choice:** Separate finance and CRM interfaces return revenue and customer records with timestamps and field-level provenance. Join only under a declared identifier rule.

**Changed constraint and recovery:** The host offers supported federation. It may simplify retrieval, but still retain origin, time and conflict checks.

**Failure:** CRM says customer active while finance reports suspended at a different date. Preserve both assertions and their scope; ask for policy or current authoritative evidence.

**Nearest alternative:** A joined table can erase provenance and make mismatched-age sources look consistent. Federation does not establish truth by itself.

**Conditional cue:** Join identifiers; retain origins; expose disagreement.

**Proof:** Inspect `row={customer_id:C7,revenue:{value:120,source:FIN9,as_of:d1},status:{value:active,source:CRM4,as_of:d2}}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.6.md#variant-fv-30).

</details>



<span data-assessment-exposure="cct-fv-01-base-v1,cct-fv-01-retry-v1,cct-fv-02-base-v1,cct-fv-02-retry-v1,cct-fv-03-base-v1,cct-fv-03-retry-v1,cct-fv-04-base-v1,cct-fv-04-retry-v1,cct-fv-05-base-v1,cct-fv-05-retry-v1,cct-fv-06-base-v1,cct-fv-06-retry-v1,cct-fv-07-base-v1,cct-fv-07-retry-v1,cct-fv-08-base-v1,cct-fv-08-retry-v1,cct-fv-09-base-v1,cct-fv-09-retry-v1,cct-fv-10-base-v1,cct-fv-10-retry-v1,cct-fv-11-base-v1,cct-fv-11-retry-v1,cct-fv-12-base-v1,cct-fv-12-retry-v1,cct-fv-13-base-v1,cct-fv-13-retry-v1,cct-fv-14-base-v1,cct-fv-14-retry-v1,cct-fv-15-base-v1,cct-fv-15-retry-v1,cct-fv-16-base-v1,cct-fv-16-retry-v1,cct-fv-17-base-v1,cct-fv-17-retry-v1,cct-fv-18-base-v1,cct-fv-18-retry-v1,cct-fv-19-base-v1,cct-fv-19-retry-v1,cct-fv-20-base-v1,cct-fv-20-retry-v1,cct-fv-21-base-v1,cct-fv-21-retry-v1,cct-fv-22-base-v1,cct-fv-22-retry-v1,cct-fv-23-base-v1,cct-fv-23-retry-v1,cct-fv-24-base-v1,cct-fv-24-retry-v1,cct-fv-25-base-v1,cct-fv-25-retry-v1,cct-fv-26-base-v1,cct-fv-26-retry-v1,cct-fv-27-base-v1,cct-fv-27-retry-v1,cct-fv-28-base-v1,cct-fv-28-retry-v1,cct-fv-29-base-v1,cct-fv-29-retry-v1,cct-fv-30-base-v1,cct-fv-30-retry-v1"></span>