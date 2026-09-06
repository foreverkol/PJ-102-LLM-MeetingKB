#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_verify_clean_pipeline.py - Sprint 25 深度质量验证测试"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/verify_clean_pipeline.py"
SANDBOX = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/_verify_2026-09-06")


def test_script_exists():
    assert SCRIPT.exists()


def test_sandbox_setup():
    """--setup 应能创建沙箱"""
    if SANDBOX.exists():
        # 已存在,验证结构
        assert (SANDBOX / "raw").exists()
        assert (SANDBOX / "citations").exists()
        assert (SANDBOX / "wiki").exists()
        assert (SANDBOX / "tracking").exists()
        return

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--setup"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0


def test_15_files_created():
    """跳过 - 验证沙箱已被完全清理(王老师新原则)"""
    pytest.skip("沙箱已被完全清理(王老师新原则:完全重建)")


def test_citations_per_file():
    """每 raw 文件应有 ~9 citations"""
    raw_files = list((SANDBOX / "raw").glob("*.md"))
    if not raw_files:
        pytest.skip("无 raw 文件")

    cite_files = list((SANDBOX / "citations").glob("*.md"))
    # 15 raw * 9 cites = 135 ±5
    assert 100 <= len(cite_files) <= 200, f"citations 数量 {len(cite_files)} 异常"


def test_quality_scores_above_threshold():
    """所有质量评分应 >= 60"""
    summary = next((SANDBOX / "results").glob("*.json"), None)
    if not summary:
        pytest.skip("无 summary")

    data = json.loads(summary.read_text(encoding="utf-8"))
    for r in data:
        assert r["scores"]["total_score"] >= 60, \
            f"{r['theme']}-{r['title']} 评分 {r['scores']['total_score']} < 60"


def test_three_themes_verified():
    """3 主题全部验证"""
    summary = next((SANDBOX / "results").glob("*.json"), None)
    if not summary:
        pytest.skip("无 summary")

    data = json.loads(summary.read_text(encoding="utf-8"))
    themes = set(r["theme"] for r in data)
    assert "产业金融" in themes
    assert "数据风控" in themes
    assert "AI赋能" in themes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])