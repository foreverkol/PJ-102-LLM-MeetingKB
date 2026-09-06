#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_l345_integration.py - L3/L4/L5 集成测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
CODEX_REVIEWER = PROJECT_ROOT / "scripts/codex_reviewer.py"
NOTEBOOKLM_RAG = PROJECT_ROOT / "scripts/notebooklm_rag.py"
PROMOTE_V2 = PROJECT_ROOT / "scripts/promote_v2_to_pj.py"


def test_codex_reviewer_status():
    """--status 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(CODEX_REVIEWER), "--status"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "评审模式" in result.stdout


def test_codex_reviewer_imports():
    """codex_reviewer 应能 import"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("codex_reviewer", CODEX_REVIEWER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "check_codex_login")
    assert hasattr(module, "get_current_mode")


def test_notebooklm_rag_setup():
    """--setup 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(NOTEBOOKLM_RAG), "--setup"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "notebooklm" in result.stdout.lower()


def test_promote_v2_list():
    """--list 应能列出候选 PJ"""
    result = subprocess.run(
        [sys.executable, str(PROMOTE_V2), "--list"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "PJ 项目" in result.stdout or "发现" in result.stdout


def test_promote_v2_dry_run():
    """--promote --dry-run 应能预览(不实际复制)"""
    result = subprocess.run(
        [sys.executable, str(PROMOTE_V2), "--promote", "PJ-001", "--dry-run"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0
    assert "预览" in result.stdout or "PJ-001" in result.stdout


def test_l345_pipeline_integration():
    """L3/L4/L5 三脚本端到端集成"""
    # L3 状态
    r3 = subprocess.run(
        [sys.executable, str(CODEX_REVIEWER), "--status"],
        capture_output=True, text=True, timeout=30
    )
    # L4 setup
    r4 = subprocess.run(
        [sys.executable, str(NOTEBOOKLM_RAG), "--setup"],
        capture_output=True, text=True, timeout=30
    )
    # L5 报告
    r5 = subprocess.run(
        [sys.executable, str(PROMOTE_V2), "--report"],
        capture_output=True, text=True, timeout=30
    )

    assert r3.returncode == 0
    assert r4.returncode == 0
    assert r5.returncode == 0
    assert "mode" in r3.stdout.lower() or "模式" in r3.stdout
    assert "notebooklm" in r4.stdout.lower()
    assert "PJ" in r5.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])