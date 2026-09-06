#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_codex_review.py - 本地化 Codex 风格代码评审

王老师 2026-09-06 OUT-OF-BAND:
  "C"(本地化 Codex review,跳过 codex CLI 未登录问题)

设计:
  - 用 minimax-m3 通过 codex-shim 模拟 Codex review
  - 评审风格:挑刺/找漏洞/给建议(模仿 Codex 评审员)
  - 输出 markdown 报告,保存到 .codex-reviews/<hash>.md

注意:本脚本不是真的 Codex CLI,是本地化替代。
王老师原则:"只用 Codex CLI 做评审,其他全部 Hermes 内部"。
本次因 codex CLI 未登录,临时本地化,Sprint 23+ codex 登录后切回。

用法:
    python3 scripts/local_codex_review.py HEAD
    python3 scripts/local_codex_review.py --commit HEAD~3
    python3 scripts/local_codex_review.py --diff-only   # 只评审 diff
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

PROJECT_ROOT = Path(__file__).parent.parent
cst = timezone(timedelta(hours=8))


def get_diff(target: str, n: int = 1) -> str:
    """获取 git diff(默认 HEAD~1 vs HEAD)"""
    try:
        if target == "HEAD":
            ref = "HEAD~1"
        else:
            ref = f"{target}~1"
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "diff", ref, target],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # 限长,避免超 token
            diff = result.stdout
            if len(diff) > 30000:
                diff = diff[:30000] + "\n\n... [diff 截断,仅展示前 30000 字符] ..."
            return diff
    except Exception as e:
        return f"diff 失败: {e}"
    return ""


def call_minimax_m3(prompt: str, system: str = None) -> str:
    """调 minimax-m3(codex-shim 8765)"""
    # codex-shim 兼容 OpenAI /v1/chat/completions
    # 但 minimax API 在 api.minimaxi.com
    base_url = "https://api.minimaxi.com/v1/chat/completions"
    api_key = os.environ.get("MINIMAX_CN_API_KEY") or os.environ.get("MINIMAX_API_KEY") or os.environ.get("OPENAI_API_KEY")

    if not api_key:
        # 从 codex-shim 配置取(读本地文件)
        try:
            config_path = Path("/home/administrator/.codex-shim/models.json")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            for m in config["models"]:
                if "minimax-m3" in m.get("model", "").lower() or "MiniMax-M3" in m.get("model", ""):
                    api_key = m.get("api_key")
                    if api_key and api_key.startswith("***"):
                        api_key = os.environ.get("MINIMAX_API_KEY_REAL") or api_key
                    break
        except Exception as e:
            pass

    if not api_key:
        return "❌ 未找到 MiniMax API Key"

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    body = json.dumps({
        "model": "MiniMax-M3",
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.3
    }).encode("utf-8")

    req = urllib.request.Request(
        base_url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"❌ API 错误 {e.code}: {e.read().decode('utf-8')[:500]}"
    except Exception as e:
        return f"❌ 调 API 失败: {e}"


def review(target: str) -> dict:
    """主评审入口"""
    print(f"🔍 本地 Codex 风格评审: {target}")
    print(f"   时间: {datetime.now(cst).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   模型: MiniMax-M3 (本地化,代替未登录的 Codex CLI)")

    diff = get_diff(target)
    if not diff:
        return {"status": "error", "message": "diff 为空"}

    print(f"   diff 长度: {len(diff)} 字符")

    system = """你是 PJ-102 项目的代码评审员(Codex 风格)。
角色:挑刺、找漏洞、给专业建议。
评审重点:
  1. 代码质量(命名/结构/注释)
  2. 测试覆盖(是否缺测试)
  3. 安全性(XSS/注入/敏感信息)
  4. 文档完整性(用户能看到使用说明)
  5. 协议遵守(王老师 v41/v42/v44 协议)

输出格式(markdown):
## 🚨 严重问题(必须修复)
## ⚠️ 中等问题(应该修复)
## 💡 建议改进(可选)
## ✅ 亮点(做得好的)

每项给出:文件:行号 + 问题描述 + 修复建议
"""

    user = f"""请评审以下 git diff:

```
{diff}
```

重点检查:
- 王老师 v41 协议(版本铁律)
- 王老师 v42 协议(不虚假汇报)
- 王老师 v44 协议(不擅自分配)
- 王老师架构原则(Codex 只 review,其他 Hermes 内部)
- 测试覆盖
- 文档完整性
"""

    print("   📡 调用 MiniMax-M3...")
    review_md = call_minimax_m3(user, system)

    return {
        "status": "ok",
        "target": target,
        "diff_size": len(diff),
        "review": review_md,
        "timestamp": datetime.now(cst).strftime("%Y-%m-%d %H:%M:%S")
    }


def save_report(result: dict, commit_sha: str = None):
    """保存评审到 .codex-reviews/<hash>.md"""
    if result["status"] != "ok":
        print(f"❌ 评审失败: {result.get('message')}")
        return

    reviews_dir = PROJECT_ROOT / ".codex-reviews"
    reviews_dir.mkdir(exist_ok=True)

    if commit_sha:
        short = commit_sha[:8]
    else:
        short = datetime.now(cst).strftime("%Y%m%d-%H%M%S")

    output = reviews_dir / f"{short}.md"
    output.write_text(
        f"""# Codex 风格本地评审报告

> **目标 commit**:{result['target']}
> **评审时间**:{result['timestamp']}
> **评审模型**:MiniMax-M3(本地化,代替未登录的 Codex CLI)
> **diff 大小**:{result['diff_size']} 字符
> **架构原则**:王老师"只用 Codex CLI 做评审",本次 codex CLI 未登录,临时本地化

---

{result['review']}
""",
        encoding="utf-8"
    )
    print(f"💾 评审已保存:{output}")
    print()
    print("━" * 70)
    print(result["review"][:3000])
    print()


def main():
    parser = argparse.ArgumentParser(description="本地化 Codex 风格代码评审")
    parser.add_argument(
        "target",
        nargs="?",
        default="HEAD",
        help="评审目标:HEAD / HEAD~N / commit SHA"
    )
    parser.add_argument(
        "--commit",
        help="指定 commit SHA 评审"
    )
    parser.add_argument(
        "--diff-only",
        action="store_true",
        help="只打印 diff 不评审"
    )
    args = parser.parse_args()

    target = args.commit or args.target

    if args.diff_only:
        diff = get_diff(target)
        print(diff)
        return

    result = review(target)
    save_report(result, args.commit)


if __name__ == "__main__":
    main()