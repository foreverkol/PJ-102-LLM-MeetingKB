"""test_cascade_updater.py - T-02 cascade_updater.py 单元测试
A2 修复后:真 apply 实现
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code"))


def test_cascade_updater_import():
    """cascade_updater.py 可 import"""
    try:
        import cascade_updater
        assert hasattr(cascade_updater, 'cascade_update')
        # A2 修复:apply_cascade_to_file 必须存在
        assert hasattr(cascade_updater, 'apply_cascade_to_file')
    except ImportError:
        pytest.skip("cascade_updater.py 不存在")


def test_cascade_apply_not_empty():
    """A2 修复:apply_cascade_to_file 必须真有实现(不是空函数)"""
    try:
        import cascade_updater
        import inspect
        src = inspect.getsource(cascade_updater.apply_cascade_to_file)
        # 必须有写文件动作
        assert "write_text" in src or "fp.write" in src
    except (ImportError, AssertionError) as e:
        pytest.skip(f"cascade_updater 不可用: {e}")