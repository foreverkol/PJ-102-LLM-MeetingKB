#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
promote_v2_to_pj.py - L5 模式 v2.0 推广到其他 PJ 项目

王老师 2026-09-06 '按推荐执行 L5':
  - 把 where.py / state_to_md.py / build_web_dashboard.py 等工具复制到其他 PJ
  - 让其他 PJ 也用上"STATE.json 单一真值源 + 自动看板"

用法:
    python3 scripts/promote_v2_to_pj.py --list            # 列出所有候选 PJ
    python3 scripts/promote_v2_to_pj.py --promote PJ-XXX  # 复制到指定 PJ
    python3 scripts/promote_v2_to_pj.py --report          # 推广报告
"""
import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_SCRIPTS = [
    "where.py",
    "state_to_md.py",
    "sync_state.py",
    "build_web_dashboard.py",
    "feishu_notify.py",
    "kanban_refresh.py",
]

# 候选 PJ 项目根目录
PJ_BASE_DIR = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目")
CODEX_BASE_DIR = Path("/mnt/d/BaiduSyncdisk/codex/01-项目")


def find_pj_projects() -> list:
    """查找所有 PJ 项目"""
    pj_dirs = []

    for base in [PJ_BASE_DIR, CODEX_BASE_DIR]:
        if not base.exists():
            continue
        for d in base.iterdir():
            if d.is_dir() and (d.name.startswith("PJ-") or d.name.startswith("PJ")):
                pj_dirs.append(d)

    return sorted(pj_dirs)


def has_state_json(pj_dir: Path) -> bool:
    """检查 PJ 是否有 STATE.json"""
    return (pj_dir / "STATE.json").exists()


def has_scripts(pj_dir: Path) -> bool:
    """检查 PJ 是否有 scripts/ 目录"""
    scripts_dir = pj_dir / "scripts"
    return scripts_dir.exists() and any(scripts_dir.glob("*.py"))


def promote_to_pj(pj_dir: Path, dry_run: bool = False) -> dict:
    """推广模式 v2.0 工具到指定 PJ"""
    target_scripts = pj_dir / "scripts"
    target_scripts.mkdir(parents=True, exist_ok=True)

    copied = []
    skipped = []
    for script_name in SOURCE_SCRIPTS:
        source = PROJECT_ROOT / "scripts" / script_name
        target = target_scripts / script_name

        if not source.exists():
            skipped.append(f"{script_name}(源不存在)")
            continue

        if not dry_run:
            shutil.copy2(source, target)

        copied.append(script_name)

    return {
        "pj": pj_dir.name,
        "target": str(target_scripts),
        "copied": copied,
        "skipped": skipped,
        "dry_run": dry_run
    }


def main():
    parser = argparse.ArgumentParser(description="模式 v2.0 推广到其他 PJ")
    parser.add_argument("--list", action="store_true", help="列出候选 PJ")
    parser.add_argument("--promote", help="推广到指定 PJ")
    parser.add_argument("--dry-run", action="store_true", help="只显示不复制")
    parser.add_argument("--report", action="store_true", help="推广报告")
    parser.add_argument("--all", action="store_true", help="推广到所有 PJ")
    args = parser.parse_args()

    pj_dirs = find_pj_projects()

    if args.list:
        print(f"📊 发现 {len(pj_dirs)} 个 PJ 项目:")
        for d in pj_dirs:
            has_state = "✅" if has_state_json(d) else "❌"
            has_script = "✅" if has_scripts(d) else "❌"
            print(f"  {has_state} STATE.json / {has_script} scripts {d.name}")
        return

    if args.promote:
        target = None
        for d in pj_dirs:
            if d.name.startswith(args.promote):
                target = d
                break
        if not target:
            print(f"❌ 找不到 PJ: {args.promote}")
            print(f"   候选:{[d.name for d in pj_dirs]}")
            return

        result = promote_to_pj(target, dry_run=args.dry_run)
        print(f"{'🔍 预览' if args.dry_run else '✅ 已推广'}: {result['pj']}")
        print(f"   目标: {result['target']}")
        print(f"   复制: {result['copied']}")
        if result['skipped']:
            print(f"   跳过: {result['skipped']}")
        return

    if args.all:
        print(f"🔄 推广到所有 {len(pj_dirs)} 个 PJ 项目")
        for d in pj_dirs:
            if d.name.startswith("PJ-102"):  # 跳过自己
                print(f"   ⏭️ 跳过自身:{d.name}")
                continue
            result = promote_to_pj(d, dry_run=args.dry_run)
            print(f"   {'🔍' if args.dry_run else '✅'} {result['pj']}:{len(result['copied'])} 个脚本")
        return

    if args.report:
        pj_with_state = sum(1 for d in pj_dirs if has_state_json(d))
        pj_with_scripts = sum(1 for d in pj_dirs if has_scripts(d))
        print(f"📊 推广报告:")
        print(f"   总 PJ 数:{len(pj_dirs)}")
        print(f"   有 STATE.json:{pj_with_state}")
        print(f"   有 scripts/:{pj_with_scripts}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()