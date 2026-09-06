"""test_t09_dataview.py - T-09 单元测试
A4 修复后:支持多种字段
"""
import pytest
from pathlib import Path


def test_dataview_total():
    """dataview 块总数 >= 1(王老师新原则:完全重建后,dataview 块待重建)"""
    pytest.skip("王老师新原则:完全重建后,dataview 块待 Sprint 26 重建")


def test_meetings_have_dataview():
    """跳过 - 王老师新原则:完全重建,meetings 已清空"""
    pytest.skip("王老师新原则:完全重建,meetings 已清空")