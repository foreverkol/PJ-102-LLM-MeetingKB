#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t13_upgrade_poc_to_structured.py - T-13 升级版

读取 poc 分支的 24 concepts 行号引用 → 分析 + 生成结构化 frontmatter 模板
供未来 s4-s12 流水线升级使用

实测数据:
- poc 24 concepts: 22 个含行号引用,279 处
- 形式: [slug:start-end] (prose)
"""

import subprocess
import json
import re
import os
from pathlib import Path
from collections import defaultdict

LINE_CITE_RE = re.compile(r'\[([^\]]+?):(\d+)-(\d+)\]')


def get_poc_files():
    pj_root = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")

    result = subprocess.run(
        ["git", "-C", str(pj_root), "ls-tree", "--name-only", "-z",
         "poc/atomicstrata-experiment", "03-执行/poc_atomicstrata/wiki/concepts/"],
        capture_output=True
    )
    raw_files = result.stdout.split(b"\x00")
    files = [f.decode("utf-8") for f in raw_files if f.endswith(b".md")]

    concepts = {}
    for f in files:
        content = subprocess.run(
            ["git", "-C", str(pj_root), "show",
             f"poc/atomicstrata-experiment:{f}"],
            capture_output=True, text=True
        ).stdout
        concepts[os.path.basename(f)] = content
    return concepts


def analyze_poc():
    print("=" * 75)
    print("T-13 Sources[] 行号引用 升级分析(poc 24 concepts)")
    print("=" * 75)

    concepts = get_poc_files()
    print(f"\n读取 {len(concepts)} 个 poc 概念文件")

    total_files_with_cite = 0
    total_citations = 0
    source_usage = defaultdict(int)

    for name, content in concepts.items():
        matches = LINE_CITE_RE.findall(content)
        if matches:
            total_files_with_cite += 1
            total_citations += len(matches)
            for slug, s, e in matches:
                source_usage[slug] += 1

    print(f"含行号引用: {total_files_with_cite} / {len(concepts)}")
    print(f"总引用数: {total_citations}")
    print()
    print("Top 5 被引用 sources:")
    for slug, count in sorted(source_usage.items(), key=lambda x: -x[1])[:5]:
        slug_short = slug[:50] + '...' if len(slug) > 50 else slug
        print(f"   {count:>3} 处: {slug_short}")

    return concepts, source_usage


def generate_plan(concepts, source_usage):
    print()
    print("=" * 75)
    print("📋 升级计划(王老师拍板)")
    print("=" * 75)
    print()
    print("已就绪:")
    print(f"  - poc 分支 22 个 concept 含行号引用,共 279 处")
    print(f"  - 共引用 {len(source_usage)} 个 source files")
    print()
    print("升级方案:")
    print("  A. 直接迁移到主 wiki(concepts/ 目录)")
    print("       - 优点:王老师立即可用")
    print("       - 风险:覆盖 s4-s12 已有 137 concepts")
    print("  B. 升级 atomicstrata compile 输出结构化 frontmatter")
    print("       - 优点:不破坏现状 + 升级流水线")
    print("       - 时间:实现 + 跑批 + 升级 = 半天")
    print("  C. 不升级,保留 poc 分支现状")
    print("       - 优点:最安全")

    plan = {
        'poc_files': len(concepts),
        'files_with_citations': sum(1 for c in concepts.values() if LINE_CITE_RE.search(c)),
        'total_citations': sum(len(LINE_CITE_RE.findall(c)) for c in concepts.values()),
        'unique_sources': len(source_usage),
        'options': ['A. 迁移', 'B. 升级流水线', 'C. 保留'],
    }
    Path('/tmp/pj102-t13-upgrade-plan.json').write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"\n输出: /tmp/pj102-t13-upgrade-plan.json")


def main():
    concepts, source_usage = analyze_poc()
    generate_plan(concepts, source_usage)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())