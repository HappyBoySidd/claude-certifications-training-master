# Architecture decisions: listen and converse

Reader-ready original text scripts, not recorded audio. Each contains a scene, question, pause, changed scene, second pause and closed debrief. These reuse local practice scenes; exposure must not count as unseen diagnostic success.

## FV-01 — Confirm the effect before retrying

**Scene and first decision:** A claims agent receives stop_reason=tool_use with two read-only calls, IDs u1 and u2. Both calls finish. What should its Messages orchestration loop do next?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A settlement agent receives end_turn after a write returned status=unknown. There are no pending tool calls, but business completion has not been established. What should the application do?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Return each result with its matching tool_use_id and send the next model request. The protocol requires results for the requested calls before the next model iteration.

**Answer to this exact scene:** End this model loop and check operation status through the application recovery path before retrying the write. end_turn ends the model turn, while an unknown business effect still needs reconciliation.

**Base choice:** A support agent has one refund tool call pending. Return tool_result with its matching tool_use_id and continue the conversation; keep the business transaction status separately.

**Changed constraint and recovery:** The model returns end_turn, but the payment request timed out. Stop the model loop; do not describe the refund as committed.

**Failure:** A network timeout leaves operation r-17 unknown. Query r-17 status or reconcile by idempotency key before sending another refund.

**Nearest alternative:** A blind refund retry can duplicate a committed transaction. Model termination is not proof of settlement.

**Conditional cue:** Stop the loop on its signal; settle the effect from its receipt.

**Proof:** Inspect `stop_reason=tool_use; pending_id=t17; operation_id=r17; business_status=unknown` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.1.md#variant-fv-01).

</details>

## FV-02 — Cover dimensions before synthesizing

**Scene and first decision:** A law firm requests a vendor comparison covering retention, jurisdiction and operational recovery. Its draft decomposition investigates only three vendors’ prices. What is the best correction?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A lawyer asks for the current retention period of one named policy. One read-only lookup returns the authoritative clause and date. What is the best orchestration choice?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Have a coordinator allocate the missing comparison dimensions, collect attributed findings and check coverage. Dimension-based coverage repairs the omitted requirements.

**Answer to this exact scene:** Use the bounded single-agent lookup and return the supported answer. The bounded question is already supported without specialist coordination overhead.

**Base choice:** A legal team compares three vendors on evidence retention, integration cost and deployment permissions. Assign dimensions, require source-tagged findings and let the coordinator integrate the comparison.

**Changed constraint and recovery:** The task becomes one known price lookup from an authorized source. One scoped agent is sufficient; decomposition overhead adds no evidence.

**Failure:** Cost returns, but retention is missing. Re-delegate retention with an explicit gap; do not publish a complete comparison.

**Nearest alternative:** Assigning one vendor to each specialist can hide inconsistent criteria unless the return contracts enforce the same dimensions.

**Conditional cue:** Split by evidence need; count coverage before conclusion.

**Proof:** Inspect `coverage={retention:pending,cost:complete,permissions:complete}; owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.2.md#variant-fv-02).

</details>

## FV-03 — Send an attributable handoff

**Scene and first decision:** A synthesis specialist is isolated from its parent. Earlier agents found campaign claims and conflicting source dates. Which handoff should the coordinator provide?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** Two independent channel audits must finish before synthesis; neither needs the other’s output. What should the coordinator do at dispatch?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Supply the question, scoped findings, source locators, dates and expected output contract explicitly. Explicit context and attribution enable an isolated specialist to reason from prior evidence.

**Answer to this exact scene:** Dispatch both independent investigations together with bounded scopes and quality criteria. Independent investigations can run in parallel without inventing a dependency.

**Base choice:** A marketing specialist checks audience evidence. Send the precise question, permitted data, exclusions, cited upstream findings and output contract, not a reference to another unseen chat.

**Changed constraint and recovery:** New consent evidence invalidates the audience assumption. Send the changed evidence and require a revised conclusion.

**Failure:** The specialist claims it used a result never included in its brief. Reject that claim and resend the bounded evidence packet.

**Nearest alternative:** Shared task naming is not shared conversation context; a bare “use the earlier findings” instruction is insufficient.

**Conditional cue:** Send scope, source and shape; never assume shared memory.

**Proof:** Inspect `brief={question:segment_fit,scope:consented_records,evidence:[source:CRM42],return:[finding,source,limits]}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.3.md#variant-fv-03).

</details>

## FV-04 — Bind approval to this action

**Scene and first decision:** A transfer approval is bound to account A, amount 800 and proposal version 3. The agent changes the destination and produces version 4. What should the execution gate do?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A bank customer explicitly requests a human while a transfer dispute is unresolved. The receiving officer cannot read the transcript. What should the agent do?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Reject execution until the changed proposal receives current scoped authorization. Authorization for a different proposal cannot justify the new effect.

**Answer to this exact scene:** Escalate with verified identity, unresolved issue, evidence, proposal version and operation status. A complete handoff lets the human continue without guessing current state.

**Base choice:** A finance support workflow proposes a 40-unit credit for account A and proposal v2. Trusted verification, scope and current approval are checked by the action handler before the effect.

**Changed constraint and recovery:** The target changes to account B or amount changes to 80. Invalidate the prior approval and request the newly scoped authorization.

**Failure:** Verification expires between draft and execute. Reject the protected action and hand off the complete case with blocked status.

