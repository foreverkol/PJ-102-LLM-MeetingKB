#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pj_swarm.py - Sprint 25 L3 跨 PJ 看板 Swarm

王老师 2026-09-06 '全部执行 L3':
  - 一屏看所有 PJ 项目状态
  - 每个 PJ 显示进度 + 决策点 + Sprint 状态

用法:
    python3 scripts/pj_swarm.py --scan              # 扫描所有 PJ
    python3 scripts/pj_swarm.py --dashboard         # 生成跨 PJ Swarm HTML
    python3 scripts/pj_swarm.py --report            # 调研报告
    python3 scripts/pj_swarm.py --serve [PORT]      # 启动 Swarm HTTP 服务
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

PJ_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目")
CODEX_BASE = Path("/mnt/d/BaiduSyncdisk/codex/01-项目")
SWARM_DIR = PJ_BASE / "PJ-102-LLM-MeetingKB" / ".swarm"
SWARM_HTML = SWARM_DIR / "index.html"

cst = timezone(timedelta(hours=8))


def scan_pj_projects() -> list:
    """扫描所有 PJ 项目"""
    pj_status = []
    for base in [PJ_BASE, CODEX_BASE]:
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir() or not d.name.startswith("PJ"):
                continue
            scripts_dir = d / "scripts"
            has_scripts = scripts_dir.exists() and any(scripts_dir.glob("*.py"))
            has_state = (d / "STATE.json").exists()
            has_kanban = (d / ".kanban" / "index.html").exists()
            has_git = (d / ".git").exists()

            # 读 STATE.json(如果有)
            state_data = {}
            if has_state:
                try:
                    state_data = json.loads((d / "STATE.json").read_text(encoding="utf-8"))
                except Exception:
                    pass

            # 读 VERSION(如果有)
            version_file = d / "VERSION"
            version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "无"

            # 读 git log(如果有)
            git_log = []
            if has_git:
                try:
                    result = subprocess.run(
                        ["git", "log", "--oneline", "-3"],
                        cwd=d,
                        capture_output=True, text=True, timeout=5
                    )
                    if result.returncode == 0:
                        git_log = result.stdout.strip().split("\n")
                except Exception:
                    pass

            pj_status.append({
                "name": d.name,
                "path": str(d),
                "has_scripts": has_scripts,
                "has_state": has_state,
                "has_kanban": has_kanban,
                "has_git": has_git,
                "version": version,
                "sprint": state_data.get("current_sprint", "无"),
                "git_log": git_log,
                "completed_count": len(state_data.get("completed_decisions", [])),
                "pending_count": len(state_data.get("pending_decisions", []))
            })
    return pj_status


