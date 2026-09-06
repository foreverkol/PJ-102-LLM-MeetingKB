---
pj: PJ-102
title: PJ-102 Sprint 21 · 原生 LLM Wiki 核心实现 · 详细迭代方案 v1.0
version: v3.0.1-stable + Sprint 21 设计
date: 2026-09-05
status: 📋 设计阶段(等待评审)
method: 王老师语音 9-05 详化 + Sprint 18 Karpathy 对照 + 9-05 外部研究
---

# PJ-102 Sprint 21 · 原生 LLM Wiki 核心实现 · 详细迭代方案 v1.0

> **王老师核心诉求(2026-09-05 语音)**:
> 1. **基于 PJ-102 原生基础上 + Karpathy 核心逻辑实现**,不调 atomicstrata 黑盒
> 2. **关键逻辑必须自己实现**(raw→citations→wiki / 增量更新 / 矛盾标注 / Sources[])
> 3. **借鉴,不是抄** — 参考 atomicstrata 设计哲学 + Karpathy 模式
> 4. **需求设计要全量及时同步**(STATE.md / dashboard / VERSION)
> 5. **稳妥逐步迭代** — 一步一个脚印

---

## 第一部分:外部参考研究(王老师要求"专业参考")

### 1.1 Karpathy LLM Wiki 官方核心(2026-02 起源)

**来源**:karpathy/gist(2026-02 公开)+ 多个社区实现

**3 个核心原则**(原文引用):
1. **"The LLM writes and maintains the wiki; the human reads and asks questions."**
2. **"The wiki is a persistent, compounding artifact."**
3. **Grounding Invariant** — 每个 load-bearing fact 必须 verbatim 存在于 raw 文件中

**三层架构**:
- `raw/` — 不可变源材料(Karpathy 关键设计)
- `wiki/` — LLM 维护的 wiki(`index.md` + `log.md`)
- `SKILL.md` — Schema 层(定义结构 + 工作流规则)

**完整工作流**:
- **Ingest 5 步**:Fetch → Triage → Compile → Cascade → Post-Ingest
- **Query 4 步**:读 index → 全文搜索 → 读文章 → 优先 wiki 内容
- **Lint 3 类**:Safe Fixes(自动)/ Mechanical Reports(报告)/ Judgment Reports(判断)

### 1.2 atomicstrata(具体实现参考)

**来源**:atomicstrata/llm-wiki-compiler(GitHub, MIT v1.1.0,2026-09-05 实测)

**关键设计**:
- **Configurable Lifecycle Profiles (CLP)** — `.llmwiki/profile.json` 是 single contract
- **12 entities × 12 relations × 7 artifacts × 5 workflows**
- **3 层状态机**:lifecycle state machine + workflow run state
- **每个 page 写入前验证**:entity type / required fields / relation preconditions

**实测(2026-09-05)**:
- ✅ 自动 sources[] 字段(file 级引用)
- ✅ 自动矛盾检测(contradictions)
- ✅ 跨文档 query 中文 100% 命中
- ❌ 默认只产 concepts/(compile 默认行为,profile 声明的 5 类不被生成)
- ⚠️ 行号引用是 prose 中提及,非结构化 frontmatter

**王老师决策**:**借鉴 atomicstrata 的 profile 设计和 lifecycle 思想,但所有代码自己写**(不调 npm 包)。

### 1.3 社区 3 个典型实现

| 实现 | 核心价值 | 局限 |
|------|---------|------|
| **rohitg00 v2** (2026-03) | confidence scoring + supersession + contradiction detection | 没开源完整 schema |
| **ashbhatia Substack** (2026-04) | sources[] 强制 raw/ 完整路径(不只是文件名)| v1.2 才加,迁移成本大 |
| **cozypet "Schema Is the Product"** | **关键洞察:80% 努力放 schema,wiki 自动生成** | 没代码,纯架构 |

