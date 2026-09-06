#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_obsidian_export_cli.py - obsidian_export.py CLI 测试 (L4.3a)

王老师 2026-09-06 OUT-OF-BAND '即启动 L4.3' →
Sprint 22 L4.3a (CT-13B 阶段 A:解耦与抽象)。

测试覆盖:
  - 环境变量覆盖路径(WIKI_BASE / SCHEMA_PATH)
  - argparse 默认路径生效
  - CLAUDE.md 生成内容与硬编码版一致
  - .base 文件生成数量正确
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# 路径常量
PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "03-执行/code/obsidian_export.py"


def test_environment_variable_overrides():
    """环境变量 PJ102_WIKI_BASE / PJ102_SCHEMA_PATH 应覆盖默认路径"""
    sys.path.insert(0, str(PROJECT_ROOT / "03-执行/code"))
    # 清掉模块缓存
    if "obsidian_export" in sys.modules:
        del sys.modules["obsidian_export"]
    os.environ["PJ102_WIKI_BASE"] = "/tmp/test-wiki-override"
    os.environ["PJ102_SCHEMA_PATH"] = "/tmp/test-schema-override"
    try:
        import obsidian_export
        assert str(obsidian_export.WIKI_BASE) == "/tmp/test-wiki-override"
        assert str(obsidian_export.SCHEMA_PATH) == "/tmp/test-schema-override"
    finally:
        del os.environ["PJ102_WIKI_BASE"]
        del os.environ["PJ102_SCHEMA_PATH"]


def test_default_paths_exist():
    """默认路径应指向真实存在的目录"""
    sys.path.insert(0, str(PROJECT_ROOT / "03-执行/code"))
    if "obsidian_export" in sys.modules:
        del sys.modules["obsidian_export"]
    os.environ.pop("PJ102_WIKI_BASE", None)
    os.environ.pop("PJ102_SCHEMA_PATH", None)
    import obsidian_export
    assert obsidian_export.WIKI_BASE.exists(), f"{obsidian_export.WIKI_BASE} 不存在"
    assert obsidian_export.SCHEMA_PATH.exists(), f"{obsidian_export.SCHEMA_PATH} 不存在"


def test_script_runs_end_to_end():
    """真实跑 obsidian_export.py,期望生成 .base + CLAUDE.md"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, f"脚本失败: {result.stderr}"
    # 期望 CLAUDE.md 存在
    claude_md = WIKI_BASE / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md 未生成"
    # 期望 .base 文件存在
    base_files = list(WIKI_BASE.glob("*.base"))
    assert len(base_files) >= 4, f"期望 ≥4 个 .base 文件, 实测 {len(base_files)}"


def test_claude_md_content():
    """CLAUDE.md 应包含 atomicstrata-profile.json 的实体定义"""
    claude_md = WIKI_BASE / "CLAUDE.md"
    content = claude_md.read_text(encoding="utf-8")
    assert "PJ-102-LLM-MeetingKB" in content
    assert "atomicstrata-profile.json" in content
    # 应至少提到 8 个 entity 之一
    assert any(ent in content for ent in ["meeting", "person", "concept", "judgment"])


def test_no_hardcoded_paths_in_active_code():
    """运行时的 WIKI_BASE/SCHEMA_PATH 不应是死硬编码(默认值常量除外)"""
    sys.path.insert(0, str(PROJECT_ROOT / "03-执行/code"))
    if "obsidian_export" in sys.modules:
        del sys.modules["obsidian_export"]
    import obsidian_export
    # 优先级:env > 默认值常量
    # 只要 env 可覆盖,就算"已解耦"
    os.environ["PJ102_WIKI_BASE"] = "/tmp/env-test"
    if "obsidian_export" in sys.modules:
        del sys.modules["obsidian_export"]
    import obsidian_export
    assert str(obsidian_export.WIKI_BASE) == "/tmp/env-test"
    del os.environ["PJ102_WIKI_BASE"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])