"""
v3.0 lint_wiki.py - 7 维健康巡检 + v7.0 §8.1 必填字段检查

7 维度:
  1. orphan_pages       — 无 inbound link 的页面
  2. dead_links         — [[wikilink]] 指向不存在的页面
  3. missing_sources    — frontmatter 缺 source_ref
  4. contradiction_pending — Status: Disputed 待 verified_by
  5. stale_pages        — >90 天未更新
  6. unindexed          — 在 WIKI/ 但没在 index.md
  7. emoji_garbled      — frontmatter emoji 解析异常

v7.0 §8.1 必填字段检查(集成进维度 3):
  - meeting: subtype + publishability + reusable_for + ldamc + source_ref
  - person: entity_id + thinking_framework + values_beliefs + decision_style + emotional_tone
  - judgment: topic_key + evidence_chain + confidence_rationale
  - organization: entity_id + org_name + org_type + business_model + cooperation_status
  - scenario: theme + customer + pain_point + offering + value_capture + channel + key_resources

返回 JSON report,feishu_lint_alert 可直接读
"""

import re
import json
import datetime
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


# v7.0 §8.1 必填字段映射(每个 type 的强制字段)
REQUIRED_FIELDS = {
    "meeting": ["subtype", "publishability", "reusable_for",
                "ldamc", "source_ref"],
    "person": ["entity_id", "thinking_framework", "values_beliefs",
               "decision_style", "emotional_tone"],
    "judgment": ["topic_key", "evidence_chain", "confidence_rationale"],
    "organization": ["entity_id", "org_name", "org_type",
                     "business_model", "cooperation_status"],
    "scenario": ["theme", "customer", "pain_point", "offering",
                 "value_capture", "channel", "key_resources",
                 "key_constraints", "hidden_assumptions",
                 "trigger_signals", "failure_modes"],
}


def lint_wiki(wiki_root: Path) -> Dict[str, List[str]]:
    """主入口:返回 7 维报告"""
    wiki_root = Path(wiki_root)
    if not wiki_root.exists():
        return {"error": [f"wiki root 不存在: {wiki_root}"]}

    md_files = list(wiki_root.rglob("*.md"))
    md_files = [f for f in md_files if f.name not in ("index.md", "log.md")]

    return {
        "1_orphan_pages": _check_orphans(md_files),
        "2_dead_links": _check_dead_links(md_files),
        "3_missing_sources": _check_missing_sources(md_files),
        "4_contradiction_pending": _check_contradiction_pending(md_files),
        "5_stale_pages": _check_stale_pages(md_files, threshold_days=90),
        "6_unindexed": _check_unindexed(md_files, wiki_root),
        "7_emoji_garbled": _check_emoji_garbled(md_files),
        "8_required_field_violations": _check_required_fields(md_files),  # v7.0 增强
    }


# ============ 维度 1: orphan_pages ============

def _check_orphans(md_files: List[Path]) -> List[str]:
    inbound = defaultdict(int)
    for f in md_files:
        try:
            for link in _extract_wikilinks(f.read_text(encoding="utf-8", errors="ignore")):
                inbound[link] += 1
        except Exception:
            pass
    orphans = []
    for f in md_files:
        name = f.stem
        # 自链不计
        if name in ("index", "log"):
            continue
        if inbound[name] == 0:
            orphans.append(str(f))
    return orphans


# ============ 维度 2: dead_links ============

def _check_dead_links(md_files: List[Path]) -> List[str]:
    stems = {f.stem for f in md_files}
    dead = []
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for link in _extract_wikilinks(text):
            if link not in stems:
                dead.append(f"{f.name} -> [[{link}]]")
    return dead


# ============ 维度 3: missing_sources ============

def _check_missing_sources(md_files: List[Path]) -> List[str]:
    missing = []
    for f in md_files:
        fm = _parse_frontmatter(f)
        if fm.get("type") and not fm.get("source_ref"):
            missing.append(str(f))
    return missing


# ============ 维度 4: contradiction_pending ============

def _check_contradiction_pending(md_files: List[Path]) -> List[str]:
    pending = []
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "Status: Disputed" in text and "<!-- verified_by" not in text:
            pending.append(str(f))
    return pending


