#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu_notify.py - 飞书自动推送脚本

王老师 2026-09-06 OUT-OF-BAND:
  "对项目工程计划实时掌控 看看hermes agent 是否有功能支持 比如浏览器的模式"

王老师架构原则:
  - Hermes 内部 = 写代码、写文档、写脚本
  - Codex CLI = 只做 review
  - 飞书推送 = 实时通知王老师(看板更新 + Codex review 完成)

用法:
    python3 scripts/feishu_notify.py
        # 推送当前 STATE.json 摘要到飞书

    python3 scripts/feishu_notify.py --codex-review /tmp/codex-review-last.log
        # 推送 Codex review 结果

    python3 scripts/feishu_notify.py --dashboard-url http://localhost:8788
        # 推送看板 URL
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
cst = timezone(timedelta(hours=8))


def load_state() -> dict:
    state_file = PROJECT_ROOT / "STATE.json"
    return json.loads(state_file.read_text(encoding="utf-8"))


def build_dashboard_message(state: dict, dashboard_url: str = None) -> str:
    """构建飞书看板更新消息(简洁版)"""
    version = state.get("version", "?")
    sprint = state.get("current_sprint", "?")
    status = state.get("current_sprint_status", "?")
    now = state.get("now", {})
    pending = state.get("pending_decisions", [])
    completed = state.get("completed_decisions", [])

    msg = f"""📚 **PJ-102 看板更新**

**版本**:v{version} | **{sprint}** | {status}

🎯 **当前唯一动作**:
{now.get('current_action', '(无)')}

🚫 **阻塞**:{now.get('blocking', '(无)')}
⏱ **预计**:{now.get('estimated_time', '(无)')}
➡️ **解除后**:{now.get('next_action_after_unblock', '(无)')}

📊 **进度**:
- 待决策点:{len(pending)} 项
- 已闭环:{len(completed)} 项

🔗 **看板**:{dashboard_url or 'http://localhost:8788'}
"""

    if pending:
        msg += "\n📋 **决策点状态**:\n"
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
        for d in pending[:5]:
            emoji = risk_emoji.get(d.get("risk", ""), "⚪")
            msg += f"{emoji} [{d.get('priority', '?')}] {d.get('id')}:{d.get('title', '')[:25]}\n"
            msg += f"   阻塞:{d.get('blocker', '')[:40]}\n"

    return msg


def build_codex_review_message(review_log_path: str) -> str:
    """构建 Codex review 完成通知"""
    log_path = Path(review_log_path)
    if not log_path.exists():
        return f"❌ Codex review 日志不存在:{review_log_path}"

    content = log_path.read_text(encoding="utf-8", errors="ignore")

    # 提取关键信息(查找"P0/P1/P2"等关键词)
    findings = []
    for line in content.split("\n"):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if any(kw in line_stripped for kw in ["⚠️", "❌", "critical", "high", "warning", "error"]):
            findings.append(line_stripped[:200])
        if len(findings) >= 5:
            break

    msg = "🔨 **Codex Review 完成**\n\n"
    msg += f"📄 日志:`{log_path}`\n"
    msg += f"⏱ 时间:{datetime.now(cst).strftime('%H:%M:%S')}\n"

    if findings:
        msg += "\n**关键发现**:\n"
        for f in findings:
            msg += f"- {f}\n"
    else:
        msg += "\n**未发现严重问题** ✅\n"

    return msg


def send_feishu(message: str, target: str = "feishu") -> tuple:
    """通过 hermes send 发送飞书"""
    print(f"📤 hermes send -t {target}")
    try:
        result = subprocess.run(
            ["hermes", "send", "-t", target, message],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -1, "", "hermes CLI 未安装"


def main():
    parser = argparse.ArgumentParser(description="飞书通知")
    parser.add_argument("--target", "-t", default="feishu", help="目标平台")
    parser.add_argument("--dashboard-url", help="看板 URL")
    parser.add_argument("--codex-review", help="Codex review 日志路径")
    parser.add_argument("--dry-run", action="store_true", help="只打印不发送")
    args = parser.parse_args()

    if args.codex_review:
        msg = build_codex_review_message(args.codex_review)
    else:
        state = load_state()
        msg = build_dashboard_message(state, args.dashboard_url)

    print("━" * 70)
    print("📋 飞书消息内容:")
    print("━" * 70)
    print(msg)
    print()

    if args.dry_run:
        print("🔍 dry-run:未发送")
        return 0

    rc, stdout, stderr = send_feishu(msg, args.target)
    if rc == 0:
        print("✅ 飞书推送成功")
        if stdout:
            print(stdout[:500])
    else:
        print(f"❌ 飞书推送失败:rc={rc}")
        if stderr:
            print(f"stderr: {stderr[:500]}")
    return rc


if __name__ == "__main__":
    sys.exit(main())