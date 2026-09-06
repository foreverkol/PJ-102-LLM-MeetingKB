#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
codex_review.py - Codex CLI 评审统一入口

王老师 2026-09-06 OUT-OF-BAND:
  "只需要 能用Codex CLI 只有评审可以调用 其他全部用hermes 内部处理"

架构原则:
  - Hermes 内部 = 写代码、写文档、写脚本、生成文件
  - Codex CLI = 只做评审/挑刺(读,不改)
  - 严格隔离:codex 不参与创作,只做质量门禁

用法:
    python3 scripts/codex_review.py              # 评审 HEAD
    python3 scripts/codex_review.py HEAD~3       # 评审最近 3 commit
    python3 scripts/codex_review.py --uncommitted # 评审未提交变更
    python3 scripts/codex_review.py --output file.md # 保存评审结果
"""
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
cst = timezone(timedelta(hours=8))


def run_review(target: str, output: str = None) -> tuple:
    """跑 Codex review(只读,不改)"""
    if target == "--uncommitted":
        cmd = ["codex", "review", "--uncommitted"]
    else:
        cmd = ["codex", "review", "--commit", target]

    print(f"🔍 Codex review: {' '.join(cmd)}")
    print(f"   cwd: {PROJECT_ROOT}")
    print(f"   模式: read-only(只评审,不改)")
    print()

    start = datetime.now(cst)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=300,
            cwd=str(PROJECT_ROOT)
        )
        elapsed = (datetime.now(cst) - start).seconds
        print(f"⏱  耗时:{elapsed}s")
        print(f"📊 退出码:{result.returncode}")
        if output:
            output_path = Path(output)
            output_path.write_text(
                f"# Codex Review\n\n"
                f"- **目标**:{target}\n"
                f"- **时间**:{datetime.now(cst).strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"- **耗时**:{elapsed}s\n\n"
                f"## STDOUT\n\n```\n{result.stdout}\n```\n\n"
                f"## STDERR\n\n```\n{result.stderr}\n```\n",
                encoding="utf-8"
            )
            print(f"💾 结果已保存:{output}")
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("❌ Codex review 超时(300s)")
        return -1, "", "timeout"


def main():
    parser = argparse.ArgumentParser(
        description="Codex CLI 评审(只读,不改)"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="HEAD",
        help="评审目标:HEAD / HEAD~N / commit SHA / --uncommitted"
    )
    parser.add_argument(
        "--output", "-o",
        help="保存评审结果到文件"
    )
    args = parser.parse_args()

    print("━" * 70)
    print("🔨 Codex Review (王老师架构原则: 只有评审用 Codex, 其他 Hermes)")
    print("━" * 70)

    rc, stdout, stderr = run_review(args.target, args.output)

    print()
    print("━" * 70)
    print("📋 Codex 输出 (前 3000 字符):")
    print("━" * 70)
    if stdout:
        print(stdout[:3000])
    if stderr and stderr.strip():
        print("\n[STDERR]:")
        print(stderr[:500])

    sys.exit(rc)


if __name__ == "__main__":
    main()