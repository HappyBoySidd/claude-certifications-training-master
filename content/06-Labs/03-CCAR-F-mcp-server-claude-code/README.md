# Lab 03 — An MCP server, wired into Claude Code with a guardrail hook (CCAR-F, CCDV-F, CCAR-P)

<!-- layered-scenario-migration -->
## Read the experiment before building

**Two ways to use this lab:** read and predict with no setup, or run the separately identified fixtures/build steps after completing their prerequisites below. These layers are paper experiments until you execute an implementation. An expected trace is not a captured run. Use fictional records in a disposable folder; do not connect real customer data or business effects. Keep input, expected result, observed result and recovery evidence separately.

### Stage 1 — Two tools sound equally useful

A service assistant handles a balance question and an address change. Both tools are named `manage_account` and described as “manage customer data.” A balance request sometimes triggers the write operation. The working one-tool demo hid this ambiguity.

**Original exam-style practice — choose ONE.** Which tool-interface change most directly improves selection reliability while preserving the read/write boundary?

A. Use one generic tool and explain all differences in a long system prompt.

B. Give each capability a distinct purpose, precise description, input schema and side-effect boundary.

C. Add more overlapping aliases so the model has more options.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** Name the actual job, such as read balance versus propose address change, and state when each is appropriate. A hides the distinction inside one broad interface; C increases confusion. A schema describes accepted arguments; authorization is a separate check.

**Follow the changed path:**

```text
customer need → distinct tool purpose → typed arguments → runtime authorization → service result
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Use a balance request and an address request. Record the selected capability and arguments separately from permission and execution outcome. A selected write tool does not authorize the write.

</details>

**Changed-constraint decision — choose ONE before revealing:** The model chooses the correct tool but supplies an invalid account ID. A: redesign names alone; B: validate arguments and return a specific correctable error without executing.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Correct selection and valid arguments are different requirements. Repair the failing layer.

</details>

**Objective connections:** [2.1](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md), [2.3](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.3.md).

### Stage 2 — An unavailable service looks like an empty account

The balance tool normally returns current funds. Today the server cannot reach the bank service. It returns an empty list and the assistant says the customer has no accounts. The error was hidden as ordinary data.

**Original exam-style practice — choose ONE.** Which MCP tool-result contract best supports correct error propagation and recovery?

A. Return an empty successful result on every failure.

B. Return an explicit failure category and useful retryability context without exposing secrets; preserve available partial data as partial.

C. Ask the model to infer the failure from response length.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The caller must distinguish “there are no accounts” from “we could not check.” A confuses those meanings; C guesses. Permission denial, invalid input, insufficient stock and transient outage need different responses.

**Follow the changed path:**

```text
business API failure → tool failure category → caller recovery policy
confirmed empty data → successful empty result → ordinary answer
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Inject a timeout, bad input and permission denial. Expect different categories; do not retry permanent invalid input as though waiting would fix it.

</details>

**Changed-constraint decision — choose ONE before revealing:** The service denies access. A: retry with higher model confidence; B: stop that action and use the approved permission/escalation route.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Confidence cannot grant access. Keep access failures separate from temporary outages.

</details>

**Objective connections:** [2.2](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md).

### Stage 3 — A proposal becomes a money movement

The customer now requests a refund. A person approves USD 80 for ORD4, but a later proposal changes to USD 90. The old design remembers only “approved: yes.” That broad flag would let a changed action through.

**Original exam-style practice — choose ONE.** Which control best enforces approval scope before execution of a side-effecting tool?

A. Instruct Claude to remember the approved amount.

B. Validate the current principal, order, amount and approval validity against the bound proposal in the runtime/backend before submitting the action.

C. Execute first and inspect the model explanation afterward.

<details><summary>What is this asking? (optional, after reading the choices)</summary>

Identify the requirement that the current application fails to meet. Compare the proposed mechanisms against that requirement. Explain unfamiliar terms using the context above, then record a choice and your reason before opening the repair.

</details>

<details><summary>Reveal the repair and replay evidence</summary>

**Choice B.** The program compares this exact action with what was approved. A model reminder can help behavior but cannot replace that gate. C finds the problem after money may already move. A hook can intercept an attempted call; business authorization still belongs at the authoritative service boundary.

**Follow the changed path:**

```text
proposal → approval bound to exact action → runtime/backend gate → business API
changed target, amount or expired approval → deny or request new approval
```

The arrows show information or control moving between components; they do not imply that the model executes backend code itself.

**Replay and inspect:** Keep the approval record and action fields. Changing one field must block submission; a matching permitted action still needs a real business receipt before being called settled.

</details>

