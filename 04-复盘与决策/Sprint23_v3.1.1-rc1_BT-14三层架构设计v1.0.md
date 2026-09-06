# PJ-102 BT-14 三层架构 v1.0 设计方案

> **触发**:王老师 2026-09-06 OUT-OF-BAND "按推荐执行"→ L2 BT-14 三层架构评估
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **关联**:Sprint 23 L2.1 数据模型设计

---

## 🎯 BT-14 三层架构目标

**问题**:当前 wiki 缺少清晰的**数据血缘**追溯,原始录音 → 引用 → 实体卡 → 知识库的链条混乱。

**目标**:建立 **raw → citations → wiki** 三层架构,每层职责清晰可追溯。

---

## 📐 三层架构设计

### Layer 1: raw(原始层)

**职责**:保留**最原始**的内容,只读,严禁修改。

**目录**:
- `02-知识库/PJ-102/raw/`
  - `meetings/` — 原始录音转写(MD/text,来源 AUD)
  - `clips/` — Web Clipper 抓取的网页/文章(来源 URL)
  - `external/` — 外部资料(微信/飞书原文 JSON)
  - `attachments/` — 原始附件(录音/图片/PDF)

**特征**:
- 不可修改(只读权限)
- 不参与 schema 校验
- 每个文件有原始来源标记(audio_filename/url/chat_export)

### Layer 2: citations(引用层)

**职责**:**结构化引用** raw 层的关键片段,每条引用可追溯回原始。

**目录**:
- `02-知识库/PJ-102/citations/`
  - `judgments/` — 从 raw 抽取的**判断/观点**(每条 = raw 文件 + offset + 原文)
  - `concepts/` — 从 raw 抽取的**概念定义**(每条 = 多 raw 源汇总)
  - `scenarios/` — 从 raw 抽取的**场景**(每条 = 多 judgment 聚合)
  - `quotes/` — 直接引用(raw 文件 + offset + 原文)

**特征**:
- 每个引用含:**raw_source + offset + original_text + structured_data**
- 可被反复重用
- 修改受控(每次修改留 audit trail)

### Layer 3: wiki(知识库层)

**职责:**面向王老师的高质量知识卡 + 实体页 + 检索图谱。

**目录**:
- `02-知识库/PJ-102/wiki/`
  - `persons/` — 人物实体卡(99/99 已填)
  - `meetings/` — 会议汇总(从 raw + citations 编译)
  - `concepts/` — 概念主题卡(从 citations 编译)
  - `judgments/` — 判断汇总卡(从 citations 编译)
  - `index.md` — 知识库索引
  - `CLAUDE.md` — Agent 上下文

**特征**:
- 可读、可写、可搜索
- 每个内容**反向链接**到 citations
- 由 atomicstrata 编译器自动维护

---

## 🔄 三层数据流

```
┌─────────────┐
│   RAW 层     │  (不可修改)
│ meetings/   │
│ clips/      │  → 原始录音转写
│ external/   │  → Web Clipper
└──────┬──────┘  → 微信/飞书原文
       │
       │ LLM 抽取(Offset + 原文 + 引用)
       ▼
┌─────────────┐
│ CITATIONS层 │  (受控修改)
│ judgments/  │
│ concepts/   │  → 结构化判断
│ scenarios/  │  → 结构化概念
│ quotes/     │  → 场景汇总
└──────┬──────┘  → 直接引用
       │
       │ LLM 编译(引用 → 实体卡)
       ▼
┌─────────────┐
│   WIKI 层    │  (可读可写)
│ persons/    │
│ meetings/   │  → 人物实体
│ concepts/   │  → 会议汇总
│ judgments/  │  → 概念主题
│ index.md    │  → 判断汇总
└─────────────┘  → 知识库索引
```

---

## 📊 与当前架构对比

### 改进点

| 维度 | 当前 | 改进后 |
|---|---|---|
| 数据血缘 | 混乱(直跳 wiki) | 三层清晰(raw → citations → wiki) |
| 引用可追溯 | 无 | 100%(每条 citation 有 raw_source + offset)|
| 重用性 | 低(每个 wiki 重新抽取) | 高(citations 可被多 wiki 复用)|
| 修改审计 | 无 | 受控(citations 每次修改留 audit)|
| 工具支撑 | 混合 | 分层(每层独立工具)|

### 迁移成本

| 子任务 | 文件数 | 时间 |
|---|---|---|
| L2.1 数据模型设计 | 1 | 0.5 天 |
| L2.2 目录创建 | 3 | 0.5 天 |
| L2.3 数据迁移(raw → citations) | ~150 judgments | 2-3 天 |
| L2.4 数据迁移(citations → wiki) | ~7 categories | 1-2 天 |
| L2.5 工具支撑 | 4-5 个脚本 | 2-3 天 |
| **总计** | - | **6-9 天** |

### 风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 数据迁移破坏现有 wiki | 高 | 先备份 + 灰度迁移 |
| LLM 抽取成本 | 中 | 分批处理 |
| 三层概念学习成本 | 中 | 写明确文档 |

---

## 🚀 L2 BT-14 实施路径

**推荐顺序**(7-9 天):

| 天 | L 单元 | 交付 |
|---|---|---|
| Day 1 | L2.1 三层数据模型 | 本文 + schema 定义 |
| Day 2 | L2.2 目录创建 | raw/citations/wiki 三层 |
| Day 3-4 | L2.3 raw → citations 迁移 | 150 judgments → citations |
| Day 5-6 | L2.4 citations → wiki 迁移 | 7 categories → wiki 重编译 |
| Day 7-8 | L2.5 工具支撑 | scripts/raw2citations.py + citations2wiki.py |
| Day 9 | L2.6 测试 + 评审 | 154 PASS + Codex review |

---

## 💡 王老师单一推荐路径

**A 选项**(推荐):**完整 L2 实施**(7-9 天),建立三层清晰架构
**B 选项**:**仅 L2.1 + L2.2**(1 天),先建空架构,后续填充
**C 选项**:**暂缓 BT-14**,先做 L3 codex 登录 + L4 Web Clipper 完整化

王老师按推荐选 **A**(已选:按推荐执行)。开始 Day 1 L2.1。

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**关联**:Sprint 23 L2 BT-14 三层架构评估
**下一里程碑**:L2.2 目录创建 → Day 2