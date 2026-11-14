#!/usr/bin/env python3
"""Pre-push backlog check. Exits non-zero if the study workspace's BACKLOG.md has work that is
started but not finished, because its content is already in the build and hasn't cleared its gates.

    python3 tools/backlog_check.py --src "<study workspace path>"
    python3 tools/backlog_check.py --src "<path>" --allow B-12,S-06   # Amar-approved exceptions

Fails on any row whose status starts with `doing` or `blocked`; on a `todo` row whose item names
a published page (`*.html`); on a `done` row whose status still says work is pending ("still
needs", "not yet", "awaiting", "waiting on"); and on an owner cell naming a seat that isn't on the
`.project.md` `personas:` list (--manifest; a missing manifest fails, unless it was only the
default `<src>/.project.md`). Warns (does not fail) on a content row (B-) marked `done` with no gate
rounds recorded, such as `G4 r1 PASS`, and on lines in the newest `--changelog` entry that say
"open" or "waiting" without a B- or S- id or a DECISIONS row number.

Fix rows (B63-FX-N, optionally with a letter suffix such as B63-FX-14a) are checked the same way,
plus three stricter rules: an ID cell that mentions FX but isn't a well-formed id (`FX-14`,
`B63-FX-`, `B63 FX-3`) is reported MALFORMED and fails; a `done` FX row must record gate rounds
(`G4 r1 PASS`) or a real evidence pointer (an `FX-14a.md` filename, or `Evidence: <path>`; the bare
word "evidence" does not count), else it fails as UNPROVEN; and every roster id FX-1..FX-N must be
present (--expect-fx, default `B63:16`), else it fails as MISSING. The roster needs the exact parent
id (B63-FX-14); suffixed rows alone (B63-FX-14a, B63-FX-14b) do not satisfy it. A malformed FX row
is reported once as MALFORMED, not also as MISSING. The FX rows found are listed on every run,
before the pass/fail result. No third-party packages.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROW_ID = re.compile(r"^(?:[BS]-\d+|B\d+-FX-\d+[a-z]?)$")
LOOKS_LIKE_ID = re.compile(r"\b[BS]-\d+\b|\bB\d+-FX-\d+[a-z]?\b|\bFX\b|\bB\d+\s*-?\s*FX", re.I)
FX_ID = re.compile(r"^(B\d+)-FX-(\d+)[a-z]?$")
EVIDENCE = re.compile(r"\bFX-\d+[a-z]?\.md\b|\bevidence:\s*\S*[/.]\S*", re.I)
FX_IN_BAD_ID = re.compile(r"\b(B\d+)-FX-(\d+)", re.I)
OPEN = re.compile(r"^(doing|blocked)\b", re.I)
DONE = re.compile(r"^done\b", re.I)
ROUNDS = re.compile(r"\bG\d+\s*r\d", re.I)
PIPE = re.compile(r"(?<!\\)\|")
TODO = re.compile(r"^todo\b", re.I)
PAGE = re.compile(r"\b[\w/-]+\.html\b")


def published_page(text: str) -> str | None:
    """First `*.html` name in text that isn't under a `private/` folder (those never publish)."""
    return next((m.group(0) for m in PAGE.finditer(text) if "private/" not in m.group(0)), None)
PENDING = re.compile(r"\b(still needs?|not yet|awaiting|waiting on)\b", re.I)
SEAT = re.compile(r"^[a-z]+(?:-[a-z]+)*$")
UNTRACKED = re.compile(r"\b(open|waiting)\b(?!\s+(?:source|graph)\b)", re.I)
TRACKED = re.compile(r"\b[BS]-\d+\b|\bB\d+-FX-\d+[a-z]?\b|DECISIONS(?:\.md)?\W+(?:rows?\s+)?\d+")


def cells(line: str) -> list[str]:
    return [c.strip() for c in PIPE.split(line.strip().strip("|"))]


def plain(cell: str) -> str:
    return cell.replace("*", "").replace("`", "").strip()