**Changed-constraint decision — choose ONE before revealing:** The write timed out after submission. A: blindly resubmit; B: inspect the business operation status with the operation key before deciding whether retry is safe.

<details><summary>Reveal changed-constraint reasoning</summary>

B. Timeout means the caller lacks a result, not that the operation failed. Reconciliation prevents a duplicate effect.

</details>

**Objective connections:** [1.4](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.4.md), [1.5](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md), [1.7](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.7.md).

<!-- /layered-scenario-migration -->


**Supports:** CCAR-F L02, L03 · CCDV-F L05, L06, L07 · CCAR-P L04, L07 · **Time:** 2–3 hours ·
**Needs:** Claude Code, Python 3.10+, and `pip install mcp`.

## Understand the design before setup

Before executing this lab, read the [grounded assistant and MCP boundary](../../02-Lessons/02-CCAR-F-Architect-Foundations/architecture-studio/AS-03-grounded-assistant.md) and its plain-language/technical choices. Reading requires no credentials; **running this lab does require the setup, account, environment and permission prerequisites below**. Keep its real execution evidence separate from the paper case and local Lab08 fixture. Use the [full learning journey](../../02-Lessons/02-CCAR-F-Architect-Foundations/learning-journey.md) to return to objectives, practice and repair.

## Connect this build to scenario decisions

**Before building:** [Choose a case in the scenario studio](../../02-Lessons/02-CCAR-F-Architect-Foundations/scenario-studio.md). Predict the result before running each failure injection.

Compare a denied permission, insufficient stock and an uncertain reservation result. They need different recovery. Verify connection, tool inclusion and execution authority separately; do not infer settlement or safe unattended execution from a mode flag.

**Evidence to keep:** synthetic input, observed tool/result or hook outcome, expectation, actual failure category, recovery and a changed-condition retest. Do not mark this lab complete from reading alone.

