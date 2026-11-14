# CCAR-P Lesson 4 — Governance, Safety and Risk Management (14%, about 9 questions)

**Time:** 2 hours plus lab 03 (hook part) · **Practice:** [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Already covered:** the three bands of use, data minimization and "the stricter policy wins" are in
[CCAO-F L06](../01-CCAO-F-Associate/L06-governance-risk-and-responsible-use.md). This lesson is about
what the *architect* builds so those rules hold in production.

## 5.0 The big idea

Safety is built, not asked for. Remove what an agent doesn't need, enforce rules in code rather than in the prompt, put a human on any decision that can't be undone, and design so the compliance team can check your work.

## 5.1 Guardrails and safety controls: layer them

One control is a single point of failure. Put a check at every place where things can go wrong:

| Layer | What it does | Claude example |
| --- | --- | --- |
| **Input** | Screens what users send before the main call | A small, fast model (the docs use Haiku 4.5) classifies input as harmful or not, returning a structured verdict |
| **Untrusted content** | Treats emails, web pages, files and tool results as *data*, not orders | Put third-party text only in `tool_result` blocks, JSON-encode it, say where it came from, screen it before Claude acts |
| **Tool permissions** | Limits what a successful attack can do | Remove tools the role doesn't need; sandbox the rest; scope credentials narrowly |
| **Hooks / code gates** | Deterministic checks the model can't talk its way past | A `PreToolUse` hook that blocks a dangerous command; a code check before a refund over a limit |
| **Output** | Checks the answer before anyone sees or uses it | Schema validation, citation checks, a policy classifier |
| **Monitoring** | Catches what got through | Review outputs for signs of successful injection and refine the layers |

- **Removing beats watching.** The official sample rationale for least privilege: logging and
  confirmation prompts are *compensating* controls; removing an unneeded capability eliminates the
  risk. (Exam guide, sample 1.)
- **Prompts guide, code enforces.** "Never delete accounts" in a system prompt is a request. A hook or
  a missing tool is a guarantee.

## 5.2 Risks, limitations and failure modes

AI systems fail in a few predictable ways. Know what each one looks like and its main fix:

| Failure mode | What it looks like | Main mitigation |
| --- | --- | --- |
| **Hallucination** | Confident, fluent, wrong | Let Claude say "I don't know"; ground in direct quotes; require citations and retract unsupported claims; restrict to provided documents |
| **Prompt injection** | A document or tool result tells Claude to do something else | The untrusted-content layer plus least privilege, so a successful injection does little damage |
| **Non-determinism** | Same input, different output | Structured outputs, examples, fixed templates; evaluate on a *set*, not one run |
| **Drift** | Quality slides after a model, prompt or data change | Regression suite and monitoring (see [L03](L03-evaluation-testing-and-optimization.md)) |
| **Over-reliance** | Reviewers approve smooth text without reading it | Show sources and confidence; sample reviewer decisions; make disagreement easy |

The hallucination guide ends with the key point: these techniques **reduce** hallucinations but
don't **eliminate** them, so always validate critical information.

## 5.3 Human-in-the-loop: route by confidence *and* consequence

Ask two questions: how sure is the system, and how bad is it if it's wrong? The answers tell you who decides:

| | Low consequence (reversible) | High consequence (irreversible, money, health, legal) |
| --- | --- | --- |
| **High confidence** | Automate, spot-check a sample | Human approval anyway |
| **Low confidence** | Queue for review | Human decides; Claude only drafts |

- Reviewing **everything** doesn't scale; reviewing **nothing** is negligent; **random sampling**
  misses the rare risky case. Route on both axes.
- **Irreversible actions need an approval step** in the workflow, not just a prompt instruction.
  Anthropic's prompting guide suggests asking before destructive, hard-to-reverse or externally
  visible actions; the architect makes that ask a real gate.
- Confidence must be **calibrated** against labeled data before you trust it for routing.

## 5.4 Compliance: what the architect decides

You don't certify anything; you design so the compliance team *can*. For any regulated scenario, ask:

| Question | Why it matters to the design |
| --- | --- |
| **Which regime applies?** GDPR (personal data of people in the EU), HIPAA (US health information), FedRAMP (US federal cloud) | Decides the rest of this table |
| **Data residency:** where may the data be processed and stored? | Which platform, region or deployment you can use |
| **Retention:** how long may prompts, outputs and logs be kept? | Log design, deletion jobs, erasure requests |
| **Contracts:** is a business associate agreement (BAA) or other agreement needed and in place? | Whether regulated data may be sent at all |
| **Access logging:** who saw what, when? | Audit trail at the boundary |
| **Minimization:** does the model need this field? | De-identify or tokenize *before* the call; re-associate locally |

- **Enforce compliance before the boundary.** An instruction to the model acts too late: the data has
  already been sent.
- **Audit logging vs data protection:** find out what the audit actually needs before logging full
  prompts, which may contain personal data.
- **Don't assert which certifications or agreements Anthropic or a cloud platform holds.** Check with
  your compliance team and Anthropic's current commercial terms and trust center.

## 5.5 Ethical AI: bias, fairness, transparency

- **Bias and fairness** are tested, not assumed: slice your eval set by user group and compare error
  rates. A good average can hide a bad group.
- **Transparency:** tell users when AI is involved, show sources, and explain how to reach a human.
- **Accountability** stays with the organization that deployed the system, not the model provider.
- Anthropic's [constitution](https://www.anthropic.com/constitution) describes Claude as aiming to be
  broadly safe, broadly ethical, compliant with Anthropic's guidelines and genuinely helpful, in that
  priority order. Claude's own values are one layer; your design is still responsible for the rest.

## Worked example

A regional clinic network wants Claude to draft replies to patient portal messages and to cancel or
rebook appointments. **Design:** strip or tokenize identifiers before the call and re-associate
locally; confirm the required agreements with compliance first. Treat the message body as untrusted
data. Give the agent a `rebook` tool but no `cancel` tool; cancellations go to a staff queue. A
`PreToolUse`-style gate blocks any rebooking more than 30 days out. Drafts about symptoms always get a
clinician's review; routine scheduling replies with high confidence are spot-checked. Log access at
the boundary, with retention set by the compliance team.

## Traps

- "Add logging to the dangerous tool." Remove the tool if the role doesn't need it.
- "Tell the model to ignore PHI." The data has already crossed the boundary.
- "Review a random 5%." It misses the rare high-consequence case.
- "Anthropic is certified for X, so we're compliant." Check the current terms; compliance is yours.
- "The model is aligned, so we don't need guardrails."

## Try it (45 min): lab 03, hook part

In [lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md), add a `PreToolUse` hook that
blocks one destructive command (for example `rm -rf`) and explains why. Then add an approval step: a
tool that proposes an irreversible action and waits for a human "yes" before the action runs. Write
down which layer each control belongs to.

## Done when

- [ ] You can name the six guardrail layers and give a Claude example of each
- [ ] You can place a scenario in the confidence-by-consequence grid
- [ ] You can list the six compliance questions without claiming a certification
- [ ] You can explain why a prompt instruction isn't a compliance control
- [ ] You scored 80% or more on [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L05 Stakeholder Communication and Lifecycle](L05-stakeholder-communication-and-lifecycle.md)

Source: official exam guide v1.0, Domain 5 objectives and sample 1;
https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks;
https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations;
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices (balancing autonomy and safety);
https://docs.claude.com/en/docs/claude-code/hooks; https://www.anthropic.com/constitution.