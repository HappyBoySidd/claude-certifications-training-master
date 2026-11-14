# Deep practice 5: context management and reliability

**Picture the application:** A support conversation grows long while a research report accumulates results from several sources. The final response still needs the right amounts, current issue status and traceable evidence. Start with those business facts, then use the mechanisms below to inspect context loss, failures, recovery and source attribution.

This page covers Domain 5 of CCAR-F, context management and reliability, one task statement at a time. It goes
deeper than [Lesson 5](../L05-context-management-and-reliability.md): each section gives the core idea, how it works under the hood,
the look-alike wrong answers, a worked example and a one-line exam reflex. Read the lesson first.
Objective lessons for this page: [1.7](../objectives/objective-1.7.md) · [5.1](../objectives/objective-5.1.md) · [5.3](../objectives/objective-5.3.md) · [5.4](../objectives/objective-5.4.md) · [5.6](../objectives/objective-5.6.md).

TS 5.2 (escalation) is in [deep practice 1](01-agentic-architecture-and-orchestration.md). TS 5.5 (human review and confidence) is in
[04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md).
Section 1.7 (what a resumed session still knows) comes last, because it belongs to Domain 1.

---

## 5.1 Preserving context in long interactions

Lesson: [L05 section 5.1](../L05-context-management-and-reliability.md#51-keeping-the-facts-that-matter-in-long-conversations) · Objective: [5.1](../objectives/objective-5.1.md)

**Exam wording:** `Task Statement 5.1: Manage conversation context to preserve critical information across long interactions`

### Core idea

Claude's API has **no memory**. Every call starts from zero. The only thing Claude knows is what you send
in that call. So your app must send the whole conversation every time, and it must protect the exact
facts (amounts, dates, order numbers) from getting blurred when the conversation gets long.

### How it works under the hood

- **Stateless.** Doc wording: "The Messages API is stateless, which means that you always send the full
  conversational history to the API" [messages]. Your code keeps the `messages` list and appends each
  assistant reply and each user turn (including `tool_result` blocks) before the next call. Earlier turns
  can even be synthetic `assistant` messages you wrote [messages].
- Exam knowledge wording: "The importance of passing complete conversation history in subsequent API
  requests to maintain conversational coherence" [guide, TS 5.1].
- **Summaries lose numbers.** Exam knowledge: "Progressive summarization risks: condensing numerical values,
  percentages, dates, and customer-stated expectations into vague summaries" [Guide]. "$212.40 refund on
  order ORD-88123 promised by Friday" becomes "customer wants a refund".
- **Fix: a case-facts block.** Exam skill: extract "transactional facts (amounts, dates, order numbers,
  statuses) into a persistent "case facts" block included in each prompt, outside summarized history"
  [Guide]. The summary may shrink. The facts block never does.
- **Lost in the middle.** Exam knowledge: models "reliably process information at the beginning and end of
  long inputs but may omit findings from middle sections" [Guide]. Fix: put a key-findings summary **at
  the start** and use clear section headers [Guide].
- **Trim tool output.** Exam knowledge: tool results consume tokens "disproportionately to their relevance
  (e.g., 40+ fields per order lookup when only 5 are relevant)" [Guide]. Keep only the fields you need
  before appending.
- **Upstream agents return structure.** When the downstream agent has a small budget, have upstream agents
  return "key facts, citations, relevance scores" instead of "verbose content and reasoning chains"
  [Guide].

```python
case_facts = {"customer_id": "C-4471", "order": "ORD-88123", "refund_amount": 212.40,
              "promised_by": "2026-10-09", "status": "approved_pending_payout"}
system = BASE_PROMPT + "\n<case_facts>\n" + json.dumps(case_facts) + "\n</case_facts>"
resp = client.messages.create(model=M, system=system,
                              messages=summarized_history + recent_turns,   # full history, every call
                              max_tokens=1024, tools=TOOLS)
```

