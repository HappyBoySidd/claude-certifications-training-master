# CCAR-P Lesson 5 — Stakeholder Communication and Lifecycle (14%, about 9 questions)

**Time:** 90 min plus the paper exercise · **Practice:** [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Colleague note:** a colleague who passed (944) said about half the exam is standard system
design with Claude wording. So real engagement experience (discovery, RACI, rollout, change
management) transfers directly. This lesson adds the Claude-specific twists.

## 6.0 The big idea

Most of this domain is ordinary good consulting with a Claude twist. Find out what people really need, write down why you chose what you chose, bring bad news early with numbers and options, and hand over something the next team can run.

## 6.1 Structured discovery and requirements

Discovery comes **before** architecture. Work through it in this order:

| Step | Ask | Claude-specific twist |
| --- | --- | --- |
| **Problem** | What decision or task is slow, costly or error-prone today? | Is an LLM even the right tool, or would a rule or a search box do? |
| **Users and stakeholders** | Who uses it, who owns it, who signs off, who can say no (security, legal, compliance)? | Who reviews AI output, and who is accountable for it? |
| **Success measures** | What number must move, and from what baseline? | Set eval metrics now: accuracy, latency, cost, safety |
| **Constraints** | Budget, latency, data sensitivity, regulation, existing systems | Data residency, retention, which data may reach the model |
| **Data** | What data exists, where, how clean, who owns it? | Is there a labeled set to evaluate against? If not, build one |
| **Risk tolerance** | What's the cost of a wrong answer? | Drives human-in-the-loop design ([L04](L04-governance-safety-and-risk-management.md)) |

- A **RACI** (responsible, accountable, consulted, informed) for each decision stops "who approves the
  prompt change?" from becoming an incident.
- Capture **non-goals**. What the system won't do is as important as what it will.

## 6.2 Communicating decisions and trade-offs: the ADR

An **architecture decision record (ADR)** is a short document per significant decision:

| Section | Contents |
| --- | --- |
| **Title and status** | "ADR-004: Use retrieval, not fine-tuning, for policy answers" · Proposed / Accepted / Superseded |
| **Context** | The problem and the constraints that force a choice |
| **Options considered** | At least two real alternatives, each with pros and cons |
| **Decision** | What you chose |
| **Consequences** | What gets better, what gets worse, what you'll monitor, when you'll revisit |

- **A decision record without alternatives is a press release.** The trade-offs are the point.
- **Tailor the message, not the facts.** Executives get outcome, cost and risk; engineers get the
  design; compliance gets data flows and controls. Same numbers for everyone.
- **Present honest, segmented numbers.** "94% overall, 71% on handwritten forms" beats a single
  flattering average. Say how you measured it.

## 6.3 Feedback loops and expectations (including SLAs)

- **Set expectations about non-determinism early.** Stakeholders used to deterministic software need
  to hear that an AI system is measured on a *rate* across a test set, not on one demo.
- **Agree SLAs in terms you can measure:**

| SLA item | Example target (set per project) | Measured by |
| --- | --- | --- |
| Availability | Agreed uptime | Monitoring |
| Latency | p95 response time | Traces |
| Quality | Accuracy on the eval set, per segment | Regression suite |
| Escalation | Share of cases routed to a human, and human turnaround | Queue metrics |
| Cost | Cost per task or per month ceiling | Usage reports |

- Include a **quality SLA**, not just uptime. A system that is up and wrong is failing.
- **Feedback loops:** capture user ratings and reviewer corrections, turn them into new eval cases,
  and report back what changed. Stakeholders who see their feedback used keep giving it.

## 6.4 Documentation and implementation guidance

- **Architecture docs:** context diagram, data flow (what data goes to the model and what comes
  back), components, the ADR log.
- **Implementation guidance** for the build team: prompt and template locations, tool contracts,
  eval commands, how to add a test case, and how to roll back.
- **Runbooks** for operations: known failure modes and their first diagnostic step.
- A handoff with diagrams but no "how to change it safely" guidance is incomplete.

## 6.5 Lifecycle support

An AI system is never "done". Each phase below has a job for the architect and a clear sign it's time to move on:

| Phase | Architect's job | Exit criterion |
| --- | --- | --- |
| **Discovery** | Problem, constraints, success measures, risk | Signed-off requirements and metrics |
| **Design** | Architecture, ADRs, eval plan | Design reviewed by security and compliance |
| **Build and handoff** | Guidance, eval suite, runbooks | Build team can change and test it without you |
| **Monitoring** | Dashboards on quality, latency, cost, escalations | Alerts are tied to SLAs |
| **Iteration** | Feedback into evals, A/B tests, prompt and model updates | Changes pass the regression suite first |

- **Change management is part of the design:** train reviewers, roll out in stages (pilot group,
  then wider), and keep the old process as a fallback until the new one meets its SLAs.
- **Model upgrades are a lifecycle event.** Run the eval suite on the new model before switching.

## Worked example

A logistics firm's operations director asks for "an AI that answers carrier questions." Discovery
shows the real pain is 40 minutes per email looking up contract terms, the contracts contain
confidential rates, and legal must approve anything sent externally. **Response:** write down the
problem, the baseline and the non-goals (no automatic replies to carriers). Record ADR-001: retrieval
over the contract library, with drafts reviewed by staff. Agree SLAs for p95 latency, accuracy on a
labeled set of 200 past questions, and review turnaround. Pilot with one team, feed corrections back
into the eval set, and report segmented results monthly.

## Traps

- Jumping to architecture before success measures are agreed.
- An ADR listing only the chosen option.
- An SLA with uptime but no quality measure.
- One flattering average instead of results by segment.
- Treating handoff as "send the diagram."

## Try it (30 min): paper exercise

**Brief:** a property-management company wants Claude to summarize tenant maintenance requests and
suggest a priority for dispatchers. Requests contain tenants' names and addresses; dispatchers make
the final call; leadership wants "faster repairs."
Write a **one-page ADR** for one decision (for example, which model tier, or batch vs real time) with
at least two options and their consequences. Then write an **SLA table** with five rows: availability,
latency, quality, escalation and cost, each with how you'd measure it.

## Done when

- [ ] You can run discovery in the six-step order and name the Claude twist in each
- [ ] You can write an ADR with context, options, decision and consequences
- [ ] You can explain why an AI SLA needs a quality row
- [ ] You can name each lifecycle phase and its exit criterion
- [ ] You scored 80% or more on [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L06 Models, Prompting and Context](L06-models-prompting-and-context.md)

Source: official exam guide v1.0, Domain 6 objectives and section 4 (MQC: discovery through
deployment and operationalization); `11-Lessons-Learned/INSIGHTS.md` (one colleague who passed, single report);
https://platform.claude.com/docs/en/about-claude/models/choosing-a-model (evaluate before upgrading models).