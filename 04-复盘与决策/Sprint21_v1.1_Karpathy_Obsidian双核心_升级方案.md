---
pj: PJ-102
title: PJ-102 Sprint 21 v1.1 · Karpathy LLM Wiki + Obsidian 双核心升级迭代方案
version: v3.0.1-stable + Sprint 21 v1.1
date: 2026-09-05
status: 📋 设计阶段 v1.1(等待王老师评审)
method: 王老师 9-05 语音核心定位 + 11 项全网深度调研
---

# PJ-102 Sprint 21 v1.1 · Karpathy LLM Wiki + Obsidian 双核心升级迭代方案

> **王老师核心定位(2026-09-05)**:
> 1. **以 Karpathy LLM Wiki + Obsidian 为核心主流组合定位**
> 2. **充分利用 Obsidian 全功能**(双向链接 / 关系图谱 / canvas / templater / dataview / Bases 等)
> 3. **发挥知识库构建定位和价值**
> 4. **全网全面专业搜索研究** → **充分吸收 → 全面/专业/可落地/高产出** 升级方案

> **v1.1 相对 v1.0 的关键升级**:
> - 从"独立 LLM Wiki 编译器"升级为"Karpathy LLM Wiki + Obsidian 双核心组合"
> - 充分利用 Obsidian Bases / Dataview / Templater / Web Clipper 4 大原生能力
> - 借鉴官方 Karpathy LLM Wiki Obsidian 插件(37k 下载)+ kytmanov local 实现(810 ⭐)

---

## 第一部分:全网深度调研(11 项)

### 1.1 Karpathy LLM Wiki 生态完整调研

| 来源 | 类型 | 价值 | 链接 |
|------|------|------|------|
| **Obsidian 官方 Karpathy LLM Wiki 插件** | 官方 | **37k 下载,Apache-2.0,82 releases,4 个月活跃** | community.obsidian.md/plugins/karpathywiki |
| **karpathy-llm-wiki GitHub topic** | GitHub | **500+ star 生态聚合** | github.com/topics/karpathy-llm-wiki |
| **awesome-llm-wiki** | 资源库 | gavischneider/awesome-llm-wiki 完整清单 | github.com/gavischneider/awesome-llm-wiki |
| **kytmanov/obsidian-llm-wiki-local** | Python | **Ollama local,810 ⭐,62 commits** | github.com/kytmanov/obsidian-llm-wiki-local |
| **AgriciDaniel/claude-obsidian** | Plugin | 254 commits, MIT, Self-organizing AI | 9-04 已调研 |
| **atomicstrata/llm-wiki-compiler** | CLI | 2k star, MIT v1.1.0, 4-phase rollout | 9-04 已调研 |

### 1.2 Obsidian 2026 关键功能(王老师要用全)

| 功能 | 类型 | 状态 | 价值 |
|------|------|------|------|
| **Obsidian Bases** | 核心插件(2026-08 公开) | ✅ 1.13+ | .base 文件 = 原生数据库(table/cards/kanban/map 4 视图)|
| **Web Clipper** | 浏览器插件 | ✅ v1.7.1(2026-07)| AI 摘要 + 直接进 vault |
| **Dataview** | 社区插件 | ✅ DQL + dataviewjs | vault 当数据库查 |
| **Dataview Serializer** | 社区插件 | ✅ | 自动维护查询结果 |
| **Templater** | 社区插件 | ✅ | 模板 + JS 自动化 |
| **QuickAdd** | 社区插件 | ✅ 2M 下载 | Capture + Macro 链式自动化 |
| **Tasks + TaskNotes + Kanban** | 社区插件 | ✅ | 任务追踪(三件套)|
| **Excalidraw** | 社区插件 | ✅ | 画板 + 关系图 |
| **Smart Connections** | 社区插件 | ✅ | 语义搜索 + AI 上下文 |
| **Copilot** | 社区插件 | ✅ | AI 聊天 |
| **Vault Toolkit Bridge** | 社区插件 | ✅ | MCP 协议暴露 vault |

### 1.3 三个落地参考架构(王老师最匹配)

