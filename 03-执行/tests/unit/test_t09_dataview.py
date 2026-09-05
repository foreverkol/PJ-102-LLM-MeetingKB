"""test_t09_dataview.py - T-09 单元测试
A4 修复后:支持多种字段
"""
import pytest
from pathlib import Path


def test_dataview_total():
    """dataview 块总数 >= 400 (A4 修复后)"""
    wiki = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
    total = 0
    for etype in ["meetings", "persons", "concepts", "judgments"]:
        d = wiki / etype
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            total += content.count("```dataview")
    assert total >= 400, f"应有 400+ dataview 块,实测 {total}"


def test_meetings_have_dataview():
    """A4 修复:meetings 应该有 dataview"""
    meetings = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings")
    if not meetings.exists():
        pytest.skip("meetings 目录不存在")
    with_dv = 0
    for f in meetings.glob("*.md"):
        if "```dataview" in f.read_text(encoding='utf-8'):
            with_dv += 1
    assert with_dv >= 15, f"meetings 应 15+ 有 dataview,实测 {with_dv}"