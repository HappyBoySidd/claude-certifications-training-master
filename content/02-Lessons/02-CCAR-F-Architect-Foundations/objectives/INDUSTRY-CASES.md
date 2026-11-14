# Production transfer cases for all 30 CCAR-F objectives

These six synthetic cases teach how a Claude architecture changes when constraints change. They are project-authored exercises, not customer implementations, exam questions or predictions of exam difficulty. All names, data, limits and targets below are invented training inputs. They pair with the objective lessons, rather than replacing them. Sources support the Claude mechanisms; business designs and targets are our teaching choices. Expected decisions are examples of defensible reasoning, not the only possible architecture.

Allow 45–75 minutes per case for a written design and failure trace. All six add approximately 4.5–7.5 hours of production-depth practice beyond the introductory module route. No learner completion is assumed. Read each case, produce your answer, and only then use the review guide. Keep implementations in a synthetic local sandbox.

## Case A — Insurance: claims extraction with binding approvals

**Objectives:** [1.4](objective-1.4.md), [1.5](objective-1.5.md), [4.3](objective-4.3.md), [4.4](objective-4.4.md), [5.5](objective-5.5.md).

**Situation.** Three document classes arrive: a structured claim form, a scanned repair estimate and a free-form policy endorsement. A claims assistant must produce a proposed payment, with source references. It may prepare a proposal but cannot authorize payment. Reviewers can inspect only 100 of 1,000 incoming documents per day. Dates arrive as ISO strings, epoch values and local-language dates; “coverage not found” is different from “coverage lookup unavailable.”

**Competing designs.** A single prompt that extracts all fields and says “never pay without approval” is cheaper to build and useful for an advisory prototype. A controlled pipeline separates extraction, normalization, validation, policy lookup and approval; it costs more engineering and latency but provides explicit failure and authority boundaries. The requirement concerns effects, so backend prerequisites—not merely model cooperation—control those effects. Strict schema constraints can improve tool input shape; source interpretation and business rules still need validation. Do not replace a missing policy fact with a schema-valid guess.

**Worked decision.** Use a schema with explicit missing/unknown states and source evidence, normalize only values whose meaning is known, and validate cross-field consistency. Normalize Unix/ISO timestamps in a post-tool stage; preserve ambiguous dates and original text for review. A payment prerequisite checks verified identity, validated proposal and a current authorized approval. The approval is tied to the proposal version so a later amount change cannot reuse it. That last version-binding control is production enrichment, not a quoted blueprint requirement.

**Failure injection.** The endorsement says the limit changed but the policy service returns last year's rule. Another document contains an impossible total. A third has a confident extraction with no supporting page. Show which are retried with useful validation feedback, which are held for review, and which stop authorization. Set a bounded retry policy for recoverable extraction errors; repeating the same malformed input does not create evidence.

**Produce.** A state diagram; an extraction schema; a normalization table retaining raw values; three validation results; and a review-routing proposal segmented by document type and field. Calibrate any model confidence thresholds on labeled examples. For the synthetic numbers, state what happens when more than 100 records require review; a full queue must not silently lower safety requirements.

**Review guide.** A strong answer keeps syntax, correctness and authority separate; routes unsupported/contradictory fields to review; measures each document class and critical field; and blocks downstream effects. Raising confidence thresholds blindly or measuring only overall accuracy is insufficient. If the workflow becomes advisory with no payment tool, a simpler prompt-based prototype may be reasonable.

