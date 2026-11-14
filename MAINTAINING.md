# Maintaining the Claude certifications study site

A guide for the site owner on handling messages, running the weekly routine, and releasing updates. Read `HANDOVER.md` first for setup and governance.

---

## The one habit

**Don't fix anything yourself in a direct reply. Log it first.**

Open a Git Soma issue (or open a `BACKLOG.md` row) for anything that changes the site. That way status lives in one place and nothing gets lost.

---

## Quick table — what kind of message is it?

| They say… | Kind | What to do | How fast |
|---|---|---|---|
| "Your site shows my name / a Slack link / something private" | Privacy | Fix first as a patch; add a gate rule so it can't come back | Same day |
| "This page is broken / link is dead / typo" | Defect | Open a backlog S- row; fix in the next patch | That week |
| "This fact is wrong" | Wrong fact | Open a backlog row; the exam's specialist checks it against Anthropic's own docs | 1–2 weeks |
| "This page is confusing" | Enhancement | Open a backlog row; learner-advocate reviews it | Next minor release |
| "Can you add X?" | Content request | Open a backlog B- row; decide against the charter (exam prep comes first) | Next minor or parked |
| "I passed! Here's what helped" | Debrief | The issue is the record; add the lesson to `content/11-Lessons-Learned/INSIGHTS.md` (anonymized, no scores) | Next harvest |
| "Can I help / edit / send a PR?" | Contributor | Yes, through issues; ideas come in as issues, edits go in `content/`, never `docs/` | Reply same week |
| "Can you share real exam questions?" | Out of scope | Polite no | Reply once |
| "What about other vendor products or credential programs?" | Out of scope | Polite no, Claude only | Reply once |
| "Where do I start / how do I book?" | Exam question | Point to the site page; no backlog row | Reply once |
| "I can't open the site" | Access | Salesforce Git Soma login required | Reply once |
| "Can I share my question bank / notes?" | Third-party content | Only if they own it and say it may be published, or its licence allows it | Reply once |

---

## The answers, with a reply you can send

### 1. Something private is showing (a name, a Slack link, a workspace path)

This jumps the queue. Fix it as a patch release the same day. After fixing, add a new check to `tools/gate.py` so it can't come back.

> *"Thanks for catching that. It's fixed now; the site refreshes in a few minutes."*

### 2. A broken page, dead link or typo

Open a backlog S- row, fix it, ship a patch. No announcement; it appears on the "What's new" page.

> *"Thanks! Logged it; it'll be fixed in the next update."*

### 3. "This fact is wrong"

Don't agree or disagree until a specialist checks it against Anthropic's own docs (Tier 1). Anthropic's docs and exam guides win every conflict, even over a colleague who passed the exam.

> *"Thanks. I'll check it against Anthropic's docs and fix it if it's out of date. Do you have the link you're going by?"*

### 4. "Can you add…" / "It would be nice if…"

Open a backlog row. Decide when using the charter: exam prep comes first. It's fine to say "later".

> *"Good idea. It's on the list. There may be a few weeks' wait while other work is in progress."*

### 5. "I passed, here are my tips"

Great. The issue itself is the record. Add the lessons (anonymized, no scores, no actual questions) to `content/11-Lessons-Learned/INSIGHTS.md` in the repo. On the site, everyone stays anonymous by default (DECISIONS row 14). Ask whether they'd like to be credited by name later.

> *"Congrats, and thank you! Mind if I add your tips (anonymously) to the insights page? Never any actual exam questions, just topics and prep advice."*

If they include actual exam questions, do not copy them anywhere. Keep only the topics and general themes.

### 6. "Can I contribute / edit / send a pull request?"

Yes, through issues or messages. If someone sends a pull request, treat it as a proposal: copy the idea into `content/` (the page sources), close the PR with thanks, and credit the person if they agree.

> *"Yes please! Open an issue on the repo (or message me what you'd change) and I'll fold it in. Edits go in content/ (the page sources), never in docs/ (generated) — but ideas are very welcome."*

### 7. "Can I share my question bank / notes / course?"

Only if they own it and say it may be published, or its licence allows it (for example MIT). Until then it stays private (DECISIONS row 17).

> *"Thanks! Can I publish it on the site with your name and a link? If yes, I'll add it in a later batch."*

### 8. "Do you have the real exam questions?"