**关键洞察(王老师借鉴)**:
- **80/20 法则**:schema 设计比实现重要 4 倍 — 王老师 9-04 已设计 8 entities(P0 基础)
- **ling 优先级**:先 lint 后 ingest,避免"compiling garbage"
- **Sources 必填**:`sources:` 必须是 Obsidian [[]] 完整路径,不是文件名(对应 PJ-102 P2 严重违反)

### 1.4 PJ-001-05i 内部实战参考

**已有产物**(2026-09-05 实测):
- poc_2026q3_llmwiki/poc_outputs/ 多个 phase 目录
- concepts/ 多个 phase,每个 ~5-15 个 concept
- 跟 PJ-102 的差异:phase21 用 PJ-001-finance profile,跑的是 PJ-001 财务数据

**PJ-102 借鉴**:
- 王老师已经有 PJ-001 + PJ-102 两套 LLM Wiki 实践
- PJ-001-05i 的 schema 可复用 + 优化
- 跳过 PJ-001 早期 phase 的试错(proven 路径)

---

## 第二部分:王老师已有工作摸底(冲突清单)

### 2.1 ✅ 已完成(不需要重复)

| 项 | 位置 | 状态 |
|---|------|------|
| 8 entities 完整 profile 设计 | `02-设计/atomicstrata-profile.json` (3424 B) | ✅ |
| v6.1 P-1/P-2/P-3/P-4 4 补丁 | `03-执行/code/steps/s12_wiki.py` | ✅ |
| v7.0 ldamc 5 维 + 10 新规 | `03-执行/code/steps/s12_wiki.py` | ✅ |
| Karpathy 完整对照 | `04-复盘与决策/Sprint18_全项目复盘_Karpathy对照_优化方案.md` | ✅ |
| P0-P3 优先级方案 | Sprint 18 报告第 4 部分 | ✅ |
| Sprint 18-22 路线图 | Sprint 18 报告第 5 部分 | ✅ |
| 70 commits + v3.0.1-stable tag | git tag `ff7ca8e` | ✅ |
| L1 测试 82 个 100% PASS | `03-执行/tests/unit` | ✅ |
| atomicstrata PoC | `03-执行/poc_atomicstrata/` (24 concepts) | ✅ |

### 2.2 ❌ 缺失(需要 Sprint 21 实现)

| 缺失项 | Karpathy 要求 | 影响 | 优先级 |
|--------|-------------|------|--------|
| **wiki/index.md** 全局索引 | 必须 | Query 效率低 | **P0** |
| **wiki/log.md** 操作日志 | 必须 | 无法审计历史 | **P1** |
| **check_evidence.py** Grounding Invariant 验证 | 必须 | 77% persons 关联事实为空 | **P0** |
| **Triage**(New/Update/Disputed/No material)| 必须 | 每次 ingest 创建新文件不合并 | **P1** |
| **Cascade Updates** 涟漪更新 | 推荐 | 同 entity 多版本不联动 | **P1** |
| **Status: Disputed 块** | 推荐 | 矛盾知识可能并存 | **P2** |
| **Sources[] 行号级引用** | 必须 | 当前只有 source_meeting 字段 | **P0** |
| **content_hash dedup** | 必须 | 重复处理同 source | **P0** |
| **3 类缺失 entities**(organization / decision / external_ref) | 王老师 profile 要求 | profile 已设计但未实现 | **P1** |
| **person 16 字段深度化** | 王老师 profile 要求 | 当前只有基础 10 字段 | **P2** |
| **scenario 实质化** | 王老师 profile 要求 | 当前 1.1 KB 空壳 | **P2** |
| **Archive 归档页面** | 推荐 | Query 答案无持久化 | **P3** |
| **Query 同义词扩展** | 推荐 | kb_retriever 缺同义词表 | **P2** |
| **三层架构 citations 层** | 推荐 | 缺中间层 | **P3** |
| **CLI**(ingest/compile/query/lint/status) | 推荐 | 当前只能手动跑 pipeline.py | **P2** |

### 2.3 ⚠️ 冲突点(王老师要求"定在方案里")

