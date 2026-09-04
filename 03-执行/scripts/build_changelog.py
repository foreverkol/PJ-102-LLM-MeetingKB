#!/usr/bin/env python3
"""PJ-102 build_changelog.py - 自动从 git log 生成 CHANGELOG.md。

数据源:git log --pretty=format:每个 commit 转 CHANGELOG 一行
"""
import subprocess
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
CHANGELOG = REPO_ROOT / "CHANGELOG.md"

def get_commits_grouped_by_version():
    """git log 按 version 分组(用 tag 作为分界)"""
    r = subprocess.run(
        ["git", "log", "--tags", "--simplify-by-decoration",
         "--pretty=format:%ai|%d|%s", "--reverse"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    # 简化版:按 date + version 分组
    commits = []
    for line in r.stdout.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            date, refs, subject = parts
            commits.append({
                "date": date[:10],
                "refs": refs.strip(),
                "subject": subject.strip()
            })
    return commits

def get_commits_for_tag(tag):
    """特定 tag 范围的 commits"""
    # 简化:拿所有 commit,人眼归类
    r = subprocess.run(
        ["git", "log", "--oneline", f"{tag}", "-50"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    return r.stdout.strip().splitlines()

def categorize_commit(subject):
    """按 commit 消息分类"""
    s = subject.lower()
    if "release:" in s or "v3.0." in s:
        return "release"
    if "feat:" in s:
        return "feat"
    if "fix:" in s:
        return "fix"
    if "docs:" in s:
        return "docs"
    if "perf:" in s:
        return "perf"
    if "refactor:" in s:
        return "refactor"
    return "chore"

def build_changelog():
    """生成 CHANGELOG.md"""
    version = (REPO_ROOT / "VERSION").read_text().strip()
    today = datetime.now().strftime("%Y-%m-%d")

    # 拿 git log
    r = subprocess.run(
        ["git", "log", "--oneline", "--reverse"],
        cwd=REPO_ROOT, capture_output=True, text=True
    )
    all_commits = r.stdout.strip().splitlines()

    # 按时间倒序整理(最新在上)
    commits_grouped = defaultdict(list)
    for line in reversed(all_commits):
        # 格式:hash subject
        parts = line.split(" ", 1)
        if len(parts) == 2:
            hash_, subject = parts
            cat = categorize_commit(subject)
            commits_grouped[cat].append(f"- {cat}: {subject} (`{hash_[:8]}`)")

    # 写入
    content = f"""# PJ-102-LLM-MeetingKB · 变更日志

> **自动生成**:`python3 03-执行/scripts/build_changelog.py`
> **最后更新**:{today}
> **当前版本**:**{version}**

---

## [Unreleased]

(基于 git log 自动跟踪)

---

## 历史版本(按类别)

### 🚀 Release

{chr(10).join(commits_grouped.get('release', ['(无)'])[-10:])}

### ✨ Features

{chr(10).join(commits_grouped.get('feat', ['(无)'])[-10:])}

### 🐛 Fixes

{chr(10).join(commits_grouped.get('fix', ['(无)'])[-10:])}

### 📝 Docs

{chr(10).join(commits_grouped.get('docs', ['(无)'])[-10:])}

### ⚡ Performance

{chr(10).join(commits_grouped.get('perf', ['(无)'])[-10:])}

### ♻️ Refactor

{chr(10).join(commits_grouped.get('refactor', ['(无)'])[-10:])}

---

## 📊 总统计

- **总 commits**:`git rev-list --count HEAD`
- **当前版本**:`{version}`
- **GitHub tags**:`git tag -l | wc -l`

---

**说明**:本文件由 `build_changelog.py` 自动生成,数据源是 `git log`。
每次 Sprint 完工 commit 后,可执行 `python3 03-执行/scripts/build_changelog.py` 刷新。
"""

    CHANGELOG.write_text(content, encoding="utf-8")
    print(f"✅ CHANGELOG.md 已生成 ({len(content)} 字符)")

if __name__ == "__main__":
    build_changelog()