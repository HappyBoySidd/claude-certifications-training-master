# CCAR-F SIM-06 — Scenario 5: Claude Code for Continuous Integration

<!-- layered-scenario-migration -->
## After your independent attempt: replay the failure layers

Complete the existing decision set and record your answers before opening this coached replay. Reading requires no credentials or execution. The following original decision variants supplement the existing simulation; they do not change its question IDs, answer key or practice scoring. For timed rehearsal keep this entire section closed until review.

<details><summary>Open coached replay after recording the independent decisions</summary>

### Stage 1 — The interactive review hangs in CI

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

**Objective connections:** [3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.6.md), [4.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.6.md).

### Stage 2 — A review flags everything that looks unusual

A marketing compliance reviewer flags any mention of price as a violation. The business actually forbids unsupported discount promises, not ordinary published pricing. The prompt says only “find risky copy.”

**Original exam-style practice — choose ONE.** Which prompt revision most directly improves precision without suppressing genuine violations?

A. Ask for fewer findings regardless of evidence.

B. Specify the violation criteria, require supporting text, and give contrasting compliant/noncompliant examples.

C. Tell the model to be absolutely certain without defining the rule.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The model needs to know what counts as a problem. Include a compliant published price and an unsupported discount promise, with the reason for each. A hides real problems; C changes tone rather than the decision rule.

**Follow the changed path:**

