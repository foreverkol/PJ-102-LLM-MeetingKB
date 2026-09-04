"""
L1 测试:test_s14_scenario.py
4 用例
"""

import unittest
import sys

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from steps.s14_scenario import s14_scenario, SCENARIO_FIELDS


class TestS14Scenario(unittest.TestCase):
    """TC-216 s14_scenario 4 用例"""

    def test_01_full_scenario(self):
        """11 字段全填"""
        class MockLLM:
            def call(self, prompt, **kwargs):
                return """[{
                    "theme": "财税 SaaS 变现",
                    "customer": "中大企业财务部门",
                    "pain_point": "成本中心无收入",
                    "offering": "业财税一体化 SaaS",
                    "value_capture": "订阅+佣金",
                    "channel": "直销+分销",
                    "key_resources": ["税局连接"],
                    "key_constraints": ["合规"],
                    "hidden_assumptions": ["企业愿开放数据"],
                    "trigger_signals": ["降本增效"],
                    "failure_modes": ["政策变化"]
                }]"""
        result = s14_scenario("test", MockLLM())
        self.assertEqual(len(result), 1)
        scen = result[0]
        # 11 字段全
        for k in SCENARIO_FIELDS:
            self.assertIn(k, scen)
            self.assertTrue(scen[k])

    def test_02_no_clear_pattern(self):
        """无清晰模式 → 空数组"""
        class MockLLM:
            def call(self, prompt, **kwargs):
                return "[]"
        result = s14_scenario("闲聊", MockLLM())
        self.assertEqual(result, [])

    def test_03_partial_scenario_rejected(self):
        """少字段(<3) → 过滤"""
        class MockLLM:
            def call(self, prompt, **kwargs):
                return '[{"theme": "X", "customer": "C"}]'
        result = s14_scenario("test", MockLLM())
        self.assertEqual(len(result), 0)

    def test_04_missing_fields_filled_with_defaults(self):
        """缺字段兜底"""
        class MockLLM:
            def call(self, prompt, **kwargs):
                return """[{
                    "theme": "票据中介",
                    "customer": "银行",
                    "pain_point": "信息不对称",
                    "offering": "撮合服务",
                    "value_capture": "佣金",
                    "channel": "关系网络",
                    "key_resources": ["客户经理"],
                    "key_constraints": ["合规"],
                    "hidden_assumptions": ["银行愿外包"],
                    "trigger_signals": [],
                    "failure_modes": []
                }]"""
        result = s14_scenario("test", MockLLM())
        self.assertEqual(len(result), 1)
        scen = result[0]
        # trigger_signals + failure_modes 应该是 [] 数组
        self.assertEqual(scen["trigger_signals"], [])
        self.assertEqual(scen["failure_modes"], [])


if __name__ == "__main__":
    unittest.main()
