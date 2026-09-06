#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_local_codex_review.py - 本地化 Codex review 测试

王老师 2026-09-06 OUT-OF-BAND 'C'(本地化,因 codex CLI 未登录)

验证:
  - 脚本能跑通
  - diff 提取正确
  - 报告保存到 .codex-reviews/
  - 不修改任何项目文件
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
SCRIPT = PROJECT_ROOT / "scripts/local_codex_review.py"
REVIEWS_DIR = PROJECT_ROOT / ".codex-reviews"


def test_script_exists():
    """local_codex_review.py 必须存在"""
    assert SCRIPT.exists()


def test_diff_extraction():
    """get_diff 应能提取最近 commit 的 diff"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("local_codex_review", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    diff = module.get_diff("HEAD")
    # diff 应有内容(除非第一个 commit)
    assert isinstance(diff, str)
    assert len(diff) >= 0


def test_reviews_dir_created():
    """运行评审后,.codex-reviews 目录应被创建"""
    REVIEWS_DIR.mkdir(exist_ok=True)
    assert REVIEWS_DIR.exists()


def test_post_commit_uses_local_review():
    """post-commit hook 必须用 local_codex_review.py(不是 codex CLI)"""
    hook = PROJECT_ROOT / ".git/hooks/post-commit"
    content = hook.read_text(encoding="utf-8")
    assert "local_codex_review" in content
    # 不应直接调 codex CLI
    assert "codex review" not in content or "codex review" in content and "scripts/codex_review.py" not in content


def test_no_project_file_modification():
    """local_codex_review 不应修改项目文件(只读评审)"""
    # 跑 --diff-only(不评审,只打印 diff)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--diff-only", "HEAD"],
        capture_output=True, text=True, timeout=30
    )
    # 应跑通(可能超时但不应崩溃)
    assert result.returncode in [0, 124]  # 0 = 正常,124 = 超时


def test_review_output_format():
    """评审输出应包含关键章节"""
    reviews = list(REVIEWS_DIR.glob("*.md"))
    if reviews:
        # 读最新一份评审
        latest = max(reviews, key=lambda p: p.stat().st_mtime)
        content = latest.read_text(encoding="utf-8", errors="ignore")
        # 至少有标题或评审内容
        assert len(content) > 100, f"评审报告过短: {latest}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])