| # | 冲突点 | A 方案 | B 方案 | 王老师选择 |
|---|--------|--------|--------|-----------|
| C1 | atomicstrata 处理 5 篇 PoC 数据 | 保留作 reference | 删除(占空间)| **保留**(王老师 9-05 决策) |
| C2 | s4-s12 vs atomicstrata 取舍 | 配合(A 方案)| 替换 | **配合**(王老师 9-05 决策) |
| C3 | PJ-001-05i vs PJ-102 Sprint 21 | 共享 profile | 独立 | **共享**(借鉴 PJ-001-05i proven 路径) |
| C4 | Sprint 21 起点 | 重写 profile | 扩展 profile | **扩展**(v3.0.1-stable 不破坏) |
| C5 | LLM 调用预算 | 不限 | 限 MiniMax-M3 | **限 MiniMax-M3**(9-04 王老师决策) |
| C6 | Sprint 21 与 Sprint 18 P0 重叠 | 跳过已写 | 全部重写 | **跳过已写**(check_evidence.py Sprint 18 已规划) |

---

## 第三部分:详细需求规格(Sprint 21)

### 3.1 功能需求(FR)

| FR 编号 | 需求描述 | 优先级 | 验收标准 |
|---------|---------|--------|---------|
| **FR-21-01** | 补 3 类缺失 entities: organization / decision / external_ref | P1 | 各 1 个 step + s12 写入函数,跑 3 个 sample 验证 |
| **FR-21-02** | scenario 实质化(1.1 KB → 5 KB) | P2 | s14_scenario.py 重写 + 13 字段全填 |
| **FR-21-03** | person 16 字段深度化 | P2 | s6_entity.py 升级 + LLM prompt 增强 |
| **FR-21-04** | Sources[] 行号级引用 | **P0** | citations.py + s12 写入 + lint 验证 |
| **FR-21-05** | content_hash dedup 增量更新 | **P0** | triage.py + 4 dispose(Insert/Update/Disputed/Skip) |
| **FR-21-06** | 矛盾自动检测(judgment.contradictions) | P2 | dispute_detector.py 升级 + lint_wiki 集成 |
| **FR-21-07** | check_evidence.py Grounding 验证 | **P0** | scripts/check_evidence.py 150 行 + 跑通 276 文件 |
| **FR-21-08** | wiki/index.md 全局索引 | **P0** | scripts/build_index.py 自动生成 |
| **FR-21-09** | wiki/log.md 操作日志 | P1 | scripts/build_wiki_log.py + append-only |
| **FR-21-10** | Triage 4 状态判定 | P1 | triage.py + 嵌入 pipeline.py |
| **FR-21-11** | Cascade Updates 涟漪更新 | P1 | cascade_updater.py + 跑通单 source 测试 |
| **FR-21-12** | CLI(ingest/compile/query/lint/status)| P2 | cli.py 300 行 + 5 子命令 |
| **FR-21-13** | Query 同义词扩展 | P2 | kb_retriever.py + SYNONYMS 表 |
| **FR-21-14** | 三层架构 raw/citations/wiki | P3 | raw/ 中间层 + citations JSON 层 |
| **FR-21-15** | Status: Disputed 块 | P2 | s12_wiki 加 status 字段 |

### 3.2 非功能需求(NFR)

| NFR 编号 | 需求描述 | 验收标准 |
|---------|---------|---------|
| **NFR-21-01** | 不引入 atomicstrata npm 包 | `package.json` 不存在 + grep 检查 |
| **NFR-21-02** | 不破坏 v3.0.1-stable tag | git tag ff7ca8e 不变 |
| **NFR-21-03** | 不删除现有 5 类 entities | s12_write_xxx 5 函数保留 |
| **NFR-21-04** | 王老师可审计(每 entity sources[])| lint_wiki 检查覆盖率 100% |
| **NFR-21-05** | LLM-native(不用正则模板糊弄)| 每 step 真 LLM 调用 |
| **NFR-21-06** | 代码可读(王老师 Python 水平)| 单文件 < 500 行 |
| **NFR-21-07** | 全量 L1 测试通过 | 82 → 100+ 测试全 PASS |
| **NFR-21-08** | 文档全量同步 | STATE.md / dashboard / VERSION 同步 |

