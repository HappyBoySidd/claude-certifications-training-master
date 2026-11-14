# CCAR-F Lesson 1 — Agentic Architecture and Orchestration (27%, about 16 questions, the BIGGEST)

**Picture the application:** A support customer asks about an order and a possible refund. The service should investigate the right account, explain what happened and report only actions actually completed. Agentic architecture is the technical topic: deciding who gathers evidence, how work continues and where executable prerequisites protect the action boundary.

**Time:** 2–3 hours plus [lab 02, the agent loop, subagents and schema-checked extraction lab](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) · **Practice:** [CCAR-F practice — choose Domain 1](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)
**Scenarios:** 1 Support, 3 Research, 4 Dev productivity


<!-- layered-scenario-migration -->
## Learn this domain through connected case studies

Read and predict; no account, code execution or setup is required for these teaching scenes. Each stage names its application and the requirement that fails. Some stages transfer the same decision to a different application; follow the named people and data rather than assuming every stage belongs to one system. The original reference sections remain below for detail. These are original teaching questions, not claimed live exam items. Write your choice before revealing the repair. Diagrams below show AI reasoning and ordinary software checks explicitly in their labels.

### Stage 1 — The assistant asks for a fact, but nobody fetches it

A support worker asks whether order ORD4 can be returned. In the small working version, the application fetches the order and Claude explains it. The broken version stops as soon as Claude asks to call `lookup_order`: the customer receives no order information. A tool call is a request to the application to do work, not evidence that the work happened.

**Original exam-style practice — choose ONE.** A Messages API application receives a `tool_use` block and `stop_reason: tool_use`. Which implementation correctly advances the agentic loop?

A. Treat the tool request as the final customer answer.

B. Execute the permitted tool, append the assistant turn and matching tool results, then request the next model turn.

C. Discard the assistant turn and send an unrelated user message.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The application fetches the fact and returns it with the identifier of the request that asked for it. A stops before the work; C loses the connection between request and result. The model proposes a call; application code owns execution and error handling.

**Follow the changed path:**

```text
customer → Claude tool request → application checks and executes lookup
lookup result + matching call ID → Claude → customer explanation
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Inspect the trace for one request ID, its matching result, and a final answer grounded in that result. A truncated response or exhausted safety cap remains incomplete, even if text exists.

</details>

**Changed-constraint decision — choose ONE before revealing:** The tool reports a timeout. A: return an empty successful order; B: return an explicit failure and let the application apply its bounded recovery policy.

<details><summary>Reveal changed-constraint reasoning</summary>

B. No response is different from an order with no return eligibility. Preserve the failed operation and avoid inventing a result.

</details>

**Objective connections:** [1.1](objectives/objective-1.1.md).

### Stage 2 — Another investigator joins, but receives the wrong brief

The support case now needs both an order check and a policy check. Each specialist works in a separate conversation. The coordinator tells the policy specialist “use what the other agent found,” but sends neither the order nor its evidence. The reply confidently discusses a different product.

**Original exam-style practice — choose ONE.** Which coordinator-subagent design best preserves context isolation while enabling evidence-grounded synthesis?

A. Assume all subagents inherit the coordinator conversation automatically.

B. Broadcast all transcripts to every specialist indefinitely.

C. Pass a bounded brief containing the task, relevant facts, source references and expected return contract; validate the returned evidence before synthesis.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice C.** A separate conversation needs an explicit briefing packet. C supplies what this job requires and lets the receiver check it. A assumes memory that may not exist; B carries unrelated history, extra cost and potentially unnecessary sensitive data.

**Follow the changed path:**

```text
coordinator → bounded brief → specialist → result + sources + status
receiver checks required fields and evidence → integrated answer
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Remove the order reference from the brief: the specialist must flag missing evidence rather than supply a made-up answer. Restore it and trace the returned claim back to that order.

</details>

**Changed-constraint decision — choose ONE before revealing:** Both checks can be completed reliably with one agent and two tools. A: always add specialists; B: keep the simpler design unless specialization solves a demonstrated requirement.

<details><summary>Reveal changed-constraint reasoning</summary>

B. More agents are not a quality guarantee. Split work when independent expertise, context or work boundaries justify the coordination cost.

