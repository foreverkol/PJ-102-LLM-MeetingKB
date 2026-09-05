#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t01_fix_persons_relationship.py - T-01 persons relationship 字段自动修复

王老师 9-05 Superpower 模式自主推进:
"修 persons 67 个空关联事实" (Sprint 18 P0-2 未真做)

实测 (2026-09-05 22:20):
- persons 总数: 99
- relationship 字段空: 94 (94.9%)
- source_meeting 字段空: 0 (OK)

策略:
1. 从 source_meeting 推断 relationship(粗略分类)
2. 从 file name / body 推断 person type → relationship
3. 提供报告,需要王老师审核

不擅自修改:
- 不能从全文胡乱推断 → 输出建议清单,王老师决定
- 实测重要:用 dry-run 模式

用法:
    python3 t01_fix_persons_relationship.py --dry-run
    python3 t01_fix_persons_relationship.py --apply
"""

import argparse
import json
import os
import sys
from pathlib import Path

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/persons")

# role → relationship 推断规则(粗略分类)
ROLE_TO_RELATIONSHIP = {
    "客户经理": "客户关系",
    "客户": "客户关系",
    "行长": "银行联系人",
    "客户代表": "客户关系",
    "银行": "银行联系人",
    "律师": "法律顾问",
    "财务": "财务联系人",
    "评审人": "评审联系人",
    "": "未分类",
}


def parse_frontmatter(content: str) -> tuple:
    """解析 frontmatter,返回 (fm_dict, body, raw_fm_text)"""
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


def suggest_relationship(fm: dict, body: str, filename: str) -> str:
    """基于 role 字段建议 relationship"""
    role = fm.get('role', '').strip()
    name = fm.get('name', '').strip()

    # 1. 直接匹配
    if role in ROLE_TO_RELATIONSHIP:
        return ROLE_TO_RELATIONSHIP[role]

    # 2. 模糊匹配
    if '行长' in role or '客户经理' in role or '银行' in role:
        return '银行联系人'
    if '客户' in role or '老板' in role or '经理' in role:
        return '客户关系'
    if '律师' in role or '法务' in role:
        return '法律顾问'
    if '财务' in role or '会计' in role:
        return '财务联系人'
    if '评审' in role or '审批' in role:
        return '评审联系人'

    # 3. 兜底
    return '未分类(待人工确认)'


def main():
    parser = argparse.ArgumentParser(description="T-01 persons relationship 自动修复")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="Dry run(默认)")
    parser.add_argument("--apply", action="store_true",
                       help="应用修改")
    parser.add_argument("--output", default="/tmp/pj102-t01-suggestions.json",
                       help="建议输出文件")
    args = parser.parse_args()

    apply_mode = args.apply

    print("=" * 75)
    print("T-01 persons relationship 自动修复")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN(只报告不修改)'}")
    print()

    if not WIKI_BASE.exists():
        print(f"❌ Wiki 目录不存在:{WIKI_BASE}")
        return 1

    suggestions = []
    modified = 0

    for f in sorted(os.listdir(WIKI_BASE)):
        if not f.endswith('.md'):
            continue
        fp = WIKI_BASE / f
        content = fp.read_text(encoding='utf-8')
        fm, body, raw_fm = parse_frontmatter(content)

        # 检查 relationship 是否空
        rel = fm.get('relationship', '').strip()
        # A1 修复:如果 rel 已经是带引号的值(原始文件已存),当作"已存在"跳过
        if rel and rel not in ['unknown', 'N/A', '[]', '{}', '未分类', '']:
            # 已存在有效 relationship,跳过(避免再次破坏 frontmatter)
            continue

        # 推断 relationship
        suggested = suggest_relationship(fm, body, f)

        suggestion = {
            'file': f,
            'name': fm.get('name', ''),
            'role': fm.get('role', ''),
            'current_relationship': rel,
            'suggested_relationship': suggested,
        }
        suggestions.append(suggestion)

        if apply_mode and '未分类' not in suggested:
            # A1 修复:用新 frontmatter 重建而不是 raw_fm 拼接(避免 H1 三引号 bug)
            new_lines = []
            for line in raw_fm.split('\n'):
                # 跳过空的或已经是 relationship 的行
                if line.strip().startswith('relationship:'):
                    continue
                new_lines.append(line)
            new_lines.append(f'relationship: "{suggested}"')
            new_fm = '\n'.join(new_lines)
            new_content = content.replace(raw_fm, new_fm, 1)
            fp.write_text(new_content, encoding='utf-8')
            modified += 1

    # 输出建议
    Path(args.output).write_text(
        json.dumps(suggestions, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    # 统计
    sugg_count = sum(1 for s in suggestions if '未分类' not in s['suggested_relationship'])
    manual_count = sum(1 for s in suggestions if '未分类' in s['suggested_relationship'])

    print(f"扫描文件: {sum(1 for f in os.listdir(WIKI_BASE) if f.endswith('.md'))}")
    print(f"relationship 为空: {len(suggestions)}")
    print(f"  可自动分类: {sugg_count}")
    print(f"  需人工确认: {manual_count}")
    print()
    print(f"输出建议文件: {args.output}")

    if apply_mode:
        print(f"\n✅ 已修改: {modified} 个文件")
    else:
        print(f"\n🔍 Dry-run 完成。如要应用: --apply")

    return 0


if __name__ == "__main__":
    sys.exit(main())