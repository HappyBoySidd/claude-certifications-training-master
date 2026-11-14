# Architecture choice workshop — decide under competing constraints

[CCAR-F home](site:exams/ccar-f.html) · [Mechanism clinic](mechanism-clinic.md) · [Learning journey](learning-journey.md)

**Start here:** no installation. These are 12 original formative questions in six application cases, not copied exam questions and not a timed mock. Allow 20–30 minutes. Before revealing each answer, name the requirement, select exactly the requested number of options, and explain why the closest alternative fails. One constraint changes in the second question of each case.

**How to use the choices:** several options can help in general. Choose what meets the stated requirement at the stated boundary. A schema addresses shape; a runtime guard addresses an action; retrieved evidence supports a claim. Do not silently add requirements. These exercises use current documented contracts, checked 2026-10-21, and link to the saved-guide objectives; they do not establish official exam wording or frequency.

## 1. A marketing experiment changes after approval

A campaign operator approves experiment E7: 10% of visitors, one country, seven days. Before execution, another editor changes it to 50% and adds two countries. The experiment controller can reject a stale revision.

### Decision 1.1

Choose ONE. Which control directly prevents execution under the old approval?

- **A.** Keep approval on the experiment ID and show the newest configuration in the audit log.
- **B.** Bind approval to the displayed revision and reject execution if that revision changes.
- **C.** Repeat the campaign policy in the system prompt before asking Claude to execute.
- **D.** Require a second confirmation click on the experiment ID after a fixed delay.

<details>
<summary>Reveal decision 1.1: answer and alternatives</summary>

**Answer: B.** A records the mismatch after the decision but leaves approval unbound. C supplies guidance without enforcing the revision. D adds friction without identifying the approved configuration. B couples the human decision to the executable revision; show audience, allocation, duration and consequences before approval.

[Repair objective 1.4](objectives/objective-1.4.md).

</details>

### Decision 1.2

Choose TWO. Now a revision is approved, but controller timeouts can occur after activation. Which two controls address a safe retry?

- **A.** Resolve the existing operation ID against controller state before attempting activation again.
- **B.** Issue a new operation ID for each retry so every attempt has an independent history.
- **C.** Reuse an idempotency key tied to the intended activation when the controller supports it.
- **D.** Ask the model whether the wording of its prior response implies successful activation.

<details>
<summary>Reveal decision 1.2: answer and alternatives</summary>

**Answer: A and C.** B can create duplicate business operations. D treats generated text as execution evidence. A establishes observed state; C prevents replay from creating a second activation under the stated controller contract. If state cannot be resolved, surface uncertainty rather than claim completion.

[Repair objective 1.4](objectives/objective-1.4.md).

</details>

## 2. A facilities assistant needs a narrow status check

A campus assistant has a room ID and needs current occupancy. Its room-profile tool also depends on a slow legacy maintenance system. A separate occupancy service already accepts room IDs and enforces caller access. The assistant does not need maintenance data.

### Decision 2.1

Choose ONE. Which tool boundary best isolates this request?

- **A.** Expose the maintenance retry policy and keep using the full room-profile operation.
- **B.** Request the full room profile and cache its maintenance fields for later turns.
- **C.** Combine room profile, occupancy and maintenance into one comprehensive tool.
- **D.** Expose an authorized occupancy query by room ID without the maintenance dependency.

<details>
<summary>Reveal decision 2.1: answer and alternatives</summary>

**Answer: D.** A and B retain the unrelated dependency; caching does not remove its first-call coupling. C broadens the failure surface. D follows the existing narrow service contract and preserves authorization. This is not a universal rule against combined tools: combine when one business operation genuinely needs a coherent result.

[Repair objective 2.1](objectives/objective-2.1.md).

</details>

### Decision 2.2

Choose ONE. Change: occupancy estimates now require a location-specific sensor correction factor returned only by a fresh sensor read. What should happen?

- **A.** Fetch and validate the correction factor, then request the dependent estimate with that result.
- **B.** Keep estimates independent by asking the model to infer the missing correction factor.
- **C.** Launch both calls together and rely on the tool array order to imply their dependency.
- **D.** Replace the sensor dependency with a longer description of the occupancy tool.

<details>
<summary>Reveal decision 2.2: answer and alternatives</summary>

**Answer: A.** B invents required evidence. C does not enforce a data dependency. D documents a requirement without satisfying it. The first design removed an accidental dependency; this new constraint creates a real one. The host/runtime must sequence it.

