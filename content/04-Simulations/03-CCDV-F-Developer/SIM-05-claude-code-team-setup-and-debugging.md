# CCDV-F SIM-05 — Claude Code Team Setup, a Cost Check, then Debugging a Failure

**Primary domains:** 2 Applications and Integration, 5 Model Selection and Optimization, 3 Claude
Code, 4 Eval, Testing, and Debugging · **Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

Your eight-person team is rolling out Claude Code on a shared monorepo. The lead has been using it
alone for months, with most of the setup in personal files. You also own a nightly CI job that runs
Claude Code to summarize failing tests as JSON for a team dashboard, plus a small script that calls
the Messages API to tag each failing test by area (UI, API or database): a few thousand short calls
a night. Setup goes first, then finance asks why the tagging script costs so much. A few weeks
later the dashboard starts breaking on some nights and you have to find out why.


---

## The decisions (answer these before you open the key)

1. A new hire's Claude Code ignores the team's coding conventions. They live in the lead's `~/.claude/CLAUDE.md`.
2. Let Claude run the test command without prompting, but never read `.env` files
3. The CI job hangs forever
4. The tagging script runs on the most capable model and costs more than the rest of CI combined. Tagging is a simple three-way label.
5. To save money, someone set the tagger's `max_tokens` very low, and some tags now come back cut off
6. One night in five the dashboard rejects the JSON. First step?
7. The trace shows valid JSON from Claude, but the script mixed warning messages into the same stream
8. Other nights the JSON is valid but sometimes misses the required `owner` field
9. The trouble began the day the job's model alias moved to a newer release
10. You later upgrade the pinned version on purpose, after the evals pass. The next bill shows noticeably more input tokens for the same tests.

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | A new hire's Claude Code ignores the team's coding conventions. They live in the lead's `~/.claude/CLAUDE.md`. | **Move them to the project CLAUDE.md** checked into the repo. User-level files aren't shared. | Email the new hire a copy; paste the rules into each prompt; switch to a stronger model | D3 Claude Code Operation (CLAUDE.md hierarchy) | [Lesson 7, section 3.2](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |
| 2 | Let Claude run the test command without prompting, but never read `.env` files | **Allow and deny rules in the project's checked-in `settings.json`** | "Please don't read .env" in CLAUDE.md; each developer clicks approve every time; turn off permission checks | D2 Configuration Management; D3 settings.json | [Lesson 7, section 3.2](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md), [Lesson 1, section 2.6](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 3 | The CI job hangs forever | **Run headless (`-p`)** with JSON output so nothing waits for keyboard input | Add a timeout and rerun; answer the prompt with `yes` piped in; run it interactively on a build agent | D3 Claude Code Operation (headless mode) | [Lesson 7, section 3.3](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |
| 4 | The tagging script runs on the most capable model and costs more than the rest of CI combined. Tagging is a simple three-way label. | **Measure cheaper setups on an eval set first**: lower the effort, and try a small, fast tier (such as Haiku) for this simple classification; switch only if the eval holds | Keep the top model "to be safe"; switch to the cheapest model with no test; pick by price alone | D5 Model Selection and Tradeoffs | [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 5 | To save money, someone set the tagger's `max_tokens` very low, and some tags now come back cut off | **You pay for tokens generated, not for the cap.** Set `max_tokens` to fit the longest valid answer, check `stop_reason` for `max_tokens`, and keep the answer short with a schema or an enum of allowed tags | Lower the cap further; treat a cut-off tag as "UI" by default; retry until it happens to fit | D5 Cost and Token Management | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 6 | One night in five the dashboard rejects the JSON. First step? | **Pull the trace for a failing run** and compare the raw model output with what the parser received, to find out whether the integration layer or the model is at fault | Rewrite the prompt right away; switch to a bigger model; add blind retries | D4 Debugging and Error Handling (problem origin isolation) | [Lesson 7, section 4.2](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |
| 7 | The trace shows valid JSON from Claude, but the script mixed warning messages into the same stream | **Fix the plumbing** (separate output from warnings). It's an integration bug, not a model bug. | Add "output only JSON" to the prompt; change models; strip non-JSON with a regex and move on | D4 Debugging and Error Handling (trace analysis) | [Lesson 7, section 4.2](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |
| 8 | Other nights the JSON is valid but sometimes misses the required `owner` field | **Validate against a schema** (structured output), and reject or retry with the validation error instead of passing it on | Trust it because it parsed; fill a default owner silently; ask the model to "always include owner" | D2 Claude Application Design (schema design); D6 Output Handling | [Lesson 1, section 2.5](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 4, section 6.5](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 9 | The trouble began the day the job's model alias moved to a newer release | **Pin a specific model version** in config and run your evals before upgrading on purpose | Always track the latest alias; roll back the prompt instead; blame the CI runner | D2 Configuration Management (model version pinning); D5 Model Selection (breaking changes) | [Lesson 1, section 2.6](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 10 | You later upgrade the pinned version on purpose, after the evals pass. The next bill shows noticeably more input tokens for the same tests. | **Expect the newer tokenizer**: newer models can count more tokens for the same text. Re-measure with token counting and `usage`, then reset budgets and cost forecasts. | Roll back at once; assume it's a billing error; cut the prompt by the same percentage without testing | D5 LLM Fundamentals (tokens) | [Lesson 2, section 5.1](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |

**Scoring:** 8 or more is a pass. The three principles: *put shared rules where the whole team gets
them (project files, settings), not in personal files or prompt pleas*, *cut cost with evidence:
cheaper settings proven on an eval, and a budget based on measured tokens*, and *find where the
failure starts, integration layer or model output, from the trace before you change anything*.

Sources (Tier 1): [CCDV-F exam guide, Domains 2–5](https://anthropic-partners.skilljar.com/page/partner-certifications),
[CCAR-F exam guide, Task Statements 3.1, 3.2 and 3.6](https://anthropic-partners.skilljar.com/page/partner-certifications),
structured outputs,
choosing a model,
effort,
context windows.

</details>