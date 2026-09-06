#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_rebuild_from_zero.py - Sprint 25 完全重建测试(修正版)"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
ARCHIVE = WIKI_ROOT / "archive" / "wiki-2026-09-06-final"
TRACKING = PROJECT_ROOT / "04-复盘与决策" / "深度重建日志"


def test_script_exists():
    assert (PROJECT_ROOT / "scripts/rebuild_from_zero.py").exists()


def test_archive_exists():
    assert ARCHIVE.exists()


def test_5_samples_created():
    """5 样例应全部创建(S5 因 theme='判断/观点' 是目录而非文件)"""
    raw_clips = WIKI_ROOT / "raw_clips"
    wiki_dir = WIKI_ROOT / "wiki"

    # 支持 .md 文件和 S5 目录两种情况
    raw_files = list(raw_clips.glob("sample_S*"))
    sample_count = sum(1 for f in raw_files if f.name.startswith("sample_S"))
    assert sample_count >= 5, f"raw 期望 5,实际 {sample_count}"

    wiki_files = list(wiki_dir.glob("wiki_S*"))
    wiki_count = sum(1 for f in wiki_files if f.name.startswith("wiki_S"))
    assert wiki_count >= 5, f"wiki 期望 5,实际 {wiki_count}"


def test_citations_per_sample():
    """每样例 12 citations,总 ~60"""
    cite_files = list((WIKI_ROOT / "citations").glob("cite_sample_S*.md"))
    assert 50 <= len(cite_files) <= 70, f"citations 数量 {len(cite_files)} 异常"


def test_quality_above_threshold():
    """质量评分应 >= 75"""
    summary_files = list(TRACKING.glob("rebuild_summary_*.json"))
    if not summary_files:
        pytest.skip("无 summary,跳过")

    latest = max(summary_files, key=lambda f: f.stat().st_mtime)
    data = json.loads(latest.read_text(encoding="utf-8"))

    avg = data.get("avg_quality", 0)
    assert avg >= 75, f"平均质量 {avg} < 75"


def test_tracking_log_has_steps():
    """跟踪日志应包含关键步骤"""
    log_files = list(TRACKING.glob("rebuild_log_*.log"))
    if not log_files:
        pytest.skip("无 log")

    latest = max(log_files, key=lambda f: f.stat().st_mtime)
    content = latest.read_text(encoding="utf-8")

    # 关键步骤标识
    assert "STEP 1" in content, "缺 STEP 1 备份"
    assert "STEP 2" in content, "缺 STEP 2 清理"
    assert "STEP 3" in content, "缺 STEP 3 选样例"
    assert "S1" in content, "缺 S1 样例"
    assert "S5" in content, "缺 S5 样例"
    assert "quality" in content.lower(), "缺 quality 步骤"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])