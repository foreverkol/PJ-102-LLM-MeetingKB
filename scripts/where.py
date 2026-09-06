#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
where.py - PJ-102 "我在哪、下一步是什么" 统一推进脚本

王老师 2026-09-06 OUT-OF-BAND:
  "项目的目标迭代工程流程计划怎么执行 执行到哪一步 现在都不明确 比较混乱"
  "最好利用 hermes 看板kanban 结合 Superpower深度应用 给出更好更成熟 更专业体验"

设计原则:
  - 一键显示:王老师只输入 `python3 scripts/where.py` 就看到全部状态
  - 3 屏看完:位置(屏1) + 决策点(屏2) + 怎么推进(屏3)
  - 不需要 JSON 解析技能,纯文本输出
  - 集成 git log + STATE.json + Hermes CLI Kanban

用法:
    python3 scripts/where.py                # 完整输出(3 屏)
    python3 scripts/where.py --brief        # 只看第 1 屏(一句话位置)
    python3 scripts/where.py --next         # 只看下一步具体动作
    python3 scripts/where.py --kanban       # 同步到 Hermes CLI Kanban
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

cst = timezone(timedelta(hours=8))


def load_state() -> dict:
    project_root = Path(__file__).parent.parent
    state_file = project_root / "STATE.json"
    if not state_file.exists():
        print(f"❌ STATE.json 不存在:{state_file}")
        sys.exit(1)
    return json.loads(state_file.read_text(encoding="utf-8"))


def git_log(n: int = 5) -> list:
    """git log -n --oneline"""
    project_root = Path(__file__).parent.parent
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "log", f"-{n}", "--oneline"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
    except:
        pass
    return []


def git_status() -> str:
    project_root = Path(__file__).parent.parent
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "status", "-sb"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            return lines[0] if lines else "(无)"
    except:
        pass
    return "(无法获取)"


def screen_one(state: dict) -> str:
    """屏 1:我现在在哪 - 一句话 + 5 行"""
    version = state.get("version", "?")
    sprint = state.get("current_sprint", "?")
    status = state.get("current_sprint_status", "?")
    branch = state.get("branch", "?")
    ahead = state.get("ahead_of_main", "?")
    last = state.get("last_commit", {})
    last_hash = last.get("hash", "?")[:8]
    last_subj = last.get("subject", "?")[:50]

    completed = len(state.get("completed_decisions", []))
    pending = len(state.get("pending_decisions", []))
    do_now = state.get("do_now", [])

    lines = []
    lines.append("━" * 70)
    lines.append(f"📍 PJ-102 当前位置(一句话)")
    lines.append(f"   v{version} | {sprint} | {status}")
    lines.append("━" * 70)
    lines.append("")
    lines.append(f"🌿 分支:{branch}(ahead of main {ahead} commits)")
    lines.append(f"📝 最后 commit:{last_hash} {last_subj}")
    lines.append(f"✅ 本 Sprint 已闭环:{completed} 项")
    lines.append(f"⏸️  待决策点:{pending} 项")
    lines.append(f"🎯 当前唯一动作:{do_now[0] if do_now else '(无)'}")
    lines.append("")
    lines.append(f"💡 看全部:python3 scripts/where.py")
    lines.append(f"💡 看下一步:python3 scripts/where.py --next")
    lines.append(f"💡 同步看板:python3 scripts/where.py --kanban")
    lines.append("")
    return "\n".join(lines)


def screen_two(state: dict) -> str:
    """屏 2:5 决策点状态"""
    lines = []
    lines.append("━" * 70)
    lines.append(f"📋 决策点状态({len(state.get('pending_decisions', []))} 项)")
    lines.append("━" * 70)
    lines.append("")
    for d in state.get("pending_decisions", []):
        pid = d["id"]
        prio = d["priority"]
        title = d["title"][:30]
        # 找推荐选项(⭐ 强烈推荐 > ✅ 推荐,跳过 👎/⚠️)
        recommended = ""
        for opt in d.get("options", []):
            rec = opt.get("my_recommendation", "")
            if "强烈推荐" in rec or "推荐" in rec and "不推荐" not in rec and "👎" not in rec:
                recommended = f"{opt['key']}({rec})"
                break
        risk = d.get("risk", "?")

        # 风险 emoji
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk, "⚪")

        lines.append(f"{risk_emoji} [{prio}] {pid}:{title}")
        lines.append(f"   状态:{d.get('current_status', '?')[:40]}")
        if recommended:
            lines.append(f"   推荐:{recommended}")
        if d.get("options"):
            lines.append(f"   选项:{', '.join(o['key'] for o in d['options'])}")
        lines.append("")

    return "\n".join(lines)


