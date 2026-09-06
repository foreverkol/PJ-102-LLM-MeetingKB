#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tier_classifier.py - BT-14 三层架构核心工具

王老师 2026-09-06 '按推荐执行 L2 BT-14':
  - 三层架构: raw → citations → wiki (逻辑分层)
  - 用 frontmatter tier 字段标识,不强制物理目录
  - 向后兼容:7 个现有目录保留

用法:
    python3 scripts/tier_classifier.py scan              # 扫描现有文件
    python3 scripts/tier_classifier.py assign-tier <file> <tier>  # 指定 tier
    python3 scripts/tier_classifier.py add-frontmatter <file>     # 自动添加 tier 字段
    python3 scripts/tier_classifier.py report            # 三层分布报告
    python3 scripts/tier_classifier.py stats             # 统计信息
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")

# 物理目录 → tier 映射(逻辑分层,实际由 frontmatter 控制)
PHYSICAL_DIR_TIER = {
    "raw_clips": "raw",  # Web Clipper 原始剪藏
    "judgments": "citations",
    "scenarios": "citations",
    "concepts_poc_structured": "citations",
    "meetings": "wiki",
    "concepts": "wiki",
    "persons": "wiki",
}


def extract_frontmatter(content: str) -> tuple:
    """提取 frontmatter"""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        import yaml
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        # 简单 key: value 解析
        fm = {}
        for line in parts[1].strip().split("\n"):
            if ":" in line and not line.startswith("#"):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
    body = parts[2]
    return fm, body


def add_tier_frontmatter(file_path: Path, tier: str) -> bool:
    """添加 tier 字段到 frontmatter"""
    content = file_path.read_text(encoding="utf-8")
    fm, body = extract_frontmatter(content)

    if "tier" in fm:
        if fm["tier"] == tier:
            return False
        fm["tier"] = tier
    else:
        fm["tier"] = tier

    # 重新生成 frontmatter
    new_lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, str) and ":" in v:
            new_lines.append(f'{k}: "{v}"')
        elif isinstance(v, list):
            new_lines.append(f"{k}:")
            for item in v:
                new_lines.append(f"  - {item}")
        else:
            new_lines.append(f"{k}: {v}")
    new_lines.append("---")

    new_content = "\n".join(new_lines) + body
    file_path.write_text(new_content, encoding="utf-8")
    return True


def infer_tier(file_path: Path) -> str:
    """根据物理目录推断 tier"""
    for parent in file_path.parents:
        if parent.name in PHYSICAL_DIR_TIER:
            return PHYSICAL_DIR_TIER[parent.name]
    return "unknown"


def scan_files() -> list:
    """扫描所有 MD 文件,提取 tier 信息"""
    results = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            fm, _ = extract_frontmatter(content)
            tier = fm.get("tier") or infer_tier(md_file)
            results.append({
                "path": str(md_file.relative_to(WIKI_ROOT)),
                "tier": tier,
                "has_frontmatter": bool(fm),
                "physical_dir": md_file.parent.name,
                "size": md_file.stat().st_size
            })
        except Exception as e:
            results.append({
                "path": str(md_file.relative_to(WIKI_ROOT)),
                "tier": "error",
                "error": str(e)
            })
    return results


def report(files: list = None) -> dict:
    """生成三层分布报告"""
    if files is None:
        files = scan_files()

    tier_counts = Counter(f["tier"] for f in files)
    dir_tier = defaultdict(Counter)
    for f in files:
        dir_tier[f.get("physical_dir", "?")][f["tier"]] += 1

    report = {
        "total": len(files),
        "by_tier": dict(tier_counts),
        "by_dir_tier": {k: dict(v) for k, v in dir_tier.items()},
        "files_with_frontmatter": sum(1 for f in files if f.get("has_frontmatter")),
        "files_without_frontmatter": sum(1 for f in files if not f.get("has_frontmatter")),
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="BT-14 三层架构 tier 分类器")
    parser.add_argument("command", choices=["scan", "assign-tier", "add-frontmatter", "report", "stats"],
                       help="子命令")
    parser.add_argument("file", nargs="?", help="目标文件(assign-tier/add-frontmatter)")
    parser.add_argument("tier", nargs="?", choices=["raw", "citations", "wiki"],
                       help="目标 tier(assign-tier)")
    parser.add_argument("--all", action="store_true", help="应用到所有文件")
    args = parser.parse_args()

    if args.command == "scan":
        files = scan_files()
        print(f"📊 扫描 {len(files)} 个文件:")
        for f in files[:20]:
            tier = f.get("tier", "?")
            fm = "✅" if f.get("has_frontmatter") else "❌"
            print(f"  {fm} [{tier:10}] {f['path']}")
        if len(files) > 20:
            print(f"  ... (还有 {len(files) - 20} 个)")

    elif args.command == "assign-tier":
        if not args.file or not args.tier:
            print("用法: assign-tier <file> <tier>")
            sys.exit(1)
        file_path = WIKI_ROOT / args.file
        if not file_path.exists():
            print(f"文件不存在: {file_path}")
            sys.exit(1)
        success = add_tier_frontmatter(file_path, args.tier)
        print(f"{'✅ 更新' if success else '⚠️ 已存在'}: {args.file} → {args.tier}")

    elif args.command == "add-frontmatter":
        if args.all:
            files = scan_files()
            updated = 0
            for f in files:
                if not f.get("has_frontmatter") or "tier" not in (f.get("tier") or ""):
                    path = WIKI_ROOT / f["path"]
                    tier = f.get("tier", "unknown")
                    if tier != "unknown":
                        if add_tier_frontmatter(path, tier):
                            updated += 1
            print(f"✅ 已为 {updated} 个文件添加 tier frontmatter")
        else:
            print("用法: add-frontmatter --all")

    elif args.command == "report" or args.command == "stats":
        files = scan_files()
        r = report(files)
        print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()