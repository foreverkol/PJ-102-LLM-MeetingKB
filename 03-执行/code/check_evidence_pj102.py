#!/usr/bin/env python3
"""PJ-102 专用 check_evidence.py - Grounding Invariant 验证。

适配 PJ-102 实际目录结构:
- wiki 在 02-知识库/PJ-102-LLM-MeetingKB/{meetings,persons,concepts,judgments}/
- raw 在 system/data/raw/

与 Karpathy 标准的差异:
1. raw 在 system/data/raw/ 而非 <root>/raw/
2. wiki 是 4 个子目录而非 wiki/<topic>/
3. 没有 Raw metadata 字段,而是用 source_meeting 字段
4. 没有 log.md

适配方案:
- Raw 等价 = source_meeting + source_hash 字段
- raw 路径 = system/data/raw/<source_meeting>
"""
import re
import sys
import os
from pathlib import Path
from dataclasses import dataclass

# === PJ-102 路径常量 ===
WIKI_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB")
RAW_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/system/data/raw")

# === Karpathy 验证逻辑(简化 + 适配) ===

@dataclass(frozen=True)
class Candidate:
    kind: str
    value: str

NUMBER_TOKEN_RE = re.compile(
    r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)*(?:\s*[KMB%](?![A-Za-z]))?"
    r"|\d+(?:\.\d+)*(?:\s*[KMB%](?![A-Za-z]))?)(?![A-Za-z])"
)
DATE_RE = re.compile(r"\d{4}-\d{2}(?:-\d{2})?")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
WS_RE = re.compile(r"\s+")
QUOTE_RES = [re.compile(r'"([^"\n]*)"'), re.compile(r'"([^"\n]*)"')]

def normalize(text):
    return WS_RE.sub(" ", text).strip()

def keep_number(token):
    token = token.strip()
    if "," in token or "." in token:
        return True
    return len(token) >= 4

def extract_candidates_from_text(text):
    """从 wiki 文章提取候选事实(数字/日期/引用)。

    排除 frontmatter 中的元数据(generated_at / llm_model / source_hash 等),
    因为这些是 LLM 生成时填的,不属于内容事实。
    """
    # 去掉 frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            text = text[end+3:]

    candidates = []
    text = INLINE_CODE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)

    for m in DATE_RE.finditer(text):
        candidates.append(Candidate("date", m.group(0)))

    for m in NUMBER_TOKEN_RE.finditer(text):
        if keep_number(m.group(0)):
            candidates.append(Candidate("number", m.group(0)))

    for quote_re in QUOTE_RES:
        for m in quote_re.finditer(text):
            if len(m.group(1).strip()) >= 15:
                candidates.append(Candidate("quote", m.group(1).strip()))

    return candidates

def get_raw_path_from_article(article_text, article_path):
    """从 PJ-102 wiki 文章提取 source_meeting 字段(等价于 Karpathy 的 Raw)"""
    # PJ-102 frontmatter: source_meeting: xxx.md
    m = re.search(r"^source_meeting:\s*(.+)$", article_text, re.MULTILINE)
    if m:
        filename = m.group(1).strip()
        return RAW_ROOT / filename
    return None

def get_associated_meetings(article_text):
    """获取所有 source / source_meeting 引用(PJ-102 两种格式)。

    PJ-102 source_meeting 引用可能是:
    - 完整文件名:20220419_100811xxx.md
    - 但 raw/ 里可能是:20220419_100811xxx_原文.md(去掉 .md + 加 _原文.md 后缀)
    """
    raw_files = list(RAW_ROOT.glob("*.md"))
    matches = re.findall(r"^source(?:_meeting)?:\s*(.+)$", article_text, re.MULTILINE)
    paths = []
    for m in matches:
        ref = m.strip()
        ref_base = ref.replace(".md", "")
        # 直接匹配
        direct = RAW_ROOT / ref
        if direct.is_file():
            paths.append(direct)
            continue
        # 尝试 _原文.md 后缀
        with_suffix = RAW_ROOT / f"{ref_base}_原文.md"
        if with_suffix.is_file():
            paths.append(with_suffix)
            continue
        # 模糊匹配(去掉中文部分找前缀匹配)
        prefix_match = ref_base[:13]  # YYYYMMDD_HHMMSS
        for rf in raw_files:
            if rf.stem.startswith(prefix_match):
                paths.append(rf)
                break
        else:
            paths.append(direct)  # not found,记录为 unresolvable
    return paths