**Nearest alternative:** A prompt reminding Claude to verify cannot enforce the backend boundary. Read-only investigation follows its own access policy.

**Conditional cue:** Bind identity, scope and version; changed target means new gate.

**Proof:** Inspect `gate={account:A,proposal:v2,amount:40,verified:true,approval:current}; requested={account:B,proposal:v2}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.4.md#variant-fv-04).

</details>

## FV-05 — Separate prevention from detection

**Scene and first decision:** Two document tools return ISO dates and epoch timestamps. Raw evidence must remain auditable, and no external write is involved. Which mechanism best normalizes what the model receives?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A records deletion must never execute when a legal hold is active. The current proposal checks only after the delete tool succeeds. Which design fixes the timing?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Normalize returned data in a post-tool transformation while preserving raw values and provenance. Post-tool normalization is appropriate for already returned read data.

**Answer to this exact scene:** Check the hold in a pre-action application gate or blocking pre-tool hook before deletion. A prevention requirement must be enforced before the side effect.

**Base choice:** A fictional service normalizes a successful date result after the tool returns while retaining the original value and parse status.

**Changed constraint and recovery:** The requirement becomes preventing an irreversible account mutation. Move the authorization check before execution, in the application or supported pre-tool control.

**Failure:** A post-result check finds a bad write already happened. Record the effect and invoke reviewed compensation or escalation; result replacement does not undo it.

**Nearest alternative:** A post-action hook can change model-visible output where supported, but cannot retroactively block the completed effect.

**Conditional cue:** Before prevents; after detects; retain raw evidence.

**Proof:** Inspect `trace=proposal -> precheck -> execute -> effect -> postcheck; raw_date=03/04; locale=unknown` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.5.md#variant-fv-05).

</details>

## FV-06 — Choose decomposition by uncertainty

**Scene and first decision:** A campaign compliance review always checks each file against three known criteria and then checks cross-file consistency. Which decomposition fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A campaign launch failure has an unknown cause; each log finding may expose a new dependency. Which decomposition fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Use predictable per-file review stages followed by a cross-file integration pass. Known stages support a fixed review chain plus integration.

**Answer to this exact scene:** Start an adaptive investigation that expands tasks as evidence reveals relevant dependencies. Unknown causes require investigation that responds to discoveries.

**Base choice:** A government intake follows a known sequence: validate, classify, route. Use an explicit workflow with defined outputs and stop states.

**Changed constraint and recovery:** The task becomes an open-ended investigation with unknown evidence paths. Use bounded adaptive decomposition and review discovered gaps.

**Failure:** After ten iterations the agent has activity but no evidence for one requirement. Stop or re-plan using the coverage ledger, not iteration count alone.

**Nearest alternative:** Multiple agents do not cure an unclear completion contract. Fixed steps are easier to test when the process is known.

**Conditional cue:** Known path: workflow; unknown path: bounded discovery.

**Proof:** Inspect `steps=[validate,classify,route]; done={valid:true,route_assigned:true}; missing=[]` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.6.md#variant-fv-06).

</details>

## FV-07 — Resume with fresh permissions

**Scene and first decision:** A resumed contract session points to an older file revision; the repository revision and user permissions changed overnight. What must happen before relying on its findings?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** An analyst wants to compare two independent interpretations from the same verified baseline without overwriting the original investigation. Which session approach fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Reacquire changed files and permissions, retaining only still-valid evidence. Resumption preserves conversation state, not the freshness of external evidence.

**Answer to this exact scene:** Fork from the baseline and keep branch conclusions separately attributable. Forking supports alternative exploration while retaining the shared starting point.

**Base choice:** An interrupted legal repository investigation resumes with source pointers and a checkpoint. Re-read changed files and revalidate permissions before continuing.

**Changed constraint and recovery:** The learner wants an alternative investigation without replacing the existing trajectory. Fork the session, but revalidate the same mutable assumptions.

**Failure:** A stored path was renamed and prior access revoked. Reacquire current evidence; do not trust an old tool result just because the session resumed.

**Nearest alternative:** Resume and fork preserve or branch state; neither renews authorization nor makes stale evidence current.

**Conditional cue:** Resume the reasoning; refresh the mutable evidence.

**Proof:** Inspect `checkpoint={commit:abc,paths:[policy.md],permissions_checked:old}; current_commit:def` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-1.7.md#variant-fv-07).

</details>

## FV-08 — Make capabilities distinguishable

**Scene and first decision:** A payment catalog has tools named payment_action1 and payment_action2; one drafts, one executes. Their descriptions omit side effects. What change best reduces confusion?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A redesign proposes one universal execute tool that accepts arbitrary action strings. The application must enforce separate read and payment capabilities. Which choice best preserves the boundary?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Give draft and execute distinct names, inputs, side-effect descriptions and prerequisite contracts. Distinct tool contracts make operational purpose and requirements explicit.

**Answer to this exact scene:** Keep a separate scoped execution capability with an application authorization check. A narrow execution boundary can be enforced independently of model selection.

**Base choice:** A support catalog separates get_balance, draft_credit and execute_credit. Descriptions specify read versus proposal versus mutation, required scope and return status.

**Changed constraint and recovery:** Two tools both say “manage account.” Rename them and tighten schemas/descriptions so capability boundaries are clear.

**Failure:** Claude picks execute_credit for a lookup. Reject the call at the handler, then repair the catalog rather than merely lengthening the prompt.

**Nearest alternative:** A universal tool can conceal prohibited effects and confuse selection; splitting should follow real capability boundaries, not arbitrary tool-count ceilings.

**Conditional cue:** Name the effect; describe the boundary; validate the arguments.

**Proof:** Inspect `get_balance(account_id)->amount; draft_credit(account_id,amount)->proposal; execute_credit(proposal_id,approval)->receipt` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.1.md#variant-fv-08).

</details>

## FV-09 — Route the actual error category

**Scene and first decision:** A CRM campaign lookup returns success=true and records=[]. What is the appropriate recovery?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A campaign creation request times out after transmission; it may have committed and accepts an idempotency key. What should happen before creating another campaign?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Treat this as an empty successful lookup and clarify or widen the query if the task requires records. An empty result is not evidence of transport failure.

**Answer to this exact scene:** Look up the existing operation by its stable key and reconcile status before deciding whether to retry. A potentially committed write needs status reconciliation to avoid duplicates.

**Base choice:** An MCP lookup succeeds with records=[]; report no matching record and clarify filters rather than retrying a supposed outage.

**Changed constraint and recovery:** A timeout is transient and read-only. Retry with a bounded policy. A permission refusal instead requires changed authorization or escalation.

**Failure:** A write times out after submission. Query operation status before retrying; a transient category alone does not establish safe re-execution.

**Nearest alternative:** MCP protocol errors and the application payload are different layers; error strings alone do not define a safe recovery policy.

**Conditional cue:** Empty is evidence; timeout is uncertainty; denied needs authority.

**Proof:** Inspect `application_result={status:success,records:[]}; failure={category:permission,retryable:false}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.2.md#variant-fv-09).

