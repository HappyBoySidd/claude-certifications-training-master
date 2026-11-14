# CCDV-F Lesson 0 — Orientation: how the Developer exam thinks

**Time:** 45 min · **Do first:** the baseline mock (step 3)

## What you're preparing for

- **53 items in 120 minutes.** That's a little over 2 minutes per item.
- Two item types: **multiple-choice** (pick one) and **multiple-response** (pick several).
  **Each item tells you how many to pick.** Count your ticks before moving on.
- **Pass mark: a scaled 720** on a 100–1,000 scale. It's a fixed standard, not a curve: you're
  measured against the bar, not against other people.
- Your score report shows pass/fail, the scaled score, and **percent correct per domain**. The
  domain numbers don't decide the result, but they tell you what to fix if you retake.
- **Fee $125 USD** (your partner tier may lower it at checkout).
- **Valid 12 months.** Renewing on time is a **free, unproctored assessment** on the Anthropic
  Partner Academy. Let it lapse and you pay for the full exam again.
- Retakes wait 14, then 30, then 90 days; at most 4 attempts in a rolling 12 months.

## The eight domains, and where they're taught

| # | Domain | Weight | ≈ Items | Lesson |
| --- | --- | --- | --- | --- |
| 2 | Applications and Integration | **33.1%** | 18 | [L01](L01-applications-and-integration.md) |
| 5 | Model Selection and Optimization | **16.8%** | 9 | [L02](L02-model-selection-and-optimization.md) |
| 1 | Agents and Workflows | **14.7%** | 8 | [L03](L03-agents-and-workflows.md) |
| 6 | Prompt and Context Engineering | 11.0% | 6 | [L04](L04-prompt-and-context-engineering.md) |
| 8 | Tools and MCPs | 10.6% | 6 | [L05](L05-tools-and-mcps.md) |
| 7 | Security and Safety | 8.1% | 4 | [L06](L06-security-and-safety.md) |
| 3 | Claude Code | 3.1% | 2 | [L07](L07-claude-code-eval-and-debugging.md) |
| 4 | Eval, Testing, and Debugging | 2.6% | 1 | [L07](L07-claude-code-eval-and-debugging.md) |

The top three domains are **almost two-thirds of the exam**. Study in that order.
Every lesson numbers its sections by exam domain: section 2.3 is Domain 2, skill 3, whichever
lesson it's in, and each lesson opens with a short *big idea* (section D.0). Item counts
are 53 × weight, rounded; the guide gives only percentages.

## The six rules that decide most questions

1. **Change the structure, not a knob.** Wrong answers usually tweak a parameter: raise
   `max_tokens`, change temperature, "use a bigger model". Right answers change the design: a
   different API mode, a schema, a hook, a subagent.
2. **Ask "who is waiting?" before "what's cheapest?"** A person waiting means the real-time
   Messages API (stream it). Nobody waiting and lots of volume means the Message Batches API.
   Same long prefix every call means prompt caching.
3. **Enforce in code what must always hold.** A prompt line is a request; a hook, a schema or a
   missing tool is a guarantee. Untrusted content never gets to trigger sensitive actions.
4. **Pick the right home for a capability.** One app: a custom tool. Many apps, maintained
   separately: an MCP server. A reusable procedure or convention: a Skill. File, shell and search
   basics: built-in tools.
5. **The cheapest structure that works wins.** Known steps: a workflow, not an agent. Smallest
   model that passes your evals, not the biggest one. Tune effort before switching models.
6. **Pin it, version it, test the change.** Pin model versions, version prompts and config, and
   treat a model upgrade as a change that needs an eval run, not a drop-in.

Rules 2–4 come straight from the rationales of the guide's three sample items (batch vs real
time, prompt injection, MCP for reuse). Rules 1, 5 and 6 are our synthesis of the blueprint
objectives.

## What people who passed say

- **More Claude Code than the 3.1% weight suggests.** CLI, CLAUDE.md, Skills, settings.json and
  subagents all came up. *Confirmed:* two colleagues who passed (INSIGHTS, 2026-09-26).
  Don't skip L07; Claude Code also shows up inside Domain 2 (Configuration Management, Claude
  Application Design).
- About **two-thirds overlap with CCAR-F**, so take it soon after. *Single report:* one
  colleague who passed.
- **Agent SDK, streaming and protocols**, all inside scenario questions. *Single report:* one
  colleague who passed.
- **Harder than CCAR-P**, with many development-specific questions. *Single report:* one
  colleague who passed.
- One colleague reported 135 minutes and a 772 pass mark. **The official guide says 120 minutes and
  a scaled 720; the guide wins.** (The community cheat sheet also mentions "135 minutes of seat
  time", which probably includes the agreement and tutorial screens. Unconfirmed.)
- Across all exams: **full, timed mocks matter more than reading** (*Confirmed*, four people),
  and some items ask for 2 or more answers (*Confirmed*, and in the guide).

## Steps

1. [ ] Skim the [official exam guide v1.0](https://anthropic-partners.skilljar.com/page/partner-certifications)
       ([text](https://anthropic-partners.skilljar.com/page/partner-certifications)):
       section 5 (format) and section 6 (every objective).
2. [ ] Do the **3 official sample items** in section 8. Answer first, then read the rationales.
       Notice how each wrong option adjusts a knob while the right one changes the structure.
3. [ ] **Baseline:** a CCDV-F mock in the [practice tool](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html),
       timed. Log it in your own notes.
4. [ ] Start [lab 04](../../06-Labs/04-CCDV-F-api-modes/README.md) (API modes) now. It feeds
       L01 and L02, and the exam assumes you've actually called the API.

## Self-check

- How many items, how long, what pass mark? *(53, 120 minutes, scaled 720)*
- How do you know how many options to pick? *(The item says so)*
- Which three domains make up about two-thirds? *(Applications and Integration, Model
  Selection, Agents and Workflows)*
- Nobody is waiting and there are 20,000 requests. Which API? *(Message Batches API)*
- Why does "add a line to the system prompt" lose to "add a hook"? *(A prompt can be ignored; a
  hook runs every time)*

**Next:** [L01 Applications and Integration](L01-applications-and-integration.md)

Source: official CCDV-F exam guide v1.0 (July 2026), sections 5, 6, 8, 9, 11 and 14;
`11-Lessons-Learned/INSIGHTS.md` (CCDV-F and Across all exams, updated 2026-09-26).