---
type: schema
version: "7.0"
date: 2026-05-05
status: "与设计总纲v9.0配套——所有页面生成以此为准"
parent: "PJ-001 设计总纲 v9.0"
---

# PJ-001 知识库 SCHEMA v7.0

> 页面模板、字段定义、数据格式、规则约束

---

## 一、页面类型体系

| type | 用途 | 目录 | 关键特征 |
|:-----|:-----|:-----|:-----|
| `meeting` | 时间入口，FJV编译 | Meetings/ | ldamc + chapters + contradictions |
| `person` | 人物实体 | Entities/Persons/ | entity_id + business_relations + 隐性知识 |
| `organization` | 机构实体 | Entities/Organizations/ | entity_id + business_relations + cooperation_status |
| `judgment` | 商业判断 | Knowledge/Judgments/ | topic_key + evolved_from + evolved_to + contradictions |
| `decision` | 决策记录 | Knowledge/Decisions/ | constraints + alternatives + expected_outcome |
| `scenario` | 商业模式片段 🆕 | Knowledge/Scenarios/ | customer + pain_point + failure_modes |
| `concept` | 行业概念 | Concepts/ | related_patterns + counter_examples |
| `synthesis` | 跨域综合 | Synthesis/ | topic_aggregation |
| `external_ref` | 外部参考 🆕 | Knowledge/External/ | can_update_internal(false) |
| `moc` | 主题地图 | MOCs/ | dataview_query (可选) |

---

## 二、Meeting 页面模板

```yaml
---
# ═══ 基础 ═══
type: meeting
knowledge_tier: L3_wiki
source_origin: transcript_PJ001
source_ref: "RAW/transcripts/2024/20240825_xxx_原文.md"
perspective: partner       # partner | bank | internal | investor | speaker | expert
date: 2024-08-25
duration_min: 7

# ═══ 参与者 ═══
participants:
  - name: "黄国华"
    entity_id: "person_huangguohua_0001"
    org: "慧穗科技"
    role: "创始人/CEO"

# ═══ 内容索引 ═══
key_topics: [业财税数字化, 税务数据底座, 供应链金融]
chapters:
  - time: "00:00-00:40"
    topic: "三层价值模型"
    type: business

# ═══ 行动项 ═══
action_items:
  - who: "王老师"
    what: "深入评估数据底座对供应链金融的可赋能程度"
    deadline: ""
    status: pending

# ═══ 分类 ═══
subtype: partner             # partner | bank | internal | investor | technical | information
value_grade: A               # S | A | B | C
sensitivity: internal         # public | internal | sensitive | highly-sensitive
publishability: internal      # internal | public (脱敏后)

# ═══ 质量 ═══
review_state: deep_extraction_v2
confidence: extracted         # extracted | inferred | ambiguous | unverified
reusable_for:
  - decision_reference
  - external_expression
  - investor_communication
  - internal_training
  - digital_human_training

# ═══ v7.0 新增 ═══
contradictions:
  - target: "乐意回=传销性质"
    type: conflict
    resolution: pending_verification

ldamc:
  lost: "税局连接是企业数字化的刚性入口"
  different: "SaaS从工具升级为底座+变现双层模型"
  added: "供应链金融新增税务数据入口"
  more: "慧穗客户规模/金融变现案例/竞品验证"
  connected:
    - "供应链金融变现路径"
    - "企业数字化底座"

update_targets:
  - entity: "person_huangguohua_0001"
    action: "update"
    fields: ["last_interact", "capabilities"]

# ═══ 元数据 ═══
tags: [PJ001, 业财税数字化, 商业模式, 供应链金融]
created: 2024-08-25
updated: 2026-05-05
version: 2
---

# 会议标题

## 一句话结论
> 核心判断，单行

## 🔍 核心要点

### 事实 [F]
- **[F] 描述**（证据强度：strong | moderate | weak，依据）

### 判断 [J]
- **[J] 描述**（证据强度：strong | moderate | weak，依据）

### 愿景 [V]
- **[V] 描述**

## 🧠 隐性知识

### 思维框架
### 价值观与信念
### 表达与语言风格

## ⚠️ 待确认 / 知识盲区
- [未量化] ...
- [待校准] ...

## 🔗 关联页面
- [[page1]]
- [[page2]]
```

---

## 三、Person 页面模板

