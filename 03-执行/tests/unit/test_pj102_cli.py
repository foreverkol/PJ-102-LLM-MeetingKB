"""test_pj102_cli.py - T-12 CLI 单元测试"""
import pytest
import subprocess
from pathlib import Path


def test_pj102_help():
    """pj102.py --help 必须 exit 0"""
    code_dir = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
    r = subprocess.run(
        ["python3", "pj102.py", "--help"],
        capture_output=True, text=True, cwd=code_dir
    )
    assert r.returncode == 0
    assert "ingest" in r.stdout
    assert "compile" in r.stdout
    assert "status" in r.stdout


def test_pj102_status():
    """pj102.py status 必须 exit 0"""
    code_dir = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code")
    r = subprocess.run(
        ["python3", "pj102.py", "status"],
        capture_output=True, text=True, cwd=code_dir
    )
    assert r.returncode == 0
    assert "Wiki" in r.stdout
    assert "persons" in r.stdout