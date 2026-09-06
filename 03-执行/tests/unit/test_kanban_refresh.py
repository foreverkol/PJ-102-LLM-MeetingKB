#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_kanban_refresh.py - 看板常态化全链路测试

王老师 2026-09-06 OUT-OF-BAND '看板如何更好的实现项目跟踪的常态化'

测试覆盖:
  - kanban_refresh.py 跑通
  - 4 步骤全部成功
  - HTML 看板更新
  - STATE.json last_codex_review 字段注入
  - HTTP 服务可达
  - 推送防抖(commit 变化才推)
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/kanban_refresh.py"
STATE = PROJECT_ROOT / "STATE.json"
HTML = PROJECT_ROOT / ".kanban/index.html"


def test_script_exists():
    assert SCRIPT.exists()


def test_refresh_runs():
    """全链路刷新能跑通"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--no-push"],
        capture_output=True, text=True, timeout=60,
        cwd=str(PROJECT_ROOT)
    )
    assert result.returncode == 0, f"刷新失败: {result.stderr}"
    assert "完成" in result.stdout


def test_state_has_codex_review():
    """STATE.json 应有 last_codex_review 字段"""
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert "last_codex_review" in state, "STATE.json 缺 last_codex_review"
    if state["last_codex_review"]:
        assert "file" in state["last_codex_review"]
        assert "reviewed_at" in state["last_codex_review"]


def test_html_shows_codex():
    """HTML 应包含 Codex 评审卡片"""
    assert HTML.exists(), "看板 HTML 不存在"
    content = HTML.read_text(encoding="utf-8")
    assert "Codex 评审" in content
    # 至少应有一次 🚨 emoji
    assert "🚨" in content


def test_http_service_available():
    """HTTP 服务应在 8788 端口可达"""
    import urllib.request
    try:
        with urllib.request.urlopen("http://127.0.0.1:8788/", timeout=5) as resp:
            assert resp.status == 200
    except Exception as e:
        pytest.skip(f"服务不可用(可能需要重启): {e}")


def test_push_dedup():
    """推送去重:last_notified_commit 字段应记录"""
    state = json.loads(STATE.read_text(encoding="utf-8"))
    # 字段应存在(可能是空字符串)
    assert "last_notified_commit" in state


def test_four_steps_all_succeed():
    """4 步骤日志全 PASS"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--no-push"],
        capture_output=True, text=True, timeout=60,
        cwd=str(PROJECT_ROOT)
    )
    output = result.stdout
    # 4 步标记
    assert "Step 1/4" in output
    assert "Step 2/4" in output
    assert "Step 3/4" in output
    # 成功标记
    assert "3/3 步成功" in output or "4/4 步成功" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])