[Repair objective 2.3](objectives/objective-2.3.md).

</details>

## 3. A government inventory service has two kinds of failure

An MCP tool queries permitted public-equipment records. A valid call reaches its handler, which finds that the selected warehouse is temporarily unavailable. No inventory update occurred. The client and server use the linked 2025-06-18 protocol contract.

### Decision 3.1

Choose ONE. What response preserves an actionable tool-execution failure?

- **A.** Return an empty successful collection and leave diagnosis to server logs.
- **B.** Return a protocol method-not-found error although the requested tool was executed.
- **C.** Return tool-result error content with isError true and bounded recovery information.
- **D.** Return a normal result with an unavailable status field while leaving isError false.

<details>
<summary>Reveal decision 3.1: answer and alternatives</summary>

**Answer: C.** A conflates unavailable with empty. B misclassifies an executed tool failure as a protocol lookup failure. D leaves the execution failure unmarked at the protocol tool-result boundary. C lets the client/model distinguish the failure; retryability and recovery fields are application design, not additional universal protocol fields. Do not leak credentials or internal diagnostics.

[Repair objective 2.4](objectives/objective-2.4.md).

</details>

### Decision 3.2

Choose ONE. Change: the request names a tool that does not exist on this server. Which distinction matters?

- **A.** Treat every server-side failure as a successful tool result to preserve consistency.
- **B.** Report the protocol-level tool lookup failure, rather than a warehouse execution failure.
- **C.** Convert the missing tool into an empty inventory result for that warehouse.
- **D.** Automatically substitute a similarly named write tool and retry its operation.

<details>
<summary>Reveal decision 3.2: answer and alternatives</summary>

**Answer: B.** A and C conceal the lookup failure; D changes capability and risk without authority. B preserves the layer where the request failed. The protocol distinguishes server/protocol problems from errors inside an invoked tool. Consult negotiated protocol and SDK behavior for the exact error code.

[Repair objective 5.3](objectives/objective-5.3.md).

</details>

## 4. A legal review pipeline receives the wrong revision

A coordinator delegates clause analysis and then prepares a risk summary. The analyst returns findings from revision 3, while the requested signed agreement is revision 4. Both fit within the available context budget. The synthesis worker has no automatic access to other workers’ histories.

### Decision 4.1

Choose TWO. What must the coordinator do before relying on the analysis?

- **A.** Expand the synthesis context window so the revision-3 findings become authoritative.
- **B.** Provide the synthesis worker with the actual validated findings and document identifiers.
- **C.** Forward only the analyst’s completion label to reduce prompt size.
- **D.** Resolve the revision mismatch and reanalyze affected material before treating it as current.

<details>
<summary>Reveal decision 4.1: answer and alternatives</summary>

**Answer: B and D.** A does not repair provenance. C omits the evidence. B addresses explicit handoff, and D addresses whether the handed-off findings answer the requested task. Passing more context alone cannot make an outdated analysis current.

[Repair objective 1.2](objectives/objective-1.2.md).

</details>

### Decision 4.2

Choose ONE. Change: revision 4 is unavailable, and the business accepts a clearly labeled preliminary review. Which response preserves that boundary?

- **A.** Use revision 3 and describe the review as final because the analyst completed its work.
- **B.** Ask the synthesis worker to infer the changes without seeing the signed agreement.
- **C.** Label the review preliminary, retain revision-3 evidence and identify unverified changes.
- **D.** Remove revision identifiers so readers judge only the summary’s substantive language.

<details>
<summary>Reveal decision 4.2: answer and alternatives</summary>

**Answer: C.** A changes acceptance criteria; B invents unseen changes; D hides the limitation. C communicates what the available evidence supports. Application policy must decide whether any downstream action is permitted on a preliminary review.

[Repair objective 5.6](objectives/objective-5.6.md).

</details>

## 5. Finance reconciliation parses correctly but disagrees

A reconciliation assistant emits schema-valid JSON containing a payment amount and source reference. The source ledger uses integer minor units; a model-produced amount differs by a factor of 100. The downstream system requires verified amounts before posting.

### Decision 5.1

Choose ONE. What directly addresses the observed defect?

- **A.** Validate units and amount against authoritative ledger evidence before permitting posting.
- **B.** Lower temperature and accept any response that satisfies the existing JSON schema.
- **C.** Add stricter property types and treat successful parsing as proof of ledger agreement.
- **D.** Increase the output-token limit so the model can explain its converted amount.