```yaml
---
type: person
knowledge_tier: L3_wiki
name: "黄国华"

# ═══ v7.0 统一实体 ═══
entity_id: "person_huangguohua_0001"
canonical_name: "黄国华"
aliases: ["慧穗黄总"]

# ═══ 基础 ═══
org: "慧穗科技"
job_title: "创始人/CEO"
relation_to_wang: "引荐合作方"
trust_level: medium          # high | medium | low
first_meet: 2024-08-25
last_interact: 2024-08-25

# ═══ 能力 ═══
capabilities:
  resources: [税务局连接能力, 业财税软件平台]
  strengths: [商业模式认知清晰, 表达能力极强]
  weaknesses: [客户规模待验证]
  decision_power: high

# ═══ 隐性知识 ═══
thinking_framework: "递进式问题拆解：降本→促发展→能经营"
values_beliefs: "实质性服务优于渠道收割"
decision_style: "理性分析型，用数据和逻辑推导"
emotional_tone: "自信、开放、专业"

# ═══ 生态位 ═══
value_chain_position:
  upstream: [税局系统]
  downstream: [银行, 保理, 园区/财税公司]
  competitor: [乐意回]
  complementor: [深度数科, 供应链金融平台]

# ═══ v7.0 关系 ═══
business_relations:
  - subject: "person_cuijiasheng_0001"
    predicate: "introduced_by"
    strength: 4
  - subject: "org_huisui_0001"
    predicate: "founded"

# ═══ 状态 ═══
status_stage: compiled         # raw | compiled | reviewed | canonical
adoption_status: native
confidence: extracted

# ═══ 复用 ═══
reusable_for: [external_expression, investor_communication, digital_human_training]
value_grade: A
sensitivity: internal
review_state: deep_extraction_v2

source_ref: "Meetings/20240825_xxx.md"
tags: [PJ001, 业财税数字化, 创业者, SaaS]
created: 2026-05-05
updated: 2026-05-05
version: 1
---
```

---

## 四、Organization 页面模板

```yaml
---
type: organization
knowledge_tier: L3_wiki

# ═══ v7.0 统一实体 ═══
entity_id: "org_huisui_0001"
canonical_name: "慧穗科技"
aliases: ["慧穗"]

# ═══ 基础 ═══
org_name: "慧穗科技"
org_type: fintech             # bank | non_bank_fi | fintech | channel | industry_core | saas | platform
industry: "业财税数字化 / SaaS"

# ═══ 合作 ═══
cooperation_status: target    # active | paused | terminated | target | exploring
relationship_depth: exploring  # strategic | cooperative | pilot | exploring | past

# ═══ 业务 ═══
business_model: "业票财税一体化SaaS，税局连接为核心，数据底座→供应链金融变现"
competitive_moat: "税局强连接+业财税票数据双重锁定"
target_market: "中大企业深度服务 + 小企业渠道分销"
revenue_model: "SaaS订阅+金融服务佣金"

# ═══ 关系 ═══
business_relations:
  - subject: "person_huangguohua_0001"
    predicate: "founded_by"
  - subject: "org_shendu_0001"
    predicate: "cooperates_with"
    status: "exploring"

# ═══ 风险 ═══
risk_detail:
  - "数据安全合规：企业核心经营数据平台化"
  - "税局政策变化风险"
competitors: [乐意回, 传统ERP厂商]

# ═══ 行动 ═══
next_action: "深入评估数据底座对供应链金融的可赋能程度"

# ═══ 状态 ═══
status_stage: compiled
value_grade: A
sensitivity: internal
review_state: deep_extraction_v2
source_ref: "Meetings/20240825_xxx.md"
tags: [PJ001, 业财税数字化, SaaS, 供应链金融]
created: 2026-05-05
updated: 2026-05-05
version: 1
---
```

---

## 五、Judgment 页面模板

```yaml
---
type: judgment
knowledge_tier: L3_wiki

# ═══ v7.0 主题聚合 ═══
topic_key: "bank_cooperation/weizhong"
judgment_id: "J-20230308-001"

# ═══ 判断内容 ═══
statement: "深度数科从撮合平台向综合金融服务商转型是正确方向"
judgment_type: strategic       # strategic | operational | market | personnel | technical
evidence_strength: strong      # strong | moderate | weak | inferred

# ═══ 证据 ═══
evidence_chain:
  - source: "Meeting/20230308_微众银行来访"
    quote: "撮合模式客户还掌握在中介手中"
  - source: "Meeting/20221020_xxx"
    quote: "..."

# ═══ v7.0 演化 ═══
evolved_from: ""
evolved_to: []
contradictions:
  - target_judgment: "J-xxx"
    type: refinement
    resolution: pending_review

# ═══ 反方 ═══
counter_arguments:
  - "直客比例未验证，转型速度可能低于预期"
confidence_rationale: "李洋自我坦白+行业常识"

# ═══ 状态 ═══
status_stage: compiled
verified_status: pending       # pending | verified | disputed | superseded
value_grade: A
sensitivity: internal
source_ref: "Meetings/20230308_xxx.md"
tags: [深度数科, 平台转型, 银行合作]
created: 2026-05-05
updated: 2026-05-05
version: 1
---
```