```text
copy + explicit criteria + examples → evidence-backed finding → reviewer checks rule fit
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Replay both examples and a new wording. Measure false positives and missed violations separately; a shorter report is not automatically a better report.

</details>

**Changed-constraint decision — choose ONE before revealing:** New documents put payment terms in footnotes. A: add representative input/output examples for varied layouts; B: add only more emphatic wording.

<details><summary>Reveal changed-constraint reasoning</summary>

A. Examples teach the mapping across layouts. Keep a genuine absence example so the system does not invent a field just to satisfy the demonstration.

</details>

**Objective connections:** [4.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.1.md), [4.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.2.md).

</details>

<!-- /layered-scenario-migration -->


**Picture the application:** A team wants automated feedback when a pull request changes its application. The pipeline receives code changes and review criteria; it should return useful findings and test suggestions without burying developers in false alarms. This simulation asks you to design the review workflow behind those results.

**Build the application picture first:** [AS 06 ci review](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-06-ci-review.md) · [AS 07 work queue](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-07-work-queue.md)

**Primary domains:** 3 Claude Code, 4 Prompting and Structured Output · **Decisions:** 10 ·
**Time:** 20 min for the decisions, plus about 15 for the twists and about 10 for the play-by-play

## Scene (paraphrased from the official exam guide v1.0, Scenario 5, Tier 1)

You're adding Claude Code to your CI/CD pipeline. It runs automated code reviews, generates test
cases and comments on pull requests. You need to design prompts that give **actionable feedback and
keep false positives low**.

**On your own:** write down your answer to each decision, then open the coach key. For the reasoning behind each answer, open Play by play at the end.

**With a Claude chat:** paste the scene and the decision list, ask Claude to quiz you one decision at a time, and don't paste the coach key.

## The decisions (answer these before you open the key)

1. Alongside Claude Code, the team runs a small PR bot of its own built on the Claude API. Its
   reviews end mid-thought ("Let me open `utils.py` next…"), because the script treats any
   response that contains text as the final answer. How should the bot decide it's finished?
2. Findings must be posted as inline PR comments. How do you get output the pipeline can use?
3. Reviews should follow the team's criteria and test fixtures. Answering the way the exam guide
   describes it, where do those go?
4. Developers ignore the reviews because of false positives. What changes in the prompt?
5. Most of the false positives come from the "comment accuracy" category, and developers have
   started ignoring the whole review, including the accurate findings. What do you do with that
   category?
6. The findings already come back as valid JSON, but what goes in each one varies from run to
   run: some name the line and suggest a fix, some only describe the problem, and severity is
   judged differently each time. How do you make them consistent?
7. The same session that wrote the code is also reviewing it. What's the problem, and the fix?
8. Before writing tests for the 900-file `payments/` package, the job's context fills with search
   output, and the generated tests call classes that don't exist. How do you restructure it?
9. Re-running the review after a new commit duplicates earlier comments. What do you change?
10. A weekly job re-documents 1,200 public functions through the Message Batches API. About 40
    requests fail each week, and the script resubmits the whole batch. What should it do?

---

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | The team's own API-based PR bot stops at "Let me open `utils.py` next…" because any text counts as finished | **Loop on `stop_reason`:** on `"tool_use"`, run the tool and send back a `tool_result`; stop only on `"end_turn"`. Keep an iteration cap as a safety net, not the stop signal. | Stop when the text contains "Done" or "Summary"; set a 5-turn cap as the stop rule; tell it in the prompt to "finish the whole review in one reply" | D1 1.1 Agentic loops | [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| 2 | Findings must be posted as inline PR comments | **`--output-format json` with `--json-schema`** | Parse the prose with a regex; ask for "JSON only" in the prompt; `--output-format json` alone, with no `--json-schema`, which wraps the reply in JSON but doesn't fix the shape of the findings | D3 3.6 CI/CD integration | [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 3 | Reviews should follow the team's criteria and fixtures | **Document them in the project CLAUDE.md** (exam answer). Today's docs say to add `--bare` in CI, which skips `CLAUDE.md`; also accept "pass the standards in explicitly, for example with `--append-system-prompt-file`" as right for today's product; on the exam, pick the project CLAUDE.md. See [exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today) | Paste them into every CI prompt by hand; put them in each developer's `~/.claude/CLAUDE.md`, which CI never sees; a longer CI prompt | D3 3.6 CI/CD integration; D3 3.1 CLAUDE.md hierarchy | [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md), [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 4 | Developers ignore reviews because of false positives | **Explicit categories to report and to skip**, plus severity examples | "Be conservative"; "only report high-confidence findings"; a bigger model | D4 4.1 Explicit criteria | [Lesson 4, section 4.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 5 | The "comment accuracy" category is mostly noise | **Turn that category off temporarily** while you fix its prompt | Keep it on and hope; raise the model tier; ask it to "be careful" with comment findings | D4 4.1 Explicit criteria | [Lesson 4, section 4.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 6 | What goes in each finding varies from run to run | **2–4 few-shot examples** in the target format (location, issue, severity, fix) | More detailed prose instructions; one example of a finding with every field filled, so every ambiguous case gets forced into that one shape; a regex post-processor that reformats whatever comes back | D4 4.2 Few-shot prompting | [Lesson 4, section 4.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |
| 7 | The same session that wrote the code reviews it | An **independent review instance** without the generator's context | "Review your work critically"; extended thinking in the same session; run the same session's review twice | D4 4.6 Multi-instance and multi-pass review; D3 3.6 CI/CD integration | [Lesson 4, section 4.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md), [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 8 | Discovery output fills the context before test writing in a 900-file package, and tests call classes that don't exist | **Delegate the discovery to a subagent** (for example the Explore subagent) that searches the package and **returns a short summary** of the real classes, entry points and fixtures; the main session writes tests from that summary. A scratchpad file of findings helps too. | A bigger context window; a longer prompt listing every file in the package; raise the turn limit so it can keep searching | D5 5.4 Large-codebase exploration | [Lesson 5, section 5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| 9 | Re-running after a new commit duplicates comments | **Include the earlier findings; report only new or unaddressed issues** | Delete the old comments and repost everything; tell it to "avoid repeating itself" without giving it the earlier findings; review only the first commit of each PR | D3 3.6 CI/CD integration | [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) |
| 10 | About 40 of 1,200 batch requests fail each week, and the script resubmits all 1,200 | **Match results by `custom_id` and resubmit only the failed items**, adjusted if needed (for example split ones that were too long). Batches suit this job: nobody is waiting on it. | Keep resubmitting the whole batch; move the job to synchronous calls to avoid failures, at double the cost; match results by their position in the output, which isn't guaranteed to follow input order | D4 4.5 Batch processing | [Lesson 4, section 4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) |

**Scoring:** 8 or more is a pass. Decisions 4 and 7 are the heart of the scenario: *explicit
criteria beat "be conservative"*, and *the writer shouldn't grade its own work*.

Sources: CCAR-F exam guide v1.0 (Anthropic),
Scenario 5 and task statements 1.1, 3.1, 3.6, 4.1, 4.2, 4.5, 4.6, 5.4 (Tier 1); Claude Code
[CLI reference](https://code.claude.com/docs/en/cli-reference), Claude Code
[headless docs](https://code.claude.com/docs/en/headless) (`--bare`, `structured_output`; checked 2026-10-12)
and Message Batches docs on
platform.claude.com (Tier 1). Taught in lessons
[L01](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md),
[L03](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md),
[L04](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) and
[L05](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).

</details>

## Round 2: twists

Same scenario, one thing changed. Decide first, then open the answer.

### Twist 1: you can't tell which findings get dismissed

**What changed:** developers dismiss a lot of findings, but the team can't tell which kinds of
issue are the noisy ones, so it doesn't know which prompt rules to fix.

**Question:** what do you add to the review output?

<details><summary><b>Answer and why</b></summary>

**Add a `detected_pattern` field to each structured finding** (the kind of code pattern that
triggered it). Then you can count which patterns developers dismiss most and fix the criteria for
those.

**Why the others lose:** asking the model to "only report what it's sure about" doesn't improve
precision. Exam guide wording (task statement 4.1): "How general instructions like "be
conservative" or "only report high-confidence findings" fail to improve precision compared to
specific categorical criteria". Reading dismissed comments by hand doesn't scale. Turning off
every category that has any dismissals, useful ones included, throws away findings developers do
act on. (Turning off one known-noisy category for a while, as in decision 5, is different.)

**Tests:** Domain 4, task statement 4.4 (validation and retry loops); also 4.1 (explicit criteria).

**Lesson:** [Lesson 4, section 4.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#44-validate-retry-feed-back) · [Deep practice, Domain 4](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/04-prompt-engineering-and-structured-output.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 4.4 (Tier 1).

</details>

### Twist 2: a tool loop someone wants to batch

**What changed:** a nightly job asks Claude to fix flaky tests. For each test, Claude calls your
`run_test` tool, looks at the result, changes the code and calls `run_test` again. To cut cost,
someone wants to move the whole job to the Message Batches API.

**Question:** does that work, and what do you do?

<details><summary><b>Answer and why</b></summary>

**Not as built. Keep the fix-and-retest loop on regular API calls**, where your code runs
`run_test` and sends each result back. Batches suit single requests that need no tool results
partway through. Exam guide wording: "The batch API does not support multi-turn tool calling
within a single request (cannot execute tools mid-request and return results)". The guide also
lists "50% cost savings, up to 24-hour processing window", which is why it's tempting. Batches do support tools, including server tools (tools Anthropic runs for you, such as web search); the blocker here is the client-side `run_test` loop (Anthropic docs, Message Batches, Tier 1, checked 2026-10-12).

**Why the others lose:** moving it to batches as it is fails, because nothing can run `run_test`
inside a batch request and hand the result back. Sending each round as a new batch with the last
result attached works on paper, but every round can take up to 24 hours, so one test could take
days. Using `custom_id` to pass tool results back mixes things up: `custom_id` only matches each
request to its result.

**Tests:** Domain 4, task statement 4.5 (batch processing).

**Lesson:** [Lesson 4, section 4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#45-batch-processing) · [Deep practice, Domain 4](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/04-prompt-engineering-and-structured-output.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 4.5 (Tier 1); Message Batches docs on platform.claude.com (Tier 1; check the current limits).

</details>

### Twist 3: generated tests repeat tests that already exist

**What changed:** the job that writes test cases keeps proposing tests the repo already has.

**Question:** what do you give Claude so it stops?

<details><summary><b>Answer and why</b></summary>

**Put the existing test files for that code in its context**, so it can see what's already
covered and suggest only new cases.

**Why the others lose:** "don't write duplicate tests" in the prompt asks it to avoid something it
can't see. Removing duplicates afterwards with string matching misses tests that are worded
differently and still pays for writing them.

**Tests:** Domain 3, task statement 3.6 (CI/CD integration).

**Lesson:** [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd) · [Deep practice, Domain 3](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/03-claude-code-configuration-and-workflows.md)

**Source:** CCAR-F exam guide v1.0 (Anthropic), task statement 3.6 (Tier 1).

</details>

<details><summary><b>Play by play</b>: try the decisions first, then open this</summary>

All exam wording below is from the CCAR-F exam guide v1.0 (Tier 1).

**Decision 1: the PR bot stops mid-thought**

- **What's going on:** the bot hangs up while Claude is still halfway through the job.
- **Under the hood:** each reply has a `stop_reason` (why the model stopped). `"tool_use"` means it wants a tool run: your code runs it and sends back a `tool_result` (the tool's output). `"end_turn"` means it's done. Text can appear in either kind of reply (unless a tool is forced).
- **How to make the call:** if `stop_reason` is `"tool_use"`, run the tool, add the result and call again; if it's `"end_turn"`, stop. Keep an iteration cap only as a safety net. Exam wording (task statement 1.1): "Implementing agentic loop control flow that continues when stop_reason is "tool_use" and terminates when stop_reason is "end_turn"".
- **Why the tempting answers are wrong:**
  - **Stop on "Done" or "Summary":** guesses from words that may come early or never.
  - **5-turn cap as the rule:** cuts long reviews off; a cap is a safety net.
  - **"Finish in one reply" prompt:** a request; the loop still ignores `stop_reason`.
- **Go deeper:** [Lesson 1, section 1.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md#11-the-agentic-loop)

**Decision 2: findings must become inline PR comments**

- **What's going on:** the pipeline needs data it can read, not an essay.
- **Under the hood:** `claude -p` runs once with no chat and prints the reply. `--output-format json` wraps that reply in JSON. `--json-schema` (the shape the answer must match) makes the findings themselves follow your fields, such as file, line and issue. Findings arrive in the JSON's `structured_output` field. Treat a missing or malformed envelope (no `structured_output`, or `is_error` true; Agent SDK reference, result message, https://code.claude.com/docs/en/agent-sdk/typescript, Tier 1, checked 2026-10-13) as a failed run, never as "no findings"; only a valid envelope with an empty findings list counts as a clean pass.
- **How to make the call:** if a program reads the output, use `--output-format json` and pass the finding fields in `--json-schema`; if only a person reads it, plain text is fine. Exam wording (task statement 3.6): "Using --output-format json with --json-schema to produce machine-parseable structured findings for automated posting as inline PR comments".
- **Why the tempting answers are wrong:**
  - **Regex over the prose:** breaks when the wording shifts.
  - **"JSON only" in the prompt:** a request; nothing enforces it.
  - **`--output-format json` alone:** a JSON wrapper; the findings' shape isn't fixed.
- **Go deeper:** [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd)

**Decision 3: where the team's criteria and fixtures go**

- **What's going on:** the rules live where CI can't see them.
- **Under the hood:** Claude Code reads CLAUDE.md files (instruction files it loads at start). The project one is committed in the repo, so every clone and every CI run gets it. `~/.claude/CLAUDE.md` sits on one person's machine only.
- **How to make the call:** if a rule should apply to the whole team and to CI, put it in the project CLAUDE.md in the repo; if it's one person's preference, user level is fine. Exam wording (task statement 3.6): "CLAUDE.md as the mechanism for providing project context (testing standards, fixture conventions, review criteria) to CI-invoked Claude Code". Today's docs say add `--bare` in CI, which skips `CLAUDE.md`; on the exam, pick `CLAUDE.md` ([exam answer vs today](../../02-Lessons/02-CCAR-F-Architect-Foundations/deep-practice/conditions-and-errors.md#exam-answer-vs-today)).
- **Why the tempting answers are wrong:**
  - **Paste into every prompt:** by hand, and copies drift apart.
  - **Each developer's `~/.claude/CLAUDE.md`:** CI never sees it.
  - **A longer CI prompt:** lives in one job only.
- **Go deeper:** [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd), [Lesson 3, section 3.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#31-the-claudemd-hierarchy)

**Decision 4: developers ignore reviews full of false alarms**

- **What's going on:** too many false alarms, so people stop reading any of them.
- **Under the hood:** a vague word like "conservative" gives the model no line to apply; it can't know where your line sits. Named categories, plus an example finding at each severity, give it a line it can follow.
- **How to make the call:** if the prompt says how sure to be but not what to report, replace that with lists: report (bugs, security), skip (minor style, local patterns), plus a code example per severity. If the prompt already lists them, look at examples next (Decision 6). Exam wording (task statement 4.1): "Writing specific review criteria that define which issues to report (bugs, security) versus skip (minor style, local patterns) rather than relying on confidence-based filtering".
- **Why the tempting answers are wrong:**
  - **"Be conservative":** too vague to raise precision.
  - **"High-confidence findings only":** confidence filtering, not criteria.
  - **A bigger model:** same vague rules, same noise.
- **Go deeper:** [Lesson 4, section 4.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#41-explicit-criteria-reduce-false-positives)

**Decision 5: one category is mostly noise**

- **What's going on:** one noisy category makes people ignore the useful ones too.
- **Under the hood:** developers judge the whole bot, not each category. False alarms in one category drag down trust in the accurate ones. Switching that one off stops the damage while you rewrite its rule.
- **How to make the call:** if one category makes most of the false alarms, turn it off for now, rewrite its criteria (for example "flag a comment only when it contradicts the code"), then bring it back; if noise is spread everywhere, fix the criteria overall. Exam wording (task statement 4.1): "Temporarily disabling high false-positive categories to restore developer trust while improving prompts for those categories".
- **Why the tempting answers are wrong:**
  - **Keep it on and hope:** trust keeps falling.
  - **A higher model tier:** vague criteria stay vague.
  - **"Be careful" with comments:** a general instruction, no criterion.
- **Go deeper:** [Lesson 4, section 4.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#41-explicit-criteria-reduce-false-positives)

**Decision 6: the output format changes from run to run**

- **What's going on:** same job, a different-looking answer every time.
- **Under the hood:** the model copies the pattern in examples more reliably than it follows a description. A few examples, including tricky cases, show both the shape and how to handle the unclear ones.
- **How to make the call:** if detailed instructions still give mixed formats, add 2–4 examples in the exact target format, covering different kinds of finding; if the format is already steady, don't. Exam wording (task statement 4.2): "Including few-shot examples that demonstrate specific desired output format (location, issue, severity, suggested fix) to achieve consistency".
- **Why the tempting answers are wrong:**
  - **More detailed prose:** instructions already gave mixed results.
  - **One fully filled example:** forces every case into one shape.
  - **Regex reformatter:** patches afterwards and guesses on odd cases.
- **Go deeper:** [Lesson 4, section 4.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#42-few-shot-examples)

**Decision 7: the session that wrote the code reviews it**

- **What's going on:** the author is grading their own homework.
- **Under the hood:** the writing session still holds its reasoning for every choice, so it tends to agree with itself. An independent instance (a separate Claude run with fresh context) sees only the code.
- **How to make the call:** if the reviewer can see the reasoning that produced the code, start a separate review instance without it; if it already starts fresh, keep it. Exam wording (task statement 4.6): "Independent review instances (without prior reasoning context) are more effective at catching subtle issues than self-review instructions or extended thinking".
- **Why the tempting answers are wrong:**
  - **"Review your work critically":** same context, same blind spots.
  - **Extended thinking (more reasoning before answering):** more thought, same bias.
  - **Review twice in that session:** repeats the bias.
- **Go deeper:** [Lesson 4, section 4.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#46-multi-instance-and-multi-pass-review), [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd)

**Decision 8: search output fills the context, and tests call classes that don't exist**

- **What's going on:** the notes pile up until the real facts get pushed out.
- **Under the hood:** every search result stays in context. As it fills, the model loses the specific classes it found and falls back on "typical patterns", so it invents some. A subagent explores in its own context and returns only a summary.
- **How to make the call:** if exploration output is crowding out the work, hand exploration to a subagent that returns a short list of real classes, entry points and fixtures, then write tests from that. If the context is still clear, keep exploring in the main session. A scratchpad file of findings helps too. Exam wording (task statement 5.4): "Subagent delegation for isolating verbose exploration output while the main agent coordinates high-level understanding".
- **Why the tempting answers are wrong:**
  - **Bigger context window:** more room to fill; the drift stays.
  - **List every file:** adds bulk, not understanding.
  - **Higher turn limit:** more searching, more clutter.
- **Go deeper:** [Lesson 5, section 5.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md#54-exploring-a-large-codebase)

**Decision 9: a re-run repeats earlier comments**

- **What's going on:** each review forgets what it said last time.
- **Under the hood:** each CI run of `claude -p` starts a new session. It knows nothing about earlier comments unless your job puts them in its input.
- **How to make the call:** if a review re-runs on a PR that already has findings, pass those findings in and ask for only new or still-unaddressed issues; on a first review there's nothing to pass. Exam wording (task statement 3.6): "Including prior review findings in context when re-running reviews after new commits, instructing Claude to report only new or still-unaddressed issues to avoid duplicate comments".
- **Why the tempting answers are wrong:**
  - **Delete and repost everything:** noise, and comment threads get lost.
  - **"Avoid repeating yourself":** it can't see what it said before.
  - **Review the first commit only:** misses every later change.
- **Go deeper:** [Lesson 3, section 3.6](../../02-Lessons/02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md#36-claude-code-in-cicd)

**Decision 10: 40 of 1,200 batch requests fail, and all 1,200 get resent**

- **What's going on:** a few failed, so everything gets redone.
- **Under the hood:** the Message Batches API runs many requests at half price, within up to 24 hours. Each request carries a `custom_id` (a label you choose), and its result comes back with the same label. Results aren't guaranteed to come back in input order.
- **How to make the call:** if some requests fail, find them by `custom_id`, fix the cause and resubmit only those; if someone is waiting on the answer, use regular calls instead. Exam wording (task statement 4.5): "Handling batch failures: resubmitting only failed documents (identified by custom_id) with appropriate modifications (e.g., chunking documents that exceeded context limits)".
- **Why the tempting answers are wrong:**
  - **Resubmit the whole batch:** pays again for 1,160 good results.
  - **Switch to synchronous calls:** double the cost for a job nobody waits on.
  - **Match by position:** output order isn't guaranteed.
- **Go deeper:** [Lesson 4, section 4.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md#45-batch-processing)

</details>

## After this sim

1. For each decision you got wrong, reread the lesson section the key links to.
2. Missed a twist? Reread the task statement it names, then open its **Lesson** link.
3. Next: [SIM-07](SIM-07-structured-data-extraction.md).

## Blind decision and recovery checkpoints

Answer these free-response scenes before opening the coach rubric. They reuse locally authored practice scenes and do not establish unseen success after exposure. Submit mechanism, alternative, failure signal, recovery owner and proof; no automatic grading is claimed here. All cases are fictional.

### SIM-FV-18 — decision checkpoint

A separate job summarizes 2,000 independent supplied texts, needs no local filesystem or dependent tool loop and tolerates asynchronous completion. Which runtime is eligible for consideration?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Consider Messages Batch for independent supported API requests and recover individual failed or expired items. Independent eligible requests can be processed asynchronously; this is not a completion-time guarantee.

**Base choice:** A scheduled repository-dependent Code review runs headless with available credentials, scoped permissions, project context, exit handling and retained artifacts. Parse its CLI envelope before validating the findings payload.

**Changed constraint and recovery:** The work becomes independent eligible Messages requests with no local iterative state and a tolerant deadline. Consider batch; an urgent dependent tool loop remains a different runtime.

**Failure:** Missing credentials or malformed findings must produce an observable failure or bounded repair, never an empty “passed” report.

**Nearest alternative:** Nonblocking alone does not justify Messages Batch. JSON CLI output alone does not prove the findings schema or source accuracy.

**Conditional cue:** Runtime by dependency; gate by validated evidence.

**Proof:** Inspect `ci_packet={commit,permissions,environment,prompt,exit_code,envelope,findings}; accept=all_required_checks_pass` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.6.md#variant-fv-18).

</details>

### SIM-FV-23 — decision checkpoint

A launch approval now requires one result before constructing the next prompt, with a five-minute deadline and human clarification. What design fits?

<details>
<summary>Coach rubric — open after attempting</summary>


**Answer to this exact scene:** Use an appropriate interactive or synchronous dependent workflow with deadline and escalation handling. Dependent, time-sensitive human interaction changes the runtime requirements.

**Base choice:** Independent eligible document requests tolerate delayed completion and have per-item recovery. Messages Batch is a candidate; retain custom IDs and item states.

**Changed constraint and recovery:** A result is needed before the next dependent local tool step or a tight user deadline. Use the appropriate immediate/interactive runtime instead.

**Failure:** Some items expire or fail. Recover those items with their recorded inputs; do not treat a submission as completed work.

**Nearest alternative:** A 24-hour processing window is not a guaranteed finish time. Batch does not substitute for a local Code agent loop with filesystem state.

**Conditional cue:** Independent plus tolerant plus recoverable; otherwise another lane.

**Proof:** Inspect `items={i1:succeeded,i2:expired,i3:errored}; recovery=[i2,i3]; deadline_policy=explicit` and record the source/permission/state check that proves the result.

[Exact repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.5.md#variant-fv-23).

</details>


<span data-assessment-exposure="cct-fv-18-base-v1,cct-fv-18-retry-v1,cct-fv-23-base-v1,cct-fv-23-retry-v1"></span>

## Connected scenario learning route

[Scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md) · [Reference drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md) · [Recall cards](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md)

**Before the coach key:** name the deciding constraint, tool or instruction artifact, nearest losing alternative and recovery boundary. After the simulation, use a changed case below. Reading its lesson first is assisted practice.

- [FV-18 — Run CI with observable failure](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.6.md#variant-fv-18) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.6&variant=FV-18)
- [FV-23 — Choose batch by dependencies and deadline](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-4.5.md#variant-fv-23) · [Targeted question](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.5&variant=FV-23)

**Build the mechanism:** [Lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md). Execute only the relevant safe synthetic exercise; a written design is not an executed lab.