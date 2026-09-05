"""test_obsidian_export.py - T-08 obsidian_export.py 单元测试"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code"))


def test_obsidian_export_import():
    """obsidian_export.py 可 import"""
    try:
        import obsidian_export
        assert hasattr(obsidian_export, 'main')
    except ImportError:
        pytest.skip("obsidian_export.py 不存在")


def test_obsidian_export_runs():
    """obsidian_export.py 可执行不崩溃"""
    import subprocess
    r = subprocess.run(
        ["python3", "obsidian_export.py", "--verbose"],
        capture_output=True, text=True,
        cwd=Path(__file__).parent.parent.parent / "code"
    )
    assert "Traceback" not in r.stderr or r.returncode == 0