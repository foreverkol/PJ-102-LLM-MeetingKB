#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
raw2citations.py - BT-14 L2.5 工具: raw 层 → citations 层

王老师 2026-09-06 '按推荐执行 L2.5':
  - 把 raw tier 文件提取关键引用,生成 citations
  - 每条 citation = raw_source + offset + original_text + structured_data

用法:
    python3 scripts/raw2citations.py --file <raw_file>       # 单文件提取
    python3 scripts/raw2citations.py --batch [--limit N]      # 批量 raw → citations
    python3 scripts/raw2citations.py --report                # 报告 raw → citations 进度
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
CITATIONS_DIR = WIKI_ROOT  # 物理目录不变,通过 tier 字段标识


def extract_citations_from_raw(raw_file: Path) -> list:
    """从 raw tier 文件提取 citations"""
    if not raw_file.exists():
        return []

    content = raw_file.read_text(encoding="utf-8", errors="ignore")

    # 简单规则抽取:提取 URL/章节标题/关键句子
    citations = []

    # 1. URL 提取
    urls = re.findall(r'https?://[^\s\)\]\>]+', content)
    for i, url in enumerate(urls[:10]):  # 限制 10 条/文件
        offset = content.find(url)
        citations.append({
            "type": "url_reference",
            "raw_source": raw_file.name,
            "offset": offset,
            "original_text": url,
            "structured_data": {"url": url}
        })

    # 2. 标题提取(## 开头)
    headings = re.findall(r'^##?\s+(.+)$', content, re.MULTILINE)
    for heading in headings[:5]:
        citations.append({
            "type": "heading",
            "raw_source": raw_file.name,
            "offset": content.find(heading),
            "original_text": heading,
            "structured_data": {"heading": heading}
        })

    # 3. 关键句子(包含"是"、"为"、"需要" 等判断词)
    sentences = re.split(r'[。！？\n]', content)
    for sent in sentences:
        sent = sent.strip()
        if 20 < len(sent) < 200 and re.search(r'(是|为|需要|应该|必须)', sent):
            citations.append({
                "type": "judgment",
                "raw_source": raw_file.name,
                "offset": content.find(sent),
                "original_text": sent[:200],
                "structured_data": {"judgment": sent[:100]}
            })

    return citations[:20]  # 每文件最多 20 条 citation


def generate_citation_id(raw_name: str, idx: int) -> str:
    """生成 citation ID"""
    base = raw_name.replace(".md", "").replace(" ", "_")[:30]
    return f"cite_{base}_{idx:03d}"


def save_citation(citation: dict, idx: int) -> Path:
    """保存 citation 到 citations/ 目录"""
    cite_id = generate_citation_id(citation["raw_source"], idx)
    output = CITATIONS_DIR / "citations" / f"{cite_id}.md"
    output.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在

    metadata = {
        "type": citation["type"],
        "raw_source": citation["raw_source"],
        "offset": citation["offset"],
        "structured_data": citation["structured_data"],
        "tier": "citations",
        "extracted_at": "2026-09-06"
    }

    content = f"""---
{json.dumps(metadata, ensure_ascii=False, indent=2)}
---

# {citation['type']}: {citation['raw_source']}

**来源**:`{citation['raw_source']}` (offset: {citation['offset']})
**类型**:{citation['type']}

## 原始内容

> {citation['original_text']}

## 结构化数据

```json
{json.dumps(citation['structured_data'], ensure_ascii=False, indent=2)}
```
"""
    output.write_text(content, encoding="utf-8")
    return output


def get_raw_files() -> list:
    """获取所有 raw tier 文件"""
    import yaml
    raw_files = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            fm_text = content.split("---", 2)[1]
            fm = yaml.safe_load(fm_text) or {}
            if fm.get("tier") == "raw":
                raw_files.append(md_file)
        except Exception:
            continue
    return raw_files


def main():
    parser = argparse.ArgumentParser(description="raw → citations 提取器")
    parser.add_argument("--file", help="单个 raw 文件")
    parser.add_argument("--batch", action="store_true", help="批量处理所有 raw 文件")
    parser.add_argument("--limit", type=int, default=10, help="批量处理文件数限制")
    parser.add_argument("--report", action="store_true", help="报告 raw 状态")
    args = parser.parse_args()

    if args.report:
        raw_files = get_raw_files()
        print(f"📊 raw 层统计:")
        print(f"   总 raw 文件数:{len(raw_files)}")
        print(f"   预计 citation 数:{len(raw_files) * 20}")
        for rf in raw_files[:5]:
            print(f"   - {rf.relative_to(WIKI_ROOT)}")
        return

    if args.file:
        # 单文件模式
        file_path = WIKI_ROOT / args.file
        citations = extract_citations_from_raw(file_path)
        print(f"📄 {args.file}:提取 {len(citations)} 条 citations")
        for i, c in enumerate(citations):
            saved = save_citation(c, i + 1)
            print(f"   ✅ {saved.name}")
        return

    if args.batch:
        raw_files = get_raw_files()[:args.limit]
        print(f"🔄 批量提取 {len(raw_files)} 个 raw 文件 → citations")
        total = 0
        for raw_file in raw_files:
            citations = extract_citations_from_raw(raw_file)
            for i, c in enumerate(citations):
                save_citation(c, i + 1)
                total += 1
            print(f"   ✅ {raw_file.name}:{len(citations)} citations")
        print(f"\n🎉 共生成 {total} 条 citations")
        return

    parser.print_help()


if __name__ == "__main__":
    main()