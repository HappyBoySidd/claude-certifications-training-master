# Scenario learning studio

**New to building applications?** Start with the [architecture apprenticeship](architecture-studio/README.md): eight complete original application cases, beginning with a plain-language primer, then decisions, diagrams, lab experiments, simulations, questions and conversation prompts. These are additional teaching scenarios, not additional official exam families.

The six stories in [orientation](L00-orientation.md#the-six-scenarios-and-the-lessons-that-cover-them) are the scenario families described by the saved exam guide. They are not the limit of your preparation. This studio brings together **30 original objective-level decision variants**, six walkthroughs, six extended industry cases, diagrams, practice and recall. Supplemental cases are teaching exercises, not additional official exam scenarios or a promise to cover every possible exam question.

## Use one complete learning loop

1. **Understand:** open a scenario below; name its goal, evidence, constraints and possible side effects.
2. **Decide before reading:** write the mechanism you would choose and why the nearest alternative loses.
3. **Inspect:** open the linked objective packet and its inline drawing, example code, prompt or contract. Explain the failure and recovery path aloud.
4. **Change one condition:** reverse a deadline, authorization, evidence or dependency assumption. Explain whether your architecture changes.
5. **Test:** answer the matching original question without the lesson open. Use its exact repair link after a miss; return to the same saved question.
6. **Recall:** use the [closed-answer cards](FLASHCARDS.md) and [conversation scripts](decision-conversation.md); attempt the different delayed retry when due.

**Memory cue: GATES** — Goal, Authority, Tools, Evidence, Stop/recover. This is an original recall aid, not an official exam framework. Always justify the actual mechanism; a mnemonic cannot decide the answer for you.

## Choose the decision you need to strengthen

Each row goes directly to a worked base case, changed constraint, failure/recovery, mechanism and blind check. The question link selects that variant. These are practice opportunities, not completion or mastery claims.

Choose a domain and open only the decisions you need. Each domain stays independently expandable so the industry cases remain close at hand.

<details>
<summary>Domain 1: Agentic architecture and orchestration — 7 decisions</summary>

| Decision | Objective lesson | Apply the contrast | Check yourself |
| --- | --- | --- | --- |
| FV-01 — Confirm the effect before retrying | [1.1](objectives/objective-1.1.md#variant-fv-01) | The model returns end_turn, but the payment request timed out. Stop the model loop; do not describe the refund as committed. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.1&variant=FV-01) |
| FV-02 — Cover dimensions before synthesizing | [1.2](objectives/objective-1.2.md#variant-fv-02) | The task becomes one known price lookup from an authorized source. One scoped agent is sufficient; decomposition overhead adds no evidence. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.2&variant=FV-02) |
| FV-03 — Send an attributable handoff | [1.3](objectives/objective-1.3.md#variant-fv-03) | New consent evidence invalidates the audience assumption. Send the changed evidence and require a revised conclusion. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.3&variant=FV-03) |
| FV-04 — Bind approval to this action | [1.4](objectives/objective-1.4.md#variant-fv-04) | The target changes to account B or amount changes to 80. Invalidate the prior approval and request the newly scoped authorization. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.4&variant=FV-04) |
| FV-05 — Separate prevention from detection | [1.5](objectives/objective-1.5.md#variant-fv-05) | The requirement becomes preventing an irreversible account mutation. Move the authorization check before execution, in the application or supported pre-tool control. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.5&variant=FV-05) |
| FV-06 — Choose decomposition by uncertainty | [1.6](objectives/objective-1.6.md#variant-fv-06) | The task becomes an open-ended investigation with unknown evidence paths. Use bounded adaptive decomposition and review discovered gaps. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.6&variant=FV-06) |
| FV-07 — Resume with fresh permissions | [1.7](objectives/objective-1.7.md#variant-fv-07) | The learner wants an alternative investigation without replacing the existing trajectory. Fork the session, but revalidate the same mutable assumptions. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.7&variant=FV-07) |

</details>

<details>
<summary>Domain 2: Tool design and MCP integration — 5 decisions</summary>

| Decision | Objective lesson | Apply the contrast | Check yourself |
| --- | --- | --- | --- |
| FV-08 — Make capabilities distinguishable | [2.1](objectives/objective-2.1.md#variant-fv-08) | Two tools both say “manage account.” Rename them and tighten schemas/descriptions so capability boundaries are clear. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.1&variant=FV-08) |
| FV-09 — Route the actual error category | [2.2](objectives/objective-2.2.md#variant-fv-09) | A timeout is transient and read-only. Retry with a bounded policy. A permission refusal instead requires changed authorization or escalation. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.2&variant=FV-09) |
| FV-10 — Scope tools to the assigned role | [2.3](objectives/objective-2.3.md#variant-fv-10) | One bounded read-only lookup fits a single agent with two relevant tools. Do not add agents merely to satisfy a tool-count slogan. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.3&variant=FV-10) |
| FV-11 — Separate connection from inclusion | [2.4](objectives/objective-2.4.md#variant-fv-11) | A developer tests a personal server. Keep its configuration in the appropriate personal/local scope instead of committing credentials to the team project. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.4&variant=FV-11) |
| FV-12 — Search before making a scoped edit | [2.5](objectives/objective-2.5.md#variant-fv-12) | A genuinely new standalone artifact has no existing file to patch. Write the new file after verifying its placement and contract. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.5&variant=FV-12) |

</details>

<details>
<summary>Domain 3: Claude Code configuration and workflows — 6 decisions</summary>

| Decision | Objective lesson | Apply the contrast | Check yourself |
| --- | --- | --- | --- |
| FV-13 — Put instructions at their real scope | [3.1](objectives/objective-3.1.md#variant-fv-13) | A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.1&variant=FV-13) |
| FV-14 — Give reusable skills a contract | [3.2](objectives/objective-3.2.md#variant-fv-14) | A single ad hoc explanation is needed. Use a brief rather than creating a reusable asset without repeated need. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.2&variant=FV-14) |
| FV-15 — Load rules for the affected paths | [3.3](objectives/objective-3.3.md#variant-fv-15) | A security policy genuinely applies across the repository. Move that requirement to an appropriate broader scope. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.3&variant=FV-15) |
| FV-16 — Plan when uncertainty crosses boundaries | [3.4](objectives/objective-3.4.md#variant-fv-16) | The task becomes a precise typo in an isolated documented comment. Direct execution and a focused check are proportionate. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.4&variant=FV-16) |
| FV-17 — Change the hypothesis after repeated failure | [3.5](objectives/objective-3.5.md#variant-fv-17) | Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.5&variant=FV-17) |
| FV-18 — Run CI with observable failure | [3.6](objectives/objective-3.6.md#variant-fv-18) | The work becomes independent eligible Messages requests with no local iterative state and a tolerant deadline. Consider batch; an urgent dependent tool loop remains a different runtime. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.6&variant=FV-18) |

</details>

<details>
<summary>Domain 4: Prompt engineering and structured output — 6 decisions</summary>

| Decision | Objective lesson | Apply the contrast | Check yourself |
| --- | --- | --- | --- |
| FV-19 — Define a finding with evidence criteria | [4.1](objectives/objective-4.1.md#variant-fv-19) | The policy wording is ambiguous about mutual termination. Ask for clarification or label the case uncertain instead of treating every termination mention as a violation. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.1&variant=FV-19) |
| FV-20 — Teach the edges with representative examples | [4.2](objectives/objective-4.2.md#variant-fv-20) | A new document population uses credit notes and negative amounts. Revise the example distribution and validate on unseen cases. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.2&variant=FV-20) |
| FV-21 — Validate shape and truth separately | [4.3](objectives/objective-4.3.md#variant-fv-21) | A field truly absent from the source may be null only when the declared contract allows it. A wrong non-null amount does not call for a nullable-only repair. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.3&variant=FV-21) |
| FV-22 — Repair the failed check within a budget | [4.4](objectives/objective-4.4.md#variant-fv-22) | The source itself contains contradictory totals. Preserve both values and route review instead of asking Claude to manufacture reconciliation. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.4&variant=FV-22) |
| FV-23 — Choose batch by dependencies and deadline | [4.5](objectives/objective-4.5.md#variant-fv-23) | A result is needed before the next dependent local tool step or a tight user deadline. Use the appropriate immediate/interactive runtime instead. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.5&variant=FV-23) |
| FV-24 — Give the critic independent evidence | [4.6](objectives/objective-4.6.md#variant-fv-24) | A simple low-risk formatting task has deterministic validation. Extra model passes may not justify their cost. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=4.6&variant=FV-24) |

</details>

<details>
<summary>Domain 5: Context management and reliability — 6 decisions</summary>

| Decision | Objective lesson | Apply the contrast | Check yourself |
| --- | --- | --- | --- |
| FV-25 — Compact the decision state, not just prose | [5.1](objectives/objective-5.1.md#variant-fv-25) | Source consent or policy changes. Refresh the relevant evidence and revise the stored decision state. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.1&variant=FV-25) |
| FV-26 — Honor explicit escalation with context | [5.2](objectives/objective-5.2.md#variant-fv-26) | The customer says “this is frustrating” without requesting a person. Clarify or continue according to the fictional support policy; do not invent an escalation mandate. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.2&variant=FV-26) |
| FV-27 — Propagate partial success without hiding failure | [5.3](objectives/objective-5.3.md#variant-fv-27) | The unavailable source is explicitly optional. Publish a bounded partial answer with the omission and limitations visible. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.3&variant=FV-27) |
| FV-28 — Build a minimal code evidence ledger | [5.4](objectives/objective-5.4.md#variant-fv-28) | The failure crosses the API boundary. Add the adjacent client/server dependencies and contract tests rather than preserving an artificially narrow scope. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.4&variant=FV-28) |
| FV-29 — Test risk slices and review capacity | [5.5](objectives/objective-5.5.md#variant-fv-29) | A review queue exceeds available capacity. Apply a declared overflow policy or reduce scope; do not silently accept low-confidence items. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.5&variant=FV-29) |
| FV-30 — Keep sources through a join | [5.6](objectives/objective-5.6.md#variant-fv-30) | The host offers supported federation. It may simplify retrieval, but still retain origin, time and conflict checks. | [Practice](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=5.6&variant=FV-30) |

</details>

## Transfer the decision across industries

Finance, Legal and Marketing receive dedicated practice below because they matter to this learner. Education and Government extend the transfer. This is a curriculum choice; no official industry weighting is claimed. All inputs and policies are fictional. Use the same Claude mechanisms while changing the business constraints.

### Finance — approved payment changes after review

**Situation:** A treasury assistant proposes a payment of 4,000 units, obtains approval, then receives a corrected invoice for 4,600. The bank request later times out. **Decide first:** May it reuse approval? May it retry the payment?

<details>
<summary>Reveal the worked choice after deciding</summary>

**Worked choice:** Bind approval to the exact target, amount and proposal version. The changed amount requires a new valid approval. An uncertain write requires status reconciliation or a supported idempotency mechanism before another effect; `end_turn` does not prove settlement. A prompt saying “never pay twice” cannot enforce this.

**Changed constraint:** If the system only drafts advice and has no payment capability, a simpler advisory workflow may suffice. **Produce:** an approval-state table and unknown-result branch. [Approval packet](objectives/objective-1.4.md#variant-fv-04) · [Unknown effects](objectives/objective-1.1.md#variant-fv-01) · [Flow D01](decision-atlas.md#diagram-d01).

</details>

### Legal — conflicting contract evidence and a missing specialist

**Situation:** Compare three fictional supplier contracts for retention, exit terms and integration cost. One specialist returns cost; retention evidence is absent and another source contradicts the draft conclusion. **Decide first:** What can be concluded now, and what must be investigated?

<details>
<summary>Reveal the worked choice after deciding</summary>

**Worked choice:** Use explicit shared criteria, source-tagged findings and a coordinator coverage ledger. Preserve useful partial findings, reopen the missing dimension and retain conflicting evidence. Do not call the comparison complete or let a critic certify a conclusion without independent source access.

**Changed constraint:** A single authorized clause lookup may need only one scoped agent. **Produce:** a claim/source/coverage table and a targeted recovery brief. [Coordination packet](objectives/objective-1.2.md#variant-fv-02) · [Independent critique](objectives/objective-4.6.md#variant-fv-24) · [Flow D03](decision-atlas.md#diagram-d03).

</details>

### Marketing — campaign audience, ambiguous fields and a hard launch

**Situation:** A campaign assistant extracts audience attributes from inconsistent briefs. A record has no consent status; a local date is ambiguous; launch is in two hours. **Decide first:** Should it guess fields, send everything to batch, or hold dependent actions?

<details>
<summary>Reveal the worked choice after deciding</summary>

**Worked choice:** Model unknown/missing states explicitly, retain original text and source locators, validate meaning as well as shape, and keep the fictional application's consent prerequisite in executable authorization logic. Batch is appropriate only where its completion characteristics and independence fit the deadline. Do not silently convert missing consent into permission or assume a deadline guarantees completion.

**Changed constraint:** With independent overnight analysis and no launch dependency, batch may become reasonable. **Produce:** three validation outcomes, an audience-exclusion rule and a deadline fallback. [Shape versus truth](objectives/objective-4.3.md#variant-fv-21) · [Batch choice](objectives/objective-4.5.md#variant-fv-23) · [Flow D04](decision-atlas.md#diagram-d04).

</details>

### Education — tutoring history after compaction

**Situation:** A tutor resumes after its long conversation was summarized. The learner's accessibility requirement and unresolved misconception disappeared. **Decide first:** Is a longer context window sufficient?

<details>
<summary>Reveal the worked choice after deciding</summary>

**Worked choice:** Preserve explicit learning goals, constraints, misconceptions, source references and next checks in structured state, then verify that the summary retains them. A larger window cannot recreate omitted facts. **Changed constraint:** For a short session with all relevant facts already present, no elaborate memory workflow is necessary. **Produce:** a before/after context checklist. [Context packet](objectives/objective-5.1.md#variant-fv-25) · [Conversation practice](decision-conversation.md).

</details>

### Government — policy evidence changes during a paused case

**Situation:** An advisory service resumes a fictional permit case after permissions and a policy source changed. A second system returns a conflicting record. **Decide first:** Can it trust saved authorization and silently merge records?

<details>
<summary>Reveal the worked choice after deciding</summary>

**Worked choice:** Revalidate current authority before effects, retain source/time/identifier lineage through the join and surface unresolved conflicts. An MCP connection alone does not establish that the needed capability is included or authorized. **Changed constraint:** A public read-only lookup reduces the action boundary but still needs attributable evidence. **Produce:** a resume gate and source-preserving join. [Resume packet](objectives/objective-1.7.md#variant-fv-07) · [Source join](objectives/objective-5.6.md#variant-fv-30) · [Connection versus inclusion](objectives/objective-2.4.md#variant-fv-11).

</details>

## Go deeper, then test transfer

- [Six complete walkthroughs](scenario-walkthroughs/README.md): trace the tools, state and failures in the saved blueprint's six families.
- [Six extended industry cases](objectives/INDUSTRY-CASES.md): produce design artifacts before reading their review guides.
- [Architecture drawings](decision-atlas.md): inspect branching and recovery beside your decision.
- [Signals and errors](site:lessons/ccar-f/scenario-walkthroughs/signals-and-errors.html): diagnose failures and revisit missed what-ifs.
- [Simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md): rehearse longer decisions before full mocks.
- [Coverage limits](skill-coverage.md): teaching coverage, diagnostic mappings and your demonstrated mastery are different things.

**Exit check:** Explain a base decision, a condition that reverses it, the losing alternative, the enforcing artifact and its recovery path without opening the explanation. Record help used. Revisit a different case later; recognizing an answer you just read is assisted recall.


<div data-assessment-exposure="cct-fv-01-base-v1,cct-fv-01-retry-v1,cct-fv-02-base-v1,cct-fv-02-retry-v1,cct-fv-03-base-v1,cct-fv-03-retry-v1,cct-fv-04-base-v1,cct-fv-04-retry-v1,cct-fv-05-base-v1,cct-fv-05-retry-v1,cct-fv-06-base-v1,cct-fv-06-retry-v1,cct-fv-07-base-v1,cct-fv-07-retry-v1,cct-fv-08-base-v1,cct-fv-08-retry-v1,cct-fv-09-base-v1,cct-fv-09-retry-v1,cct-fv-10-base-v1,cct-fv-10-retry-v1,cct-fv-11-base-v1,cct-fv-11-retry-v1,cct-fv-12-base-v1,cct-fv-12-retry-v1,cct-fv-13-base-v1,cct-fv-13-retry-v1,cct-fv-14-base-v1,cct-fv-14-retry-v1,cct-fv-15-base-v1,cct-fv-15-retry-v1,cct-fv-16-base-v1,cct-fv-16-retry-v1,cct-fv-17-base-v1,cct-fv-17-retry-v1,cct-fv-18-base-v1,cct-fv-18-retry-v1,cct-fv-19-base-v1,cct-fv-19-retry-v1,cct-fv-20-base-v1,cct-fv-20-retry-v1,cct-fv-21-base-v1,cct-fv-21-retry-v1,cct-fv-22-base-v1,cct-fv-22-retry-v1,cct-fv-23-base-v1,cct-fv-23-retry-v1,cct-fv-24-base-v1,cct-fv-24-retry-v1,cct-fv-25-base-v1,cct-fv-25-retry-v1,cct-fv-26-base-v1,cct-fv-26-retry-v1,cct-fv-27-base-v1,cct-fv-27-retry-v1,cct-fv-28-base-v1,cct-fv-28-retry-v1,cct-fv-29-base-v1,cct-fv-29-retry-v1,cct-fv-30-base-v1,cct-fv-30-retry-v1"></div>