<details>
<summary>Reveal decision 5.1: answer and alternatives</summary>

**Answer: A.** B may reduce variation but does not establish evidence agreement. C checks representation, not this semantic error. D changes capacity. A validates meaning at the posting boundary; a schema-valid result is still only a candidate business value.

[Repair objective 4.4](objectives/objective-4.4.md).

</details>

### Decision 5.2

Choose ONE. Change: the value is correct, but a legacy parser rejects occasional malformed final JSON. A supported schema-constrained API output mode is available. Which primary repair fits?

- **A.** Add a second reconciliation analyst without changing the response-format contract.
- **B.** Accept every parse failure and infer fields from surrounding natural-language text.
- **C.** Use a smaller temperature and treat formatting variation as an authorization failure.
- **D.** Configure supported final-response schema constraints and handle non-success outcomes.

<details>
<summary>Reveal decision 5.2: answer and alternatives</summary>

**Answer: D.** A adds analysis to a formatting problem. B hides a contract failure. C mixes layers. D addresses final output shape while preserving refusal/truncation handling and semantic validation from the first question. Tool-input strictness alone targets a different output boundary.

[Repair objective 4.3](objectives/objective-4.3.md).

</details>

## 6. Education policy answers have conflicting sources

An assistant has retrieved a current district policy and an older school handbook. They disagree on a deadline. Both are authentic documents. The application specifies that the current district policy governs, and responses must identify the controlling source.

### Decision 6.1

Choose ONE. Which behavior meets the full requirement?

- **A.** Cite both dates and ask the user to choose, without applying the stated district rule.
- **B.** Use the current district rule, cite it, and explain the handbook conflict where relevant.
- **C.** Quote whichever document the retrieval system ranked first without checking policy priority.
- **D.** Select a single confident date and omit source identity to keep the answer concise.

<details>
<summary>Reveal decision 6.1: answer and alternatives</summary>

**Answer: B.** A leaves an already specified precedence rule unapplied. C substitutes retrieval rank for authority. D loses the required evidence. Retrieval supplies candidate context; the application’s source-priority rule determines which evidence governs this case.

[Repair objective 5.6](objectives/objective-5.6.md).

</details>

### Decision 6.2

Choose ONE. Change: the application has no precedence rule and two current authoritative policies conflict. What is the appropriate next step?

- **A.** Increase sampling determinism and trust the most consistently repeated date.
- **B.** Use a more specific role prompt to make the assistant the final policy authority.
- **C.** Disclose the conflict and seek an authorized clarification before giving a definitive deadline.
- **D.** Run retrieval again until one source has a higher similarity score than the other.

<details>
<summary>Reveal decision 6.2: answer and alternatives</summary>

**Answer: C.** A changes variability, not authority. B invents decision rights. D cannot resolve a normative conflict through relevance alone. C preserves uncertainty at the point where the evidence and policy do not justify a unique answer.

[Repair objective 5.5](objectives/objective-5.5.md).

</details>

## Review your reasoning, not just your letter

Record privately: decision number → missed constraint → closest distractor → what would make that distractor correct. For a choose-two item, explain what each choice independently contributes. Revisit the second decision later without the first answer visible. This is a learning exercise, not a validated readiness score; it does not change the graded bank or browser progress.

Return to the [mechanism clinic](mechanism-clinic.md), apply one control in [Lab 08](../../06-Labs/08-CCAR-F-architecture-decisions/README.md), or use [existing CCAR-F timed practice](site:practice/index.html?exam=CCAR-F). These new items are page-local formative practice, not included in that timed bank.

## Technical contracts and further study

- [MCP tools specification, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): tool errors, client interaction and result contracts. Confirm the version actually negotiated by your implementation.
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools): descriptions, input schemas and tool choice.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): supported final-output constraints and non-success handling.
- [Coordinator handoffs](objectives/objective-1.2.md), [semantic validation](objectives/objective-4.4.md), [uncertainty and human review](objectives/objective-5.5.md), [source provenance](objectives/objective-5.6.md).

Business revision binding, idempotency and source-precedence rules in these cases are stated application contracts and architecture reasoning, not claims of automatic model or protocol enforcement. All cases and options are original teaching material; no third-party flashcards or claimed exam-dump questions are incorporated.