#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_tier_classifier.py - BT-14 三层架构 tier 分类器测试"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/tier_classifier.py"
WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")


def test_script_exists():
    assert SCRIPT.exists()


def test_script_imports():
    import importlib.util
    spec = importlib.util.spec_from_file_location("tier_classifier", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "scan_files")
    assert hasattr(module, "infer_tier")
    assert hasattr(module, "add_tier_frontmatter")
    assert hasattr(module, "report")


def test_infer_tier():
    """物理目录 → tier 推断应正确"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("tier_classifier", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.infer_tier(WIKI_ROOT / "raw_clips/clip_xyz.md") == "raw"
    assert module.infer_tier(WIKI_ROOT / "judgments/judgment_xyz.md") == "citations"
    assert module.infer_tier(WIKI_ROOT / "persons/person_xyz.md") == "wiki"
    assert module.infer_tier(WIKI_ROOT / "CLAUDE.md") == "unknown"


def test_scan_runs():
    """scan 命令应能跑通"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "scan"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    assert "扫描" in result.stdout


def test_report_structure():
    """report 应返回结构化数据"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "report"],
        capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0
    import json
    data = json.loads(result.stdout)
    assert "total" in data
    assert "by_tier" in data
    assert "raw" in data["by_tier"]
    assert "citations" in data["by_tier"]
    assert "wiki" in data["by_tier"]
    # 至少 300 个文件
    assert data["total"] >= 300


def test_three_tier_separation():
    """三层应清晰分离,无重叠"""
    import json
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "report"],
        capture_output=True, text=True, timeout=60
    )
    data = json.loads(result.stdout)
    by_tier = data["by_tier"]
    # 三个 tier 都有文件
    assert by_tier["raw"] > 0, "raw 层应有文件(Web Clipper)"
    assert by_tier["citations"] > 50, f"citations 层应有 >50 文件, 实际 {by_tier['citations']}"
    assert by_tier["wiki"] > 200, f"wiki 层应有 >200 文件, 实际 {by_tier['wiki']}"


def test_add_tier_frontmatter_idempotent():
    """add_tier_frontmatter 应幂等(已设置不重复)"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("tier_classifier", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 找一个 citations 文件
    j_file = next(WIKI_ROOT.glob("judgments/*.md"), None)
    if j_file is None:
        pytest.skip("无 judgments 文件")

    # 第一次设置
    success1 = module.add_tier_frontmatter(j_file, "citations")
    # 第二次设置相同 tier
    success2 = module.add_tier_frontmatter(j_file, "citations")

    # 第一次应成功,第二次应跳过
    assert success1 is True
    assert success2 is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])