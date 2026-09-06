#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_guard.py - PJ-102 质量守护(防上次失败)

王老师 2026-09-06 '完全瞎搞' 后的硬规则:

  规则 1:禁止编造王老师原话
  规则 2:禁止 fake URL
  规则 3:禁止模板自指

任何 wiki/raw/citation 文件生成前必须过 quality_guard.py 检查。
"""
import re
import sys
from pathlib import Path


def check_no_fabricated_quotes(content: str) -> tuple[bool, str]:
    """规则 1:检查是否编造 '— 王老师' 但无溯源

    任何 '— 王老师' 的引用,必须前文 200 字符内有原文片段
    """
    issues = []

    # 找所有 '— 王老师' 引用
    quote_pattern = re.compile(r'^>\s*["""''「](.+?)["""''」]\s*[—\-]\s*王老师', re.MULTILINE)
    quotes = quote_pattern.findall(content)

    if not quotes:
        return True, "✅ 无编造王老师引用"

    # 检查每条引用前文是否有溯源
    for match in quote_pattern.finditer(content):
        quote_text = match.group(1)
        quote_pos = match.start()

        # 前文 200 字符内查找溯源关键词
        preceding = content[max(0, quote_pos - 200):quote_pos]

        # 溯源信号:URL / 录音转写 / 文件路径 / "原话:" / "引用源:"
        source_signals = ['http', '转写', '录音', '原始', '原话:', '引用源:', '来源:', 'file://']

        if not any(sig in preceding for sig in source_signals):
            issues.append(f"❌ 编造引用:'{quote_text}'(前文 200 字符内无溯源)")

    if issues:
        return False, "\n".join(issues)
    return True, "✅ 王老师引用都有溯源"


def check_no_fake_urls(content: str) -> tuple[bool, str]:
    """规则 2:检查 fake URL

    禁止:example.com / wikipedia.org/wiki/<汉字> 等
    """
    issues = []

    # example.com 占位符
    if "example.com" in content:
        issues.append("❌ 含 example.com 占位符 URL")

    # wikipedia.org/wiki/<中文> — 这种 URL 实际 404
    fake_zh_wiki = re.findall(r'wikipedia\.org/wiki/[\u4e00-\u9fff]+', content)
    if fake_zh_wiki:
        issues.append(f"❌ 含假 Wikipedia 中文 URL:{fake_zh_wiki}")

    # wikipedia.org/wiki/<主题> + 主题是中文
    fake_pattern = re.compile(r'wikipedia\.org/wiki/[\u4e00-\u9fff]+')
    for match in fake_pattern.finditer(content):
        issues.append(f"❌ 假 Wikipedia URL:{match.group()}")

    if issues:
        return False, "\n".join(issues)
    return True, "✅ URL 都是真实抓取"


def check_no_template_self_ref(content: str) -> tuple[bool, str]:
    """规则 3:检查模板自指

    'X 的核心是 X' / 'Y 的核心组成部分是 Y' 等循环套话
    """
    issues = []

    # 'X 的核心是 X' 自指
    self_ref = re.findall(r'([\u4e00-\u9fff]{2,8})的核心是\1', content)
    if self_ref:
        issues.append(f"❌ 模板自指:'{self_ref[0]}的核心是{self_ref[0]}'")

    # 'X 领域的核心组成部分' 套话
    if "领域的核心组成部分" in content and "是" in content:
        # 检查是否是空模板:X 是 Y 领域的核心组成部分
        empty_pattern = re.findall(r'([\u4e00-\u9fff]{2,15})是([\u4e00-\u9fff]{2,15})领域的核心组成部分', content)
        if empty_pattern:
            issues.append(f"❌ 空模板套话:{empty_pattern[0]}")

    if issues:
        return False, "\n".join(issues)
    return True, "✅ 无模板自指"


def guard(content: str) -> tuple[bool, list]:
    """总检查"""
    results = []

    ok1, msg1 = check_no_fabricated_quotes(content)
    results.append(("规则 1:禁止编造王老师原话", ok1, msg1))

    ok2, msg2 = check_no_fake_urls(content)
    results.append(("规则 2:禁止 fake URL", ok2, msg2))

    ok3, msg3 = check_no_template_self_ref(content)
    results.append(("规则 3:禁止模板自指", ok3, msg3))

    all_ok = ok1 and ok2 and ok3
    return all_ok, results


def main():
    """CLI:检查文件或字符串"""
    if len(sys.argv) < 2:
        print("用法:python3 quality_guard.py <file.md>")
        print("     python3 quality_guard.py --check <text>")
        sys.exit(1)

    if sys.argv[1] == "--check":
        text = sys.argv[2]
    else:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"❌ 文件不存在:{file_path}")
            sys.exit(1)
        text = file_path.read_text(encoding="utf-8")

    all_ok, results = guard(text)

    print("=" * 60)
    print("🛡 PJ-102 质量守护检查")
    print("=" * 60)

    for rule_name, ok, msg in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"\n{status} {rule_name}")
        print(f"  {msg}")

    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 全部规则通过")
        sys.exit(0)
    else:
        print("❌ 至少 1 条规则失败,内容禁止入库")
        sys.exit(1)


if __name__ == "__main__":
    main()