</details>

## FV-10 — Scope tools to the assigned role

**Scene and first decision:** A clause research specialist only needs read access to a policy corpus. The coordinator also has a deletion tool. Which tool allocation fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A schema-constrained tool call returns an account identifier that is outside the requester’s authorization. What should the application do?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Give the specialist the relevant read tools without the unrelated deletion capability. Minimum relevant capabilities reduce accidental exposure without assuming multi-agent structure alone is safe.

**Answer to this exact scene:** Reject the unauthorized operation even if invocation and schema validation succeeded. Invocation control and shape validation do not confer business authorization.

**Base choice:** Research specialists get only their relevant read tools. A separate authorized executor handles accepted mutations; the coordinator tracks ownership.

**Changed constraint and recovery:** One bounded read-only lookup fits a single agent with two relevant tools. Do not add agents merely to satisfy a tool-count slogan.

**Failure:** Forced tool choice invokes the named tool with invalid semantics. Authorization and application validation still reject it.

**Nearest alternative:** tool_choice governs invocation; it does not prove business permission, factual truth or a sound result.

**Conditional cue:** Choose the call; separately prove permission and meaning.

**Proof:** Inspect `tools={research:[search,read],executor:[approved_write]}; proposal_owner=coordinator` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.3.md#variant-fv-10).

</details>

## FV-11 — Separate connection from inclusion

**Scene and first decision:** A team needs a reviewed MCP server configuration shared with its repository, but each developer has a separate credential. What should be committed?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A connected MCP server advertises a resource. The host has not discovered or included that resource in the agent’s context. What should the architect verify?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Commit safe project-scoped configuration with credentials supplied externally through the supported mechanism. Configuration sharing and secret handling are separate responsibilities.

**Answer to this exact scene:** Verify host resource discovery, permissions and explicit inclusion rather than assume connection supplied content. Server availability does not establish host inclusion or model-visible evidence.

**Base choice:** A shared marketing repository uses safe project MCP configuration with secrets provided outside committed files. Inspect the actual host’s tool/resource discovery behavior.

**Changed constraint and recovery:** A developer tests a personal server. Keep its configuration in the appropriate personal/local scope instead of committing credentials to the team project.

**Failure:** The server connects but the expected resource is not in model context. Check listing, host support and explicit inclusion; do not claim automatic availability.

**Nearest alternative:** Connectivity is not proof that every resource was discovered or supplied. Resource behavior depends on host support and invocation.

**Conditional cue:** Connect, discover, include: prove each stage.

**Proof:** Inspect `project_config={server:crm,secret:environment}; trace=[connected,listed,included]` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.4.md#variant-fv-11).

</details>

## FV-12 — Search before making a scoped edit

**Scene and first decision:** A campaign repository has hundreds of templates. You must find the code emitting an incorrect unsubscribe URL and make a small repair. Which sequence fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** The requested artifact is a brand-new standalone CSV with an explicit schema; no existing file needs modification. Which operation fits after inspecting the target location?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Find relevant paths and text, read the matching code, then edit the smallest supported region and inspect its diff. Search and read establish evidence for a scoped edit.

**Answer to this exact scene:** Write the new artifact at the agreed path and validate its schema. Creating a new artifact is different from patching an existing region.

**Base choice:** An unfamiliar education repository needs a one-function fix. Glob relevant paths, Grep the symbol, Read callers and tests, then Edit the precise existing region.

**Changed constraint and recovery:** A genuinely new standalone artifact has no existing file to patch. Write the new file after verifying its placement and contract.

**Failure:** A broad replacement changes unrelated handlers. Restore the unintended changes and inspect the focused diff and targeted behavior.

**Nearest alternative:** Dumping or rewriting the repository risks losing context and unrelated code. Tool selection follows the task, not a fixed ritual for every edit.

