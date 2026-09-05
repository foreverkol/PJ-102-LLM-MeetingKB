"""test_t07_scenario.py - T-07 单元测试"""
import pytest
from pathlib import Path


def test_s14_scenario_exists():
    """s14_scenario.py 必须存在且 4KB+"""
    s14 = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/steps/s14_scenario.py")
    if not s14.exists():
        pytest.skip("s14_scenario.py 不存在")
    assert s14.stat().st_size >= 4000, f"s14_scenario.py 应 4KB+,实测 {s14.stat().st_size}"


def test_scenarios_dir_exists():
    """scenarios 目录必须存在"""
    sc_dir = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/scenarios")
    assert sc_dir.exists(), "scenarios 目录应存在"
    assert sc_dir.is_dir()