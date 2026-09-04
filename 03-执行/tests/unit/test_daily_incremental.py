"""
L1 测试:test_daily_incremental.py
v3.0 增量调度
6 用例
"""

import unittest
import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
from daily_incremental import (
    compute_content_hash,
    load_processed,
    save_processed,
    find_new_files,
    run_incremental,
    mark_processed,
)


class TestDailyIncremental(unittest.TestCase):
    """TC-212 daily_incremental 6 用例"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.source = Path(self.tmp) / "source"
        self.source.mkdir()
        self.state_file = Path(self.tmp) / "processed_files.json"

    def _write(self, name, content):
        p = self.source / name
        p.write_text(content, encoding="utf-8")
        return p

    def test_01_content_hash_deterministic(self):
        """相同内容 → 相同 hash"""
        h1 = compute_content_hash("hello")
        h2 = compute_content_hash("hello")
        self.assertEqual(h1, h2)
        # 12 字符
        self.assertEqual(len(h1), 12)

    def test_02_find_new_files(self):
        """扫描新文件"""
        self._write("a.md", "A content")
        self._write("b.md", "B content")
        state = load_processed(self.state_file)
        new = find_new_files(self.source, state)
        self.assertEqual(len(new), 2)

    def test_03_skips_processed(self):
        """跳过已处理"""
        self._write("a.md", "A content")
        state = load_processed(self.state_file)
        # 标记 a 已处理
        mark_processed(state, self.source / "a.md",
                       compute_content_hash("A content"),
                       {"ok": True, "s2": {}, "s11": {}, "wiki_files_written": 1})
        save_processed(self.state_file, state)
        # 再扫描
        state2 = load_processed(self.state_file)
        new = find_new_files(self.source, state2)
        self.assertEqual(len(new), 0)

    def test_04_dry_run_no_process(self):
        """dry-run 不真正处理"""
        self._write("a.md", "A")
        report = run_incremental(
            source_dir=self.source,
            state_file=self.state_file,
            pipeline_fn=None,
            dry_run=True,
        )
        self.assertEqual(report["processed_count"], 0)
        # 状态文件不应有 processed 字段
        state = load_processed(self.state_file)
        self.assertEqual(len(state.get("processed", [])), 0)

    def test_05_pipeline_run_marks_processed(self):
        """跑 1 个 sample 成功 → state 追加"""
        self._write("a.md", "A content unique")

        def fake_pipeline(file_path, content, content_hash):
            return {
                "ok": True,
                "s2": {"scene_type": "client_visit"},
                "s11": {"value_score": 0.85},
                "wiki_files_written": 5,
            }

        report = run_incremental(
            source_dir=self.source,
            state_file=self.state_file,
            pipeline_fn=fake_pipeline,
            lint_fn=lambda: {},
        )
        self.assertEqual(report["processed_count"], 1)
        state = load_processed(self.state_file)
        self.assertEqual(len(state["processed"]), 1)
        self.assertEqual(state["processed"][0]["filename"], "a.md")
        self.assertEqual(state["processed"][0]["status"], "ok")
        self.assertEqual(state["processed"][0]["wiki_files_written"], 5)

    def test_06_error_captured_not_blocking(self):
        """1 个失败不应阻塞后续"""
        self._write("bad.md", "BAD")
        self._write("good.md", "GOOD")

        def fake_pipeline(file_path, content, content_hash):
            if "BAD" in content:
                raise RuntimeError("simulated LLM failure")
            return {"ok": True, "s2": {}, "s11": {}, "wiki_files_written": 5}

        report = run_incremental(
            source_dir=self.source,
            state_file=self.state_file,
            pipeline_fn=fake_pipeline,
            lint_fn=lambda: {},
        )
        # 1 成功 1 失败 — processed_count=1
        self.assertEqual(report["processed_count"], 1)
        self.assertEqual(len(report["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
