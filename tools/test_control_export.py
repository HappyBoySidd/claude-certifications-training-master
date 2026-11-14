"""Regression: local operating controls must not become broken portable-source links."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'site'))
import build
class ControlsExport(unittest.TestCase):
 def test_local_controls_are_plain_text_in_export(self):
  md='See [source and release contract](13-Plans/active/PLAN-02-evidence/folder-fixes-2026-10-22/SOURCE-AND-RELEASE-CONTRACT.md) and [tracker](TRACKER.md).'
  exported=build.scrub(md,'CREW-WORKFLOW.md')
  self.assertNotIn('](13-Plans/',exported);self.assertNotIn('](TRACKER.md)',exported)
  self.assertIn('source and release contract',exported);self.assertIn('tracker',exported)
 def test_public_filter_still_preserves_nonprivate_rows(self):
  md='# Backlog\n| B-11 | PRIVATE-SENTINEL |\n| B-124 | workflow repair |\n'
  public=build.public_rows('BACKLOG.md',md)
  self.assertNotIn('PRIVATE-SENTINEL',public);self.assertIn('| B-124 | workflow repair |',public)
if __name__=='__main__':unittest.main()