### Look-alikes

1. **"Claude remembers the session, so only send the new message."** No. The API is stateless. (Claude
   Code and the Agent SDK **store** sessions for you, but they still send history to the model on every
   call; the plain Messages API does not store anything.)
2. **"Summarize the whole history every 10 turns to save tokens."** Fine for chatter, but on its own it
   blurs the exact numbers. Pair it with a case-facts block.
3. **"Use a model with a bigger context window."** Doesn't fix lost-in-the-middle or blurred summaries.
4. **"Keep every field from every lookup in case it's useful later."** Fills context with noise.

### Worked example (Scenario: customer support resolution agent)

A 45-minute chat covers two orders. By turn 30, the agent says the refund is "about $200" and mixes up
which order was damaged. Fix: keep a `case_facts` block per issue (order ID, amount, status, promise date)
in the system prompt on every call; trim `lookup_order` results to the 5 return-relevant fields; keep the
summarized history for the chatter.

### Exam reflex

**The API remembers nothing: send the full history, pin exact facts in a case-facts block, trim tool output.**

---

## 5.3 Error propagation across multi-agent systems

Lesson: [L05 section 5.3](../L05-context-management-and-reliability.md#53-passing-errors-between-agents) · Objective: [5.3](../objectives/objective-5.3.md)

**Exam wording:** `Task Statement 5.3: Implement error propagation strategies across multi-agent systems`

### Core idea

When a helper agent hits a problem, it should fix what it can by itself, and pass up **the rest with
details**: what failed, what it tried, what it already got, and what else could work. Never hide a failure.
Never kill the whole job over one failure.

### How it works under the hood

- Exam knowledge wording: "Structured error context (failure type, attempted query, partial results,
  alternative approaches)" enables "intelligent coordinator recovery decisions" [guide, TS 5.3].
- The two anti-patterns, exam wording: "silently suppressing errors (returning empty results as success)
  or terminating entire workflows on single failures" [Guide].
- "Generic error statuses ("search unavailable") hide valuable context from the coordinator" [Guide].
- Access failure vs valid empty result: same rule as 2.2 (see [deep practice 2](02-tool-design-and-mcp-integration.md)).
- Local recovery first: subagents handle transient failures themselves and "only propagate errors they
  cannot resolve, including what was attempted and partial results" [Guide].
- **Coverage notes in the output.** Exam skill: synthesis output "with coverage annotations indicating
  which findings are well-supported versus which topic areas have gaps due to unavailable sources" [Guide].
- Anthropic's research system: letting "the agent know when a tool is failing and letting it adapt works
  surprisingly well", and they built it to "resume from where the agent was when the errors occurred"
  [research-system].

**A good subagent error report (practice, not doc):**

```json
{"status": "partial", "failure_type": "timeout", "attempted": "search: 'EU AI Act enforcement 2026' on news API (3 tries, backoff)",
 "partial_results": [{"claim": "...", "source_url": "..."}],
 "alternatives": ["try the legal-database source", "narrow to 2026-Q3"],
 "coverage_gap": "No enforcement data after July 2026"}
```

### Look-alikes

1. **Subagent returns `[]` as success after a timeout.** Coordinator thinks "no news exists". Silent
   suppression.
2. **Coordinator aborts the whole report when one of five searches fails.** Over-reaction; keep the other
   four and annotate the gap.
3. **Subagent returns "search unavailable".** Too generic; no retry decision possible.
4. **Subagent passes every transient error up to the coordinator.** It should retry those locally first.

### Worked example (Scenario: multi-agent research system)

Five search subagents run; one gets rate-limited. Good design: it retries with backoff, still fails, then
returns `failure_type`, the query it tried, its two results so far, and an alternative source. The
coordinator re-delegates to the alternative source. The final report says "Regulatory section: limited
coverage, primary source unavailable".

### Exam reflex