def contains_candidate(haystack, candidate):
    """检查 raw 文件内容是否包含候选事实"""
    haystack_norm = normalize(haystack)
    if candidate.kind == "quote":
        return normalize(candidate.value) in haystack_norm
    if candidate.kind == "date":
        # 短日期 YYYY-MM 不能匹配 YYYY-MM-DD 后面
        right = r"(?!-\d{2})" if len(candidate.value) == 7 else ""
        pattern = r"(?<![\d.,])" + re.escape(candidate.value) + right + r"(?![A-Za-z0-9]|[.,]\d|%)"
    else:
        pattern = r"(?<![\d.,])" + re.escape(candidate.value) + r"(?![A-Za-z0-9]|%)"
    return re.search(pattern, haystack_norm) is not None

def check_article(article_path):
    """对单篇文章做 Grounding Invariant 验证"""
    text = article_path.read_text(encoding="utf-8")
    # 跳过 index.md 和 log.md
    if article_path.name in ("index.md", "log.md"):
        return [], []

    # 获取 Raw 等价(可能多个 source_meeting)
    raw_paths = get_associated_meetings(text)
    if not raw_paths:
        # 看是否有 source_hash 但没 source_meeting
        if re.search(r"^source_hash:", text, re.MULTILINE):
            return [], ["missing source_meeting field (has source_hash)"]
        return [], ["no source_meeting / Raw reference"]

    errors = []
    raw_contents = []
    for raw_path in raw_paths:
        if not raw_path.is_file():
            errors.append(f"unresolvable raw: {raw_path.name}")
        else:
            raw_contents.append(raw_path.read_text(encoding="utf-8"))

    if not raw_contents:
        return [], errors

    # 提取候选 + 验证
    candidates = extract_candidates_from_text(text)
    misses = []
    seen = set()
    for c in candidates:
        if c.value in seen:
            continue
        seen.add(c.value)
        if not any(contains_candidate(raw, c) for raw in raw_contents):
            misses.append(f"{c.kind}={c.value[:80]}")

    return misses, errors

def main():
    """主入口 - 跑全部 wiki 文章"""
    print("# PJ-102 Evidence Check (Grounding Invariant)\n")

    if not WIKI_ROOT.is_dir():
        print(f"ERROR: wiki root not found: {WIKI_ROOT}")
        return 1

    # 4 类 wiki 子目录
    categories = ["meetings", "persons", "concepts", "judgments"]

    total_articles = 0
    total_misses = 0
    total_errors = 0

    print("## Fidelity Suspects(数字/日期/引用未在 raw 中找到)\n")
    for cat in categories:
        cat_dir = WIKI_ROOT / cat
        if not cat_dir.is_dir():
            continue
        articles = sorted(cat_dir.glob("*.md"))
        cat_misses = 0
        for article in articles:
            if article.name in ("index.md", "log.md"):
                continue
            misses, errors = check_article(article)
            if misses or errors:
                total_articles += 1
            if misses:
                cat_misses += 1
                # 仅输出前 10 个示例,避免刷屏
                if cat_misses <= 5:
                    print(f"  {article.name}: {len(misses)} 候选未溯源")
                    for m in misses[:3]:
                        print(f"    - {m}")
            total_misses += len(misses)
            total_errors += len(errors)
        if cat_misses > 0:
            print(f"\n  [{cat}] 总计 {cat_misses}/{len(articles)} 文章有未溯源事实\n")

    print("\n## Evidence Errors(无法验证)\n")
    err_count = 0
    for cat in categories:
        cat_dir = WIKI_ROOT / cat
        if not cat_dir.is_dir():
            continue
        for article in sorted(cat_dir.glob("*.md")):
            if article.name in ("index.md", "log.md"):
                continue
            _, errors = check_article(article)
            for err in errors:
                err_count += 1
                if err_count <= 10:
                    print(f"  {article.name}: {err}")
    if err_count == 0:
        print("(none)")

    print(f"\n## Summary")
    print(f"- 文章总数: {sum(len(list((WIKI_ROOT/c).glob('*.md'))) for c in categories if (WIKI_ROOT/c).is_dir())}")
    print(f"- 有未溯源候选的文章数: {total_articles}")
    print(f"- 未溯源候选总数: {total_misses}")
    print(f"- Evidence errors 总数: {total_errors}")
    print(f"\n[Grounding Invariant]: {'❌ VIOLATED' if total_misses > 0 else '✅ PASS'}")

    return 0

if __name__ == "__main__":
    sys.exit(main())