</details>

**Objective connections:** [1.2](objectives/objective-1.2.md), [1.3](objectives/objective-1.3.md), [1.6](objectives/objective-1.6.md).

### Stage 3 — A proposal becomes a money movement

The customer now requests a refund. A person approves USD 80 for ORD4, but a later proposal changes to USD 90. The old design remembers only “approved: yes.” That broad flag would let a changed action through.

**Original exam-style practice — choose ONE.** Which control best enforces approval scope before execution of a side-effecting tool?

A. Instruct Claude to remember the approved amount.

B. Validate the current principal, order, amount and approval validity against the bound proposal in the runtime/backend before submitting the action.

C. Execute first and inspect the model explanation afterward.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The program compares this exact action with what was approved. A model reminder can help behavior but cannot replace that gate. C finds the problem after money may already move. A hook can intercept an attempted call; business authorization still belongs at the authoritative service boundary.

**Follow the changed path:**

```text
proposal → approval bound to exact action → runtime/backend gate → business API
changed target, amount or expired approval → deny or request new approval
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Keep the approval record and action fields. Changing one field must block submission; a matching permitted action still needs a real business receipt before being called settled.

</details>

**Changed-constraint decision — choose ONE before revealing:** The write timed out after submission. A: blindly resubmit; B: inspect the business operation status with the operation key before deciding whether retry is safe.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Timeout means the caller lacks a result, not that the operation failed. Reconciliation prevents a duplicate effect.

</details>

**Objective connections:** [1.4](objectives/objective-1.4.md), [1.5](objectives/objective-1.5.md), [1.7](objectives/objective-1.7.md).

<!-- /layered-scenario-migration -->

## Connect plain reasoning to technical choices

Start with the business constraint, then learn the documentation term and the option it rules out. These worked application bridges show both levels: [AS-01-action-service](architecture-studio/AS-01-action-service.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-04-research-system](architecture-studio/AS-04-research-system.md#connect-the-simple-explanation-to-technical-design-choices) · [AS-08-resumable-case](architecture-studio/AS-08-resumable-case.md#connect-the-simple-explanation-to-technical-design-choices). Read [artifact types and study mode](architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course) before interpreting examples as build instructions. Reading needs no API setup; runnable activities retain their own prerequisites.


## 1.0 The big idea

An agent is a loop: Claude asks for a tool, your code runs it and hands back the result, and this
repeats until Claude says it's finished. Bigger jobs split into a coordinator that hands focused
pieces to subagents, which see only what you pass them. When a rule must always hold, you enforce
it in code, not in the prompt.

## 1.1 The agentic loop

```text
send request → read stop_reason
  "tool_use"  → run the requested tool(s) → append the results to history → loop
  "end_turn"  → finished