**Conditional cue:** Locate, inspect, change, prove; create only when new.

**Proof:** Inspect `evidence=[paths,symbol_hits,caller_read,test_read]; change={file:handler.py,region:retry_condition}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-2.5.md#variant-fv-12).

</details>

## FV-13 — Put instructions at their real scope

**Scene and first decision:** Repository conventions must apply to all contributors, while one analyst’s preferred response tone is personal. What instruction placement fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A child directory’s instructions conflict with applicable project policy on retaining evidence. The conflict changes the requested output. What should the agent do?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Keep shared conventions in project instructions and personal preferences in the personal scope. Scope should match who owns and needs the instruction.

**Answer to this exact scene:** Identify the applicable instruction files and resolve the conflict according to authority before editing. An identified instruction conflict needs explicit resolution rather than accidental behavior.

**Base choice:** A shared repository convention belongs in project instructions; personal preferences stay in personal configuration. Trace which nested instructions apply to the current path.

**Changed constraint and recovery:** A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file.

**Failure:** Two applicable files disagree on test behavior. Surface and resolve the conflict using the runtime’s documented loading/scope rules.

**Nearest alternative:** More copies increase drift. Instruction files guide model behavior; they do not replace enforced permission checks.

**Conditional cue:** Shared at project; specific at path; resolve conflicts.

**Proof:** Inspect `instructions={shared:CLAUDE.md,package:services/CLAUDE.md,personal:user}; target=services/api.py` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.1.md#variant-fv-13).

</details>

## FV-14 — Give reusable skills a contract

**Scene and first decision:** The team repeatedly produces campaign evidence packets from a supplied brief, source list and output directory. What reusable artifact fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A user gives one short task with complete inputs that is unlikely to recur. What should the agent create?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Create a scoped command or skill with documented inputs, dependencies, output contract and explicit missing-input behavior. A repeatable workflow benefits from explicit invocation and failure contracts.

**Answer to this exact scene:** Use the task brief directly without introducing a reusable workflow solely for this one case. A one-off complete brief does not automatically justify maintaining a reusable abstraction.

**Base choice:** A repeated reviewed-release brief becomes a scoped skill with required commit, evidence paths and output expectations. Check discovery and allowed dependencies.

**Changed constraint and recovery:** A single ad hoc explanation is needed. Use a brief rather than creating a reusable asset without repeated need.

**Failure:** The skill is invoked without the reviewed commit. Stop with a missing-input message instead of inventing a build identity.

**Nearest alternative:** A reusable skill is not permission to publish. Invocation and downstream authorization remain separate.

**Conditional cue:** Reuse the workflow; require its inputs; preserve permission.

**Proof:** Inspect `skill_input={reviewed_commit,tests,evidence}; output={changes,limits,next_action}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.2.md#variant-fv-14).

</details>

## FV-15 — Load rules for the affected paths

**Scene and first decision:** Only files in backend/payments require the payment-specific test convention. What configuration is appropriate?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** The same repository has a policy requiring evidence attribution in every generated artifact, regardless of path. What rule scope fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Use a path-scoped rule whose pattern matches the payment files and verify it is actually loaded for the change. Conditional conventions should load for their relevant paths.

**Answer to this exact scene:** Use an applicable broader instruction for the cross-cutting attribution policy. A genuinely cross-cutting requirement needs correspondingly broad applicability.

**Base choice:** Backend and test conventions are scoped to their respective path patterns. Predict applicable rules for a change touching both areas and verify actual loading.

**Changed constraint and recovery:** A security policy genuinely applies across the repository. Move that requirement to an appropriate broader scope.

**Failure:** A test file moved outside the expected glob, so its rule was not loaded. Correct the scope and check a matching and nonmatching path.

**Nearest alternative:** Duplicating every rule into the main prompt can hide mismatches and flood context; path scope must match actual files.

**Conditional cue:** Match the path; verify the rule; broaden only when shared.

**Proof:** Inspect `paths=[services/api.py,tests/test_api.py]; rules={backend:services/**,testing:tests/**}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.3.md#variant-fv-15).

</details>

## FV-16 — Plan when uncertainty crosses boundaries

**Scene and first decision:** A change spans authentication, ingestion and retention behavior; dependencies and acceptance boundaries are still unclear. Which starting mode fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A reviewed typo fix touches one documented label, has an exact replacement and no behavior change. Which starting mode fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Inspect dependencies and develop a reviewed plan before making the broad change. Uncertainty and cross-file impact justify planning and evidence gathering.

**Answer to this exact scene:** Perform the clear bounded edit directly and verify the rendered label. A small unambiguous low-impact change can be executed and checked directly.

**Base choice:** A cross-service authentication change has unclear callers and migration impact. Inspect evidence, produce a plan and review dependencies before editing.

**Changed constraint and recovery:** The task becomes a precise typo in an isolated documented comment. Direct execution and a focused check are proportionate.

**Failure:** An apparently small edit reveals a shared API dependency. Pause to revise the plan rather than continuing under the old assumption.

**Nearest alternative:** Always planning adds overhead to bounded simple work; always executing can miss uncertain dependencies.

**Conditional cue:** Plan the unknown boundaries; execute the bounded known edit.

**Proof:** Inspect `plan={affected:[client,server,tests],unknown:[migration],acceptance:[old_client_works]}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.4.md#variant-fv-16).

</details>

## FV-17 — Change the hypothesis after repeated failure