---

## 第四部分:详细设计(技术规格)

### 4.1 模块架构

```
03-执行/code/
├── pipeline.py              (主入口,159 行,✅ 不动)
├── llm_client.py            (LLM 客户端,242 行,✅ 不动)
├── citations.py             [升级] +100 行 P2 行号级引用
├── triage.py                [升级] +200 行 4 dispose + content_hash
├── dispute_detector.py      [升级] +150 行 contradictions 字段集成
├── lint_wiki.py             [升级] +100 行 4 维检查
├── kb_retriever.py          [升级] +80 行 SYNONYMS 同义词扩展
├── check_evidence.py        [新增] 200 行 Grounding Invariant 验证
├── cli.py                   [新增] 300 行 5 子命令
├── state.py                 [新增] 150 行 state.json 状态机
└── steps/
    ├── s1_basic.py          (✅ 不动)
    ├── ...                  (s2-s11 不动)
    ├── s12_wiki.py          [升级] +300 行 8 类全实现 + sources[] 注入
    ├── s13_financial_params.py (✅ 不动)
    ├── s14_scenario.py      [升级] 1.1KB → 5KB
    ├── s15_organization.py  [新增] 200 行
    ├── s16_decision.py      [新增] 200 行
    ├── s17_external_ref.py  [新增] 200 行
```

### 4.2 数据流

```
原始录音 (.md)
  ↓ fetch
raw/{topic}/YYYY-MM-DD-slug.md (immutable, 留 sha256 frontmatter)
  ↓ triage(content_hash)
[New | Update | Disputed | No material]
  ↓ compile (LLM call)
citations/{slug}.json (行号 + 引用)
  ↓ write
wiki/{topic}/{article}.md (sources[] 数组 + Status 块)
  ↓ lint
[Safe fixes | Mechanical reports | Judgment reports]
```

### 4.3 关键接口

**triage.py**:
```python
def triage(source: dict, existing_wiki: dict) -> Literal['New', 'Update', 'Disputed', 'No material']:
    """根据 content_hash 判断处置"""
```

**citations.py**:
```python
def extract_citations(wiki_page: str, raw_file: str) -> List[Citation]:
    """从 wiki 页提取每个事实,在 raw 文件中 grep 验证"""
```

**cli.py**:
```bash
python3 cli.py ingest <file>      # 加 raw/
python3 cli.py compile <topic>    # LLM 抽取 → citations → wiki
python3 cli.py query "问题"        # BM25 + LLM 推理
python3 cli.py lint                # 4 维质量报告
python3 cli.py status              # 当前状态
```

---

## 第五部分:迭代计划(一步一个脚印)

### 阶段 S1(本周, 5 天)— P0 基础(对齐 Karpathy 必须项)

| 天 | 任务 | 产出 | Sprint 报告 |
|---|------|------|------------|
| D1 | FR-21-04 Sources[] 行号级引用 | citations.py(100 行)| Sprint21_D1 |
| D2 | FR-21-05 content_hash dedup | triage.py(200 行)| Sprint21_D2 |
| D3 | FR-21-07 check_evidence.py | scripts/check_evidence.py(200 行)| Sprint21_D3 |
| D4 | FR-21-08 wiki/index.md | scripts/build_index.py + index.md | Sprint21_D4 |
| D5 | Sprint 21 S1 报告 + git commit + tag v3.0.2-stable | commit + tag | Sprint21_S1报告 |

**S1 验收**:
- ✅ 276 文件跑通 check_evidence,输出 evidence_errors 报告
- ✅ index.md 自动生成 + 行号引用覆盖率 > 50%
- ✅ 跑 1 sample 测试 dedup(同 hash 二次跑只 1 次 LLM)
- ✅ 82 L1 测试 + 新增 5 个测试全 PASS

