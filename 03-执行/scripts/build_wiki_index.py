#!/usr/bin/env python3
"""PJ-102 专用 build_index.py - 自动生成 wiki/index.md 全局索引。

对齐 Karpathy LLM Wiki 标准:
- 每篇文章一行(summary + Updated)
- 按 topic 分组
- 链接到具体文章
"""
import os
import re
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
INDEX_FILE = WIKI_ROOT / "index.md"

def extract_summary_from_article(article_path):
    """从文章 frontmatter 提取 summary / description"""
    text = article_path.read_text(encoding="utf-8")
    # frontmatter 后第一段
    m = re.search(r"^---\n.*?\n---\n\n(.+?)(?:\n\n|\Z)", text, re.DOTALL)
    if m:
        summary = m.group(1).strip()
        # 截断到 100 字符
        return summary[:100].replace("\n", " ")
    return "(no summary)"

def extract_updated_date(article_path):
    """从文件 mtime 提取 Updated 日期"""
    mtime = article_path.stat().st_mtime
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

def build_index():
    """生成 wiki/index.md"""
    content = "# Knowledge Base Index\n\n"
    content += f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"> 项目: PJ-102-LLM-MeetingKB\n"
    content += f"> 当前稳定版本: v3.0.1-stable\n\n"

    categories = {
        "meetings": "会议(meetings)",
        "persons": "人物(persons)",
        "concepts": "概念(concepts)",
        "judgments": "判断(judgments)",
    }

    total = 0
    for cat, desc in categories.items():
        cat_dir = WIKI_ROOT / cat
        if not cat_dir.is_dir():
            continue
        articles = sorted(cat_dir.glob("*.md"))
        if not articles:
            continue

        content += f"\n## {desc}\n\n"
        content += f"共 {len(articles)} 篇文章\n\n"

        for article in articles:
            if article.name in ("index.md", "log.md"):
                continue
            summary = extract_summary_from_article(article)
            updated = extract_updated_date(article)
            content += f"- [{article.stem}]({cat}/{article.name}) | Updated: {updated} | {summary}\n"
            total += 1

    content += f"\n---\n\n"
    content += f"**总计**: {total} 篇文章,4 个 topic 子目录\n"
    content += f"\n**索引方法**:Karpathy LLM Wiki 标准\n"
    content += f"- 每篇文章:文件名 + Updated 日期 + summary\n"
    content += f"- 完整操作日志:见 `wiki/log.md`\n"

    INDEX_FILE.write_text(content, encoding="utf-8")
    print(f"✅ index.md 已生成: {INDEX_FILE} ({len(content)} 字符, {total} 篇文章)")

if __name__ == "__main__":
    build_index()