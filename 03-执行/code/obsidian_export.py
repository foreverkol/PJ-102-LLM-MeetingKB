#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsidian_export.py - Obsidian Bases .base + CLAUDE.md 自动生成器

王老师 9-05 OUT-OF-BAND:
"充分利用实现 obsidian 功能和能力,更好发挥知识库构建定位和价值"

Sprint 21 v3.1.0-rc1 T-08 落地

用法:
    python3 obsidian_export.py                    # 生成所有
    python3 obsidian_export.py --type meetings    # 只生成 meetings.base
    python3 obsidian_export.py --type all --verbose
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 默认路径(L4.3a 阶段 A:支持 argparse + 环境变量覆盖)
DEFAULT_WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
DEFAULT_SCHEMA_PATH = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/02-设计/atomicstrata-profile.json")

# 优先级:argparse --wiki-base > 环境变量 PJ102_WIKI_BASE > 默认
WIKI_BASE = Path(os.environ.get("PJ102_WIKI_BASE", str(DEFAULT_WIKI_BASE)))
SCHEMA_PATH = Path(os.environ.get("PJ102_SCHEMA_PATH", str(DEFAULT_SCHEMA_PATH)))


def human_size(n: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def parse_frontmatter(md_path: Path) -> dict:
    try:
        content = md_path.read_text(encoding='utf-8')
    except Exception:
        return {}
    if not content.startswith('---'):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm


def get_md_files(entity_dir: Path) -> list:
    files = []
    if not entity_dir.exists():
        return files
    for f in sorted(entity_dir.glob("*.md")):
        fm = parse_frontmatter(f)
        if fm:
            files.append((f, fm))
    return files


BASE_TEMPLATES = {
    'meetings': '''filters:
  and:
    - file.folder == "meetings"
    - file.ext == "md"
formulas:
  status_label: if(status_stage = "compiled", "Done", "InProgress")
views:
  - type: table
    name: AllMeetings
    order:
      - file.name
      - meeting_type
      - value_grade
      - status_label
      - date
    groupBy:
      property: meeting_type
  - type: kanban
    name: ByStatus
    groupBy:
      property: status_stage
  - type: cards
    name: CardView
    order:
      - file.name
      - meeting_type
      - cover
''',
    'persons': '''filters:
  and:
    - file.folder == "persons"
    - file.ext == "md"
formulas:
  role_short: if(role = "", "Unspecified", role)
views:
  - type: table
    name: AllPersons
    order:
      - file.name
      - role_short
      - relationship
      - source_meeting
  - type: cards
    name: CardView
    order:
      - file.name
      - role_short
''',
    'concepts': '''filters:
  and:
    - file.folder == "concepts"
    - file.ext == "md"
formulas:
  definition_short: if(definition = "", "Undefined", definition)
views:
  - type: table
    name: AllConcepts
    order:
      - file.name
      - definition_short
      - source_meeting
    groupBy:
      property: source_meeting
  - type: cards
    name: CardView
    order:
      - file.name
      - definition_short
''',
    'judgments': '''filters:
  and:
    - file.folder == "judgments"
    - file.ext == "md"
views:
  - type: table
    name: AllJudgments
    order:
      - file.name
      - source_meeting
  - type: cards
    name: CardView
''',
}


def generate_claude_md() -> str:
    if not SCHEMA_PATH.exists():
        return "# CLAUDE.md\n\n(02-设计/atomicstrata-profile.json does not exist)"

    with open(SCHEMA_PATH, encoding='utf-8') as f:
        profile = json.load(f)

    entities = profile.get('entities', {})
    relations = profile.get('relations', [])

    lines = [
        "# PJ-102-LLM-MeetingKB · CLAUDE.md Schema",
        "",
        "> **王老师 9-05 OUT-OF-BAND**:Karpathy LLM Wiki + Obsidian dual-core positioning",
        "> **Auto-generated** from 02-设计/atomicstrata-profile.json",
        f"> **Generated**:{datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## 8 Entities Schema",
        "",
        "| Entity | Directory | Key Fields |",
        "|--------|-----------|------------|",
    ]

    for ename, edef in entities.items():
        directory = edef.get('directory', 'N/A')
        fields = ', '.join(edef.get('fields', [])[:5])
        required = edef.get('required', [])
        lines.append(f"| **{ename}** | `{directory}` | {fields}... |")
        if required:
            lines.append(f"|  required | | {', '.join(required)} |")
        lines.append("")

    lines.extend([
        f"## {len(relations)} Relations",
        "",
        "(Auto-generated from atomicstrata-profile.json)",
        "",
        "---",
        "",
        "## Usage",
        "",
        "1. Open Obsidian and select `02-知识库/PJ-102-LLM-MeetingKB/` as Vault",
        "2. Open `meetings.base` / `persons.base` / `concepts.base` / `judgments.base`",
        "3. Browse `meetings/` `persons/` `concepts/` `judgments/` directories",
        "4. Use Dataview blocks embedded in wiki pages for queries",
        "",
        "## Directory Structure",
        "",
        "```",
        "02-知识库/PJ-102-LLM-MeetingKB/",
        "  CLAUDE.md            # this file (auto-generated)",
        "  index.md             # global index (Sprint 18 P0)",
        "  log.md               # operation log (Sprint 19 P1)",
        "  meetings.base        # Bases dashboard",
        "  persons.base         # Bases dashboard",
        "  concepts.base        # Bases dashboard",
        "  judgments.base       # Bases dashboard",
        "  meetings/            # meeting wiki",
        "  persons/             # person wiki",
        "  concepts/            # concept wiki",
        "  judgments/           # judgment wiki",
        "```",
        "",
        "---",
        "",
        "## Meta",
        "",
        f"- Generator: 03-执行/code/obsidian_export.py",
        f"- Source: 02-设计/atomicstrata-profile.json (8 entities)",
        f"- Atomicstrata PoC: poc/atomicstrata-experiment branch",
        f"- PJ-102 version: v3.0.1-stable + Sprint 21 v3.1.0-rc1",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Obsidian Bases .base auto-generator")
    parser.add_argument("--type", choices=list(BASE_TEMPLATES.keys()) + ['all'],
                       default='all', help="Entity type to generate")
    parser.add_argument("--wiki-base", default=str(WIKI_BASE),
                       help="Wiki base path (default 02-知识库/PJ-102-LLM-MeetingKB)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    wiki_base = Path(args.wiki_base)
    if not wiki_base.exists():
        print(f"Wiki directory not found: {wiki_base}")
        return 1

    print("=" * 75)
    print("Obsidian Bases .base + CLAUDE.md Auto-Generator")
    print("=" * 75)
    print(f"Wiki base: {wiki_base}")
    print()

    # Generate .base files
    generated = []
    types = list(BASE_TEMPLATES.keys()) if args.type == 'all' else [args.type]

    entity_dirs = {
        'meetings': 'meetings/',
        'persons': 'persons/',
        'concepts': 'concepts/',
        'judgments': 'judgments/',
    }

    for tname in types:
        entity_dir = wiki_base / entity_dirs[tname]
        md_files = get_md_files(entity_dir)
        base_file = wiki_base / f"{tname}.base"
        base_file.write_text(BASE_TEMPLATES[tname], encoding='utf-8')
        generated.append((tname, len(md_files), base_file))
        print(f"OK {tname}.base generated ({len(md_files)} wiki sources)")

    # Generate CLAUDE.md
    claude_md_path = wiki_base / "CLAUDE.md"
    claude_content = generate_claude_md()
    claude_md_path.write_text(claude_content, encoding='utf-8')
    print(f"\nOK CLAUDE.md generated ({human_size(len(claude_content.encode('utf-8')))} B)")

    # Statistics
    print()
    print("=" * 75)
    print("Generation Complete - Statistics")
    print("=" * 75)
    print(f"  .base files: {len(generated)}")
    for tname, n, path in generated:
        print(f"     - {path.name} (source: {n} wiki)")
    print(f"  CLAUDE.md: 1")
    print(f"  Total wiki sources: {sum(n for _, n, _ in generated)}")

    if args.verbose:
        print()
        print("Preview of meetings.base:")
        print("-" * 40)
        print(BASE_TEMPLATES['meetings'])

    return 0


if __name__ == "__main__":
    sys.exit(main())
