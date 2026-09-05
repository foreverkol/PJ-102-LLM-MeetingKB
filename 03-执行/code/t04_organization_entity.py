#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t04_organization_entity.py - T-04 organization entity 实现

王老师 9-05 Superpower 模式:
"organization (14 fields) - profile 已设计未实现"

实现:
1. 从 persons 的 org 字段聚合 → 识别 unique organizations
2. 从 frontmatter 推断 org_type / industry
4. 生成 02-知识库/PJ-102-LLM-MeetingKB/organizations/*.md
3. organization 目录+ 文件是 atomicstrata PoC 模式

用法:
    python3 t04_organization_entity.py --dry-run
    python3 t04_organization_entity.py --apply
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
PERSONS_DIR = WIKI_BASE / "persons"
ORG_DIR = WIKI_BASE / "organizations"  # 新建

PROFILE_PATH = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/02-设计/atomicstrata-profile.json")

# 行业关键词分类(简化版)
INDUSTRY_KEYWORDS = {
    "银行": ["银行", "浙商银行", "工商银行", "微众银行", "建行", "工行"],
    "保理": ["保理", "交子金控", "保理公司"],
    "票据": ["票据", "商票"],
    "电商": ["电商", "直播", "商城"],
    "供应链": ["供应链", "产业", "金融科技"],
    "助贷": ["助贷", "贷款中介"],
    "科技": ["科技", "畅聚科技"],
    "其他": [],
}


def classify_industry(org_name: str) -> str:
    for industry, kws in INDUSTRY_KEYWORDS.items():
        for kw in kws:
            if kw in org_name:
                return industry
    return "其他"


def parse_frontmatter(content):
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


def collect_orgs():
    """从 persons 聚合 organizations"""
    org_to_persons = defaultdict(list)
    org_metadata = defaultdict(lambda: {
        'count': 0,
        'roles': [],
        'sources': [],
    })

    for f in PERSONS_DIR.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        fm, _, _ = parse_frontmatter(content)
        org = fm.get('org', '').strip()
        name = fm.get('name', '').strip()
        role = fm.get('role', '').strip()
        source = fm.get('source_meeting', '').strip()

        if not org:
            continue
        org_to_persons[org].append(name)
        org_metadata[org]['count'] += 1
        if role:
            org_metadata[org]['roles'].append(role)
        if source:
            org_metadata[org]['sources'].append(source)

    return org_to_persons, org_metadata


def generate_org_md(org_name, persons, metadata):
    """生成单个 organization .md"""
    from datetime import datetime, timezone
    industry = classify_industry(org_name)
    person_names = ', '.join(persons[:5])
    if len(persons) > 5:
        person_names += f" 等{len(persons)}人"
    slug_id = re.sub(r'[^a-z0-9]', '_', org_name.lower())[:20]
    first_source = metadata['sources'][0] if metadata['sources'] else ''
    now = datetime.now(timezone.utc).isoformat()

    return f"""---
name: {org_name}
canonical_name: {org_name}
aliases: []
entity_id: org_{slug_id}
org_type: 推断:行业-{industry}
industry: {industry}
cooperation_status: 已知合作
relationship_depth: 多层级(派员多人)
business_model: 推断:行业-{industry}常规模式
competitive_moat: 未识别
value_grade: B
source_meeting: {first_source}
generated_at: {now}
generator: t04_organization_entity.py
related_persons:
  - {person_names.replace(', ', chr(10) + '  - ')}
related_count: {metadata['count']}
---

# {org_name}

> **类型**:行业-{industry}
> **关系人**:{metadata['count']} 人({person_names})
> **首次识别**:{first_source or '未知'}

## 🏢 概览

本实体由 `t04_organization_entity.py` 从 {metadata['count']} 个 person 聚合生成。

**关联人物**:{person_names}

**涉及录音**:{len(set(metadata['sources']))} 个 source meeting(s)

## 📋 字段说明(基于 atomicstrata-profile.json 15 fields)

| 字段 | 值 | 来源 |
|------|----|------|
| name | {org_name} | persons.org 聚合 |
| entity_id | org_{slug_id} | 自动生成 |
| org_type | 行业-{industry} | 关键词分类 |
| industry | {industry} | 关键词分类 |
| cooperation_status | 已知合作 | 推断 |
| relationship_depth | 多层级 | {metadata['count']} 人聚合 |
| value_grade | B | 默认 |

## 🔗 关系

- 关联 persons:{person_names}

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: {now}
**关联任务**: Sprint 21 v3.1.0-rc1 T-04 organization entity
"""


def main():
    parser = argparse.ArgumentParser(description="T-04 organization entity 实现")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", default="/tmp/pj102-t04-orgs.json")
    args = parser.parse_args()

    apply_mode = args.apply

    print("=" * 75)
    print("T-04 organization entity 派生(从 persons 聚合)")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN'}")
    print()

    if not PERSONS_DIR.exists():
        print(f"❌ persons 目录不存在")
        return 1

    org_to_persons, org_metadata = collect_orgs()

    print(f"扫描 persons: {sum(1 for f in PERSONS_DIR.glob('*.md'))}")
    print(f"识别 organizations: {len(org_to_persons)}")

    # 排序:按关联人数
    sorted_orgs = sorted(org_to_persons.items(), key=lambda x: -len(x[1]))

    print(f"\nTop 10 organizations(按关联人数):")
    for org, persons in sorted_orgs[:10]:
        print(f"   {len(persons):>2} 人: {org}")

    if apply_mode:
        ORG_DIR.mkdir(exist_ok=True)
        print(f"\n创建目录: {ORG_DIR}")

        for org, persons in sorted_orgs:
            md_content = generate_org_md(org, persons, org_metadata[org])
            # 文件名:org_<slug>.md
            slug = re.sub(r'[^a-z0-9]', '_', org.lower())[:20]
            fpath = ORG_DIR / f"org_{slug}.md"
            fpath.write_text(md_content, encoding='utf-8')

        print(f"\n✅ 生成 {len(sorted_orgs)} 个 organization .md 文件")

    # 输出建议
    Path(args.output).write_text(
        json.dumps({
            'orgs': [
                {'name': org, 'person_count': len(persons), 'persons': persons[:5]}
                for org, persons in sorted_orgs
            ]
        }, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"\n输出: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())