def rows(text: str):
    """Yield (id, item, status, owner, problem) for every backlog table row.

    Status is found by its header. `problem` is set when a row can't be read reliably, so the
    caller fails closed instead of skipping it.
    """
    status_col = width = owner_col = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            status_col = width = owner_col = None
            continue
        c = cells(line)
        heads = [plain(x) for x in c]
        if "Status" in heads:
            status_col, width = heads.index("Status"), len(c)
            owner_col = next((i for i, h in enumerate(heads) if h.startswith("Owner")), None)
            continue
        first = plain(c[0]) if c else ""
        if not LOOKS_LIKE_ID.search(first):
            continue
        if status_col is None:
            yield first, "", "", "", "no Status header above this row"
        elif not ROW_ID.match(first):
            yield first, "", "", "", "ID cell isn't a well-formed B-N, S-N or B<n>-FX-N[a-z] id"
        elif len(c) != width:
            yield first, c[1] if len(c) > 1 else "", "", "", f"{len(c)} cells, header has {width}"
        else:
            yield first, c[1], c[status_col], c[owner_col] if owner_col is not None else "", None


def owner_seats(owner: str) -> set[str]:
    """Seat names in an owner cell like "Author: lead session. G4: claude-architect-specialist"."""
    owner = re.sub(r"\([^)]*\)", " ", plain(owner))
    # Remove complete concrete path tokens before interpreting '/' as a seat separator.
    # A hyphenated role pair has no filename extension and remains reviewable.
    owner = re.sub(r"\S*/\S*\.[A-Za-z0-9]+(?:#[^\s]*)?", " ", owner)
    names = set()
    # Split prose delimiters first. Only a whole role/role clause is slash-separated;
    # "Codex author/integrator" is prose and must not fabricate an integrator seat.
    for chunk in re.split(r"\.(?=\s|$)|[,;]|\band\b|\bwith\b|\s+when\b.*", owner):
        chunk = re.sub(r"^\s*[\w/ -]*:\s*", "", chunk).strip()
        candidates = chunk.split("/") if re.fullmatch(r"[a-z][a-z-]*(?:/[a-z][a-z-]*)+", chunk) else [chunk]
        for candidate in candidates:
            if SEAT.fullmatch(candidate):
                names.add(candidate)
    return names