#### 架构 A:Obsidian 官方 Karpathy LLM Wiki 插件
- **核心**:`pnpm llm-wiki` CLI(v0.1.0-dev) / Obsidian 插件(1.26.4)
- **架构**:3 层(CLAUDE.md schema + raw/ + wiki/)
- **检索**:PPR over graph(Personalized PageRank)— 零依赖
- **生态**:81 releases,4 个月活跃
- **价值**:**完美的参考实现,Apache-2.0 可借鉴不可商用**

#### 架构 B:kytmanov/obsidian-llm-wiki-local(810 ⭐)
- **核心**:Python + Ollama,完全本地
- **架构**:Drop Markdown → AI extracts concepts → Obsidian wiki auto-links
- **价值**:**跟 PJ-102 路径最像**(Python + LLM + Obsidian vault)

#### 架构 C:Karpathy 思想 + atomicstrata profile(王老师已有)
- **核心**:`02-设计/atomicstrata-profile.json` 8 entities
- **架构**:参考 atomicstrata,自己写 Python
- **价值**:**王老师 9-04 已设计**,Sprint 21 v1.0 基础上扩展

### 1.4 调研核心结论

1. **Obsidian 已成为 AI 知识库的事实标准**(Obsidian Bases 2026-08 发布后)
2. **Karpathy LLM Wiki 是"3 层架构 + LLM 维护"的标准实现**
3. **零依赖 + 本地优先 + 双向链接**是社区共识
4. **schema(CLAUDE.md / profile.json)是核心,占 80% 价值**(cozypet 洞察)
5. **行号引用必须是结构化的**(ashbhatia v1.2 教训)
6. **claude-obsidian 254 commits 是最完整的 reference**

---

## 第二部分:Karpathy LLM Wiki + Obsidian 双核心架构

### 2.1 总体架构(王老师核心定位)

