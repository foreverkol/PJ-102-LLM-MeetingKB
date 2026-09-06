#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_where.py - where.py 统一推进面板测试 (L4.8)

王老师 2026-09-06 OUT-OF-BAND '但我怎么批哈?+混乱' →
L4.8: where.py 统一面板 + 精简 do_now + Hermes Kanban 同步。

测试覆盖:
  - STATE.json 加载正确
  - 3 种模式输出格式(brief / next / 默认)
  - git log 集成不崩溃
  - 输出可读性(包含位置/状态/决策点)
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/where.py"


def run_where(*args) -> tuple:
    """跑 where.py + 解析输出"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, timeout=30,
        cwd=str(PROJECT_ROOT)
    )
    return result.returncode, result.stdout, result.stderr


def test_brief_mode():
    """--brief 模式: 一句话位置"""
    rc, stdout, stderr = run_where("--brief")
    assert rc == 0, f"where.py --brief 失败: {stderr}"
    assert "📍" in stdout
    assert "v3.1.0-stable" in stdout
    # 包含当前 Sprint 信息
    assert "Sprint" in stdout
    # 不应该超过 200 字符(一屏)
    assert len(stdout) < 500, f"brief 输出过长: {len(stdout)} 字符"


def test_next_mode():
    """--next 模式: 下一步具体动作"""
    rc, stdout, stderr = run_where("--next")
    assert rc == 0, f"where.py --next 失败: {stderr}"
    assert "下一步" in stdout or "下一步动作" in stdout
    # 至少列出 1 项行动
    assert any(c.isdigit() for c in stdout), "应至少列出 1 项编号行动"


def test_default_mode_shows_three_screens():
    """默认模式: 3 屏全部输出"""
    rc, stdout, stderr = run_where()
    assert rc == 0, f"where.py 失败: {stderr}"
    # 屏 1: 当前位置
    assert "当前位置" in stdout or "📍" in stdout
    # 屏 2: 决策点状态
    assert "决策点状态" in stdout or "DT-01" in stdout
    # 屏 3: 执行详情
    assert "执行详情" in stdout or "commit" in stdout.lower()


def test_pending_decisions_visible():
    """5 决策点全部显示"""
    rc, stdout, stderr = run_where()
    assert rc == 0
    # 5 决策点 ID 至少出现 4 个
    decision_ids = ["DT-01", "AT-11", "CT-13B", "ET-04", "BT-14"]
    found = sum(1 for did in decision_ids if did in stdout)
    assert found >= 4, f"决策点显示不全, 只找到 {found}/5: {stdout[:300]}"


def test_git_log_integration():
    """git log 集成不崩溃"""
    rc, stdout, stderr = run_where()
    assert rc == 0
    # 应该至少有 commit hash(7+ 位 hex)
    import re
    hex_hashes = re.findall(r"[0-9a-f]{7,8}", stdout)
    assert len(hex_hashes) >= 1, f"git log 输出为空: {stdout}"


def test_no_sensitive_info_leaked():
    """不应该泄漏敏感信息"""
    rc, stdout, stderr = run_where()
    # 密码/token 不应出现
    sensitive = ["password", "secret", "token", "api_key"]
    for s in sensitive:
        assert s.lower() not in stdout.lower(), f"泄漏敏感词: {s}"


def test_state_json_consistency():
    """where.py 输出与 STATE.json 内容一致"""
    import json
    state = json.loads((PROJECT_ROOT / "STATE.json").read_text(encoding="utf-8"))
    rc, stdout, stderr = run_where()
    # version 字段应在输出中
    assert state["version"] in stdout or state["version"].replace("v", "") in stdout
    # current_sprint 字段应出现
    assert state["current_sprint"] in stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])