**Scene and first decision:** An agent has twice returned a campaign report with a broken date parser. The feedback only said improve it. What feedback should be supplied next?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** The same precise failing fixture still fails after two different implementations. The team is repeating its initial diagnosis without inspecting new evidence. What should change?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Provide the failing input, observed output, expected result and relevant diagnostic so refinement targets a reproducible defect. Concrete fixtures and diagnostics define measurable refinement.

**Answer to this exact scene:** Revisit the failure hypothesis and inspect the implementation or dependency evidence before another change. Repeated failure can signal a wrong hypothesis rather than insufficient repetition.

**Base choice:** A date parser fails on one fixture. Supply actual input, expected result, failing assertion and relevant code; make a targeted change and re-run the fixture plus nearby cases.

**Changed constraint and recovery:** Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign.

**Failure:** The same failure survives two identical retries. Investigate a new cause, such as locale interpretation or preprocessing, instead of repeating the same prompt.

**Nearest alternative:** More iterations do not imply learning. Narrow evidence and hypothesis changes matter more than request length.

**Conditional cue:** Example, expectation, evidence; failed hypothesis must change.

**Proof:** Inspect `feedback={input:03/04,locale:en_GB,expected:2026-04-03,actual:2026-03-04,check:date_locale}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.5.md#variant-fv-17).

</details>

## FV-18 — Run CI with observable failure

**Scene and first decision:** A nightly repository audit must inspect local files, run tests and emit a machine-readable findings artifact. It must run without a user at the terminal. Which runtime fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A separate job summarizes 2,000 independent supplied texts, needs no local filesystem or dependent tool loop and tolerates asynchronous completion. Which runtime is eligible for consideration?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Use a configured headless Claude Code job with scoped credentials, exit handling and validated findings extraction. The audit depends on the Code runtime and repository environment.

**Answer to this exact scene:** Consider Messages Batch for independent supported API requests and recover individual failed or expired items. Independent eligible requests can be processed asynchronously; this is not a completion-time guarantee.

**Base choice:** A scheduled repository-dependent Code review runs headless with available credentials, scoped permissions, project context, exit handling and retained artifacts. Parse its CLI envelope before validating the findings payload.

**Changed constraint and recovery:** The work becomes independent eligible Messages requests with no local iterative state and a tolerant deadline. Consider batch; an urgent dependent tool loop remains a different runtime.

**Failure:** Missing credentials or malformed findings must produce an observable failure or bounded repair, never an empty “passed” report.

**Nearest alternative:** Nonblocking alone does not justify Messages Batch. JSON CLI output alone does not prove the findings schema or source accuracy.

**Conditional cue:** Runtime by dependency; gate by validated evidence.

**Proof:** Inspect `ci_packet={commit,permissions,environment,prompt,exit_code,envelope,findings}; accept=all_required_checks_pass` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-3.6.md#variant-fv-18).

</details>

## FV-19 — Define a finding with evidence criteria

**Scene and first decision:** A contract scanner flags any occurrence of fee as an unexpected charge, causing false positives on clauses that expressly prohibit fees. What prompt change best addresses the defect?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** The policy owner cannot say whether conditional pass-through costs count as prohibited fees. Which next step fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Define the prohibited-charge criterion, exclusions, evidence citation and examples of negated versus operative clauses. Explicit operational criteria and exclusions reduce this known classification ambiguity.

**Answer to this exact scene:** Request the missing policy interpretation or label those cases unresolved before classifying them. An unresolved business definition cannot be repaired by confident model wording.

**Base choice:** A legal clause review flags only an explicit unilateral termination right without the fictional required notice. Provide threshold, exclusions and source locator expectations.

**Changed constraint and recovery:** The policy wording is ambiguous about mutual termination. Ask for clarification or label the case uncertain instead of treating every termination mention as a violation.

**Failure:** False positives cluster around historical examples. Add the exclusion and test borderline cases against actual text.

**Nearest alternative:** “Be careful” does not operationalize the criterion. A longer prompt without measurable boundaries can preserve the same errors.

**Conditional cue:** Name trigger, exclusion and evidence before flagging.

**Proof:** Inspect `finding_rule={trigger:unilateral_right,required:notice,evidence:clause_locator,exclude:historical_example}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.1.md#variant-fv-19).

</details>

## FV-20 — Teach the edges with representative examples

**Scene and first decision:** A campaign classifier sees regular examples but fails on disclaimers and conditional promotions. Which few-shot set best addresses the observed distribution?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A new market introduces a promotion structure absent from the original examples; held-out results show systematic mistakes. What should the team do?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Add representative contrastive examples for the failing edge cases with the intended labels and evidence. Representative edge cases teach the distinction the current set omits.

**Answer to this exact scene:** Revise or add examples for the changed distribution and evaluate on a separate held-out set. Distribution change needs evidence-driven example revision and independent measurement.

**Base choice:** A finance extraction prompt includes ordinary invoices, absent tax IDs and source conflicts, with explanations of allowed nulls and unresolved values.

**Changed constraint and recovery:** A new document population uses credit notes and negative amounts. Revise the example distribution and validate on unseen cases.

**Failure:** All examples are clean positive invoices; the model invents rare fields. Add realistic counterexamples rather than simply adding more clean examples.

**Nearest alternative:** Few-shot consistency is not a factual guarantee. Examples should represent the relevant error modes, not leak held-out answers.

**Conditional cue:** Examples teach boundaries; holdouts test transfer.

