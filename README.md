# PJ-102-LLM-MeetingKB

> 基于 LLM 真实调用（MiniMax M3）+ 12 步 pipeline 的会议转写→知识库全流程处理

[![Status](https://img.shields.io/badge/status-v1.0-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## 🎯 项目简介

PJ-102-LLM-MeetingKB 是一个**完全独立**的会议转写→知识库处理项目。它使用 LLM 真实调用（默认 MiniMax M3）+ 12 步 pipeline，将会议录音原文转换为高质量的 Markdown 知识库。

### 核心特性

- ✅ **12 步全流程**：基础信息 → 场景识别 → FJV → 隐性知识 → 实体 → 决策 → 风险 → 知识归类 → 认知提炼 → 价值评级 → WIKI 落地
- ✅ **LLM 真实调用**：MiniMax M3（中国区，api.minimaxi.com）
- ✅ **5 类 WIKI 产出**：meeting / person / concept / judgment / comparison
- ✅ **完全独立**：零依赖其他项目
- ✅ **生产级质量**：王老师认可 13/13 样本验证

## 🚀 快速开始

### 前置条件

- Python 3.11+
- 网络连接（访问 api.minimaxi.com）
- LLM API key（MiniMax 或其他支持的 provider）

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/wanglaoshi/pj102-llm-meetingkb.git
cd pj102-llm-meetingkb

# 2. 配置环境变量
export MINIMAX_API_KEY="your_key_here"
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"

# 3. 准备源文件
mkdir -p system/data/raw
cp /path/to/your/meeting_transcripts/*.md system/data/raw/

# 4. 生成索引
python3 -c "
import shutil, json, hashlib, re
from pathlib import Path

SRC = Path('system/data/raw')
samples = []
for f in sorted(SRC.glob('*.md')):
    content = f.read_text(encoding='utf-8')
    h = hashlib.sha256(content.encode()).hexdigest()[:12]
    m = re.search(r'(202\d)(\d{2})(\d{2})', f.name)
    date = f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else 'unknown'
    samples.append({
        'filename': f.name,
        'content_hash': h,
        'date': date,
        'size_bytes': len(content)
    })

Path('system/data/index.json').write_text(
    json.dumps({'version': 'v1.0', 'sample_count': len(samples), 'samples': samples},
              ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print(f'Indexed {len(samples)} samples')
"

# 5. 跑批
cd 03-执行/code
python3 pipeline.py --limit 10  # 测试 10 个
python3 pipeline.py              # 全量
```

## 📊 性能

- **单文件处理**：~135 秒（11 次 LLM 调用）
- **成功率**：> 95%（实测 100%）
- **WIKI 大小**：平均 13.9 KB

## 🛠️ 架构

```
PJ-102-LLM-MeetingKB/
├── 01-需求/              5 份需求文档
├── 02-设计/              7 份设计文档
├── 03-执行/code/         Python 代码（16 个文件）
│   ├── pipeline.py       (主入口)
│   ├── llm_client.py     (LLM 客户端)
│   └── steps/            (12 步拆分)
├── 04-复盘与决策/         状态与运维
├── system/               系统目录
├── tests/                测试
├── config/               配置文件
└── 培训材料/             使用手册
```

## 🎯 12 步 Pipeline

| 步骤 | 名称 | 文件 | LLM |
|---|---|---|---|
| S1 | 基础信息 | s1_basic.py | ❌ |
| S2 | 场景识别 | s2_scene.py | ✅ |
| S3 | 标准摘要 | s3_summary.py | ✅ |
| S4 | FJV 三分法 | s4_fjv.py | ✅ |
| S5 | 隐性知识 | s5_implicit.py | ✅ ×3 |
| S6 | 5 类实体 | s6_entity.py | ✅ |
| S7 | 决策+行动 | s7_decision.py | ✅ |
| S8 | 风险+盲区 | s8_risk.py | ✅ |
| S9 | 知识归类 | s9_classify.py | ✅ |
| S10 | 认知提炼 | s10_cognitive.py | ✅ |
| S11 | 价值评级 | s11_value.py | ✅ |
| S12 | WIKI 写入 | s12_wiki.py | ❌ |

## 📚 文档

- [需求总纲](./01-需求/需求总纲_v1.0.md)
- [系统架构](./02-设计/系统架构_v1.0.md)
- [12 步 Pipeline 详细设计](./02-设计/12步Pipeline详细设计_v1.0.md)
- [使用手册](./培训材料/使用手册_v1.0.md)
- [FAQ](./培训材料/FAQ_v1.0.md)

## 🧪 测试

```bash
cd tests/unit
python3 smoke_test.py
```

输出：
```
Ran 9 tests in 0.184s
OK
```

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 王老师（需求方 & 质量验收）
- MiniMax M3（LLM Provider）
- Hermes Agent（运行环境）

---

**v1.0** · 2026-09-03 · 王老师认可质量
