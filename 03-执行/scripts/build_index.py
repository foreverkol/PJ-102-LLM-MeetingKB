"""build_index.py - Sprint 11.1 自动重建 index.json
扫描 system/data/raw/ 全部 _原文.md,生成 index.json 样本索引。
"""
import json
import hashlib
from pathlib import Path

RAW = Path("system/data/raw")
INDEX = Path("system/data/index.json")


def content_hash(path: Path) -> str:
    """取文件前 64KB 算 SHA1(快 + 避免大文件慢)"""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read(65536))
    return h.hexdigest()[:12]


def build():
    files = sorted(RAW.glob("*.md"))
    samples = []
    for f in files:
        size = f.stat().st_size
        h = content_hash(f)
        samples.append({
            "filename": f.name,
            "content_hash": h,
            "size_bytes": size,
        })
    idx = {
        "version": "v3.0",
        "created": "2026-09-04",
        "source_dir": str(RAW.absolute()),
        "sample_count": len(samples),
        "total_size_bytes": sum(s["size_bytes"] for s in samples),
        "samples": samples,
    }
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ index.json 已更新: {len(samples)} sample")
    for s in samples:
        print(f"  - {s['filename'][:50]} ({s['size_bytes']:,}B, hash={s['content_hash']})")


if __name__ == "__main__":
    build()