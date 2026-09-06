#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
citations2wiki.py - BT-14 L2.5 工具: citations 层 → wiki 层

王老师 2026-09-06 '按推荐执行 L2.5':
  - 把 citations tier 编译为 wiki tier
  - 按 type 分组成 wiki 实体卡

用法:
    python3 scripts/citations2wiki.py --type <type>     # 按类型分组
    python3 scripts/citations2wiki.py --all [--limit N]  # 全部编译
    python3 scripts/citations2wiki.py --report           # 报告 citations 状态
"""
import argparse
import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

import yaml

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")


def get_citations_by_type() -> dict:
    """按 type 分组获取 citations"""
    citations_by_type = defaultdict(list)
    for md_file in WIKI_ROOT.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            fm_text = content.split("---", 2)[1]
            fm = yaml.safe_load(fm_text) or {}
            if fm.get("tier") == "citations":
                cite_type = fm.get("type", "unknown")
                citations_by_type[cite_type].append({
                    "path": str(md_file.relative_to(WIKI_ROOT)),
                    "fm": fm
                })
        except Exception:
            continue
    return citations_by_type


def generate_wiki_card(cite_type: str, citations: list) -> Path:
    """从一组 citations 生成 wiki 实体卡"""
    safe_type = cite_type.replace(" ", "_").lower()
    output = WIKI_ROOT / "wiki" / f"compiled_{safe_type}.md"
    output.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在

    metadata = {
        "title": f"Compiled: {cite_type}",
        "type": "wiki_entity",
        "citation_count": len(citations),
        "sources": [c["fm"].get("raw_source") for c in citations[:10]],
        "tier": "wiki",
        "compiled_at": "2026-09-06"
    }

    # 内容:列出所有来源 + 关键判断
    lines = [
        f"# {cite_type} 汇总",
        "",
        f"**来源数**:{len(citations)}",
        f"**类型**:{cite_type}",
        "",
        "## 来源列表",
        ""
    ]
    for c in citations[:20]:
        src = c["fm"].get("raw_source", "?")
        offset = c["fm"].get("offset", 0)
        lines.append(f"- `{src}` (offset: {offset})")

    if len(citations) > 20:
        lines.append(f"- ... (还有 {len(citations) - 20} 个)")

    content = f"""---
{json.dumps(metadata, ensure_ascii=False, indent=2)}
---

{chr(10).join(lines)}
"""
    output.write_text(content, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description="citations → wiki 编译器")
    parser.add_argument("--type", help="按 type 分组编译")
    parser.add_argument("--all", action="store_true", help="编译所有 types")
    parser.add_argument("--limit", type=int, default=100, help="每类型 citation 限制")
    parser.add_argument("--report", action="store_true", help="报告 citations 状态")
    args = parser.parse_args()

    if args.report:
        citations = get_citations_by_type()
        print(f"📊 citations 层统计:")
        print(f"   总 type 数:{len(citations)}")
        for t, cs in sorted(citations.items(), key=lambda x: -len(x[1])):
            print(f"   {t}:{len(cs)} citations")
        return

    citations = get_citations_by_type()

    if args.type:
        if args.type not in citations:
            print(f"❌ type '{args.type}' 不存在")
            print(f"   可用 types: {list(citations.keys())}")
            return
        cites = citations[args.type][:args.limit]
        saved = generate_wiki_card(args.type, cites)
        print(f"✅ 编译:{saved.name} ({len(cites)} citations)")
        return

    if args.all:
        print(f"🔄 编译所有 {len(citations)} 个 types → wiki")
        for t, cs in citations.items():
            cites = cs[:args.limit]
            saved = generate_wiki_card(t, cites)
            print(f"   ✅ {saved.name} ({len(cites)} citations)")
        return

    parser.print_help()


if __name__ == "__main__":
    main()