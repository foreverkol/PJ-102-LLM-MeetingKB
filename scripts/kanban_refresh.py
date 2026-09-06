#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kanban_refresh.py - 看板全链路自动刷新(常态化核心)

王老师 2026-09-06 OUT-OF-BAND:
  "看板如何更好的实现项目跟踪的常态化"

常态化 = 4 件事全自动:
  1. 重建看板 HTML(读 STATE.json + git log)
  2. 集成 Codex 评审报告(.codex-reviews/*.md → 卡片角标)
  3. 检查 HTTP 服务(死了自动重启)
  4. 推送变更摘要到王老师 qqbot

用法:
    python3 scripts/kanban_refresh.py           # 全自动跑一轮
    python3 scripts/kanban_refresh.py --no-push  # 不推送,只刷新
    python3 scripts/kanban_refresh.py --notify-only # 只推送,不重建

cron:*/5 * * * * cd <project> && python3 scripts/kanban_refresh.py
"""
import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
cst = timezone(timedelta(hours=8))
KANBAN_URL = "http://127.0.0.1:8788"
PORT = 8788


def log(msg: str):
    print(f"[{datetime.now(cst).strftime('%H:%M:%S')}] {msg}")


def step1_rebuild_html() -> bool:
    """重建看板 HTML"""
    log("🔨 Step 1/4: 重建看板 HTML")
    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/build_web_dashboard.py")],
            capture_output=True, text=True, timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        if result.returncode == 0:
            log(f"   ✅ HTML 已生成: {result.stdout.split('大小:')[1].split('字节')[0].strip()} 字节")
            return True
        else:
            log(f"   ❌ HTML 生成失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"   ❌ 异常: {e}")
        return False


def step2_integration() -> bool:
    """看板集成: 把 Codex 评审报告 → 看板"""
    log("📊 Step 2/4: 集成 Codex 评审报告")
    reviews_dir = PROJECT_ROOT / ".codex-reviews"
    if not reviews_dir.exists():
        log("   ⚠️  .codex-reviews/ 不存在,跳过")
        return True

    reviews = sorted(reviews_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not reviews:
        log("   ⚠️  无评审报告,跳过")
        return True

    latest = reviews[0]
    # 提取评审摘要(统计问题数)
    content = latest.read_text(encoding="utf-8", errors="ignore")

    # 简单统计(看 🚨/⚠️/💡 几个)
    critical = content.count("🚨")
    medium = content.count("⚠️")
    improvements = content.count("💡")

    log(f"   ✅ 最新评审: {latest.name}")
    log(f"      🚨 严重: {critical} / ⚠️ 中等: {medium} / 💡 改进: {improvements}")

    # 写入 STATE.json 的 codex_review 字段(看板会自动显示)
    state_file = PROJECT_ROOT / "STATE.json"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    state["last_codex_review"] = {
        "file": str(latest.relative_to(PROJECT_ROOT)),
        "critical_count": critical,
        "medium_count": medium,
        "improvements_count": improvements,
        "reviewed_at": datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")
    }
    state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log(f"   ✅ STATE.json last_codex_review 已更新")
    return True


def step3_check_service() -> bool:
    """检查 HTTP 服务,死了重启"""
    log("🌐 Step 3/4: 检查 HTTP 服务")
    try:
        with urllib.request.urlopen(KANBAN_URL, timeout=5) as resp:
            if resp.status == 200:
                log(f"   ✅ 服务正常 (HTTP 200, {KANBAN_URL})")
                return True
    except Exception as e:
        log(f"   ⚠️  服务不可用: {e}")

    # 重启
    log("   🔄 尝试重启...")
    try:
        subprocess.run(
            ["pkill", "-f", "http.server 8788"],
            capture_output=True, timeout=5
        )
        subprocess.Popen(
            [sys.executable, "-m", "http.server", str(PORT),
             "--bind", "0.0.0.0", "--directory", str(PROJECT_ROOT / ".kanban")],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        import time
        time.sleep(2)
        with urllib.request.urlopen(KANBAN_URL, timeout=5) as resp:
            if resp.status == 200:
                log(f"   ✅ 重启成功")
                return True
    except Exception as e:
        log(f"   ❌ 重启失败: {e}")
    return False


def step4_push_qqbot() -> bool:
    """推送变更摘要到 qqbot(王老师默认平台)"""
    log("📤 Step 4/4: 推送 qqbot 摘要")
    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/feishu_notify.py"),
             "--target", "qqbot"],
            capture_output=True, text=True, timeout=60,
            cwd=str(PROJECT_ROOT)
        )
        if result.returncode == 0:
            log("   ✅ qqbot 推送成功")
            return True
        else:
            log(f"   ❌ 推送失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        log(f"   ❌ 异常: {e}")
        return False


def should_push_now() -> bool:
    """是否应该推送(避免 5 分钟刷一次都推,只在状态变化时推)"""
    state_file = PROJECT_ROOT / "STATE.json"
    state = json.loads(state_file.read_text(encoding="utf-8"))

    # 看 last_commit 是否变化
    result = subprocess.run(
        ["git", "-C", str(PROJECT_ROOT), "log", "-1", "--format=%H"],
        capture_output=True, text=True, timeout=5
    )
    current_hash = result.stdout.strip()

    last_notified = state.get("last_notified_commit", "")
    if current_hash != last_notified:
        # 状态变化了,推送
        state["last_notified_commit"] = current_hash
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="看板常态化全链路自动刷新")
    parser.add_argument("--no-push", action="store_true", help="不推送 qqbot")
    parser.add_argument("--notify-only", action="store_true", help="只推送")
    args = parser.parse_args()

    log("━" * 70)
    log("🚀 kanban_refresh 启动(常态化全链路)")
    log("━" * 70)

    if args.notify_only:
        step4_push_qqbot()
        return

    results = []
    results.append(step1_rebuild_html())
    results.append(step2_integration())
    results.append(step3_check_service())

    if not args.no_push:
        if should_push_now():
            results.append(step4_push_qqbot())
        else:
            log("📤 Step 4/4: 跳过推送(无 commit 变化)")

    log("━" * 70)
    log(f"🏁 完成:{sum(results)}/{len(results)} 步成功")
    log("━" * 70)
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()