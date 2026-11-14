# CCDV-F Lesson 4 — Prompt and Context Engineering (11%, about 6 questions)

**Time:** 90 min plus lab 02 · **Practice:** [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Skills:** Context Engineering 3.8% · Prompt Engineering 4.6% · Output Handling 2.6%
**Already covered in CCAR-F:** [L04 Prompt Engineering and Structured Output](../02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md)
and [L05 Context Management](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md).
Review those, then spend your time on what's new here: the API-level mechanics.

## 6.0 The big idea

The context window is a desk, not a warehouse: everything on it costs room and attention. Put
only what the task needs on it, in a clear order, and check the output in code instead of
trusting that it looks right.

## 6.1 What fills the context window

- **Everything in the request counts:** the system prompt, every message (tool results, images,
  documents), and your **tool definitions**. The output counts too, including thinking.
- **Cached tokens still count.** Caching changes what you pay, not how much room you use.
- **More context isn't automatically better.** As tokens grow, recall drops ("context rot"). What
  you put in matters as much as how big the window is.
- **Overflow:** input bigger than the window gets a **400 `invalid_request_error`** ("prompt is too
  long"). On newer models, running out mid-answer stops with
  `stop_reason: "model_context_window_exceeded"`. Handle both.
- Estimate before you send with the **token counting API**. Read what you used in `usage`.

## 6.2 Stopping drift and bloat

Drift is the model losing track of the task. Bloat is context full of stuff it no longer needs.

| Technique | What it does | Where |
| --- | --- | --- |
| **Prune tool output** | Return only the fields that matter, not the whole 40-field record | Your tool code |
| **Tool result clearing** | Drops old tool results in long agent runs | API context editing |
| **Compaction** | Summarizes earlier turns so the conversation continues past the limit | API server-side compaction (beta, check the current docs for models); `/compact` in Claude Code |
| **Case facts block** | Keeps exact amounts, dates and IDs outside the summarized history | Your prompt ([CCAR-F 5.1](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md)) |
| **Defer tool definitions** | Loads tools on demand instead of all up front | Tool search tool |

- Summaries blur details. **Compaction plus a case-facts block** keeps both room and precision.
- For work across several context windows, keep **state in files** (progress notes, a test list)
  so a fresh session recovers quickly.

## 6.3 Isolation with subagents and steps

- A **subagent** does the noisy work (search 200 files, read long logs) in its own context and
  returns a **short structured summary**. The parent never sees the noise.
- A **multi-step workflow** does the same: each step gets only the inputs it needs.
- **Don't overuse it.** Newer models spawn subagents readily. For a simple grep or a single-file
  edit, work directly. Tell the model when subagents are and aren't warranted.

## 6.4 Writing the prompt

- **Be clear and direct.** Golden rule: if a colleague with no context would be confused, Claude
  will be too. Use numbered steps when order matters.
- **Say why.** "This is read aloud by text-to-speech, so no ellipses" beats "NEVER use ellipses".
  Claude generalizes from the reason.
- **Few-shot:** 3–5 examples that are **relevant, diverse** (cover edge cases) and wrapped in
  `<example>` tags so they aren't read as instructions.
- **XML tags** separate instructions, context, examples and input: `<instructions>`, `<document>`.
- **Long documents go at the top**, the question at the end. Anthropic's tests show up to 30%
  better answers on complex multi-document inputs.

**Where each instruction belongs:**

| Component | Put here |
| --- | --- |
| System prompt | Role, durable rules, the untrusted-content policy |
| User turn | The task, the data, the question (after long documents) |
| Tool description | When to use this tool and when not to ([L05](L05-tools-and-mcps.md)) |
| Tool result | **Data only.** Your own instructions there may be treated as injection. Send them in the next user turn. |
| CLAUDE.md / Skill | Project standards / on-demand workflows ([L07](L07-claude-code-eval-and-debugging.md)) |

- **Output constraints:** state the format and length. **Prefill is not supported** on Claude 4.6
  and later models (400 error). Use structured outputs or a direct instruction instead.
- **Iterate like an engineer:** keep a small test set, change **one thing** at a time, rerun, compare.
- **Sanitize input:** wrap user text in tags or JSON-encode it, cap its length, and screen it
  before it reaches the main prompt ([L06](L06-security-and-safety.md)).

## 6.5 Handling the output

- **Structured outputs** (`output_config.format` with a JSON schema) and **strict tool use**
  (`strict: true`) guarantee schema-valid output through constrained decoding. This is newer and
  stronger than the "tool use removes syntax errors" rule in CCAR-F L04.
- **It still can break:** `stop_reason: "refusal"` or `"max_tokens"` can return output that doesn't
  match the schema, and enum values can come back with different capitalization.
- **Schema-valid is not correct.** Totals can still not add up. **Validate the meaning in code.**
- **Defensive parsing:** check `stop_reason` first, find content blocks **by type**, not by position,
  treat missing optional fields as normal, and log failures. Never swallow them silently.
- **Be skeptical of confident output.** A fluent answer can be invented. Let Claude say "I don't
  know", ask for **direct quotes** first on long documents, and have it retract any claim it can't
  back with a quote. For high stakes, run it several times and compare.

## Worked example

A log-triage agent works well for 10 turns, then starts repeating itself and missing obvious
errors. Each tool call returns 5,000 raw log lines. **Answer:** prune the tool to return only
matching error lines with timestamps, move full-log scanning into a subagent that returns a
summary, and compact older turns. A model with a bigger window only delays the same failure.

## Traps

- "Use a bigger context window." Curate the context instead.
- "Put the formatting rules inside the tool result." That's data, not instructions.
- "Prefill `{` to force JSON." Unsupported on current models. Use structured outputs.
- "It matched the schema, so it's right." Syntax is guaranteed; meaning isn't.
- "Cached tokens are free space." They still fill the window.

## Try it, lab 02 (45 min)

In [lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md), switch the extraction call to
`output_config.format`. Add code checks for the meaning (totals add up, dates are real), check
`stop_reason` before parsing, and trim one subagent's tool output to 5 fields. Compare
`usage.input_tokens` before and after.

## Done when

- [ ] You can list everything that counts toward the context window
- [ ] You can pick pruning, compaction or a subagent for a given bloat problem
- [ ] You can say where an instruction belongs across system, user, tool and CLAUDE.md
- [ ] You can name the three ways structured output can still come back wrong
- [ ] You scored 80% or more on [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L05 Tools and MCPs](L05-tools-and-mcps.md)

Source: CCDV-F exam guide v1.0, Domain 6; [context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows);
[prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices);
[structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs);
[mitigate jailbreaks](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks);
[reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations).