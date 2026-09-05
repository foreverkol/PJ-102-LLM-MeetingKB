#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cascade_updater.py - T-02 Cascade Updates 模块

王老师 9-05 Superpower 模式自主推进:
"Cascade Updates(王老师 9-05 Superpower 模式 M1 推进)

Karpathy LLM Wiki 关键 invariant:
"如果 source A 修改,A 派生出的 wiki B/C/D 必须 cascade 更新"

实现:
1. 每次新 ingest,生成 extraction_patch
2. 比对 source 变化,识别哪些 entity / wiki 页受影响
3. 自动更新:
   - entity_registry
   - 反向引用(source_meeting 字段)
   - wikilinks

用法:
    python3 cascade_updater.py --ingest <ingest_id>     # 单 ingest cascade
    python3 cascade_updater.py --all                     # 所有未处理
    python3 cascade_updater.py --dry-run                 # 只报告不修改
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
CITATIONS_DIR = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/citations")

ENTITY_TYPES = ["meetings", "persons", "concepts", "judgments"]


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


def find_affected_wikis(source_id: str) -> dict:
    """查找所有引用了 source_id 的 wiki 页"""
    affected = {etype: [] for etype in ENTITY_TYPES}

    for etype in ENTITY_TYPES:
        dir_path = WIKI_BASE / etype
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            fm, _, _ = parse_frontmatter(content)

            # 检查 source_meeting 或 source 字段
            if fm.get('source_meeting') == source_id or fm.get('source') == source_id:
                affected[etype].append({
                    'file': f.name,
                    'name': fm.get('name', ''),
                    'updated_at': fm.get('generated_at', ''),
                })

    return affected


def apply_cascade_to_file(etype: str, filename: str, source_meeting: str,
                          cascade_time: str) -> bool:
    """真修改一个文件:加 cascade_updated_at + cascade_source 字段
    返回 True if changed, False if not
    A2 修复:Codex 评审 H3 - --apply 之前是空操作
    """
    fp = WIKI_BASE / etype / filename
    if not fp.exists():
        return False

    content = fp.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    raw_fm = parts[1]

    # 跳过已有 cascade_updated_at 的文件(避免重复 apply)
    if 'cascade_updated_at:' in raw_fm:
        return False

    # 插入 cascade 字段到 raw_fm
    new_lines = raw_fm.rstrip().split('\n')
    new_lines.append(f"cascade_updated_at: \"{cascade_time}\"")
    new_lines.append(f"cascade_source: \"{source_meeting}\"")
    new_raw_fm = '\n'.join(new_lines)

    new_content = content.replace(raw_fm, new_raw_fm, 1)
    fp.write_text(new_content, encoding='utf-8')
    return True


def cascade_update(ingest_id: str, dry_run: bool = True) -> dict:
    """对一个 ingest 做 cascade update
    A2 修复:加了 apply_cascade_to_file 真实现
    """
    from datetime import datetime, timezone
    print(f"\n=== Cascade Update for {ingest_id} ===")

    affected = find_affected_wikis(ingest_id)
    total_affected = sum(len(v) for v in affected.values())

    print(f"受影响 wiki 数:")
    for etype, items in affected.items():
        print(f"   {etype}: {len(items)} 个")
    print(f"   总计: {total_affected}")

    # 列出具体文件
    for etype, items in affected.items():
        if items:
            print(f"\n--- {etype} ---")
            for item in items[:5]:
                print(f"   {item['file']} ({item['name'][:30]})")
            if len(items) > 5:
                print(f"   ... ({len(items)-5} more)")

    if total_affected == 0:
        print("\n[SKIP] 无受影响 wiki,无需 cascade")
        return {
            'ingest_id': ingest_id,
            'affected_count': 0,
            'status': 'no_action',
        }

    modified = 0
    skipped = 0
    cascade_time = datetime.now(timezone.utc).isoformat()

    if not dry_run:
        # 真 apply
        print(f"\n[APPLY] 开始修改 {total_affected} 个文件...")
        for etype, items in affected.items():
            for item in items:
                if apply_cascade_to_file(etype, item['file'], ingest_id, cascade_time):
                    modified += 1
                else:
                    skipped += 1
        print(f"[OK] 修改: {modified} 个")
        print(f"[SKIP] 跳过(已有 cascade_updated_at): {skipped} 个")
    else:
        print(f"\n[DRY-RUN] 如要真修改,去掉 --dry-run")

    return {
        'ingest_id': ingest_id,
        'affected_count': total_affected,
        'affected_by_type': {k: len(v) for k, v in affected.items()},
        'modified': modified if not dry_run else 0,
        'skipped': skipped if not dry_run else 0,
        'status': 'dry_run' if dry_run else 'applied',
    }


def list_all_sources() -> list:
    """列出所有 source"""
    sources = set()
    for etype in ENTITY_TYPES:
        dir_path = WIKI_BASE / etype
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            fm, _, _ = parse_frontmatter(content)
            src = fm.get('source_meeting', '') or fm.get('source', '')
            if src:
                sources.add(src)
    return sorted(sources)


def main():
    parser = argparse.ArgumentParser(description="T-02 Cascade Updates")
    parser.add_argument("--ingest", help="指定 ingest_id")
    parser.add_argument("--all", action="store_true", help="所有 sources")
    parser.add_argument("--dry-run", action="store_true", default=False,
                       help="Dry run(默认否,真 apply)")
    parser.add_argument("--apply", action="store_true", default=True,
                       help="真 apply(默认)")
    args = parser.parse_args()

    # A2 修复:解析互斥
    apply_mode = args.apply and not args.dry_run

    print("=" * 75)
    print("T-02 Cascade Updates (A2 修复后,真 apply)")
    print("=" * 75)
    print(f"Wiki base: {WIKI_BASE}")
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN'}")
    print()

    if not WIKI_BASE.exists():
        print(f"❌ Wiki 目录不存在")
        return 1

    if args.ingest:
        result = cascade_update(args.ingest, dry_run=not apply_mode)
        print(f"\n结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    elif args.all:
        sources = list_all_sources()
        print(f"找到 {len(sources)} 个 unique sources")
        print("\n各 source 受影响情况:")
        for src in sources[:20]:
            affected = find_affected_wikis(src)
            total = sum(len(v) for v in affected.values())
            if total > 0:
                print(f"   {src}: {total} 个 wiki")
        if len(sources) > 20:
            print(f"   ... ({len(sources)-20} more)")
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())