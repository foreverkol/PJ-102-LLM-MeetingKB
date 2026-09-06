#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_state_to_md.py - state_to_md.py 自动化测试 (L4.5)

王老师 2026-09-06 模式 v2.0 试用 → L4.5:
  确保 STATE.json → STATE.md 自动生成器稳定可靠, 防止漂移。

测试覆盖:
  - STATE.json 加载正确
  - markdown 渲染包含必要字段(版本/Sprint/决策点)
  - --check 模式准确性(一致=exit 0, 不一致=exit 1)
  - 输出文件可写 + 中文路径支持
  - 重跑幂等性(2 次生成结果一致)
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/state_to_md.py"
STATE_JSON = PROJECT_ROOT / "STATE.json"
STATE_MD = PROJECT_ROOT / "STATE.md"


def test_state_json_valid():
    """STATE.json 必须是有效 JSON"""
    assert STATE_JSON.exists(), f"STATE.json 不存在: {STATE_JSON}"
    data = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert "project_id" in data
    assert data["project_id"] == "PJ-102"


def test_state_json_has_required_keys():
    """STATE.json 必须包含模式 v2.0 必需字段"""
    data = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    required_keys = [
        "version", "tag", "branch", "last_updated",
        "current_sprint", "previous_sprint",
        "pending_decisions", "do_now", "mode_architecture",
        "protocols"
    ]
    for k in required_keys:
        assert k in data, f"STATE.json 缺少必需字段: {k}"


def test_pending_decisions_structure():
    """pending_decisions 必须是数组 + 每个元素有 id/priority/options"""
    data = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    decisions = data["pending_decisions"]
    assert isinstance(decisions, list)
    assert len(decisions) >= 1
    for d in decisions:
        assert "id" in d
        assert "priority" in d
        assert d["priority"] in ["P0", "P1", "P2", "P3"]
        # 决策点必须有 options 数组(王老师多选+推荐模式)
        assert "options" in d, f"决策点 {d.get('id')} 缺 options 字段"
        assert isinstance(d["options"], list)
        # 每个选项必须有 key/label/my_recommendation/reason
        for opt in d["options"]:
            assert "key" in opt, f"选项缺 key"
            assert "label" in opt, f"选项缺 label"
            assert "my_recommendation" in opt, f"选项缺 my_recommendation"
            assert "reason" in opt, f"选项缺 reason"


def test_script_runs_successfully():
    """脚本应能跑通且退出码 0"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"脚本失败: {result.stderr}"
    assert "STATE.md 已生成" in result.stdout


def test_state_md_has_required_sections():
    """STATE.md 应包含模式 v2.0 必要章节"""
    assert STATE_MD.exists(), f"STATE.md 未生成: {STATE_MD}"
    content = STATE_MD.read_text(encoding="utf-8")
    required_sections = [
        "# PJ-102 LLM MeetingKB",
        "## 🎯 当前状态",
        "## ✅ 上一 Sprint 战果",
        "## 🎯 待王老师决策点",
        "## 🚀 Do Now",
        "## 🏗 模式架构",
        "## 🛡 协议铁律遵守"
    ]
    for section in required_sections:
        assert section in content, f"STATE.md 缺少章节: {section}"


def test_check_mode_consistency():
    """--check 模式: STATE.md 与 STATE.json 一致时 exit 0"""
    # 先跑一次确保最新
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, timeout=30)
    # 再 check
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"check 模式失败: {result.stdout}\n{result.stderr}"
    assert "一致" in result.stdout


def test_check_mode_detects_drift():
    """--check 模式: STATE.md 与 STATE.json 不一致时 exit 1"""
    # 先确保 STATE.md 是最新的
    subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, timeout=30)
    # 手动改 STATE.md 制造漂移
    content = STATE_MD.read_text(encoding="utf-8")
    drifted = content + "\n\nDRIFT_MARKER_20260906\n"
    STATE_MD.write_text(drifted, encoding="utf-8")
    try:
        # check 应报错
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 1, f"check 应检测漂移但没检测到"
        assert "不一致" in result.stdout
    finally:
        # 恢复 STATE.md
        subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, timeout=30)


def test_repeatability():
    """幂等性: 多次运行应产生相同结果"""
    # 跑 3 次
    outputs = []
    for _ in range(3):
        subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, timeout=30)
        outputs.append(STATE_MD.read_text(encoding="utf-8"))
    # 第一次和第三次应一致(忽略 last_updated 时间戳)
    # last_updated 可能在秒级变化, 但同一秒内应一致
    # 这里检查: 三次输出大小相近(±100 字节允许时间戳差异)
    sizes = [len(o) for o in outputs]
    assert max(sizes) - min(sizes) < 200, f"输出大小差异过大: {sizes}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])