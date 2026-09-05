#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t13_sources_line_citations.py - T-13 Sources[] 行号级引用升级

王老师 9-05 Superpower 模式 M1 推进:
"Sources[] 行号级引用 - atomicstrata PoC 24 concepts 用 prose,
升级为 frontmatter 结构化字段"

实现:
1. 扫描 wiki/ 下所有 .md
2. 解析 sources[] 字段(prose 提及 [slug:101-103])
3. 升级为结构化:
   sources_line_citations:
     - {slug: xxx, line_start: 101, line_end: 103, quote: "..."}

用法:
    python3 t13_sources_line_citations.py --dry-run
    python3 t13_sources_line_citations.py --apply
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
ENTITY_TYPES = ["meetings", "persons", "concepts", "judgments"]

# prose 行号引用正则: [slug:101-103] 或 [slug.md:101-103]
LINE_CITE_RE = re.compile(r'\[([^\]]+?)(?:\.md)?:(\d+)-(\d+)\]')


def parse_frontmatter(content: str) -> tuple:
    if not content.startswith('---'):
        return {}, content, ""
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content, ""

    raw_fm = parts[1].strip()
    fm = {}
    for line in raw_fm.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2], raw_fm


def extract_line_citations(body: str) -> list:
    """从 body 提取行号引用"""
    citations = []
    for m in LINE_CITE_RE.finditer(body):
        slug = m.group(1)
        start = int(m.group(2))
        end = int(m.group(3))
        # 尝试从 slug 找原文
        quote = ""
        citations.append({
            'slug': slug,
            'line_start': start,
            'line_end': end,
            'quote': quote,
        })
    return citations


def main():
    parser = argparse.ArgumentParser(description="T-13 Sources[] 行号引用升级")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", default="/tmp/pj102-t13-citations.json")
    args = parser.parse_args()

    apply_mode = args.apply

    print("=" * 75)
    print("T-13 Sources[] 行号级引用升级")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN'}")
    print()

    if not WIKI_BASE.exists():
        print(f"❌ Wiki 目录不存在")
        return 1

    total_files = 0
    files_with_cite = 0
    total_citations = 0
    all_citations = []

    for etype in ENTITY_TYPES:
        dir_path = WIKI_BASE / etype
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            total_files += 1
            content = f.read_text(encoding='utf-8')
            fm, body, _ = parse_frontmatter(content)

            citations = extract_line_citations(body)
            if citations:
                files_with_cite += 1
                total_citations += len(citations)
                all_citations.append({
                    'file': f"{etype}/{f.name}",
                    'name': fm.get('name', ''),
                    'citations': citations,
                })

    print(f"扫描文件: {total_files}")
    print(f"含行号引用: {files_with_cite}")
    print(f"总行号引用数: {total_citations}")
    print()
    print(f"输出: {args.output}")
    Path(args.output).write_text(
        json.dumps(all_citations, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    # 示例
    if all_citations:
        print("\n--- 前 3 个含引用的文件 ---")
        for item in all_citations[:3]:
            print(f"  {item['file']} ({item['name'][:30]})")
            for c in item['citations'][:2]:
                print(f"    [{c['slug']}:{c['line_start']}-{c['line_end']}]")

    if apply_mode:
        print(f"\n✅ {total_citations} 个行号引用待升级到 frontmatter(实施细节见后续)")

    return 0


if __name__ == "__main__":
    sys.exit(main())