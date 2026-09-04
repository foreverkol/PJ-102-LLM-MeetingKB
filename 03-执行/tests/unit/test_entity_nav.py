"""
L1 测试:test_entity_nav.py
5 用例
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from entity_nav import EntityNav


class TestEntityNav(unittest.TestCase):
    """TC-214 entity_nav 5 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.registry_path = Path(self.tmp) / "entity_registry.json"
        self.persons_master_path = Path(self.tmp) / "persons_master.json"

        # 准备 fixtures
        registry = {
            "version": "1.0",
            "entities": [
                {
                    "entity_id": "org_zzzbank_0001",
                    "canonical_name": "浙商银行",
                    "aliases": ["浙商"],
                    "entity_type": "organization",
                    "status_stage": "compiled",
                    "first_seen_at": "2026-08-01T10:00:00",
                    "last_seen_at": "2026-08-05T14:30:00",
                },
                {
                    "entity_id": "person_xxperson_0001",
                    "canonical_name": "陈凌昌",
                    "aliases": ["陈总", "台州陈凌昌"],
                    "entity_type": "person",
                    "status_stage": "compiled",
                    "first_seen_at": "2026-08-02T11:00:00",
                    "last_seen_at": "2026-08-03T09:15:00",
                },
                {
                    "entity_id": "org_weizhong_0001",
                    "canonical_name": "微众银行",
                    "aliases": ["微众"],
                    "entity_type": "organization",
                    "status_stage": "compiled",
                },
            ],
        }
        self.registry_path.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        persons_master = {
            "persons": {
                "陈凌昌": {
                    "name": "陈凌昌",
                    "primary_role": "渠道方",
                    "primary_org": "票圈",
                    "observations": [
                        {"meeting_id": "m1", "role": "渠道方",
                         "org": "票圈", "relation_to_wang": "渠道"},
                        {"meeting_id": "m2", "role": "渠道方",
                         "org": "票圈", "relation_to_wang": "渠道"},
                    ],
                },
            },
            "organizations": {
                "浙商银行": {
                    "name": "浙商银行",
                    "observations": [
                        {"meeting_id": "m3"},
                        {"meeting_id": "m4"},
                        {"meeting_id": "m5"},
                    ],
                },
            },
        }
        self.persons_master_path.write_text(
            json.dumps(persons_master, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.nav = EntityNav(self.registry_path, self.persons_master_path)

    def test_01_org_name_match(self):
        """org 关键字匹配"""
        result = self.nav.nav("我与浙商银行上次聊到什么程度")
        self.assertEqual(len(result["matches"]), 1)
        m = result["matches"][0]
        self.assertEqual(m["canonical_name"], "浙商银行")
        self.assertEqual(m["entity_id"], "org_zzzbank_0001")
        self.assertEqual(m["type"], "organization")
        self.assertEqual(m["occurrences"], 3)

    def test_02_person_title_match(self):
        """X总 匹配 person"""
        result = self.nav.nav("陈总上次说什么了")
        self.assertGreater(len(result["matches"]), 0)
        names = [m["canonical_name"] for m in result["matches"]]
        self.assertIn("陈凌昌", names)

    def test_03_alias_lookup(self):
        """别名反查"""
        result = self.nav.nav("微众银行合作进展")
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["canonical_name"], "微众银行")

    def test_04_complex_query_fallback(self):
        """综合类查询触发 L2 fallback"""
        result = self.nav.nav("综合总结所有银行合作演化")
        self.assertTrue(result["fallback_to_llm"])

    def test_05_no_match_fallback(self):
        """无匹配 → fallback"""
        result = self.nav.nav("xyz不存在的关键字")
        self.assertEqual(len(result["matches"]), 0)
        self.assertTrue(result["fallback_to_llm"])


if __name__ == "__main__":
    unittest.main()
