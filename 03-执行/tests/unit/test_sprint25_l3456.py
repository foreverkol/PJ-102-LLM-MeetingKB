#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_sprint25_l3456.py - Sprint 25 L3-L6 集成测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
PJ_SWARM = PROJECT_ROOT / "scripts/pj_swarm.py"
INIT_PJ_STATE = PROJECT_ROOT / "scripts/init_pj_state.py"


def test_pj_swarm_script_exists():
    assert PJ_SWARM.exists()


def test_pj_swarm_scan():
    """--scan 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(PJ_SWARM), "--scan"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "PJ 项目" in result.stdout or "扫描" in result.stdout


def test_pj_swarm_dashboard():
    """--dashboard 应能生成 HTML"""
    result = subprocess.run(
        [sys.executable, str(PJ_SWARM), "--dashboard"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    html_path = PROJECT_ROOT / ".swarm" / "index.html"
    assert html_path.exists()
    assert html_path.stat().st_size > 5000  # 至少 5KB


def test_pj_swarm_html_content():
    """Swarm HTML 应包含关键内容"""
    html_path = PROJECT_ROOT / ".swarm" / "index.html"
    if not html_path.exists():
        pytest.skip("HTML 不存在")
    content = html_path.read_text(encoding="utf-8")
    assert "PJ Swarm" in content
    assert "swarm-card" in content
    assert "总 PJ 项目" in content
    # 至少包含 5 个 PJ 名称
    pj_count = sum(1 for line in content.split("\n") if "pj-name" in line)
    assert pj_count >= 5


def test_init_pj_state_script_exists():
    assert INIT_PJ_STATE.exists()


def test_init_pj_state_report():
    """--report 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(INIT_PJ_STATE), "--report"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "PJ" in result.stdout


def test_init_pj_state_dry_run():
    """--all --dry-run 应能预览(不实际写)"""
    result = subprocess.run(
        [sys.executable, str(INIT_PJ_STATE), "--all", "--dry-run"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "预览" in result.stdout or "未激活" in result.stdout


def test_l3456_integration():
    """L3 + L5 + L6 集成"""
    # L3 Swarm
    r3 = subprocess.run(
        [sys.executable, str(PJ_SWARM), "--report"],
        capture_output=True, text=True, timeout=30
    )
    # L5 Web Clipper
    r5 = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts/tier_classifier.py"), "report"],
        capture_output=True, text=True, timeout=30
    )
    # L6 init_pj_state
    r6 = subprocess.run(
        [sys.executable, str(INIT_PJ_STATE), "--report"],
        capture_output=True, text=True, timeout=30
    )

    assert r3.returncode == 0
    assert r5.returncode == 0
    assert r6.returncode == 0
    assert "PJ" in r3.stdout
    assert "tier" in r5.stdout
    assert "PJ" in r6.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])