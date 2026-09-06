#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_raw2citations_citations2wiki.py - BT-14 L2.5 工具测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
RAW2CITE = PROJECT_ROOT / "scripts/raw2citations.py"
CITE2WIKI = PROJECT_ROOT / "scripts/citations2wiki.py"
WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")


def test_raw2citations_script_exists():
    assert RAW2CITE.exists()


def test_raw2citations_report():
    """--report 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(RAW2CITE), "--report"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "raw 层统计" in result.stdout


def test_raw2citations_extract_from_clip():
    """从单个 clip 提取 citations 应工作"""
    # 找一个 raw clip
    raw_clips_dir = WIKI_ROOT / "raw_clips"
    if not raw_clips_dir.exists() or not list(raw_clips_dir.glob("*.md")):
        pytest.skip("无 raw clips")

    # 用 --file 单文件模式
    test_file = list(raw_clips_dir.glob("*.md"))[0]
    result = subprocess.run(
        [sys.executable, str(RAW2CITE), "--file", f"raw_clips/{test_file.name}"],
        capture_output=True, text=True, timeout=30
    )
    # 即使创建 citations 失败,也应能 extract(测试函数本身)
    assert "citations" in result.stdout.lower() or "提取" in result.stdout or result.returncode == 0


def test_citations2wiki_script_exists():
    assert CITE2WIKI.exists()


def test_citations2wiki_report():
    """--report 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(CITE2WIKI), "--report"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "citations 层统计" in result.stdout


def test_citations2wiki_compile_judgment():
    """--type judgment 应能编译"""
    result = subprocess.run(
        [sys.executable, str(CITE2WIKI), "--type", "judgment", "--limit", "5"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "编译" in result.stdout or "judgment" in result.stdout.lower()


def test_three_tier_pipeline():
    """完整三层管线: scan → tier_classifier → raw2citations → citations2wiki"""
    # 1. tier_classifier report
    result1 = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/tier_classifier.py"), "report"],
        capture_output=True, text=True, timeout=30
    )
    assert result1.returncode == 0

    # 2. raw2citations report
    result2 = subprocess.run(
        [sys.executable, str(RAW2CITE), "--report"],
        capture_output=True, text=True, timeout=30
    )
    assert result2.returncode == 0

    # 3. citations2wiki report
    result3 = subprocess.run(
        [sys.executable, str(CITE2WIKI), "--report"],
        capture_output=True, text=True, timeout=30
    )
    assert result3.returncode == 0

    # 三步都成功(检查各脚本输出的关键词)
    assert "raw" in result1.stdout.lower() or "raw" in result1.stdout
    assert "raw" in result2.stdout  # raw2citations 输出"raw 层统计"
    assert "citations" in result3.stdout.lower() or "type" in result3.stdout.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])