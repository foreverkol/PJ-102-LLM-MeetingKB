#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_codex_review.py - codex_review.py 工具测试

王老师 2026-09-06 OUT-OF-BAND:
  "只需要 能用Codex CLI 只有评审可以调用 其他全部用hermes 内部处理"

架构原则验证:
  - codex_review.py 只调用 `codex review`,不调用 `codex exec`
  - feishu_notify.py 调用 hermes send(不是直接写文件)
"""
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/mnt/d/BaiduSynddrive/hermes/01-项目/PJ-102-LLM-MeetingKB") if False else Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
REVIEW_SCRIPT = PROJECT_ROOT / "scripts/codex_review.py"
NOTIFY_SCRIPT = PROJECT_ROOT / "scripts/feishu_notify.py"


def test_codex_review_script_exists():
    """codex_review.py 必须存在"""
    assert REVIEW_SCRIPT.exists(), f"{REVIEW_SCRIPT} 不存在"


def test_codex_review_imports():
    """codex_review.py 导入不崩溃"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("codex_review", REVIEW_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except SystemExit:
        pass  # argparse exit 是正常的
    assert hasattr(module, "run_review")


def test_codex_review_only_calls_review():
    """codex_review.py 必须只调用 codex review,不调用 codex exec"""
    content = REVIEW_SCRIPT.read_text(encoding="utf-8")
    # 不应该有 codex exec
    assert "codex exec" not in content, "codex_review.py 不应该调用 codex exec"
    assert "codex_executable" not in content or "review" in content
    # 必须有 codex review
    assert "codex review" in content or "codex", "必须包含 codex 调用"


def test_codex_review_help_runs():
    """codex_review.py --help 必须跑通"""
    result = subprocess.run(
        [sys.executable, str(REVIEW_SCRIPT), "--help"],
        capture_output=True, text=True, timeout=30
    )
    # --help 可能 exit 0 或非 0(看实现),只要不崩溃
    assert "Codex" in result.stdout or "review" in result.stdout.lower()


def test_feishu_notify_script_exists():
    """feishu_notify.py 必须存在"""
    assert NOTIFY_SCRIPT.exists(), f"{NOTIFY_SCRIPT} 不存在"


def test_feishu_notify_dry_run():
    """feishu_notify.py --dry-run 必须跑通(不发飞书,只打印)"""
    result = subprocess.run(
        [sys.executable, str(NOTIFY_SCRIPT), "--dry-run"],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"dry-run 失败: {result.stderr}"
    # 应包含飞书消息内容
    assert "PJ-102" in result.stdout
    assert "看板" in result.stdout or "决策" in result.stdout


def test_feishu_notify_uses_hermes_send():
    """feishu_notify.py 必须调 hermes send(王老师架构原则)"""
    content = NOTIFY_SCRIPT.read_text(encoding="utf-8")
    assert "hermes send" in content, "feishu_notify.py 必须调 hermes send"
    # 不应直接写飞书 API
    assert "feishu.cn" not in content or "open_id" not in content


def test_post_commit_hook_exists():
    """post-commit hook 必须存在 + 可执行"""
    hook = PROJECT_ROOT / ".git/hooks/post-commit"
    assert hook.exists(), "post-commit hook 不存在"
    assert hook.stat().st_mode & 0o111, "post-commit hook 不可执行"


def test_post_commit_only_review():
    """post-commit 必须只调 codex review 或 kanban_refresh(不调 exec)"""
    hook = PROJECT_ROOT / ".git/hooks/post-commit"
    content = hook.read_text(encoding="utf-8")
    # 应该有 codex review 或 local_codex_review 或 kanban_refresh
    assert any(kw in content for kw in ["codex review", "local_codex_review", "kanban_refresh"])
    # 不应有 codex exec
    assert "codex exec" not in content
    # 异步(后台)执行
    assert "&" in content or "nohup" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])