**Proof:** Inspect `examples=[ordinary,missing_field,conflict,credit_note]; holdout=unseen_edge_cases` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.2.md#variant-fv-20).

</details>

## FV-21 — Validate shape and truth separately

**Scene and first decision:** A source invoice omits a purchase-order number; the approved schema permits null for that field. What should the extractor return?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** Another invoice explicitly states PO-782, but the schema-valid output says PO-728. What validation fixes this defect?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Return null for the unsupported field and preserve the source locator. The approved nullable contract supports absence without invention.

**Answer to this exact scene:** Compare the field against source evidence and correct the non-null value through semantic validation. The wrong value has valid shape but conflicts with the source.

**Base choice:** Use supported strict schema enforcement for an extraction tool, then independently validate source evidence and arithmetic. Tool selection, structural conformance and semantic validity are separate checks.

**Changed constraint and recovery:** A field truly absent from the source may be null only when the declared contract allows it. A wrong non-null amount does not call for a nullable-only repair.

**Failure:** The JSON is well typed but says 900 where the source says 90. Reject the semantic mismatch and return the exact failed check.

**Nearest alternative:** Forcing a tool call does not prove schema adherence unless the applicable mechanism enforces it; even conforming output can be wrong.

**Conditional cue:** Call, shape, truth: three proofs, not one.

**Proof:** Inspect `candidate={amount:900,currency:USD}; source={amount:90}; shape=pass; source_match=fail` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.3.md#variant-fv-21).

</details>

## FV-22 — Repair the failed check within a budget

**Scene and first decision:** An extracted invoice has line totals summing to 980 but reports 890; the source clearly shows 980. What recovery fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** After the allowed correction attempts, two source pages still disagree about the invoice total. What should happen?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Send the exact failed arithmetic and source checks with the previous output for a bounded targeted correction. A clear check payload targets the evidenced error and bounds recovery.

**Answer to this exact scene:** Keep the discrepancy unresolved and escalate with source evidence and attempt history. Persistent source conflict cannot be resolved by inventing agreement.

**Base choice:** An invoice candidate’s subtotal plus tax differs from total. Return the precise values, source locators and failed arithmetic check for a bounded correction.

**Changed constraint and recovery:** The source itself contains contradictory totals. Preserve both values and route review instead of asking Claude to manufacture reconciliation.

**Failure:** The retry budget is exhausted. Escalate with source, previous outputs, failed checks and unresolved discrepancy.

**Nearest alternative:** Retrying the whole document without diagnostic feedback can repeat the error or mutate correct fields.

**Conditional cue:** Repair the named failure; stop when evidence cannot resolve it.

**Proof:** Inspect `failed_check={subtotal:80,tax:8,total:100,expected:88}; retry_budget=2; status=unresolved` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.4.md#variant-fv-22).

</details>

## FV-23 — Choose batch by dependencies and deadline

**Scene and first decision:** An overnight job classifies independent supplied campaign snippets with no local runtime requirement; each can finish asynchronously. Which design fits?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A launch approval now requires one result before constructing the next prompt, with a five-minute deadline and human clarification. What design fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Use eligible independent batch requests with stable item IDs and per-item result reconciliation. Independence and asynchronous tolerance make batch a candidate.

**Answer to this exact scene:** Use an appropriate interactive or synchronous dependent workflow with deadline and escalation handling. Dependent, time-sensitive human interaction changes the runtime requirements.

**Base choice:** Independent eligible document requests tolerate delayed completion and have per-item recovery. Messages Batch is a candidate; retain custom IDs and item states.

**Changed constraint and recovery:** A result is needed before the next dependent local tool step or a tight user deadline. Use the appropriate immediate/interactive runtime instead.

**Failure:** Some items expire or fail. Recover those items with their recorded inputs; do not treat a submission as completed work.

**Nearest alternative:** A 24-hour processing window is not a guaranteed finish time. Batch does not substitute for a local Code agent loop with filesystem state.

**Conditional cue:** Independent plus tolerant plus recoverable; otherwise another lane.

**Proof:** Inspect `items={i1:succeeded,i2:expired,i3:errored}; recovery=[i2,i3]; deadline_policy=explicit` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.5.md#variant-fv-23).

</details>

## FV-24 — Give the critic independent evidence

**Scene and first decision:** A consequential contract finding needs review against the source. The producer and reviewer currently share only the producer’s conclusion. What architecture best improves review?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A low-risk internal formatting task has an exact deterministic validator; no substantive conclusion is produced. What review approach is proportionate?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Give an independent reviewer the source, producer artifact and explicit criteria; preserve and resolve disagreements. Independent source-based critique can identify producer omissions.

**Answer to this exact scene:** Use the deterministic validator and bounded human or automated spot checks appropriate to the low risk. Additional model passes need to justify their cost and failure exposure for this bounded task.

**Base choice:** A producer proposes extracted claims; a separate critic checks source locators, omissions and contradictions under explicit criteria. Resolve disagreement by evidence.

**Changed constraint and recovery:** A simple low-risk formatting task has deterministic validation. Extra model passes may not justify their cost.

**Failure:** Both instances share a misleading summary and agree. Give the critic original sources or a different check; agreement alone is not validation.

**Nearest alternative:** Repeated identical prompts can amplify the same blind spot. Independence needs evidence and criteria, not just another instance.

**Conditional cue:** Separate the reviewer’s evidence; resolve with the source.

