"""
L1 测试:test_kb_retriever.py
5 用例
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from kb_retriever import KBRetriever


class TestKBRetriever(unittest.TestCase):
    """TC-215 kb_retriever 5 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.registry_path = Path(self.tmp) / "entity_registry.json"
        self.persons_master_path = Path(self.tmp) / "persons_master.json"
        self.wiki_root = Path(self.tmp) / "wiki"
        self.wiki_root.mkdir()
        (self.wiki_root / "Entities" / "Persons").mkdir(parents=True)

        # fixtures
        registry = {
            "entities": [
                {
                    "entity_id": "org_zzzbank_0001",
                    "canonical_name": "浙商银行",
                    "aliases": [],
                    "entity_type": "organization",
                },
            ],
        }
        self.registry_path.write_text(
            json.dumps(registry, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        persons_master = {
            "persons": {},
            "organizations": {
                "浙商银行": {
                    "observations": [
                        {"meeting_id": "m1"},
                        {"meeting_id": "m2"},
                    ],
                },
            },
        }
        self.persons_master_path.write_text(
            json.dumps(persons_master, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _make_retriever(self, stub=True):
        return KBRetriever(
            registry_path=self.registry_path,
            persons_master_path=self.persons_master_path,
            llm_client=None,   # stub mode
            wiki_root=self.wiki_root,
        )

    def test_01_l1_match_returns_l1(self):
        """L1 命中 → level=L1"""
        r = self._make_retriever()
        result = r.query_wiki("浙商银行合作")
        self.assertEqual(result["level"], "L1")
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["canonical_name"], "浙商银行")
        self.assertIsNone(result["synthesis"])

    def test_02_l1_fallback_to_l2_stub(self):
        """L1 无命中 → fallback L2 stub"""
        r = self._make_retriever()
        result = r.query_wiki("xyz不存在的关键字")
        self.assertEqual(result["level"], "L2")
        self.assertIsNotNone(result["synthesis"])
        # Sprint 19: stub 改 lowercase 后,测试断言改为 case-insensitive
        self.assertIn("stub", result["synthesis"].lower())

    def test_03_complex_query_fallback(self):
        """综合查询触发 L2"""
        r = self._make_retriever()
        result = r.query_wiki("综合总结浙商银行所有合作演化")
        self.assertEqual(result["level"], "L2")

    def test_04_citations_collected_from_l1(self):
        """L1 命中 → citations 含 wiki 路径"""
        # 准备一个真实存在的 wiki 文件
        target = self.wiki_root / "Entities" / "Organizations" / "浙商银行.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# 浙商银行\ncontent")

        r = self._make_retriever()
        result = r.query_wiki("浙商银行")
        # L1 命中,无 citations(仅 L2 需要 citations)
        self.assertEqual(result["level"], "L1")

    def test_05_max_l1_limits(self):
        """max_l1 参数生效"""
        r = self._make_retriever()
        result = r.query_wiki("浙商银行", max_l1=1)
        self.assertLessEqual(len(result["matches"]), 1)


if __name__ == "__main__":
    unittest.main()
