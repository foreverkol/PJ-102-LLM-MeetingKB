"""
L1 测试:test_scenario_extractor.py
5 用例
"""

import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from scenario_extractor import scenario_to_md, write_scenarios, _list_to_md


class TestScenarioExtractor(unittest.TestCase):
    """TC-217 scenario_extractor 5 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.wiki = Path(self.tmp) / "wiki"
        self.wiki.mkdir()

    def test_01_md_contains_11_fields(self):
        """md 输出含 11 字段(中文标签 + 英文 key)"""
        scen = {
            "theme": "财税 SaaS",
            "customer": "中大企业",
            "pain_point": "成本中心",
            "offering": "SaaS",
            "value_capture": "订阅",
            "channel": "直销",
            "key_resources": ["税局连接"],
            "key_constraints": ["合规"],
            "hidden_assumptions": ["开放数据"],
            "trigger_signals": ["降本"],
            "failure_modes": ["政策"],
        }
        md = scenario_to_md(scen)
        # 检查 11 字段的中文标签都在(frontmatter 或正文)
        chinese_labels = ["客户", "痛点", "Offering", "价值捕获", "销售渠道",
                          "关键资源", "关键约束", "隐性假设", "触发信号", "失败模式"]
        for label in chinese_labels:
            self.assertIn(label, md, f"md 缺中文标签 {label}")

    def test_02_md_has_v7_frontmatter(self):
        """v7.0 §8.1 frontmatter 含 status_stage"""
        scen = {"theme": "Test"}
        md = scenario_to_md(scen)
        self.assertIn("type: scenario", md)
        self.assertIn("status_stage: compiled", md)
        self.assertIn("knowledge_tier: L3_knowledge", md)

    def test_03_write_scenarios_to_dir(self):
        """写入 WIKI/Knowledge/Scenarios/"""
        scenarios = [
            {
                "theme": "财税 SaaS",
                "customer": "中大企业", "pain_point": "x",
                "offering": "SaaS", "value_capture": "订阅",
                "channel": "直销", "key_resources": ["税局"],
                "key_constraints": ["合规"],
                "hidden_assumptions": [], "trigger_signals": [],
                "failure_modes": [],
            },
        ]
        written = write_scenarios(scenarios, self.wiki,
                                 source_ref="RAW/2026-08-02_xxx.md",
                                 meeting_date="2026-08-02")
        self.assertEqual(len(written), 1)
        # 文件存在
        self.assertTrue(written[0].exists())
        # 在 Scenarios/ 子目录
        self.assertIn("Scenarios", str(written[0]))
        # 文件名含 slug
        self.assertIn("财税_SaaS", written[0].name)

    def test_04_empty_list_returns_empty(self):
        """空 scenario 列表 → 不写"""
        written = write_scenarios([], self.wiki)
        self.assertEqual(written, [])
        # 目录可能创建但不应当有 md 文件
        scen_dir = self.wiki / "Knowledge" / "Scenarios"
        if scen_dir.exists():
            self.assertEqual(len(list(scen_dir.glob("*.md"))), 0)

    def test_05_list_to_md_empty(self):
        """_list_to_md 空列表 → (无)"""
        self.assertEqual(_list_to_md([]), "(无)")
        self.assertEqual(_list_to_md(["A", "B"]), "A; B")


if __name__ == "__main__":
    unittest.main()