**Proof:** Inspect `producer={claims,sources}; critic={criteria,original_sources,failed_checks}; dispute={claim,source,verdict}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-4.6.md#variant-fv-24).

</details>

## FV-25 — Compact the decision state, not just prose

**Scene and first decision:** A long investigation is approaching its context limit. A rare jurisdiction exception determines the final action. What should the compact state preserve?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** After compaction, a referenced policy document is revised and the summary no longer establishes the applicable exception. What should happen?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Preserve the exception, decisions, unresolved issues and precise source pointers in the compact state. Critical constraints and pointers must survive compaction to support later decisions.

**Answer to this exact scene:** Reacquire the revised source and revalidate the affected decision instead of reconstructing missing details. A changed source requires fresh evidence even when conversation state persists.

**Base choice:** A long marketing investigation stores the current question, accepted constraints, unresolved issues, source pointers and next bounded action before compaction.

**Changed constraint and recovery:** Source consent or policy changes. Refresh the relevant evidence and revise the stored decision state.

**Failure:** A summary drops the “do not contact” exception. Restore it from the source before proceeding; never infer that omitted means revoked.

**Nearest alternative:** Keeping every transcript token can overwhelm context. A compact record must retain decisive exceptions and reacquisition paths.

**Conditional cue:** Keep decisions and exceptions; reacquire the detail.

**Proof:** Inspect `state={question,constraints:[no_contact],sources:[CRM42],unresolved:[consent_age],next:verify}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.1.md#variant-fv-25).

</details>

## FV-26 — Honor explicit escalation with context

**Scene and first decision:** A customer explicitly asks to speak to a human about disputed campaign billing. Policy permits that escalation. What should the assistant do?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A customer says the report is confusing but does not request a human; policy calls for clarification of the disputed metric first. What should happen?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Escalate promptly with the issue, verified identifiers, evidence and unresolved status. The explicit request is a defined escalation trigger.

**Answer to this exact scene:** Ask a targeted clarification under the support policy while keeping escalation available. Ambiguity without the trigger should follow the applicable clarification route.

**Base choice:** A customer explicitly asks for a human. Route promptly with verified identity status, issues, evidence, attempted and blocked actions, and next owner.

**Changed constraint and recovery:** The customer says “this is frustrating” without requesting a person. Clarify or continue according to the fictional support policy; do not invent an escalation mandate.

**Failure:** The handoff says credit issued, but only a proposal exists. Correct status and include the operation ledger before transferring.

**Nearest alternative:** A transcript dump does not ensure an actionable handoff; a vague complaint is not identical to an explicit human request.

**Conditional cue:** Hear the trigger; hand over facts, status and next action.

**Proof:** Inspect `handoff={identity_status,issues,confirmed,proposed,blocked,reason,next_owner}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.2.md#variant-fv-26).

</details>

## FV-27 — Propagate partial success without hiding failure

**Scene and first decision:** A coordinator receives valid findings from two specialists and a retryable source timeout from a third. The missing source is mandatory for the final conclusion. What should it do?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A different brief explicitly permits a partial overview; an optional source is unavailable and cannot be recovered now. Which output fits?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Preserve successful findings, report the missing mandatory evidence and dispatch targeted recovery before a final supported conclusion. Targeted recovery retains valid work while respecting the mandatory evidence requirement.

**Answer to this exact scene:** Return the permitted partial overview with attributed findings and an explicit unavailable-source limitation. Explicit permission for partial coverage changes whether a bounded output is acceptable.

**Base choice:** Specialists return findings and structured failures to the coordinator. Preserve successful evidence and decide which missing dimensions block the final claim.

**Changed constraint and recovery:** The unavailable source is explicitly optional. Publish a bounded partial answer with the omission and limitations visible.

**Failure:** A mandatory permissions source fails. Target that recovery or stop the affected conclusion; do not replace its facts with another specialist’s guess.

**Nearest alternative:** Discarding all successes wastes evidence; silently dropping a failed mandatory dimension fabricates completeness.

**Conditional cue:** Keep the successes; name the gap; block dependent claims.

**Proof:** Inspect `result={dimension:permissions,status:failed,reason:access_denied,retryable:false}; aggregate=partial` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.3.md#variant-fv-27).

</details>

## FV-28 — Build a minimal code evidence ledger

**Scene and first decision:** A defect appears in one generated campaign URL among a large codebase. What exploration strategy fits before editing?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A targeted read shows that the URL builder depends on a shared encoding helper used by three services. What should exploration do next?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Search narrowly, read relevant files and keep a compact evidence ledger of paths, dependencies and findings. Targeted evidence reduces context noise and supports a justified local diagnosis.

**Answer to this exact scene:** Expand into the demonstrated dependency chain and inspect affected callers before choosing the repair. Newly evidenced cross-cutting dependencies require appropriately expanded investigation.

**Base choice:** A large codebase bug starts with targeted symbol search, relevant caller reads and a file/dependency ledger. Expand only the evidence path needed for the defect.

**Changed constraint and recovery:** The failure crosses the API boundary. Add the adjacent client/server dependencies and contract tests rather than preserving an artificially narrow scope.

**Failure:** Compaction loses a function’s exception condition. Re-read the actual file at the current commit before editing.

**Nearest alternative:** A guessed summary cannot replace current code evidence. Reading the whole repository also makes the decisive detail harder to retain.

**Conditional cue:** Map the path; read the dependency; refresh before edit.

**Proof:** Inspect `ledger={commit,files:[handler,caller],symbols:[retry],unresolved:[ownership],next:test_contract}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.4.md#variant-fv-28).