Never. The exams come with a confidentiality agreement. Everything on the site is original practice material written from Anthropic's public exam guides.

> *"No, sorry. Everything on the site is our own practice material written from Anthropic's public exam guides."*

### 9. Questions about other Salesforce products or certification programs

Out of scope. The site covers Anthropic's Claude certifications only.
Never Salesforce Agentforce, Einstein, Data Cloud or Salesforce certifications.

> *"This site only covers Anthropic's Claude certifications, so I'm not the right source for that one."*

### 10. "Where do I start / how do I book / is it free?"

Answer with a link, no backlog row needed. The home page has a three-path chooser. Each exam page has a "Before you book" list. Price varies at checkout; get reimbursement approval before paying.

> *"The home page has a 'where to start' chooser, and each exam page has a 'before you book' list."*

### 11. "I can't open the site"

The site requires a Salesforce Git Soma login. It is visible to Salesforce employees signed in to Git Soma with SSO (DECISIONS row 18).

> *"Sign in at git.soma.salesforce.com first, then open the link again."*

---

## How changes go out

- **Patch (e.g. v0.4.1):** fixes only. No announcement. Shows on the "What's new" page.
- **Minor (e.g. v0.5):** new pages, exercises, or a changed fact or correct answer. One Slack post in the study cohort channel. The crew drafts it; the site owner sends it (DECISIONS row 22).
- **Every push** waits for the gates and a clean backlog check (gate G10). The site owner gave standing approval to push once they pass.
- **Something broke after a release?** Use `git revert` on the release commit and push. Never force-push.
- **Tell the person** when their thing ships: reply in their thread with the version number. If they agreed to be credited, add their name to the release notes.

---

## What to do with an issue

1. Add a label: `defect`, `enhancement`, or `debrief`.
2. Reply briefly to acknowledge it.
3. If it's accepted, open a `content/BACKLOG.md` row. Put the issue number in the row.
4. Comment on the issue with the backlog ID (e.g. "Logged as S-42").
5. Close the issue when its backlog row reaches `done` and the change is live. Link the release.

The issue is intake. `BACKLOG.md` is the only status list. Do not track status in two places.

---

## Where things live

| What | Where |
|---|---|
| Every open item and its status | `content/BACKLOG.md` — the only status list |
| Why something was decided | `content/DECISIONS.md` — append only |
| What changed on the site, for colleagues | `CHANGELOG.md` and the "What's new" page |
| Incoming requests from colleagues | Git Soma issues on the repo |
| Exam debriefs from colleagues | `content/11-Lessons-Learned/INSIGHTS.md` (not the backlog) |

---

## Hard rules (never break these)

- **Claude and Anthropic only.** Never Salesforce Agentforce, Einstein, Data Cloud or Salesforce certifications.
- **No real exam questions**, ever. The exams come with a confidentiality agreement.
- **Colleague names stay anonymous** unless each person gives explicit permission (DECISIONS row 14). Write "a colleague" until they agree.
- **No Slack links or channel IDs** on any published page.
- **Personal study files never enter the repo.** The pre-commit hook enforces this. Do not unstage it.
- **Third-party question banks do not go on site pages.** They can live in `practice/` outside `docs/` if licenced.
- **Never force-push.** Rollback = `git revert`.

## Diagram release checks

A page-opening review does not verify the diagrams below it. For viewer or diagram changes, inventory every `pre.mermaid` instance in the built HTML, including copies inside closed disclosures, and separately inventory static SVG maps/previews. Record the page and instance index so the completion denominator is inspectable.

Run `node tools/diagram_controller_check.cjs` from the repository root for controller regressions. This uses synthetic geometry and does not replace browser checks. In the browser, check every instance at desktop and phone widths: readable initial framing, starting node, contained scrolling, zoom in/out, whole-diagram overview, Reset, larger view and text alternative. Open hidden diagrams before testing them. Check keyboard panning and focus return, resize a larger view, and inspect actual screenshots. An overview that shrinks labels is not evidence of reading legibility. Preserve source labels, arrows and assessment/progress data.

Viewer and site stylesheet links carry content hashes. After publication, verify the exact Pages commit and a refreshed live diagram; currently open pages need a reload to use updated assets. Save the inventory, per-instance results, visual review and release evidence in the canonical project.
