"""
PJ-102-LLM-MeetingKB · 主入口 v1.0

用法：
    python3 pipeline.py                    # 跑全部
    python3 pipeline.py --limit 13        # 跑 13 个样本
    python3 pipeline.py --no-llm          # mock 模式
    python3 pipeline.py --clear           # 先清空 WIKI
    python3 pipeline.py --provider minimax # 指定 provider
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# 添加当前目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from llm_client import LLMClient
from steps import (
    s1_basic_info, s2_scene_recognition, s3_standard_summary,
    s4_fjv, s5_implicit_knowledge, s6_entity_extraction,
    s7_action_decision, s8_risk_blindspot, s9_knowledge_classify,
    s10_cognitive_refine, s11_value_rating, s12_write_wiki,
)

PROJECT_ROOT = Path(__file__).parent.parent.parent  # PJ-102-LLM-MeetingKB/
DATA_RAW = PROJECT_ROOT / "system/data/raw"
DATA_INDEX = PROJECT_ROOT / "system/data/index.json"
WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")


def load_index():
    if not DATA_INDEX.exists():
        print(f"❌ 找不到 index: {DATA_INDEX}")
        sys.exit(1)
    return json.loads(DATA_INDEX.read_text(encoding='utf-8'))


def process_one(sample: dict, llm: LLMClient) -> dict:
    """处理一个样本的 12 步全流程"""
    raw_file = DATA_RAW / sample["filename"]
    if not raw_file.exists():
        raise FileNotFoundError(f"找不到: {raw_file}")
    content = raw_file.read_text(encoding='utf-8')

    s1 = s1_basic_info(sample["filename"], content)
    s2 = s2_scene_recognition(content, llm)
    s3 = s3_standard_summary(content, llm)
    s4 = s4_fjv(content, llm)
    s5 = s5_implicit_knowledge(content, llm)
    s6 = s6_entity_extraction(content, llm)
    s7 = s7_action_decision(content, llm)
    s8 = s8_risk_blindspot(content, llm)
    s9 = s9_knowledge_classify(content, llm)
    s10 = s10_cognitive_refine(content, llm)
    s11 = s11_value_rating(content, llm)

    return {
        "sample": sample["filename"],
        "content_hash": sample["content_hash"],
        "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5,
        "s6": s6, "s7": s7, "s8": s8, "s9": s9, "s10": s10, "s11": s11,
        "_meta": {
            "llm_provider": llm.provider,
            "llm_model": llm.model,
        }
    }


def clear_wiki():
    """清空所有 WIKI"""
    if WIKI_BASE.exists():
        for sub in WIKI_BASE.iterdir():
            if sub.is_dir():
                for f in sub.glob("*.md"):
                    f.unlink()
        print("✅ 已清空 WIKI")


def main():
    parser = argparse.ArgumentParser(description="PJ-102-LLM-MeetingKB Pipeline")
    parser.add_argument("--limit", type=int, default=0, help="限制样本数（0=全部）")
    parser.add_argument("--no-llm", action="store_true", help="跳过 LLM（mock）")
    parser.add_argument("--clear", action="store_true", help="先清空 WIKI")
    parser.add_argument("--provider", type=str, default="auto", help="LLM provider")
    parser.add_argument("--dry-run", action="store_true", help="干跑，不写文件")
    args = parser.parse_args()

    if args.clear:
        clear_wiki()

    if args.no_llm:
        os.environ["DEEPSEEK_API_KEY"] = ""
        os.environ["MINIMAX_API_KEY"] = ""
        os.environ["OPENAI_API_KEY"] = ""
        os.environ["ANTHROPIC_API_KEY"] = ""

    llm = LLMClient(provider=args.provider)
    print(f"🤖 LLM Provider: {llm.provider} / {llm.model}")
    print(f"📁 WIKI 输出: {WIKI_BASE}")
    print()

    index = load_index()
    samples = index["samples"]
    if args.limit > 0:
        samples = samples[:args.limit]

    print(f"📂 共 {len(samples)} 个样本待处理")
    print()

    success = 0
    fail = 0
    total_time = 0

    for i, sample in enumerate(samples, 1):
        sample_file = sample["filename"]
        short = sample_file[:40]
        print(f"[{i}/{len(samples)}] {short}...", end=" ", flush=True)
        start = time.time()

        try:
            result = process_one(sample, llm)
            if not args.dry_run:
                out_path = s12_write_wiki(result, WIKI_BASE)
                elapsed = time.time() - start
                total_time += elapsed
                print(f"✅ ({elapsed:.1f}s) → {Path(out_path).name}")
            else:
                print("✅ (dry-run)")
            success += 1
        except Exception as e:
            print(f"❌ {e}")
            fail += 1

    print()
    avg = total_time / success if success else 0
    print(f"📊 {success} 成功 / {fail} 失败")
    print(f"⏱️  总耗时: {total_time:.1f}s, 平均: {avg:.1f}s/文件")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())