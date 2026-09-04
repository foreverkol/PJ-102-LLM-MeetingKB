#!/usr/bin/env python3
"""PJ-102 专用 triage.py - Triage 4 状态判定。

对齐 Karpathy LLM Wiki 标准:
- New: 新概念,创建新文章
- Update: 合并到已有文章
- Disputed: 与已有内容矛盾
- No material: 无新增价值

输入:新 source 文本 + 已有 wiki 索引
输出:4 状态之一 + 详细说明
"""
import re
from pathlib import Path
from typing import Literal

WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")

TriageStatus = Literal["New", "Update", "Disputed", "No material"]

def extract_key_entities(text, max_entities=20):
    """从文本提取 key entities(中文姓名 / 机构 / 概念)"""
    entities = set()
    # 提取双引号引用
    for m in re.finditer(r'"([^"\n]{2,30})"', text):
        entities.add(m.group(1))
    # 提取 ## 标题
    for m in re.finditer(r'^#+\s+(.+)$', text, re.MULTILINE):
        title = m.group(1).strip()
        if len(title) < 30:
            entities.add(title)
    return list(entities)[:max_entities]

def find_existing_articles(entity):
    """在 wiki 中找包含 entity 的现有文章"""
    matches = []
    for sub in ["meetings", "persons", "concepts", "judgments"]:
        sub_dir = WIKI_ROOT / sub
        if not sub_dir.is_dir():
            continue
        for f in sub_dir.glob("*.md"):
            try:
                content = f.read_text(encoding="utf-8")
                if entity in content:
                    matches.append((sub, f.name))
            except Exception:
                pass
    return matches

def check_contradictions(new_text, existing_text):
    """检查新文本是否与现有内容矛盾"""
    # 简化版:检查明显的"反转"关键词
    contradict_words = [
        ("应该", "不应该"), ("支持", "反对"), ("同意", "不同意"),
        ("可以", "不可以"), ("能", "不能"), ("好", "不好"),
    ]
    new_lower = new_text.lower()
    existing_lower = existing_text.lower()
    # 必须同时出现"反转对"
    for pos, neg in contradict_words:
        if pos in new_lower and neg in existing_lower:
            return True
    return False

def triage(source_text: str, threshold_new: float = 0.7) -> dict:
    """Triage 判定。

    Args:
        source_text: 新 source 文本
        threshold_new: 判定 New 的实体覆盖率阈值(默认 0.7)

    Returns:
        dict: {
            "status": "New"|"Update"|"Disputed"|"No material",
            "entities": [...],
            "matched_articles": [...],
            "reason": "..."
        }
    """
    if not source_text or len(source_text.strip()) < 50:
        return {
            "status": "No material",
            "entities": [],
            "matched_articles": [],
            "reason": "source_text 太短(<50 字符)"
        }

    entities = extract_key_entities(source_text)

    if not entities:
        return {
            "status": "No material",
            "entities": [],
            "matched_articles": [],
            "reason": "无 key entities 提取"
        }

    # 在 wiki 中找匹配
    all_matches = {}
    for entity in entities:
        articles = find_existing_articles(entity)
        if articles:
            all_matches[entity] = articles

    if not all_matches:
        return {
            "status": "New",
            "entities": entities,
            "matched_articles": [],
            "reason": f"无现有文章引用 entities {entities[:3]},判定 New"
        }

    # 计算覆盖率
    coverage = len(all_matches) / len(entities)
    matched_articles = []
    for ents, arts in all_matches.items():
        for sub, name in arts:
            matched_articles.append(f"{sub}/{name}")

    # 矛盾检查
    has_contradiction = False
    if matched_articles:
        # 取第一个匹配文章看是否有矛盾
        sub, name = list(all_matches.values())[0][0]
        existing_path = WIKI_ROOT / sub / name
        try:
            existing_text = existing_path.read_text(encoding="utf-8")
            has_contradiction = check_contradictions(source_text, existing_text)
        except Exception:
            pass

    if has_contradiction:
        return {
            "status": "Disputed",
            "entities": entities,
            "matched_articles": matched_articles[:5],
            "reason": f"新内容与现有文章存在反转词(矛盾)"
        }

    if coverage >= threshold_new:
        return {
            "status": "Update",
            "entities": entities,
            "matched_articles": matched_articles[:5],
            "reason": f"覆盖率 {coverage:.0%} ≥ {threshold_new:.0%},合并到现有文章"
        }

    return {
        "status": "New",
        "entities": entities,
        "matched_articles": matched_articles[:5],
        "reason": f"覆盖率 {coverage:.0%} < {threshold_new:.0%},判定 New(部分匹配)"
    }


if __name__ == "__main__":
    # 实测 demo
    sample_text = """
## 浙商银行总行交流票据经纪业务合作

### 王老师与吴英杰到浙商银行总行
讨论票据经纪业务合作模式...

"我们需要拓展融资性票据端口" 王老师说

### 关键决策
1. 优先接入浙商银行票据系统
2. 建立经纪业务的合规框架
"""
    result = triage(sample_text)
    print(f"Triage 结果:{result['status']}")
    print(f"原因:{result['reason']}")
    print(f"匹配 entities:{result['entities']}")
    print(f"匹配文章:{result['matched_articles']}")