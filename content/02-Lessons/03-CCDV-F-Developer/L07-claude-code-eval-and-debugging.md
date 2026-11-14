# CCDV-F Lesson 7 — Claude Code, Eval and Debugging (5.7%, about 3 questions)

**Time:** 2 hours plus lab 03 · **Practice:** [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Skills:** Claude Code Operation 3.1% (Domain 3) · Debugging and Error Handling 2.6% (Domain 4)
**Already covered in CCAR-F:** [L03 Claude Code Configuration and Workflows](../02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md)
and [L05 5.3](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) (error passing). Review them first.

## 3.0 The big idea

Two small domains share this lesson, so its sections carry both prefixes: 3.x is Domain 3 (Claude
Code), 4.x is Domain 4 (Eval, Testing, and Debugging). For Claude Code: shared rules go in project
files committed to git, permissions go in `settings.json`, and CI runs headless. For debugging:
name the error, find the first step that went wrong in the trace, and fix only that.

## What people who passed say

- **Two colleagues who passed:** more Claude Code than the 3% weight suggests (CLI,
  CLAUDE.md, Skills, `settings.json`, subagents). It also sits inside Domain 2's Configuration
  Management. **One of them:** the Agent SDK, streaming and protocols came up in scenarios.
  ([Insights](../../11-Lessons-Learned/INSIGHTS.md))

## 3.1 The five building blocks

| Block | What it is | Where it lives | Loaded |
| --- | --- | --- | --- |
| **Rules** | Standards and conventions (CLAUDE.md plus topic files) | `CLAUDE.md`, `.claude/rules/*.md` (with optional `paths`) | Always, or when matching files are touched |
| **Skills** | A folder with `SKILL.md` plus optional scripts and files | `.claude/skills/<name>/` or `~/.claude/skills/` | **On demand**, when the task matches its description |
| **Commands** | A saved prompt you run by name (`/review`) | `.claude/commands/` or `~/.claude/commands/` | When you type it |
| **Agents** | Subagents with their own prompt, tools and context | `.claude/agents/<name>.md` (check the current docs for user level) | When Claude delegates or you ask |
| **Agent Memory** | What persists between sessions | CLAUDE.md you write; notes Claude Code can keep itself | Start of session |

- For Claude's own notes, check the current docs for where they're stored and how to turn them off.
- **Project level is shared through git; user level is only yours.** Same rule for every block.

## 3.2 CLAUDE.md, `/init` and `settings.json`

- **Hierarchy:** user `~/.claude/CLAUDE.md` → project `CLAUDE.md` (or `.claude/CLAUDE.md`) →
  directory `sub/CLAUDE.md`. More specific files add to the general ones.
- **`/init`** reads the repo and drafts a starting CLAUDE.md (build commands, layout,
  conventions). Review it, trim it, commit it.
- **`settings.json`** holds **configuration**, not instructions: permissions, hooks, environment
  variables, model and similar.

| File | Scope | Commit it? |
| --- | --- | --- |
| `~/.claude/settings.json` | You, every project | No |
| `.claude/settings.json` | The team, this project | **Yes** |
| `.claude/settings.local.json` | You, this project | No (git-ignored) |

- **Permissions** are `allow`, `ask` and `deny` rules per tool, for example allow
  `Bash(npm test *)` (the older `Bash(npm test:*)` form means the same), deny reading `.env`.
  Rules are checked deny, then ask, then allow, so **deny wins**. When the same setting appears
  at several levels, the order from highest to lowest is: managed settings (users can't
  override them), command-line flags, `.claude/settings.local.json`, `.claude/settings.json`,
  then your user `~/.claude/settings.json`
  ([permissions](https://code.claude.com/docs/en/permissions),
  [settings](https://code.claude.com/docs/en/settings), Tier 1).
- **Rule of thumb:** "how we write code" goes in CLAUDE.md; "what Claude may do" in `settings.json`.

## 3.3 Sessions, modes and automation

- **Slash commands:** built-ins include `/init`, `/memory`, `/compact`, `/clear`, `/permissions`,
  `/agents`, `/mcp`, `/hooks`; custom ones come from commands and skills. `/help` lists them.
- **Sessions:** `--continue` picks up the latest; `--resume` a named or earlier one. `/clear` starts
  clean; `/compact` summarizes to free room ([L04](L04-prompt-and-context-engineering.md)).
- **Headless mode:** `claude -p "..."` runs once, never waits for input, and exits. Use it in CI;
  add `--output-format json` for a parseable result.
- **Streaming output:** a streaming JSON format (`stream-json`) emits events as they happen, so a
  script can show progress mid-run. Check the current docs for flag names.
- **Permission modes:** default (asks), accept-edits, **plan** (read-only planning) and an
  **auto mode** that lets Claude proceed without asking for each step, with safeguards. Check the
  current docs for exactly what auto mode approves. Use it only where mistakes are cheap and
  reversible, and keep deny rules and hooks on ([L06 7.4](L06-security-and-safety.md)).

## 4.1 Name the error before you fix it

| Signal | Meaning | Recovery |
| --- | --- | --- |
| **429 `rate_limit_error`** | Too many requests or tokens per minute | Wait for `retry-after`, then retry with **exponential backoff and jitter** |
| 429 with no `retry-after`, `enforced_spend_limit_reached` | Monthly spend cap hit | **Retrying won't help.** Raise the limit |
| **529 `overloaded_error`** | Anthropic is busy | Retry with backoff; can also arrive **mid-stream** after a 200 |
| **500 `api_error`** | Server-side fault | Retry with backoff, a few times |
| **400 `invalid_request_error`** | Your request is wrong: bad schema, prompt too long, prefill on a new model | **Fix the input.** Retrying the same request fails the same way |
| 401 / 403 | Bad key or no permission | Fix credentials; never retry blindly |
| `tool_result` with `is_error` | Your tool failed | Depends on the tool's error type ([L05](L05-tools-and-mcps.md)) |
| `stop_reason` `max_tokens` / `refusal` | Not an error, but output is cut off or declined | Raise `max_tokens` or split; handle refusals in the UI |

- **Transient: retry. Validation: fix.** The SDKs retry some errors automatically (check the docs).

## 4.2 Traces and where the problem lives

- **Log a trace for every call:** request (model, prompt version, tools), response, `stop_reason`,
  each tool call and result, `usage` and the **`request_id`**. Find the **first** step that went wrong.

| Integration-layer problem | Model-output problem |
| --- | --- |
| HTTP error, wrong model string, bad JSON sent | Request fine, answer wrong or off-format |
| Tool dispatched to the wrong function; result not returned | Claude picked the wrong tool (fix the description) |
| Retrieval returned the wrong documents | Right documents, wrong reasoning (fix the prompt, examples) |
| Parser broke on a valid response | Answer invented a fact (ground it, allow "I don't know") |

- **Isolation test:** replay the **exact** logged request. Good output means the bug is in your
  code; bad output means work on the prompt or model.

## 4.3 Simple evals

- A **test set** of real inputs with expected outputs, including edge cases and past failures.
  **Grade by code** where you can (valid JSON, right label); use a **model grader with a rubric**
  for open-ended answers. **Rerun on every change** to prompt, model version or tools.

## Worked example

A nightly Claude Code CI job hangs, and when it runs, the summary step sometimes fails with a
400. **Answer:** run it headless (`claude -p ... --output-format json`) so it never waits for
input. The 400 message says the prompt is too long: trim the input. Retrying a 400 changes
nothing; backoff is for 429, 500 and 529.

## Traps

- Retrying a 400 in a loop.
- Treating a mid-stream `overloaded_error` as impossible because the HTTP status was 200.
- Blaming the model before replaying the logged request.
- Team permissions in `~/.claude/settings.json`; auto mode with no deny rules or hooks.

## Try it, lab 03 part 2 (60 min)

In [lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md), run `/init`, then add a
`.claude/settings.json` that allows `npm test` and denies reading `.env`. Add the `PreToolUse`
hook from [L06](L06-security-and-safety.md). Run one task with `claude -p --output-format json`.
Then write a 10-case eval for the MCP tool and log a trace for each run.

## Done when

- [ ] You can place Rules, Skills, Commands, Agents and Memory, and say who sees each
- [ ] You can say what goes in CLAUDE.md vs `settings.json`, and which settings file to commit
- [ ] You can match 429, 529, 500 and 400 to the right recovery
- [ ] You can sort a failure into integration layer or model output from a trace
- [ ] You scored 80% or more on [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [CCDV-F scenario simulations](../../04-Simulations/03-CCDV-F-Developer/README.md)

Source: CCDV-F exam guide v1.0, Domains 3 and 4; [rate limits](https://platform.claude.com/docs/en/api/rate-limits);
[streaming, error events](https://platform.claude.com/docs/en/build-with-claude/streaming);
[context windows, overflow](https://platform.claude.com/docs/en/build-with-claude/context-windows);
[API errors](https://platform.claude.com/docs/en/api/errors); CCAR-F exam guide v1.0, 3.1–3.6;
Claude Code docs (settings, permissions, CLI reference; not saved locally, check current pages).