### 阶段 S2(第 2 周, 7 天)— P1 缺失 entities + 增量流程

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-01 organization | s15_organization.py + s12_write_organizations |
| D2 | FR-21-01 decision | s16_decision.py + s12_write_decisions |
| D3 | FR-21-01 external_ref | s17_external_ref.py + s12_write_external_refs |
| D4 | FR-21-09 wiki/log.md | log.md + 自动回填历史 |
| D5 | FR-21-10 Triage 4 状态 | 嵌入 pipeline.py |
| D6 | FR-21-11 Cascade Updates | cascade_updater.py |
| D7 | Sprint 21 S2 报告 + 跑 3 sample + tag v3.0.3-stable | commit + tag |

**S2 验收**:
- ✅ 8 entities 全部实现(profile 100% 对齐)
- ✅ log.md 回填历史 + 新增自动 append
- ✅ Triage 4 状态跑 3 sample 全命中
- ✅ L1 测试 92 → 110 个

### 阶段 S3(第 3 周, 7 天)— P2 深度优化

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-02 scenario 实质化 | s14_scenario.py 升级到 5KB |
| D2 | FR-21-03 person 16 字段 | s6_entity.py + LLM prompt |
| D3 | FR-21-06 contradictions 自动检测 | dispute_detector.py 升级 |
| D4 | FR-21-13 Query 同义词 | kb_retriever.py + SYNONYMS |
| D5 | FR-21-15 Status: Disputed 块 | s12_wiki + lint |
| D6 | FR-21-12 CLI 5 子命令 | cli.py 300 行 |
| D7 | Sprint 21 S3 报告 + 全量回归 + tag v3.1.0-minor | commit + tag |

**S3 验收**:
- ✅ 8 entities + 16 字段全实装
- ✅ 矛盾自动检测 + 标注覆盖率 100%
- ✅ CLI 5 命令可用 + 中文 query 准确率 90%+
- ✅ L1 测试 110 → 130+

### 阶段 S4(第 4 周, 5 天)— P3 三层架构 + 评审发布

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-14 raw/citations/wiki 三层 | raw/ 中间层 + citations JSON |
| D2 | 修 persons 67 个空关联事实 | 重跑 + 验证 |
| D3 | 全量回归测试 + lint | 0 evidence error |
| D4 | Sprint 21 完整报告 + 王老师评审 | Sprint21_v1.0报告 |
| D5 | git tag v3.1.0 + GitHub push + 文档发布 | release notes |

**S4 验收**:
- ✅ 276 文件 0 evidence error
- ✅ 三层架构完整(raw/ + citations/ + wiki/)
- ✅ v3.1.0 评审通过 + tag + push

---

## 第六部分:王老师要求"全量同步"的清单

按王老师要求,**需求/设计/改动任何东西都要全量同步**。Sprint 21 涉及同步的文件:

### 6.1 文档同步清单

| 文件 | 何时同步 | 当前状态 |
|------|---------|---------|
| `STATE.md` | 每 Sprint 阶段结束 | 7475 B(9-05 同步 v3.0.1-stable)|
| `EXECUTION_DASHBOARD.md` | 每 Sprint 阶段结束 | 3550 B(自动重生成)|
| `VERSION` | Sprint S1 完工 → v3.0.2-stable | 13 B |
| `VERSION_MANAGEMENT.md` | Sprint S1/S2/S3 完工 | 6762 B |
| `README.md` | Sprint S4 完工 | 3084 B |
| `02-设计/atomicstrata-profile.json` | Sprint S1/S2 完成 | 3424 B(Sprint 18 P2 升级)|
| `04-复盘与决策/` | 每 Sprint 报告落地 | 已有 13 份 Sprint 报告 |
| `STATE.md` 9-04 vs 9-05 增量 | 同步 v3.0.2-stable + Sprint 21 | 已 commit 4f034b6 |

### 6.2 代码同步清单

