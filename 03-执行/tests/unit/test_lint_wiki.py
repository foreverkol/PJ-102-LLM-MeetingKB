"""
L1 测试:test_lint_wiki.py
v3.0 lint_wiki.py 7 维 + v7.0 §8.1 必填字段检查
10 个测试用例(精简关键路径)
"""

import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from lint_wiki import lint_wiki, REQUIRED_FIELDS, _extract_wikilinks, _parse_frontmatter


class TestLintWiki(unittest.TestCase):
    """TC-210 lint_wiki 10 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.wiki = Path(self.tmp) / "wiki"
        self.wiki.mkdir()

    def _write(self, name, content):
        p = self.wiki / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def test_01_all_8_keys(self):
        """8 个维度全报告"""
        report = lint_wiki(self.wiki)
        for k in ["1_orphan_pages","2_dead_links","3_missing_sources",
                  "4_contradiction_pending","5_stale_pages",
                  "6_unindexed","7_emoji_garbled",
                  "8_required_field_violations"]:
            self.assertIn(k, report)

    def test_02_orphan_detected(self):
        """维度 1:无 inbound link"""
        self._write("lonely.md", "---\ntype: person\nsource_ref: x\n---\n# Lonely")
        r = lint_wiki(self.wiki)
        self.assertGreater(len(r["1_orphan_pages"]), 0)

    def test_03_dead_link_detected(self):
        """维度 2:链接不存在的页面"""
        self._write("a.md", "---\ntype: meeting\nsource_ref: x\n---\n# A links [[ghost]]")
        r = lint_wiki(self.wiki)
        self.assertGreater(len(r["2_dead_links"]), 0)

    def test_04_missing_sources(self):
        """维度 3:缺 source_ref"""
        self._write("x.md", "---\ntype: meeting\n---\n# X")
        r = lint_wiki(self.wiki)
        self.assertGreater(len(r["3_missing_sources"]), 0)

    def test_05_contradiction_pending(self):
        """维度 4:Status: Disputed 待验证"""
        self._write("d.md",
                    "---\ntype: meeting\nsource_ref: x\n---\n# D\n"
                    "<!-- Status: Disputed -->\nDetails")
        r = lint_wiki(self.wiki)
        self.assertGreater(len(r["4_contradiction_pending"]), 0)

    def test_06_unindexed(self):
        """维度 6:无 index.md 全部 unindexed"""
        self._write("page.md", "---\ntype: meeting\nsource_ref: x\n---\n# P")
        r = lint_wiki(self.wiki)
        self.assertGreater(len(r["6_unindexed"]), 0)

    def test_07_required_fields_meeting(self):
        """v7.0 §8.1 meeting 5 字段必填"""
        # 缺 ldamc → 必触发
        self._write("m.md", """---
type: meeting
date: 2026-08-02
title: 测试
source_ref: RAW/x.md
subtype: partner_coordination
publishability: internal
reusable_for: []
---
# Meeting
""")
        r = lint_wiki(self.wiki)
        # ldamc 缺失 → 必报
        violations = r["8_required_field_violations"]
        self.assertGreater(len(violations), 0)
        self.assertTrue(any("ldamc" in v for v in violations))

    def test_08_required_fields_person(self):
        """v7.0 §8.1 person 5 隐性知识字段"""
        self._write("p.md", """---
type: person
name: 张三
entity_id: person_test_0001
source_ref: RAW/x.md
---
# Person
""")
        r = lint_wiki(self.wiki)
        violations = r["8_required_field_violations"]
        # 缺 thinking_framework / values_beliefs / decision_style / emotional_tone
        self.assertGreater(len(violations), 0)
        msg = " ".join(violations)
        self.assertIn("thinking_framework", msg)
        self.assertIn("values_beliefs", msg)
        self.assertIn("decision_style", msg)
        self.assertIn("emotional_tone", msg)

    def test_09_required_fields_judgment(self):
        """v7.0 §8.1 judgment 3 字段"""
        self._write("j.md", """---
type: judgment
date: 2026-08-02
source_ref: RAW/x.md
---
# J
""")
        r = lint_wiki(self.wiki)
        violations = r["8_required_field_violations"]
        self.assertGreater(len(violations), 0)
        msg = " ".join(violations)
        self.assertIn("topic_key", msg)
        self.assertIn("evidence_chain", msg)
        self.assertIn("confidence_rationale", msg)

    def test_10_required_fields_complete(self):
        """v7.0 §8.1 完整字段 → 0 violations"""
        self._write("perfect.md", """---
type: meeting
date: 2026-08-02
title: 测试
source_ref: RAW/x.md
subtype: partner_coordination
publishability: internal
reusable_for: [decision_reference]
ldamc:
  lost: '-'
  different: '-'
  added: '-'
  more: '-'
  connected: []
---
# M
""")
        self._write("index.md", "# Index\n- [[perfect]]\n")
        r = lint_wiki(self.wiki)
        # meeting 字段完整,无 violation
        meeting_violations = [
            v for v in r["8_required_field_violations"]
            if "[meeting]" in v
        ]
        self.assertEqual(len(meeting_violations), 0)
        # orphan = 0(因为 [[perfect]] 链回)
        # 注意:[[perfect]] 链向自己不算 inbound,所以 orphan 可能 1
        # 主要看必填字段


if __name__ == "__main__":
    unittest.main()
