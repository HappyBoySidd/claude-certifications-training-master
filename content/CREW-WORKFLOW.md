# Crew workflow — who does what, and which gates every piece of work passes

This is the operating model for building the four Claude certifications (CCAO-F, CCAR-F, CCDV-F,
CCAR-P) and the learning site. `/crew` reads it. Every item in [BACKLOG.md](BACKLOG.md) runs
through one of the pipelines below.

**Why the work exists** is in [CHARTER.md](CHARTER.md): two intents (Amar passes all four exams;
a site for colleagues), one north star, and the rule that **Amar's own exam prep wins when the two
compete** (charter §3). Decisions are logged in [DECISIONS.md](DECISIONS.md).

**Four rules hold everywhere:**

1. **The author never verifies their own work.** Each gate is held by a different seat from the
   one that wrote the item. There's no "same seat, fresh context" exception.
2. **One exam per run.** Pipelines never merge exams, and no exam ships at a lower depth than the
   others.
3. **Tier 1 first.** Anthropic's own material is the source. The tiers are in
   the reference library (in the study workspace).
4. **Study first.** Work for the exam Amar is studying now goes before work for a later exam
   (charter §3).

## Current operating contract — 22 October 2026

Git Soma publication within the owner-authorized scope uses standing approval (DECISIONS rows 64, 79, 93 and 94): complete independent review, applicable build/privacy/backlog gates and recorded exceptions, then push without asking again and verify the exact live commit. Never force-push. This does not authorize messages to colleagues, use of names, disclosure of private records or unrelated outward actions.

Use the pipeline definitions below rather than copying their count into editor adapters. The latest applicable owner decision overrides earlier timing holds; the backlog records actual completion. Shared source ownership and checkout identity are documented in the source and release contract.

Runtime capabilities are observed, not assumed. Check available tools and filesystem/network permissions in the current session. Use native named seats when available. A separate agent explicitly assigned an allowed seat must read its exact definition and record that adapter and reviewer identity; it is not a native named runtime. If a required definition or independent reviewer is unavailable, record the missing gate and route a bounded handoff; do not count author self-review as independent. Do not reuse September sandbox grants as current permission evidence.

## 1. How the crew is organized

| Group | Seat | Owns | New or reused |
| --- | --- | --- | --- |
| **Decide** | Amar | Outward actions (push, publish, names), exam order, anything irreversible | — |
| | `amar-proxy` | Frame Gate: does this serve the charter's north star and the intent it belongs to? Answers as Amar where the charter or DECISIONS.md is clear | reused |
| | `exec-reviewer` | Approves forks the cpo escalates | reused |
| | `cpo` | Integrates reviews into one plan, sequences the backlog, signs off each release | reused |
| **Plan** | `learning-strategist` | Learner outcomes, track order, what to build next | new |
| | `learning-architect` | Certification design: blueprint → curriculum → lessons → simulations → checks | new |
| **Author** | `claude-associate-specialist` | CCAO-F content (Claude apps, prompting, governance for non-technical roles) | new |
| | `claude-architect-specialist` | CCAR-F and CCAR-P content (agentic architecture, MCP, context, evaluation, governance) | new |
| | `claude-developer-specialist` | CCDV-F content (API, Agent SDK, Claude Code, tools, security) | new |
| | `assessment-designer` | Scenario simulations and our own practice questions | new |
| **Question bank** | `question-scout` | Finds legitimate question sources (official samples, openly licensed or permission-granted sets), checks the licence, sorts each by origin. Never dumps | new |
| | `question-bank-curator` | The intake register, merge, origin labels, duplicates, answer balance; runs G12. Never writes or grades question content | new |
| **Check** | `teaching-coach` | Does it teach? Plain language, worked example, traps, Try it, Done when | new |
| | `content-steward` | Sources and tiers, rights, Claude-only scope, freshness | new |
| | `learner-advocate` | A busy first-time learner's view: can I find my next step in 10 seconds? | new |
| | `sf-quality-analyst` | What "it works" means for the site; test strategy for gates | reused |
| **Design** | `ux-experience-lead` | Learner journeys and observable acceptance criteria for each page type | reused |
| | `information-designer` | Exhibits: the curriculum map, domain weight bars, progress views | reused |
| | `design-system-engineer` | Design tokens, CSS, accessibility, the build script's HTML | reused |
| | `creative-director` | The final design verdict | reused |
| **Ship** | `site-publisher` | Build, preview, commit, push and live checks on Git Soma Pages | reused |
| | `change-manager` | Release notes, version tags, rollback | new |
| | `defect-rca-analyst` | Root cause of any defect, by class, before a fix | reused |
| | `code-review` | Reviews `site/build.py` and `tools/gate.py` changes | reused |

