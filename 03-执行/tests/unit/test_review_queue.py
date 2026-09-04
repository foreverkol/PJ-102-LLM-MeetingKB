"""
L1 测试:test_review_queue.py
6 用例
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from review_queue import classify_item, enqueue


class TestReviewQueue(unittest.TestCase):
    """TC-218 review_queue 6 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.queue_root = Path(self.tmp) / "review_queue"

    def test_01_auto_pass_normal_judgment(self):
        """普通判断 → auto_pass"""
        item = {
            "type": "judgment",
            "title": "贷转票可行性",
            "source_ref": "RAW/2026-08-02_xxx.md",
            "status_stage": "compiled",
            "judgment": "贷转票适合短期周转",
            "topic_key": "loan_to_note/feasibility",
        }
        self.assertEqual(classify_item(item), "auto_pass")

    def test_02_forced_review_high_value_keyword(self):
        """高价值关键词 → forced_review"""
        item = {
            "type": "decision",
            "title": "战略调整",
            "source_ref": "RAW/x.md",
            "status_stage": "compiled",
            "content": "决定 1000万 大额投入,颠覆原有方向",
        }
        self.assertEqual(classify_item(item), "forced_review")

    def test_03_forced_review_contradiction_pending(self):
        """contradiction pending → forced_review"""
        item = {
            "type": "judgment",
            "title": "微众合作",
            "source_ref": "RAW/x.md",
            "status_stage": "compiled",
            "contradictions": [
                {"target": "J1", "type": "conflict", "resolution": "pending_review"},
            ],
        }
        self.assertEqual(classify_item(item), "forced_review")

    def test_04_batch_confirm_missing_fields(self):
        """缺字段 → batch_confirm"""
        item = {
            "type": "judgment",
            "title": "X",
            # 缺 source_ref / status_stage
        }
        self.assertEqual(classify_item(item), "batch_confirm")

    def test_05_enqueue_writes_files(self):
        """enqueue 实际写文件"""
        item = {
            "type": "judgment",
            "title": "测试判断",
            "source_ref": "RAW/x.md",
            "status_stage": "compiled",
            "judgment": "测试",
        }
        result = enqueue(item, self.queue_root, batch_id="test-batch")
        self.assertEqual(result["level"], "auto_pass")
        self.assertTrue(Path(result["item_path"]).exists())

        # batch_info.json 存在
        today = item.get("source_ref", "")  # 占位
        info_files = list(self.queue_root.rglob("batch_info.json"))
        self.assertGreater(len(info_files), 0)

    def test_06_multiple_items_in_same_batch(self):
        """同一 batch 多 item"""
        items = [
            {"type": "judgment", "title": "A", "source_ref": "x",
             "status_stage": "compiled"},
            {"type": "judgment", "title": "B", "source_ref": "y",
             "status_stage": "compiled"},
        ]
        for it in items:
            enqueue(it, self.queue_root, batch_id="multi-batch")
        # auto_pass 目录应当有 2 个 item
        auto_pass_items = list(self.queue_root.rglob("auto_pass/*.json"))
        self.assertGreaterEqual(len(auto_pass_items), 2)


if __name__ == "__main__":
    unittest.main()
