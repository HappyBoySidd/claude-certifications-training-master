# Claude Certifications Study Site

A study site for colleagues preparing for Anthropic's four Claude certifications:

- CCAO-F Associate – Foundations
- CCAR-F Architect – Foundations
- CCDV-F Developer – Foundations
- CCAR-P Architect – Professional

**Open the site:** https://git.soma.salesforce.com/pages/akumthekar/claude-certifications-training/
(Salesforce login required.)

**Taking over this site?** See [`HANDOVER.md`](HANDOVER.md) — it covers setup, build commands, governance and a handover checklist for a new owner. [`MAINTAINING.md`](MAINTAINING.md) covers day-to-day message handling.

## What's on the site

| For each exam | What you get |
| --- | --- |
| **Study plan** | Exam facts from the official guide, domain weights, a week plan, a "before you book" checklist, and ticks that stay in your browser |
| **Lessons** | One per exam domain (29 in total): what to know, a worked example, traps, a Try it and a Done when |
| **Scenario simulations** | Ten decisions each, with a coach key to open when you're done (at least 4 per exam) |
| **Labs** | Five hands-on builds: a Claude Project, an agent loop with subagents, an MCP server with a guardrail hook, API modes (real time, caching, batch), and an eval harness |
| **Insights** | What colleagues who passed said, with names withheld until each person agrees |
| **FAQ, Contribute, What's new** | Quick answers, how to report or suggest things, and every release |
| **Design style guide** | Colours, type, components and writing style, generated from the stylesheet |

The site covers Claude and Anthropic only. It contains **no real exam questions** and no personal
scores, and the site pages carry no third-party question banks. It stores nothing except your theme
and checklist ticks, in your own browser.

**Practice tool:** [`practice/`](practice/README.md) holds a downloadable, offline practice tool with
Anthropic's sample questions and Amey Thakur's MIT-licensed questions. It lives outside `docs/`, so
it is not part of the site pages.

## Where the facts come from

| Tier | What counts | How it's used |
| --- | --- | --- |
| 1 · Anthropic original | Exam guides, Claude docs, Anthropic Academy courses, Anthropic posts and videos | Taught first; always wins |
| 2 · Guides and lessons by others | Study guides, courses, repos and video lessons | Only where Tier 1 is silent, and labelled |
| 3 · Blogs and sites | Articles, posts and practice sites | Never the only source for a fact |
| Field reports | Debriefs from colleagues who passed | Change emphasis, never facts |

## How it's built

The content is written in markdown in the study workspace. This repo holds the generator, the
design kit, the quality gate and the generated `docs/` folder that Git Soma Pages serves.

```
site/build.py          markdown → docs/*.html (own converter, no packages); anonymizes names, drops private links
site/assets/           site.css (tokens, dark mode, print, phones) and site.js (theme, checklists, path planner)
tools/gate.py          quality gate G9: NFR-01 to NFR-10, zero failures required
tools/make_blocklist.py  hashes private colleague names so the gate can block them without storing them
tools/build_practice.py  builds practice/index.html from shareable questions only (licence kept)
tools/publish.sh       build → gate → stage; never pushes
tools/backlog_check.py refuses a push while work in the build is still open
.githooks/pre-commit   reruns the gate and refuses private files
docs/                  the published site (generated; don't edit by hand)
```

### Release workflow (pipeline P7)

1. Edit the content in the study workspace. Each piece passes its own gates first: sources, scope
   and rights, accuracy by a different specialist, teaching, and the learner check.
2. Run `CERT_SRC="<workspace path>" tools/publish.sh`, which builds, runs the gate and stages files
   by explicit path.
3. Preview with `python3 -m http.server -d docs 8000`, and review the changed pages.
4. Add a `CHANGELOG.md` entry, then commit. The pre-commit hook reruns the gate.
5. **Push to `master` only after the owner approves.** Pages serves `docs/` from `master`.
6. Check the live pages. Anything broken becomes a defect with a root cause and a prevention step.

Setup once after cloning: `git config core.hooksPath .githooks`

### Quality gate

| ID | Requirement | Checked by |
| --- | --- | --- |
| NFR-01 | Accessible: one h1, a lang attribute, alt text, labelled SVGs, colour contrast of 4.5:1 or more | `gate.py` |
| NFR-02 | Each page under 200 KB | `gate.py` |
| NFR-03 | No outside scripts, styles, fonts or images | `gate.py` |
| NFR-04 | No cookies, tracking or network calls | `gate.py` |
| NFR-05 | Content rights and scope: no colleague names, Slack links, internal hosts or off-scope products; no question-bank text | `gate.py`, `build.py` |
| NFR-06 | Exam pages reviewed in the last 60 days | `gate.py` |
| NFR-07 | Works on phones | viewport check, plus a manual phone check before each release |
| NFR-08 | No broken internal links or anchors | `gate.py` |
| NFR-09 | No secrets | `gate.py` |
| NFR-10 | Prints cleanly | `gate.py` (print stylesheet) |

## Found a problem, or want to help?

- **Report a problem:** use the link at the bottom of any page, or **Issues → New issue → Report a
  problem**.
- **Suggest content** or **share an exam debrief:** the other two issue forms.
- Details, and why there are no pull requests, are in [`CONTRIBUTING.md`](CONTRIBUTING.md) and on
  the site's **Contribute** page. Quick answers are on the **FAQ** page.

## Versions and announcements

- Every release is in [`CHANGELOG.md`](CHANGELOG.md), which is also the site's **What's new**
  page. The home page shows the latest update.
- Each release has an annotated git tag (`v0.3`, `v0.4`, …). A minor release adds pages or
  exercises, or changes a fact or a correct answer; a patch (`v0.4.1`) only fixes things.
- Minor releases are announced in the study cohort's Slack channel. Patches aren't announced.
- Roll back with `git revert` on the release commit. Never force-push.

Not affiliated with or endorsed by Anthropic. The official exam guides always win.
