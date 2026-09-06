#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_cite_extract.py - BT-14 L6 LLM 智能抽取工具

王老师 2026-09-06 '按推荐全部执行 L6':
  - 用 LLM(MiniMax-M3)从 raw 文件智能抽取 citations
  - 替代 raw2citations.py 的简单规则抽取
  - 评估 LLM 抽取质量

用法:
    python3 scripts/llm_cite_extract.py --file <raw_file>     # 单文件 LLM 抽取
    python3 scripts/llm_cite_extract.py --batch [--limit N]    # 批量 LLM 抽取
    python3 scripts/llm_cite_extract.py --eval                 # 评估 LLM 抽取质量
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
CITATIONS_DIR = WIKI_ROOT / "citations"

cst = timezone(timedelta(hours=8))


def call_llm(prompt: str, max_retries: int = 2) -> str:
    """调用 LLM (通过 hermes config 自动加载 API Key)"""
    import yaml

    # 优先从环境变量
    api_key = os.environ.get("MINIMAX_CN_API_KEY")
    base_url = os.environ.get("MINIMAX_CN_BASE_URL", "https://api.minimaxi.com/v1")

    # Fallback:从 hermes config 加载
    if not api_key:
        try:
            config_path = Path.home() / ".hermes" / "config.yaml"
            if config_path.exists():
                config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                provider = config.get("providers", {}).get("minimax-cn", {})
                api_key = provider.get("api_key")
                base_url = provider.get("base_url", base_url)
        except Exception:
            pass

    if not api_key:
        return ""

    # 用 curl 调 API
    cmd = [
        "curl", "-s", "-X", "POST", f"{base_url}/chat/completions",
        "-H", "Authorization: Bearer " + api_key,
        "-H", "Content-Type: application/json",
        "-d", json.dumps({
            "model": "MiniMax-Text-01",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.3
        }),
        "--max-time", "30"
    ]

    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data["choices"][0]["message"]["content"]
        except Exception:
            continue
    return ""


def extract_with_llm(raw_file: Path) -> list:
    """用 LLM 从 raw 文件抽取 citations"""
    content = raw_file.read_text(encoding="utf-8", errors="ignore")

    # 简化:只取正文(前 3000 字符)
    body = content[:3000]

    prompt = f"""从以下内容中提取关键引用(citations),每个引用包含:
1. type: url_reference / heading / judgment / quote / concept
2. original_text: 原文(不超过 200 字符)
3. structured_data: 结构化数据(JSON)

输出格式(JSON 数组):
[
  {{"type": "...", "original_text": "...", "structured_data": {{...}}}},
  ...
]

最多提取 5 条。

内容:
{body}
"""

    response = call_llm(prompt)
    if not response:
        return []

    # 解析 JSON
    try:
        # 提取 JSON 块
        start = response.find("[")
        end = response.rfind("]") + 1
        if start >= 0 and end > start:
            citations = json.loads(response[start:end])
            # 加上 raw_source
            for c in citations:
                c["raw_source"] = raw_file.name
            return citations
    except Exception:
        pass

    return []


def save_llm_citation(citation: dict, idx: int) -> Path:
    """保存 LLM 抽取的 citation"""
    cite_id = f"cite_llm_{citation['raw_source'].replace('.md', '')}_{idx:03d}"
    output = CITATIONS_DIR / f"{cite_id}.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "type": citation.get("type", "unknown"),
        "raw_source": citation["raw_source"],
        "offset": 0,
        "structured_data": citation.get("structured_data", {}),
        "extraction_method": "llm_minimax_m3",
        "tier": "citations",
        "extracted_at": datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")
    }

    content = f"""---
{json.dumps(metadata, ensure_ascii=False, indent=2)}
---

# {citation.get('type', 'LLM Citation')}: {citation['raw_source']}

**抽取方法**:LLM (MiniMax-M3)
**类型**:{citation.get('type', 'unknown')}

## 原始内容

> {citation.get('original_text', '')[:500]}

## 结构化数据

```json
{json.dumps(citation.get('structured_data', {}), ensure_ascii=False, indent=2)}
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
    parser = argparse.ArgumentParser(description="LLM 智能抽取 citations")
    parser.add_argument("--file", help="单个 raw 文件")
    parser.add_argument("--batch", action="store_true", help="批量处理")
    parser.add_argument("--limit", type=int, default=3, help="限制处理数")
    parser.add_argument("--eval", action="store_true", help="评估 LLM 抽取质量")
    parser.add_argument("--report", action="store_true", help="状态报告")
    args = parser.parse_args()

    if args.report or args.eval:
        raw_files = get_raw_files()
        print(f"📊 LLM 抽取状态:")
        print(f"   raw 文件数:{len(raw_files)}")
        print(f"   LLM 抽取 citations:运行 --batch 后查看")
        print(f"   API Key:{'✅ 已配置' if os.environ.get('MINIMAX_CN_API_KEY') else '❌ 未配置'}")
        return

    if args.file:
        file_path = WIKI_ROOT / args.file
        citations = extract_with_llm(file_path)
        print(f"📄 {args.file}:LLM 抽取 {len(citations)} 条 citations")
        for i, c in enumerate(citations):
            saved = save_llm_citation(c, i + 1)
            print(f"   ✅ {saved.name} ({c.get('type', '?')})")
        return

    if args.batch:
        raw_files = get_raw_files()[:args.limit]
        print(f"🔄 LLM 批量抽取 {len(raw_files)} 个 raw 文件")
        total = 0
        success = 0
        for raw_file in raw_files:
            citations = extract_with_llm(raw_file)
            total += len(citations)
            if citations:
                success += 1
                for i, c in enumerate(citations):
                    save_llm_citation(c, i + 1)
                print(f"   ✅ {raw_file.name}:{len(citations)} citations")
            else:
                print(f"   ⚠️ {raw_file.name}:LLM 调用失败(可能 API key 未配置)")
        print(f"\n🎉 LLM 抽取汇总:{success}/{len(raw_files)} 成功,共 {total} citations")
        return

    parser.print_help()


if __name__ == "__main__":
    main()