def screen_three(state: dict) -> str:
    """屏 3:git 状态 + 已完成 + 执行步骤"""
    lines = []
    lines.append("━" * 70)
    lines.append(f"🛠 执行详情")
    lines.append("━" * 70)
    lines.append("")
    lines.append(f"分支状态:{git_status()}")
    lines.append("")
    lines.append("最近 commits:")
    for line in git_log(5):
        lines.append(f"  {line}")
    lines.append("")
    if state.get("completed_decisions"):
        lines.append("✅ 已闭环:")
        for c in state["completed_decisions"]:
            lines.append(f"   - {c.get('id', '?')}:{c.get('title', '?')[:50]}")
        lines.append("")
    lines.append("📍 王老师 5 决策点当前状态(quick reference):")
    lines.append("   DT-01 75 relationship ⏸ 等批 12/75 自动填 + 63 待批")
    lines.append("   AT-11 Web Clipper    ⏸ 等浏览器+API")
    lines.append("   CT-13B atomicstrata  🔄 npm 封装阶段 B 完成")
    lines.append("   ET-04 organization   ⚪ 等 PJ-201 数据")
    lines.append("   BT-14 三层架构       ⚪ Sprint 23+ 评估")
    return "\n".join(lines)


def screen_brief(state: dict) -> str:
    """brief 模式:只输出一句话位置"""
    version = state.get("version", "?")
    sprint = state.get("current_sprint", "?")
    status = state.get("current_sprint_status", "?")
    do_now = state.get("do_now", ["(无)"])[0]
    return f"📍 v{version} | {sprint} | {status} | 🎯 {do_now}"


def screen_next(state: dict) -> str:
    """next 模式:下一步具体动作"""
    lines = []
    lines.append("━" * 70)
    lines.append("🎯 下一步动作(具体到可执行)")
    lines.append("━" * 70)
    lines.append("")
    for i, action in enumerate(state.get("do_now", []), 1):
        lines.append(f"  {i}. {action}")
    lines.append("")
    lines.append("💡 等王老师触发后,告诉我具体选项,我立即执行")
    return "\n".join(lines)


def sync_to_kanban(state: dict):
    """同步 STATE.json 到 Hermes CLI Kanban"""
    project_root = Path(__file__).parent.parent

    # 创建 PJ-102 board(如果不存在)
    print("🔧 同步到 Hermes Kanban...")
    try:
        subprocess.run(
            ["hermes", "kanban", "boards", "create", "pj102-llm-meetingkb",
             "--name", "PJ-102 LLM MeetingKB",
             "--description", state.get("current_sprint_status", "Sprint 22 推进"),
             "--icon", "📚"],
            capture_output=True, text=True, timeout=30
        )
        subprocess.run(
            ["hermes", "kanban", "boards", "switch", "pj102-llm-meetingkb"],
            capture_output=True, text=True, timeout=30
        )
    except:
        pass

    # 列出当前 board 的 tasks
    result = subprocess.run(
        ["hermes", "kanban", "ls"],
        capture_output=True, text=True, timeout=30
    )
    print(f"\n📋 Hermes Kanban 当前状态:")
    print(result.stdout)

    # 显示决策点对应说明
    print("\n🎯 5 决策点 → 建议 Kanban 任务:")
    for d in state.get("pending_decisions", []):
        print(f"  - [{d['priority']}] {d['id']}:{d['title'][:30]}")
        print(f"    阻塞:{d['blocker'][:50]}")


def main():
    parser = argparse.ArgumentParser(
        description="PJ-102 统一推进面板"
    )
    parser.add_argument("--brief", action="store_true", help="只输出一句话位置")
    parser.add_argument("--next", action="store_true", help="只看下一步")
    parser.add_argument("--kanban", action="store_true", help="同步到 Hermes Kanban")
    args = parser.parse_args()

    state = load_state()

    if args.brief:
        print(screen_brief(state))
    elif args.next:
        print(screen_next(state))
    elif args.kanban:
        sync_to_kanban(state)
    else:
        # 默认:3 屏全部
        print(screen_one(state))
        print()
        print(screen_two(state))
        print()
        print(screen_three(state))


if __name__ == "__main__":
    main()