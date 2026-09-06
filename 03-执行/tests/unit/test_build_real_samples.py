#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_build_real_samples.py - Phase 2 测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/build_real_samples.py"
GUARD = PROJECT_ROOT / "scripts/quality_guard.py"


def test_real_samples_created():
    """3 样例应全部创建"""
    raw_files = list((WIKI_ROOT / "raw_clips").glob("sample_S*.md"))
    wiki_files = list((WIKI_ROOT / "wiki").glob("wiki_S*.md"))

    assert len(raw_files) >= 3, f"raw 期望 3+,实际 {len(raw_files)}"
    assert len(wiki_files) >= 3, f"wiki 期望 3+,实际 {len(wiki_files)}"


def test_real_size_above_5000():
    """真实 raw 应大于 5000 字节(模板 < 2000)"""
    for f in (WIKI_ROOT / "raw_clips").glob("sample_S*.md"):
        assert f.stat().st_size >= 5000, f"{f.name} 仅 {f.stat().st_size} 字节,可能是模板"


def test_quality_guard_pass():
    """所有 wiki 应通过 quality_guard"""
    for f in (WIKI_ROOT / "wiki").glob("wiki_S*.md"):
        content = f.read_text(encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(GUARD), "--check", content],
            capture_output=True, text=True, timeout=10
        )
        assert result.returncode == 0, f"{f.name} 未通过 quality_guard"


def test_real_wikipedia_url():
    """每 raw 应含真实 Wikipedia URL"""
    for f in (WIKI_ROOT / "raw_clips").glob("sample_S*.md"):
        content = f.read_text(encoding="utf-8")
        assert "en.wikipedia.org/wiki/" in content, f"{f.name} 缺真实 Wikipedia URL"


def test_citations_have_offset():
    """每 citation 应有 offset(真实溯源)"""
    cite_files = list((WIKI_ROOT / "citations").glob("cite_sample_S*.md"))
    assert len(cite_files) >= 50, f"citations 期望 50+,实际 {len(cite_files)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])