| 文件 | 同步方式 |
|------|---------|
| `03-执行/code/steps/s12_wiki.py` | git commit(每 stage)|
| `03-执行/code/citations.py` | git commit(Stage 1)|
| `03-执行/code/triage.py` | git commit(Stage 1)|
| `03-执行/code/check_evidence.py` | git commit(Stage 1)|
| 新增 step 文件 | git commit(Stage 2)|

### 6.3 Git 同步策略

- 每 Sprint 阶段(D1-D7)一个 commit
- Sprint 结束打 tag(v3.0.2 → v3.0.3 → v3.1.0)
- 王老师决定是否 push(等评审)

---

## 第七部分:评审与发布流程(王老师"评审"诉求)

### 7.1 评审节奏

| 时点 | 评审者 | 评审内容 | 输出 |
|------|--------|---------|------|
| Sprint S1 结束 | 王老师 | P0 基础是否达标 | 评审通过 → S2 启动 |
| Sprint S2 结束 | 王老师 + 内部 L1 | 8 entities 完整度 | 评审通过 → S3 启动 |
| Sprint S3 结束 | 王老师 | P2 深度优化质量 | 评审通过 → S4 启动 |
| Sprint S4 结束 | 王老师 + GitHub review | 全量验收 | tag v3.1.0 + release |

### 7.2 评审检查清单

每阶段 Sprint 报告需包含:
- [ ] 功能需求完成度(FR 编号列表)
- [ ] 验收测试结果(L1 测试 + 抽样测试)
- [ ] 冲突点处理记录(C1-C6 进展)
- [ ] 文档同步清单(STATE.md / dashboard / VERSION)
- [ ] Git commit + tag 信息
- [ ] 下一阶段计划 + 风险点

---

## 第八部分:风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| MiniMax-CN 高峰期超时(实测 9-05 4 次) | 高 | Sprint 拖延 | 深夜低峰跑批量 + 重试机制 |
| LLM 输出 schema 不一致 | 中 | sources[] 字段缺失 | 强 prompt 约束 + lint 验证 |
| content_hash 碰撞 | 极低 | 误判 | SHA-256(实测无碰撞) |
| 8 entities LLM 调用次数翻倍(原 12 步 → 14 步)| 高 | 成本增加 | 共用 prompt 减少调用 |
| Sprint 21 4 周跨度超期 | 中 | 评审延期 | 分 4 阶段,每阶段独立验收 |

---

## 第九部分:王老师最终决策点

### 决策 1:Sprint 21 启动时机

| 选项 | 时间 | 备注 |
|---|---|---|
| **🟢 A 立即开始**(S1 P0) | 本周 | FR-21-04/05/07/08 优先级最高 |
| 🟡 B 等 A1 报告消化完 | 下周 | 王老师想先看 A1 报告 |
| 🟣 C 等 Sprint 18 P0 实际完工 | 1-2 周后 | Sprint 18 P0-1/2/3 还没真正落地 |

### 决策 2:Sprint 21 范围

| 选项 | 范围 | 时间 |
|---|---|---|
| 🟢 **只做 S1 P0** | 5 天 | 解决 4 个 P0 缺口 |
| 🟡 S1 + S2 | 2 周 | P0 + 3 缺失 entities + Triage |
| 🟣 全 S1-S4 | 4 周 | 完整 Sprint 21 |

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 18:50 CST
**协议版本**: hermes-anti-hallucination v42 + 王老师 v44 教训
**关联文档**:
- Sprint18_全项目复盘_Karpathy对照_优化方案.md(P0-P3 基础)
- Sprint21_原生LLMWiki实现_路线图_v1.0.md(粗略版,9-05 17:46)
- A方案_atomicstrata配合s4s12_路线图_v1.0.md
- A1阶段_atomicstrata_vs_s4s12对比报告.md
- 02-设计/atomicstrata-profile.json(8 entities 设计)

**王老师拍板**:Sprint 21 启动时机 + 范围 → 我立即进入 S1