**Recover locally, propagate the rest with type, attempt, partial results and alternatives; never hide it, never abort everything.**

---

## 5.4 Context in large codebase exploration

Lesson: [L05 section 5.4](../L05-context-management-and-reliability.md#54-exploring-a-large-codebase) · Objective: [5.4](../objectives/objective-5.4.md)

**Exam wording:** `Task Statement 5.4: Manage context effectively in large codebase exploration`

### Core idea

Long exploration fills the context with search output. Claude starts to forget the specific things it
found and talks about "typical patterns" instead. Three fixes: send noisy searches to **subagents** that
return short summaries; write key findings to a **scratchpad file** that survives; and **`/compact`** when
context fills.

### How it works under the hood

- **The symptom**, exam wording: "models start giving inconsistent answers and referencing "typical
  patterns" rather than specific classes discovered earlier" [guide, TS 5.4].
- **Subagents isolate noise.** Doc: intermediate tool calls and results "stay inside the subagent; only its
  final message returns to the parent" [sdk-subagents]. Anthropic: a subagent may use "tens of thousands of
  tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)"
  [context-eng]. Exam skill example tasks: "find all test files," "trace refund flow dependencies" [Guide].
- **Scratchpad files.** Exam knowledge: "The role of scratchpad files for persisting key findings across
  context boundaries" [Guide]. Anthropic calls this structured note-taking, like "your custom agent
  maintaining a NOTES.md file" [context-eng].
- **What survives `/compact`.** Doc: "Project-root CLAUDE.md survives compaction: after `/compact`, Claude
  re-reads it from disk and re-injects it into the session." An instruction given "only in conversation"
  can disappear [cc-memory]. Compaction summarizes the conversation, so details only in chat may be lost. A
  scratchpad **file** is on disk, so Claude can read it again after `/compact` or in a new session.
  (Survival of a scratchpad file is from it being on disk; Claude must be told to re-read it: practice,
  consistent with [cc-memory] and [context-eng].)
- **`/compact`**, exam skill: "Using /compact to reduce context usage during extended exploration sessions
  when context fills with verbose discovery output" [Guide].
- **Phase summaries.** Summarize one phase's findings "before spawning sub-agents for the next phase,
  injecting summaries into initial context" [Guide].
- **Crash recovery with manifests.** Exam knowledge: "each agent exports state to a known location, and the
  coordinator loads a manifest on resume" [Guide]. Example: each agent writes `state/<agent>.json`; the
  coordinator keeps `state/manifest.json` listing done and pending tasks; on restart it loads the manifest
  and injects each agent's state into its prompt.
- **Search order** that keeps context small: Glob, then Grep file list, then narrowed Grep content, then
  Read with `offset`/`limit` [cc-tools]. Details in [deep practice 2, 2.5](02-tool-design-and-mcp-integration.md).

### Look-alikes

1. **"Use a bigger context window."** Delays the problem; doesn't remove noise.
2. **"Restart the session when answers get vague."** Loses everything not written down. Write a
   scratchpad first, or delegate the noisy part.
3. **"Do every search in the main agent so it sees everything."** That's what floods it.
4. **"Fork the session to explore."** A fork carries the full history; for isolating noisy output you
   want a fresh subagent with a short summary back.
5. **"Rely on `/compact` alone."** It helps, but a summary can drop specific class names; pair it with a
   scratchpad.

### Worked example (Scenario: developer productivity with Claude)

First day of learning a 2,000-file monorepo. After two hours Claude says "refunds are probably handled by a
typical service layer", though it found `RefundOrchestrator` earlier. Fix: (1) Claude writes
`notes/exploration.md` with entry points, key classes (`RefundOrchestrator`, `LedgerClient`) and open
questions, and re-reads it before each new question; (2) "trace refund flow dependencies" goes to a
subagent that returns a 1-page summary; (3) `/compact` when the context fills with search output.

### Exam reflex

