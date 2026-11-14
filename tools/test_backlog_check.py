#!/usr/bin/env python3
"""Fixtures for tools/backlog_check.py fix-row (B63-FX-N) handling.

    python3 tools/test_backlog_check.py
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).with_name("backlog_check.py")
HEAD = "| ID | Item | Owner | Status | Notes |\n| --- | --- | --- | --- | --- |\n"


def row(rid, status="done G4 r1 PASS"):
    return f"| {rid} | item | Author: lead | {status} | n |\n"


def full(skip=None, override=None):
    out = ""
    for i in range(1, 17):
        rid = f"B63-FX-{i}"
        if rid == skip:
            continue
        out += (override or {}).get(rid) or row(rid)
    return out


def run(body, *extra):
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "BACKLOG.md").write_text(HEAD + body, encoding="utf-8")
        p = subprocess.run([sys.executable, str(CHECK), "--src", d, *extra], capture_output=True, text=True)
        return p.returncode, p.stdout


class FxRows(unittest.TestCase):
    def test_full_roster_passes_and_lists_rows(self):
        rc, out = run(full())
        self.assertEqual(rc, 0, out)
        self.assertIn("FX rows found (16)", out)
        self.assertIn("B63-FX-16", out)

    def test_suffix_id_accepted(self):
        rc, out = run(full() + row("B63-FX-14a"))
        self.assertEqual(rc, 0, out)
        self.assertIn("B63-FX-14a", out)

    def test_deleted_row_fails(self):
        rc, out = run(full(skip="B63-FX-7"))
        self.assertEqual(rc, 1, out)
        self.assertIn("MISSING", out)
        self.assertIn("B63-FX-7", out)

    def test_doing_row_fails(self):
        rc, out = run(full(override={"B63-FX-3": row("B63-FX-3", "doing")}))
        self.assertEqual(rc, 1, out)
        self.assertIn("OPEN", out)

    def test_blocked_row_fails(self):
        rc, out = run(full(override={"B63-FX-3": row("B63-FX-3", "blocked")}))
        self.assertEqual(rc, 1, out)

    def test_done_without_proof_fails(self):
        rc, out = run(full(override={"B63-FX-5": row("B63-FX-5", "done")}))
        self.assertEqual(rc, 1, out)
        self.assertIn("UNPROVEN", out)

    def test_done_with_evidence_note_passes(self):
        rc, out = run(full(override={"B63-FX-5": row("B63-FX-5", "done, see implementation/FX-5.md")}))
        self.assertEqual(rc, 0, out)

    def test_done_but_pending_fails(self):
        rc, out = run(full(override={"B63-FX-5": row("B63-FX-5", "done G4 r1 PASS, still needs review")}))
        self.assertEqual(rc, 1, out)

    def test_malformed_ids_reported(self):
        for bad in ("FX-14", "B63-FX-", "B63 FX-3"):
            with self.subTest(bad=bad):
                rc, out = run(full() + row(bad))
                self.assertEqual(rc, 1, out)
                self.assertIn("MALFORMED", out)

    def test_unknown_seat_in_with_and_slash_forms_fails(self):
        for owner in ("Author: site-architect with ghost-seat", "Reviews: ux-experience-lead/ghost-seat", "Reviews: ghost-seat/site-architect with tools/gate.py",
                      "Reviews: site-architect; ghost-seat when facts change"):
            with self.subTest(owner=owner):
                with tempfile.TemporaryDirectory() as d:
                    (Path(d) / "BACKLOG.md").write_text(HEAD + f"| B-1 | item | {owner} | done G4 r1 PASS | n |\n", encoding="utf-8")
                    (Path(d) / "m.md").write_text("personas:\n  - site-architect\n  - ux-experience-lead\n", encoding="utf-8")
                    p = subprocess.run([sys.executable, str(CHECK), "--src", d, "--manifest", str(Path(d) / "m.md"),
                                        "--expect-fx", ""], capture_output=True, text=True)
                    self.assertEqual(p.returncode, 1, p.stdout)
                    self.assertIn("ghost-seat", p.stdout)

    def test_owner_filepaths_and_prose_do_not_fabricate_seats(self):
        for owner in ("G9 tools/gate.py", "G9 `tools/gate.py`",
                      "Review documented in site-audit/reviews/action-plan-review.md",
                      "Codex author/integrator", "site-architect with tools/gate.py"):
            with self.subTest(owner=owner):
                with tempfile.TemporaryDirectory() as d:
                    (Path(d) / "BACKLOG.md").write_text(HEAD + f"| B-1 | item | {owner} | done G4 r1 PASS | n |\n", encoding="utf-8")
                    (Path(d) / "m.md").write_text("personas:\n  - site-architect\n", encoding="utf-8")
                    p = subprocess.run([sys.executable, str(CHECK), "--src", d, "--manifest", str(Path(d) / "m.md"),
                                        "--expect-fx", ""], capture_output=True, text=True)
                    self.assertEqual(p.returncode, 0, p.stdout)

    def test_roster_can_be_skipped(self):
        rc, out = run(row("B-1"), "--expect-fx", "")
        self.assertEqual(rc, 0, out)


if __name__ == "__main__":
    unittest.main()
