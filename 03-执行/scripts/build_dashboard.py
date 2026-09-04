#!/usr/bin/env python3
"""PJ-102 build_dashboard.py - 自动生成 EXECUTION_DASHBOARD.md。

从以下数据源实时生成:
1. 04-复盘与决策/Sprint*.md 列表(已完成步骤)
2. STATE.md 当前状态
3. VERSION 当前版本
4. git log --oneline (总 commit)
5. Karpathy 对齐率(从 Sprint 18 报告)
"""
import subprocess
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
REVIEW_DIR = REPO_ROOT / "04-复盘与决策"
DASHBOARD = REPO_ROOT / "EXECUTION_DASHBOARD.md"

def get_current_version():
    """从 VERSION 文件获取当前版本"""
    v = (REPO_ROOT / "VERSION").read_text().strip()
    return v

def get_total_commits():
    """git log commit 数"""
    r = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    return int(r.stdout.strip())

def get_tags():
    """所有 tag"""
    r = subprocess.run(["git", "tag", "-l", "--sort=-creatordate"],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    return r.stdout.strip().splitlines()

def get_sprint_reports():
    """所有 Sprint 报告"""
    return sorted(REVIEW_DIR.glob("Sprint*.md"))

def extract_sprint_meta(report_path):
    """从 Sprint 报告提取关键信息"""
    text = report_path.read_text(encoding="utf-8")
    # 提取 Sprint 编号
    m = re.search(r"Sprint\s*(\d+)", report_path.stem)
    sprint_num = int(m.group(1)) if m else 0

    # 提取状态
    if "✅ PASS" in text[:500]:
        status = "✅"
    elif "⚠️" in text[:500]:
        status = "⚠️"
    else:
        status = "🔵"

    # 提取关键产出
    lines = text.splitlines()
    title = ""
    for line in lines[:10]:
        if "title:" in line or "Title:" in line:
            title = line.split(":", 1)[1].strip()
            break

    return {"num": sprint_num, "status": status, "title": title, "path": report_path.name}

def build_dashboard():
    """生成 EXECUTION_DASHBOARD.md"""
    version = get_current_version()
    commits = get_total_commits()
    tags = get_tags()
    reports = get_sprint_reports()
    sprints = [extract_sprint_meta(r) for r in reports]

    # 统计
    completed = sum(1 for s in sprints if s["status"] == "✅")
    total = len(sprints)
    pct = int(100 * completed / max(total, 1))

    # 进度条
    bar_full = "█" * (pct // 5)
    bar_empty = "░" * (20 - pct // 5)
    progress_bar = f"[{bar_full}{bar_empty}] {pct}%"

    # 写入
    content = f"""# PJ-102-LLM-MeetingKB · 执行看板(实时)

> **自动生成**:`python3 03-执行/scripts/build_dashboard.py`
> **最后更新**:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **当前版本**:**{version}**
> **总 Sprint**:{total} | **已完成**:{completed}

---

## 📊 总体进度

{progress_bar}

```
```

## ✅ 已完成 Sprint({completed}/{total})

"""

    # 按 Sprint 编号排序
    completed_sprints = [s for s in sprints if s["status"] == "✅"]
    completed_sprints.sort(key=lambda x: x["num"])

    for s in completed_sprints[-15:]:  # 最近 15 个
        title_short = s["title"][:50] if s["title"] else "Sprint 报告"
        content += f"- ✅ **Sprint {s['num']}** — {title_short} — [{s['path']}](04-复盘与决策/{s['path']})\n"

    # 进行中
    in_progress = [s for s in sprints if s["status"] != "✅"][-5:]
    if in_progress:
        content += f"\n## ⏳ 进行中(最后 5 个)\n\n"
        for s in in_progress:
            content += f"- {s['status']} **Sprint {s['num']}** — [{s['path']}](04-复盘与决策/{s['path']})\n"

    # 关键指标
    content += f"""
---

## 📈 关键指标

| 维度 | 数值 |
|---|---|
| **当前版本** | **{version}** |
| **GitHub commits** | **{commits}** |
| **GitHub tags** | **{len(tags)}** |
| **完成 Sprint** | **{completed}/{total}** |
| **总体进度** | **{pct}%** |

## 🏷️ 所有 tag

```
{chr(10).join(tags)}
```

## 📁 最近 commit(后 5)

```
"""

    r = subprocess.run(["git", "log", "--oneline", "-5"],
                       cwd=REPO_ROOT, capture_output=True, text=True)
    content += r.stdout

    content += """
```

---

**说明**:本看板由 Sprint 完工自动刷新,数据源:
- `04-复盘与决策/Sprint*.md`(已完成步骤)
- `VERSION`(当前版本)
- `git log --oneline`(commit)
- `git tag -l`(tags)

**复用方式**:任何 Superpower 模式项目可复制 `03-执行/scripts/build_dashboard.py` + `EXECUTION_DASHBOARD.md` 模板
"""

    DASHBOARD.write_text(content, encoding="utf-8")
    print(f"✅ EXECUTION_DASHBOARD.md 已生成 ({len(content)} 字符, {completed}/{total} Sprint 完成, {pct}%)")
    return DASHBOARD

if __name__ == "__main__":
    build_dashboard()