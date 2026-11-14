# Mechanism clinic — choose the control that meets the requirement

[CCAR-F home](site:exams/ccar-f.html) · [Concept course](concept-course/README.md) · [Last-minute checklist](last-minute-prep.md)

**Setup:** none. Read one explanation, hide it, then explain the decision before checking the answer. Use rounds of three to five checks; return on a different day with the changed constraint. These are original formative exercises, not recalled exam items or additions to the graded question bank. Allow 45–60 minutes in several short sessions.

**Scope:** the saved official guide and its [30 objectives](objectives/README.md) define this site's mapped syllabus. Current product documentation is labeled separately below, checked 2026-10-21. A newer feature is not automatically a new exam objective. Personal experience, a score breakdown or practice accuracy cannot establish a revised blueprint, item counts or predicted scaled marks. The [known diagnostic-coverage limits](learning-journey.md#what-is-still-a-gap) remain.

## 1. First name the guarantee

A legal intake service needs machine-readable fields. **Plain meaning:** asking for a shape, forcing an operation and proving facts are different jobs.

| Requirement | Technical mechanism to consider | What it does not establish |
|---|---|---|
| Final response must follow a supported JSON schema | Current API `output_config.format` | Correct source facts or business completion |
| Generated tool arguments must follow the supported input schema | Current tool definition `strict: true` | That a tool is selected, authorized or executed |
| A tool must be requested | Appropriate `tool_choice` | Correct values, permitted action or ordering of dependencies |
| MCP server returns a declared result shape | Protocol `outputSchema` and `structuredContent`, with client validation | Constrained generation of the model's final answer |
| CLI review needs a machine-readable result | Print-mode JSON output and result schema | Test execution, permission enforcement or correct findings |

**Today, not a replacement exam key:** supported structured-output features constrain shape. Handle refusal and truncation explicitly; don't parse them as ordinary success. Current documentation also describes enum-casing limitations. These qualifications matter even when a request succeeds. Avoid a universal ladder that treats prefill as supported on every model or tool selection as stricter factual validation.

