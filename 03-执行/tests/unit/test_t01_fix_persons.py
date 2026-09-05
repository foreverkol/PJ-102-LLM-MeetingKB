"""test_t01_fix_persons.py - T-01 单元测试
A1 修复后:不损坏 frontmatter
"""
import pytest
import re
from pathlib import Path


def test_persons_no_corruption():
    """实际验证 persons/ 没有损坏文件"""
    persons_dir = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/persons")
    if not persons_dir.exists():
        pytest.skip("persons 目录不存在")
    corrupt = 0
    for f in persons_dir.glob("*.md"):
        content = f.read_text(encoding='utf-8')
        if re.search(r'relationship:\s*"[^"]*""""', content):
            corrupt += 1
    assert corrupt == 0, f"应有 0 个损坏文件,实测 {corrupt}"


def test_t01_source_safety():
    """t01 脚本不能有 raw_fm + 'relationship:' 这种会引入额外引号的拼接"""
    src_file = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/t01_fix_persons_relationship.py")
    if not src_file.exists():
        pytest.skip("t01 脚本不存在")
    src = src_file.read_text(encoding='utf-8')
    # A1 修复:不能是单纯 raw_fm + relationship 字符串拼接
    assert 'raw_fm +' not in src or 'relationship:' not in src.split('raw_fm +')[1].split('\n')[0]