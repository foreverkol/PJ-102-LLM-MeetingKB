"""
PJ-102-LLM-MeetingKB · 烟雾测试 v1.0

验证核心流程：
1. LLM Client 初始化
2. JSON 容错解析
3. 12 步基本功能
4. WIKI 写入

用法：
    cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code
    python3 ../tests/unit/smoke_test.py
"""

import os
import sys
import unittest
from pathlib import Path

# 添加代码目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "03-执行/code"))


class TestLLMClient(unittest.TestCase):
    """测试 LLM Client"""

    def test_auto_select_provider(self):
        """测试自动选择 provider"""
        from llm_client import LLMClient

        # 不清空环境，模拟真实场景
        client = LLMClient()
        self.assertIn(client.provider, ["minimax", "deepseek", "openai", "anthropic", "mock"])
        print(f"✅ 自动选择 provider: {client.provider}")

    def test_safe_json_parse_clean(self):
        """测试 JSON 解析 - 标准 JSON"""
        from llm_client import safe_json_parse

        content = '{"name": "test", "value": 123}'
        result = safe_json_parse(content, {"default": True})
        self.assertEqual(result["name"], "test")
        self.assertEqual(result["value"], 123)
        print("✅ 标准 JSON 解析")

    def test_safe_json_parse_markdown(self):
        """测试 JSON 解析 - markdown 包裹"""
        from llm_client import safe_json_parse

        content = '```json\n{"name": "test"}\n```'
        result = safe_json_parse(content, {})
        self.assertEqual(result["name"], "test")
        print("✅ Markdown 包裹 JSON 解析")

    def test_safe_json_parse_trailing_comma(self):
        """测试 JSON 解析 - 尾随逗号"""
        from llm_client import safe_json_parse

        content = '{"items": [1, 2, 3,]}'
        result = safe_json_parse(content, {})
        self.assertEqual(result["items"], [1, 2, 3])
        print("✅ 尾随逗号 JSON 解析")

    def test_safe_json_parse_empty(self):
        """测试 JSON 解析 - 空内容"""
        from llm_client import safe_json_parse

        default = {"default": True}
        result = safe_json_parse("", default)
        self.assertEqual(result, default)
        print("✅ 空内容返回默认")


class TestPipeline(unittest.TestCase):
    """测试 Pipeline 流程"""

    def test_s1_basic(self):
        """测试 S1 基础信息"""
        from steps import s1_basic_info

        result = s1_basic_info("20260802_133331到西安_原文.md", "测试内容" * 100)
        self.assertIn("title", result)
        self.assertIn("date", result)
        self.assertEqual(result["date"], "2026-08-02")
        print(f"✅ S1 基础信息: date={result['date']}, char_count={result['char_count']}")

    def test_pipeline_imports(self):
        """测试 12 步都可以导入"""
        from steps import (
            s1_basic_info, s2_scene_recognition, s3_standard_summary,
            s4_fjv, s5_implicit_knowledge, s6_entity_extraction,
            s7_action_decision, s8_risk_blindspot, s9_knowledge_classify,
            s10_cognitive_refine, s11_value_rating, s12_write_wiki,
        )
        print("✅ 12 步全部可导入")


class TestWIKIOutput(unittest.TestCase):
    """测试 WIKI 输出"""

    def test_sample_index_exists(self):
        """测试 index.json 存在"""
        index_file = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/system/data/index.json")
        self.assertTrue(index_file.exists(), "index.json 不存在")

        import json
        data = json.loads(index_file.read_text(encoding='utf-8'))
        self.assertGreater(data["sample_count"], 0)
        print(f"✅ index.json 存在: {data['sample_count']} 个样本")

    def test_sample_files_exist(self):
        """测试源文件已复制"""
        raw_dir = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/system/data/raw")
        files = list(raw_dir.glob("*_原文.md"))
        self.assertGreater(len(files), 0)
        print(f"✅ 源文件已复制: {len(files)} 个")


def main():
    """运行所有测试"""
    print("=" * 80)
    print("  PJ-102-LLM-MeetingKB · 烟雾测试 v1.0")
    print("=" * 80)
    print()

    # 设置环境变量（如果没设）
    if not os.environ.get("MINIMAX_API_KEY"):
        try:
            env_file = Path.home() / ".hermes/.env"
            if env_file.exists():
                for line in env_file.read_text(encoding='utf-8').split("\n"):
                    if line.startswith("MINIMAX_API_KEY="):
                        os.environ["MINIMAX_API_KEY"] = line.split("=", 1)[1]
                    if line.startswith("MINIMAX_CN_BASE_URL="):
                        os.environ["MINIMAX_CN_BASE_URL"] = line.split("=", 1)[1]
        except Exception as e:
            print(f"⚠️  无法读取 ~/.hermes/.env: {e}")

    # 运行测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestLLMClient))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestWIKIOutput))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print()
        print("✅ 所有测试通过")
        sys.exit(0)
    else:
        print()
        print("❌ 测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()