- [FV-04 — Bind approval to this action](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.4.md#variant-fv-04) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=1.4&variant=FV-04)
- [FV-08 — Make capabilities distinguishable](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md#variant-fv-08) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.1&variant=FV-08)
- [FV-09 — Route the actual error category](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md#variant-fv-09) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.2&variant=FV-09)
- [FV-11 — Separate connection from inclusion](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md#variant-fv-11) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=2.4&variant=FV-11)
- [FV-13 — Put instructions at their real scope](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.1.md#variant-fv-13) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.1&variant=FV-13)
- [FV-18 — Run CI with observable failure](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.6.md#variant-fv-18) · [Test the decision](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html?exam=CCAR-F&objective=3.6&variant=FV-18)

**After building:** explain which constraint changes the answer, then use [drawings](../../02-Lessons/02-CCAR-F-Architect-Foundations/decision-atlas.md), [recall](../../02-Lessons/02-CCAR-F-Architect-Foundations/FLASHCARDS.md) and [simulations](../../04-Simulations/02-CCAR-F-Architect-Foundations/README.md) to transfer the mechanism.

## What you'll build and why

You'll build a tiny inventory tool server, plug it into Claude Code, and put guard rails around
it. The point is to feel, hands-on, where a rule has to live so it really holds.

```text
you ──> Claude Code ──(MCP)──> inventory server ──> inventory.json
             │
             ├── PreToolUse hooks: block rm -rf, ask before big reservations
             ├── CLAUDE.md + .claude/rules/: project memory
             └── restock-report skill: runs in its own forked context
```

Words you'll meet, in plain terms:

- **MCP (Model Context Protocol):** a standard way for an app like Claude Code to talk to a
  "server" program that offers tools.
- **MCP server:** a small program that lists tools and runs them when asked.
- **Tool:** one action the model can ask for, such as `get_item`.
- **`isError`:** a flag on a tool result that says "this call failed". Without it, the client
  treats the result as a success.
- **Scope:** where a server is registered. *Project* scope lives in `.mcp.json` and is shared
  with the team; *user* scope lives in your own `~/.claude.json`.
- **Hook:** a script Claude Code runs at a fixed moment, such as just before a tool call
  (**PreToolUse**). Its answer can block or pause the call. The model can't talk its way past it.
- **Skill:** a folder with a `SKILL.md` file that packages instructions Claude Code can run on
  request.
- **Forked context (`context: fork`):** the skill runs in a separate sub-context, so its
  working notes don't fill your main conversation.
- **Plan mode:** Claude Code proposes a plan and waits for your OK before it edits anything.

Task numbers refer to the task statements in the official exam guide.

## Why this matters on the exam

- A rule that *must* hold belongs in a hook or in code, not in the prompt.
- Shared config is committed, and secrets are expanded from environment variables.
- Good tool descriptions and structured errors decide whether the agent recovers.

**Done when:**

- `/mcp` shows `inventory` as connected (approve the project server when asked the first time)
- Claude calls `get_item` and `reserve_item` at least once each, and you can point to both calls
  in the transcript
- `/mcp` shows your user-scope `echo` server and the project `inventory` server at the same time
- asking to reserve 1,000 units returns an `isError` result; the agent does not retry and tells
  you the quantity actually available
- `grep -rn INVENTORY_TOKEN .` over the repo finds only the `${INVENTORY_TOKEN:-}` placeholder
  and the line in `server.py` that reads it, never a real token value
- with the token unset, every tool call returns the `permission` error
- the hook blocks each of `rm -rf build/`, `rm -fr build/` and `rm -r -f build/`, and the
  `build/` folder still exists afterwards
- reserving 20 units shows you an approval prompt; reserving 5 does not
- `/memory` lists the `tests.md` rule while you work on a `test_*.py` file and not while you work
  on `server.py`
- `restock-report` runs in a forked context and can use only the read tools (`list_items` and
  `get_item`)
- your "What I learned" section has two lines: one on what plan mode gave you, one on what it
  cost

## Steps

### 1. A three-tool server

*Practises: tasks 2.1 and 2.2.*

Write a server with the official Python MCP SDK (`FastMCP`):

- `list_items()`: returns every SKU with its name, so the agent can find SKUs it wasn't told.
- `get_item(sku)`: reads one item from a small local JSON file.
- `reserve_item(sku, qty)`: a **write** action. It checks stock and returns an error if there
  isn't enough.

Sample `inventory.json`, next to `server.py`:

```json
{
  "SKU-001": {"name": "Blue mug", "qty": 12},
  "SKU-002": {"name": "Desk lamp", "qty": 3},
  "SKU-003": {"name": "Notebook", "qty": 0}
}
```

At start-up, the server reads `INVENTORY_TOKEN` from `os.environ`. If it's missing **or empty**,
every tool call is refused with a `permission` error. (Empty matters: see step 2.)

Return errors as a result with `isError: true`. A plain returned dict reaches the client as a
*success*, so the agent can't tell anything went wrong. Inside that error result, put a body with
these fields:

- `errorCategory`: `transient`, `validation` or `permission`
- `isRetryable`: for example `false` for "not enough stock"
- a plain sentence on what to do instead

`errorCategory` and `isRetryable` are the fields the CCAR-F exam guide (task 2.2) describes.
They are **your** body fields, not fields defined by the MCP spec. The spec only gives you
`isError` and the content.

Example error body for "reserve 1,000 of SKU-001":

```json
{
  "errorCategory": "validation",
  "isRetryable": false,
  "message": "Only 12 of SKU-001 are in stock. Ask the user whether to reserve 12 or fewer."
}
```

Skeleton (marked parts are yours to fill in; check the current Python SDK docs for how to return
a result with `isError` set):

```python
import json, os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("inventory")
TOKEN = os.environ.get("INVENTORY_TOKEN", "")   # "" when unset or set to empty

def error(category, retryable, message):
    # YOUR CODE: return a tool result with isError: true whose text content is
    # json.dumps({"errorCategory": category, "isRetryable": retryable, "message": message})
    ...

@mcp.tool()
def list_items():
    """YOUR DESCRIPTION: lists every SKU and name; read-only; use it to find SKUs."""
    # YOUR CODE: token check, then return [{"sku": ..., "name": ...}, ...]

@mcp.tool()
def get_item(sku: str):
    """YOUR DESCRIPTION: what it does, the input with an example ("SKU-001"),
    and when NOT to use it (it never changes stock)."""
    if not TOKEN:
        return error("permission", False, "INVENTORY_TOKEN is not set. Ask the user to set it.")
    # YOUR CODE: read inventory.json and return the item, or a validation error for an unknown SKU

@mcp.tool()
def reserve_item(sku: str, qty: int):
    """YOUR DESCRIPTION: a write action; call get_item first; say when NOT to use it."""
    # YOUR CODE: token check, stock check, then update inventory.json

if __name__ == "__main__":
    mcp.run()
```

Write each tool description in full: what it does, its inputs with examples, and when *not* to
use it.

**How you know it worked:** `python3 server.py` starts and waits quietly for input (stop it with
Ctrl+C). After step 2, asking Claude "how many SKU-001 are there?" makes it call `get_item` and
answer 12.

### 2. Register it for the whole team

*Practises: task 2.4.*

Create `.mcp.json` at the repo root, which is committed, so everyone gets the same server.
Secrets come in through environment variables:

```json
{
  "mcpServers": {
    "inventory": {
      "command": "python3",
      "args": ["server.py"],
      "env": { "INVENTORY_TOKEN": "${INVENTORY_TOKEN:-}" }
    }
  }
}
```

Use `python3`: on macOS a bare `python` often doesn't exist. Run `claude` from the repo root, or
put an absolute path to `server.py` in `args`.

Why `${INVENTORY_TOKEN:-}` and not `${INVENTORY_TOKEN}`: if the variable is unset, Claude Code
still loads the config, shows a warning in `claude mcp list`, and passes the literal text
`${INVENTORY_TOKEN}` to the server. Your server would then see a "token" that isn't empty and
might accept it. The `:-` form with nothing after it expands to an empty string instead, and your
server treats empty as missing ([Claude Code MCP docs](https://code.claude.com/docs/en/mcp),
Tier 1, check the current docs).

Personal or experimental servers go in your user config, `~/.claude.json`. Add a tiny echo
server there. Save this as `~/mcp-echo/echo_server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("echo")

@mcp.tool()
def echo(text: str) -> str:
    """Return the text unchanged. Use only to test that MCP is wired up."""
    return text

if __name__ == "__main__":
    mcp.run()
```

Then register it at user scope (use your own absolute path):

```bash
claude mcp add --scope user echo -- python3 /Users/YOU/mcp-echo/echo_server.py
```

**How you know it worked:** `claude mcp list` shows both `echo` and `inventory`, and `/mcp`
inside Claude Code shows both as connected at the same time.

### 3. Project memory and a skill

*Practises: tasks 3.1, 3.2, 3.3 and 3.4.*

*Practises: tasks 3.1–3.4.* Do these as four small parts and check each one before moving on.

#### 3a. Trim `CLAUDE.md`

Run `/init`, then trim the `CLAUDE.md` it creates to the rules that matter, for example
"always call get_item before reserve_item".

**How you know it worked:** run `/memory` and see your trimmed `CLAUDE.md` listed; ask Claude to
reserve 2 of SKU-002 and see it call `get_item` first.

#### 3b. The `restock-report` skill

Create `.claude/skills/restock-report/SKILL.md` with `context: fork`.

Careful: `allowed-tools` **pre-approves** the tools you list, so Claude can use them without
asking. It does **not** stop the skill from using other tools. To actually restrict it, either:

- list the tools to block in `disallowed-tools`, or
- point the skill at a narrow subagent with `agent:` (together with `context: fork`), and give
  that subagent only the read tools. A report should never be able to reserve stock.

The second route is cleaner here. A sketch (check the field names in the
[skills docs](https://code.claude.com/docs/en/skills) and
[subagents docs](https://code.claude.com/docs/en/sub-agents), Tier 1, check the current docs):

```markdown
---
name: restock-report
description: List items with qty under 5 and suggest a restock amount for each.
context: fork
agent: inventory-reader
allowed-tools: mcp__inventory__list_items, mcp__inventory__get_item
---
Call list_items to get every SKU, then get_item for each one, and report which are under 5.
```

…with `.claude/agents/inventory-reader.md` whose `tools:` list holds only
`mcp__inventory__list_items` and `mcp__inventory__get_item` (no `reserve_item`). (A plain command in `.claude/commands/` also works; the skill is
what the guide tests.)

**How you know it worked:** running `/restock-report` returns SKU-002 and SKU-003, and your main
conversation shows only the final report, not the step-by-step calls. Asking the skill to also
run `ls` fails or is refused.

#### 3c. A path-scoped rule

Add `.claude/rules/tests.md` with `paths: ["**/test_*.py"]` in its front matter (check the field
name in the [memory docs](https://code.claude.com/docs/en/memory), Tier 1, check the current
docs).

**How you know it worked:** create `test_server.py`, ask Claude to edit it, then run `/memory`
and see `tests.md` listed. Work on `server.py` instead and `/memory` doesn't list it. (Trust
`/memory`, not Claude's own description of which rules apply.)

#### 3d. Plan mode versus direct

Run one multi-file change (for example "add a `location` field everywhere") in plan mode, and
one single-line fix directly.

**How you know it worked:** in plan mode Claude shows a plan and edits nothing until you approve;
the direct fix just happens. Write your two lines in "What I learned".

### 4. A guardrail hook

*Practises: tasks 1.5 and 3.2.*

In `.claude/settings.json`, add two **PreToolUse** hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/block_rm.py" }]
      },
      {
        "matcher": "mcp__inventory__reserve_item",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/ask_big_reserve.py" }]
      }
    ]
  }
}
```

**Hook 1, `block_rm.py`.** It reads the tool call as JSON on stdin, takes
`tool_input.command`, and, if it matches a recursive force delete (`rm -rf`, `rm -fr`,
`rm -r -f`), prints a reason to **stderr** and exits with code 2. Exit code 2 blocks the call,
and the stderr text is what gets fed back to Claude. A plain substring check for `rm -rf` misses
the other two.

```python
import json, re, sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")
# YOUR CODE: a regex that catches rm with both -r and -f, in any order or split across flags
if re.search(r"YOUR_PATTERN", cmd):
    print("Blocked: recursive force delete. Delete specific files instead.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
```

**Hook 2, `ask_big_reserve.py`.** When `tool_input.qty` is over 10, it prints this JSON to
stdout and **exits 0** (exit 0 is the intended code when you print JSON; exit 2 would block the
call no matter what the JSON says):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Reserving more than 10 units needs a human OK."
  }
}
```

`permissionDecision` takes `allow`, `deny`, `ask` or `defer`. For 10 or fewer, print nothing and
exit 0. See the [hooks docs](https://code.claude.com/docs/en/hooks) (Tier 1, check the current
docs) for the exact input and output format.

The approval hook is a pattern the CCAR-F, CCDV-F and CCAR-P guides all cover: a hard rule
enforced in code, not in the prompt. That's why this one lab supports all three exams.

**How you know it worked:** run `/hooks` and see both hooks listed. Step 5 tests them.

### 5. Try to break it

*Practises: tasks 2.2 and 1.5.* For each test, the expected result is in brackets. Write down
what the agent actually did.

- Ask Claude to reserve 1,000 of SKU-001. [An `isError` result with `isRetryable: false`; Claude
  does not retry and tells you only 12 are in stock.]
- Ask it to "clean up with rm -rf build/", then with `rm -fr` and `rm -r -f`. [All three are
  blocked; Claude shows your stderr reason; `ls build/` still works.]
- Ask it to reserve 20 of SKU-001. [An approval prompt with your reason comes first; after you
  approve, the server returns the stock error, because only 12 are in stock. That's expected.]
  Then 5 units. [No prompt.]
- Unset the variable (`unset INVENTORY_TOKEN`), restart `claude`, and ask for SKU-001. [`claude
  mcp list` still shows the server; every tool call returns the `permission` error, because the
  server sees an empty value.] Then change `.mcp.json` back to `${INVENTORY_TOKEN}` for a moment
  and repeat. [`claude mcp list` warns, and the server receives the literal text
  `${INVENTORY_TOKEN}`. If your check is only "is it set?", the call wrongly succeeds.] Put the
  `:-` back.

## Common traps

| Trap | Symptom you'll see |
| --- | --- |
| Returning a plain dict for an error | Claude says the reservation "worked" when it didn't |
| `${VAR}` without `:-` and an unset variable | `claude mcp list` warns; the server gets the literal `${INVENTORY_TOKEN}` as its token |
| Substring check for `rm -rf` only | `rm -fr build/` runs and the folder is gone |
| Hook prints a reason but exits 1 | The call still runs; exit 1 doesn't block |
| Printing the `ask` JSON and exiting 2 | The call is blocked instead of asking; exit 2 always blocks, whatever the JSON says |
| Using `allowed-tools` to restrict a skill | The skill still runs other tools, it just asks first |
| Bare `python` in `.mcp.json` on macOS | `/mcp` shows `inventory` as failed |
| Putting the real token in `.mcp.json` | `grep` finds the token in a committed file |

Sources: CCAR-F official exam guide v1.0 (Tier 1), task statements 1.5, 2.1–2.4 and 3.1–3.4,
Exercises 1 and 2; CCDV-F guide domains 7 and 8 (Tier 1); [MCP](https://modelcontextprotocol.io)
(Tier 1, check the current docs);
[Claude Code MCP](https://code.claude.com/docs/en/mcp),
[hooks](https://code.claude.com/docs/en/hooks),
[skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[memory](https://code.claude.com/docs/en/memory) and
[settings](https://code.claude.com/docs/en/settings) (all Tier 1, check the current docs).

## Next

Next: [SIM-05](../../04-Simulations/02-CCAR-F-Architect-Foundations/SIM-05-developer-productivity.md).

## What I learned

- Plan mode gave me:
- Plan mode cost me:

## Decision-variant failure acceptance

Use the existing synthetic fixture and a disposable local state. Retain input, trace, failed check and recovery evidence; these tests do not authorize production effects.

- **FV-09:** Return success with an empty record list, a permission denial and a timeout in separate runs. Record three different recoveries; do not treat all as retryable. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md#variant-fv-09).
- **FV-11:** Connect the server without explicitly including a resource. Inspect the host discovery/inclusion trace and avoid claiming invisible data was used. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md#variant-fv-11).
- **FV-05:** Place a validation failure after the synthetic write. Show why a pre-action gate is needed to prevent it and why a post-result check cannot undo it. [Exact teaching repair](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md#variant-fv-05).


<a id="benchmark-evidence-tasks"></a>
## Objective evidence tasks — predict, inspect, explain

**Optional offline files:** [Python inspector](site:downloads/benchmark_exercises.py) and [synthetic fixture data](site:downloads/benchmark-fixtures.json). Save both beside each other; run the script with Python 3. The output validates only the controlled example, not Claude runtime behavior.

These original tasks extend this existing LAB without replacing its integration setup. Each contains its own input, failure and checkable result. You can read them without installation. Optional Python replay is offline; live tool routing, permissions, rule loading and third-party services remain unverified until you run those integration steps.

- [1.5: Objective 1.5 — Use hooks to normalize results and intercept actions](#benchmark-exercise-1-5)
- [2.1: Objective 2.1 — Design tool interfaces that are hard to confuse](#benchmark-exercise-2-1)
- [2.2: Objective 2.2 — Return errors that support the right recovery](#benchmark-exercise-2-2)
- [2.3: Objective 2.3 — Scope each agent’s tools and control tool choice](#benchmark-exercise-2-3)
- [2.4: Objective 2.4 — Integrate MCP with the right scope and discoverability](#benchmark-exercise-2-4)
- [3.1: Objective 3.1 — Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization](#benchmark-exercise-3-1)
- [3.2: Objective 3.2 — Create and configure custom slash commands and skills](#benchmark-exercise-3-2)
- [3.3: Objective 3.3 — Apply path-specific rules for conditional convention loading](#benchmark-exercise-3-3)


<a id="benchmark-exercise-1-5"></a>
### Worked evidence task — 1.5: test the boundary

**Original technical decision.** A pre-execution gate denies a credit call, while a second run detects a violation only after the call. Which trace demonstrates prevention rather than detection?

**In everyday terms:** A warning after money moved is useful evidence, but it did not prevent the move.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "operation": "issue_credit",
  "before_hook": "deny",
  "after_hook": "flag",
  "service_call_count_before": 0
}
```

#### Break, choose, repair, prove

1. **Break:** Run one denial before execution and one detection after execution. Name the exact failed assumption before proposing another component.
2. **Choose:** Count service invocations separately for the pre-call denial and the post-call alert. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Denied pre-call produces no side effect; post-call inspection cannot undo an already completed action. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-1.5.md#intercept) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.5 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 1.5` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "pre_denial_service_calls": 0,
  "post_detection_service_calls": 1,
  "post_detection_undo_proven": false
}
```

**Why this matters:** A warning after money moved is useful evidence, but it did not prevent the move. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview) · [Claude Agent SDK Hooks Documentation](https://platform.claude.com/docs/en/agent-sdk/hooks). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-2-1"></a>
### Worked evidence task — 2.1: test the boundary

**Original technical decision.** Read-only delivery questions and authorized credit requests share a tool catalog. Which routing evaluation distinguishes description quality from prompt conflict?

**In everyday terms:** Count the actual choices. Do not report an improvement before testing it.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "tools": {
    "read_status": "lookup only",
    "issue_credit": "mutates; authorization required"
  },
  "requests": [
    "Where is order O17?",
    "Was O17 delivered?",
    "Show tracking for O17",
    "Which carrier has O17?",
    "Read the status of O17",
    "Has O17 shipped?",
    "Apply the approved credit for case C17",
    "Issue the authorized credit on O17",
    "Execute the approved refund for C18",
    "Read order O18"
  ],
  "oracle": [
    "read_status",
    "read_status",
    "read_status",
    "read_status",
    "read_status",
    "read_status",
    "issue_credit",
    "issue_credit",
    "issue_credit",
    "read_status"
  ],
  "method": "count chosen tool equal to oracle / 10; retain unparseable/abstain separately; repeat only in an isolated new session"
}
```

#### Break, choose, repair, prove

1. **Break:** Test confusing read/write descriptions with a held-out set of requests. Name the exact failed assumption before proposing another component.
2. **Choose:** Record one chosen tool per held-out request, keep abstentions visible and compare with the supplied oracle in an isolated run. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Compare observed routing before/after without promising a fixed improvement rate; inspect conflicting instructions. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.1.md#worked-example-decision-alternative-and-trade-off) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.1 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.1` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "request_count": 10,
  "oracle_read_count": 7,
  "oracle_write_count": 3,
  "observed_choices": null,
  "observed_accuracy": null,
  "reason": "No model routing run performed; compare actual choices with this oracle later"
}
```

**Why this matters:** Count the actual choices. Do not report an improvement before testing it. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [tool search docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Tool use — Anthropic API Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-2-2"></a>
### Worked evidence task — 2.2: test the boundary

**Original technical decision.** A request stream contains an unknown tool, access denial, timeout and successful empty search. Which recovery policy preserves protocol and execution distinctions?

**In everyday terms:** No matches is different from being unable to search.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "results": [
    {
      "jsonrpc_error": "unknown tool"
    },
    {
      "isError": true,
      "cause": "access_denied"
    },
    {
      "isError": true,
      "cause": "timeout"
    },
    {
      "isError": false,
      "matches": []
    }
  ]
}
```

#### Break, choose, repair, prove

1. **Break:** Inject unknown tool name, denied call, timeout and successful empty search. Name the exact failed assumption before proposing another component.
2. **Choose:** Classify each cause first; repair the name, resolve authority, retry only a justified transient failure, and preserve empty success. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Identify protocol versus execution failure; preserve unknown and empty distinctions and recovery evidence. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.2.md#objective-22--return-errors-that-support-the-right-recovery) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.2 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.2` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "classification": [
    "protocol error: unknown tool",
    "execution error: denied",
    "execution error: timeout",
    "success: empty matches"
  ],
  "retry_candidate_indexes": [
    2
  ],
  "empty_is_failure": false
}
```

**Why this matters:** No matches is different from being unable to search. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [MCP Specification — Tool Results](https://modelcontextprotocol.io/docs/concepts/tools) · [MCP Specification — Tools, Error Handling](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#error-handling). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-2-3"></a>
### Worked evidence task — 2.3: test the boundary

**Original technical decision.** A synthesis worker needs merge and source-date verification but also sees refund and delete tools. Which capability boundary reduces unnecessary mutation risk?

**In everyday terms:** Give the worker what it needs for this job, not every available tool.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "role": "synthesis",
  "needs": [
    "merge",
    "verify source date"
  ],
  "unneeded": [
    "issue_credit",
    "delete_record",
    "unrestricted_search"
  ]
}
```

#### Break, choose, repair, prove

1. **Break:** Give a synthesizer unnecessary mutating tools, then a narrow fact-check capability. Name the exact failed assumption before proposing another component.
2. **Choose:** Keep the needed synthesis and checking capabilities; remove unrelated write capabilities from this role. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Justify capability scope and distinguish role overload from ambiguous descriptions. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.3.md#scope) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.3 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.3` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "retain": [
    "merge",
    "verify source date"
  ],
  "remove": [
    "issue_credit",
    "delete_record",
    "unrestricted_search"
  ],
  "role": "synthesis"
}
```

**Why this matters:** Give the worker what it needs for this job, not every available tool. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [define-tools page](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use) · [tool search docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-2-4"></a>
### Worked evidence task — 2.4: test the boundary

**Original technical decision.** Project MCP configuration references a token variable, but the environment is unprovisioned and no resource was read. Which evidence supports a successful integration claim?

**In everyday terms:** A configuration file is a plan to connect. It is not proof of a connection or retrieved content.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "scope": "project",
  "config_file": ".mcp.json",
  "token_variable": "DOCS_TOKEN",
  "token_provisioned": false,
  "server_connected": false,
  "resource_read": false
}
```

#### Break, choose, repair, prove

1. **Break:** Use project-shared server configuration with missing environment provisioning and disconnected content. Name the exact failed assumption before proposing another component.
2. **Choose:** Verify provisioning, connection, discovery and actual resource inclusion separately without embedding secrets. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Separate configuration scope, connection, discovery and actual resource inclusion; no embedded secret. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-2.4.md#config) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.4 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 2.4` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "configuration_scope": "project",
  "secret_value_in_fixture": false,
  "provisioned": false,
  "connected": false,
  "resource_included": false,
  "integration_proven": false
}
```

**Why this matters:** A configuration file is a plan to connect. It is not proof of a connection or retrieved content. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [MCP documentation](https://code.claude.com/docs/en/mcp) · [MCP Server Configuration — Claude Code Documentation](https://code.claude.com/docs/en/mcp). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-3-1"></a>
### Worked evidence task — 3.1: test the boundary

**Original technical decision.** A teammate lacks one developer’s home instructions and project guidance contains opposing naming rules. Which repair addresses distribution without assuming settings override behavior?

**In everyday terms:** Your home file does not travel with the repository to another person.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

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

#### Break, choose, repair, prove

1. **Break:** Place team rules only in one developer home directory and add contradictory project text. Name the exact failed assumption before proposing another component.
2. **Choose:** Put shared guidance in the repository and reconcile conflicting instructions explicitly; inspect settings precedence separately. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Explain missing team distribution and distinguish instruction loading from settings precedence. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.1.md#foundation) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.1 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.1` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

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


<a id="benchmark-exercise-3-2"></a>
### Worked evidence task — 3.2: test the boundary

**Original technical decision.** A reusable release procedure accepts a candidate ID and should execute in an isolated context with Read access. Which artifacts separate procedure, universal rule and actual permission?

**In everyday terms:** A written instruction can request a boundary, but the runtime has to enforce it.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "workflow": "release_check",
  "argument": "candidate_id",
  "universal_rule": "do not expose secrets",
  "isolated_output": true,
  "required_capability": "Read"
}
```

#### Break, choose, repair, prove

1. **Break:** Move a reusable procedure into a skill with an argument and a limited execution context. Name the exact failed assumption before proposing another component.
2. **Choose:** Define the reusable procedure and argument, preserve the universal secret rule, and test isolation and permissions in the actual installed runtime. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Identify actual loading/invocation behavior and verify permission behavior independently of prompt text. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.2.md#foundation) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.2 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.2` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "procedure": "release_check",
  "argument": "candidate_id",
  "universal_rule": "do not expose secrets",
  "requested_capability": "Read",
  "runtime_isolation_verified": false,
  "runtime_permissions_verified": false
}
```

**Why this matters:** A written instruction can request a boundary, but the runtime has to enforce it. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [skills frontmatter reference](https://code.claude.com/docs/en/skills) · [Claude Code skills docs](https://code.claude.com/docs/en/skills). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>


<a id="benchmark-exercise-3-3"></a>
### Worked evidence task — 3.3: test the boundary

**Original technical decision.** A test-only path rule is evaluated in two fresh sessions, one matching and one not. Which experiment avoids attributing cached guidance to new conditional loading?

**In everyday terms:** Start clean so yesterday’s loaded rule cannot confuse today’s test.

**Before you start:** No account, API key or package installation is needed for the paper task. Optional replay needs Python 3 and the two provided lab files in the same directory. This local inspector models the stated fixture; it does not call Claude, load Claude Code rules or run an MCP server.

#### Inspect the supplied input

All identifiers and business rules here are fictional application data. This is **not an SDK request schema**. Keep the input separate from your proposed decision.

```json
{
  "rule_path": "**/*.test.ts",
  "match": "packages/a/x.test.ts",
  "nonmatch": "packages/b/main.ts",
  "sessions": [
    "fresh-A",
    "fresh-B"
  ],
  "no_cross_session_history": true
}
```

#### Break, choose, repair, prove

1. **Break:** Put tests in several packages, then compare a global convention with a path-scoped rule. Name the exact failed assumption before proposing another component.
2. **Choose:** Record the matched path per fresh session and inspect loaded guidance; do not treat path matching as a security boundary. Write the nearest alternative you would reject and the requirement it fails.
3. **Repair:** Write the corrected contract or recovery step, keeping successful evidence and unknowns separate.
4. **Prove:** Use fresh isolated sessions for matching and nonmatching paths, inspect loaded guidance, and record observed loading. Previously loaded guidance is not automatically revoked; conditional loading is not a security boundary. Record `decision`, `reason`, `rejected_alternative`, `evidence` and `remaining_unknowns`.

[Revisit the objective explanation](../../02-Lessons/02-CCAR-F-Architect-Foundations/objectives/objective-3.3.md#foundation) · [Return to the LAB task index](#benchmark-evidence-tasks)

**Optional local replay:** From this LAB folder, first run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.3 --input-only` and write your prediction. Then run `python3 ../08-CCAR-F-architecture-decisions/benchmark_exercises.py --objective 3.3` and compare the fixed-fixture calculations and reference decisions. From a different folder, use the script’s actual path.

<details><summary>Compare the offline evidence — after making your decision</summary>

The local inspector presents **controlled-fixture calculations and authored reference decisions** below. Some fields are calculated (such as counts or arithmetic); policy labels and recovery choices are supplied worked answers for this fixed example, not executed policies or a general-purpose validator. No Claude, rule loader, service or reviewer was run. `false` or `null` observations remain unresolved when no corresponding live test was performed.

```json
{
  "match_path": true,
  "nonmatch_path": false,
  "isolated_sessions": true,
  "actual_guidance_loading_observed": false
}
```

**Why this matters:** Start clean so yesterday’s loaded rule cannot confuse today’s test. The output is a self-check for this controlled example, not certification-score evidence. To test the real mechanism, perform the existing LAB’s integration steps in a fresh disposable context and keep its actual trace beside this prediction.

**Primary-source leads for mechanism review:** [Claude Code Memory and Rules Documentation](https://code.claude.com/docs/en/memory). The external benchmark helped identify the exercise gap; this task and its data were authored here. Current implementation details must be verified against the installed runtime and those primary sources.

</details>