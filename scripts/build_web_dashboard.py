#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_web_dashboard.py - 生成 PJ-102 实时 HTML 看板

王老师 2026-09-06 OUT-OF-BAND:
  "可以结合 hermes 浏览器监控 展示项目整体计划执行进展情况"

设计:
  - 单文件 HTML (含 inline CSS + JS)
  - 5 决策点卡片(可点击)
  - git 时间线(最近 commit)
  - 自动每 30 秒刷新
  - 移动端响应式
  - 离线可看(file:// 协议)
  - 状态色:🟢 P0=绿 / 🟡 P1=橙 / 🟠 P2=深橙 / ⚪ P3=灰

用法:
    python3 scripts/build_web_dashboard.py
        # 生成 .kanban/index.html

    python3 -m http.server 8788 --directory .kanban
        # 启动 HTTP 服务
        # 浏览器打开 http://localhost:8788

    # 或双击 .kanban/index.html (无需服务)
"""
import json
import subprocess
import html
from pathlib import Path
from datetime import datetime, timezone, timedelta

cst = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).parent.parent
KANBAN_DIR = PROJECT_ROOT / ".kanban"


def load_state() -> dict:
    state_file = PROJECT_ROOT / "STATE.json"
    if not state_file.exists():
        return {}
    return json.loads(state_file.read_text(encoding="utf-8"))


def git_log(n: int = 10) -> list:
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "log", f"-{n}", "--oneline", "--decorate"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split("\n")
    except:
        pass
    return []


def render_dashboard(state: dict) -> str:
    """生成完整 HTML"""
    if not state:
        return "<h1>STATE.json 不存在</h1>"

    version = state.get("version", "?")
    sprint = state.get("current_sprint", "?")
    status = state.get("current_sprint_status", "?")
    branch = state.get("branch", "?")
    ahead = state.get("ahead_of_main", "?")
    last = state.get("last_commit", {})
    now = state.get("now", {})
    pending = state.get("pending_decisions", [])
    completed = state.get("completed_decisions", [])

    now_str = datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")

    # 决策点卡片 HTML
    decision_cards = ""
    risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}
    for d in pending:
        emoji = risk_emoji.get(d.get("risk", ""), "⚪")
        prio = d.get("priority", "?")
        title = html.escape(d.get("title", ""))
        blocker = html.escape(d.get("blocker", ""))
        next_step = html.escape(d.get("next_step", "")[:60])
        progress = d.get("progress", "")

        decision_cards += f"""
<div class="card {d.get('risk', 'low')}-risk">
    <div class="card-header">
        <span class="risk-emoji">{emoji}</span>
        <span class="prio-badge prio-{prio}">{prio}</span>
        <span class="id-badge">{d.get('id', '?')}</span>
    </div>
    <h3>{title}</h3>
    <div class="blocker">🚫 {blocker}</div>
    {f'<div class="progress">📊 {progress}</div>' if progress else ''}
    <div class="next-step">➡️ {next_step}</div>
</div>
"""

    # 已闭环 HTML
    completed_html = ""
    for c in completed:
        title = html.escape(c.get("title", ""))
        cid = c.get("id", "?")
        completed_html += f"""
<li class="completed-item">
    <span class="check">✅</span>
    <span class="cid">{cid}</span>
    <span class="ctitle">{title}</span>
</li>
"""

    # git log HTML
    log_html = ""
    for line in git_log(10):
        log_html += f'<div class="commit-line">{html.escape(line)}</div>\n'

    # now 卡片
    now_html = ""
    if now:
        now_html = f"""
<div class="now-banner">
    <div class="now-label">🎯 当前唯一动作</div>
    <div class="now-text">{html.escape(now.get('current_action', ''))}</div>
    <div class="now-meta">🚫 阻塞:{html.escape(now.get('blocking', ''))}</div>
    <div class="now-meta">⏱ 预计:{html.escape(now.get('estimated_time', ''))}</div>
    <div class="now-meta">➡️ 解除后:{html.escape(now.get('next_action_after_unblock', ''))}</div>
</div>
"""

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PJ-102 实时看板 · {version}</title>
<style>
:root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #58a6ff;
    --success: #3fb950;
    --warning: #d29922;
    --danger: #f85149;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}}
header {{
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 24px;
}}
h1 {{ font-size: 28px; margin-bottom: 8px; }}
.subtitle {{ opacity: 0.9; font-size: 14px; }}
.status-bar {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
}}
.status-cell {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
}}
.status-label {{ font-size: 12px; color: var(--text-dim); text-transform: uppercase; }}
.status-value {{ font-size: 16px; font-weight: 600; margin-top: 4px; }}
.now-banner {{
    background: linear-gradient(135deg, #d29922, #f0c674);
    color: #0d1117;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 24px;
    font-weight: 500;
}}
.now-label {{ font-size: 12px; text-transform: uppercase; opacity: 0.7; margin-bottom: 8px; }}
.now-text {{ font-size: 18px; font-weight: 700; margin-bottom: 8px; }}
.now-meta {{ font-size: 14px; opacity: 0.85; margin-top: 4px; }}
h2 {{ font-size: 20px; margin: 32px 0 16px; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
}}
.card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 16px;
    transition: transform 0.2s;
}}
.card:hover {{ transform: translateY(-2px); }}
.card.low-risk {{ border-left-color: var(--success); }}
.card.medium-risk {{ border-left-color: var(--warning); }}
.card.high-risk {{ border-left-color: var(--danger); }}
.card-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }}
.risk-emoji {{ font-size: 18px; }}
.prio-badge {{
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}}
.prio-P0 {{ background: var(--danger); color: white; }}
.prio-P1 {{ background: var(--warning); color: #0d1117; }}
.prio-P2 {{ background: #8b949e; color: white; }}
.prio-P3 {{ background: #484f58; color: white; }}
.id-badge {{
    background: var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-family: 'SF Mono', Monaco, monospace;
}}
.card h3 {{ font-size: 16px; margin-bottom: 8px; }}
.blocker {{ font-size: 13px; color: var(--text-dim); margin-bottom: 8px; line-height: 1.5; }}
.progress {{
    background: rgba(63, 185, 80, 0.1);
    border: 1px solid rgba(63, 185, 80, 0.3);
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 13px;
    color: var(--success);
    margin-bottom: 8px;
}}
.next-step {{
    font-size: 13px;
    color: var(--accent);
    background: rgba(88, 166, 255, 0.1);
    padding: 8px 10px;
    border-radius: 4px;
    margin-top: 8px;
}}
.completed-list {{ list-style: none; }}
.completed-item {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.completed-item .check {{ color: var(--success); }}
.completed-item .cid {{
    background: var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
}}
.completed-item .ctitle {{ flex: 1; }}
.git-log {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 13px;
}}
.commit-line {{ padding: 4px 0; color: var(--text-dim); }}
.commit-line:hover {{ color: var(--text); }}
footer {{
    margin-top: 40px;
    padding: 16px;
    text-align: center;
    color: var(--text-dim);
    font-size: 12px;
    border-top: 1px solid var(--border);
}}
.refresh-info {{ display: inline-block; margin-left: 12px; }}
</style>
</head>
<body>
<header>
    <h1>📚 PJ-102 LLM MeetingKB · 实时看板</h1>
    <div class="subtitle">
        版本 v{version} · {sprint} · {html.escape(status)}
        · 🌿 {branch}(ahead {ahead}) · 🕐 {now_str}
    </div>
</header>

<div class="status-bar">
    <div class="status-cell">
        <div class="status-label">📝 最后 Commit</div>
        <div class="status-value">{last.get('hash', '?')[:8]}</div>
        <div style="font-size:12px;color:var(--text-dim);margin-top:4px">{html.escape(last.get('subject', '')[:40])}</div>
    </div>
    <div class="status-cell">
        <div class="status-label">⏸ 待决策点</div>
        <div class="status-value">{len(pending)} 项</div>
    </div>
    <div class="status-cell">
        <div class="status-label">✅ 已闭环</div>
        <div class="status-value">{len(completed)} 项</div>
    </div>
    <div class="status-cell">
        <div class="status-label">🎯 Sprint</div>
        <div class="status-value">{sprint}</div>
    </div>
</div>

{now_html}

<h2>📋 决策点状态 ({len(pending)} 项)</h2>
<div class="cards">
{decision_cards}
</div>

<h2>✅ 已闭环 ({len(completed)} 项)</h2>
<ul class="completed-list">
{completed_html}
</ul>

<h2>🛠 最近 Commits</h2>
<div class="git-log">
{log_html}
</div>

<footer>
    <span>Hermes Kanban 实时同步</span>
    <span class="refresh-info">· 30 秒自动刷新 · 最后更新:{now_str}</span>
    <br><br>
    <span>📁 本地打开:file://{KANBAN_DIR}/index.html</span>
    <br>
    <span>🌐 HTTP 服务:cd .kanban && python3 -m http.server 8788</span>
</footer>

<script>
// 自动刷新(每 30 秒)
setTimeout(function() {{
    location.reload();
}}, 30000);
console.log('🔄 PJ-102 看板自动刷新:30 秒后');
</script>

</body>
</html>
"""
    return html_content


def main():
    KANBAN_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    html_content = render_dashboard(state)

    output = KANBAN_DIR / "index.html"
    output.write_text(html_content, encoding="utf-8")

    print(f"✅ 看板已生成:{output}")
    print(f"   大小:{output.stat().st_size} 字节")
    print(f"")
    print(f"💡 王老师查看方式(任选):")
    print(f"   1. 双击打开:{output}")
    print(f"   2. HTTP 服务:cd {KANBAN_DIR} && python3 -m http.server 8788")
    print(f"      → http://localhost:8788")
    print(f"   3. 文件 URL:file://{output}")
    print(f"")
    print(f"🔄 自动刷新:30 秒")
    print(f"📡 同步命令:python3 scripts/build_web_dashboard.py")


if __name__ == "__main__":
    main()