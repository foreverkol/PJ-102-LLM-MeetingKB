"""
L1 测试:tests/unit/test_entity_resolver.py
v7.0 FR-v7.0-003 entity_id + FR-v7.0-004 canonical_name/aliases + §8.3 消歧
8 用例,覆盖率覆盖核心方法
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from entity_resolver import EntityResolver


class TestEntityResolver(unittest.TestCase):
    """TC-208 entity_resolver 8 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.registry = Path(self.tmp) / "entity_registry.json"

    def test_01_new_entity_creates_id(self):
        """新 entity → 创建 + entity_id 格式"""
        r = EntityResolver(self.registry)
        result = r.resolve_or_create("person", "黄国华", aliases=["慧穗黄总"])
        self.assertEqual(result["action"], "create")
        self.assertTrue(result["entity_id"].startswith("person_"))
        # entity_id 格式:person_{hash8}_{seq4}
        parts = result["entity_id"].split("_")
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[2]), 4)  # 4 位序号
        self.assertEqual(result["canonical_name"], "黄国华")
        self.assertEqual(result["aliases"], ["慧穗黄总"])

    def test_02_same_canonical_returns_same_id(self):
        """§8.3 同 canonical → 同 entity_id"""
        r1 = EntityResolver(self.registry)
        first = r1.resolve_or_create("person", "黄国华")
        r1.save()

        r2 = EntityResolver(self.registry)
        second = r2.resolve_or_create("person", "黄国华")
        self.assertEqual(first["entity_id"], second["entity_id"])
        self.assertEqual(second["action"], "update")

    def test_03_aliases_merge(self):
        """aliases 合并不覆盖"""
        r = EntityResolver(self.registry)
        first = r.resolve_or_create("person", "陈凌昌", aliases=["陈总"])
        r.save()

        r2 = EntityResolver(self.registry)
        second = r2.resolve_or_create("person", "陈凌昌", aliases=["台州陈凌昌", "陈总"])
        self.assertIn("台州陈凌昌", second["aliases"])
        self.assertIn("陈总", second["aliases"])

    def test_04_seq_increments(self):
        """seq 自增"""
        r = EntityResolver(self.registry)
        a = r.resolve_or_create("person", "陈凌昌")
        b = r.resolve_or_create("person", "郭小艳")
        c = r.resolve_or_create("person", "吴英杰")
        # 不同 person → 不同 entity_id
        ids = {a["entity_id"], b["entity_id"], c["entity_id"]}
        self.assertEqual(len(ids), 3)

    def test_05_organization_type(self):
        """organization 用 org_ 前缀"""
        r = EntityResolver(self.registry)
        result = r.resolve_or_create("organization", "微众银行")
        self.assertTrue(result["entity_id"].startswith("org_"))
        self.assertEqual(result["action"], "create")

    def test_06_normalize_strips_whitespace(self):
        """规范化去空格"""
        r = EntityResolver(self.registry)
        result = r.resolve_or_create("person", "  王老师  ")
        self.assertEqual(result["canonical_name"], "王老师")

    def test_07_persistence_round_trip(self):
        """持久化 reload 不丢"""
        r = EntityResolver(self.registry)
        r.resolve_or_create("person", "陈凌昌")
        r.resolve_or_create("organization", "浙商银行")
        r.save()

        r2 = EntityResolver(self.registry)
        # 重启后能 lookup
        result = r2.resolve_or_create("person", "陈凌昌", aliases=["台州陈"])
        self.assertEqual(result["action"], "update")

    def test_08_alias_lookup(self):
        """通过 alias 反查命中"""
        r = EntityResolver(self.registry)
        first = r.resolve_or_create("person", "黄国华", aliases=["慧穗黄总"])
        r.save()

        r2 = EntityResolver(self.registry)
        # 用 alias 调用也能命中
        result = r2.resolve_or_create("person", "X", aliases=["慧穗黄总"])
        self.assertEqual(first["entity_id"], result["entity_id"])


if __name__ == "__main__":
    unittest.main()