</details>

## FV-29 — Test risk slices and review capacity

**Scene and first decision:** A routing model is 98% accurate overall but only 65% accurate on a rare high-loss claim category. What should review routing use?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** The routing team has calibrated scores but reviewer demand exceeds daily capacity; a published policy forbids silently dropping flagged claims. What is required?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Use stratified error and loss evidence to route the high-risk category rather than rely on the overall average. Aggregate accuracy can hide consequential subgroup failure.

**Answer to this exact scene:** Define and test a capacity and overflow policy with observable escalation for unresolved review demand. A review design must specify what happens when its required human queue exceeds capacity.

**Base choice:** A finance extractor has high overall accuracy but weaker rare-currency performance. Evaluate severity-weighted slices on independent holdout and calibrate review thresholds with actual human capacity.

**Changed constraint and recovery:** A review queue exceeds available capacity. Apply a declared overflow policy or reduce scope; do not silently accept low-confidence items.

**Failure:** Distribution drift breaks calibration. Recalibrate on suitable data and evaluate on a separate holdout; do not tune against the final test set.

**Nearest alternative:** The average can hide dangerous categories; confidence scores alone are not calibrated correctness probabilities.

**Conditional cue:** Average, slice, severity, capacity: check all four.

**Proof:** Inspect `metrics={overall:0.98,rare_currency:0.70}; capacity=20; queued=35; overflow=hold` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.5.md#variant-fv-29).

</details>

## FV-30 — Keep sources through a join

**Scene and first decision:** Two systems disagree about a contract’s termination date and have different update timestamps. What should the synthesis preserve?

**Pause:** Say your choice and its decisive evidence before continuing.

**Changed factual scene:** A supported federation now provides one query interface over both sources, but their records still conflict. What changes?

**Pause again:** Say which constraint changed, whether it reverses the choice, and what failure/recovery evidence is needed.

<details>
<summary>Debrief after both answers</summary>


**Answer to this exact scene:** Keep field-level source locators, timestamps and the explicit discrepancy without inventing a merged date. Attribution and explicit uncertainty preserve the actual evidence state.

**Answer to this exact scene:** Return a structured claim-to-source mapping with document locators, relevant evidence and timestamps, retaining the conflict for the coordinator. A unified query interface does not replace structured claim-source mappings. Downstream synthesis needs attributable claims and explicit conflict, not inferred source identity.

**Base choice:** Separate finance and CRM interfaces return revenue and customer records with timestamps and field-level provenance. Join only under a declared identifier rule.

**Changed constraint and recovery:** The host offers supported federation. It may simplify retrieval, but still retain origin, time and conflict checks.

**Failure:** CRM says customer active while finance reports suspended at a different date. Preserve both assertions and their scope; ask for policy or current authoritative evidence.

**Nearest alternative:** A joined table can erase provenance and make mismatched-age sources look consistent. Federation does not establish truth by itself.

**Conditional cue:** Join identifiers; retain origins; expose disagreement.

**Proof:** Inspect `row={customer_id:C7,revenue:{value:120,source:FIN9,as_of:d1},status:{value:active,source:CRM4,as_of:d2}}` and record the source/permission/state check that proves the result.

[Exact repair](objectives/objective-5.6.md#variant-fv-30).

</details>


<span data-assessment-exposure="cct-fv-01-base-v1,cct-fv-01-retry-v1,cct-fv-02-base-v1,cct-fv-02-retry-v1,cct-fv-03-base-v1,cct-fv-03-retry-v1,cct-fv-04-base-v1,cct-fv-04-retry-v1,cct-fv-05-base-v1,cct-fv-05-retry-v1,cct-fv-06-base-v1,cct-fv-06-retry-v1,cct-fv-07-base-v1,cct-fv-07-retry-v1,cct-fv-08-base-v1,cct-fv-08-retry-v1,cct-fv-09-base-v1,cct-fv-09-retry-v1,cct-fv-10-base-v1,cct-fv-10-retry-v1,cct-fv-11-base-v1,cct-fv-11-retry-v1,cct-fv-12-base-v1,cct-fv-12-retry-v1,cct-fv-13-base-v1,cct-fv-13-retry-v1,cct-fv-14-base-v1,cct-fv-14-retry-v1,cct-fv-15-base-v1,cct-fv-15-retry-v1,cct-fv-16-base-v1,cct-fv-16-retry-v1,cct-fv-17-base-v1,cct-fv-17-retry-v1,cct-fv-18-base-v1,cct-fv-18-retry-v1,cct-fv-19-base-v1,cct-fv-19-retry-v1,cct-fv-20-base-v1,cct-fv-20-retry-v1,cct-fv-21-base-v1,cct-fv-21-retry-v1,cct-fv-22-base-v1,cct-fv-22-retry-v1,cct-fv-23-base-v1,cct-fv-23-retry-v1,cct-fv-24-base-v1,cct-fv-24-retry-v1,cct-fv-25-base-v1,cct-fv-25-retry-v1,cct-fv-26-base-v1,cct-fv-26-retry-v1,cct-fv-27-base-v1,cct-fv-27-retry-v1,cct-fv-28-base-v1,cct-fv-28-retry-v1,cct-fv-29-base-v1,cct-fv-29-retry-v1,cct-fv-30-base-v1,cct-fv-30-retry-v1"></span>