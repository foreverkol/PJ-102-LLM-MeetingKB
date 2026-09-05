#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pj102.py - PJ-102 LLM MeetingKB CLI

王老师 9-05 Superpower 模式 M3 推进:
T-12 CLI 5 子命令 (ingest/compile/query/lint/status)

用法:
    python3 pj102.py ingest <file_or_dir>
    python3 pj102.py compile <topic>
    python3 pj102.py query "<question>"
    python3 pj102.py lint
    python3 pj102.py status
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

PJ_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
SCRIPTS = PJ_ROOT / "03-执行/code"

ENTITY_TYPES = ["meetings", "persons", "concepts", "judgments", "comparisons"]


def cmd_ingest(args):
    """ingest 文件或目录"""
    target = Path(args.target)
    if not target.exists():
        print(f"❌ 目标不存在: {target}")
        return 1

    if target.is_file():
        files = [target]
    else:
        files = list(target.glob("*.md"))

    print(f"📥 Ingest {len(files)} 个文件")
    for f in files:
        size = f.stat().st_size / 1024
        print(f"   {f.name} ({size:.1f} KB)")
    print(f"\n✅ Ingest 完成(模拟 — 实际由 s1-s4 流水线处理)")
    return 0


def cmd_compile(args):
    """compile topic"""
    topic = args.topic
    print(f"🔨 Compile topic: {topic}")
    print(f"   wiki dir: {WIKI_BASE}/{topic}/")
    print(f"   实际由 s12_wiki.py + llm_client.py 处理")
    print(f"✅ Compile 完成(模拟)")
    return 0


def cmd_query(args):
    """query 问题"""
    question = args.question
    print(f"❓ Query: {question}")
    print(f"   实际由 kb_retriever.py 处理(Sprint 19 P1 含 SYNONYMS)")
    print(f"✅ Query 完成(模拟)")
    return 0


def cmd_lint(args):
    """lint wiki"""
    print("🔍 Lint wiki 检查")
    # 实际跑 lint_wiki.py
    lint_script = SCRIPTS / "lint_wiki.py"
    if lint_script.exists():
        r = subprocess.run(["python3", str(lint_script)],
                          capture_output=True, text=True)
        print(r.stdout[:1000])
        return r.returncode
    else:
        print("❌ lint_wiki.py 不存在")
        return 1


def cmd_status(args):
    """status 项目状态"""
    print("=" * 60)
    print("PJ-102 当前状态")
    print("=" * 60)
    print()

    # Wiki 数量
    print("📊 Wiki 数量:")
    for etype in ENTITY_TYPES:
        d = WIKI_BASE / etype
        if d.exists():
            n = len([f for f in d.glob("*.md")])
            print(f"   {etype}: {n} 个")
        else:
            print(f"   {etype}: 0 个")

    # 02-知识库 关键文件
    print()
    print("📂 02-知识库 关键文件:")
    for f in ["CLAUDE.md", "meetings.base", "persons.base",
              "concepts.base", "judgments.base", "index.md", "log.md"]:
        p = WIKI_BASE / f
        if p.exists():
            print(f"   ✅ {f} ({p.stat().st_size} B)")
        else:
            print(f"   ❌ {f} 不存在")

    # git 状态
    print()
    print("🔧 Git 状态:")
    os.chdir(PJ_ROOT)
    r = subprocess.run(["git", "branch", "--show-current"],
                       capture_output=True, text=True)
    print(f"   分支: {r.stdout.strip()}")
    r = subprocess.run(["git", "rev-list", "--count", "main..HEAD"],
                       capture_output=True, text=True)
    print(f"   ahead of main: {r.stdout.strip()} commits")
    r = subprocess.run(["git", "status", "--short"],
                       capture_output=True, text=True)
    dirty = len([l for l in r.stdout.strip().split('\n') if l])
    print(f"   脏区: {dirty} 项")

    return 0


def main():
    parser = argparse.ArgumentParser(description="PJ-102 LLM MeetingKB CLI")
    subparsers = parser.add_subparsers(dest='cmd')

    # ingest
    p_ingest = subparsers.add_parser('ingest', help='ingest file or dir')
    p_ingest.add_argument('target', help='file or directory')
    p_ingest.set_defaults(func=cmd_ingest)

    # compile
    p_compile = subparsers.add_parser('compile', help='compile topic')
    p_compile.add_argument('topic', help='topic name')
    p_compile.set_defaults(func=cmd_compile)

    # query
    p_query = subparsers.add_parser('query', help='query question')
    p_query.add_argument('question', help='question string')
    p_query.set_defaults(func=cmd_query)

    # lint
    p_lint = subparsers.add_parser('lint', help='lint wiki')
    p_lint.set_defaults(func=cmd_lint)

    # status
    p_status = subparsers.add_parser('status', help='project status')
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())