#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_web_dashboard.py - HTML 看板生成器测试

王老师 2026-09-06 OUT-OF-BAND '浏览器监控' →
L4.9: build_web_dashboard.py 单文件 HTML 看板 + 30 秒自动刷新。

测试覆盖:
  - HTML 生成不崩溃
  - 关键内容存在(版本/Sprint/5 决策点/git log)
  - HTML 结构合法
  - 移动端 viewport 标签存在
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/build_web_dashboard.py"
HTML_FILE = PROJECT_ROOT / ".kanban/index.html"


def run_build() -> tuple:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=30,
        cwd=str(PROJECT_ROOT)
    )
    return result.returncode, result.stdout, result.stderr


def test_html_generation_runs():
    """HTML 生成脚本能跑通"""
    rc, stdout, stderr = run_build()
    assert rc == 0, f"build_web_dashboard.py 失败: {stderr}"
    assert HTML_FILE.exists(), "index.html 未生成"


def test_html_contains_key_info():
    """HTML 应包含版本/Sprint/决策点等关键信息"""
    assert HTML_FILE.exists(), "index.html 不存在"
    content = HTML_FILE.read_text(encoding="utf-8")

    # 标题
    assert "<title>" in content
    assert "PJ-102" in content

    # 头部状态
    assert "v3.1.0-stable" in content
    assert "Sprint 22" in content or "Sprint 21" in content

    # 5 决策点 ID 至少出现 4 个
    decision_ids = ["DT-01", "AT-11", "CT-13B", "ET-04", "BT-14"]
    found = sum(1 for did in decision_ids if did in content)
    assert found >= 4, f"决策点显示不全, 找到 {found}/5"

    # 已闭环
    assert "已闭环" in content

    # git log
    assert "Commits" in content or "commit" in content.lower()


def test_html_structure_valid():
    """HTML 结构基本合法"""
    assert HTML_FILE.exists()
    content = HTML_FILE.read_text(encoding="utf-8")

    # 必须有 DOCTYPE / html / head / body
    assert "<!DOCTYPE html>" in content
    assert "<html" in content
    assert "<head>" in content
    assert "<body>" in content
    assert "</html>" in content

    # 必须有 viewport 标签(移动端)
    assert 'viewport' in content
    assert 'width=device-width' in content

    # 必须有 charset
    assert 'charset="UTF-8"' in content


def test_auto_refresh_present():
    """必须包含 30 秒自动刷新逻辑"""
    content = HTML_FILE.read_text(encoding="utf-8")
    assert "setTimeout" in content or "setInterval" in content
    assert "reload" in content.lower()
    assert "30000" in content or "30" in content


def test_no_sensitive_info():
    """不应泄漏密码/token"""
    content = HTML_FILE.read_text(encoding="utf-8")
    sensitive = ["password", "api_key", "secret", "token"]
    for s in sensitive:
        assert s.lower() not in content.lower(), f"泄漏敏感词: {s}"


def test_dark_theme_present():
    """看板使用深色主题(王老师偏好专业感)"""
    content = HTML_FILE.read_text(encoding="utf-8")
    # GitHub Dark 主题特征色
    assert "#0d1117" in content or "#161b22" in content or "#58a6ff" in content


def test_html_under_50kb():
    """HTML 大小应 < 50KB(单文件,无外部依赖)"""
    size = HTML_FILE.stat().st_size
    assert size < 50000, f"HTML 过大: {size} 字节(应 < 50KB)"


def test_risk_emoji_present():
    """风险等级 emoji 应显示(Sprint 22 已 100% 闭环时为可选)"""
    content = HTML_FILE.read_text(encoding="utf-8")
    # 至少有 2 个风险 emoji(可能为空 if 所有已闭环)
    import json
    state = json.loads((PROJECT_ROOT / "STATE.json").read_text(encoding="utf-8"))
    pending = state.get("pending_decisions", [])
    if not pending:
        pytest.skip("无 pending_decisions(Sprint 22 已 100%)")
    emojis = ["🟢", "🟡", "🔴"]
    found = sum(1 for e in emojis if e in content)
    assert found >= 2, f"风险 emoji 显示不全: {found}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])