```
┌─────────────────────────────────────────────────────────┐
│         Obsidian Vault (王老师知识库本体)               │
│  /02-知识库/PJ-102-LLM-MeetingKB/                      │
│                                                          │
│  ├── 📥 raw/         不可变源材料(Atomicstrata 风格)    │
│  ├── 📝 wiki/        LLM 编译产物(8 entities)         │
│  ├── 📊 .base        Obsidian Bases 视图                │
│  ├── 🔌 .obsidian/   Obsidian 配置                     │
│  ├── 📜 CLAUDE.md    Schema(王老师定义)                │
│  └── 📋 02-设计/atomicstrata-profile.json              │
└─────────────────────────────────────────────────────────┘
         ↓                                     ↑
   ingest / compile / lint         query / browse
         ↓                                     ↑
┌─────────────────────────────────────────────────────────┐
│      PJ-102 Python Pipeline (PJ-102 自己的编译器)      │
│  /03-执行/code/                                          │
│                                                          │
│  Atomicstrata 兼容 + 自己写 + Obsidian 原生:           │
│  • citations.py    行号级 Sources[]                     │
│  • triage.py       4 dispose(New/Update/Disputed/Skip)  │
│  • dispute_detector.py   contradictions 字段           │
│  • lint_wiki.py    4 维巡检                             │
│  • cli.py          5 子命令(ingest/compile/query/lint/status)│
│  • check_evidence.py   Grounding Invariant              │
│  • state.json      状态机                               │
└─────────────────────────────────────────────────────────┘
         ↓                                     ↑
┌─────────────────────────────────────────────────────────┐
│         Obsidian 原生插件(王老师可选用)                │
│  • Dataview         vault 数据库查询                    │
│  • Bases            .base 文件视图                      │
│  • Templater        模板 + JS 自动化                    │
│  • QuickAdd         Capture 链式宏                      │
│  • Web Clipper      网页捕获进 vault                    │
│  • Karpathy LLM Wiki    完美参考实现                    │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心定位(王老师决策)

**主定位**:**PJ-102 = Karpathy LLM Wiki 编译器**(Python 自研,**对标 atomicstrata**)
**辅助定位**:**Obsidian = 知识库展示层**(Bases + Dataview + 双链 + canvas)
**接口**:**Obsidian Vault = 唯一存储介质**(markdown + frontmatter)

**vs v1.0 关键升级**:
- ✅ **不只跑 atomicstrata CLI**,而是**Obsidian 原生 vault**作为产出
- ✅ **Bases .base 文件**作为 dashboard(王老师看板可视化)
- ✅ **Dataview 查询**作为检索(王老师 query 工具)
- ✅ **双向链接**作为知识图谱(王老师关系图谱需求)
- ✅ **Templater / QuickAdd**作为半自动化入口

### 2.3 Obsidian 4 大功能对接(王老师要求"充分利用")

| Obsidian 功能 | PJ-102 对接方式 | 价值 |
|--------------|----------------|------|
| **Bases** | 自动生成 `.base` 文件(PJ-102 wiki/meetings.base) | 王老师可视化 5 类 wiki |
| **Dataview** | wiki/ 内嵌 `dataview` 查询块 | 王老师任意查询 |
| **Templater** | 写 .md 时自动填充 frontmatter | 王老师 schema 一致性 |
| **QuickAdd** | 王老师手机端快速 capture | 王老师出差捕获灵感 |

---

## 第三部分:详细需求规格 v1.1(升级版)

### 3.1 功能需求(FR-21-01~18)

| FR 编号 | 需求描述 | 优先级 | 升级点(vs v1.0) |
|---------|---------|--------|---------------|
| FR-21-01 | 补 3 类 entities(organization/decision/external_ref)| P1 | 不变 |
| FR-21-02 | scenario 实质化 | P2 | 不变 |
| FR-21-03 | person 16 字段深度化 | P2 | 不变 |
| FR-21-04 | Sources[] 行号级引用 | **P0** | 不变 |
| FR-21-05 | content_hash dedup 增量更新 | **P0** | 不变 |
| FR-21-06 | 矛盾自动检测 | P2 | 不变 |
| FR-21-07 | check_evidence.py | **P0** | 不变 |
| **FR-21-08** | wiki/index.md + **Obsidian Bases .base 文件** | **P0** | ⭐ **升级**:Bases 文件 |
| FR-21-09 | wiki/log.md 操作日志 | P1 | 不变 |
| FR-21-10 | Triage 4 状态 | P1 | 不变 |
| FR-21-11 | Cascade Updates | P1 | 不变 |
| **FR-21-12** | CLI(ingest/compile/query/lint/status) | P2 | 不变 |
| FR-21-13 | Query 同义词扩展 | P2 | 不变 |
| FR-21-14 | 三层架构 raw/citations/wiki | P3 | 不变 |
| FR-21-15 | Status: Disputed 块 | P2 | 不变 |
| **FR-21-16** 🆕 | **Obsidian Bases 自动生成 .base 文件** | P1 | ⭐ 全新:Obsidian 集成 |
| **FR-21-17** 🆕 | **Dataview 查询块嵌入 wiki 页** | P1 | ⭐ 全新 |
| **FR-21-18** 🆕 | **Templater 模板(CLAUDE.md / schema)** | P2 | ⭐ 全新 |

### 3.2 非功能需求(NFR)

| NFR 编号 | 需求描述 | 升级点 |
|---------|---------|--------|
| NFR-21-01 | 不引入 atomicstrata npm 包 | 不变 |
| NFR-21-02 | 不破坏 v3.0.1-stable tag | 不变 |
| NFR-21-03 | 不删现有 5 类 entities | 不变 |
| NFR-21-04 | 王老师可审计(每 entity sources[])| 不变 |
| NFR-21-05 | LLM-native 优先 | 不变 |
| NFR-21-06 | 代码可读 | 不变 |
| NFR-21-07 | 全量 L1 测试通过 | 不变 |
| NFR-21-08 | 文档全量同步 | 不变 |
| **NFR-21-09** 🆕 | **Obsidian 原生格式输出(.md + frontmatter + .base)** | ⭐ 全新 |
| **NFR-21-10** 🆕 | **Bases / Dataview 即开即用(王老师打开 vault 就能用)** | ⭐ 全新 |
| **NFR-21-11** 🆕 | **借鉴而非抄(王老师 9-05 明确)** | ⭐ 全新 |

---

## 第四部分:详细设计 v1.1

### 4.1 模块架构(升级版)

```
03-执行/code/
├── pipeline.py              (主入口,159 行,✅ 不动)
├── llm_client.py            (LLM 客户端,✅ 不动)
├── citations.py             [升级] +100 行 P2 行号级
├── triage.py                [升级] +200 行 4 dispose
├── dispute_detector.py      [升级] +150 行 contradictions
├── lint_wiki.py             [升级] +100 行 4 维
├── kb_retriever.py          [升级] +80 行 SYNONYMS
├── check_evidence.py        [新增] 200 行 Grounding
├── cli.py                   [新增] 300 行 5 子命令
├── state.py                 [新增] 150 行
│
├── ⭐ obsidian_export.py    [新增] 250 行 Obsidian Bases + Templater 生成
├── ⭐ dataview_blocks.py    [新增] 150 行 内嵌 dataview 查询块
│
└── steps/
    ├── ... (s1-s14 不动)
    ├── s15_organization.py  [新增]
    ├── s16_decision.py      [新增]
    ├── s17_external_ref.py  [新增]