```

- Tool results are **appended to the conversation history**, so Claude can reason about the next
  step.
- **Handling a tool result, step by step:** the assistant turn that asked for the tool stays in
  history; your code runs every `tool_use` block in it; then it sends one user turn holding a
  `tool_result` for each, matched by `tool_use_id`. If a tool failed, send the result anyway,
  marked as an error, so Claude can change course instead of guessing.
- **An iteration cap is a safety net, not the stop signal.** Keep a cap so a broken loop can't run
  up cost forever, but the normal exit is `stop_reason: "end_turn"`. Hitting the cap means
  something is wrong: log it and fix the design.
- *Model-driven* decisions (Claude picks the next tool) vs a *pre-set decision tree*. Know the
  difference. Model-driven means Claude reads each tool result and chooses the next step itself. A
  pre-set decision tree means your code fixes the order of steps in advance, whatever the results
  say. The exam cares because questions about loops and tools test whether you let Claude decide
  when the path depends on what it finds.
- **Anti-patterns (these are the wrong answers):**
  - parsing natural language ("I'm done") to decide when to stop
  - an **arbitrary iteration cap as the main stop signal**
  - treating "the assistant returned text" as the completion signal

## 1.2 Coordinator and subagents (hub and spoke)

- The **coordinator** handles all communication between subagents, error handling and routing. It
  decomposes the task, delegates it and aggregates the results.
- **Subagents have isolated context.** They don't inherit the coordinator's history.
- Route **all** subagent traffic through the coordinator, for observability and consistent error
  handling.
- Pick subagents **dynamically** according to how complex the query is. Don't always run the full
  pipeline.
- **Partition the scope** (distinct subtopics or source types) to avoid duplicated work.
- **Risk:** decomposition that's too narrow leaves gaps in coverage. The fix is an *iterative
  refinement loop*: the coordinator checks the synthesis for gaps, re-delegates targeted queries,
  and re-synthesizes.

## 1.3 Spawning subagents and passing context

- **Saved-guide terminology:** task 1.3 uses the `Task` tool and its permission configuration
  for delegation. Current Claude Code uses `Agent` (`Task` remains an alias), and `allowedTools`
  pre-approves permission prompts; do not treat it as a complete tool-availability or downstream
  authorization policy. Compare [saved-guide wording with current contracts](deep-practice/conditions-and-errors.md#exam-answer-vs-today).
- Context must be **passed explicitly in the prompt**, because there's no shared memory. Pass
  *complete* findings, for example the search results and the analysis output going to synthesis.
- Use **structured formats** to separate content from metadata (URL, document, page) so
  attribution survives.
- **Parallel spawning** means several Task calls **in one coordinator response**, not spread across
  turns.
- Give coordinator prompts **goals and quality criteria**, not step-by-step procedures, so
  subagents can adapt.
- `AgentDefinition` (the Agent SDK object that describes one kind of subagent) holds the
  description, system prompt and tool restrictions for each subagent type.
- **Design the handoff:** isolated workers return a report rather than automatically sharing their
  whole context. Require findings, exact source locators, relevant failure excerpts and artifact
  paths. Current Claude Code can persist/resume worker transcripts; this does not automatically
  put their evidence into the parent's context.
- **Choose delegation for a reason:** keep small or tightly coupled work together when handoffs
  lose evidence or add latency. Sequential workers and test runners can help when their reports
  preserve what the next step needs. Scope tools to authorized work; a role label alone does not
  establish expertise or correctness.
  ([subagent guidance](https://code.claude.com/docs/en/sub-agents), checked 2026-10-21.)

## 1.4 Enforcement and handoff

- **Programmatic enforcement** (hooks, prerequisite gates) vs **prompt guidance**. When
  compliance must be deterministic, prompts alone fail some of the time.
- **Classic example:** block `process_refund` until `get_customer` has returned a **verified
  customer ID**.
- For a request with several concerns, split it into items, investigate them in parallel with
  shared context, then give one resolution.
- **Handoff to a human:** a structured summary with the customer ID, root cause, amount and
  recommended action. The human **can't see the transcript**.

## 1.5 Agent SDK hooks

A hook is your own code that the Agent SDK runs at a fixed point in the loop. Each row is one hook point; the "Use" column says what you would do there.

| Hook | Use |
| --- | --- |
| **PostToolUse** | Transform results *before* the model sees them. For example, normalize Unix, ISO 8601 and numeric status codes coming from different MCP tools. |
| **PreToolUse** (tool-call interception) | Block actions that break policy, such as a **refund over $500**, and redirect to human escalation |

PreToolUse runs before the tool and sees only the inputs; PostToolUse runs after and sees the
result.

**Current hook contracts (implementation context for objective 1.5).** An Agent SDK
`PreToolUse` callback can return `hookSpecificOutput` containing `hookEventName: "PreToolUse"`,
`permissionDecision: "deny"` and a reason. `{}` makes no overriding decision; other permissions
still apply. `PostToolUse` can transform observed output but cannot prevent a completed effect.
Current SDK pre-tool callback timeout blocks the call; check the installed runtime contract.

**Claude Code command hooks use a separate contract:**

| Result | Interpretation |
| --- | --- |
| Exit 0 | Parse supported stdout JSON; its decision may deny, ask, allow or leave normal checking in place. |
| Exit 2 | Blocks on a blockable event and reports the reason. |
| Other exit or timeout | Normally no blocking hook decision; normal permission checks still apply. |

Current command/HTTP hooks support `onFailure: "block"` from version 2.1.295. A post-tool failure
cannot undo execution. Enforce mandatory predicates at a supported pre-effect hook **or action
service**, with complete effect-path coverage and tested rejection/failure handling. Instructions
explain desired behavior; they do not implement enforcement.

Current fail-closed command-hook illustration (requires a real, tested script and supported version):

```json
{ "hooks": { "PreToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command", "onFailure": "block",
    "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-path.sh" } ] } ] } }