# ============ 维度 5: stale_pages ============

def _check_stale_pages(md_files: List[Path], threshold_days: int = 90) -> List[str]:
    today = datetime.date.today()
    stale = []
    for f in md_files:
        fm = _parse_frontmatter(f)
        updated_str = fm.get("updated")
        if not updated_str:
            continue
        try:
            updated = datetime.date.fromisoformat(updated_str)
            if (today - updated).days > threshold_days:
                stale.append(str(f))
        except (ValueError, TypeError):
            continue
    return stale


# ============ 维度 6: unindexed ============

def _check_unindexed(md_files: List[Path], wiki_root: Path) -> List[str]:
    index_file = wiki_root / "index.md"
    if not index_file.exists():
        # 没 index.md,全部 unindexed
        return [str(f.relative_to(wiki_root)) for f in md_files]
    try:
        index_text = index_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return [str(f.relative_to(wiki_root)) for f in md_files]
    unindexed = []
    for f in md_files:
        rel = str(f.relative_to(wiki_root))
        if rel not in index_text:
            unindexed.append(rel)
    return unindexed


# ============ 维度 7: emoji_garbled ============

EMOJI_RE = re.compile(
    "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+",
    flags=re.UNICODE,
)


def _check_emoji_garbled(md_files: List[Path]) -> List[str]:
    garbled = []
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # 检测 "Status: Disputed" 但有乱码(如 ?Status: Disputed?)
        if "Status: Disputed" in text and "?" in text[:200]:
            garbled.append(str(f))
        # 检测双冒号乱码
        if "::" in text and "Status" in text:
            garbled.append(str(f))
    return garbled


# ============ 维度 8: required_field_violations(v7.0 §8.1) ============

def _check_required_fields(md_files: List[Path]) -> List[str]:
    violations = []
    for f in md_files:
        fm = _parse_frontmatter(f)
        page_type = fm.get("type")
        if not page_type:
            continue
        required = REQUIRED_FIELDS.get(page_type)
        if not required:
            continue
        missing = [k for k in required if not fm.get(k)]
        if missing:
            violations.append(f"{f.name} [{page_type}]: missing {missing}")
    return violations


# ============ Helpers ============

def _extract_wikilinks(text: str) -> List[str]:
    """[[link]] 或 [[link|alias]] 提取"""
    return re.findall(r"\[\[([^\[\]|]+?)(?:\|[^\[\]]+?)?\]\]", text)


def _parse_frontmatter(md_file: Path) -> dict:
    """简易 YAML frontmatter 解析(支持嵌套 indent block 如 ldamc)"""
    if not md_file.exists():
        return {}
    try:
        text = md_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm = {}
    parent_key = None
    parent_indent = 0
    parent_obj = None

    for line in parts[1].split("\n"):
        # 跳过空行和注释
        if not line.strip() or line.strip().startswith("#"):
            continue
        # 计算缩进
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)

        if indent == 0 and ":" in stripped:
            # 顶层字段
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip()
            v = _parse_value(v)
            fm[k] = v
            # 判断是否为 dict 起点
            if v == "":
                parent_key = k
                parent_indent = 1
                parent_obj = {}
                fm[k] = parent_obj
            else:
                parent_key = None
                parent_obj = None
        elif parent_key is not None and indent > 0 and ":" in stripped:
            # 嵌套字段
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = _parse_value(v.strip())
            parent_obj[k] = v

    return fm


def _parse_value(v: str):
    """解析单值:list / string / number"""
    if not v:
        return ""
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
    if (v.startswith("'") and v.endswith("'")) or \
       (v.startswith('"') and v.endswith('"')):
        return v[1:-1]
    return v


# ============ CLI ============

if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/WIKI")
    report = lint_wiki(target)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # 7 维加 1 = 8 个 key 全非空(空 list 也算)
    fail = sum(1 for v in report.values() if isinstance(v, list) and len(v) > 0)
    print(f"\n📊 巡检:共 {fail} 类问题", file=sys.stderr)
    sys.exit(1 if fail > 0 else 0)