The new seats' definitions are in [`.claude/agents/`](.claude/agents). Specialists author content
for their own exams, and a **different** specialist holds the accuracy gate (G4):

| Exam | Usual author | G4 accuracy check |
| --- | --- | --- |
| CCAO-F | `claude-associate-specialist` | `claude-architect-specialist` |
| CCAR-F | `claude-architect-specialist` | `claude-developer-specialist` |
| CCAR-P | `claude-architect-specialist` | `claude-developer-specialist`, plus `claude-associate-specialist` for the governance, rollout and stakeholder domains |
| CCDV-F | `claude-developer-specialist` | `claude-architect-specialist` |

If someone other than the usual author wrote the item (for example the lead session), the exam's
usual author holds G4. Every dispatch names the mode: **AUTHOR** (write it) or **REVIEW** (check
work you didn't write).

## 2. The gates

| Gate | Held by | Passes when |
| --- | --- | --- |
| **G0 Frame** | `amar-proxy` | The work serves an objective in [CHARTER.md](CHARTER.md) §4 (A1–A4 for Amar, B1–B4 for the site), respects the study-first rule (charter §3), and the backlog item exists. For anything colleagues will read (a site page, release notes, a post), the request that starts the work also includes a **claims inventory**: a list of every page, tool, feature or file the draft will mention, each with its file path, plus the `DECISIONS.md` rows that set its scope. `amar-proxy` opens each path: it must be live on the site, or in the next release's build (the staging copy) with its backlog row in this release. The inventory check (G7 for a post, G10 for release notes) compares the draft with the inventory; any later edit that adds a claim goes back through that check. Anything not on the list is cut, not promised |
| **G1 Blueprint** | `learning-architect`. In P1, `learning-architect` writes the coverage map, so the exam's author specialist holds G1 instead | Every official objective for the exam is covered once, weighted as in the guide, and nothing is outside the blueprint |
| **G2 Sources** | `content-steward` | Every fact cites a source with its tier. Tier 1 is used where it exists; no fact rests on Tier 3 alone |
| **G3 Scope and rights** | `content-steward` | Claude and Anthropic only; no exam questions; no third-party question banks; no colleague names without permission; no secrets |
| **G4 Accuracy** | the G4 seat for the exam (table in §1), never the author | Facts match Tier 1 today; anything uncertain says "check the current docs" |
| **G5 Teaching** | `teaching-coach` | Plain language, the house lesson shape, a worked example, traps, Try it, Done when |
| **G6 Assessment** | `assessment-designer`, or the exam's usual author specialist when the designer wrote the item (always the case in P3) | One best answer, plausible wrong options, each tied to an official objective; not an exam item |
| **G7 Learner** | `learner-advocate` | The next step is obvious, time estimates are realistic, links work |
| **G8 Design** | `information-designer`, then `creative-director` (only `creative-director` when `information-designer` built the exhibit) | Exhibits read in seconds; the verdict is "ship" |
| **G9 Build** | `tools/gate.py`, plus `code-review` for code changes | NFR-01 to NFR-10 pass with zero failures |
| **G10 Release** | `cpo` signs off, `change-manager` writes notes, **the crew pushes once the gates pass** (standing approval from the site owner) | The release notes list what changed and why. Every feature claim and backlog id in them is checked against the release commit itself (the built `docs/` and its diff), never from memory or another branch |
| **G12 Bank integrity** | `question-bank-curator`, running the practice tool (in the study workspace) (never on a batch it normalised itself; then `cpo` runs it) | Every register entry has an origin, licence, author and backlog row; licensed sources carry their attribution; nothing is `approved` until each gate it lists is `pass`; schema, domains and answers are valid; no repeat of an official sample or an existing item; project-authored items say so; answer letters balanced |
| **G11 Live** | `site-publisher` | Every changed page loads on Pages; `defect-rca-analyst` handles anything broken |

## 3. The pipelines

Each pipeline lists its stages in order. A stage in **bold** is a gate.

| Pipeline | Stages | Output |
| --- | --- | --- |
| **P1 Certification design** (once per exam, then on guide changes) | **G0** → learning-architect maps the official blueprint → **G1** → curriculum file (checklist, week plan, book-by bar) → **G2** → **G4** → **G7** → cpo sign-off | `01-Curriculum/<track>/<exam>.md` |
| **P2 Lesson** | learning-architect writes the brief (objectives, weight, practice session, lab) → specialist drafts → **G2** → **G3** → **G4** → **G5** → **G7** → CHANGELOG | `02-Lessons/<exam>/L0N-*.md` |
| **P3 Simulation and assessment** | learning-architect picks the domains and decisions → assessment-designer drafts → **G3** → **G4** → **G6** → **G7** | `04-Simulations/<exam>/SIM-*.md`; our own questions later |
| **P4 Lab** | specialist drafts → a second specialist dry-runs it → **G3** (secrets, laptop note) → **G5** | `06-Labs/NN-*/README.md` |
| **P5 Feedback** | `/harvest` or `/debrief` → content-steward updates INSIGHTS (tier F, or F-relayed for what Anthropic told a colleague) → the exam's specialist checks the tiers and facts → proposed edits → **Amar approves** → P2 or P1 | `11-Lessons-Learned/` |
| **P6 Site design** | ux-experience-lead writes journeys and acceptance criteria → information-designer designs exhibits → design-system-engineer builds the kit → **G8** → **G7** | `site/`, `docs/assets/` |
| **P7 Build and deploy** | content is edited in this Drive project → `python3 site/build.py` → **G9** → local preview → review of changed pages (**G7**, plus **G8** if design changed) → backlog check (`tools/backlog_check.py`, step 5 of `tools/publish.sh`: no `doing` or `blocked` rows) → commit by explicit path (the pre-commit hook reruns G9) → **G10** → push to `master` → **G11** | `docs/` on Git Soma Pages |
| **P8 Defect** | report (a site issue or a note) → `defect-rca-analyst` names the root-cause class → fix through the pipeline that owns the cause → a prevention step (a gate check or a rule) → verified by a different seat | `BACKLOG.md` row, and a gate check where possible |
| **P9 Study feedback** (Amar's results improve the material) | a trigger in your own notes (below) → learning-architect maps the weak domain to the lesson section, practice session or simulation behind it → **G0** (is this for the exam in progress?) → P2 or P3 on just that section | A `BACKLOG.md` row per fix; the changed lesson or simulation |
| **P11 Question bank** (grow the practice bank; one exam per batch) | **G0** → `question-scout` finds and classifies sources, or `learning-architect` names thin domains for new items → **G3** (licence, no dumps, Claude-only) → author writes or adapts the batch (exam specialist or `assessment-designer`, into a `*-draft.json` with `status: draft` in `bank-sources.json`) → **G4** → **G6** → `question-bank-curator` normalises and sets `approved` → **G12** → `build.py` → **G9** → **G7** on the practice tool | New questions in the practice tool (in the study workspace), labelled by origin |
| **P10 Announcement** (Slack posts to colleagues, including one per minor release; the crew only drafts, and Amar posts) | **G0** with the claims inventory → `voice-drafter` drafts → **G2** → **G3** → **G7** (also checks the draft against the inventory) → `creative-director` (does it look and read well?) → `voice-validator` (does it sound like Amar, with clean grammar?) → `cpo` signs off → Amar posts it himself. For a release post, `change-manager`'s G10 release notes are the input; P10 doesn't rewrite them | A draft message in the backlog row; the crew never posts |
| **P12 Study-site revision with content review** (a redesign of a site plus a review of all its content in one run) | **G0** (`amar-proxy`) → plan, in parallel: `information-designer` (layout, stem formatting rules) and `ux-experience-lead` (journeys, acceptance criteria) → content review, in parallel: `learning-architect` (**G1** coverage), `claude-architect-specialist` and `claude-developer-specialist` (**G4**, each only on items the other wrote) → **G8** `creative-director` on the plan → `cpo` integrates every finding into one sequenced plan → `design-system-engineer` builds; content fixes go back to each item's author through P2, P3 or P11 → **G4**/**G6** on changed facts or keys → **G8** recheck → **G7** → **G9** (rebuild plus click test) | The revised site; one review file per seat; a backlog row with every gate round |

**P9 triggers:**

- The same domain scores under 70% in two sessions or mocks in a row.
- A simulation decision is missed and the lesson it cites doesn't teach the correct move.
- Amar notes "the lesson didn't cover this" in the progress log.
- After an exam, the score report's weakest domain (never the questions).

P9 runs only for the exam in progress or just finished (charter §3). A trigger for a later exam
waits as a `todo` backlog row.

## 3a. Hand-offs: what passes between seats

| From | To | What is handed over |
| --- | --- | --- |
| `cpo` | the pipeline's first seat | The backlog row: ID, exam, pipeline, the named author seat and the named G4 seat |
| `learning-architect` | author | A brief: official objectives, domain weight, question count, linked practice session, lab, neighbouring lessons |
| author | first gate | The file path, the backlog row, and "author: `<seat>`" at the top of the dispatch |
| each gate | next gate | The verdict line and the findings list, added to the backlog row |
| any gate | author | `PASS WITH FIXES` or `FAIL` with numbered findings (file, section, problem, fix). See §3b |
| last gate | `cpo` | All verdicts for the item; `cpo` marks it `done` and adds the CHANGELOG entry |
| `cpo` | `change-manager` | The release's done items, for release notes and the proposed tag (G10) |
| `change-manager` | Amar | Release notes and rollback step; release owner verifies G10 and the current operating contract before pushing |
| `site-publisher` | `defect-rca-analyst` | Any page failing the live check (G11), which opens P8 |
| your own notes | `learning-architect` | A P9 trigger |
| `change-manager` | `voice-drafter` | The G10 release notes, for a release post (P10) |
| `cpo` | Amar | The signed-off draft post; Amar sends it (P10) |
| `question-scout` | `content-steward` | The scouting report and the draft register entries (P11, G3) |
| last content gate (G6) | `question-bank-curator` | The passed batch and its gate verdicts, written into its `bank-sources.json` entry |
| `question-bank-curator` | `cpo` | G12 result and new counts per exam and origin; `cpo` marks the row `done` |

**Every dispatch and hand-off carries a contract** (the template is in
`~/.claude/standards/ops/DISPATCH-CONTRACT.md`): mode and seat, goal, inputs, a **definition of
done**, numbered **acceptance criteria** the receiver will test, **guardrails** (scope, no
outward actions, limits), and a return shape (`DONE`, `INCOMPLETE` or `BLOCKED`, with a
pass/fail check per criterion). A seat that can't meet the definition of done returns
`INCOMPLETE`; it never reports partial work as done. Every backlog row states its definition of
done before work starts. Stalled or failed seats follow `~/.claude/standards/ops/AGENT-RESILIENCE.md`.
**Permissions are planned up front:** before dispatching, the lead lists every step that needs
elevation or Amar's OK, bundles them, and asks once at the start (DECISIONS row 46).

## 3b. Fix loop: what happens when a gate doesn't pass

| Verdict | Next step |
| --- | --- |
| `PASS` | Go to the next gate |
| `PASS WITH FIXES` | The **author** fixes the listed items. The **same gate seat** rechecks only those items |
| `FAIL` | The **author** reworks the item. The **same gate seat** rechecks the whole item |

**Rules:**

1. **The gate seat never edits the item it's grading.** It may suggest exact wording in a finding;
   the author applies it.
2. **A fix reopens any earlier gate it touches.** Changed facts go back through G2 and G4. Changed
   scope or names go back through G3. Changed exhibits or CSS go back through G8.
3. **At most 2 fix rounds per gate.** Round 1 is the first recheck; round 2 is the last.
4. **Stop early if it isn't improving.** If round 2 has as many findings as round 1 or more, stop.
5. **Still failing after that:** the backlog row goes to `blocked` with the label
   `[GATE INCOMPLETE — Gn, N findings]`, and it escalates `cpo` → `exec-reviewer` → `amar-proxy`
   → Amar. Each seat settles it if it can; only a genuine cost, scope or outward call reaches Amar.
   The outcome is a row in [DECISIONS.md](DECISIONS.md).
6. **Record every round** in the backlog row's status, for example
   `G4 r1 FAIL (3) → r2 PASS`.
7. **G9 build failures** follow the same loop. A second failure of the same check opens P8, so the
   cause gets fixed, not just the symptom.

## 3c. RASIC: who does what in each pipeline

**R** Responsible (does the work) · **A** Accountable (one seat; signs it off) · **S** Supporting
(helps the R) · **I** Informed (told when it's done) · **C** Consulted (their verdict is needed;
the gate holders).

| Pipeline | R | A | S | I | C (gates) |
| --- | --- | --- | --- | --- | --- |
| P1 Certification design | `learning-architect` | `cpo` | exam author specialist | Amar | `amar-proxy` (G0), exam author specialist (G1), `content-steward` (G2), G4 seat, `learner-advocate` (G7) |
| P2 Lesson | exam author specialist | `cpo` | `learning-architect` (brief) | Amar | `content-steward` (G2, G3), G4 seat, `teaching-coach` (G5), `learner-advocate` (G7) |
| P3 Simulation and assessment | `assessment-designer` | `cpo` | `learning-architect` | Amar | `content-steward` (G3), G4 seat, exam author specialist (G6), `learner-advocate` (G7) |
| P4 Lab | exam author specialist | `cpo` | a second specialist (dry run) | Amar | `content-steward` (G3), `teaching-coach` (G5) |
| P5 Feedback | `content-steward` | Amar (approves each edit) | `learning-architect` | `cpo` | the exam's specialist (checks the INSIGHTS update) |
| P6 Site design | `ux-experience-lead`, `information-designer`, `design-system-engineer` | `cpo` | `sf-quality-analyst` | Amar | `creative-director` (G8), `learner-advocate` (G7) |
| P7 Build and deploy | `site-publisher` | `cpo` (standing push approval from Amar) | `change-manager`, `code-review` | colleagues, through release notes | `tools/gate.py` + `code-review` (G9), `cpo` (G10 sign-off), `learner-advocate` (G7) |
| P8 Defect | `defect-rca-analyst` (cause), then the owning pipeline's R (fix) | `cpo` | `sf-quality-analyst` | Amar | a seat other than the fixer (verification) |
| P9 Study feedback | `learning-architect` | `cpo` | exam author specialist | Amar | `amar-proxy` (G0), then P2 or P3's gates |
| P10 Announcement | `voice-drafter` | `cpo` (signs off the draft) | `change-manager` (hands over the G10 release notes) | Amar (posts it himself) | `amar-proxy` (G0, claims inventory), `content-steward` (G2, G3), `learner-advocate` (G7), `creative-director`, `voice-validator` |
| P11 Question bank | `question-scout` (sources), then the exam author specialist or `assessment-designer` (items) | `cpo` | `question-bank-curator` (intake, merge), `learning-architect` (thin domains) | Amar | `amar-proxy` (G0), `content-steward` (G3), G4 seat, `assessment-designer` or the exam's specialist (G6, never the item's author), `question-bank-curator` (G12), `learner-advocate` (G7) |
| P12 Study-site revision | `design-system-engineer` (build); `information-designer`, `ux-experience-lead` (plan); each item's author (content fixes) | `cpo` | `sf-quality-analyst` (click test) | Amar | `amar-proxy` (G0), `learning-architect` (G1), G4 seats, `assessment-designer` (G6), `creative-director` (G8), `learner-advocate` (G7), `code-review` (G9) |

In P6, `information-designer` builds the exhibits, so it doesn't hold G8 on its own work;
`creative-director` holds G8 alone there.

## 4. How to run it

| Say | What happens |
| --- | --- |
| *"/crew build CCDV-F lessons"* | P2 for each missing lesson, with gates in order; results logged in BACKLOG |
| *"/crew review CCAR-P"* | G1–G7 over every file for that exam; defects go to P8 |
| *"/crew publish"* | P7 end to end, through the push once G10 passes |
| *"Ingest the new transcripts"* | P5 for files in the reference library (in the study workspace) |
| *"/crew study feedback CCAR-F"* | P9: read the exam's progress log, list the triggers, open backlog rows for the fixes |

## 5. Where status lives

- **Practice questions surface only in the practice tool** (the practice tool (in the study workspace)) and the
  generated practice sessions. Each one shows an origin pill (Official, Official course, Community,
  or **Project-authored (written by us)**), each origin can be filtered on or off, and questions we
  wrote are never labelled Official. The intake register is the practice tool (in the study workspace).

- **Why, and what winning looks like:** [CHARTER.md](CHARTER.md).
- **Decisions and who made them:** [DECISIONS.md](DECISIONS.md), append only.
- **Work items:** [BACKLOG.md](BACKLOG.md), one row per item, with the gate it's waiting on and
  the fix round.
- **Plans:** local project plans and operating controls (not published) is the register. Live plans sit in
  local project plans and operating controls (not published) with a phase tracker; a plan whose rows are all done moves to
  local project plans and operating controls (not published) with its evidence in the same session. Only the nine core files
  stay in the project root. local project plans and operating controls (not published) runs before every push.
- **What changed and why:** [CHANGELOG.md](CHANGELOG.md).
- **Exam status:** your private progress tracker (not published). **Scores:** your own notes, which is never
  published.
- **Site releases:** the site repo's `CHANGELOG.md` and version tags.