# PJ-102 Sprint 21 · 原生 LLM Wiki 核心实现 路线图 v1.0

> **王老师核心诉求**:基于 Karpathy LLM Wiki + atomicstrata 核心逻辑,**自己实现**(不调黑盒),对齐 PJ-102 profile 设计的 8 entities。

---

## 🎯 Sprint 21 目标(一句话)

**在 PJ-102 s4-s12 流水线基础上,实现 Karpathy LLM Wiki 的 P2/P3/P4/P5 核心原则,补齐 8 entities 完整版,出 PJ-102 自己的 LLM Wiki 编译器 v0.1**。

---

## 📊 实测摸底(2026-09-05 王老师语音前)

| 维度 | 当前状态 | 王老师 profile 设计 | 差距 |
|------|---------|-------------------|------|
| 实现 entities 数 | **5**(meetings/persons/concepts/judgments/comparisons)| **8**(+ organization/decision/external_ref)| **缺 3 类** |
| person 字段数 | **10** 基础 | **16** 完整 | **缺 6 深度字段** |
| Sources[] 引用 | `source_meeting` 单字段 | `source_ref` 数组 | **缺数组 + hash** |
| Incremental update | ❌ content_hash dedup 未实现 | ✅ content_hash + 增量跳过 | **缺失** |
| 矛盾标注 | dispute_detector.py 模块存在 | contradictions 字段集成 | **未跟 LLM 链接** |
| 三层架构 | raw → s12_write → 02-知识库 | raw → citations 中间层 → wiki | **缺 citations 层** |
| Profile schema | PJ-102 v3.0 完整 8 entities 已设计 | 同左 | ✅ 已有 |
| 8 entities 完整字段定义 | 02-设计/atomicstrata-profile.json | 同左 | ✅ 已设计 |

**结论**:**profile 已设计,s4-s12 未对齐。Sprint 21 = 把 profile 完整实现出来**。

---

## 🛠️ Sprint 21 实施路径(分 3 阶段)

### 阶段 S1(1-2 周):补 8 entities + 深度字段

**目标**:把 s4-s12 缺失的 3 类补齐,person 升级到 16 字段完整版

具体工作:
1. **新增 organization 实现**
   - `s15_organization.py`(从 s6_entity 拆出 org 字段)
   - 14 字段:org_type / industry / cooperation_status / relationship_depth / business_model / competitive_moat / target_market / revenue_model 等
   - `s12_write_organizations()` 写 `wiki/organizations/org_{hash}.md`

2. **新增 decision 实现**
   - `s16_decision.py`(从 s7_action_decision 扩展)
   - 10 字段:problem / alternatives / chosen / reason / outcome / constraints / review_trigger 等
   - `s12_write_decisions()` 写 `wiki/decisions/decision_{date}_{hash}.md`

3. **新增 external_ref 实现**
   - `s17_external_ref.py`(从外部文章引用,如 9-04 王老师提到的 PJ-901-05 NotebookLM 集成)
   - 6 字段:title / source_url / authors / publication_date / key_claims / can_update_internal
   - `s12_write_external_refs()` 写 `wiki/external_refs/ext_{hash}.md`

4. **升级 person 到 16 字段完整版**
   - 在 s6_entity 增强 prompt,加 6 个深度字段:thinking_framework / values_beliefs / decision_style / emotional_tone / value_chain_position / business_relations
   - `entity_resolver.py` 升级支持 entity_id_pattern `person_{canonical_name_hash8}_{seq4}`

5. **scenario 实质化**(当前 1.1 KB 是空壳)
   - `s14_scenario.py` 从 1.1 KB 扩到 ~5 KB
   - 13 字段全填:theme/customer/pain_point/offering/value_capture/channel/key_resources/key_constraints/hidden_assumptions/trigger_signals/failure_modes/extraction_perspective

### 阶段 S2(2 周):Karpathy P2/P3/P4 核心实现

**目标**:实现 引用溯源 / 增量更新 / 矛盾标注

具体工作:
1. **P2 Sources[] 引用溯源**
   - 新增 `citations.py`(atomicstrata 已有,自己写)
   - 改 s12_wiki:每个 wiki 页加 `sources: [{source_file, line_range, quote}]` 数组
   - 每个 LLM 调用 prompt 加 "必须输出 sources 数组" 强制约束
   - 验证:`lint_wiki.py` 检查所有 wiki 页必须有 sources[] 字段

2. **P3 Incremental update(增量更新)**
   - `triage.py` 增强:处理每个 source 前查 `content_hash`
   - 已处理过(同 hash)→ 跳过
   - 同 source 新版本(同 filename 不同 hash)→ Update 分流
   - 新 source → Insert
   - 改动 entity(同名不同 hash)→ Merge
   - 改 `s12_write_all_5_types()` 支持 4 种 dispose:New/Update/Disputed/Skip

