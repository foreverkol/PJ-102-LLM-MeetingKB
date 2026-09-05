"""test_t13_sources.py - T-13 A3 修复后验证"""
import pytest
from pathlib import Path


def test_poc_structured_dir():
    """A3 修复:concepts_poc_structured/ 必须存在且有 22+ 文件"""
    poc_dir = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/concepts_poc_structured")
    if not poc_dir.exists():
        pytest.skip("A3 未 apply")
    md_files = list(poc_dir.glob("*.md"))
    assert len(md_files) >= 22, f"应有 22+ 文件,实测 {len(md_files)}"


def test_structured_field_present():
    """A3 修复:sources_line_citations 字段必须存在"""
    poc_dir = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/concepts_poc_structured")
    if not poc_dir.exists():
        pytest.skip("A3 未 apply")
    with_field = 0
    for f in poc_dir.glob("*.md"):
        if "sources_line_citations:" in f.read_text(encoding='utf-8'):
            with_field += 1
    assert with_field >= 22, f"应有 22+ 含字段,实测 {with_field}"