---

## 六、Scenario（商业模式片段）模板 🆕

```yaml
---
type: scenario
subtype: business_model_fragment
knowledge_tier: L3_wiki

# ═══ 业务定义 ═══
theme: "财税数据→供应链金融变现"
customer: "中大企业的财务部门"
pain_point: "财务部门是成本中心，无法从数据中产生额外收入"
offering: "以税局连接为基础，打通业财税票，形成数据底座，嵌入金融服务"
value_capture: "SaaS订阅 + 金融服务佣金/分润"
channel: "直销（中大企业）+ 园区/财税公司分销（小企业）"

# ═══ 关键资源 ═══
key_resources:
  - "税局系统级连接"
  - "业财税一体化软件"
key_constraints:
  - "税局接口稳定性"
  - "数据安全合规"

# ═══ 深层分析 ═══
hidden_assumptions:
  - "企业愿意将核心经营数据放在第三方平台"
trigger_signals:
  - "企业财务部门有降本增效压力"
  - "企业已有多个银行合作关系，需要统一数据出口"
failure_modes:
  - "税局政策变化阻断连接"
  - "中大企业自研或选ERP巨头方案"

# ═══ 视角 ═══
extraction_perspective: entrepreneur   # entrepreneur | expert | manager | persona

source_ref: "Meetings/20240825_xxx.md"
value_grade: A
sensitivity: internal
tags: [商业模式, 财税SaaS, 供应链金融]
created: 2026-05-05
updated: 2026-05-05
version: 1
---
```

---

## 七、L2编译中间层数据格式

### 7.1 extraction_patch

```yaml
---
type: extraction_patch
ingest_id: "ING-20260505-0001"
target_page: "WIKI/Entities/Organizations/微众银行.md"
operation: update              # create | update | merge | flag
confidence: high               # high | medium | low
source_ref: "RAW/transcripts/2023/20230308_xxx.md"

candidate_fields:              # 待写入的字段值
  cooperation_status: "exploring"
  last_interact_date: "2023-03-08"

diff_summary:
  added: [cooperation_status]
  changed: [last_interact_date]
  conflicts: []

review_required: false
status: pending                # pending | approved | rejected
---
```

### 7.2 candidate_entity

```yaml
---
type: candidate_entity
ingest_id: "ING-20260505-0001"
entity_type: person            # person | organization
raw_name: "黄国华"
matched_entity_id: "person_huangguohua_0001"   # null 表示新实体
match_confidence: high         # high | medium | low
canonical_name: "黄国华"
suggested_aliases: ["慧穗黄总"]

# 低置信度时填充
disambiguation_candidates:
  - entity_id: "person_huangguohua_0002"
    match_score: 0.72
    reason: "名字相同但场景上下文差异大"

action: create | update | merge | reject
review_required: false
---
```

### 7.3 entity_registry

```yaml
entities:
  - entity_id: "org_weibank_0001"
    canonical_name: "微众银行"
    aliases: ["微众", "微众行", "微重银行"]
    entity_type: organization
    wiki_path: "WIKI/Entities/Organizations/微众银行.md"
    source_count: 7
    status_stage: reviewed
    first_seen: "2023-03-08"
    last_seen: "2024-10-16"
```

---

## 八、规则约束

### 8.1 必填字段规则
- Meeting: subtype, publishability, reusable_for, ldamc, source_ref — **5字段缺一不入库**
- Person: entity_id, thinking_framework, values_beliefs, decision_style, emotional_tone — **5隐性知识字段缺一不标记compiled**
- Judgment: topic_key, evidence_chain, confidence_rationale — **3字段缺一不入库**

### 8.2 纯度规则
- 外部参考（external_ref）的 `can_update_internal` 必须为 `false`
- 外部知识不能直接写入内部 Person/Org/Judgment 主页
- 必须经过 Synthesis 或 Review 页面过渡

### 8.3 消歧规则
- 同一 canonical_name 只能有一个 entity_id
- aliases 不能与任何其他实体的 canonical_name 重复
- status_stage 为 canonical 的实体视为"金标准"

### 8.4 版本规则
- 每次 Update 操作 `version` 递增
- `previous_version` 记录被替换的旧版本路径
- 旧版本不删除，追加到 `_log.md`