3. **P4 矛盾标注 contradictions**
   - `dispute_detector.py` 升级:每次 LLM 输出 contradictions 字段,自动存入 judgment.contradictions
   - 写 `lint_wiki.py` 报告 contradictions > 0 的页
   - cross-source contradictions:同一 judgment 在不同 source 有冲突 evidence

4. **lint 工具强化**
   - `lint_wiki.py` 增加 4 维:缺 sources / 有 contradictions / stale content(>90 天)/ orphan page(无 inbound link)
   - 输出 JSON 报告到 `04-复盘与决策/lint_reports/`

### 阶段 S3(2 周):三层架构 + CLI

**目标**:对齐 Karpathy 三层架构 + 出 CLI

具体工作:
1. **三层架构(raw / citations / wiki)**
   - 新增 `raw/` 中间层:从 system/data/raw/ 复制 source → raw/{topic}/{source}.md,加 sha256 frontmatter
   - citations 层:每个 wiki 页生成 `_citations/{slug}.json`,含 line_range + quote + provenance
   - wiki 层:s4-s12 现状 02-知识库/PJ-102-LLM-MeetingKB/(已存在)

2. **CLI 命令**(`03-执行/code/cli.py`)
   - `python3 cli.py ingest <file>` → 加 raw/
   - `python3 cli.py compile <topic>` → LLM 抽取 → citations → wiki
   - `python3 cli.py query "问题"` → BM25 + LLM 推理
   - `python3 cli.py lint` → 4 维质量报告
   - `python3 cli.py status` → 当前状态

3. **状态机**
   - `state.json`:每个 entity 的 lifecycle(transcribed→extracted→linked→archived)
   - 复用 atomicstrata profile 的 lifecycle 设计

---

## 📦 交付物(Sprint 21 完整产物)

```
03-执行/code/
├── steps/
│   ├── s15_organization.py       (新增)
│   ├── s16_decision.py            (新增)
│   ├── s17_external_ref.py        (新增)
│   ├── s14_scenario.py            (实质化,1.1KB → 5KB)
│   └── s12_wiki.py                (升级:8 类全实现)
├── cli.py                         (新增,Sprint S3)
├── triage.py                      (升级:增量更新)
├── citations.py                   (升级:P2 引用溯源)
├── dispute_detector.py            (升级:矛盾标注)
├── lint_wiki.py                   (升级:4 维检查)
└── raw/                           (新增中间层)
    └── {topic}/
        └── {source_hash}.md
```

新增 4 个 step, 升级 5 个文件。代码量预估:**+1500 行**(从 4722 → 6222 行)。

---

## 🔒 铁律(王老师底线)

1. **不引入 atomicstrata npm 包** — 所有逻辑自己写 Python
2. **不破坏 v3.0.1-stable tag** — 现有 5 类不删,只补 3 类
3. **增量更新启用** — content_hash 自动跳过已处理
4. **LLM-native 优先** — 每步必须真 LLM 调用,不用正则/模板糊弄
5. **王老师可审计** — 每 entity 都有 sources[] 数组,每条 evidence 都有 line_range

---

## 📊 Sprint 21 vs atomicstrata 对比

| 能力 | Sprint 21 自研 | atomicstrata 黑盒 |
|------|---------------|------------------|
| 8 entities 完整实现 | ✅ PJ-102 profile 对齐 | ❌ 12 entities 是通用模板 |
| Sources[] 引用 | ✅ 行号级 | ⚠️ file 级(prose 提及 line) |
| 矛盾标注 | ✅ judgment.contradictions 字段 | ✅ contradictions 字段 |
| 增量更新 | ✅ content_hash + 4 dispose | ✅ content_hash dedup |
| 三层架构 | ✅ raw/citations/wiki | ✅ raw/citations/wiki |
| 跨文档 query | ✅ 自己写 BM25 + LLM | ✅ 已内置 |
| 中文支持 | ✅ 原生 | ✅ 原生 |
| **代码可审计** | **✅ 自己 Python** | **❌ TypeScript 黑盒** |
| **PJ-102 适配** | **✅ profile 完全对齐** | **⚠️ 默认 profile 不匹配** |

**Sprint 21 的核心价值**:不调黑盒,**代码可审计、profile 可定制、增量可控制**。

---

## 🎯 王老师请决策

| 选项 | 内容 | 时间 | 价值 |
|------|------|------|------|
| **S1 立即开始** | 补 8 entities(1-2 周) | 高 | profile 已设计,实现即可 |
| **S2 立即开始** | P2/P3/P4 核心(2 周)| 高 | 解决 60% Karpathy 违反 |
| **S3 立即开始** | 三层架构 + CLI(2 周)| 中 | 跟 Karpathy 完全对齐 |
| **分阶段推** | S1→S2→S3 各 2 周 | **6 周完整 Sprint 21** | **最稳妥,一步一个脚印** |
| **暂停** | 消化 4 个 commit + 2 个文档 | - | 王老师先看 |

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 18:30 CST
**协议版本**: hermes-anti-hallucination v42
**关联文档**: A1 对比报告 / A 方案路线图 / 02-设计/atomicstrata-profile.json
