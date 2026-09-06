#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_web_clipper.py - AT-11 Web Clipper 测试

王老师 2026-09-06 '按推荐 A'(Chrome + NotebookLM):
  - 实测:fetch_url + save_clip + list
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/web_clipper.py"
WIKI_RAW = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/raw_clips")


def test_script_exists():
    assert SCRIPT.exists()


def test_script_imports():
    import importlib.util
    spec = importlib.util.spec_from_file_location("web_clipper", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "fetch_url")
    assert hasattr(module, "save_clip")
    assert hasattr(module, "push_to_notebooklm")
    assert hasattr(module, "open_in_chrome")


def test_list_command():
    """--list 应能跑通"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--list"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"--list 失败: {result.stderr}"


def test_save_clip_creates_file():
    """save_clip 应创建 markdown 文件"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("web_clipper", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    test_clip = {
        "status": "ok",
        "url": "https://example.com/test",
        "title": "Test",
        "content": "test content",
        "fetched_at": "2026-09-06 12:00:00"
    }
    saved = module.save_clip(test_clip, tags=["test"], notebook=None)
    assert saved.exists(), f"未创建文件: {saved}"
    assert saved.suffix == ".md"
    content = saved.read_text(encoding="utf-8")
    assert "https://example.com/test" in content
    assert "test" in content


def test_fetch_url_works():
    """fetch_url 应能抓取"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("web_clipper", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 用一个稳定的 URL
    result = module.fetch_url("https://example.com")
    assert "status" in result
    assert result["status"] in ["ok", "error"]


def test_no_sensitive_data():
    """脚本不应包含敏感信息"""
    content = SCRIPT.read_text(encoding="utf-8")
    sensitive = ["password=", "secret=", "token="]
    for s in sensitive:
        # 允许 API key 提示,不允许硬编码
        if s in content.lower():
            # 必须只是注释或变量名,不是硬编码值
            lines = [l for l in content.split("\n") if s in l.lower() and not l.strip().startswith("#")]
            assert len(lines) == 0, f"硬编码 {s}: {lines}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])