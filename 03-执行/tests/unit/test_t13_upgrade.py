"""test_t13_upgrade.py - T-13 升级分析脚本验证"""
import pytest
import subprocess
from pathlib import Path


def test_poc_concepts_count():
    """poc 分支应有 24 个 concepts"""
    r = subprocess.run(
        ["git", "ls-tree", "--name-only", "-z",
         "poc/atomicstrata-experiment",
         "03-执行/poc_atomicstrata/wiki/concepts/"],
        capture_output=True,
        cwd="/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
    )
    files = [f for f in r.stdout.split(b'\x00') if f.endswith(b'.md')]
    assert len(files) == 24, f"poc 应有 24 个,实测 {len(files)}"


def test_t13_upgrade_script_exists():
    """t13_upgrade_poc_to_structured.py 存在"""
    src = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code/t13_upgrade_poc_to_structured.py")
    assert src.exists()
    assert src.stat().st_size >= 3000, f"应 3KB+,实测 {src.stat().st_size}"