# Objective 3.5 — Apply iterative refinement techniques for progressive improvement

[Test this decision with a supplied example](#benchmark-exercise-3-5) — predict first, then compare the fixed-fixture evidence.

**Picture the application:** An importer turns missing quantities into zero, producing totals that look complete but change the data’s meaning. The developer needs examples and checks that preserve missing, zero and numeric-string cases correctly. Iterative refinement is the technical process for turning a vague cleanup request into observable behavior.



**Exam:** CCAR-F · **Domain 3:** 20% of exam; no separate objective weight is published here.  
**Time:** 30–40 minutes foundation/applied; 15–25 additional minutes production extension.  
**Prerequisites:** 3.4 scope decisions and basic behavior tests. New to the Claude API? Start with the [five-minute primer in Lesson 0](../L00-orientation.md#five-minute-primer-how-a-claude-app-works).  
**Continue from:** [Domain lesson](../L03-claude-code-configuration-and-workflows.md) · [Objective map](../../../01-Curriculum/02-Architect-Track/CCAR-F-objectives.md).

**Official task statement:** Apply iterative refinement techniques for progressive improvement


<!-- layered-episode:FV-17:start -->
<a id="learn-fv-17"></a>
### Learn the decision in context — FV-17

**Picture the job.** The same date keeps coming out wrong even after the assistant was asked twice to try again. This is an original fictional teaching scene, not a recalled live exam question. Read and trace it; no account, installation or API call is required.

**Start small.** Follow the ordinary route: a person supplies a request or record, software passes the needed evidence to the assistant, and a receiving service or person checks the result. The first demonstration assumes the input, access and evidence are suitable. Now remove that assumption in the situation above. Predict what the receiver would see before choosing a repair.

**Original exam-style practice — choose ONE.** Repeated identical retries preserve a locale-dependent parsing failure. Which refinement is most useful?

A. Repeat make it better until the model changes its answer.

B. Provide the actual fixture, locale, expected result and failing assertion, then investigate a changed hypothesis and rerun neighboring cases.

C. Increase iteration count and treat effort as evidence of improvement.

<details>
<summary>What is this asking? Plain-language help, without the answer</summary>

Identify what the application needs to trust, what has actually been observed, and what remains unknown. Compare the choices against this situation, rather than choosing the most complicated design. A proposal is an intended action; evidence is what you can point to; a contract says what the receiving part expects. Decide which option fixes the stated failure without pretending another requirement has also been solved.

</details>

**Choose before opening the walkthrough.** Say your answer and the closest alternative aloud, or record them in your own notes.

<details>
<summary>Reveal the repair, evidence and changed condition</summary>

**Answer: B.** Provide the actual fixture, locale, expected result and failing assertion, then investigate a changed hypothesis and rerun neighboring cases.

**Walk it through.** For 03/04 under en_GB, the expected April 3 result is compared with the observed March 4 result. The corrected rule must also pass nearby dates.

**Why the alternatives fail here.** Repeat make it better until the model changes its answer. This leaves the stated boundary or evidence requirement unsatisfied. Increase iteration count and treat effort as evidence of improvement. This also fails to establish the required result. The closest competing mechanism fails for this specific reason: More iterations do not imply learning. Narrow evidence and hypothesis changes matter more than request length.

**Inspect the small artifact.** This is an illustrative application-state note for reading, not an SDK signature or executable configuration. The application or workflow owner creates it; the receiver uses it to distinguish what is known from what still needs checking. Its labels describe this scene; do not paste it into Claude settings.

```text
feedback={input:03/04,locale:en_GB,expected:2026-04-03,actual:2026-03-04,check:date_locale}
```

**Layer added.** AI reasoning proposes, selects or summarizes where the job needs judgment. Ordinary software checks identifiers, permissions, required fields, recorded outcomes and stop conditions where applicable. A human resolves a policy or evidence gap when the story requires it. Inspect which owner actually supplies the evidence in this scene.

```mermaid
flowchart LR
 N0["Failing date fixture and locale"] --> N1
 N1["Compare expected April with observed March"] --> N2
 N2["Investigate changed parsing hypothesis"] --> N3
 N3["Apply focused correction"] --> N4
 N4["Rerun fixture and neighboring cases"]
```

**Change one condition.** Keep the application in mind and consider the new situation below. Choose before opening its explanation.

**Technical transfer question — choose ONE.** The only refinement request is make it better. What is needed first?

A. A reproducible expected outcome and observable criterion.

B. More unmeasured iterations until the answer looks different.

<details>
<summary>Transfer check</summary>

**A.** Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign. Name the changed fact before naming a tool. Preserve unrelated access, source-validation and result checks.

</details>

**Recall in ordinary language.** What broke? Who can fix it? What observable result proves the repair? If you cannot answer all three, replay the concrete scene rather than memorize the option letter.

</details>

**Continue from this decision:** [objective 3.5](objective-3.5.md) · [inspect its decision map](../decision-atlas.md#diagram-d12) · [targeted practice](../../../practice/index.html?exam=CCAR-F&objective=3.5). Existing mapped question IDs: `cct-fv-17-base-v1`, `cct-fv-17-retry-v1`. The new guided question above is separate from those stored items and does not change their answers or progress.
<!-- layered-episode:FV-17:end -->

## Read this objective in both vocabularies

For reading and paper reasoning, no installation or credentials are needed. Keep this page's stated concept prerequisites; any runnable challenge still needs its own setup. If an implementation example feels abrupt, first read [how to interpret its artifact type](../architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course), then use the relevant application bridge: [AS-05 decision bridge](../architecture-studio/AS-05-code-change.md#connect-the-simple-explanation-to-technical-design-choices).

Explain the business purpose first, name the precise mechanism second, and distinguish it from the nearest plausible alternative using the stated constraint. Return here for the objective-specific protocol, options and practice. The bridges are teaching aids, not additional official objectives.


## Big idea

Make improvement observable. Examples express meaning, tests express acceptance and interviews reveal missing decisions before code makes them expensive.

## Foundation

### 3.5-K1

**Blueprint focus:** Concrete input/output examples as the most effective way to communicate expected transformations when prose descriptions are interpreted inconsistently

A phrase such as “normalize empty values” leaves multiple valid interpretations. Concrete input/output pairs remove that ambiguity: null may remain null, an empty string may become null and zero may remain zero. Include examples that differ on the exact boundary you care about.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-K2

**Blueprint focus:** Test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement

Tests written before implementation give iteration a stable target. Cover normal behavior, edge cases and a measurable performance constraint when performance matters. A failing test identifies the remaining mismatch more precisely than telling Claude that the implementation still feels wrong.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-K3

**Blueprint focus:** The interview pattern: having Claude ask questions to surface considerations the developer may not have anticipated before implementing

An interview asks Claude to surface questions before proposing a solution. In an unfamiliar caching design, ask about invalidation, stale reads, concurrency and failure behavior. Answering those questions makes the requirements explicit; the model should not invent product policy on your behalf.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-K4

**Blueprint focus:** When to provide all issues in a single message (interacting problems) versus fixing them sequentially (independent problems)

Interacting problems need shared context because a fix to one changes the other. Independent problems can be fixed sequentially with separate checks. For example, timezone parsing and date-boundary validation interact, while a documentation typo and an unrelated log label usually do not.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

## Applied skills

These are design applications. Pseudocode and schemas are illustrative unless separately dry-run; a saved design is not a completed implementation.

### 3.5-S1

**Blueprint focus:** Providing 2-3 concrete input/output examples to clarify transformation requirements when natural language descriptions produce inconsistent results

Provide two or three paired examples when prose produces inconsistent transformations. Include a normal case and boundary cases with expected types. Ask Claude to explain the rule inferred from them; correct that rule before generating another implementation.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-S2

**Blueprint focus:** Writing test suites covering expected behavior, edge cases, and performance requirements before implementation, then iterating by sharing test failures

Write behavior tests first and include meaningful edge and performance assertions. Share the actual failure output, relevant code and intended behavior on each iteration. Preserve passing cases so a new fix cannot quietly reverse an earlier requirement.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-S3

**Blueprint focus:** Using the interview pattern to surface design considerations (e.g., cache invalidation strategies, failure modes) before implementing solutions in unfamiliar domains

Use an interview before building in an unfamiliar area. Request the few decisions that materially affect correctness, answer them and record the selected contract. Stop the interview when the important uncertainties are resolved; endless questions do not improve a well-understood task.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-S4

**Blueprint focus:** Providing specific test cases with example input and expected output to fix edge case handling (e.g., null values in migration scripts)

For a migration that mishandles nulls, give a specific record and its expected transformed record. Add the case to the acceptance suite. Distinguish absent fields, explicit nulls and valid zero values rather than treating all falsy values as equivalent.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.5-S5

**Blueprint focus:** Addressing multiple interacting issues in a single detailed message when fixes interact, versus sequential iteration for independent issues

Bundle issues when they share a root cause or acceptance contract. Explain the interaction and provide all failing cases together. For independent issues, complete one fix and its checks before the next so failures stay attributable.

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

## Worked example

A fictional importer turns null quantities into zero, then calculates a misleading total. The author had asked only to “clean missing data.” The learner supplies three examples: null stays null, numeric zero stays zero and a numeric string becomes a number. Tests also require totals to become unknown when any contributing quantity is missing. Both defects are sent together because normalization controls total calculation. A credible alternative is a prose-only clarification; it is sufficient when the rule is already unambiguous, but here concrete examples expose the null-versus-zero distinction. The iteration costs a small test suite and clearer requirements. It prevents a superficially neat output from changing business meaning, and success means the original plus new boundary cases pass.

Original synthetic scenario; decision principles: [Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

## Production transfer

**Healthcare administration; enrichment beyond the blueprint examples.** A synthetic appointment importer must preserve missing contact preferences without treating them as consent. Examples distinguish absent, explicitly declined and accepted values. Tests first make those meanings observable; an interview resolves whether old records can be migrated automatically. Compare a precise prompt with a broader test-driven change: simple formatting may need only examples, while state migration needs regression checks. Recovery quarantines records with contradictory preferences. Extension: add a legacy value that is not in the new enum and explain why guessing a replacement is inappropriate.

In your own notes, save your decision, rejected alternative, evidence and recovery path. Re-run the decision with the changed constraint before calling the pattern transferable. This is a design exercise, not industry compliance advice.

## Traps and counterexamples

Do not create tests that merely reproduce the implementation. Do not erase failing tests to make an iteration pass. More examples help only when they represent meaningful variation, not five copies of the same easy case.

## Supplied acceptance and iteration fixture

All values are synthetic. Contract: valid YYYY-MM-DD dates remain unchanged; null and empty string become null; invalid dates return a validation error; numeric zero is **not** an absent date and must be rejected. Migration quantity rules are separate: null stays null and zero stays zero.

Illustrative broken logic:

```text
normalizeDate(x): if not x: return "1970-01-01"; else return x
migrateQuantity(x): return x or 0
```

Observed teaching-fixture outputs: normalizeDate(null) -> "1970-01-01"; normalizeDate("2026-02-30") -> "2026-02-30"; migrateQuantity(null) -> 0. These are supplied simulated outputs, not results from running a repository implementation.

### Write the acceptance suite before changing logic

| Test | Input | Expected result |
| --- | --- | --- |
| Normal date | "2026-10-02" | "2026-10-02" |
| Missing date | null | null |
| Empty date | "" | null |
| Invalid calendar day | "2026-02-30" | validation error |
| Wrong type | 0 | validation error |
| Explicit zero quantity | {quantity: 0} | {quantity: 0} |
| Missing quantity | {quantity: null} | {quantity: null} |
| Performance requirement | 10,000 fixed records | Proposed local benchmark: median of 5 runs < 500 ms on recorded runner; no semantic mismatch |

The performance bound is an invented acceptance requirement to practice measurement, not an Anthropic throughput claim. Record runner, warmup, sample and timing method; revise the target if the actual environment requires it.

### Failure-guided correction cycle

First correct the falsy-value conflation: handle null and empty string explicitly; preserve zero in the quantity path; reject nonstring date inputs. Rerun **all** tests in the written plan. Simulated next failure: invalid calendar dates still pass because the implementation only matches the string shape. Add calendar validity parsing, then rerun normal, missing, type and performance tests. Correcting the null case without the calendar check is incomplete.

**Explicit migration record:** input `{record_id: "M-7", quantity: null, price: 8}` must produce `{record_id: "M-7", quantity: null, price: 8, total: null}`. Input `{record_id: "M-8", quantity: 0, price: 8}` produces total 0. Share both failures together because normalization and total computation interact. An unrelated log spelling error can be handled later.

**Your deliverable:** save a test-spec table, pseudocode correction, one failure-feedback message quoting the exact mismatch, and three cache interview questions covering invalidation, stale reads and failed refresh. The written suite demonstrates design; only actual runner output establishes execution and performance acceptance.

[Guide section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1).

<a id="decision-variants"></a>
<a id="variant-fv-17"></a>
## Decision variant FV-17 — Change the hypothesis after repeated failure

This is original fictional practice, not an official exam question. All policies, amounts and records below are synthetic.

**Choose in the base case.** A date parser fails on one fixture. Supply actual input, expected result, failing assertion and relevant code; make a targeted change and re-run the fixture plus nearby cases.

**Change one constraint.** Feedback says only “make it better.” First obtain a reproducible criterion rather than guessing a redesign.

**What failed, and who recovers?** The same failure survives two identical retries. Investigate a new cause, such as locale interpretation or preprocessing, instead of repeating the same prompt.

**Inspect the artifact — illustrative contract, not a drop-in SDK implementation:**

```text
feedback={input:03/04,locale:en_GB,expected:2026-04-03,actual:2026-03-04,check:date_locale}
```

**Why not the nearest alternative?** More iterations do not imply learning. Narrow evidence and hypothesis changes matter more than request length.

**Memory cue with its condition:** Example, expectation, evidence; failed hypothesis must change.

**Proof before accepting success:** Produce a trace or artifact showing the decisive constraint, the selected mechanism, rejected alternative and observable result. Preserve unresolved status; a plausible explanation alone is not completion.

[Inspect D12 and its equivalent decision procedure](../decision-atlas.md#diagram-d12) · [See this decision at walkthrough step 6](../scenario-walkthroughs/WT-02-code-generation-claude-code.md#variant-fv-17) · [Return to the objective map](README.md).

**Blind transfer:** Before opening practice, explain which single change in the scene would reverse your choice and which would only require revalidation. Write the failure signal and the next safe action. The practice app provides separately authored base and later-retry items, with a free-response transfer rubric; assistance/exposure must remain visible in learning history.

**Current runtime reference:** [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) (reviewed 2026-10-14). The saved blueprint remains the exam coverage source; application policy in this packet is invented teaching context.


## Try it

Use the supplied fixture above for the required skill outputs first. The following design activity is an extension, not a substitute for those concrete checks.

Specify a date normalizer using three input/output examples, one invalid-input case and a performance requirement you can actually measure. Add two interacting defects and explain why they belong in one iteration. Write three interview questions for an unfamiliar cache.

Attempt your design before reading the self-check. Save the artifact and the decision rationale so an independent reviewer can inspect them.

### Expected output and self-check

Your examples distinguish valid, invalid and missing dates without guessing. Tests define expected behavior before implementation. Interacting timezone and boundary defects share one message; an unrelated typo can be separate. Cache questions address invalidation, stale-read tolerance and failures, with decisions recorded before build.

## Done when

- [ ] **3.5-S1:** Supply three date input/output pairs that distinguish valid, missing and invalid input; explain the inferred rule.
- [ ] **3.5-S2:** Write behavior, edge and measurable performance tests from the supplied fixture before proposing code; label execution and timing as pending until actually run.
- [ ] **3.5-S3:** Ask and answer cache interview questions for invalidation, stale reads and failed refresh; preserve the chosen contract.
- [ ] **3.5-S4:** Produce null-quantity and zero-quantity transformed records plus the exact failure-feedback message and correction cycle.
- [ ] **3.5-S5:** Group normalization/total defects into one iteration with all failing examples; identify an independent issue suitable for sequential work.

In your own notes, save each stated artifact and check against the supplied expected outputs. Written design evidence and actual implementation evidence remain separate; learner mastery is not inferred from reading.

## Coverage checklist

| Official bullet, in guide order | Exact teaching section |
| --- | --- |
| 3.5-K1: Concrete input/output examples as the most effective way to communicate expected transformations when prose descriptions are interpreted inconsistently | [3.5-K1](#35-k1) |
| 3.5-K2: Test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement | [3.5-K2](#35-k2) |
| 3.5-K3: The interview pattern: having Claude ask questions to surface considerations the developer may not have anticipated before implementing | [3.5-K3](#35-k3) |
| 3.5-K4: When to provide all issues in a single message (interacting problems) versus fixing them sequentially (independent problems) | [3.5-K4](#35-k4) |
| 3.5-S1: Providing 2-3 concrete input/output examples to clarify transformation requirements when natural language descriptions produce inconsistent results | [3.5-S1](#35-s1) |
| 3.5-S2: Writing test suites covering expected behavior, edge cases, and performance requirements before implementation, then iterating by sharing test failures | [3.5-S2](#35-s2) |
| 3.5-S3: Using the interview pattern to surface design considerations (e.g., cache invalidation strategies, failure modes) before implementing solutions in unfamiliar domains | [3.5-S3](#35-s3) |
| 3.5-S4: Providing specific test cases with example input and expected output to fix edge case handling (e.g., null values in migration scripts) | [3.5-S4](#35-s4) |
| 3.5-S5: Addressing multiple interacting issues in a single detailed message when fixes interact, versus sequential iteration for independent issues | [3.5-S5](#35-s5) |

## Sources and freshness

[Exam guide v1.0, section 6 task 3.5](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

The official objective wording is reproduced for traceability; explanations and all scenarios are project-authored. Existing L03–L05 provide domain synthesis; this module expands each bullet into a teachable decision. The saved July guide is the blueprint baseline, not a claim that no newer guide exists.

**Go deeper:** [Deep practice 3, section 3.5](../deep-practice/03-claude-code-configuration-and-workflows.md#35-iterative-refinement)



<a id="benchmark-exercise-3-5"></a>
## Worked evidence task — 3.5: test the boundary

**Original technical decision.** Examples define numeric zero and an empty string, but the unseen input is string zero. Which acceptance policy avoids guessing an unspecified transformation?

**In everyday terms:** Two examples do not answer every edge case.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "examples": [
    {
      "input": 0,
      "output": 0
    },
    {
      "input": "",
      "output": null
    }
  ],
  "unseen_input": "0",
  "unresolved": "string zero policy requires clarification"
}
```

### Break, choose, repair, prove

1. **Break:** Repeat a failing transformation with prose, then concrete examples and failing tests. Name the exact failed assumption before proposing another component.
2. **Choose:** Preserve observed example behavior and request the missing string-zero policy before asserting correctness. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** State which hypothesis changed and demonstrate acceptance on an unseen boundary case. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Open this actual task in the existing LAB](../../../06-Labs/08-CCAR-F-architecture-decisions/README.md#benchmark-exercise-3-5) · [Return to the teaching subsection](#supplied-acceptance-and-iteration-fixture)

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "known_numeric_zero": 0,
  "known_empty_string": null,
  "string_zero_result": null,
  "requires_clarification": true
}
```

**Why this matters:** Two examples do not answer every edge case. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Code Iterative Development Documentation](https://code.claude.com/docs/en/best-practices). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>