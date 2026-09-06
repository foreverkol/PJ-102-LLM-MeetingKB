#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_quality_guard.py - 防上次失败"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/scripts/quality_guard.py")


def test_bad_template_fails():
    """模板垃圾应被 quality_guard 拒绝"""
    bad_text = "产业金融的核心是产业金融。https://example.com/x https://wikipedia.org/wiki/产业金融 > \"X\" — 王老师"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check", bad_text],
        capture_output=True, text=True, timeout=10
    )
    # 应该非零退出
    assert result.returncode != 0


def test_real_content_passes():
    """真实内容应通过"""
    good_text = """# Supply Chain Finance

来源:https://en.wikipedia.org/wiki/Supply_chain_finance

Supply chain finance (SCF) is a term...

> "SCF is an approach" — Wikipedia

## See also
- Working capital
"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check", good_text],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0


def test_failed_run_files_caught():
    """归档的失败文件应被 quality_guard 拒绝"""
    archive_dir = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/archive/failed-runs/2026-09-06-瞎搞-rebuild-from-zero")
    if not archive_dir.exists():
        pytest.skip("无失败归档")

    # 找含模板垃圾的文件(原始 sample_S*.md 而非 cite)
    raw_files = list(archive_dir.glob("sample_*.md"))
    if not raw_files:
        pytest.skip("无失败 raw 文件")

    bad_count = 0
    for f in raw_files[:5]:
        content = f.read_text(encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check", content],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            bad_count += 1

    # 至少 1 个失败文件应被拒绝
    assert bad_count >= 1, f"应至少 1 个失败文件被拒绝,实际 {bad_count}/{len(raw_files[:5])}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])