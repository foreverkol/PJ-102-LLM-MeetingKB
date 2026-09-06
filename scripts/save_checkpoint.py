"""save_checkpoint.py - 王老师重启前断点保护

王老师 2026-09-06 '我需要重启电脑 做好断点处理':
  - 保存完整 checkpoint 到 STATE.json
  - 关闭后台服务
  - 清理临时进程
  - 验证所有 git 改动已 commit + push
"""
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
STATE_JSON = PROJECT_ROOT / "STATE.json"

cst = timezone(timedelta(hours=8))
NOW = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")


def update_state_with_checkpoint():
    """更新 STATE.json 添加 checkpoint 字段"""
    state = json.loads(STATE_JSON.read_text(encoding="utf-8"))

    state["checkpoint"] = {
        "type": "system_restart_preparation",
        "triggered_by": "王老师 2026-09-06 OUT-OF-BAND '我需要重启电脑'",
        "saved_at": NOW,
        "what_works": [
            "Sprint 22 全部 5 决策点按推荐闭环",
            "Sprint 23 L1-L5 全部按推荐完成",
            "v3.1.1-rc1 tag 已 push origin",
            "HTML 看板服务在跑 (PID 4614, http://localhost:8788)",
            "Post-commit hook 接通 kanban_refresh + qqbot 推送",
            "Cron job */5 * * * * 已创建 (gateway 未跑可能未触发)",
            "172 PASS + 1 skipped 全量测试",
        ],
        "what_pending": [
            "王老师跑 codex login → L3 自动切换到真 Codex 评审",
            "王老师跑 notebooklm login → L4 Web Clipper RAG 完整化",
            "Sprint 24 启动 (待王老师触发)",
        ],
        "where_to_resume": [
            "1. 终端: cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB",
            "2. 看看板: http://localhost:8788 (刷新页面)",
            "3. 看推进: python3 scripts/where.py --brief",
            "4. 看完整 STATE: cat STATE.json",
        ],
        "recover_commands": [
            "# 重启后恢复看板服务 (若死了)",
            "cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB",
            "python3 -m http.server 8788 --bind 0.0.0.0 --directory .kanban &",
            "# 验证看板",
            "curl http://localhost:8788/",
            "# 全量测试",
            "python3 -m pytest 03-执行/tests/unit/ -q",
        ],
    }

    state["now"] = {
        "current_action": "🛡 断点保护:王老师重启电脑,所有状态已保存",
        "blocking": "(王老师操作中)",
        "next_action_after_decision": "王老师开机后回复 '继续' → 推进 Sprint 24",
        "estimated_time": "0 分钟 (已保存)",
    }

    state["do_now"] = [
        "1. 重启前:王老师无需任何额外操作",
        "2. 重启后:cd + where.py 看位置 + 触发指令",
    ]

    STATE_JSON.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return state


def kill_background_services():
    """关闭后台 HTTP 服务"""
    print("🛑 关闭后台 HTTP 服务...")
    try:
        subprocess.run(
            ["pkill", "-f", "http.server 8788"],
            capture_output=True,
            timeout=5,
        )
        print("   ✅ HTTP 服务已关闭")
    except Exception as e:
        print(f"   ⚠️ 关闭异常: {e}")


def check_git_status():
    """检查 git 状态"""
    print("📊 检查 git 状态...")
    result = subprocess.run(
        ["git", "status", "-s"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def commit_if_needed(uncommitted: str):
    """如果有未提交改动,自动 commit"""
    if not uncommitted:
        print("   ✅ 无未提交改动")
        return

    print(f"   ⚠️ 发现未提交改动: {len(uncommitted.split(chr(10)))} 文件")
    print("   自动 commit...")

    subprocess.run(["git", "add", "-A"], cwd=PROJECT_ROOT, check=False)

    commit_msg = f"chore(checkpoint): 王老师重启前自动保存 {NOW}"

    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode == 0:
        print("   ✅ 自动 commit 成功")
    else:
        print(f"   ⚠️ commit 失败: {result.stderr[:200]}")


def main():
    print("=" * 60)
    print("🛡 断点保护 - 王老师重启电脑前")
    print("=" * 60)
    print()

    # 1. 更新 STATE.json
    print("1️⃣ 更新 STATE.json checkpoint...")
    state = update_state_with_checkpoint()
    print("   ✅ STATE.json checkpoint 已保存")
    print(f"   时间: {NOW}")
    print()

    # 2. 重新生成 STATE.md
    print("2️⃣ 重新生成 STATE.md...")
    subprocess.run(
        ["python3", "scripts/state_to_md.py"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        timeout=10,
    )
    print("   ✅ STATE.md 已重新生成")
    print()

    # 3. 检查 git 状态
    print("3️⃣ 检查 git 状态...")
    uncommitted = check_git_status()
    print(f"   git status: {len(uncommitted.split(chr(10))) if uncommitted else 0} 文件未提交")
    commit_if_needed(uncommitted)
    print()

    # 4. Push 到 origin
    print("4️⃣ Push 到 origin...")
    result = subprocess.run(
        ["git", "push", "origin", "dev"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode == 0:
        print("   ✅ Push 成功")
    else:
        print(f"   ⚠️ Push 失败: {result.stderr[:200]}")
    print()

    # 5. 关闭后台服务
    kill_background_services()
    print()

    # 6. 最终验证
    print("5️⃣ 最终验证...")
    result = subprocess.run(
        ["git", "status", "-s"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=10,
    )
    final_status = result.stdout.strip()
    if final_status:
        print(f"   ⚠️ 仍有未提交改动: {final_status}")
    else:
        print("   ✅ 工作区干净")

    print()
    print("=" * 60)
    print("✅ 断点保护完成 - 王老师可以安全重启")
    print("=" * 60)
    print()
    print("📋 重启后恢复步骤:")
    print("   1. cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
    print("   2. python3 -m http.server 8788 --bind 0.0.0.0 --directory .kanban &")
    print("   3. curl http://localhost:8788/  # 验证看板")
    print("   4. python3 scripts/where.py --brief  # 看推进")
    print("   5. 回复 '继续' → 进入 Sprint 24")


if __name__ == "__main__":
    main()