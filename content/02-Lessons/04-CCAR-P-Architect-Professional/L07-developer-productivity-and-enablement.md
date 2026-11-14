# CCAR-P Lesson 7 — Developer Productivity and Enablement (7%, about 4 questions)

**Time:** 60 min plus lab 03 · **Practice:** [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)
**Already covered:** the CLAUDE.md hierarchy, commands, skills, plan mode and `-p` in CI are in
[CCAR-F L03](../02-CCAR-F-Architect-Foundations/L03-claude-code-configuration-and-workflows.md).
Small domain: learn the team-level decisions and don't overspend here.

## 7.0 The big idea

The goal is to make Claude Code behave the same way for every engineer on the team. Put shared settings, commands and guardrails in the repo, and use headless mode to bring Claude into CI.

## 7.1 Configuring Claude tools and environments for teams

The Professional question is **"how do I make this the same for fifty engineers?"** Answer: shared,
versioned configuration in the repo, plus organization policy on top.

| File | Scope | Commit it? |
| --- | --- | --- |
| `CLAUDE.md` (root or `.claude/`) | Project standards, always loaded | **Yes** |
| `.claude/settings.json` | Shared project settings: permissions, hooks, environment | **Yes** |
| `.claude/settings.local.json` | One person's overrides | **No** (keep it out of git) |
| `~/.claude/settings.json` | User settings across all projects | No, personal |
| Managed (enterprise) policy settings | Set by IT or admins at system level; users can't override | Deployed by admins, not the repo |
| `.mcp.json` (project root) | Project MCP servers shared with the team | **Yes**, with secrets as environment variables |

- **Precedence:** managed policy wins over everything; more specific project settings override user
  settings. Check the settings page for the exact order.
- **Permissions:** `allow`, `ask` and `deny` rules on tools and commands (for example allow
  `Bash(npm run test:*)`, deny reading `.env`). **Deny wins**, so put the non-negotiables in `deny`,
  ideally in managed settings where no one can loosen them.
- **MCP secrets:** reference `${API_TOKEN}`-style environment variables in `.mcp.json`; never commit
  the token itself. Team members approve project MCP servers before they run.
- **Least privilege applies to developer tools too:** give Claude Code the tools and MCP servers the
  task needs, not every server in the company.

## 7.2 Improving developer workflows

Each tool here saves engineers time in a different way; the team pattern is how you roll it out to everyone:

| Tool | What it's for | Team pattern |
| --- | --- | --- |
| **Custom slash commands** (`.claude/commands/`) | A repeatable prompt, like `/review` or `/release-notes` | Commit them so everyone runs the same review |
| **Skills** (`.claude/skills/<name>/SKILL.md`) | A procedure plus files, loaded on demand | Package "how we write migrations" once |
| **Hooks** (in settings) | Deterministic actions at lifecycle events | `PreToolUse` blocks risky commands; `PostToolUse` runs the formatter or linter after edits |
| **Subagents** | Isolate verbose or specialized work | A test-writer or explorer that returns a summary |
| **Headless mode** (`claude -p`) | Non-interactive runs in CI | PR review with `--output-format json`, posted as comments |

- **Hooks vs prompts:** if it must happen every time (format, block, log), use a hook. If it needs
  judgment, use a prompt, command or skill.
- **Onboarding path:** clone the repo and the shared CLAUDE.md, settings, commands, skills and MCP
  config all arrive together. That's the enablement win.
- **Measure adoption and effect** (cycle time, review turnaround, escaped defects) rather than
  counting prompts.

## 7.3 Supporting debugging and operational issue resolution

- **Give Claude the evidence:** stack trace, failing test, recent diff, relevant logs. A focused
  context beats "it's broken."
- **Reproduce first, then fix:** have Claude write a failing test that shows the bug, then fix it
  and keep the test.
- **Read-only first in production:** investigation tools (logs, metrics, traces through MCP) with
  read access; changes go through the normal pipeline and approvals.
- **Runbooks as commands or skills:** turn "how we triage a latency alert" into a shared skill so
  on-call engineers follow the same steps.
- **When Claude Code misbehaves for one person:** check which memory and settings files are loaded
  (`/memory`), whether an instruction lives in *user* instead of *project* scope, and whether local
  settings override the shared ones.

## Worked example

A platform team of 40 engineers wants consistent Claude Code use. Today every engineer has a
personal setup, one person committed an API token in an MCP config, and CI reviews hang. **Response:**
commit a root CLAUDE.md, `.claude/settings.json` with `deny` rules for secrets files and destructive
commands, shared `/review` and `/triage` commands, and a `PostToolUse` formatter hook. Move MCP servers
to `.mcp.json` with environment-variable secrets, rotate the leaked token, and have IT push managed
settings with the organization-wide deny list. In CI, run `claude -p` with JSON output.

## Traps

- Team standards in `~/.claude/` instead of the repo.
- A token pasted into `.mcp.json`.
- Relying on "please don't run `rm -rf`" in CLAUDE.md instead of a `deny` rule or hook.
- Giving the production agent write access "to fix things faster."
- A CI job without `-p`.

## Try it (45 min): lab 03

In [lab 03](../../06-Labs/03-CCAR-F-mcp-server-claude-code/README.md), commit a
`.claude/settings.json` with one `allow` and one `deny` rule, a `.mcp.json` that reads its token from
an environment variable, one shared slash command, and a `PostToolUse` hook that runs a formatter.
Clone the repo into a second folder and confirm everything works there without extra setup.

## Done when

- [ ] You can say which config file to commit, which to keep local and which admins manage
- [ ] You can explain deny-wins and where to put non-negotiable rules
- [ ] You can choose between a hook, a command and a skill for a given need
- [ ] You can describe a safe AI-assisted debugging flow for production
- [ ] You scored 80% or more on [Lesson 7 practice set](https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/practice/index.html)

**Next:** [CCAR-P simulations](../../04-Simulations/04-CCAR-P-Architect-Professional/README.md)

Source: official exam guide v1.0, Domain 7 objectives;
https://docs.claude.com/en/docs/claude-code/settings;
https://docs.claude.com/en/docs/claude-code/iam;
https://docs.claude.com/en/docs/claude-code/hooks;
https://docs.claude.com/en/docs/claude-code/mcp;
https://docs.claude.com/en/docs/claude-code/slash-commands;
https://docs.claude.com/en/docs/claude-code/skills;
https://docs.claude.com/en/docs/claude-code/sdk/sdk-headless.