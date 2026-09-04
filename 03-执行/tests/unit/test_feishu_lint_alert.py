"""
L1 测试:test_feishu_lint_alert.py
v3.0 feishu_lint_alert.py
4 用例(精简)
"""

import unittest
import sys
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from feishu_lint_alert import build_message, lint_alert, get_webhook_url


class TestFeishuLintAlert(unittest.TestCase):
    """TC-213 feishu_lint_alert 4 用例"""

    def test_01_build_message_clean(self):
        """无 critical → 显示 ✅"""
        report = {"3_missing_sources": [], "8_required_field_violations": []}
        payload = build_message(report)
        self.assertIn("PJ-102 Wiki Lint 巡检报告", payload["content"]["text"])
        self.assertIn("全部维度无 critical issues", payload["content"]["text"])

    def test_02_build_message_with_issues(self):
        """有 missing_sources → 列前 5 条"""
        report = {
            "3_missing_sources": [f"file{i}.md" for i in range(7)],
            "8_required_field_violations": [
                "m.md [meeting]: missing ['ldamc']",
            ],
        }
        payload = build_message(report)
        text = payload["content"]["text"]
        self.assertIn("源引用缺失: 7 处", text)
        self.assertIn("v7.0 §8.1 必填字段缺失: 1 处", text)
        self.assertIn("file0.md", text)
        # 限 5 条
        self.assertNotIn("file5.md", text)
        self.assertNotIn("file6.md", text)

    def test_03_dry_run_no_send(self):
        """dry-run 不发"""
        report = {"3_missing_sources": ["x.md"]}
        result = lint_alert(report, webhook_url="https://invalid", dry_run=True)
        self.assertFalse(result["sent"])
        self.assertEqual(result["mode"], "dry_run")
        # 中文 label 应出现在 payload
        self.assertIn("源引用缺失", result["payload"]["content"]["text"])

    def test_04_env_disable(self):
        """MINIMAX_LINT_ALERT=0 时不发"""
        import os
        os.environ["MINIMAX_LINT_ALERT"] = "0"
        try:
            report = {"3_missing_sources": ["x.md"]}
            result = lint_alert(report, webhook_url="https://invalid")
            self.assertFalse(result["sent"])
            self.assertEqual(result["mode"], "disabled")
        finally:
            del os.environ["MINIMAX_LINT_ALERT"]


if __name__ == "__main__":
    unittest.main()
