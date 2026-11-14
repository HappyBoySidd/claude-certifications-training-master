# CCAR-P SIM-05 — Rollout and Stakeholder Lifecycle

**Primary domains:** 6 Stakeholder Communication & Lifecycle Management, 7 Developer Productivity &
Operational Enablement, 4 Evaluation, Testing & Optimization · **Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

You're the lead architect for a contract-review assistant at a manufacturing company. It flags
risky clauses in supplier contracts for the procurement team. Before discovery even started, the
procurement VP told the executive board it would be "95% accurate". Legal, IT security and finance
all have a stake, and an internal engineering team will **own and run the system after you hand it
over**.


---

## The decisions (answer these before you open the key)

1. How to start
2. Legal wants the most capable model with extended thinking on every clause; finance wants low cost and speed
3. The eval shows 88% on clause flagging against the promised 95%
4. Most errors are in indemnity clauses
5. What to hand the engineering team
6. Setting up Claude Code for that team
7. The team loses days chasing prompt regressions
8. What to monitor after launch
9. After a model version change, output format shifts and a downstream report breaks
10. Procurement users keep flagging false positives

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | How to start | **Structured discovery**: stakeholders, the current process, volumes, constraints (data, security, compliance), baselines, and an agreed definition of "accurate" | Build a demo first; adopt the VP's 95% as the spec; copy requirements from another project | D6 Structured discovery and requirement gathering | [Lesson 5, section 6.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |
| 2 | Legal wants the most capable model with extended thinking on every clause; finance wants low cost and speed | **Write an ADR**: context, options, decision and consequences, backed by eval data, and share it with both | Decide quietly; let each team pick its own model; settle it in a chat thread | D6 Communicate architectural decisions and trade-offs | [Lesson 5, section 6.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |
| 3 | The eval shows 88% on clause flagging against the promised 95% | **Reset expectations early, with data and options**: where errors fall, human review for high-risk clauses, narrower scope, a revised SLA agreed with the sponsor | Wait until launch; trim hard cases from the eval set; promise it will improve | D6 Expectation alignment (including SLAs) | [Lesson 5, section 6.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |
| 4 | Most errors are in indemnity clauses | **Target the failure class**: send those clauses to human review now, and iterate prompts and examples on that class against the eval | Rewrite the whole prompt; switch models blindly; add more generic instructions | D4 Diagnose system issues; D4 Iterative improvements | [Lesson 3, section 4.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md), [Lesson 3, section 4.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 5 | What to hand the engineering team | **Handoff pack**: architecture doc, ADRs, runbook (failure modes, alerts, rollback), pinned model and prompt versions, the eval suite and how to run it, named owners | A slide deck; "the code is the documentation"; a one-hour walkthrough | D6 Document architectures and implementation guidance | [Lesson 5, section 6.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |
| 6 | Setting up Claude Code for that team | **Shared, checked-in setup**: project CLAUDE.md, settings.json permissions, team slash commands or Skills (e.g., "run evals"), and hooks for guardrails | Each developer configures it alone; one training session and done; personal files shared by email | D7 Configure Claude tools and environments for teams | [Lesson 7, section 7.1](../../02-Lessons/04-CCAR-P-Architect-Professional/L07-developer-productivity-and-enablement.md) |
| 7 | The team loses days chasing prompt regressions | **Run the eval suite in CI** on every prompt or model change; Claude Code's headless mode (`claude -p`) can add automated PR review alongside it | Manual spot checks; a regressions wiki page; freeze all prompt changes | D7 Improve developer workflows with AI-assisted tooling | [Lesson 7, section 7.2](../../02-Lessons/04-CCAR-P-Architect-Professional/L07-developer-productivity-and-enablement.md) |
| 8 | What to monitor after launch | **Quality and operations together**: sampled human-graded accuracy, escalation rate, latency, cost and drift, with alerts | Uptime only; wait for user complaints; token spend only | D4 Monitor performance; D6 Lifecycle (monitoring) | [Lesson 3, section 4.6](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md); [Lesson 5, section 6.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |
| 9 | After a model version change, output format shifts and a downstream report breaks | **Pin versions, roll back, then test the new version against the eval** before switching again | Patch the report parser and move on; always track the newest alias; blame the users | D7 Support operational issue resolution; D4 Diagnose model mismatch | [Lesson 7, section 7.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L07-developer-productivity-and-enablement.md); [Lesson 3, section 4.4](../../02-Lessons/04-CCAR-P-Architect-Professional/L03-evaluation-testing-and-optimization.md) |
| 10 | Procurement users keep flagging false positives | **A regular feedback loop**: add flagged cases to the eval set, prioritize fixes, and report changes back to stakeholders | Ignore them unless volume spikes; tell users to adjust; fix one-offs without tracking | D6 Stakeholder feedback loops; D6 Lifecycle (iteration) | [Lesson 5, section 6.3](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md), [Lesson 5, section 6.5](../../02-Lessons/04-CCAR-P-Architect-Professional/L05-stakeholder-communication-and-lifecycle.md) |

**Scoring:** 8 or more is a pass. The two principles: *bring bad news early, with data and options*,
and *leave the team able to run it: documented decisions, runbooks, shared config and evals in CI*.

Sources: [CCAR-P exam guide, Section 6 (community mirror of the official guide)](https://anthropic-partners.skilljar.com/page/partner-certifications),
[CCAR-F exam guide, Task Statements 3.1, 3.2 and 3.6](https://anthropic-partners.skilljar.com/page/partner-certifications).

</details>