# 06 — Labs

One folder per lab. Number the folders in the order you do them. All five labs are written. They come from
each exam's plan in [`../01-Curriculum/`](../01-Curriculum/00-Overview.md), and each lesson's "Try it"
section links to the one it needs:

- `06-Labs/01-CCAO-F-engagement-project/`: a Project with instructions, versioned knowledge and a pass / revise / fail review
- `06-Labs/02-CCAR-F-coordinator-extraction/`: a coordinator with two subagents, extraction against a JSON schema, and a validation-and-retry loop
- `06-Labs/03-CCAR-F-mcp-server-claude-code/`: an MCP server with structured errors, `.mcp.json`, CLAUDE.md, a slash command and a hook
- `06-Labs/04-CCDV-F-api-modes/`: the same task run in real time, with caching and through the Batch API, comparing cost and latency
- `06-Labs/05-CCAR-P-eval-harness/`: a test set, graded scoring and a regression check for lab 02

Each lab folder gets a `README.md` with three lines:

1. Which credential this lab supports (the exam code).
2. What “done” looks like.
3. What you learned, written after you finish.

Then add the lab path on that credential’s row in your private progress tracker (not published).

If a lab becomes a tool you will keep using on delivery work, move it to its own folder under `01 - Projects/` and leave the lab folder here as a one-line pointer to the new home. Customer project files stay in the customer folder.

## Begin with the architecture decision boundary

New to cloud applications? [Lab 08: eight local architecture experiments](08-CCAR-F-architecture-decisions/README.md) teaches the code-owned boundary before API setup. Then follow the actual API/MCP labs; local fixtures are not a substitute for executed tool-call experience.