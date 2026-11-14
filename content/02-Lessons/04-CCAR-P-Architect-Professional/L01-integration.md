# CCAR-P Lesson 1 — Integration (19%, about 12 questions, the BIGGEST)

**Time:** 2–3 hours plus lab 05 · **Practice:** [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Already covered in CCAR-F:** tool descriptions, structured errors, `.mcp.json` and MCP basics
are in [CCAR-F L02](../02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md).
This lesson is about the judgment on top: which mechanism, how many tools, who is allowed to call
them, and how you'd know it's working.

## 3.0 The big idea

Integration is the plumbing that connects Claude to real systems, and the exam tests whether that plumbing is safe and fit. Give each agent only the tools it needs, carry the user's identity all the way to the data, pick the retrieval method that fits the data, and log enough to see which part broke.

## 3.1 Capability bloat

- Every tool you add makes every other tool a little harder to pick correctly, and it costs
  tokens on every request.
- **Scope tools by role.** Each agent gets the tools its job needs and nothing more.
- A tool the role never uses is **pure risk with no benefit**. Remove it from the configuration.
- **Wrong fixes:** shorten every description, merge everything into one "mega-tool" with a mode
  parameter, or switch to a bigger model and hope it chooses better.

## 3.2 Authentication and authorization gaps

- **Authentication** asks *who is calling?* **Authorization** asks *what may they do?* Most gaps
  on the exam are authorization gaps.
- The classic gap: the agent, or the retrieval service, runs under **one shared service account
  with broad rights**. Then any user can reach anything that account can reach.
- **Carry the end user's identity through** to the tools and the data. Filter by that user's
  permissions **at the data layer**, before anything reaches the model.
- Never rely on the prompt for access control. "Don't show HR files to non-HR staff" is a
  suggestion, not a boundary.
- Keep **credentials out of the prompt and out of logs.** Scope each token to the fewest actions
  it needs.
- **Order of controls:** remove the privilege → enforce it in code → add a human approval for
  consequential actions → log and audit. Detective controls come last.

## 3.3 Accuracy vs latency

Every speed or quality dial costs something. Here is what each one buys and what you pay for it:

| Lever | Buys | Costs |
| --- | --- | --- |
| Bigger model, or higher [effort](https://platform.claude.com/docs/en/build-with-claude/effort) | Quality on hard tasks | Latency and tokens |
| Retrieve more chunks, add a reranker | Recall and precision | Latency, and noise in context |
| An extra verification step | Fewer errors | One more round trip |
| [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) of the static prefix | Lower latency **and** cost | Cache writes cost more than normal input (1.25× for the 5-minute cache, 2× for the 1-hour cache); reads cost 0.1×; prompts under the model's minimum length can't be cached. It pays off when the prefix is reused within the cache lifetime ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |

Justify a setting with a **measured number** against a stated SLA. "It felt faster" is not a
justification. The docs say that tuning effort within one model is often a better lever than
switching models ([choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)).

## 3.4 Observability at scale

- Log **traces, not just final answers:** the input, the retrieved chunks and their IDs, each tool
  call with its arguments and result, the model and prompt version, tokens, latency and cost.
- Without traces you can't tell whether a bad answer came from retrieval, a tool, the prompt or
  the model.
- At scale, **sample** full traces and keep metrics for everything. Alert on drift: retrieval hit
  rate, refusal rate, error rate, cost per request.
- Redact personal data in logs, because logs are data too.

## 3.5 RAG pipeline: chunking and indexing

```text
ingest → clean → chunk → embed and index (plus metadata) → retrieve → rerank → assemble context → generate
```

- **Chunk along the document's own structure:** sections, clauses, FAQ entries, table rows. A
  fixed character count cuts ideas in half.
- Keep a **little overlap** between chunks, and give each chunk its **context** (the document
  title, the section path). Anthropic calls this [contextual retrieval](https://www.anthropic.com/news/contextual-retrieval).
- Store **metadata** with each chunk: source, date, version, owner, and the access-control list.
- **Re-indexing is a release.** Re-embed with the *same* embedding model the query side uses,
  remove stale versions, and run a retrieval eval before switching over.

## 3.6 Retrieval matched to data shape and query pattern

Searching is like asking for help in a library: an index finds exact words, a librarian finds "something like this". Match the method to what's being searched:

| Data or query | Best fit |
| --- | --- |
| Exact terms: codes, part numbers, names, error strings | **Keyword or BM25** |
| Paraphrased, conceptual questions | **Vector (semantic)** |
| A mix of both, which is most enterprise search | **Hybrid** (keyword + vector), then **rerank** |
| "Only current policy", "only my region", "only docs I may see" | **Metadata filters** |
| Numbers, totals, joins across tables | **A structured query** (SQL or an API) exposed as a tool, not embeddings |
| Frequently changing knowledge | Retrieval at query time, never pasted permanently into the prompt |

## 3.7 Connection protocols

There are three ways to connect Claude to another system. Pick by who decides when the call happens:

| Use | When |
| --- | --- |
| **MCP server** | The same capability is reused by several agents or clients, and the model should discover and call it |
| **Direct API or CLI call** | A fixed step in a pipeline that your code runs anyway. The model doesn't need to choose it |
| **Agent-to-agent** | Two independently owned autonomous agents have to negotiate or hand off work |

The Messages API can connect to remote MCP servers directly through the
[MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).

## 3.8 Progressive discovery vs monolithic context

- **Monolithic:** load every tool and every document up front. It's simple, but it wastes tokens,
  and as context grows, "accuracy and recall degrade" (**context rot**, [context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)).
- **Progressive:** start with a small, relevant set and let the agent pull in more as needed.
  The [tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
  discovers and loads tools on demand, and Skills load their full instructions only when they're
  relevant ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)).
- Choose monolithic when the surface is small and stable. Choose progressive when there are many
  tools or documents, or they change often.

## Worked example

A hospital builds a policy assistant for clinicians. It uses vector search over policy PDFs,
through one service account. Three problems show up. Nurses see draft HR policies. Queries for a
drug code ("the rule for code X-104") miss. And totals like "beds free on ward 3" come back wrong.
**Answer:** pass the clinician's identity through and filter by document permissions at retrieval
time. Go hybrid, with BM25 for the codes, plus a metadata filter for status = approved. Answer the
bed counts through a structured-query tool on the bed system, not from embedded text. "Add a line
to the prompt saying not to show drafts" and "use a bigger model" fix nothing.

## Traps

- "Log the delete tool's use so misuse can be audited." Remove the tool.
- "The model got worse after the re-index." Check retrieval first.
- "Embed the spreadsheet so Claude can add up the column." Use a structured query.
- "Load all 60 tools, in case one's needed." Scope by role, and discover progressively.
- "Make everything an MCP server." A fixed pipeline step is a plain API call.

## Try it (60 min): lab 05, Retrieval comparison

Do step 7, **Retrieval comparison**, in
[lab 05](../../06-Labs/05-CCAR-P-eval-harness/README.md#7-retrieval-comparison). Build about 20
question and right-chunk pairs over a small document set. Run keyword-only, vector-only and hybrid
retrieval, score how often the right chunk lands in the top 5 (recall@5), and note which question
types each method wins.

## Done when

- [ ] You can list the order of controls, from removing privilege to auditing
- [ ] You can match 6 data or query shapes to a retrieval strategy
- [ ] You can say when MCP, a direct API call or agent-to-agent fits
- [ ] You can explain context rot and when progressive discovery wins
- [ ] You scored 80% or more on [Lesson 1 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L02 Solution Design and Architecture](L02-solution-design-and-architecture.md)

Source: official CCAR-P exam guide v1.0, Domain 3 objectives and sample 1; Anthropic docs linked above.