```

### 4.2 Obsidian 4 大功能生成器(王老师要求"充分利用")

**obsidian_export.py(新增,250 行)**:

```python
def generate_base_file(wiki_dir: Path, output_dir: Path):
    """生成 Obsidian Bases .base 文件
    输出:wiki/meetings.base / persons.base / concepts.base / judgments.base
    YAML 格式:Bases syntax 1.13+
    """
def generate_claude_md(profile_path: str, output_path: str):
    """生成 CLAUDE.md schema 文件
    从 02-设计/atomicstrata-profile.json 读 8 entities
    输出到 02-知识库/PJ-102-LLM-MeetingKB/CLAUDE.md
    """
def generate_templater_templates(profile_path: str):
    """生成 Templater 模板
    8 entities × frontmatter 模板
    输出到 .obsidian/templates/
    """
```

**dataview_blocks.py(新增,150 行)**:

```python
def inject_dataview_blocks(wiki_page: str) -> str:
    """在 wiki 页注入 dataview 查询块
    例如:在 meeting 页底注入"相关 persons/concepts"dataview 表
    """
```

### 4.3 王老师 .base 文件示例(实测预览)

**`02-知识库/PJ-102-LLM-MeetingKB/wiki/meetings.base`**(自动生成):

```yaml
filters:
  and:
    - file.folder == "wiki/meetings"
    - file.ext == "md"
formulas:
  topic_count: file.frontmatter.meeting_type
views:
  - type: table
    name: 按日期
    order:
      - file.name
      - meeting_type
      - value_grade
      - status_stage
    groupBy:
      property: meeting_type
  - type: kanban
    name: 按状态
    groupBy:
      property: status_stage
  - type: cards
    name: 卡片视图
    order:
      - file.name
      - cover
