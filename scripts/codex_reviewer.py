#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
codex_reviewer.py - L3 codex CLI 智能切换器

王老师 2026-09-06 '按推荐执行 L3':
  - 自动检测 codex CLI 是否登录
  - 已登录 → 调 codex review(真 Codex)
  - 未登录 → fallback 到 local_codex_review.py(MiniMax-M3 via codex-shim)

用法:
    python3 scripts/codex_reviewer.py HEAD           # 评审最新 commit
    python3 scripts/codex_reviewer.py <commit_sha>   # 评审指定 commit
    python3 scripts/codex_reviewer.py --status       # 查看当前模式
"""
import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CODEX_REVIEW_SCRIPT = PROJECT_ROOT / "scripts/codex_review.py"
LOCAL_REVIEW_SCRIPT = PROJECT_ROOT / "scripts/local_codex_review.py"


def check_codex_login() -> bool:
    """检查 codex CLI 是否已登录"""
    try:
        result = subprocess.run(
            ["codex", "login", "status"],
            capture_output=True, text=True, timeout=10
        )
        return "logged in" in result.stdout.lower() and "not logged in" not in result.stdout.lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_current_mode() -> str:
    """获取当前评审模式"""
    if check_codex_login():
        return "codex_cli"
    return "local_minimax"


def run_codex_review(target: str) -> dict:
    """执行 codex review(已登录模式)"""
    print(f"🌐 使用 Codex CLI 真 Codex 评审: {target}")
    result = subprocess.run(
        ["python3", str(CODEX_REVIEW_SCRIPT), target],
        capture_output=True, text=True, timeout=300
    )
    return {
        "mode": "codex_cli",
        "returncode": result.returncode,
        "stdout": result.stdout[:2000],
        "stderr": result.stderr[:500]
    }


def run_local_review(target: str) -> dict:
    """执行 local review(fallback 模式)"""
    print(f"🔄 使用本地 MiniMax-M3 评审(fallback): {target}")
    result = subprocess.run(
        ["python3", str(LOCAL_REVIEW_SCRIPT), target],
        capture_output=True, text=True, timeout=180
    )
    return {
        "mode": "local_minimax",
        "returncode": result.returncode,
        "stdout": result.stdout[:2000],
        "stderr": result.stderr[:500]
    }


def main():
    parser = argparse.ArgumentParser(description="Codex 智能评审(自动切换)")
    parser.add_argument("target", nargs="?", help="评审目标(commit/branch)")
    parser.add_argument("--status", action="store_true", help="查看当前模式")
    args = parser.parse_args()

    mode = get_current_mode()

    if args.status:
        print(f"📊 当前评审模式: {mode}")
        if mode == "codex_cli":
            print(f"   ✅ Codex CLI 已登录")
        else:
            print(f"   ⚠️ Codex CLI 未登录,使用本地 fallback")
        return

    if not args.target:
        print("用法: codex_reviewer.py <target> [--status]")
        sys.exit(1)

    # 自动选择评审模式
    if mode == "codex_cli":
        result = run_codex_review(args.target)
    else:
        result = run_local_review(args.target)

    print(f"\n{'='*60}")
    print(f"模式: {result['mode']}")
    print(f"返回码: {result['returncode']}")
    print(f"\n输出片段:")
    print(result['stdout'][:1500])
    if result['stderr']:
        print(f"\n错误:")
        print(result['stderr'])


if __name__ == "__main__":
    main()