def generate_swarm_html(pj_status: list) -> Path:
    """生成跨 PJ Swarm HTML 看板"""
    SWARM_DIR.mkdir(parents=True, exist_ok=True)

    # 按状态分类
    active = [p for p in pj_status if p["has_state"]]
    inactive = [p for p in pj_status if not p["has_state"]]
    with_tools = [p for p in pj_status if p["has_scripts"]]
    with_kanban = [p for p in pj_status if p["has_kanban"]]

    # 生成 HTML
    html_parts = ["""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PJ Swarm 跨项目看板 · Hermes</title>
<style>
:root {
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #58a6ff;
    --success: #3fb950;
    --warning: #d29922;
    --danger: #f85149;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 20px;
    max-width: 1600px;
    margin: 0 auto;
}
header {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 24px;
}
h1 { font-size: 28px; margin-bottom: 8px; }
.subtitle { opacity: 0.9; font-size: 14px; }
.status-bar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
}
.status-cell {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
}
.status-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; }
.status-value { font-size: 20px; font-weight: 600; margin-top: 4px; }
.swarm-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.swarm-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    transition: transform 0.2s;
}
.swarm-card:hover { transform: translateY(-2px); }
.swarm-card.active { border-left: 3px solid var(--success); }
.swarm-card.inactive { border-left: 3px solid var(--text-dim); opacity: 0.7; }
.pj-name { font-size: 14px; font-weight: 600; margin-bottom: 8px; color: var(--accent); }
.pj-meta { font-size: 12px; color: var(--text-dim); margin-bottom: 4px; }
.pj-stats {
    display: flex;
    gap: 12px;
    margin-top: 8px;
    font-size: 12px;
}
.pj-stat { padding: 2px 8px; border-radius: 4px; background: rgba(88, 166, 255, 0.1); }
.pj-git {
    margin-top: 8px;
    font-size: 11px;
    color: var(--text-dim);
    font-family: monospace;
    line-height: 1.4;
}
@media (max-width: 768px) {
    body { padding: 10px; }
    h1 { font-size: 20px; }
    .swarm-grid { grid-template-columns: 1fr; }
    .status-bar { grid-template-columns: 1fr 1fr; }
}
</style>
<script>
setTimeout(() => location.reload(), 30000);  // 30 秒自动刷新
</script>
</head>
<body>
<header>
    <h1>🌐 PJ Swarm 跨项目看板</h1>
    <div class="subtitle">王老师 2026-09-06 · L3 模式 v2.0 v3.0 · 自动 30 秒刷新</div>
</header>
"""]

    # 状态栏
    html_parts.append(f"""
<div class="status-bar">
    <div class="status-cell">
        <div class="status-label">总 PJ 项目</div>
        <div class="status-value">{len(pj_status)}</div>
    </div>
    <div class="status-cell">
        <div class="status-label">已激活(STATE.json)</div>
        <div class="status-value" style="color: var(--success);">{len(active)}</div>
    </div>
    <div class="status-cell">
        <div class="status-label">工具已复制</div>
        <div class="status-value" style="color: var(--accent);">{len(with_tools)}</div>
    </div>
    <div class="status-cell">
        <div class="status-label">看板已建</div>
        <div class="status-value" style="color: var(--warning);">{len(with_kanban)}</div>
    </div>
    <div class="status-cell">
        <div class="status-label">未激活</div>
        <div class="status-value" style="color: var(--text-dim);">{len(inactive)}</div>
    </div>
</div>
""")

    # PJ 卡片网格
    html_parts.append('<h2 style="margin-bottom: 16px;">📋 项目列表</h2><div class="swarm-grid">')

    for p in pj_status:
        status_class = "active" if p["has_state"] else "inactive"
        status_text = "✅ 已激活" if p["has_state"] else "⚪ 未激活"

        git_html = ""
        if p["git_log"]:
            for line in p["git_log"][:2]:
                git_html += f'<div class="pj-git">{line[:60]}</div>'

        html_parts.append(f"""
<div class="swarm-card {status_class}">
    <div class="pj-name">{p["name"]}</div>
    <div class="pj-meta">{status_text} · {p["version"]} · {p["sprint"]}</div>
    <div class="pj-meta">git:{"✅" if p["has_git"] else "❌"} · scripts:{"✅" if p["has_scripts"] else "❌"} · kanban:{"✅" if p["has_kanban"] else "❌"}</div>
    <div class="pj-stats">
        <span class="pj-stat">✅ {p["completed_count"]}</span>
        <span class="pj-stat">⏸ {p["pending_count"]}</span>
    </div>
    {git_html}
</div>
""")

    html_parts.append("</div>")
    html_parts.append("</body></html>")

    SWARM_HTML.write_text("".join(html_parts), encoding="utf-8")
    return SWARM_HTML


def main():
    parser = argparse.ArgumentParser(description="PJ Swarm 跨项目看板")
    parser.add_argument("--scan", action="store_true", help="扫描所有 PJ")
    parser.add_argument("--dashboard", action="store_true", help="生成 Swarm HTML")
    parser.add_argument("--report", action="store_true", help="调研报告")
    parser.add_argument("--serve", type=int, nargs="?", const=8789, help="启动 Swarm HTTP 服务")
    args = parser.parse_args()

    if args.scan:
        pj_status = scan_pj_projects()
        print(f"📊 扫描 {len(pj_status)} 个 PJ 项目:")
        for p in pj_status:
            state = "✅" if p["has_state"] else "⚪"
            scripts = "✅" if p["has_scripts"] else "❌"
            print(f"  {state} {p['name']} (scripts:{scripts})")
        return

    if args.report or args.dashboard:
        pj_status = scan_pj_projects()
        active = sum(1 for p in pj_status if p["has_state"])
        with_tools = sum(1 for p in pj_status if p["has_scripts"])
        with_kanban = sum(1 for p in pj_status if p["has_kanban"])
        print(f"📊 PJ Swarm 报告:")
        print(f"   总 PJ 数:{len(pj_status)}")
        print(f"   已激活(STATE.json):{active}")
        print(f"   工具已复制:{with_tools}")
        print(f"   看板已建:{with_kanban}")
        if args.dashboard:
            html_path = generate_swarm_html(pj_status)
            print(f"\n✅ Swarm HTML 已生成:{html_path}")
        return

    if args.serve is not None:
        port = args.serve
        # 先生成 HTML
        pj_status = scan_pj_projects()
        generate_swarm_html(pj_status)

        print(f"🌐 启动 Swarm HTTP 服务:http://localhost:{port}/")
        print(f"   工作目录:{SWARM_DIR}")
        print(f"   退出: Ctrl+C")
        try:
            subprocess.run([
                "python3", "-m", "http.server", str(port),
                "--bind", "0.0.0.0", "--directory", str(SWARM_DIR)
            ])
        except KeyboardInterrupt:
            print("\n✅ 服务已停止")
        return

    parser.print_help()


if __name__ == "__main__":
    main()