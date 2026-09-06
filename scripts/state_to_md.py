#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
state_to_md.py - STATE.json → STATE.md 自动生成器

王老师 2026-09-06 OUT-OF-BAND 触发:
  "那之前的业务应该" → 工程化模式重设计 → STATE.json 单一真值源 + MD 自动生成

原理:
  STATE.json 是机器可读单一真值源
  STATE.md 是 STATE.json 的 markdown 视图(自动生成)
  任何手工改 STATE.md 都会被下次生成覆盖(预期行为)

用法:
  python3 scripts/state_to_md.py           # 生成到 STATE.md(项目根)
  python3 scripts/state_to_md.py --check   # 仅检查 STATE.md 与 STATE.json 是否一致
  python3 scripts/state_to_md.py --out path/to/output.md

设计:
  - 读取 STATE.json
  - 渲染 markdown(标准 GitHub 风格)
  - 写文件 + 实测(wc -l + head)
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

cst = timezone(timedelta(hours=8))


def render(state: dict) -> str:
    """从 STATE.json 渲染 markdown"""
    lines = []
    lines.append(f"# {state['project_id']} {state['project_name']} · 项目状态")
    lines.append("")
    lines.append(f"> **自动生成**:`python3 scripts/state_to_md.py`")
    lines.append(f"> **生成时间**:{state['last_updated']}")
    lines.append(f"> **真值源**:`STATE.json`(不要手改本文件,改 STATE.json 后跑本脚本)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 当前状态卡片 ===
    lines.append("## 🎯 当前状态(一眼到底)")
    lines.append("")
    lines.append("| 项 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| **版本** | `{state['version']}` |")
    lines.append(f"| **tag** | `{state['tag']}` |")
    lines.append(f"| **分支** | `{state['branch']}` |")
    lines.append(f"| **ahead of main** | {state['ahead_of_main']} commits |")
    lines.append(f"| **当前 Sprint** | **{state['current_sprint']}** |")
    lines.append(f"| **Sprint 状态** | {state['current_sprint_status']} |")
    lines.append(f"| **最后 commit** | `{state['last_commit']['hash']}` {state['last_commit']['subject'][:60]} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 上一 Sprint 战果 ===
    ps = state['previous_sprint']
    lines.append(f"## ✅ 上一 Sprint 战果({ps['id']})")
    lines.append("")
    lines.append(f"**完成日期**:{ps['completed_at']}  ")
    lines.append(f"**版本演进**:{ps['version']}")
    lines.append("")
    m = ps['metrics']
    lines.append("| 指标 | 数值 |")
    lines.append("|---|---|")
    lines.append(f"| L1 测试 | **{m['L1_tests']}** |")
    lines.append(f"| Wiki 文件 | **{m['wiki_files_total']}** |")
    lines.append(f"| BAD YAML | **{m['wiki_bad_yaml']}** |")
    lines.append(f"| Sprint 子任务 | {m['sub_tasks_completed']}/{m['sub_tasks_total']} 完成 + {m['sub_tasks_pending_decision']} 待决策 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 待决策点(Do Now) ===
    lines.append("## 🎯 待王老师决策点(优先级排序)")
    lines.append("")
    lines.append(f"**当前生效 Sprint**:{state['current_sprint']}")
    lines.append("")
    lines.append("| 优先级 | ID | 标题 | 阻塞 | ETA | 风险 |")
    lines.append("|---|---|---|---|---|---|")
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    sorted_decisions = sorted(state['pending_decisions'], key=lambda d: priority_order.get(d['priority'], 99))
    for d in sorted_decisions:
        title_short = d['title'][:30]
        blocker_short = d['blocker'][:40].replace('|', '/')
        lines.append(f"| {d['priority']} | `{d['id']}` | {title_short} | {blocker_short} | {d.get('eta_after_decision', d.get('eta', '-'))} | {d['risk']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === Do Now ===
    lines.append("## 🚀 Do Now(本 Sprint 立即行动)")
    lines.append("")
    for i, item in enumerate(state['do_now'], 1):
        lines.append(f"{item}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 模式架构 v2.0 ===
    mode = state['mode_architecture']
    lines.append(f"## 🏗 模式架构 {mode['version']}")
    lines.append("")
    lines.append(f"- **单一真值源**:`{mode['single_source_of_truth']}`")
    lines.append(f"- **生成脚本**:`{mode['regen_script']}`")
    lines.append(f"- **核心原则**:{mode['principle']}")
    lines.append("")
    lines.append("**文档体系**(副作用而非主体):")
    lines.append("")
    for k, v in state['documents'].items():
        lines.append(f"- `{k}`:{v}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 协议铁律 ===
    lines.append("## 🛡 协议铁律遵守")
    lines.append("")
    for k, v in state['protocols'].items():
        lines.append(f"- **{k}**:{v}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 详细决策点 ===
    lines.append("## 📋 决策点详情(完整)")
    lines.append("")
    for d in sorted_decisions:
        lines.append(f"### {d['id']}:{d['title']}")
        lines.append("")
        lines.append(f"- **优先级**:{d['priority']}")
        lines.append(f"- **阻塞**:{d['blocker']}")
        if 'blocking_artifact' in d:
            lines.append(f"- **关联文件**:`{d['blocking_artifact']}`")
        if 'pending_count' in d:
            lines.append(f"- **待批数**:{d['pending_count']}")
        if 'eta_after_decision' in d:
            lines.append(f"- **ETA(批后)**:{d['eta_after_decision']}")
        elif 'eta' in d:
            lines.append(f"- **ETA**:{d['eta']}")
        lines.append(f"- **风险**:{d['risk']}")
        lines.append(f"- **下一步**:{d['next_step']}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append(f"_本文件由 `state_to_md.py` 从 `STATE.json` 自动生成于 {state['last_updated']}_")
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="STATE.json → STATE.md")
    parser.add_argument("--check", action="store_true", help="仅检查一致性,不写文件")
    parser.add_argument("--out", type=str, default="STATE.md", help="输出文件路径")
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    state_file = project_root / "STATE.json"
    out_file = project_root / args.out
    
    if not state_file.exists():
        print(f"❌ STATE.json 不存在:{state_file}")
        sys.exit(1)
    
    state = json.loads(state_file.read_text(encoding="utf-8"))
    md = render(state)
    
    if args.check:
        if not out_file.exists():
            print(f"❌ {out_file} 不存在,需要先生成")
            sys.exit(1)
        existing = out_file.read_text(encoding="utf-8")
        if existing.strip() == md.strip():
            print(f"✅ {out_file} 与 STATE.json 一致")
            sys.exit(0)
        else:
            print(f"⚠️  {out_file} 与 STATE.json 不一致,需要重新生成")
            print(f"   跑:python3 scripts/state_to_md.py")
            sys.exit(1)
    
    out_file.write_text(md, encoding="utf-8")
    
    # 实测落盘
    size = out_file.stat().st_size
    lines = md.count("\n") + 1
    print(f"✅ STATE.md 已生成")
    print(f"   - 路径:{out_file}")
    print(f"   - 大小:{size} 字节 / {lines} 行")
    print(f"   - 渲染键数:{len(state)}")


if __name__ == "__main__":
    main()