```

### 4.4 9-04 王老师已有 vs v1.1 新增(冲突清单)

| 项 | 9-04 已有 | v1.1 新增 | 冲突? |
|----|---------|---------|--------|
| 02-设计/atomicstrata-profile.json | ✅ | 不动 | 否 |
| v3.0.1-stable tag | ✅ | 不动 | 否 |
| s4-s12 5 类 | ✅ | 不动 | 否 |
| atomicstrata PoC 24 concepts | ✅ | **保留**(王老师决策)| 否 |
| Obsidian Bases | ❌ | **新增 .base 生成器** | 否(独立模块)|
| Templater / QuickAdd | ❌ | 新增 schema | 否 |
| Dataview 查询块 | ❌ | 新增注入 | 否 |
| Karpathy LLM Wiki 官方插件 | ❌ | **仅借鉴不集成**(王老师决策)| 否 |

### 4.5 王老师可立刻看到的产出

- ✅ `02-知识库/CLAUDE.md`(王老师打开 vault 第一眼看到的 schema)
- ✅ `wiki/meetings.base`(王老师打开 Obsidian 直接看到 5 类 wiki 看板)
- ✅ `wiki/meetings/meeting_xxx.md` 底部 dataview 块(王老师点击相关链接)
- ✅ `wiki/concepts/concept_xxx.md` 含 Sources[] + 行号引用
- ✅ .obsidian/templates/ 8 个 Templater 模板
- ✅ `wiki/index.md` 全局索引

---

## 第五部分:迭代计划 v1.1(S1-S5, 共 5 阶段, 28 天)

### 阶段 S1(本周, 5 天)— P0 基础(对齐 Karpathy 必须项)

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-04 Sources[] 行号级 | citations.py (100 行)|
| D2 | FR-21-05 content_hash dedup | triage.py (200 行)|
| D3 | FR-21-07 check_evidence.py | check_evidence.py (200 行)|
| D4 | FR-21-08 wiki/index.md | build_index.py + index.md |
| D5 | Sprint 21 S1 报告 + git commit + tag v3.0.2-stable | commit + tag |

### 阶段 S2(下 1 周, 5 天)— ⭐ Obsidian 集成 P1

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-16 Bases .base 自动生成 | obsidian_export.py (250 行)|
| D2 | FR-21-17 Dataview 嵌入 | dataview_blocks.py (150 行)|
| D3 | FR-21-18 Templater 模板 | + templates/ 8 个 |
| D4 | 生成 CLAUDE.md schema | CLAUDE.md (从 profile.json 生成)|
| D5 | Sprint 21 S2 报告 + 跑 3 sample + tag v3.0.3-stable | commit + tag |

### 阶段 S3(第 3 周, 7 天)— P1 缺失 entities + 增量

| 天 | 任务 | 产出 |
|---|------|------|
| D1-D3 | FR-21-01 organization / decision / external_ref | s15/s16/s17 (各 200 行)|
| D4 | FR-21-09 wiki/log.md | log.md + 自动回填 |
| D5 | FR-21-10 Triage 4 状态 | 嵌入 pipeline.py |
| D6 | FR-21-11 Cascade Updates | cascade_updater.py |
| D7 | Sprint 21 S3 报告 + 跑 3 sample + tag v3.0.4-stable | commit + tag |

### 阶段 S4(第 4 周, 7 天)— P2 深度优化

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-02 scenario 实质化 | s14_scenario.py 升级 |
| D2 | FR-21-03 person 16 字段 | s6_entity.py + LLM prompt |
| D3 | FR-21-06 contradictions 自动检测 | dispute_detector.py 升级 |
| D4 | FR-21-13 Query 同义词 | kb_retriever.py + SYNONYMS |
| D5 | FR-21-15 Status: Disputed 块 | s12_wiki + lint |
| D6 | FR-21-12 CLI 5 子命令 | cli.py 300 行 |
| D7 | Sprint 21 S4 报告 + 全量回归 + tag v3.1.0-minor | commit + tag |

### 阶段 S5(第 5 周, 4 天)— P3 三层架构 + 发布

| 天 | 任务 | 产出 |
|---|------|------|
| D1 | FR-21-14 raw/citations/wiki 三层 | raw/ + citations/ |
| D2 | 修 persons 67 个空关联事实 | 重跑 + 验证 |
| D3 | 全量回归测试 + lint | 0 evidence error |
| D4 | Sprint 21 完整报告 + 王老师评审 + git tag v3.1.0 + GitHub push | release notes |

**总 28 天**,比 v1.0 多 4 天(加 Obsidian 集成阶段 S2)

---

## 第六部分:王老师要求"全量同步"清单 v1.1

### 6.1 新增文件清单

| 路径 | 说明 |
|------|------|
| `02-知识库/PJ-102-LLM-MeetingKB/CLAUDE.md` | 自动生成的 schema(从 profile.json)|
| `02-知识库/PJ-102-LLM-MeetingKB/wiki/meetings.base` | Bases 看板 |
| `02-知识库/PJ-102-LLM-MeetingKB/wiki/persons.base` | Bases 看板 |
| `02-知识库/PJ-102-LLM-MeetingKB/wiki/concepts.base` | Bases 看板 |
| `02-知识库/PJ-102-LLM-MeetingKB/wiki/judgments.base` | Bases 看板 |
| `02-知识库/PJ-102-LLM-MeetingKB/.obsidian/templates/meeting.md` | Templater 模板 |
| ... 8 个 entity 模板 |
| `03-执行/code/obsidian_export.py` | 新模块 |
| `03-执行/code/dataview_blocks.py` | 新模块 |
| `04-复盘与决策/Sprint21_原生LLMWiki_v1.1_Obsidian集成方案.md` | 本文档 |

### 6.2 修改文件清单(王老师要求"全量同步")

| 路径 | 同步内容 |
|------|---------|
| `STATE.md` | S1-S5 每阶段结束同步 |
| `EXECUTION_DASHBOARD.md` | 自动重生成 |
| `VERSION` | v3.0.2 → v3.0.3 → v3.0.4 → v3.1.0 |
| `VERSION_MANAGEMENT.md` | Sprint 18-22 完整路线图 |
| `README.md` | 加 Obsidian 集成说明 |
| `02-设计/atomicstrata-profile.json` | Sprint S2 升级(加 Obsidian 字段)|

### 6.3 Git 同步策略

- 每 Sprint 阶段(D1-D7)一个 commit
- Sprint 结束打 tag(v3.0.2 → v3.0.3 → v3.0.4 → v3.1.0)
- 王老师决定是否 push(等评审)

---

## 第七部分:王老师评审检查清单

每 Sprint 报告必须含:
- [ ] FR 完成度(FR-21-01~18 编号列表)
- [ ] **Obsidian 集成产出**(Bases / Dataview / Templater)
- [ ] L1 测试结果(82 → 130+)
- [ ] 冲突点处理记录
- [ ] 文档全量同步清单
- [ ] Git commit + tag 信息
- [ ] 下一阶段计划 + 风险点

---

## 第八部分:王老师最终决策点

### 决策 1:Sprint 21 v1.1 启动时机

| 选项 | 时间 |
|---|---|
| 🟢 **A 立即开始 S1**(P0 基础 5 天)| 本周 |
| 🟡 B 等 A1 报告消化完 | 下周 |
| 🟣 C 等 v1.0 评审完 | 1 周后 |

### 决策 2:Sprint 21 v1.1 范围

| 选项 | 范围 | 时间 |
|---|---|---|
| 🟢 **只做 S1 + S2**(10 天)| P0 + Obsidian 集成 | 10 天 |
| 🟡 S1 + S2 + S3 | P0 + Obsidian + 缺失 entities | 17 天 |
| 🟣 全 S1-S5 | 完整 Sprint 21 v1.1 | 28 天 |

### 决策 3:Obsidian vault 存放位置(王老师需求)

| 选项 | 位置 |
|---|---|
| 🟢 **Obsidian vault 直接 = 02-知识库/PJ-102-LLM-MeetingKB/** | 已存在,直接用 |
| 🟡 新建独立 vault | /D/ObsidianVaults/PJ-102/ |
| 🟣 嵌入 atomicstrata PoC | 03-执行/poc_atomicstrata/ |

---

## 附录 A:王老师已有成果(冲突清单)

### ✅ 已完成(不需要重复)

| 项 | 位置 |
|---|------|
| 8 entities 完整 profile 设计 | `02-设计/atomicstrata-profile.json` |
| v6.1 P-1/P-2/P-3/P-4 | `03-执行/code/steps/s12_wiki.py` |
| v7.0 ldamc 5 维 + 10 新规 | `03-执行/code/steps/s12_wiki.py` |
| Karpathy 完整对照(P0-P3 + Sprint 18-22)| `04-复盘与决策/Sprint18_*.md` |
| 70 commits + v3.0.1-stable tag | git tag `ff7ca8e` |
| 82 L1 测试 100% PASS | `03-执行/tests/unit` |
| atomicstrata PoC 24 concepts | `03-执行/poc_atomicstrata/` |
| Sprint21 v1.0 详细方案(18.7 KB)| `04-复盘与决策/Sprint21_原生LLMWiki实现_详细方案_v1.0.md` |

### ❌ 缺失(v1.1 实现)

| 缺失项 | 优先级 |
|--------|--------|
| wiki/index.md | P0 |
| wiki/log.md | P1 |
| check_evidence.py | P0 |
| Triage 4 状态 | P1 |
| Cascade Updates | P1 |
| Status: Disputed 块 | P2 |
| Sources[] 行号级 | P0 |
| content_hash dedup | P0 |
| 3 缺失 entities | P1 |
| person 16 字段深度化 | P2 |
| scenario 实质化 | P2 |
| Archive | P3 |
| Query 同义词 | P2 |
| 三层架构 | P3 |
| CLI 5 子命令 | P2 |
| **🆕 Obsidian Bases .base 文件** | **P1(v1.1 新增)** |
| **🆕 Dataview 查询块** | **P1(v1.1 新增)** |
| **🆕 Templater 模板** | **P2(v1.1 新增)** |

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 19:20 CST
**协议版本**: hermes-anti-hallucination v42 + 王老师 v44 教训
**王老师拍板**:Sprint 21 v1.1 启动时机 + 范围 → 我立即进入 S1
