# CCDV-F Lesson 5 — Tools and MCPs (10.6%, about 6 questions)

**Time:** 2 hours plus lab 03 · **Practice:** [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Skills:** Tool Implementation 4.4% · MCP Server Development 2.1% · Agentic Customization 4.1%
**Already covered in CCAR-F:** [L02 Tool Design and MCP Integration](../02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md)
(descriptions, error categories, 4–5 tools, `tool_choice`, `.mcp.json`). Review it first. This
lesson adds the developer side: the round trip in code, where tools run, and writing a server.

## 8.0 The big idea

Claude only *asks* for a tool; your code runs it and sends the result back. Then pick the right
home for each capability: built-in tools first, a custom tool for one app, a Skill for know-how,
an MCP server for a connection many apps share.

## 8.1 The tool round trip

1. You send `tools`: each has a `name`, a `description` and an `input_schema` (JSON Schema).
2. Claude replies with `stop_reason: "tool_use"` and one or more `tool_use` blocks (`id`, `name`,
   `input`).
3. **Your code runs the tool** and sends back a `tool_result` block with the matching `tool_use_id`
   in the next user message.
4. Repeat until `stop_reason: "end_turn"`. That loop is your **agentic harness**.

- **Dispatch:** the harness maps `name` to a function. An unknown name or bad input is **your** bug
  to catch and report back, not a crash.
- **Errors:** return a `tool_result` with **`is_error: true`** and a clear message (what failed,
  whether retrying helps). Claude can then retry, try another tool, or tell the user.
- **Several tools in one reply** (parallel calls): return **all** their results together. Use
  `disable_parallel_tool_use` if you need one at a time.
- **`strict: true`** on a tool guarantees its input matches your schema ([L04 6.5](L04-prompt-and-context-engineering.md)).
- The SDKs' **Tool Runner** can run this loop for you. Write it by hand once so you understand it.
- **Descriptions steer choice.** If Claude isn't using a tool, sharpen the description or add "Use
  the tools to investigate before responding". To require a call, set `tool_choice`.
- **Missing inputs:** Claude may **guess** a required value (for example a city) instead of asking,
  especially smaller models. Validate inputs; don't trust a plausible default.

## 8.2 Client-side vs server-side tools

| | Client tools | Server tools |
| --- | --- | --- |
| Runs on | **Your** application | **Anthropic's** infrastructure |
| Examples | Your own functions; Anthropic-schema tools like `bash`, `text_editor`, memory | `web_search`, `web_fetch`, code execution, tool search |
| You handle | `tool_use` → execute → `tool_result` | Nothing; results come back in the same response |
| Cost | Tokens only | Tokens **plus** usage fees for some (web search per search) |

- Tool definitions cost input tokens, and a hidden tool-use system prompt is added too. Big tool
  sets cost money and context. Use the **tool search tool** to load tools on demand.

## 8.3 Approvals and building the tool set

- **Approval pattern:** for risky actions (refunds, deletes, sending email), the harness **pauses
  before executing** and asks a human, or checks a rule in code. The model proposes; your code
  decides.
- **Tool set rules:** few tools with **distinct** jobs; narrow tools (`load_document`) over generic
  ones (`fetch_url`); only the tools this agent needs. A tool the agent doesn't have can't be
  misused ([L06](L06-security-and-safety.md)).
- **External systems:** keep credentials in the tool's code or config, never in the prompt. Return
  only the fields Claude needs.

## 8.4 Writing an MCP server

MCP (Model Context Protocol) is an open standard for connecting Claude apps to tools and data.

- **Host, client, server:** the host app (Claude Code, Claude Desktop, your agent) runs an MCP
  **client** for each **server** it connects to. The server exposes capabilities; the client uses them.
- **Three things a server can offer:**

| Primitive | What it is | Who triggers it |
| --- | --- | --- |
| **Tools** | Actions with a schema (`create_ticket`) | The model decides to call them |
| **Resources** | Readable data by URI (a schema, a doc tree) | The app chooses what to load |
| **Prompts** | Reusable prompt templates | The user picks them (for example as a slash command) |

- **Transports:**
  - **stdio:** the host starts the server as a **local process** and talks over stdin/stdout. Best
    for local tools on one machine.
  - **Streamable HTTP** (network transport): the server runs **remotely** and many clients connect.
    Best for shared, team-wide or hosted servers. Check the current MCP spec for transport details.
- **Authoring:** use an official MCP SDK (Python or TypeScript). Each tool gets a name,
  description and input schema, the same rules as 8.1. Return errors with **`isError`**.
- **Deployment:** stdio servers ship as a command in `.mcp.json`; remote servers ship as a URL with
  auth. The Messages API **MCP connector** connects to **remote** servers without you writing a client.
- **Integration:** in Claude Code, project servers go in `.mcp.json` with `${ENV_VAR}` secrets
  ([CCAR-F 2.4](../02-CCAR-F-Architect-Foundations/L02-tool-design-and-mcp-integration.md)).

## 8.5 Built-in tool, custom tool, Skill or MCP?

| You need | Choose | Why |
| --- | --- | --- |
| Files, shell, search, web basics | **Built-in tools** | Already there, trained on, no code |
| An action inside **one** app, tied to its code | **Custom tool** | Simple, lives with the app |
| **Know-how**: a procedure, conventions, templates, helper scripts | **Skill** | Loaded **on demand**, so it costs little context until used |
| An integration **shared by several apps**, maintained on its own | **MCP server** | Build once, connect from any MCP host |

- Built-in tools **don't reach your internal APIs** on their own. That needs a custom tool or MCP.
- A Skill **teaches how**; a tool or MCP server **does**. They combine: a Skill can describe
  how to use an MCP server's tools well.

## Worked example

Three internal apps each need to look up shipment status from the same REST service, and the
logistics team wants to own the integration. **Answer:** an MCP server that exposes
`get_shipment_status` as a tool, deployed over HTTP so all three connect. A custom tool copied
into each app means three copies to maintain. A Skill can't call the API by itself.

## Traps

- "Claude runs my function." Claude only **asks**; your code runs client tools.
- Returning an empty result on a failure instead of `is_error: true`.
- Answering only one of several parallel `tool_use` blocks.
- "A Skill replaces an MCP server." One is instructions, the other is a live connection.
- stdio for a server many machines must share.

## Try it, lab 03 (60 min)

In [lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md), build the MCP server with
2 tools and 1 resource over stdio. Make one tool return `isError` with a retry hint. Then call the
same logic as a plain custom tool from a Messages API script with `is_error`, and note what changed.

## Done when

- [ ] You can write the 4-step tool round trip from memory
- [ ] You can sort any tool into client-side or server-side
- [ ] You can name MCP's 3 primitives and who triggers each
- [ ] You can pick stdio or HTTP and say why
- [ ] You can pick built-in, custom, Skill or MCP for a scenario, with a reason
- [ ] You scored 80% or more on [Lesson 5 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [L06 Security and Safety](L06-security-and-safety.md)

Source: CCDV-F exam guide v1.0, Domain 8 (sample 3 covers the MCP-for-reuse topic);
[tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview);
[structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs);
[MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector);
MCP primitives and transports: [modelcontextprotocol.io](https://modelcontextprotocol.io).