**Noisy searches go to subagents, findings go in a scratchpad file, `/compact` when full; never "bigger window".**

---

## 5.6 Provenance and uncertainty in multi-source synthesis

Lesson: [L05 section 5.6](../L05-context-management-and-reliability.md#56-provenance-and-uncertainty) · Objective: [5.6](../objectives/objective-5.6.md)

**Exam wording:** `Task Statement 5.6: Preserve information provenance and handle uncertainty in multi-source synthesis`

### Core idea

Every claim should carry its source, all the way to the final report. When sources disagree, show both
with their sources. Don't quietly pick one. And record dates, because "different numbers" might just be
"different years".

### How it works under the hood

Exam wording [guide, TS 5.6]:

- Knowledge: "source attribution is lost during summarization steps when findings are compressed without
  preserving claim-source mappings".
- Skill: subagents output "structured claim-source mappings (source URLs, document names, relevant
  excerpts) that downstream agents preserve through synthesis".
- Conflicts: "annotating conflicts with source attribution rather than arbitrarily selecting one value".
  Document analysis completes "with conflicting values included and explicitly annotated, letting the
  coordinator decide how to reconcile".
- Dates: require "publication or data collection dates in structured outputs to enable correct temporal
  interpretation".
- Report structure: "explicit sections distinguishing well-established findings from contested ones".
- Format by type: "financial data as tables, news as prose, technical findings as structured lists".

Anthropic's research system adds a final citation pass (a `CitationAgent`) so "all claims are properly
attributed to their sources" [research-system]. This final pass is an extra check on top of structured
claim-source mappings, not a replacement for them; on the exam, pick the mappings.

```json
{"claim": "Global AI-music market size", "values": [
  {"value": "$3.9B", "source": "Report A", "url": "...", "published": "2025-02", "method": "survey"},
  {"value": "$6.2B", "source": "Report B", "url": "...", "published": "2026-06", "method": "revenue model"}],
 "status": "contested", "note": "Different years and methods; not necessarily a contradiction."}
```

### Look-alikes

1. **"Pick the most recent / most credible number and drop the other."** Arbitrary selection; the exam
   wants both, annotated.
2. **"Average the two figures."** Invents a number no source said.
3. **"Summarize findings into clean prose first, add citations at the end."** Compression already lost the
   claim-source links.
4. **"Render everything as bullet points for consistency."** The guide wants format by content type.

### Worked example (Scenario: multi-agent research system)

Two credible sources give different market sizes. The analysis subagent includes both with source, date and
method, and marks the item `contested`. The coordinator sees one is 2025 data and one is 2026 data, so the
report shows a growth trend rather than a contradiction, in a table, with both citations.

### Exam reflex

**Claims carry sources and dates end to end; conflicts are shown with attribution, never silently resolved.**

---

## 1.7 Session resumption: what a resumed session still knows

