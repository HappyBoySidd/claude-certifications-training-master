# Objective 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

[Test this decision with a supplied example](#benchmark-exercise-3-1) — predict first, then compare the fixed-fixture evidence.

**Picture the application:** An analytics repository contains interface code and storage code, and a new colleague misses a testing convention known to its original author. The expected result is consistent generated work using the appropriate team and package guidance. The technical topic is instruction hierarchy: which guidance belongs in personal, shared or local project context.



**Exam:** CCAR-F · **Domain 3:** 20% of exam; no separate objective weight is published here.  
**Time:** 30–40 minutes foundation/applied; 15–25 additional minutes production extension.  
**Prerequisites:** L00 orientation and repository paths. New to the Claude API? Start with the [five-minute primer in Lesson 0](../L00-orientation.md#five-minute-primer-how-a-claude-app-works).  
**Continue from:** [Domain lesson](../L03-claude-code-configuration-and-workflows.md) · [Objective map](../../../01-Curriculum/02-Architect-Track/CCAR-F-objectives.md).

**Official task statement:** Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization


<!-- layered-episode:FV-13:start -->
<a id="learn-fv-13"></a>
### Learn the decision in context — FV-13

**Picture the job.** The whole team shares one convention, but a package has a special rule and one developer has a personal preference. This is an original fictional teaching scene, not a recalled live exam question. Read and trace it; no account, installation or API call is required.

**Start small.** Follow the ordinary route: a person supplies a request or record, software passes the needed evidence to the assistant, and a receiving service or person checks the result. The first demonstration assumes the input, access and evidence are suitable. Now remove that assumption in the situation above. Predict what the receiver would see before choosing a repair.

**Original exam-style practice — choose ONE.** How should repository, package and personal guidance be organized to avoid instruction drift?

A. Place conventions at their actual supported scope and resolve applicable conflicts using documented loading rules.

B. Copy every instruction into every folder to guarantee consistency.

C. Use personal preferences as the team’s enforced authorization policy.

<details>
<summary>What is this asking? Plain-language help, without the answer</summary>

Identify what the application needs to trust, what has actually been observed, and what remains unknown. Compare the choices against this situation, rather than choosing the most complicated design. A proposal is an intended action; evidence is what you can point to; a contract says what the receiving part expects. Decide which option fixes the stated failure without pretending another requirement has also been solved.

</details>

**Choose before opening the walkthrough.** Say your answer and the closest alternative aloud, or record them in your own notes.

<details>
<summary>Reveal the repair, evidence and changed condition</summary>

**Answer: A.** Place conventions at their actual supported scope and resolve applicable conflicts using documented loading rules.

**Walk it through.** For services/api.py, the learner identifies the applicable shared and package guidance, flags a conflicting test instruction and resolves it explicitly.

**Why the alternatives fail here.** Copy every instruction into every folder to guarantee consistency. This leaves the stated boundary or evidence requirement unsatisfied. Use personal preferences as the team’s enforced authorization policy. This also fails to establish the required result. The closest competing mechanism fails for this specific reason: More copies increase drift. Instruction files guide model behavior; they do not replace enforced permission checks.

**Inspect the small artifact.** This is an illustrative application-state note for reading, not an SDK signature or executable configuration. The application or workflow owner creates it; the receiver uses it to distinguish what is known from what still needs checking. Its labels describe this scene; do not paste it into Claude settings.

```text
instructions={shared:CLAUDE.md,package:services/CLAUDE.md,personal:user}; target=services/api.py
```

**Layer added.** AI reasoning proposes, selects or summarizes where the job needs judgment. Ordinary software checks identifiers, permissions, required fields, recorded outcomes and stop conditions where applicable. A human resolves a policy or evidence gap when the story requires it. Inspect which owner actually supplies the evidence in this scene.

```mermaid
flowchart LR
 N0["Current target file path"] --> N1
 N1["Find applicable shared and package guidance"] --> N2
 N2["Resolve scope and instruction conflict"] --> N3
 N3["Apply documented current convention"] --> N4
 N4["Enforce permissions outside prose"]
```

**Change one condition.** Keep the application in mind and consider the new situation below. Choose before opening its explanation.

**Technical transfer question — choose ONE.** A convention applies only to one package. Where should it be maintained?

A. The supported package-level scope, with conflicts resolved explicitly.

B. Every instruction file, including unrelated packages.

<details>
<summary>Transfer check</summary>

**A.** A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file. Name the changed fact before naming a tool. Preserve unrelated access, source-validation and result checks.

</details>

**Recall in ordinary language.** What broke? Who can fix it? What observable result proves the repair? If you cannot answer all three, replay the concrete scene rather than memorize the option letter.

</details>

**Continue from this decision:** [objective 3.1](objective-3.1.md) · [inspect its decision map](../decision-atlas.md#diagram-d11) · [targeted practice](../../../practice/index.html?exam=CCAR-F&objective=3.1). Existing mapped question IDs: `cct-fv-13-base-v1`, `cct-fv-13-retry-v1`. The new guided question above is separate from those stored items and does not change their answers or progress.
<!-- layered-episode:FV-13:end -->

## Read this objective in both vocabularies

For reading and paper reasoning, no installation or credentials are needed. Keep this page's stated concept prerequisites; any runnable challenge still needs its own setup. If an implementation example feels abrupt, first read [how to interpret its artifact type](../architecture-studio/00-foundations.md#how-to-read-technical-examples-in-this-course), then use the relevant application bridge: [AS-05 decision bridge](../architecture-studio/AS-05-code-change.md#connect-the-simple-explanation-to-technical-design-choices).

Explain the business purpose first, name the precise mechanism second, and distinguish it from the nearest plausible alternative using the stated constraint. Return here for the objective-specific protocol, options and practice. The bridges are teaching aids, not additional official objectives.


## Big idea

Configuration works only when its scope matches who needs the instruction. Separate personal preferences, team standards and package conventions before improving the wording.

## Foundation

### 3.1-K1

**Blueprint focus:** The CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md or root CLAUDE.md), and directory-level (subdirectory CLAUDE.md files)

Hierarchy is about scope, not file size. Personal instructions belong under the home directory; repository instructions belong at its root or in its .claude folder; a package can carry more specific conventions. A package instruction should explain its local exception rather than contradicting a universal safety rule.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-K2

**Blueprint focus:** That user-level settings apply only to that user—instructions in ~/.claude/CLAUDE.md are not shared with teammates via version control

A teammate cannot inherit files stored in your home directory through a repository clone. If only one developer gets the desired behavior, inspect file placement before concluding that Claude ignored the prompt. Team rules need a committed project location.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-K3

**Blueprint focus:** The @import syntax for referencing external files to keep CLAUDE.md modular (e.g., importing specific standards files relevant to each package)

Imports keep ownership visible. A package maintainer can reference the standards that apply to that package with @path syntax, rather than copying every standard into one giant file. Review imported material for relevance: modular organization does not automatically make context smaller.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-K4

**Blueprint focus:** .claude/rules/ directory for organizing topic-specific rule files as an alternative to a monolithic CLAUDE.md

Topic files make a large instruction set easier to maintain. Testing, API contracts and deployment can have distinct owners and review cycles in .claude/rules/. A topic split organizes content; conditional path scoping, covered in 3.3, controls when file-specific rules apply.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

## Applied skills

These are design applications. Pseudocode and schemas are illustrative unless separately dry-run; a saved design is not a completed implementation.

### 3.1-S1

**Blueprint focus:** Diagnosing configuration hierarchy issues (e.g., a new team member not receiving instructions because they're in user-level rather than project-level configuration)

Reproduce the discrepancy with a clean teammate checkout. Record the working directory and loaded memory files, locate the missing instruction, and move shared conventions into project scope. Verify the teammate sees the same instruction before changing its wording.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-S2

**Blueprint focus:** Using @import to selectively include relevant standards files in each package's CLAUDE.md based on maintainer domain knowledge

For each package, list its relevant standards and add only those imports to its CLAUDE.md. Check relative paths from the importing file. Explain why a frontend package does not need database migration conventions merely because both live in one repository.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-S3

**Blueprint focus:** Splitting large CLAUDE.md files into focused topic-specific files in .claude/rules/ (e.g., testing.md, api-conventions.md, deployment.md)

Split an oversized file by subject, retaining a short root orientation and stable links. Remove duplicate wording rather than letting contradictory copies drift. Compare the resulting rule set with the original requirements so organization does not silently lose an obligation.

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### 3.1-S4

**Blueprint focus:** Using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions

The July blueprint names /memory for configuration diagnosis. Current /memory lists memory locations, including entries that may not exist; /context lists, under Memory files, the CLAUDE.md files loaded at launch. A path-scoped rule or a subfolder CLAUDE.md loads later, and the terminal shows a "Loaded …" line when it does. Compare working directories and investigate absent files. [Current memory documentation](https://code.claude.com/docs/en/memory) (Tier 1, checked 2026-10-07).

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

## Worked example

A fictional analytics repository has a UI package and a storage package. Mina's personal CLAUDE.md says “use existing test fixtures”; a new colleague generates redundant fixtures. The decision is to place that universal testing convention in repository instructions, import UI accessibility standards in the UI package, and import migration standards in storage. The team checks /memory locations and /context loaded files from both packages. A credible alternative is one root file containing everything: it is easier to discover initially, but every package receives irrelevant material and future edits become harder to own. Package-only files are also reasonable for genuinely local rules. Neither alternative fixes a team rule left in Mina's home directory. The acceptance evidence is the loaded-file list and a sample generation that reuses an existing fixture, not just the creation of three Markdown files.

Original synthetic scenario; decision principles: [Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

### Example configuration tree

```text
CLAUDE.md                 # committed shared testing standards
ui/CLAUDE.md              # imports @../standards/accessibility.md
storage/CLAUDE.md         # imports storage-owned migration standards
~/.claude/CLAUDE.md       # personal tone preferences; not distributed by git
```

The paths are illustrative: compute each import from the actual importing file. Here ui/ is directly below the root, so a repository-root standards folder uses `@../standards/accessibility.md`. Check that the real file exists and that an import does not escape the intended scope.

## Production transfer

**Healthcare administration; enrichment beyond the blueprint examples.** A synthetic clinic scheduling repository separates appointment UI and billing exports. The shared instruction forbids patient identifiers in debug examples; billing-specific rounding rules load in its package. Privacy changes the stakes: review the actual loaded guidance and sample output, while access controls remain outside instruction files. A root-only policy is easier to discover, but package imports reduce irrelevant billing detail. Recovery from a missing import means stopping the affected generation and correcting its context. Extension: add a third package and show which existing rules it should receive.

In your own notes, save your decision, rejected alternative, evidence and recovery path. Re-run the decision with the changed constraint before calling the pattern transferable. This is a design exercise, not industry compliance advice.

## Traps and counterexamples

Do not confuse a personal file with a team artifact. Do not copy the same rule into four files as a substitute for ownership. Instructions guide behavior; deterministic safety controls still require enforcement.

## Supplied refactoring fixture

This synthetic root CLAUDE.md mixes universal standards, local instructions and duplicates:

```text
1. Reuse existing fixtures before adding new ones.
2. Every API error must include a stable error code.
3. Run the smallest relevant test suite after code changes.
4. All packages use npm test.
5. storage/ migrations use pytest tests/migrations.
6. Reuse existing fixtures before adding new ones.
7. UI changes must preserve keyboard navigation.
8. Do not include personal identifiers in debug examples.
```

Refactor it into focused files without losing obligations. Resolve line 4 versus line 5 using the supplied maintainer fact: **storage is Python; other packages use npm test**. Do not silently delete either test requirement. Save a retained-obligations table and a verification record.

### Worked refactoring output

| Destination | Retained obligation |
| --- | --- |
| root CLAUDE.md | Project orientation, package ownership and applicable test command rule |
| .claude/rules/testing.md | Reuse fixtures once; run the smallest relevant suite; npm test outside storage |
| .claude/rules/api.md | Stable API error codes |
| .claude/rules/privacy.md | No personal identifiers in debug examples |
| ui/CLAUDE.md | Keyboard navigation; import UI-owned accessibility standard |
| storage/CLAUDE.md | pytest tests/migrations for migrations; explicit exception to generic npm command |

The invariant checklist retains fixture reuse, error codes, relevant tests, correct package test command, keyboard navigation and privacy. Duplicate line 6 has one authoritative replacement. The testing topic remains generally loaded; UI keyboard and storage command guidance are package-specific. A blanket removal of testing line 4 would lose a real obligation for other packages.

**Illustrative verification record, not an observed run:** from ui/, `/memory` lists project and personal locations; `/context` should show project topics plus UI memory, and the sample task should preserve keyboard behavior. From storage/, loaded package context should specify pytest for migration tests. A clean teammate checkout should see the committed topics and package files, but not the author's private tone preference. Record actual paths, the context output and same-task behavior when you execute this check. A list entry in `/memory` alone does not prove loading.

**Exercise extension:** add a docs/ package that uses no tests for prose changes. Specify which universal obligations remain and how you avoid applying a code-only test rule unnecessarily. The goal is scoped preservation, not copying everything everywhere.

[Guide section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) and [current memory inspection](https://code.claude.com/docs/en/memory) (Tier 1; current behavior checked 2026-10-02).

<a id="decision-variants"></a>
<a id="variant-fv-13"></a>
## Decision variant FV-13 — Put instructions at their real scope

This is original fictional practice, not an official exam question. All policies, amounts and records below are synthetic.

**Choose in the base case.** A shared repository convention belongs in project instructions; personal preferences stay in personal configuration. Trace which nested instructions apply to the current path.

**Change one constraint.** A package-specific convention is added. Put it at the package scope rather than copying it into every project instruction file.

**What failed, and who recovers?** Two applicable files disagree on test behavior. Surface and resolve the conflict using the runtime’s documented loading/scope rules.

**Inspect the artifact — illustrative contract, not a drop-in SDK implementation:**

```text
instructions={shared:CLAUDE.md,package:services/CLAUDE.md,personal:user}; target=services/api.py
```

**Why not the nearest alternative?** More copies increase drift. Instruction files guide model behavior; they do not replace enforced permission checks.

**Memory cue with its condition:** Shared at project; specific at path; resolve conflicts.

**Proof before accepting success:** Produce a trace or artifact showing the decisive constraint, the selected mechanism, rejected alternative and observable result. Preserve unresolved status; a plausible explanation alone is not completion.

[Inspect D11 and its equivalent decision procedure](../decision-atlas.md#diagram-d11) · [See this decision at walkthrough step 1](../scenario-walkthroughs/WT-04-developer-productivity.md#variant-fv-13) · [Return to the objective map](README.md).

**Blind transfer:** Before opening practice, explain which single change in the scene would reverse your choice and which would only require revalidation. Write the failure signal and the next safe action. The practice app provides separately authored base and later-retry items, with a free-response transfer rubric; assistance/exposure must remain visible in learning history.

**Current runtime reference:** [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) (reviewed 2026-10-14). The saved blueprint remains the exam coverage source; application policy in this packet is invented teaching context.


## Try it

Use the supplied fixture above for the required skill outputs first. The following design activity is an extension, not a substitute for those concrete checks.

Sketch a root, ui/ and storage/ instruction tree. Include a personal tone preference, a shared testing rule and one package rule each. Write one @import and explain which two sessions you would compare with /memory and /context.

Attempt your design before reading the self-check. Save the artifact and the decision rationale so an independent reviewer can inspect them.

### Expected output and self-check

The tone preference stays personal. The shared test rule is committed at project scope. Each package imports only its relevant standards. Your verification compares loaded files and one same-task result in a clean teammate checkout. If the shared rule remains under ~/.claude, your design fails even if it works on your machine.

## Done when

- [ ] **3.1-S1:** Save a personal/project/package placement table; a clean teammate checkout receives every shared rule and no private preference.
- [ ] **3.1-S2:** Write one valid package import and verify its target exists; explain why the package receives that standard.
- [ ] **3.1-S3:** Refactor the supplied monolith into focused files; retained-obligations table covers all six unique obligations and resolves npm versus pytest without losing either package requirement.
- [ ] **3.1-S4:** Record /memory location inspection plus /context loaded-file verification from UI and storage; distinguish the illustrative record from observed execution.

In your own notes, save each stated artifact and check against the supplied expected outputs. Written design evidence and actual implementation evidence remain separate; learner mastery is not inferred from reading.

## Coverage checklist

| Official bullet, in guide order | Exact teaching section |
| --- | --- |
| 3.1-K1: The CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md or root CLAUDE.md), and directory-level (subdirectory CLAUDE.md files) | [3.1-K1](#31-k1) |
| 3.1-K2: That user-level settings apply only to that user—instructions in ~/.claude/CLAUDE.md are not shared with teammates via version control | [3.1-K2](#31-k2) |
| 3.1-K3: The @import syntax for referencing external files to keep CLAUDE.md modular (e.g., importing specific standards files relevant to each package) | [3.1-K3](#31-k3) |
| 3.1-K4: .claude/rules/ directory for organizing topic-specific rule files as an alternative to a monolithic CLAUDE.md | [3.1-K4](#31-k4) |
| 3.1-S1: Diagnosing configuration hierarchy issues (e.g., a new team member not receiving instructions because they're in user-level rather than project-level configuration) | [3.1-S1](#31-s1) |
| 3.1-S2: Using @import to selectively include relevant standards files in each package's CLAUDE.md based on maintainer domain knowledge | [3.1-S2](#31-s2) |
| 3.1-S3: Splitting large CLAUDE.md files into focused topic-specific files in .claude/rules/ (e.g., testing.md, api-conventions.md, deployment.md) | [3.1-S3](#31-s3) |
| 3.1-S4: Using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions | [3.1-S4](#31-s4) |

## Sources and freshness

[Exam guide v1.0, section 6 task 3.1](https://anthropic-partners.skilljar.com/page/partner-certifications) (Tier 1, July 2026 blueprint).

The official objective wording is reproduced for traceability; explanations and all scenarios are project-authored. Existing L03–L05 provide domain synthesis; this module expands each bullet into a teachable decision. The saved July guide is the blueprint baseline, not a claim that no newer guide exists.

**Version distinction:** study the July /memory terminology, but in current Claude Code use /context to check the CLAUDE.md files loaded at launch, and watch for the terminal's "Loaded …" line when a path-scoped rule or subfolder CLAUDE.md loads later. [Memory documentation](https://code.claude.com/docs/en/memory) (Tier 1, checked 2026-10-07).

**Go deeper:** [Deep practice 3, section 3.1](../deep-practice/03-claude-code-configuration-and-workflows.md#31-claudemd-hierarchy-scope-and-modules)



<a id="benchmark-exercise-3-1"></a>
## Worked evidence task — 3.1: test the boundary

**Original technical decision.** A teammate lacks one developer’s home instructions and project guidance contains opposing naming rules. Which repair addresses distribution without assuming settings override behavior?

**In everyday terms:** Your home file does not travel with the repository to another person.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "home_rules": [
    "team style"
  ],
  "repo_rules": [
    "use snake_case",
    "use camelCase"
  ],
  "new_teammate_has_home_rules": false
}
```

### Break, choose, repair, prove

1. **Break:** Place team rules only in one developer home directory and add contradictory project text. Name the exact failed assumption before proposing another component.
2. **Choose:** Put shared guidance in the repository and reconcile conflicting instructions explicitly; inspect settings precedence separately. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Explain missing team distribution and distinguish instruction loading from settings precedence. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Open this actual task in the existing LAB](../../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md#benchmark-exercise-3-1) · [Return to the teaching subsection](#foundation)

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "home_rule_distributed": false,
  "project_conflict": true,
  "repair": "repository-shared reconciled guidance",
  "settings_precedence_tested": false
}
```

**Why this matters:** Your home file does not travel with the repository to another person. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Code memory docs](https://code.claude.com/docs/en/memory) · [How Claude remembers your project (CLAUDE.md and auto memory)](https://code.claude.com/docs/en/memory). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>