```

Sources: [SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks),
[command hooks](https://code.claude.com/docs/en/hooks), checked 2026-10-21. A matcher covers only
matched tool paths; this example does not establish complete application security.

**Prompts guide; executable checks enforce stated predicates.** Choose a supported pre-effect hook or service guard for a mandatory rule. Correctness depends on event timing, trustworthy inputs, tested rejection behavior and coverage of every effect path. A post-tool transform cannot prevent an already completed action; deterministic code alone does not prove business truth.

## 1.6 Breaking the task down

| Pattern | Use for |
| --- | --- |
| **Prompt chaining**, a fixed sequence | Predictable reviews with several parts. For example, analyze each file, then run a cross-file integration pass. |
| **Dynamic, adaptive decomposition** | Open-ended investigation. For example, "add tests to a legacy codebase": map the structure, find high-impact areas, plan by priority, and adapt as you go. |

Splitting a large review per file avoids **attention dilution** (when one prompt holds too much,
the model spreads its focus thin and misses details).

**How to choose:** if you can write the steps down before you start and they won't change, chain
them; each step's output feeds the next, and each is easy to test on its own. If the next step
depends on what the last one found, let the agent decompose as it goes. A common exam shape mixes
them: a fixed chain whose middle step is an open-ended investigation handed to a subagent.

## 1.7 Sessions: resume and fork

- `--resume <session-name>` continues a named session. (`--resume` and `--continue` are flags on
  Claude Code's command line; L03 covers it.)
- `fork_session` creates independent branches from a shared starting point, for example to compare
  two refactoring approaches. It means: copy the session so far into a new session, and leave the
  original untouched. On the CLI that's `--fork-session` together with `--resume` or `--continue`;
  in the Agent SDK it's the `fork_session` option (`forkSession` in TypeScript; check the current
  docs).
- If the earlier context is **mostly valid**, resume, and **tell the agent which files changed**
  for targeted re-analysis. If the tool results are **stale**, start **fresh with an injected
  structured summary**, which is more reliable.
- **Fork or resume?** Resume when you want to carry on down one path. Fork when you want to try
  two or more paths from the same point without one polluting the other, then keep the winner.
  Neither helps if the shared starting context is itself stale; then start fresh with a summary.

## Worked example (official sample)

In 12% of cases the agent skips `get_customer` and calls `lookup_order` with only a name, which
leads to wrong refunds. **Answer:** a programmatic prerequisite that blocks `lookup_order` and
`process_refund` until there's a verified ID. More system-prompt wording, more few-shot examples or
a routing classifier are all *probabilistic* fixes for a rule that has to be deterministic.

## Traps

- "Raise the iteration cap" or "stop when Claude says it's done".
- "The subagent can see the coordinator's findings." It can't unless you pass them.
- "Put the $500 refund rule in the system prompt." Use a hook.

## Try it, lab 02: the agent loop, subagents and extraction lab (2–3 hours)

Build a coordinator with 2 subagents in the Agent SDK: a real `stop_reason` loop, one
PostToolUse hook, one prerequisite gate, and parallel Task calls. See
[lab 02](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) (all labs:
[`06-Labs/README.md`](../../06-Labs/README.md)).

Done when the prerequisite gate blocks a refund with no verified ID, and both subagent calls appear
in one response.

## Done when

- [ ] You can draw the loop and name the three anti-patterns
- [ ] You can explain why a hook beats a prompt for a $500 cap
- [ ] You can say when to resume and when to start fresh with a summary
- [ ] You scored 80% or more on [CCAR-F practice — choose Domain 1](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F)

**Go deeper:**

- **Deep practice:** [Deep practice 1](deep-practice/01-agentic-architecture-and-orchestration.md), which takes every section of this lesson further (the Claude Code halves of 1.4 and 1.5 are in [deep practice 3](deep-practice/03-claude-code-configuration-and-workflows.md#14-enforced-vs-advice-claude-code-half); what a resumed session still knows (1.7) is in [deep practice 5](deep-practice/05-context-management-and-reliability.md#17-session-resumption-what-a-resumed-session-still-knows)).
- **Official course:** the tool-use and agent parts of the official course *Building with the Claude API* from the [CCAR-F prep-courses list](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) (Anthropic, Tier 1, checked 2026-10-02).
- **Flashcards and drills:** the Domain 1 section of the [flashcards](FLASHCARDS.md) and the 14 Domain 1 drills (1–8, 31–35, 42) in [HARD-DRILLS.md](HARD-DRILLS.md).
- **Charts:** decision charts [3 When the loop stops](deep-practice/decision-charts.md#3-when-does-the-agent-loop-stop), [4 Hook or prompt](deep-practice/decision-charts.md#4-a-rule-must-always-hold-hook-or-prompt), [5a Fixed chain or adaptive plan](deep-practice/decision-charts.md#5a-fixed-chain-of-steps-or-a-plan-that-adapts), [5b What each subagent gets](deep-practice/decision-charts.md#5b-what-does-each-subagent-get) and [6 Resume, fork or fresh](deep-practice/decision-charts.md#6-resume-the-old-session-fork-it-or-start-fresh); sequence diagrams [1 The agent loop](deep-practice/sequence-diagrams.md#1-the-agent-loop-who-sends-what-until-claude-is-done), [2 Coordinator and subagents](deep-practice/sequence-diagrams.md#2-coordinator-and-subagents-what-does-each-helper-see) and [3 A PreToolUse hook](deep-practice/sequence-diagrams.md#3-a-pretooluse-hook-how-does-it-block-a-tool-call).

**Next:** [Deep practice 1](deep-practice/01-agentic-architecture-and-orchestration.md), then [Lesson 4](L04-prompt-engineering-and-structured-output.md).

## Sources

- Official exam guide v1.0, task statements 1.1–1.7 and sample questions (Tier 1).
- Claude Code docs: [subagents](https://code.claude.com/docs/en/sub-agents) (Task renamed Agent)
  and [CLI reference](https://code.claude.com/docs/en/cli-reference) (`--fork-session`) (Tier 1).
- Agent SDK docs: [permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
  (`allowedTools` pre-approves tools; checked 2026-10-07) (Tier 1).
- Claude API [tool-use docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
  for `tool_result` handling (Tier 1).

## Objective modules

For deeper learning and a separate practice/completion check for each objective:

- [Objective 1.1](objectives/objective-1.1.md)
- [Objective 1.2](objectives/objective-1.2.md)
- [Objective 1.3](objectives/objective-1.3.md)
- [Objective 1.4](objectives/objective-1.4.md)
- [Objective 1.5](objectives/objective-1.5.md)
- [Objective 1.6](objectives/objective-1.6.md)
- [Objective 1.7](objectives/objective-1.7.md)

## Decisions in this domain

| Objective | Decision variant and exact repair |
| --- | --- |
| 1.1 | [FV-01 — Confirm the effect before retrying](objectives/objective-1.1.md#variant-fv-01) |
| 1.2 | [FV-02 — Cover dimensions before synthesizing](objectives/objective-1.2.md#variant-fv-02) |
| 1.3 | [FV-03 — Send an attributable handoff](objectives/objective-1.3.md#variant-fv-03) |
| 1.4 | [FV-04 — Bind approval to this action](objectives/objective-1.4.md#variant-fv-04) |
| 1.5 | [FV-05 — Separate prevention from detection](objectives/objective-1.5.md#variant-fv-05) |
| 1.6 | [FV-06 — Choose decomposition by uncertainty](objectives/objective-1.6.md#variant-fv-06) |
| 1.7 | [FV-07 — Resume with fresh permissions](objectives/objective-1.7.md#variant-fv-07) |

**Interpret local practice targets:** any 80% target above is an optional project study heuristic, not a validated mastery threshold or conversion to the official scaled score. Use fresh decisions, explanations and delayed transfer alongside remaining objective gaps.