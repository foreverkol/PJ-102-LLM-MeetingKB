#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_pj_state.py - Sprint 25 L6 PJ 项目 STATE.json 初始化

王老师 2026-09-06 '全部执行 L6':
  - 给每个 PJ 项目自动生成 STATE.json(基础框架)
  - 让 24 个 PJ 项目都可以使用看板
  - 一键激活模式 v2.0

用法:
    python3 scripts/init_pj_state.py --list                # 列出未激活 PJ
    python3 scripts/init_pj_state.py --init PJ-XXX        # 初始化指定 PJ
    python3 scripts/init_pj_state.py --all [--dry-run]    # 全部初始化
    python3 scripts/init_pj_state.py --report             # 激活报告
"""
import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PJ_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目")
CODEX_BASE = Path("/mnt/d/BaiduSyncdisk/codex/01-项目")

cst = timezone(timedelta(hours=8))
NOW = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")


def find_inactive_pj() -> list:
    """找未激活的 PJ 项目(无 STATE.json 但有 scripts)"""
    inactive = []
    for base in [PJ_BASE, CODEX_BASE]:
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir() or not d.name.startswith("PJ"):
                continue
            scripts_dir = d / "scripts"
            has_scripts = scripts_dir.exists() and any(scripts_dir.glob("*.py"))
            has_state = (d / "STATE.json").exists()
            if has_scripts and not has_state:
                inactive.append(d)
    return inactive


def generate_state_json(pj_dir: Path) -> dict:
    """生成基础 STATE.json"""
    return {
        "version": "0.1.0-init",
        "tag": "无",
        "project_name": pj_dir.name,
        "current_sprint": "Sprint 1(初始)",
        "current_sprint_status": "模式 v2.0 v3.0 初始化",
        "last_updated": NOW,
        "created_by": "init_pj_state.py (PJ-102 推广)",
        "do_now": [
            f"1. {pj_dir.name} 初始化完成,可使用模式 v2.0 工具",
            "2. 编辑 STATE.json 添加项目特定信息",
            "3. python3 scripts/state_to_md.py  生成 STATE.md",
            "4. python3 scripts/build_web_dashboard.py  生成看板"
        ],
        "now": {
            "current_action": f"{pj_dir.name} 已接收 PJ-102 模式 v2.0 工具",
            "blocking": "(无)",
            "next_action_after_decision": "项目负责人编辑 STATE.json",
            "estimated_time": "5 分钟"
        },
        "completed_decisions": [
            {
                "id": "init",
                "title": f"{pj_dir.name} 接收模式 v2.0 工具(6 个脚本)",
                "completed_at": NOW,
                "source": "PJ-102 promote_v2_to_pj.py"
            }
        ],
        "pending_decisions": [],
        "checkpoint": None,
        "last_codex_review": {}
    }


def init_pj(pj_dir: Path, dry_run: bool = False) -> dict:
    """初始化单个 PJ"""
    target_state = pj_dir / "STATE.json"
    state_data = generate_state_json(pj_dir)

    if not dry_run:
        target_state.write_text(
            json.dumps(state_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

    return {
        "pj": pj_dir.name,
        "state_path": str(target_state),
        "dry_run": dry_run
    }


def main():
    parser = argparse.ArgumentParser(description="PJ 项目 STATE.json 初始化")
    parser.add_argument("--list", action="store_true", help="列出未激活 PJ")
    parser.add_argument("--init", help="初始化指定 PJ")
    parser.add_argument("--all", action="store_true", help="全部初始化")
    parser.add_argument("--dry-run", action="store_true", help="只显示不写")
    parser.add_argument("--report", action="store_true", help="激活报告")
    args = parser.parse_args()

    inactive = find_inactive_pj()

    if args.list:
        print(f"📊 未激活 PJ 项目:{len(inactive)}")
        for d in inactive:
            print(f"   ⚪ {d.name}")
        return

    if args.report or args.all:
        print(f"📊 PJ 激活报告:")
        print(f"   未激活(可初始化):{len(inactive)}")
        if args.all:
            print(f"\n🔄 初始化所有未激活 PJ...")
            for d in inactive:
                result = init_pj(d, dry_run=args.dry_run)
                print(f"   {'🔍' if args.dry_run else '✅'} {result['pj']}")
            print(f"\n🎉 {'预览' if args.dry_run else '已激活'} {len(inactive)} 个 PJ")
        return

    if args.init:
        target = None
        for d in inactive:
            if d.name.startswith(args.init):
                target = d
                break
        if not target:
            print(f"❌ 找不到 PJ: {args.init}")
            print(f"   候选:{[d.name for d in inactive]}")
            return

        result = init_pj(target, dry_run=args.dry_run)
        print(f"{'🔍 预览' if args.dry_run else '✅ 已激活'}: {result['pj']}")
        print(f"   STATE.json:{result['state_path']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()