# CCDV-F lessons (Claude Certified Developer: Foundations): Ready

One lesson per official domain (Claude Code and Eval share L07), organized by the skills in the
[v1.0 exam guide](https://anthropic-partners.skilljar.com/page/partner-certifications), section 6.

| # | Lesson | Weight | Practice | Lab |
| --- | --- | --- | --- | --- |
| L00 | [Orientation](L00-orientation.md) | none | diagnostic | — |
| L01 | [Applications and Integration](L01-applications-and-integration.md) | **33.1%** | [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [04 API modes](../../06-Labs/04-CCDV-F-api-modes/README.md) |
| L02 | [Model Selection and Optimization](L02-model-selection-and-optimization.md) | 16.8% | [Lesson 2 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [04 API modes](../../06-Labs/04-CCDV-F-api-modes/README.md) |
| L03 | [Agents and Workflows](L03-agents-and-workflows.md) | 14.7% | [Lesson 3 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [02 coordinator](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) |
| L04 | [Prompt and Context Engineering](L04-prompt-and-context-engineering.md) | 11.0% | [Lesson 4 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [02 coordinator](../../06-Labs/02-CCAR-F-coordinator-extraction/README.md) |
| L05 | [Tools and MCPs](L05-tools-and-mcps.md) | 10.6% | [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [03 MCP server](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) |
| L06 | [Security and Safety](L06-security-and-safety.md) | 8.1% | [Lesson 6 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [03 MCP server](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) (hook) |
| L07 | [Claude Code, Eval and Debugging](L07-claude-code-eval-and-debugging.md) | 3.1% + 2.6% | [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html) | [03 MCP server](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md) (part 2) |

**How to use:** read a lesson, do its "Try it" lab step, then take its practice session and log
the score in your own notes.

**Order:** L00, then **L01 first** (a third of the exam), then L02 to L07 in order. Don't skip L07:
people who passed saw more Claude Code than its 3% weight. After that, do the
[simulations](../../04-Simulations/03-CCDV-F-Developer/README.md).

**Overlap with CCAR-F:** about two-thirds of this exam overlaps CCAR-F (*Single report:* one colleague who passed,
August 2026, in [Insights](../../11-Lessons-Learned/INSIGHTS.md)), so take it soon after. Each
lesson links the matching CCAR-F section and spends its depth on what's new for developers.
Review these first:

| CCDV-F lesson | Review in CCAR-F |
| --- | --- |
| L01, L02 | [L04 Prompt Engineering and Structured Output](../02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) (4.5 batches) |
| L03 | [L01 Agentic Architecture and Orchestration](../02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) |
| L04 | [L04](../02-CCAR-F-Architect-Foundations/L04-prompt-engineering-and-structured-output.md) and [L05 Context Management and Reliability](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |
| L05 | [L02 Tool Design and MCP Integration](../02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| L06 | [L01 1.4–1.5 hooks](../02-CCAR-F-Architect-Foundations/L01-agentic-architecture-and-orchestration.md) and [L02 2.4 `${ENV}`](../02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md) |
| L07 | [L03 Claude Code Configuration and Workflows](../02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md) and [L05 5.3](../02-CCAR-F-Architect-Foundations/L05-context-management-and-reliability.md) |

**Build as you learn.** The guide asks you to build at least one app that uses the API, a tool,
prompt and context engineering, and simple security and evals. Labs 02, 03 and 04 in
[`06-Labs/`](../../06-Labs/README.md) cover that.