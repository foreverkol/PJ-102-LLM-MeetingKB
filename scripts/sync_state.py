#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_state.py - STATE.json 与 STATE.md 双向同步工具

王老师 2026-09-06 模式 v2.0 完整化 → L4.6:
  state_to_md.py 只单向(STATE.json → STATE.md),
  但实际工作流中王老师可能编辑 STATE.md 增加注释/章节。
  sync_state.py 提供双向同步能力:
    - --state-to-md: STATE.json → STATE.md (默认, 等价于 state_to_md.py)
    - --md-to-state: STATE.md → STATE.json (提取人工注释作为 completed_decisions)
    - --check: 一致性检查

用法:
    python3 scripts/sync_state.py                    # STATE.json → STATE.md
    python3 scripts/sync_state.py --md-to-state     # STATE.md → STATE.json(谨慎使用)
    python3 scripts/sync_state.py --check            # 一致性检查
    python3 scripts/sync_state.py --report           # 漂移报告

设计原则:
  - 默认单向(防止漂移)
  - 反向同步仅提取:STATE.md 的"## ✅ 已完成" / "## 📌 备注" 章节
  - 严禁覆盖 STATE.json 的核心字段(version/tag/Sprint/decision)
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

cst = timezone(timedelta(hours=8))


def state_to_md():
    """调用 state_to_md.py 的核心功能"""
    script = Path(__file__).parent / "state_to_md.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"❌ state_to_md.py 失败: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    print("✅ STATE.json → STATE.md 同步完成")


def md_to_state():
    """从 STATE.md 提取王老师人工注释,追加到 STATE.json"""
    project_root = Path(__file__).parent.parent
    state_json = project_root / "STATE.json"
    state_md = project_root / "STATE.md"

    if not state_md.exists():
        print(f"❌ STATE.md 不存在:{state_md}")
        sys.exit(1)

    state = json.loads(state_json.read_text(encoding="utf-8"))
    md_content = state_md.read_text(encoding="utf-8")

    # 提取"## ✅ 已完成"章节(王老师可能手工添加)
    completed_section = re.search(
        r"## ✅ 已完成(.*?)(?=^## |\Z)",
        md_content, re.MULTILINE | re.DOTALL
    )

    new_completed = []
    if completed_section:
        items = re.findall(
            r"^- (.+)$",
            completed_section.group(1),
            re.MULTILINE
        )
        for item in items:
            item = item.strip()
            if item and not item.startswith("王老师"):
                new_completed.append({
                    "title": item,
                    "extracted_from": "STATE.md",
                    "extracted_at": datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")
                })

    if new_completed:
        if "completed_decisions" not in state:
            state["completed_decisions"] = []
        state["completed_decisions"].extend(new_completed)
        state_json.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print(f"✅ 从 STATE.md 提取 {len(new_completed)} 项已完成")
        for c in new_completed:
            print(f"   - {c['title']}")
    else:
        print("⚠️  STATE.md 中未发现'## ✅ 已完成'章节或无项目")
        print("   如需人工添加, 格式:")
        print("   ## ✅ 已完成")
        print("   - 项目1")
        print("   - 项目2")


def check_consistency():
    """检查 STATE.json 与 STATE.md 一致性"""
    script = Path(__file__).parent / "state_to_md.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        capture_output=True, text=True, timeout=30
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    sys.exit(result.returncode)


def drift_report():
    """生成 STATE.json 与 STATE.md 漂移报告"""
    project_root = Path(__file__).parent.parent
    state_json = project_root / "STATE.json"
    state_md = project_root / "STATE.md"

    state = json.loads(state_json.read_text(encoding="utf-8"))

    print("=" * 75)
    print("STATE.json ↔ STATE.md 漂移报告")
    print("=" * 75)
    print()
    print(f"STATE.json last_updated: {state.get('last_updated', '?')}")
    print()

    # 检查 STATE.md 中的 last_updated 标记
    if state_md.exists():
        md_content = state_md.read_text(encoding="utf-8")
        md_match = re.search(
            r"\*\*生成时间\*\*:([0-9\-\-:\s\+]+)",
            md_content
        )
        if md_match:
            md_time = md_match.group(1).strip()
            print(f"STATE.md 生成时间: {md_time}")
            if state.get("last_updated") and md_time[:19] != state["last_updated"][:19]:
                print(f"⚠️  漂移:STATE.json 与 STATE.md 时间戳不一致")
            else:
                print(f"✅ 时间戳一致")

    # 检查决策点数量
    if state_md.exists():
        md_content = state_md.read_text(encoding="utf-8")
        md_decisions = len(re.findall(r"^\| P[0-3] \|", md_content, re.MULTILINE))
        json_decisions = len(state.get("pending_decisions", []))
        print(f"\n决策点数量:")
        print(f"  STATE.json pending_decisions: {json_decisions}")
        print(f"  STATE.md 表格行(估算): {md_decisions}")
        if md_decisions != json_decisions:
            print(f"⚠️  漂移:决策点数量不一致")


def main():
    parser = argparse.ArgumentParser(
        description="STATE.json ↔ STATE.md 双向同步工具"
    )
    parser.add_argument("--state-to-md", action="store_true",
                       help="STATE.json → STATE.md (默认)")
    parser.add_argument("--md-to-state", action="store_true",
                       help="STATE.md → STATE.json (谨慎使用)")
    parser.add_argument("--check", action="store_true",
                       help="一致性检查")
    parser.add_argument("--report", action="store_true",
                       help="漂移报告")
    args = parser.parse_args()

    if args.check:
        check_consistency()
    elif args.md_to_state:
        md_to_state()
    elif args.report:
        drift_report()
    else:
        # 默认 = --state-to-md
        state_to_md()


if __name__ == "__main__":
    main()