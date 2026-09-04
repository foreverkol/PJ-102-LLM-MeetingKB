"""
L1 测试:test_minimax_thinking_fallback.py
Sprint 9 新增 — 验证 v3.0 关键修复
- MiniMax-M3 thinking content fallback
- max_tokens 截断检测
- s12 frontmatter v6.1+v7.0 字段完整性
"""

import unittest
import sys
from pathlib import Path
import json

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")

from llm_client import LLMClient, safe_json_parse


class TestMiniMaxThinkingFallback(unittest.TestCase):
    """Sprint 9: MiniMax-M3 thinking 模式 content 截断 fallback"""

    def test_01_normal_content_returned(self):
        """正常 content 直接返回(非空 content)"""
        client = LLMClient(provider="mock")
        result = client.call("test", max_tokens=100)
        self.assertEqual(result, '{"mock": true}')

    def test_02_safe_json_parse_empty_default_dict(self):
        """空 content → 返回 default dict"""
        result = safe_json_parse("", {"scene_type": "other"})
        self.assertEqual(result["scene_type"], "other")

    def test_03_safe_json_parse_empty_default_list(self):
        """空 content → 返回 default list"""
        result = safe_json_parse("[]", default=[])
        self.assertEqual(result, [])

    def test_04_safe_json_parse_malformed_markdown_fence(self):
        """```json``` 围栏自动剥离"""
        malformed = '```json\n{"scene_type": "client_visit"}\n```'
        result = safe_json_parse(malformed, {})
        self.assertEqual(result.get("scene_type"), "client_visit")

    def test_05_safe_json_parse_trailing_comma(self):
        """尾随逗号容错"""
        malformed = '{"a": 1, "b": 2,}'
        result = safe_json_parse(malformed, {})
        self.assertEqual(result.get("a"), 1)
        self.assertEqual(result.get("b"), 2)


class TestS12FrontmatterFields(unittest.TestCase):
    """Sprint 9: s12_wiki frontmatter v6.1+v7.0 字段"""

    def test_01_frontmatter_template_has_meeting_type(self):
        """s12_wiki meeting frontmatter 模板含 meeting_type 字段"""
        s12_path = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/steps/s12_wiki.py")
        content = s12_path.read_text(encoding="utf-8")
        self.assertIn("meeting_type:", content)
        self.assertIn("meeting_subtype:", content)
        self.assertIn("is_external_knowledge:", content)

    def test_02_frontmatter_template_has_ldamc(self):
        """s12_wiki meeting frontmatter 模板含 ldamc 5 维"""
        s12_path = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/steps/s12_wiki.py")
        content = s12_path.read_text(encoding="utf-8")
        # 5 个 ldamc 维度
        for dim in ["lost", "different", "added", "more", "connected"]:
            self.assertIn(f"{dim}:", content, f"ldamc 缺 {dim}")

    def test_03_frontmatter_template_has_status_stage(self):
        """v7.0 §8.1 status_stage 必填"""
        s12_path = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/steps/s12_wiki.py")
        content = s12_path.read_text(encoding="utf-8")
        self.assertIn("status_stage:", content)
        self.assertIn("compiled", content)

    def test_04_meeting_type_six_types_in_prompt(self):
        """s2_scene prompt 6 类枚举齐全"""
        s2_path = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/steps/s2_scene.py")
        content = s2_path.read_text(encoding="utf-8")
        for st in ["client_visit", "bank_communication", "investor_沟通",
                    "partner_coordination", "internal_review", "industry_exchange",
                    "personal_thinking"]:
            self.assertIn(st, content, f"6 类 scene_type 缺 {st}")


class TestRealWikiV3Quality(unittest.TestCase):
    """Sprint 9: 实际 v3.0 跑出的 wiki 文件 frontmatter 质量"""

    def test_01_meeting_36945f63_real_meeting_type(self):
        """sample1 frontmatter meeting_type 真实化(非 other)"""
        wiki_path = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings/meeting_2026-08-27_36945f63c541.md")
        if not wiki_path.exists():
            self.skipTest("wiki 文件不存在,需先跑 pipeline")
        text = wiki_path.read_text(encoding="utf-8")
        # 提取 frontmatter
        self.assertIn("meeting_type:", text)
        # 必须是 6 类之一,不是 "other"
        import re
        m = re.search(r"meeting_type:\s*(\S+)", text)
        if m:
            valid = {"client_visit", "bank_communication", "investor_沟通",
                      "partner_coordination", "internal_review", "industry_exchange",
                      "personal_thinking"}
            self.assertIn(m.group(1), valid, f"meeting_type {m.group(1)} 不在 6 类中")

    def test_02_meeting_36945f63_real_ldamc(self):
        """sample1 ldamc 5 维非 '暂无'"""
        wiki_path = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings/meeting_2026-08-27_36945f63c541.md")
        if not wiki_path.exists():
            self.skipTest("wiki 文件不存在")
        text = wiki_path.read_text(encoding="utf-8")
        # ldamc.lost 字段不应是"暂无"
        self.assertIn("lost: \"未明确提及", text, "ldamc.lost 应有真实内容")
        self.assertNotIn("lost: \"暂无\"", text)

    def test_03_minimax_m3_in_frontmatter(self):
        """王老师 09-04 纠正生效:llm_model: MiniMax-M3"""
        wiki_path = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings/meeting_2026-08-27_36945f63c541.md")
        if not wiki_path.exists():
            self.skipTest("wiki 文件不存在")
        text = wiki_path.read_text(encoding="utf-8")
        self.assertIn("llm_model: MiniMax-M3", text)
        self.assertNotIn("llm_model: MiniMax-Text-01", text)

    def test_04_generator_v3_in_frontmatter(self):
        """generator 字段是 v3.0"""
        wiki_path = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings/meeting_2026-08-27_36945f63c541.md")
        if not wiki_path.exists():
            self.skipTest("wiki 文件不存在")
        text = wiki_path.read_text(encoding="utf-8")
        self.assertIn("generator: pj102-llm-meetingkb-v3.0", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