**Sources:** official guide section 6 tasks 1.4, 1.5, 4.3, 4.4, 5.5 (Tier 1); [SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks); [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs). [DXC's published story](https://claude.com/customers/dxc) provides insurance context only; this design is synthetic.

## Case B — Logistics: inventory reservation under partial failure

**Objectives:** [1.1](objective-1.1.md), [2.1](objective-2.1.md), [2.2](objective-2.2.md), [2.3](objective-2.3.md), [5.3](objective-5.3.md).

**Situation.** A dispatch assistant must check stock, reserve an item and find a carrier. One warehouse is intermittently unavailable; another returns “insufficient stock.” A planning agent needs reads; a booking agent can write reservations. The user wants a result within 20 seconds. A network timeout occurs after the warehouse may already have accepted a reservation.

**Competing designs.** Give every agent all 18 tools and let prompts choose safely, or expose scoped contracts for each role. The shared pool is simple and may suit a small read-only experiment. Scoping reduces accidental choice and action surface, but handoffs must carry enough context and the server must still authorize calls. Forced tool selection can ensure a required extraction tool is chosen in the appropriate mode; it cannot repair an ambiguous tool contract or grant warehouse permission.

**Worked decision.** Separate `lookup_stock`, `reserve_stock` and `get_reservation_status`, with inputs, outputs, boundaries and meaningful error categories. Keep the coordinator's message history consistent: append assistant tool requests, then the corresponding results by tool-use ID, and continue using the structured stop reason. End-turn means the model ended its turn; it is not evidence the external reservation succeeded. Handle truncation or incomplete tool requests separately. Verify an uncertain write before retrying; an idempotency key or equivalent application control is production enrichment.

**Failure injection.** Return: (a) transient lookup timeout, (b) insufficient stock, (c) expired token, (d) reservation timeout with unknown commit status. State the next action for each. Do not retry business/permission failures unchanged. Do not return “all warehouses empty” when one warehouse is unavailable. Preserve successful partial findings and source coverage limits through the coordinator.

**Produce.** Two role tool lists and a scoped shared verification tool; descriptions for two similar tools that avoid keyword overlap; a loop trace with two tool calls in one turn; structured MCP execution-error results; and a partial-success coordinator report. `isError` is protocol-defined; application fields such as `errorCategory` and `isRetryable` are your documented contract.

**Review guide.** A strong answer distinguishes model loop completion from system success; treats unknown commit status as uncertainty; preserves unavailable-source evidence; and chooses retries based on category and deadline. When all tools become read-only and few in number, a wider shared tool list may be acceptable. Backend authorization remains necessary in either case.

**Sources:** guide section 6 tasks 1.1, 2.1–2.3, 5.3; [stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons); [tool definitions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools); [MCP tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) (Tier 1). This is an original logistics case.

## Case C — Manufacturing: supplier-risk research with changing scope

**Objectives:** [1.2](objective-1.2.md), [1.3](objective-1.3.md), [1.6](objective-1.6.md), [1.7](objective-1.7.md), [5.6](objective-5.6.md).

**Situation.** A procurement analyst asks whether a component supply is resilient. One request is a simple stock lookup; another requires technical qualification, lead times, geographic exposure and contradictory dated supplier reports. Research has a fixed token budget. A supplier announcement changes midway through the investigation. Two alternative sourcing strategies should be compared from the same initial findings.

**Competing designs.** A fixed five-agent pipeline offers predictable scope and easy execution tracing. A coordinator that selects workers by query complexity avoids unnecessary calls and can investigate discoveries. The coordinator must not shrink a broad resilience question into only a price lookup. Independent workers reduce context load but can lose attribution and duplicate searches if the brief is vague.

**Worked decision.** For the simple lookup, use one bounded worker. For resilience research, partition by technical qualification, supply/lead-time evidence and exposure. Give each worker the objective, boundaries, source expectations, output format and selected prior findings. Route the results through the coordinator; explicitly pass the relevant evidence to synthesis. Require claim-source-date records and distinguish observed facts from inference. If source dates or methodology differ, annotate that before treating numbers as a conflict. The coordinator checks uncovered dimensions and launches targeted follow-up work rather than repeating everything.

**Failure injection.** A worker returns a report without collection dates; another is overloaded and times out; a resumed session contains now-stale supplier data; a fork receives an incomplete starting summary. Explain which evidence is reusable and which must be re-read. Forking creates an independent exploration branch; it does not grant shared live memory or make stale tools current.

**Produce.** A complexity-based delegation plan for both requests; three worker briefs; one structured evidence packet; a coordinator gap-check; a resume-versus-fresh-summary decision; and two branch plans with isolated outputs. Include a final report that retains contested values, methodology and dates, with tables for numeric comparisons and prose for interpretation.

**Review guide.** A strong answer passes complete relevant findings without dumping unrelated transcripts; chooses workers by need; preserves gaps and provenance; re-analyzes changed sources; and makes branch outputs comparable. A fixed chain wins when the required checks are stable and dependencies known. Dynamic decomposition wins when evidence changes what needs investigation.

**Sources:** guide section 6 tasks 1.2, 1.3, 1.6, 1.7, 5.6; [multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system); [SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions); [citations](https://platform.claude.com/docs/en/build-with-claude/citations) (Tier 1). Original manufacturing research case; no supplier facts asserted.

## Case D — Healthcare software: governed repository changes

**Objectives:** [3.1](objective-3.1.md), [3.2](objective-3.2.md), [3.3](objective-3.3.md), [3.4](objective-3.4.md), [3.6](objective-3.6.md).

**Situation.** A synthetic administrative scheduling product has separate API, web and migration directories. API conventions should load for relevant files; web conventions differ. A shared report-only command must work for every developer. The change spans authentication, schema migration and clients. CI must create a structured review artifact without modifying production or leaking credentials.

**Competing designs.** Put all conventions, procedures and permission wishes into one large CLAUDE.md, or use scoped project memory, conditional rules, reusable skills and enforced permissions. A single short file suits a small repository. Modular scope becomes useful when rules are numerous or component-specific; splitting a global rule accidentally can make it disappear from relevant contexts.

**Worked decision.** Keep cross-project essentials in appropriate project memory; load component conventions by path patterns; use imports for reusable instructions and verify team availability. Put the shared procedure in the repository's skill/legacy-command structure, distinguishing the July exam description from current docs. `allowed-tools` in a current skill is a permission grant, not an availability restriction. Enforce report-only behavior using documented permission/restriction mechanisms and CI boundaries, not its name. Explore and plan the cross-component change before making edits; direct execution is reasonable for a small verified local change. Run noninteractive CI with structured output and independently validate its schema and exit behavior.

**Failure injection.** A nested instruction contradicts the root; a rule includes only `*.ts` although the relevant file is deeper; a developer has a personal command absent from CI; an untrusted pull request contains instructions to print a secret. Trace which configuration loads, and where the effect is prevented rather than requested away.

**Produce.** A file tree showing memory/rules/skill placement; two conditional path rules; an import-availability check; a planning brief; and a CI design documenting tool permissions, synthetic inputs, credential scope, output validation and human review before merging. Do not claim the paper design ran successfully. Verify exact flags and frontmatter against the current docs before implementation.

**Review guide.** A strong answer separates guidance from controls, shared from personal configuration, conditional rules from directory placement, and planning from irreversible execution. It checks redundant review comments against existing feedback before posting. All clinical/patient data are absent: this is software architecture rehearsal, not clinical advice.

**Sources:** guide section 6 tasks 3.1–3.4, 3.6; [memory](https://code.claude.com/docs/en/memory); [skills](https://code.claude.com/docs/en/skills); [programmatic execution](https://code.claude.com/docs/en/headless) (Tier 1). [League's published engineering story](https://claude.com/customers/league-qa) is context, not evidence for this configuration.

## Case E — Legal operations: bulk review without burying exceptions

**Objectives:** [4.1](objective-4.1.md), [4.2](objective-4.2.md), [4.5](objective-4.5.md), [4.6](objective-4.6.md), [5.2](objective-5.2.md).

**Situation.** A fictional organization reviews 2,000 agreements overnight. Documents vary in formatting, and a clause may refer to a schedule in another document. Review must flag material contradictions without drowning lawyers in stylistic suggestions. Routine low-risk questions should be answered; ambiguous obligations and explicit requests for human review require escalation. The deadline is 8 hours, not 24.

**Competing designs.** One global review of all text maximizes shared context but dilutes attention and makes source verification hard. Per-document passes followed by a cross-document review isolate local findings while preserving integration checks. A batch endpoint reduces cost for independent asynchronous work but cannot guarantee an 8-hour completion deadline. A bounded interactive fallback may be worth its higher cost for critical residual work.

**Worked decision.** Specify which issues matter, severity criteria and acceptable exclusions. Add positive, negative and varied-format examples, including when to return no issue and how to preserve source spans. Keep the validation set separate. Run local analysis, then the cross-document pass, then targeted verification of uncertain findings. Reconcile batch results by custom ID; identify successful, errored, canceled and expired outcomes individually. Set a cutoff early enough to route critical unfinished work through a valid fallback or human process. Escalation criteria include unsupported interpretation, missing authority and explicit human request; frustration alone is not a sufficient classifier.

**Failure injection.** A clause looks inconsistent until its referenced schedule is read; one malformed document fails; three results arrive out of order; a batch is unfinished near the deadline; a user requests a human for an otherwise easy issue. Show what is retried, suppressed, annotated or escalated, without counting missing output as success.

**Produce.** A review rubric, varied few-shot examples, a per-document and integration-pass plan, a result-reconciliation table, deadline fallback plan, and an escalation decision tree with both resolve and escalate examples. Explain what a confidence score does and does not prove. For a small isolated contract, the multi-pass design may be unnecessary overhead.

**Review guide.** A strong answer tests prompt precision, preserves “no issue” outputs, examines references, keeps first-pass reviewers from certifying their own unsupported findings, and respects explicit escalation requests. It does not equate schema validity or an empty finding list with a correct review.

**Sources:** guide section 6 tasks 4.1, 4.2, 4.5, 4.6, 5.2; [prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview); [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) (Tier 1). [Spellbook's published story](https://claude.com/customers/spellbook) gives industry context; no legal conclusion or proprietary workflow is reproduced.

## Case F — Retail software: recoverable investigation and MCP tools

**Objectives:** [2.4](objective-2.4.md), [2.5](objective-2.5.md), [3.5](objective-3.5.md), [5.1](objective-5.1.md), [5.4](objective-5.4.md).

**Situation.** A fictional retailer has a large mixed-language repository and an intermittent pricing defect. Investigation spans sessions. An inventory MCP server is shared by the team while an experimental server is personal. The previous run crashed after analyzing 40 files; three files have since changed. Customer restrictions and investigated hypotheses must survive compaction.

**Competing designs.** Read the entire repository and every server tool into one session, or first locate relevant paths and symbols, inspect focused slices and preserve structured findings. Broad loading can be simplest for a genuinely tiny project. In a large repository, breadth-first mapping plus targeted inspection avoids wasting context and repeating completed work.

**Worked decision.** Use Glob for file paths, Grep for content, Read for inspection, Edit for precise changes, Write for new/full-file content and Bash for commands whose effects and permissions you understand. Refine an edit using diagnostics and tests, not a vague “do better” prompt. Register the shared MCP server at the appropriate project scope, keep experimental configuration personal, and supply secrets through supported environment references. Save an investigation manifest with paths, version/hash identifiers, hypotheses, findings, status and next step. On resumption, compare identities and re-open changed files before reusing conclusions. Preserve user requirements, order/transaction identifiers, decisions and unresolved questions in a structured context summary; verify it did not compress away an important constraint.

**Failure injection.** A file changes after its analysis, a tool becomes unavailable, a summary loses “never change advertised prices,” a broad edit changes unrelated lines, and a test failure points to a different component. Reprioritize investigation from evidence rather than rerunning all 40 files or trusting stale notes.

**Produce.** A tool-selection trace; shared/personal MCP config sketch; redacted environment configuration; an investigation manifest; a before/after compaction checklist; and an iterative patch/test plan. Explain what evidence supports closure and what remains untested. The manifest design is original production enrichment supporting the guide's recovery topic.

**Review guide.** A strong answer chooses tools by purpose, preserves critical state, validates changed files, avoids repeating confirmed work unnecessarily and verifies patches with relevant tests. A larger context window may help some tasks but cannot make stale findings current or restore facts that were never passed in.

**Sources:** guide section 6 tasks 2.4, 2.5, 3.5, 5.1, 5.4 and recovery appendix; [MCP](https://code.claude.com/docs/en/mcp); [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Tier 1). Original retail engineering case.

## Evidence to retain

For each of the five objectives in a case, record the relevant output section, first-attempt reasoning, corrected reasoning, help used and a changed-constraint answer. Reading the review guide first counts as assisted practice. Successful paper reasoning does not count as an executed lab. Each objective needs further unseen checks before a mastery claim. This pack ensures all 30 have production-transfer opportunities; it does not guarantee a pass or close the untagged question-bank gap.

## Practice changed constraints

Use the [decision atlas](../decision-atlas.md) to compare the base choice, changed constraint and failure path. Finance changes approval, monetary consistency and source-age risk; Legal changes evidence attribution, privilege/access and ambiguity; Marketing changes consent, segment criteria and false-positive cost. These are synthetic transfer contexts, not official industry weightings. Keep the underlying Claude mechanism explicit.