"""
v3.0 daily_incremental.py - 增量调度器(§v7.0 + FR-006)

工作流:
  1. 加载 processed_files.json(已处理文件清单)
  2. 扫描 source_dir 新文件
  3. 只对新增文件跑完整 pipeline(11+2 = 13 步)
  4. 追加到 processed_files.json
  5. 触发 lint_wiki.py 巡检

不重处理已存在文件(content_hash 跳过)
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Set


def compute_content_hash(content: str) -> str:
    """SHA256[:12] 作为 content_hash 唯一标识"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]


def load_processed(state_file: Path) -> dict:
    """加载已处理文件状态"""
    if not state_file.exists():
        return {"version": "1.0", "last_updated": "", "processed": []}
    return json.loads(state_file.read_text(encoding="utf-8"))


def save_processed(state_file: Path, state: dict):
    """持久化"""
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def find_new_files(source_dir: Path, state: dict) -> List[Path]:
    """扫描 source_dir,返回新文件列表"""
    processed_hashes = {p["content_hash"] for p in state.get("processed", [])}
    new_files = []
    for md_file in source_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        h = compute_content_hash(content)
        if h not in processed_hashes:
            new_files.append(md_file)
    return new_files


def mark_processed(state: dict, file_path: Path, content_hash: str,
                  result: dict):
    """追加 processed 清单"""
    state.setdefault("processed", []).append({
        "filename": file_path.name,
        "content_hash": content_hash,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "s2_scene_type": result.get("s2", {}).get("scene_type"),
        "s11_value_score": result.get("s11", {}).get("value_score"),
        "wiki_files_written": result.get("wiki_files_written", 0),
        "status": "ok",
    })


def run_incremental(
    source_dir: Path,
    state_file: Path,
    pipeline_fn=None,
    lint_fn=None,
    feishu_alert_fn=None,
    dry_run: bool = False,
) -> dict:
    """主入口

    Args:
        source_dir: 源文件目录(放 _原文.md)
        state_file: processed_files.json
        pipeline_fn: 单文件处理函数(pipeline.process_one 等价)
        lint_fn: lint_wiki.lint_wiki 函数
        feishu_alert_fn: 飞书告警函数
        dry_run: 只报告不处理

    Returns:
        {
            "new_files": [...],
            "processed_count": int,
            "skipped_count": int,
            "errors": [...],
            "started_at": str,
            "finished_at": str,
        }
    """
    source_dir = Path(source_dir)
    state_file = Path(state_file)
    state = load_processed(state_file)
    new_files = find_new_files(source_dir, state)
    report = {
        "new_files": [str(f) for f in new_files],
        "processed_count": 0,
        "skipped_count": 0,
        "errors": [],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": "",
    }

    if dry_run:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        return report

    if not pipeline_fn:
        report["errors"].append("pipeline_fn not provided")
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        return report

    processed_count = 0
    for f in new_files:
        try:
            content = f.read_text(encoding="utf-8")
            content_hash = compute_content_hash(content)
            result = pipeline_fn(f, content, content_hash)
            if result.get("ok"):
                mark_processed(state, f, content_hash, result)
                processed_count += 1
        except Exception as e:
            report["errors"].append(f"{f.name}: {e}")

    save_processed(state_file, state)
    report["processed_count"] = processed_count
    report["skipped_count"] = len(new_files) - processed_count
    report["finished_at"] = datetime.now(timezone.utc).isoformat()

    # 触 lint
    if lint_fn and processed_count > 0:
        try:
            lint_report = lint_fn()
            report["lint_summary"] = {
                "orphans": len(lint_report.get("1_orphan_pages", [])),
                "missing_sources": len(lint_report.get("3_missing_sources", [])),
                "required_violations": len(
                    lint_report.get("8_required_field_violations", [])
                ),
            }
            if feishu_alert_fn:
                feishu_alert_fn(lint_report)
        except Exception as e:
            report["errors"].append(f"lint failed: {e}")

    return report


# ============ CLI ============

if __name__ == "__main__":
    import os
    import argparse

    parser = argparse.ArgumentParser(description="PJ-102 daily_incremental.py")
    parser.add_argument("--source", required=True,
                       help="源文件目录")
    parser.add_argument("--state", default="SYSTEM/state/processed_files.json",
                       help="已处理文件状态")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    source_dir = Path(args.source)
    state_file = Path(args.state)

    # 默认 pipeline + lint 占位(真实使用时由 pipeline.py 注入)
    def placeholder_pipeline(file_path, content, content_hash):
        return {"ok": False, "error": "no pipeline_fn injected"}

    def placeholder_lint():
        return {}

    report = run_incremental(
        source_dir=source_dir,
        state_file=state_file,
        pipeline_fn=placeholder_pipeline,
        lint_fn=placeholder_lint,
        dry_run=args.dry_run,
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))
