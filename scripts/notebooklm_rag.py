#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
notebooklm_rag.py - L4 Web Clipper + NotebookLM RAG 完整化

王老师 2026-09-06 '按推荐执行 L4':
  - Web Clipper 抓 URL → raw_clips/
  - 本脚本:剪藏 → 自动推 NotebookLM → AI 处理结果 → 输出到 wiki

用法:
    python3 scripts/notebooklm_rag.py --setup             # 检查 notebooklm 登录状态
    python3 scripts/notebooklm_rag.py --clip URL          # 抓 URL + 推 NotebookLM
    python3 scripts/notebooklm_rag.py --sync [--limit N]  # 把所有 raw_clips 推到 NotebookLM
    python3 scripts/notebooklm_rag.py --ask <question>    # 用 NotebookLM 问问题
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
RAW_CLIPS_DIR = WIKI_ROOT / "raw_clips"
NOTEBOOKLM_DIR = WIKI_ROOT / "notebooklm_results"


def check_notebooklm_login() -> dict:
    """检查 notebooklm 登录状态"""
    try:
        result = subprocess.run(
            ["notebooklm", "list"],
            capture_output=True, text=True, timeout=15
        )
        return {
            "available": result.returncode == 0,
            "output": result.stdout[:500],
            "error": result.stderr[:200] if result.returncode != 0 else ""
        }
    except FileNotFoundError:
        return {"available": False, "error": "notebooklm CLI 未安装"}
    except subprocess.TimeoutExpired:
        return {"available": False, "error": "notebooklm 超时"}


def create_notebook(name: str = "PJ-102 知识库") -> str:
    """创建 notebook,返回 notebook ID"""
    try:
        result = subprocess.run(
            ["notebooklm", "create", name],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # 从输出提取 ID
            output = result.stdout
            # 查找类似 "abc123..." 的 ID
            import re
            match = re.search(r'\b([a-f0-9]{20,})\b', output)
            if match:
                return match.group(1)
            return output.strip().split('\n')[0]
    except Exception as e:
        print(f"❌ 创建 notebook 失败: {e}")
    return ""


def push_clip_to_notebooklm(clip_path: Path, notebook_id: str) -> dict:
    """把一个 clip 推到 notebooklm"""
    try:
        # 读 markdown 内容
        content = clip_path.read_text(encoding="utf-8")
        # 提取正文(去掉 frontmatter)
        body = content.split("---", 2)[-1].strip() if content.startswith("---") else content

        # 简化处理:用 ask 让 notebooklm 处理这个内容
        result = subprocess.run(
            ["notebooklm", "use", notebook_id, "ask", body[:2000]],
            capture_output=True, text=True, timeout=60
        )
        return {
            "clip": clip_path.name,
            "status": "ok" if result.returncode == 0 else "error",
            "response": result.stdout[:500] if result.returncode == 0 else "",
            "error": result.stderr[:200] if result.returncode != 0 else ""
        }
    except Exception as e:
        return {"clip": clip_path.name, "status": "error", "error": str(e)}


def sync_all_clips(notebook_id: str = None, limit: int = 10) -> dict:
    """同步所有 raw_clips 到 notebooklm"""
    if not RAW_CLIPS_DIR.exists():
        return {"status": "error", "error": "raw_clips 目录不存在"}

    clips = sorted(RAW_CLIPS_DIR.glob("clip_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]

    if not notebook_id:
        notebook_id = create_notebook("PJ-102 知识库")

    if not notebook_id:
        return {"status": "error", "error": "无法创建/获取 notebook"}

    results = []
    for clip in clips:
        result = push_clip_to_notebooklm(clip, notebook_id)
        results.append(result)
        print(f"  {'✅' if result['status'] == 'ok' else '❌'} {clip.name}")

    # 保存结果
    NOTEBOOKLM_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOKLM_DIR / f"sync_result_{len(clips)}.json"
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "status": "ok",
        "notebook_id": notebook_id,
        "synced": len(results),
        "results_file": str(output)
    }


def main():
    parser = argparse.ArgumentParser(description="Web Clipper + NotebookLM RAG")
    parser.add_argument("--setup", action="store_true", help="检查 notebooklm 登录")
    parser.add_argument("--clip", help="抓 URL 并推 notebooklm")
    parser.add_argument("--sync", action="store_true", help="同步所有 clips")
    parser.add_argument("--limit", type=int, default=10, help="限制同步数")
    parser.add_argument("--ask", help="向 notebooklm 提问")
    args = parser.parse_args()

    if args.setup:
        status = check_notebooklm_login()
        print(f"📊 notebooklm 状态:")
        print(f"   可用:{status['available']}")
        if not status["available"]:
            print(f"   错误:{status.get('error', '')}")
            print(f"   💡 提示:王老师跑 `notebooklm login` 完成登录")
        else:
            print(f"   输出:{status['output']}")
        return

    if args.ask:
        # 直接用 ask
        result = subprocess.run(
            ["notebooklm", "ask", args.ask],
            capture_output=True, text=True, timeout=60
        )
        print(result.stdout)
        return

    if args.clip:
        # 抓 URL(用 web_clipper.py) + 推 notebooklm
        subprocess.run(
            ["python3", str(Path(__file__).parent / "web_clipper.py"), args.clip],
            check=False
        )
        # 然后同步
        result = sync_all_clips(limit=1)
        print(f"\n🎉 {result}")
        return

    if args.sync:
        result = sync_all_clips(limit=args.limit)
        print(f"\n🎉 同步完成:{result}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()