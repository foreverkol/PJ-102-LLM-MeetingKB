#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t13_structured_writer.py - A3 修复: t13 行号引用 真升级

Codex 评审 H4 准确:原 t13 只分析没真升级
A3 修复策略:不覆盖主 wiki,从 poc 分支读 24 concepts,
生成结构化 frontmatter 字段 sources_line_citations,写入
新目录 02-知识库/PJ-102-LLM-MeetingKB/concepts_poc_structured/

这样王老师可对比新旧,决定是否迁移
用法:
    python3 t13_structured_writer.py --dry-run
    python3 t13_structured_writer.py --apply
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

PJ_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
POC_NEW_DIR = WIKI_BASE / "concepts_poc_structured"  # A3 新输出目录

LINE_CITE_RE = re.compile(r'\[([^\]]+?):(\d+)-(\d+)\]')


def get_poc_files():
    """从 poc 分支读 24 concepts"""
    result = subprocess.run(
        ["git", "-C", str(PJ_ROOT), "ls-tree", "--name-only", "-z",
         "poc/atomicstrata-experiment", "03-执行/poc_atomicstrata/wiki/concepts/"],
        capture_output=True
    )
    files = [f.decode('utf-8') for f in result.stdout.split(b'\x00') if f.endswith(b'.md')]

    concepts = {}
    for f in files:
        content = subprocess.run(
            ["git", "-C", str(PJ_ROOT), "show", f"poc/atomicstrata-experiment:{f}"],
            capture_output=True, text=True
        ).stdout
        concepts[os.path.basename(f)] = content
    return concepts


def extract_structured_citations(body: str):
    """从 body 提取行号引用 → 结构化"""
    citations = []
    for m in LINE_CITE_RE.finditer(body):
        citations.append({
            'slug': m.group(1),
            'line_start': int(m.group(2)),
            'line_end': int(m.group(3)),
            'context': '',  # 占位,王老师后续填
        })
    return citations


def add_structured_field(content: str, citations: list, poc_filename: str) -> str:
    """在 frontmatter 加 sources_line_citations 字段
    不会损坏原 frontmatter(只追加)
    """
    if not content.startswith('---'):
        return content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    raw_fm = parts[1]
    body = parts[2]

    # 跳过已有 sources_line_citations
    if 'sources_line_citations:' in raw_fm:
        return content

    # YAML 格式输出
    yaml_lines = ['sources_line_citations:']
    for c in citations:
        yaml_lines.append(f"  - slug: \"{c['slug']}\"")
        yaml_lines.append(f"    line_start: {c['line_start']}")
        yaml_lines.append(f"    line_end: {c['line_end']}")
        yaml_lines.append(f"    context: \"{c['context']}\"")

    yaml_lines.append(f"generator: t13_structured_writer.py")
    yaml_lines.append(f"structured_at: \"{datetime.now(timezone.utc).isoformat()}\"")
    yaml_lines.append(f"structured_from: \"{poc_filename}\"")

    new_fm = raw_fm.rstrip() + '\n' + '\n'.join(yaml_lines)
    return content.replace(raw_fm, new_fm, 1)


def main():
    parser = argparse.ArgumentParser(description="A3 t13 行号引用真升级")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    apply_mode = args.apply

    print("=" * 75)
    print("A3 t13 行号引用真升级 (Codex 评审 H4 修复)")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN'}")
    print(f"输出目录: {POC_NEW_DIR}")
    print(f"策略: 不覆盖主 wiki,生成新目录 concepts_poc_structured/")
    print()

    concepts = get_poc_files()
    print(f"读 poc {len(concepts)} 个 concept 文件")

    processed = 0
    skipped = 0
    errors = 0

    for name, content in concepts.items():
        citations = extract_structured_citations(content)
        if not citations:
            skipped += 1
            continue

        new_content = add_structured_field(content, citations, name)

        # 验证 YAML 仍可解析(避免 H1 重蹈)
        try:
            import yaml
            parts = new_content.split('---', 2)
            yaml.safe_load(parts[1])
        except Exception as e:
            errors += 1
            print(f"   YAML 校验失败: {name}: {e}")
            continue

        if apply_mode:
            POC_NEW_DIR.mkdir(exist_ok=True)
            fp = POC_NEW_DIR / name
            fp.write_text(new_content, encoding='utf-8')
        processed += 1

    print(f"\n处理结果:")
    print(f"   processed: {processed}")
    print(f"   skipped (无引用): {skipped}")
    print(f"   errors (YAML 校验): {errors}")

    if apply_mode:
        print(f"\n[OK] 已生成 {processed} 个结构化文件")
        print(f"   路径: {POC_NEW_DIR}")
        print(f"   王老师决定是否合并到主 concepts/")
    else:
        print(f"\n[DRY-RUN] 如要应用: --apply")

    return 0


if __name__ == "__main__":
    sys.exit(main())