def personas(manifest: Path) -> set[str] | None:
    """Every name on the `personas:` list, generic and project seats alike."""
    if not manifest.is_file():
        return None
    m = re.search(r"^personas:\s*\n((?:\s+(?:-.*|#.*)\n)+)", manifest.read_text(encoding="utf-8"), re.M)
    return set(re.findall(r"^\s+-\s*([\w-]+)", m.group(1), re.M)) if m else set()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src", required=True, help="study workspace path (holds BACKLOG.md)")
    ap.add_argument("--manifest", type=Path, help=".project.md with the personas list (default: <src>/.project.md)")
    ap.add_argument("--changelog", type=Path, help="CHANGELOG.md whose newest entry is linted for untracked open items")
    ap.add_argument("--expect-fx", default="B63:16", help="fix-row roster PREFIX:N, requires PREFIX-FX-1..N (empty to skip)")
    ap.add_argument("--allow", default="", help="comma-separated row IDs Amar approved to ship open")
    args = ap.parse_args()

    backlog = Path(args.src) / "BACKLOG.md"
    if not backlog.is_file():
        print(f"backlog check: {backlog} not found")
        return 1
    allow = {a.strip() for a in args.allow.split(",") if a.strip()}

    if args.manifest and not args.manifest.is_file():
        print(f"backlog check: FAIL, manifest {args.manifest} not found, so seats can't be checked")
        return 1
    seats = personas(args.manifest or Path(args.src) / ".project.md")
    failures, allowed, warnings, malformed = [], [], [], []
    count = 0
    fx_found: set[str] = set()
    fx_malformed: set[str] = set()
    for rid, item, status, owner, problem in rows(backlog.read_text(encoding="utf-8")):
        count += 1
        status = plain(status)
        if problem:
            malformed.append((rid, problem))
            if (m := FX_IN_BAD_ID.search(rid)):
                fx_malformed.add(f"{m.group(1).upper()}-FX-{m.group(2)}")  # reported once, not also MISSING
            continue
        if FX_ID.match(rid):
            fx_found.add(rid)
            if DONE.match(status) and not (ROUNDS.search(status) or EVIDENCE.search(status)):
                failures.append((rid, item, "done, but no gate rounds or evidence note recorded (unproven)"))
                continue
        if seats is not None:
            unknown = sorted(owner_seats(owner) - seats)
            if unknown:
                failures.append((rid, item, f"owner names seat(s) not on the .project.md personas list: {', '.join(unknown)}"))
        if OPEN.match(status):
            (allowed if rid in allow else failures).append((rid, item, status))
            continue
        elif TODO.match(status) and (page := published_page(plain(item))):
            (allowed if rid in allow else failures).append((rid, item, f"todo, and names published page {page}"))
            continue
        if DONE.match(status) and PENDING.search(status):
            failures.append((rid, item, f"done, but says \"{PENDING.search(status).group(0)}\": open a new row for the rest"))
        elif rid.startswith("B-") and DONE.match(status) and not ROUNDS.search(status):
            warnings.append((rid, item, status))

    if args.changelog:
        if not args.changelog.is_file():
            print(f"backlog check: FAIL, changelog {args.changelog} not found")
            return 1
        heads = 0
        for n, line in enumerate(args.changelog.read_text(encoding="utf-8").splitlines(), 1):
            heads += line.startswith("## ")
            if heads > 1:
                break
            if heads == 1 and UNTRACKED.search(line) and not TRACKED.search(line):
                print(f"WARN       {args.changelog.name}:{n}  says \"{UNTRACKED.search(line).group(0)}\" with no B-/S- id or DECISIONS row")
    if seats is None:
        print(f"NOTE       no .project.md in {args.src}, so the seat check was skipped")

    if args.expect_fx:
        prefix, _, n = args.expect_fx.partition(":")
        if not n.isdigit() or not prefix:
            print(f"backlog check: FAIL, --expect-fx must look like B63:16, got {args.expect_fx!r}")
            return 1
        for i in range(1, int(n) + 1):
            if f"{prefix}-FX-{i}" not in fx_found and f"{prefix}-FX-{i}" not in fx_malformed:
                failures.append((f"{prefix}-FX-{i}", "", "MISSING: fix row not in BACKLOG.md"))

    for rid, item, status in allowed:
        print(f"ALLOWED    {rid}  {status}  ({item[:60]})")
    for rid, item, status in warnings:
        print(f"WARN       {rid}  done but no gate rounds recorded  ({item[:60]})")
    for rid, item, status in failures:
        label = ("SEAT" if status.startswith("owner names") else "MISSING" if status.startswith("MISSING")
                 else "UNPROVEN" if "(unproven)" in status else "PENDING" if status.startswith("done,") else "OPEN")
        print(f"{label:<10} {rid}  {status}  ({item[:60]})")
    for rid, problem in malformed:
        print(f"MALFORMED  {rid}  {problem}")

    if fx_found:
        print(f"backlog check: FX rows found ({len(fx_found)}): "
              f"{', '.join(sorted(fx_found, key=lambda s: (int(FX_ID.match(s).group(2)), s)))}")
    elif args.expect_fx:
        print("backlog check: FX rows found (0)")
    if count == 0:
        print("backlog check: FAIL, no backlog rows found (is there a Status header?).")
        return 1
    if failures or malformed:
        print(f"backlog check: FAIL, {len(failures)} problem(s) and {len(malformed)} unreadable row(s). "
              "Not ready to push.")
        print("  Finish the gates and mark the rows done, fix unreadable rows, "
              "or pass --allow with Amar's approval.")
        return 1
    print(f"backlog check: PASS, {count} rows read, none open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
