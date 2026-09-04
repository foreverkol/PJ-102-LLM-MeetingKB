"""
L1 测试:test_lifecycle_stage.py
v7.0 FR-v7.0-005 status_stage 5 阶段 + §8.4 版本规则
6 用例,覆盖合法跃迁 + 非法跃迁拒绝 + 版本递增
"""

import unittest
import sys

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from lifecycle_stage import (
    Stage,
    TRANSITIONS,
    transition_validation,
    transition_safe,
    update_with_version,
    init_frontmatter,
)


class TestLifecycleStage(unittest.TestCase):
    """TC-209 lifecycle_stage 6 用例"""

    def test_01_raw_to_compiled(self):
        """合法跃迁 raw → compiled"""
        self.assertTrue(transition_validation(Stage.RAW, Stage.COMPILED))

    def test_02_compiled_to_reviewed(self):
        """合法跃迁 compiled → reviewed"""
        self.assertTrue(transition_validation(Stage.COMPILED, Stage.REVIEWED))

    def test_03_compiled_to_superseded(self):
        """合法跃迁 compiled → superseded(直接淘汰)"""
        self.assertTrue(transition_validation(Stage.COMPILED, Stage.SUPERSEDED))

    def test_04_reviewed_to_canonical(self):
        """合法跃迁 reviewed → canonical"""
        self.assertTrue(transition_validation(Stage.REVIEWED, Stage.CANONICAL))

    def test_05_canonical_to_superseded(self):
        """合法跃迁 canonical → superseded"""
        self.assertTrue(transition_validation(Stage.CANONICAL, Stage.SUPERSEDED))

    def test_06_superseded_terminates(self):
        """superseded 是终结态"""
        self.assertFalse(transition_validation(Stage.SUPERSEDED, Stage.COMPILED))
        self.assertFalse(transition_validation(Stage.SUPERSEDED, Stage.REVIEWED))
        self.assertFalse(transition_validation(Stage.SUPERSEDED, Stage.CANONICAL))
        self.assertFalse(transition_validation(Stage.SUPERSEDED, Stage.RAW))

    def test_07_invalid_jumps_rejected(self):
        """非法跃迁被拒"""
        # raw 跳过 compiled → canonical 不允许
        self.assertFalse(transition_validation(Stage.RAW, Stage.CANONICAL))
        # raw → reviewed 不允许
        self.assertFalse(transition_validation(Stage.RAW, Stage.REVIEWED))
        # canonical 不能跳回 reviewed
        self.assertFalse(transition_validation(Stage.CANONICAL, Stage.REVIEWED))

    def test_08_transition_safe_raises(self):
        """非法跃迁抛 ValueError"""
        with self.assertRaises(ValueError):
            transition_safe(Stage.RAW, Stage.CANONICAL)

    def test_09_version_increments(self):
        """§8.4 版本递增"""
        fm = {"version": 1, "status_stage": "compiled"}
        new_fm = update_with_version(fm, "RAW/transcripts/2026-08-02_xxx.md")
        self.assertEqual(new_fm["version"], 2)
        self.assertEqual(len(new_fm["previous_versions"]), 1)
        self.assertEqual(new_fm["previous_versions"][0]["version"], 1)
        self.assertEqual(new_fm["previous_versions"][0]["by_source"],
                         "RAW/transcripts/2026-08-02_xxx.md")

    def test_10_init_frontmatter_has_v7_fields(self):
        """§8.1 init_frontmatter 含 v7.0 必填字段"""
        fm = init_frontmatter(
            "meeting",
            "2026-08-02",
            "测试会议",
            "RAW/transcripts/2026-08-02_test.md",
        )
        # v7.0 §8.1 必填字段
        self.assertEqual(fm["status_stage"], "compiled")
        self.assertEqual(fm["version"], 1)
        self.assertEqual(fm["type"], "meeting")
        self.assertEqual(fm["source_ref"], "RAW/transcripts/2026-08-02_test.md")


if __name__ == "__main__":
    unittest.main()
