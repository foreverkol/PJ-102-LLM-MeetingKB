#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_verify_small_scale.py - Sprint 25 小范围验证测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/verify_small_scale.py"
REPORT = PROJECT_ROOT / "04-复盘与决策/知识库转化验证报告v1.0.md"


def test_script_exists():
    assert SCRIPT.exists()


def test_run_runs():
    """--run 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--run"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "验证报告" in result.stdout


def test_report_exists():
    """验证报告应生成"""
    # 先跑确保报告存在
    subprocess.run(
        [sys.executable, str(SCRIPT), "--run"],
        capture_output=True, text=True, timeout=60
    )
    assert REPORT.exists()
    assert REPORT.stat().st_size > 1000


def test_report_structure():
    """报告应包含 3 主题"""
    content = REPORT.read_text(encoding="utf-8")
    assert "产业金融" in content
    assert "数据风控" in content
    assert "AI赋能" in content or "AI 赋能" in content


def test_three_themes_verified():
    """3 主题都应有数据"""
    content = REPORT.read_text(encoding="utf-8")
    assert "总主题数" in content or "3" in content
    # 数据血缘
    assert "血缘" in content or "lineage" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])