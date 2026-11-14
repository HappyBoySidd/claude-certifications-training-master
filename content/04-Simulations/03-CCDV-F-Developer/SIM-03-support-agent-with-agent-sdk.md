# CCDV-F SIM-03 — Support Agent with the Claude Agent SDK

**Primary domains:** 1 Agents and Workflows, 6 Prompt and Context Engineering, 8 Tools and MCPs ·
**Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

You're building a support agent for a home-internet provider with the Claude Agent SDK. It has
four tools: `check_account`, `run_line_test`, `schedule_technician` and `issue_credit`. A
knowledge-base subagent looks up troubleshooting articles. Conversations run long, the line-test
service is flaky, and the business rule is firm: **no credit is ever issued to an unverified account
or above the agent's limit without a person approving it**.


---

## The decisions (answer these before you open the key)

1. In your first custom loop the customer never gets an answer after the agent calls a tool
2. Password resets always follow the same three fixed steps
3. Enforcing the credit rule
4. The agent calls `run_line_test` when it should check for an area outage
5. `run_line_test` times out
6. Line-test output is thousands of lines and fills the context
7. After a long chat the agent forgets the account was already verified
8. The knowledge-base subagent returns articles for the wrong router model
9. Tone and refund policy are pasted into every user message and ignored after many turns
10. Which tools the knowledge-base subagent gets

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | In your first custom loop the customer never gets an answer after the agent calls a tool | **Send the tool's output back** as a `tool_result` with the matching `tool_use_id`, call Claude again, keep going while `stop_reason` is `tool_use`, and stop on `end_turn` | Stop as soon as any text block appears; a fixed 5-turn cap as the main stop rule; search the text for "done" | D1 Agent Construction with Claude; D8 Tool Implementation | [Lesson 3, section 1.2](../../02-Lessons/03-CCDV-F-Developer/L03-agents-and-workflows.md) |
| 2 | Password resets always follow the same three fixed steps | **Build that path as a plain workflow in code** and keep the agent for open-ended troubleshooting | Let the agent handle everything; list the steps in a longer prompt; use a bigger model for reliability | D1 Agent Architecture (workflow vs agent) | [Lesson 3, section 1.1](../../02-Lessons/03-CCDV-F-Developer/L03-agents-and-workflows.md) |
| 3 | Enforcing the credit rule | A **hook that runs before `issue_credit`** and blocks it unless the account is verified and the amount is under the limit, routing the rest to human approval | A bold rule in the system prompt; ask the model to double-check itself; review a log of credits each week | D1 Agent Construction (hooks for deterministic actions); D7 Claude Hooks | [Lesson 3, section 1.2](../../02-Lessons/03-CCDV-F-Developer/L03-agents-and-workflows.md) |
| 4 | The agent calls `run_line_test` when it should check for an area outage | **Rewrite both tool descriptions**: what each does, when to use it instead of the other, inputs and what it returns | Rename the tools only; merge them into one tool with a mode flag and no description; add examples to the system prompt only | D8 Tool Implementation (tool descriptions) | [Lesson 5, section 8.1](../../02-Lessons/03-CCDV-F-Developer/L05-tools-and-mcps.md) |
| 5 | `run_line_test` times out | Return a `tool_result` with **`is_error: true` and a clear message** (temporary failure, safe to retry) so the agent can decide what to do | Throw an exception that ends the session; return "no faults found"; return an empty result | D8 Tool Implementation (error handling) | [Lesson 5, section 8.1](../../02-Lessons/03-CCDV-F-Developer/L05-tools-and-mcps.md) |
| 6 | Line-test output is thousands of lines and fills the context | **Prune tool output** to the fields that matter, or send the raw log to a subagent that returns a short finding | Rely on a bigger context window; keep the full log "just in case"; tell the model to skip irrelevant lines | D6 Context Engineering (tool output pruning, isolation) | [Lesson 4, section 6.2](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 7 | After a long chat the agent forgets the account was already verified | **Compact older turns** and keep a persistent "case facts" block (account ID, verified status, promises made) outside the compacted history | Keep the entire history forever; restart the session and lose the state; add "remember earlier details" to the prompt | D6 Context Engineering (compaction, drift) | [Lesson 4, section 6.2](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 8 | The knowledge-base subagent returns articles for the wrong router model | **Put the task, the customer's key facts and the expected output format in the subagent's prompt.** Subagents start with a fresh context. | Assume it inherits the parent's conversation; give it every tool; switch it to a bigger model | D1 Agent Patterns (subagents); D6 Context Engineering | [Lesson 3, section 1.3](../../02-Lessons/03-CCDV-F-Developer/L03-agents-and-workflows.md) |
| 9 | Tone and refund policy are pasted into every user message and ignored after many turns | **Put the stable role and policy in the system prompt**, clearly stated with the reason; keep per-turn data in user messages | Write the rules in all caps; repeat them in every message; add more examples of angry customers | D6 Prompt Engineering (system vs user placement) | [Lesson 4, section 6.4](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 10 | Which tools the knowledge-base subagent gets | **Only read-only article search.** No account, scheduling or credit tools. | All tools "for flexibility"; the same tools as the parent; credit tools so it can "close the loop" | D8 Tool Implementation (tool set construction); D7 Guardrails (least privilege) | [Lesson 5, section 8.3](../../02-Lessons/03-CCDV-F-Developer/L05-tools-and-mcps.md) |

**Scoring:** 8 or more is a pass. Decisions 3 and 7 are the heart of the scenario: *firm rules
live in code and hooks, not the prompt*, and *keep context lean: prune, compact, isolate*.

Sources: tool use,
context windows,
prompting best practices.

</details>