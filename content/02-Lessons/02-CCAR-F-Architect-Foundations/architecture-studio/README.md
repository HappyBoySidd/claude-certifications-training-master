# Learn to think like a Claude application architect

**Begin with a work problem, not a pattern name.** Imagine a support representative asking, “This order arrived damaged; can we give the customer a $120 credit?” A screen, program, records, Claude and a payment interface cooperate to investigate and handle that request. Together they form an application. We call this example **Customer Refund Assistant**; “action service” is its technical pattern label, explained after the example.

## How each situation grows

Start with a small application that works. Watch one specific input break it. Read the **technical original exam-style question and options first**, then use the optional plain-language help if needed. Choose before opening the answer. The answer explains the repair in everyday language, shows what changed in the data path and asks what evidence would prove success. Then change one constraint and decide again.

You do not need to memorize JSON or learn every tool before starting a story. A returned record, tool setting, instruction file or checkpoint appears only when the application needs it. Each example says what to read and who uses it. The lab and simulation continue the same architecture decisions.

## Your first 15 minutes — get the picture, not finish the course

1. Open [the primer's refund-assistant example](00-foundations.md#start-with-something-you-can-picture-a-customer-refund-assistant). Read the problem and identify the whole application and its parts.
2. Follow [one request through the data-flow table and drawing](00-foundations.md#follow-the-same-request-from-the-screen-to-the-receipt): the customer’s message → order record → proposed USD 120 credit → saved receipt. The C17/O4/CR1 labels help trace the same records; you do not need to memorize them. Read the technical names next to the familiar parts; no installation is required.
3. Say in your own words what Claude proposes and what the backend must check. If the picture is still unclear, repeat that one example with a coach rather than opening more reference pages.
4. Continue with [AS-01: help a customer with a damaged order](AS-01-action-service.md). On your first pass, read the request and worked decisions; return to its exercise and technical artifact after the flow makes sense.

Fifteen minutes is an introductory pass, not a completion promise. The deeper case work suggests 45–75 minutes per application plus labs; use shorter sessions when helpful. **Recommended first sequence:** primer → AS-01 → AS-02 (invoice intake) → AS-03 (answers from approved documents). Then continue to the remaining cases. Treat the longer index below as a route to return to, not a list to memorize before starting.

You are learning to connect a recognizable requirement to technical choices: who interprets, who checks, what data moves, what changes, and what evidence proves the outcome. These eight original teaching applications supplement the saved guide's six scenario families; the layers overlap. They do not forecast every exam story.

## How this course teaches both levels

Each application states its prerequisites and reading/paper mode before the scenario. A plain-language → technical-choice table connects the business decision to documentation terms, alternatives and the deciding signal. Every artifact explains why it appears, what to inspect and whether it runs. Read the worked choice in both vocabularies before attempting transfer questions; do not treat examples as setup commands. See [how to read technical examples](00-foundations.md#how-to-read-technical-examples-in-this-course).

<a id="first-build-the-mental-picture"></a>

## Eight complete application scenarios

Start with the story and input/output. Read the pattern name afterward; it is a way to recognize the same kind of problem in another industry. All examples are fictional and correspond to the linked lessons.

| Start with a recognizable work problem | What comes in → what you get back | Technical pattern and decisions you will learn |
|---|---|---|
| 1. [Help a customer with a damaged order](AS-01-action-service.md) | “Order O4 arrived damaged; credit $120” + case/order records → an authorized credit receipt, or a clear reason no credit was issued | **Action service:** interpret, verify, enforce prerequisites, act and reconcile uncertain outcomes |
| 2. [Turn a received invoice into a reviewable accounting record](AS-02-document-pipeline.md) | Invoice EL-8, total USD 84.50, no PO shown → fields containing 8450 cents and explicit missing PO, plus validation/review status | **Document pipeline:** schema, null/omission, source meaning, normalization and targeted repair |
| 3. [Help a technician find the approved instruction](AS-03-grounded-assistant.md) | “How long should unit M4 cool?” + authorized manual excerpts → an answer citing the right revision/page, or an explicit evidence gap | **Grounded assistant:** retrieval, MCP tools/resources, permissions, provenance and context inclusion |
| 4. [Help an operations owner decide what to pilot](AS-04-research-system.md) | Warehouse mobile-workflow question + connectivity, glove-use and training evidence → a supported pilot recommendation with remaining gaps | **Research/coordinator system:** single investigator, routing, parallel work or adaptive specialists |
| 5. [Fix a booking report that treats missing deposits as zero](AS-05-code-change.md) | Defect request + importer/caller/test files → a proposed patch and checks preserving unknown versus zero | **Code-change assistant:** search/read/edit tools, instruction scope, refinement and change evidence |
| 6. [Review a proposed code change without waiting for a person](AS-06-ci-review.md) | Changed lines, business contract and tests → structured, evidenced findings or a declared review failure; no automatic merge | **Unattended CI reviewer:** execution mode, permissions, output contract and independent review |
| 7. [Answer a waiting clerk now and process the archive later](AS-07-work-queue.md) | One urgent invoice question + 500 archived invoices → an immediate clarification result and separately validated deferred results | **Mixed work queue:** synchronous versus staged/batch work, deadlines, per-ID failures and safe replay |
| 8. [Continue a paused dispute without issuing a second refund](AS-08-resumable-case.md) | Saved C-41 dispute, changed policy/amount and unknown OP-6 → refreshed evidence and reconciled status, then current authorization or handoff | **Resumable case service:** durable state, freshness, scoped approval, measured risk and review capacity |

## Repeat the same learning cycle

1. Read the business request and identify the non-negotiable outcome. Define a measurable result before naming tools.
2. Predict the design. Mark each decision as model judgment, application code or a human policy decision. Some steps combine all three.
3. Follow the worked sequence and drawing. Ask why this order is necessary and which steps are independent.
4. Inspect the prompt, schema, instructions or code contract. A tool name without a meaningful contract does not explain an architecture.
5. Run the [local architecture decision lab](../../../06-Labs/08-CCAR-F-architecture-decisions/README.md). Predict outputs before executing; it simulates deterministic controls, not a live Claude deployment.
6. Close the lesson and attempt its simulation and three new formative questions. Open the coach key only after deciding.
7. Reverse one constraint and explain whether the winning design changes. Then use the linked existing targeted practice and recall tools.

Each case includes a listening/conversation script. Ask your assistant to read it one question at a time and wait for your answer. These are scripts, not newly recorded audio files or an automatically running voice tutor.

## What counts as understanding

Use this original practice rubric for each case:

- **Outcome:** explain what successful business completion means, separately from a model finishing a turn.
- **Boundary:** identify the decision delegated to the model and the predicate enforced by code.
- **Sequence:** explain prerequisites and which steps can safely run together.
- **Artifact:** show the actual prompt, tool contract, validation rule or instruction location.
- **Failure:** name what is known, unknown and unsafe to repeat.
- **Transfer:** change a constraint and justify the new design, including when a simpler solution wins.

Score each dimension as 0 (not explained), 1 (correct with help), or 2 (correct without help). This is an unvalidated formative rubric out of 12, **not an exam score or booking threshold**. Keep the first attempt and a later different-case attempt separate. No completion is assumed from opening a page.

The existing case self-checks and the new layered reading checks are original formative exercises, including ordering and multiple-response practice. They are **separate from the hosted mock bank**, do not automatically add diagnostically validated skills, and do not update the practice app's accuracy. Keep that distinction visible when recording progress.

## Connect to your existing preparation

[Orientation](../L00-orientation.md) · [Scenario learning studio](../scenario-studio.md) · [Official objective lessons](../objectives/README.md) · [Full simulations](../../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) · [Reference drawings](../decision-atlas.md) · [Recall cards](../FLASHCARDS.md) · [Coverage and its limits](../skill-coverage.md)