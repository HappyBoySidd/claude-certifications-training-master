# Diagram teaching system

The diagram must explain its current focus where the learner is looking. A separate reading panel is supplementary; it is not the required explanation of a highlighted object.

## Shared interaction primitives

`diagram-annotations.js` and `.css` provide one local card surface for application maps, Mermaid reference diagrams, decision-sequence previews and the home route map. Boxes/messages support pointer preview, keyboard focus and touch/keyboard pinning. The card can be entered and its text selected. Close/Escape dismiss it; focus returns to the anchor if it was inside the card. Stage changes remove stale inspection. The inspector uses blue; the stage's teaching focus uses teal and text, never color alone.

Desktop cards use available space beside the anchor without covering the anchor or active endpoints. Where that cannot fit, a named inset appears within the same visual surface. Mobile uses that inset rather than a tiny tooltip. Zoom, pan and resize recompute placement. Hover and keyboard previews do not move the page. An explicit selection brings a docked local inset into view; there is no modal focus trap.

## Authored application teaching

- Every component has a permanent short purpose, separate from its technical name.
- Every highlighted component has a phase-specific `Why this matters now` explanation within its box. It describes the present setup/failure or the revealed repair, not a later state. Mobile repeats this explanation in a 14px HTML inset directly above the canvas.
- Hover/focus/tap inspection provides purpose, input, output and owner beside the selected box. The stage's teal teaching focus remains distinguishable from blue inspection.
- An arrow explains its direction, data/instruction and receiving boundary at the arrow. Fictional contracts remain labeled; stage evidence establishes only the worked example's observed state.
- New storyboards must supply purposes and exact setup/repair focus-note mappings. Build validation fails for missing, empty or mismatched metadata.

## Reference diagram families

Existing reference diagrams retain their authored content. Flowcharts, state charts and sequence messages gain local inspection of their labels and related source statements. The viewer marks this as source-derived context; it does not fabricate component responsibilities, API contracts or progression notes. Decision preview and route-map annotations retain existing navigation semantics.

When a reference diagram becomes a guided teaching sequence, its author must add explicit purpose, state/condition, changed requirement, why-now note and evidence for each teaching step. Mechanical extraction is not equivalent to an authored explanation.

## Acceptance checks

1. Explain the teaching focus without looking at the right-hand panel.
2. Read the purpose of every application box without clicking.
3. Hover/focus/tap any box or arrow and obtain a matching local card.
4. Enter and select text in the card; close it without losing keyboard position.
5. Verify setup and repair wording separately, including AS01 stage three's ambiguous versus separated tool interfaces.
6. Verify desktop, intermediate width and touch layout, normal and fit views, edge anchors, pan/zoom and stage changes.
7. Render every affected diagram page and sample actual flow, state, sequence, preview and route-map views.
8. Preserve source content, graded question identities and learner progress. Record source-derived coverage separately from authored semantic coverage.

## Plain language and exact technical bridge (B-111)

A plain explanation alone does not satisfy technical teaching acceptance. Keep it beside an exact mechanism name and classified artifact: real API content block, CLI/configuration fragment, protocol message, or explicitly application-owned pseudocode. Include Read it as and Does not establish. Visible application subtitles use precise technical roles; local cards expose exact terms and related examples. Current-stage bridges must use current-stage facts, with setup distinct from repair. Section-level related objective examples are labeled as separate learning examples, not fabricated current execution traces.

Source review checks protocol field shapes and meanings, including response metadata versus request messages. Visual review checks that the two lenses are readable at the learner's location. Assessment review checks that graded mock assistance appears only after commitment/review. Route presence is not semantic coverage of every skill bullet.


## B-112: Selection means study; hover means preview

A pinned explanation must always occupy the diagram column's full width with16px body/14px code and natural body height. Hover previews contain only title/purpose and never replace the persistent trace. Explicit selection has keyboard focus, Close/Escape and focus return. It survives outside clicks.

Every application component and unique handoff has an authored boundary uncertainty plus a plain relevance statement. Show a clearly labelled related technical decision using that decision's own fixture; never combine a future scenario's premise with the current state. Preserve actual original options and gate rationale until choice. Context-only boundaries state why no independent question exists. A worked-layer jump is explicit and offers return to the original stage/phase/connection. The local exercise never marks mastery or writes progress.

Acceptance separates readability, semantic mapping, technical authenticity, discoverability and assessment behavior; a card that fits geometrically or mentions API terms does not by itself pass these gates.


## Audience comprehension gate (AS03 pilot feedback, 2026-10-22)

Every new or materially changed learner-facing page requires an independent Audience comprehension editor / learner advocate, alongside the Claude Architect and Developer. Review the rendered diagrams, narration, choices, artifacts and answer feedback in all affected states. A learner must identify the real-world object, actor, task and failure without decoding an unexplained ID. Introduce a descriptive noun before a stable technical identifier; distinguish entity identity from document revision, permissions and state. Use one naming glossary across fixtures and cross-links. Technical question terminology stays precise; plain explanations connect it to the scenario. Do not predict the actual exam’s wording from a training example. Confusing referents or a mismatch between the current scene and its labels block acceptance. Use EDITORIAL-GATE.md in the pilot evidence for the detailed checklist. A mechanical page-count pass cannot replace this review.

Official-course links must state what is demonstrated locally, what is a companion and what lies elsewhere. A foundation path or a source link does not establish full syllabus coverage or an exam prerequisite. Check course catalog summaries and technical claims separately; do not claim to have reviewed complete course lessons from their titles.


## Thread capabilities and AI Fluency into each scenario (pilot contract)

Each authored learning layer connects four things in its current context: what the model can do or what limitation is observed; why a specific Delegation, Description, Discernment or Diligence judgment matters; how the application/prompt/code/person responds; and what observable evidence supports the outcome. Name the capability property when helpful (knowledge, plausible generation, working memory/current context, steerability), then explain it using the same user request and data. Before a teaching choice, HOW asks the diagnostic question; after a choice it shows the repair and actual outcome. A failed read stays failed. Include this same causal explanation in optional narration, with no added compulsory connection clicks. Course links supplement the explanation; they do not substitute for teaching it. Pilot implementation covers AS03, and wider adoption requires separate reviewed evidence.


## All-path applied architecture review (AS03 pilot)

For each official path course, record an actual scenario decision, reason, concrete mechanism/design artifact and required evidence. An optional course link is not application. Apply product/entry point/model/context/decomposition choices before the first request; integrate API/MCP/capability/fluency decisions in the corresponding failure layers; close with Code implementation, deployment/data boundaries and delivery validation. Do not add components merely to match a catalog. A conscious not-needed decision must state its trigger for reconsideration. Preserve coverage while keeping the default page concise; technical alternatives, evidence and scope remain accessible. Distinguish original scenario teaching, source summaries, actual runtime evidence and exam objectives. A full-course-completion or exam-readiness claim requires separate evidence.
