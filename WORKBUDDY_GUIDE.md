# PJ-102-LLM-MeetingKB · workbuddy AI Agent 接入指南

> **本文档专门为 AI Agent 编写**（workbuddy）
> **目标**: 让 workbuddy 在自己的环境中理解和运行 PJ-102

---

## 🤖 给 AI Agent 的项目本质说明

PJ-102-LLM-MeetingKB 是一个**完全独立**的会议转写→知识库处理项目。

**核心架构**：
```
源文件 (.md) → 12 步 LLM Pipeline → WIKI Markdown
```

**关键约束**：
- ✅ 不依赖任何其他项目（完全独立）
- ✅ 12 步处理（每步独立 LLM 调用）
- ✅ 5 类 WIKI 输出（meeting / person / concept / judgment / comparison）
- ✅ 已验证质量（王老师认可 10 个样本）

---

## 📁 重要文件清单（按优先级）

### 🔴 必须读（5 个）
1. `README.md` — 项目入口（500 字符内）
2. `培训材料/使用手册_v1.0.md` — 完整使用说明
3. `02-设计/系统架构_v1.0.md` — 系统架构
4. `02-设计/12步Pipeline详细设计_v1.0.md` — 12 步详解
5. `03-执行/code/pipeline.py` — 主入口代码

### 🟡 推荐读（5 个）
6. `02-设计/LLM调用架构_v1.0.md` — LLM 关键修复（重要！）
7. `培训材料/FAQ_v1.0.md` — 常见问题
8. `04-复盘与决策/故障处理手册_v1.0.md` — 故障处理
9. `01-需求/需求总纲_v1.0.md` — 需求文档
10. `tests/unit/smoke_test.py` — 测试代码

### 🟢 可选读（其他文档）
- 设计文档（02-设计/）
- 复盘文档（04-复盘与决策/）
- 培训材料（培训材料/）
- 需求文档（01-需求/）

---

## 🚀 5 步快速运行

### Step 1: 克隆项目

```bash
git clone git@github.com:foreverkol/PJ-102-LLM-MeetingKB.git
cd PJ-102-LLM-MeetingKB
```

### Step 2: 阅读核心文档（理解项目）

**最少阅读时间**: 30 分钟

按顺序阅读：
1. `README.md`（5 分钟）
2. `STATE.md`（3 分钟）
3. `培训材料/使用手册_v1.0.md`（10 分钟）
4. `02-设计/系统架构_v1.0.md`（5 分钟）
5. `03-执行/code/pipeline.py`（7 分钟）

### Step 3: 配置环境变量

```bash
# 创建 .env 文件
cat > .env << 'EOF'
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_CN_BASE_URL=https://api.minimaxi.com/v1
EOF
```

**关键**：
- `MINIMAX_API_KEY` 必须 > 100 字符
- `MINIMAX_CN_BASE_URL` **必须是** `https://api.minimaxi.com/v1`（不是 `api.minimax.chat`）
- 端点路径：`/text/chatcompletion_v2`（base_url 已含 `/v1`，端点不重复）

### Step 4: 复制源文件 + 生成索引

```bash
# 创建源文件目录
mkdir -p system/data/raw

# 复制 workbuddy 自己的源文件
cp /path/to/workbuddy/源文件/*.md system/data/raw/

# 生成索引
python3 -c "
import json, hashlib, re
from pathlib import Path
SRC = Path('system/data/raw')
samples = []
for f in sorted(SRC.glob('*.md')):
    content = f.read_text(encoding='utf-8')
    h = hashlib.sha256(content.encode()).hexdigest()[:12]
    m = re.search(r'(202\d)(\d{2})(\d{2})', f.name)
    date = f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else 'unknown'
    samples.append({'filename': f.name, 'content_hash': h, 'date': date, 'size_bytes': len(content)})
Path('system/data/index.json').write_text(
    json.dumps({'version': 'v1.0', 'sample_count': len(samples), 'samples': samples},
              ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print(f'Indexed {len(samples)} samples')
"
```

### Step 5: 验证 + 跑批

```bash
# 验证（9 个测试必须全过）
python3 tests/unit/smoke_test.py

# 跑 5 个样本（验证流程）
cd 03-执行/code
python3 pipeline.py --limit 5

# 跑全量（生产）
python3 pipeline.py
```

---

## 🧠 关键架构理解（给 AI Agent）

