#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t09_dataview_blocks.py - T-09 Dataview 查询块嵌入

王老师 9-05 Superpower 模式:
"Dataview 查询块嵌入 - 充分利用 Obsidian 原生能力"

为每个 wiki 文件底部添加 Dataview 块:
- 同 source_meeting 的其他实体
- related_persons/concepts 的反向引用

用法:
    python3 t09_dataview_blocks.py --dry-run
    python3 t09_dataview_blocks.py --apply
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
ENTITY_TYPES = ["meetings", "persons", "concepts", "judgments"]

# Dataview 块模板
DATAVIEW_TEMPLATES = {
    "persons": """\n## 🔗 相关实体 (Dataview 自动)\n\n```dataview\nLIST\nFROM "{etype}"\nWHERE source_meeting = "{source_meeting}" AND file.name != this.file.name\nSORT file.name ASC\n```\n\n```dataview\nLIST\nFROM "{other_types}"\nWHERE contains(related_persons, "{name}") OR contains(related_persons, this.name)\nLIMIT 10\n```\n""",
    "default": """\n## 🔗 相关实体 (Dataview 自动)\n\n```dataview\nLIST\nFROM "{etype}"\nWHERE source_meeting = "{source_meeting}" AND file.name != this.file.name\nSORT file.name ASC\n```\n""",
}


def parse_frontmatter(content):
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    fm = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2]


def has_dataview_block(body):
    """检查是否已有 dataview 块"""
    return '```dataview' in body


def main():
    parser = argparse.ArgumentParser(description="T-09 Dataview 块嵌入")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    apply_mode = args.apply

    print("=" * 75)
    print("T-09 Dataview 块嵌入")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN'}")
    print()

    if not WIKI_BASE.exists():
        print(f"❌ Wiki 目录不存在")
        return 1

    total = 0
    has_block = 0
    needs_block = 0
    modified = 0

    for etype in ENTITY_TYPES:
        dir_path = WIKI_BASE / etype
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            total += 1
            content = f.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(content)

            if has_dataview_block(body):
                has_block += 1
                continue

            # A4:支持多种 source 字段(meetings 用 source,其他用 source_meeting)
            source_meeting = (fm.get('source_meeting', '') or
                             fm.get('source', '')).strip()
            # 支持多种 name 字段
            name = (fm.get('name', '') or
                    fm.get('title', '') or
                    fm.get('entity_id', '') or
                    fm.get('topic_key', '')).strip()
            if not source_meeting:
                continue

            needs_block += 1
            if apply_mode:
                other_types = ','.join([t for t in ENTITY_TYPES if t != etype])
                if etype == 'persons':
                    block = DATAVIEW_TEMPLATES["persons"].format(
                        etype=etype, source_meeting=source_meeting,
                        other_types=other_types, name=name
                    )
                else:
                    block = DATAVIEW_TEMPLATES["default"].format(
                        etype=etype, source_meeting=source_meeting
                    )
                new_content = content.rstrip() + '\n' + block
                f.write_text(new_content, encoding='utf-8')
                modified += 1

    print(f"扫描文件: {total}")
    print(f"已有 dataview 块: {has_block}")
    print(f"待添加: {needs_block}")

    if apply_mode:
        print(f"\n✅ 已修改: {modified} 个文件")
    else:
        print(f"\n🔍 Dry-run 完成。如要应用: --apply")

    return 0


if __name__ == "__main__":
    sys.exit(main())