Lesson: [L01 section 1.7](../L01-agentic-architecture-and-orchestration.md#17-sessions-resume-and-fork) · Objective: [1.7](../objectives/objective-1.7.md)

**Exam wording:** `Task Statement 1.7: Manage session state, resumption, and forking`

Flags and SDK options are in [deep practice 1, 1.7](01-agentic-architecture-and-orchestration.md). This part is about **what a resumed
session still knows** and when not to resume.

### Core idea

Resuming brings back the old conversation, **including old tool results**. If the code changed since then,
those old results are wrong, and Claude doesn't know it. So either tell it exactly what changed, or start a
new session with a clean summary.

### How it works under the hood

- `--continue` / `-c`: the most recent conversation in this directory. `--resume` / `-r`: a specific
  session by ID or name. `--fork-session`: a new session ID with the old history [cli]. SDK: `continue`,
  `resume` with a `session_id`, and `fork_session` / `forkSession` [sdk-sessions].
- In CI: plain `claude --continue` skips sessions made with `claude -p`, but "`claude -p --continue`
  includes `-p`, SDK, and `/loop` sessions" [cli].
- Exam knowledge wording [guide, TS 1.7]:
  - "The importance of informing the agent about changes to previously analyzed files when resuming
    sessions after code modifications"
  - "Why starting a new session with a structured summary is more reliable than resuming with stale tool
    results"
- Exam skill wording: "Choosing between session resumption (when prior context is mostly valid) and
  starting fresh with injected summaries (when prior tool results are stale)" and "Informing a resumed
  session about specific file changes for targeted re-analysis rather than requiring full re-exploration"
  [Guide].

**The decision:**

| What changed since the last session? | Move |
|---|---|
| Nothing, or very little | `--resume <name>` and continue. |
| A few known files | `--resume <name>`, then say: "`auth/session.py` and `auth/tokens.py` changed (commit abc123). Re-read only those and update your findings." |
| A lot (big refactor, branch switch) | New session. Inject a structured summary of the earlier findings. Let Claude re-read what it needs. |
| Want to try two directions | Fork (see deep practice 1). |

**Practice pattern** (practice, not doc): find what changed with `git diff --name-only <last-reviewed-commit>`
or file hashes, and list those files in the resume message.

### Look-alikes

1. **"Resume and ask Claude to re-check everything."** Full re-exploration wastes time and context; the
   exam wants targeted re-analysis of named files.
2. **"Resume; Claude will notice the files changed."** It won't. Its old `Read` results look current to it.
3. **"`--continue` to get yesterday's `auth-audit` session."** Only if it's the most recent one in this
   directory. Use `--resume auth-audit`.
4. **"Always start fresh to be safe."** Throws away valid context when little changed.

### Worked example (Scenario: Claude Code for continuous integration)

A PR review session found 6 issues. The developer pushes a new commit touching 2 files. Right move: resume
the review session and tell it which 2 files changed, so it re-checks just those and doesn't re-post the
other comments. Twist: the developer rebased onto a main branch that moved 300 files. Now prior results
are stale: start a fresh session with a summary of the 6 earlier findings.

### Exam reflex

**Mostly valid: resume and name the changed files; mostly stale: fresh session plus summary.**

---

## Not covered here on purpose

- TS 5.2 escalation and ambiguity: [01-agentic-architecture-and-orchestration.md](01-agentic-architecture-and-orchestration.md).
- TS 5.5 human review and confidence calibration: [04-prompt-engineering-and-structured-output.md](04-prompt-engineering-and-structured-output.md).
- Session flags and fork mechanics: [deep practice 1, 1.7](01-agentic-architecture-and-orchestration.md).

---

## Sources (citation keys)

All Tier 1, checked 2026-10-06:
[messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) ·
[sdk-subagents](https://code.claude.com/docs/en/agent-sdk/subagents) ·
[sdk-sessions](https://code.claude.com/docs/en/agent-sdk/sessions) ·
[cli](https://code.claude.com/docs/en/cli-reference) ·
[cc-memory](https://code.claude.com/docs/en/memory) ·
[cc-tools](https://code.claude.com/docs/en/tools-reference) ·
[context-eng](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ·
[research-system](https://www.anthropic.com/engineering/multi-agent-research-system) ·
[Guide] = the official CCAR-F exam guide v1.0 (July 2026, Anthropic).

## Not confirmed

- A scratchpad file surviving `/compact` (5.4) is practice. The doc confirms only that the project-root `CLAUDE.md` is re-read after `/compact`. The file stays because it's on disk, and Claude must be told to re-read it.
- Finding changed files with `git diff --name-only` before resuming (Session resumption) is practice, not a doc rule.
- The subagent error report shape (5.3) and the conflict record shape (5.6) are practice examples built from the exam wording.

**Next:** that's the last lesson in the study order. Go back to the [CCAR-F lessons page](../README.md), then run the [simulations](../../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md).