### 12 步 Pipeline

```
S1 基础信息（规则）→ S2 场景识别（LLM）→ S3 标准摘要（LLM）→
S4 FJV 三分法（LLM）→ S5 隐性知识（LLM ×3）→ S6 5 类实体（LLM）→
S7 决策+行动（LLM）→ S8 风险+盲区（LLM）→ S9 知识归类（LLM）→
S10 认知提炼（LLM）→ S11 价值评级（LLM）→ S12 WIKI 写入（规则）
```

**LLM 调用次数**: 约 11 次/文件（每个 S2-S11）

### 关键修复（避免踩坑）

#### 1. MiniMax base_url 必须是 `api.minimaxi.com`（不是 `api.minimax.chat`）

```python
# 错误：
base_url = "https://api.minimax.chat/v1"
# 正确：
base_url = "https://api.minimaxi.com/v1"
```

#### 2. 端点路径不含 `/v1` 前缀

```python
# 错误（重复 /v1）：
url = f"{base_url}/v1/text/chatcompletion_v2"
# 正确（base_url 已含 /v1）：
url = f"{base_url}/text/chatcompletion_v2"
```

#### 3. JSON 容错解析

LLM 返回可能含 markdown 包裹、尾随逗号。代码已实现 `safe_json_parse()` 自动处理。

#### 4. PROJECT_ROOT 路径

```python
# 错误（多算一层）：
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
# 正确：
PROJECT_ROOT = Path(__file__).parent.parent.parent  # 3 层
```

#### 5. Python 相对 import

steps/ 子目录用绝对路径：
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_client import LLMClient
```

---

## ⚠️ workbuddy 易错点

1. **忘记 source env**: API key 没设置会失败
2. **路径硬编码**: `system/data/raw/` 必须有源文件
3. **base_url 错误**: 写成 `api.minimax.chat` 必然 404
4. **端点路径错误**: 重复 `/v1` 前缀必然 404
5. **JSON 解析失败**: LLM 返回非标准 JSON（已容错）

---

## ✅ 验证清单（workbuddy 必查）

- [ ] GitHub 仓库克隆成功
- [ ] 5 个核心文档已读
- [ ] .env 配置正确（API key > 100 字符）
- [ ] 源文件已复制到 system/data/raw/
- [ ] index.json 已生成
- [ ] 烟雾测试 9/9 通过
- [ ] 5 个样本跑通
- [ ] WIKI 输出到 `02-知识库/PJ-102-LLM-MeetingKB/meetings/`

---

## 🎯 workbuddy 关键能力清单

workbuddy 在自己的环境必须具备：
- [ ] Linux/macOS/WSL 环境
- [ ] Python 3.11+
- [ ] 网络访问 `api.minimaxi.com`
- [ ] 至少 100 MB 磁盘空间
- [ ] （可选）GitHub Actions 理解

---

## 📊 预期输出

每个源文件 → 1 个 meeting WIKI（约 13 KB，~250 行）

**WIKI 包含 12 章节**：
1. 基础信息
2. 场景识别
3. 标准摘要
4. FJV 三分法
5. 隐性知识
6. 5 类实体
7. 决策和行动项
8. 风险与盲区
9. 知识归类
10. 认知提炼
11. 价值评级
12. 元信息

---

## 🆘 出错怎么办

1. 看 `04-复盘与决策/故障处理手册_v1.0.md`
2. 看 `培训材料/FAQ_v1.0.md`
3. 检查日志 `system/logs/`
4. 联系王老师或 Agent

---

## 📞 联系信息

- **GitHub**: https://github.com/foreverkol/PJ-102-LLM-MeetingKB
- **王老师**: 项目需求方 + 质量验收
- **workbuddy**: 接收方 AI Agent

---

**王老师认可质量**: "meetings 质量非常不错"（v1.0 13/13 验证）

---

## 🎁 给 workbuddy 的一句话总结

> 这个项目是一个**完整的、可独立运行的会议转写→知识库系统**。
> 你需要做的是：克隆 → 读 5 个文档 → 配 .env → 复制源文件 → 跑测试 → 跑批。
> 关键修复：base_url 用 `api.minimaxi.com`，端点用 `text/chatcompletion_v2`。
> 完成 5 步后，workbuddy 就具备了在任何会议录音上运行 PJ-102 的能力。