Read [API structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [strict tool inputs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) and [MCP tool results](https://modelcontextprotocol.io/specification/2025-06-18/server/tools). Repair [4.3](objectives/objective-4.3.md).

## 2. Separate a new category, ambiguity and absence

An invoice says “carbon offset,” but the approved categories are equipment and services. This is different from illegible category text or a missing category. Design distinct representable states: a permitted `other` category plus source detail for a clear new value, an explicit review/uncertainty state for ambiguous evidence, and optional/nullable representation for absence when the contract allows it. These labels are **application design choices**, not magic schema keywords. Keep the original text as evidence. Do not silently force the closest category.

A field can be required yet nullable; optional means the key may be omitted. Choose according to the downstream contract. A required non-null field does not create missing evidence: provide a review/error path rather than invent a value. A confidence number does not resolve a contradictory source. Repair [validation 4.4](objectives/objective-4.4.md) and [human review 5.5](objectives/objective-5.5.md).

## 3. Control invocation and dependencies separately

For a supported tool-use request, `auto` permits a text response; `any` requests some tool; selecting a named tool requests that tool. Neither array position nor a prompt reminder creates an executable dependency gate. Model/feature compatibility still applies.

**Trace:** request account lookup → runtime receives its result → validate customer/account binding → enable the dependent operation only when prerequisites pass. A named prerequisite call alone is insufficient: its result can be denied, missing or invalid. Independent reads may run together; a dependent action must wait. Repair [tool choice 2.3](objectives/objective-2.3.md) and [enforcement 1.4](objectives/objective-1.4.md); consult [tool definitions and choice](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools).

## 4. Pick the right configuration layer

| Need | Candidate layer | Close alternative that misses the need |
|---|---|---|
| Shared review conventions | Project `CLAUDE.md` | A personal file does not distribute team guidance |
| Conventions for matching paths | Rules with `paths` globs | Loading every rule everywhere adds irrelevant context |
| Reusable task instructions | Skill | A skill description is not authorization |
| Pre-execution interception | Appropriate pre-tool hook | Post-processing cannot prevent an action already taken |
| Post-result normalization | Appropriate post-tool hook | Natural-language guidance alone does not implement a transformation |
| Tool access policy | Settings permissions and applicable policy | `CLAUDE.md` is not an enforceable access rule |

Check effective precedence and supported behavior. An allow rule, mode, sandbox and downstream service permission are distinct boundaries. Do not assume one control covers all of them. Read [permissions](https://code.claude.com/docs/en/permissions), [settings scope](https://code.claude.com/docs/en/settings) and [hook contracts](https://code.claude.com/docs/en/hooks). Repair [3.1](objectives/objective-3.1.md), [3.3](objectives/objective-3.3.md) and [1.5](objectives/objective-1.5.md).

**Skill fields today:** `context: fork` changes execution context; `argument-hint` helps describe expected arguments; `allowed-tools` affects permission prompting for the skill. Do not interpret it as a universal deny-all policy. CLI `--tools` controls built-in tool availability; it does not control MCP tools. Configure MCP capabilities and their applicable permission rules separately. `--allowedTools` addresses permission prompting, a different concern. Check [skill frontmatter](https://code.claude.com/docs/en/skills) and the [CLI reference](https://code.claude.com/docs/en/cli-reference). Repair [3.2](objectives/objective-3.2.md).

## 5. Configure a review without confusing its three needs

A marketing-code review needs **standards**, **permitted capabilities** and **machine-readable findings**. Supply all three explicitly. Standards describe what a finding is; permission/tool configuration controls execution; output settings control the result envelope. One vague “review carefully” instruction meets none of these precisely.

Current CLI reference: `-p` runs noninteractively; `--max-turns` bounds agentic turns; `--max-budget-usd` limits estimated API spend in print mode and can overshoot. The budget is not an exact billing ceiling. `--output-format json` and `--json-schema` address output. Pin a supported CLI version, inspect its documented envelope and process status, and validate the extracted payload. Do not confuse output volume, permitted tools, turn count and budget. No permission-bypass flag is required by this lesson.

Read [current CLI contracts](https://code.claude.com/docs/en/cli-reference); repair [CI 3.6](objectives/objective-3.6.md). Treat version-specific behavior as current-product guidance, not proof of exam weighting.

## 6. Improve the feedback, not just the number of retries

A generated test ignores a project's fixture conventions. Supply a minimal input, the observed output/failure and the expected behavior. Ask a focused question if the desired behavior is uncertain. Fix one independent issue at a time; group interacting failures when a shared cause requires joint reasoning. Then rerun the relevant check. There is no universal number of examples or retries.

**Changed constraint:** several failures share an incorrect parser contract. Repair the contract and its affected cases together rather than make unrelated cosmetic edits. Repair [iterative refinement 3.5](objectives/objective-3.5.md).

## 7. Choose a plan, then revise it when evidence changes

For a small, well-understood edit, direct execution may be sufficient. For uncertain scope or consequential changes, inspect and plan; place required human approval before execution. Plan mode itself does not establish that an external approval workflow exists. Make the approval state enforceable where the application requires it.

During a repository investigation, a wrapper re-export reveals another dependency. Update the task graph and briefs; do not keep executing a now-incomplete fixed checklist. Parallelize independent investigations, sequence dependencies, and retain one integration owner. Repair [planning 3.4](objectives/objective-3.4.md) and [adaptive decomposition 1.6](objectives/objective-1.6.md).

## 8. Resume work from evidence-bearing state

A legal-document pipeline stops after two of three branches finish. An application-owned manifest can record task IDs, source versions, completed outputs, unresolved work, artifact locations and authorization context. On resume, validate the manifest, recheck permissions/freshness and rerun only invalidated or missing work. A session identifier does not by itself restore every external side effect or specialist artifact. A manifest is a useful design pattern, not a mandatory Claude SDK file format.

Pass specialists the bounded question, relevant findings, source metadata and expected output. Neither a raw transcript dump nor a brief summary is always sufficient; preserve the exact details the next step needs. Repair [sessions 1.7](objectives/objective-1.7.md), [context 5.1](objectives/objective-5.1.md) and [failures 5.3](objectives/objective-5.3.md).

## 9. Verify MCP capability, not just connection

A resource exposes URI-addressed context; a tool exposes an invocable capability, including read queries as well as writes. Do not equate resources with reads and tools with writes. The host chooses how resource context is incorporated. Compare [MCP resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) with [MCP tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).

For Claude Code, check intended configuration scope, credential resolution, trust/approval and tool discovery. A connected server with no expected tool is not ready for the workflow. Use the current server-management/status interface and inspect exposed capabilities before a harmless authorized test. Keep actual secrets outside committed configuration. Transport and version affect setup; consult [current MCP setup](https://code.claude.com/docs/en/mcp). Repair [2.4](objectives/objective-2.4.md).

## 10. Explore narrowly and route review by evidence

Use Glob for candidate paths, Grep for entry points, then Read the relevant definitions and imports/re-exports. Inspect an edit mismatch before replacing a whole file; preserve unrelated changes. Trim excessive tool results at the source when possible, rather than summarize away the only evidence needed next. Retain durable business facts while reducing working context; a sliding window is a retention strategy, not a guarantee against information loss. Repair [2.5](objectives/objective-2.5.md) and [5.4](objectives/objective-5.4.md).

Route human review using consequences, contradictory fields, unfamiliar document types and calibrated evidence. Evaluate slices and sample apparently successful cases for silent errors. A model's confidence alone is not a validated probability. Escalation policy and authority remain application-specific: avoid universal sentiment-only or confidence-only rules. Repair [5.5](objectives/objective-5.5.md).

## Eight checks — commit before opening the explanation

For **choose two**, name the two distinct requirements and justify each selection independently. A generally helpful option can still fail the stated requirement. Keep a paper tally of single-answer versus choose-two checks; these page-local checks do not change stored progress or establish readiness.

<details><summary>1. Choose TWO. A finance extractor must request a particular verification tool and constrain generated arguments. A: select the named tool through tool_choice; B: constrain final text through output_config.format; C: enable strict input-schema generation on the tool; D: declare outputSchema on the MCP server result.</summary>

**A and C.** Selection and generated argument shape are separate needs. B targets final text; D targets server results. Neither grants execution authority. **Change:** only final text needs a schema; choose its output mechanism instead. Repair sections 1 and 3.

</details>

<details><summary>2. Choose TWO. A legal repository needs shared review conventions and an enforced prohibition on a file-changing action. A: scope conventions through a personal memory file; B: distribute conventions through project guidance; C: normalize generated findings in a post-tool hook; D: enforce the action rule in effective permission policy.</summary>

**B and D.** Shared guidance distributes standards; policy constrains the prohibited action. A has the wrong audience; C acts after a result and does not prevent the action. **Change:** the convention applies only to matching files; consider path-scoped rules. Repair section 4.

</details>

<details><summary>3. One best. A clear invoice category is outside the approved enum, whose contract permits other plus source detail. A: extend the enum automatically on each observation; B: select other and retain the source detail; C: use null to represent every unfamiliar category; D: select the nearest permitted enum by semantic similarity.</summary>

**B.** It uses the explicit contract without losing the source. A changes a controlled vocabulary without approval; C confuses novelty with absence; D changes meaning. **Change:** evidence is absent or unreadable; use the corresponding absence or review state. Repair section 2.

</details>

<details><summary>4. Choose TWO. A CI review must run without interaction and bound agentic turns. A: request a JSON envelope and output schema; B: invoke the documented print execution mode; C: cap estimated API spend in the run budget; D: set the documented agentic-turn limit.</summary>

**B and D.** A controls representation; C addresses a different stopping constraint. **Change:** the requirement is estimated spend instead of turns; examine the budget control and overshoot caveat. Repair section 5.

</details>

<details><summary>5. One best. Two analysis artifacts survived an interruption, but access policy changed. A: resume worker sessions and reuse their prior authorization; B: reload the full transcript as the authoritative operation ledger; C: validate artifacts, reauthorize and recompute invalidated work; D: discard completed artifacts and rerun every branch from scratch.</summary>

**C.** A preserves stale authority; B confuses conversation with authoritative operation state; D discards potentially valid completed work. **Change:** a source version changed too; invalidate dependent outputs. Repair section 8.

</details>

<details><summary>6. One best. An MCP server connects, but its expected query tool is absent. A: treat transport status as proof of tool availability; B: revise the prompt with the expected tool description; C: increase the model context budget for the server; D: inspect discovery, configuration scope and approval.</summary>

**D.** Transport health, prompt context and capability discovery are distinct. B cannot expose an unavailable tool; C does not repair registration or approval. **Change:** the needed item is URI context rather than a tool; inspect resource support. Repair section 9.

</details>

<details><summary>7. One best. Generated tests repeatedly misuse a fixture whose required behavior is known. A: supply the failing example and expected fixture contract; B: load all repository files into the next model request; C: normalize test output with a post-execution hook only; D: rerun independent reviewers without changing their criteria.</summary>

**A.** It supplies targeted behavioral evidence. B adds broad context without isolating the error; C can change presentation without fixing assertions; D repeats the missing specification. **Change:** several failures share one parser defect; repair the interacting cause and retest affected cases together. Repair section 6.

</details>

<details><summary>8. One best. A wrapper reveals an unexamined dependency during a scoped review. A: retain the original fixed partition to preserve task order; B: revise subtasks and briefs within the approval boundary; C: fork the full conversation into each existing worker; D: persist the finding without updating task coverage.</summary>

**B.** A leaves a coverage gap; C does not assign ownership or revise dependencies; D records evidence but leaves the plan incomplete. **Change:** the finding requires an unapproved consequential action; obtain its required authorization while continuing independent permitted work. Repair section 7.

</details>

## Finish with transfer, not memorized answers

Draw one request with actors labeled **model → runtime → tool/server → authoritative evidence**. Explain a mechanism, reject its nearest alternative and change a constraint. Repeat later in another application context. Correct answer letters and immediate re-tests are not proof of durable transfer.

Continue through [Lab 08](../../06-Labs/08-CCAR-F-architecture-decisions/README.md), [CI walkthrough](scenario-walkthroughs/WT-05-claude-code-ci-cd.md), [extraction walkthrough](scenario-walkthroughs/WT-06-structured-data-extraction.md), [targeted practice](site:practice/index.html?exam=CCAR-F) and [recall checklist](last-minute-prep.md). Use the practice app's objective selector; this clinic adds no graded-bank items. [Back to CCAR-F home](site:exams/ccar-f.html).

## Practise with competing constraints

Continue with the [architecture choice workshop](choice-workshop.md): six original application cases, 12 decisions, plausible alternatives and changed constraints. Each answer explains the rejected options and links to objective repair.


<a id="verified-exercise-sources"></a>
## Verify the mechanism behind an exercise

Checked 22 October 2026 against the primary pages below. These are current-product notes, alongside the saved exam blueprint. A newer product feature does not prove an exam objective changed. The new [objective proof tasks](objectives/README.md) use fictional data and explicit application policies; running an offline check does not prove a live API integration or exam readiness.

| Decisions | Primary reference | Remember the boundary |
| --- | --- | --- |
| 1.1, 2.2 | [Messages API: Handle client tool calls; tool_result blocks](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | No SDK execution or business settlement is established by a response. |
| 1.1 | [Messages API: max_tokens; incomplete tool-use blocks](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons) | end_turn ends generation, not an application transaction. |
| 2.1, 2.3 | [Messages API: Specifying client tools; descriptions and selection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) | Tool count alone is not a universal routing limit; held-out routing improvement must be measured. |
| 4.3, 4.4 | [Messages API: JSON outputs; strict tool use; limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | Source truth and business validity remain application checks. No new scored key is inferred. |
| 4.5, 5.3 | [Message Batches API: Retrieving results; best practices](https://platform.claude.com/docs/en/build-with-claude/batch-processing) | Retry classification in exercises is a stated synthetic application policy, not a universal retry rule. |
| 5.1, 5.4 | [Messages API: Compaction overview](https://platform.claude.com/docs/en/build-with-claude/compaction) | Fixture state manifests are application artifacts; caching is a separate mechanism. |
| 3.2 | [Claude Code: Frontmatter; pre-approve tools for a skill](https://code.claude.com/docs/en/skills) | Do not generalize Claude Code frontmatter to every skill upload/API surface. Actual restrictions require applicable deny/disallowed-tool policy. |
| 1.5 | [Claude Code hooks: PreToolUse; PostToolUse; decision control](https://code.claude.com/docs/en/hooks) | A post-result flag cannot undo an already executed mutation; hook coverage must be tested in the exact surface. |
| 3.1, 3.3 | [Claude Code memory: Path-specific rules](https://code.claude.com/docs/en/memory) | Instruction loading is not an authorization boundary or guaranteed revocation. |
| 2.4 | [Claude Code MCP: Installation scopes; project scope; environment expansion](https://code.claude.com/docs/en/mcp) | Discovery/configuration is not evidence that a resource has entered model context. |
| 1.2, 1.3 | [Claude Agent SDK: Context isolation; inheritance](https://code.claude.com/docs/en/agent-sdk/subagents) | Fixture deliberately specifies no inherited history; do not claim every runtime starts without context. |
| 2.2, 2.4 | [MCP specification 2025-11-25: Calling Tools; Error Handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | Empty successful search is not the same as an unavailable service or permission denial. |
| 1.6, 3.4, 4.6 | [Anthropic engineering: Workflows versus agents; simplicity](https://www.anthropic.com/research/building-effective-agents) | No mandatory multi-agent design or universal complexity threshold. |
| 2.1, 4.1, 4.2, 5.5 | [Claude Platform evaluation guidance: Success criteria; evaluation examples](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Synthetic holdout/routing counts are learning evidence, not certification readiness or calibrated pass probability. |

For each exercise, record the decision, why it fits, the closest rejected alternative, concrete evidence and remaining unknowns. Retry/approval deadlines and acceptance thresholds supplied by a fixture belong to that fictional application. They are not universal Claude defaults.