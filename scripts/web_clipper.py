#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_clipper.py - AT-11 Web Clipper (Chrome + NotebookLM 集成)

王老师 2026-09-06 '按推荐执行 A'(Chrome + NotebookLM):
  - Chrome = Windows 端浏览器(WSL 调用 cmd.exe 启动)
  - NotebookLM = 已有 notebooklm CLI + web backend

用法:
    python3 scripts/web_clipper.py <URL> [--notebook <id>] [--tags tag1,tag2]
        # 抓取 URL → 保存到 PJ-102 wiki
        # 可选:推送 NotebookLM 让 AI 处理

    python3 scripts/web_clipper.py --import <file.html>
        # 从本地 HTML 文件导入

    python3 scripts/web_clipper.py --list
        # 列出最近剪藏
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
WIKI_RAW = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/raw_clips")
cst = timezone(timedelta(hours=8))


def fetch_url(url: str) -> dict:
    """抓取 URL 内容"""
    print(f"🌐 抓取: {url}")
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (PJ-102 Web Clipper)"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            return {
                "status": "ok",
                "url": url,
                "title": url,  # 简化版:用 URL 作 title
                "content": content[:50000],  # 限长
                "fetched_at": datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        return {"status": "error", "url": url, "error": str(e)}


def save_clip(clip: dict, tags: list = None, notebook: str = None) -> Path:
    """保存剪藏到 raw_clips/"""
    WIKI_RAW.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(cst).strftime("%Y%m%d-%H%M%S")
    url_hash = abs(hash(clip["url"])) % 100000
    fname = f"clip_{timestamp}_{url_hash:05d}.md"
    output = WIKI_RAW / fname

    metadata = {
        "url": clip["url"],
        "fetched_at": clip.get("fetched_at", ""),
        "tags": tags or [],
        "notebook": notebook,
        "status": clip["status"]
    }

    content = f"""---
{json.dumps(metadata, ensure_ascii=False, indent=2)}
---

# {clip.get('title', clip['url'])}

**URL**: {clip['url']}
**时间**: {metadata['fetched_at']}
**标签**: {', '.join(tags) if tags else '(无)'}

---

## 内容

```html
{clip.get('content', clip.get('error', '(无内容)'))[:30000]}
```

---

## 待办

- [ ] 人工摘要
- [ ] 关联到 persons / concepts
- [ ] 评估推 NotebookLM
"""
    output.write_text(content, encoding="utf-8")
    return output


def push_to_notebooklm(clip_path: Path, notebook: str = None) -> dict:
    """通过 notebooklm CLI 推送给 NotebookLM(如果配置)"""
    if not notebook:
        return {"status": "skip", "reason": "no notebook"}

    print(f"📚 推送 NotebookLM: {notebook}")
    try:
        # 读 markdown 内容
        content = clip_path.read_text(encoding="utf-8")
        # 提取正文(去掉 frontmatter)
        body = content.split("---", 2)[-1].strip() if content.startswith("---") else content

        # notebooklm CLI: ask + add(简化版)
        # 实际 notebooklm CLI 没有直接 add source,用 ask 提问模拟
        result = subprocess.run(
            ["notebooklm", "use", notebook, "ask", body[:1000]],
            capture_output=True, text=True, timeout=60
        )
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:200]
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def open_in_chrome(url: str) -> bool:
    """用 Windows Chrome 打开 URL(WSL 通过 cmd.exe)"""
    try:
        subprocess.run(
            ["cmd.exe", "/c", "start", "chrome", url],
            capture_output=True, timeout=10
        )
        return True
    except Exception as e:
        return False


def main():
    parser = argparse.ArgumentParser(description="Web Clipper (Chrome + NotebookLM)")
    parser.add_argument("url", nargs="?", help="要剪藏的 URL")
    parser.add_argument("--notebook", help="NotebookLM notebook ID")
    parser.add_argument("--tags", help="逗号分隔标签")
    parser.add_argument("--open", action="store_true", help="同时用 Chrome 打开")
    parser.add_argument("--list", action="store_true", help="列出最近剪藏")
    args = parser.parse_args()

    if args.list:
        # 列剪藏
        if not WIKI_RAW.exists():
            print("无剪藏")
            return
        clips = sorted(WIKI_RAW.glob("clip_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        print(f"📋 最近 {min(10, len(clips))} 个剪藏:")
        for c in clips[:10]:
            print(f"  {c.name} ({c.stat().st_size} 字节)")
        return

    # 抓取 + 保存
    clip = fetch_url(args.url)
    tags = args.tags.split(",") if args.tags else []
    saved = save_clip(clip, tags, args.notebook)

    print(f"✅ 已保存: {saved}")
    print(f"   大小: {saved.stat().st_size} 字节")

    if args.open:
        open_in_chrome(args.url)
        print(f"🌐 已用 Chrome 打开: {args.url}")

    if args.notebook:
        result = push_to_notebooklm(saved, args.notebook)
        print(f"📚 NotebookLM: {result['status']}")


if __name__ == "__main__":
    main()