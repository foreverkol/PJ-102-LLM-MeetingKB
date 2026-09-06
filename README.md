# PJ-102 LLM Meeting KB

> **项目**:基于 LLM 的会议知识库系统
> **作者**:王老师(资深金融科技专家)
> **维护**:Hermes Agent(MiniMax-M3)
> **当前版本**:`v3.1.3-rc1`
> **状态**:小范围验证准备就绪

---

## 🎯 项目目标

把王老师的**录音转写/外部资料 → atomicstrata wiki → Obsidian Bases/CLAUDE.md**,形成可查询、可追溯、可演化的个人知识库系统。

---

## ✨ 已实现能力(快速概览)

### 4 大子系统

| 子系统 | 描述 | 状态 |
|---|---|---|
| **L2 数据处理层** | 12 步流水线(P1-P5 + 三层编译) | ✅ 运行中 |
| **L3 知识库组织层** | raw → citations → wiki 三层架构 | ✅ 运行中 |
| **L4 工程化层** | 模式 v2.0 + 看板常态化 + Codex 评审 | ✅ 运行中 |
| **L5 跨 PJ 推广** | 24 个 PJ 全部激活 | ✅ 完成 |

### 17 个核心工具(135 KB 代码)

- **状态管理**:`where.py` / `state_to_md.py` / `sync_state.py`
- **看板**:`build_web_dashboard.py` / `kanban_refresh.py` / `pj_swarm.py`
- **三层架构**:`tier_classifier.py` / `raw2citations.py` / `citations2wiki.py` / `llm_cite_extract.py`
- **Codex 评审**:`codex_review.py` / `local_codex_review.py` / `codex_reviewer.py`
- **推送**:`feishu_notify.py`
- **剪藏**:`web_clipper.py` / `notebooklm_rag.py`
- **跨 PJ**:`promote_v2_to_pj.py` / `init_pj_state.py`
- **断点保护**:`save_checkpoint.py`

### 知识库数据

| 资产 | 数量 |
|---|---|
| 总 Wiki 文件 | 402 MD |
| 三层分布 | raw:21 / citations:123 / wiki:255 |
| 人物实体卡 | 99 |
| 概念主题卡 | 137 |
| 判断/观点 | 74 judgments + 50 wiki 编译卡 |

### 测试覆盖

**180 PASS + 1 skipped**(实测)

---

## 🚀 快速开始

### 环境要求

- **Python** 3.11+
- **Node.js** 18+(npm 包)
- **依赖**:`pip install pyyaml requests`(最小集)
- **API Key**:MiniMax-M3(`~/.hermes/config.yaml` 自动读取)

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
cd PJ-102-LLM-MeetingKB

# 2. Python 依赖(最小集)
pip install pyyaml requests

# 3. 验证
python3 scripts/where.py --brief
```

### 5 分钟体验

```bash
# 1. 看推进位置
python3 scripts/where.py --brief

# 2. 看完整面板
python3 scripts/where.py

# 3. 启动 HTML 看板
python3 -m http.server 8788 --bind 0.0.0.0 --directory .kanban
# 浏览器:http://localhost:8788

# 4. 跑 Web Clipper
python3 scripts/web_clipper.py "https://example.com" --tags "test"

# 5. 三层架构扫描
python3 scripts/tier_classifier.py --report
```

---

## 📂 项目结构

```
PJ-102-LLM-MeetingKB/
├── README.md                         # 本文件
├── VERSION                            # 3.1.3-rc1
├── STATE.json                         # 单一真值源
├── STATE.md                           # 自动生成
│
├── 01-需求/                           # 原始需求(王老师发言)
│   └── 原始输入/
│
├── 02-设计/                           # 设计文档
│   └── 设计参考/
│
├── 03-执行/                           # 实施代码
│   ├── code/                          # 核心代码
│   ├── tests/unit/                    # 单元测试
│   ├── pj102-obsidian-export/         # npm 包
│   └── 工具/                          # 工具脚本
│
├── 04-复盘与决策/                     # Sprint 报告 + 决策
│   ├── Sprint22_v3.1.0-stable_*
│   ├── Sprint23_v3.1.1-rc1_*
│   ├── Sprint24_v3.1.2-rc1_*
│   └── Sprint25_v3.1.3-rc1_*
│
├── scripts/                           # 17 个核心工具
├── .kanban/                           # HTML 看板
├── .swarm/                            # 跨 PJ Swarm 看板
├── .codex-reviews/                    # Codex 评审历史
└── .obsidian/                         # Obsidian 配置 + Bases
```

---

## 🎯 王老师单一推荐路径

**当前 Sprint 25 收尾准备 + 小范围验证**:

| # | 步骤 | 时间 |
|---|---|---|
| 1 | **README.md + 能力盘点 v1.0** | 2-3 小时 |
| 2 | **小范围验证 3 主题** | 2-3 小时 |
| 3 | **验证报告 v1.0** | 1 小时 |

---

## 🔗 相关链接

- **GitHub**:https://github.com/foreverkol/PJ-102-LLM-MeetingKB
- **HTML 看板**:http://localhost:8788
- **跨 PJ Swarm**:http://localhost:8789
- **Hermes 项目**:`PJ-904-hermes agent 工程`
- **基线知识库**:`02-知识库/PJ-102-LLM-MeetingKB/`(402 文件)

---

## 📝 License

内部项目,仅供王老师个人使用。

---

**生成**:Hermes Agent(MiniMax-M3)
**协议版本**:王老师 Superpower"按推荐执行"
**下一里程碑**:小范围验证完成 + 验证报告 v1.0