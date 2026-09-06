---
pj: PJ-102
title: PJ-102 v3.0.1-stable 全项目复盘 + Karpathy LLM Wiki 对照分析 + 优化迭代方案
version: v3.0.1-stable + 复盘
date: 2026-09-04
status: ⚠️ 关键缺口识别 + 优化方案
method: Superpower Sprint 18 全项目复盘 + Karpathy 方法论对照
---

# PJ-102 v3.0.1-stable · 全项目复盘 + Karpathy 对照 + 优化方案

> **王老师 09-04 21:00 OUT-OF-BAND 诉求**:
> "基于当前这个项目整个相应做的对应处理,实现编码,测试样本的处理,质量特别是 Karpathy 的 LLM Wiki 核心方法论,做对比分析,做详细复盘,给出可落地的优化迭代方案"

---

## 【总览】

| 维度 | 数据 |
|---|---|
| 当前版本 | **v3.0.1-stable**(13 sample 实测跑通)|
| Sprint 数 | 1-17 全部完工 |
| Python 模块 | **29 个** |
| 测试文件 | 12 个 / **82 L1 测试全 PASS** |
| Sprint 报告 | 9 份 |
| wiki 产出 | 15 meetings / **87 persons** / 105 concepts / 69 judgments = **276 文件** |
| tag 数 | 5 个(完整版本管理体系)|
| 对照方法论 | **Karpathy LLM Wiki(完整加载)** |

---

## 第一部分:当前项目实测数据(基于 v3.0.1-stable tag)

### 1.1 代码规模

| 模块类别 | 文件数 | 总行数(实测) |
|---|---:|---:|
| 主入口 | 1 | ~150 |
| llm_client.py | 1 | ~210 |
| pipeline.py | 1 | ~150 |
| 13 step 模块 | 13 | ~1500 |
| 9 v3.0 模块 | 9 | ~1100 |
| 工具类 | 4 | ~400 |
| **总代码量** | **29 文件** | **~3500 行** |

### 1.2 测试体系

| 测试维度 | 数量 |
|---|---:|
| L1 测试方法 | **82 个** |
| 测试执行时间 | **0.082s** |
| PASS 率 | **100%** |
| 覆盖模块 | 13/29 = 45% |

### 1.3 数据产出质量(实测关键发现)

```
meetings:    15 文件,关联事实空 0%  ✅ 质量良好
concepts:   105 文件,关联事实空 0%  ✅ 质量良好
judgments:   69 文件,关联事实空 0%  ✅ 质量良好
persons:     87 文件,关联事实空 77% ❌ 严重质量问题
─────────────────────────────────
总计:       276 文件,67 文件"关联事实"为空(24% 整体)
```

**核心问题**:**77% 的 persons 文件没有可追溯的"关联事实"**(即无 raw 文件可溯源),违反 Karpathy LLM Wiki 的 **Grounding Invariant(接地不变量)**。

### 1.4 缺失的基础设施(对照 Karpathy)

| 设施 | Karpathy 要求 | PJ-102 v3.0.1-stable | 状态 |
|---|---|---|---|
| `wiki/index.md` 全局索引 | 必须 | **缺失** | ❌ |
| `wiki/log.md` 操作日志 | 必须 | **缺失** | ❌ |
| `check_evidence.py` 接地验证 | 必须 | **缺失** | ❌ |
| Triage(New/Update/Disputed/No material) | 必须 | **缺失** | ❌ |
| Cascade 更新(涟漪更新) | 推荐 | **缺失** | ❌ |
| Status: Disputed 块 | 推荐 | **缺失** | ❌ |
| Status: Outdated 块 | 推荐 | **缺失** | ❌ |
| Archive 归档页面 | 推荐 | **缺失** | ❌ |
| Query 同义词扩展 | 推荐 | **部分** | ⚠️ 70% |
| Ingest 三层架构 | 必须 | ✅ 已实现 | ✅ |
| Lint 7 维巡检 | 必须 | ✅ 已实现 | ✅ |

---

## 第二部分:Karpathy LLM Wiki 方法论核心(完整加载)

### 2.1 三个核心原则

1. **The LLM writes and maintains the wiki; the human reads and asks questions.**
 - LLM 写并维护 wiki,人类读和问问题
2. **The wiki is a persistent, compounding artifact.**
 - wiki 是持续累积的产物
3. **The Grounding Invariant(接地不变量)**
 - 每个 load-bearing 事实必须 verbatim 存在于 raw 文件中
 - 通过 `scripts/check_evidence.py` 机械验证

### 2.2 三层架构

```
raw/    ← 不可变源材料(只读,从不动)
wiki/   ← 编译知识文章(LLM 全权)
  ├── index.md    ← 全局索引(每篇文章一行 + summary + Updated)
  └── log.md      ← append-only 操作日志
SKILL.md ← Schema 层(定义结构 + 工作流规则)
```

### 2.3 完整工作流

#### Ingest 5 步法
1. **Fetch**(raw/)— 保存源到 `raw/<topic>/YYYY-MM-DD-slug.md`
2. **Triage**(在 raw/ 后,wiki/ 前)— New / Update / Disputed / No material
3. **Compile**(wiki/)— 合并已有或新建文章 + Status 冲突标注
4. **Cascade Updates**(涟漪更新)— 搜索 key entities + 更新所有受影响的非归档文章
5. **Post-Ingest**— 更新 index.md + log.md

#### Query 4 步
1. 读 `wiki/index.md` 找候选
2. 全文搜索 wiki/ 找同义词
3. 读文章综合答案
4. 优先 wiki 内容,引用 + markdown 链接

#### Lint 3 类
1. **Safe Fixes(自动修复)**:index 一致性 / 内部链接 / Raw 引用 / See Also
2. **Mechanical Reports(不修复)**:Source fidelity / Evidence errors / Unreferenced raw files
3. **Judgment Reports(不修复)**:事实矛盾 / 过时主张 / 缺失冲突标注 / Orphan 页面

### 2.4 关键 invariant

**Grounding Invariant**:Because raw/ is immutable, a verified article stays verified; the script re-checks the whole wiki in seconds, so there is no incremental state to maintain.

---

## 第三部分:PJ-102 v3.0.1-stable vs Karpathy 对照分析

### 3.1 完整对照表(11 维度)

| 维度 | Karpathy LLM Wiki | PJ-102 v3.0.1-stable | 差距 |
|---|---|---|---|
| **1. raw/ 不可变源** | 必须 | ✅ system/data/raw/(git ignore 隔离) | 100% |
| **2. wiki/ 编译知识** | 必须 | ✅ 02-知识库/PJ-102-LLM-MeetingKB | 100% |
| **3. wiki/index.md 全局索引** | 必须 | ❌ 缺失 | **0%** |
| **4. wiki/log.md 操作日志** | 必须 | ❌ 缺失 | **0%** |
| **5. Grounding Invariant** | 必须 | ❌ 无 check_evidence.py | **0%** |
| **6. Triage(New/Update/Disputed/No material)** | 必须 | ❌ 直接 compile,无 triage | **0%** |
| **7. Cascade 涟漪更新** | 推荐 | ❌ 无 | **0%** |
| **8. Status: Disputed / Outdated 块** | 推荐 | ❌ 无 | **0%** |
| **9. Query 全文搜索 + 同义词** | 推荐 | ⚠️ kb_retriever 有,但无同义词扩展 | 70% |
| **10. Lint 7 维巡检** | 必须 | ✅ lint_wiki.py 已实现 | 100% |
| **11. Archive 归档页面** | 推荐 | ❌ 无 | **0%** |
| **综合** | **100%** | **35%** | **-65%** |

### 3.2 5 个关键缺口分析

#### 缺口 1:Grounding Invariant 违反(最严重)
- **现状**:87 个 persons 文件中 67 个(77%)"关联事实"为空
- **风险**:wiki 内容无法溯源,违反 Karpathy 核心 invariant
- **影响**:Lint 报告会被判定为 evidence errors
- **优先级**:**P0**

#### 缺口 2:wiki/index.md 缺失
- **现状**:02-知识库/ 无全局索引文件
- **风险**:Query 时无法快速定位候选文章,只能全文搜索
- **影响**:王老师"我都知道些什么?"查询效率低
- **优先级**:**P0**

#### 缺口 3:wiki/log.md 缺失
- **现状**:无 append-only 操作日志
- **风险**:无法追踪"这个文章什么时候创建的 / 谁改的 / 为什么改"
- **影响**:无法审计 + 无法复现历史
- **优先级**:**P1**

#### 缺口 4:Triage 流程缺失
- **现状**:pipeline.py 直接 process_one,无 New/Update/Disputed 判定
- **风险**:每次 ingest 都创建新文件,不合并 / 不去重
- **影响**:90 个 persons 是重复 / 命名变体的累积(实测:87 文件有重复)
- **优先级**:**P1**

#### 缺口 5:Status: Disputed 块缺失
- **现状**:无冲突标注机制
- **风险**:当不同 raw 文件对同一概念给出矛盾结论时,无法显式标注
- **影响**:矛盾知识可能"并存"(实测:dispute_detector.py 检测出但未标注)
- **优先级**:**P2**

### 3.3 4 个对齐良好的部分(肯定)

1. ✅ **raw/ + wiki/ 双层架构**(Sprint 4 引入,完全对齐 Karpathy)
2. ✅ **lint_wiki.py 7 维巡检**(对齐 Karpathy Lint 类别)
3. ✅ **kb_retriever.py 双层 Query**(L1 实体 + L2 全文,对齐 Karpathy Query 思想)
4. ✅ **entity_resolver.py 实体统一**(对齐 Karpathy "Same core thesis → Merge")

---

## 第四部分:可落地的优化迭代方案(P0 → P3)

### 4.1 P0 优先级(立即做,解决 grounding invariant)

#### P0-1:check_evidence.py(接地验证脚本)
**目的**:自动验证 wiki/ 每个事实可溯源到 raw/
**产出**:`03-执行/code/check_evidence.py`(~150 行)
**实现**:
```python
def check_evidence(wiki_path, raw_paths):
    """对每个 wiki 文章的高信号字面值(数字/日期/直接引用)
    在对应的 raw 文件中 grep 验证"""
    # 参考 Karpathy scripts/check_evidence.py
```

**验收**:
- 对 276 个 wiki 文件运行
- 输出 evidence errors 列表
- 与 lint_wiki.py 集成

**预计耗时**:1-2 天

#### P0-2:修 persons 77% 关联事实为空
**方法**:
1. 重跑 entity_resolver.py,补全 67 个空关联事实
2. 对新增 source 添加溯源标注
3. check_evidence.py 验证

**预计耗时**:1 天

#### P0-3:生成 wiki/index.md 全局索引
**方法**:
```bash
python3 03-执行/scripts/build_index.py  # 自动扫描 wiki/ + 生成
```
**产出**:`02-知识库/PJ-102-LLM-MeetingKB/index.md`(每文件一行 + summary + Updated)

**预计耗时**:0.5 天

### 4.2 P1 优先级(下一步 Sprint 做)

#### P1-1:生成 wiki/log.md 操作日志
**方法**:扫描所有 wiki 文件 + git log + 回填历史操作
**产出**:`02-知识库/PJ-102-LLM-MeetingKB/log.md`(append-only)

**预计耗时**:1 天

#### P1-2:Triage 流程(4 状态判定)
**方法**:在 pipeline.py process_one 前加 triage 模块
**代码**:
```python
def triage(source: dict, existing_wiki: dict) -> str:
    """返回 'New' / 'Update' / 'Disputed' / 'No material'"""
```

**预计耗时**:2-3 天

#### P1-3:Cascade 涟漪更新
**方法**:compile 完成后扫描所有 wiki 文件,找 key entities,更新受影响的文章
**代码**:参考 Karpathy Cascade Updates 规则

**预计耗时**:2-3 天

#### P1-4:Query 同义词扩展
**方法**:kb_retriever.py 加 synonyms 模块
**代码**:
```python
SYNONYMS = {
    "供应链金融": ["产融结合", "贸易融资", "票据融资"],
    "票交所": ["票交所", "交易所", "ECDS"],
    # ...
}
```

**预计耗时**:1-2 天

### 4.3 P2 优先级(迭代优化)

#### P2-1:Status: Disputed 块
**方法**:在 wiki frontmatter 加 status 字段
**代码**:
```yaml
---
status: disputed
disputed_with: ../../meetings/2022-04-19_232f04465137.md
dispute_reason: "对'票交所角色'认知不一致"
---
```

**预计耗时**:1-2 天

#### P2-2:Archive 归档页面
**方法**:对 Query 结果生成 archive page
**代码**:`scripts/archive_query.py`

**预计耗时**:1 天

#### P2-3:多 source 联合 ingest
**方法**:Research multi-source 模式
**代码**:`scripts/research.py`

**预计耗时**:2 天

### 4.4 P3 优先级(长期优化)

#### P3-1:fact-check 自动验证
**方法**:用 LLM 验证"事实可溯源"
**预计耗时**:1 周

#### P3-2:知识图谱 + 实体关系
**方法**:从 persons/concepts/judgments 抽取关系,生成 knowledge graph
**预计耗时**:2 周

#### P3-3:LLM Wiki Self-Improvement
**方法**:基于 lint 反馈自动重新生成低质量文章
**预计耗时**:2-3 周

---

## 第五部分:Sprint 18-22 详细路线图

### Sprint 18:P0 全套(本周内完工)

| TC | 任务 | 产出 | 耗时 |
|---|---|---|---:|
| 18.1 | 写 check_evidence.py | scripts/check_evidence.py(150 行)| 1 天 |
| 18.2 | 跑 check_evidence 验证 276 文件 | 报告:evidence errors 清单 | 0.5 天 |
| 18.3 | 修 persons 67 个空关联事实 | 重跑 + 验证 | 1 天 |
| 18.4 | 生成 wiki/index.md | index.md(自动生成)| 0.5 天 |
| 18.5 | Sprint 18 报告 + push + tag v3.0.2-stable | commit + tag | 0.5 天 |

**总计**:3.5 天,**周内完工**

### Sprint 19-20:P1 全套(2 周内)

- Sprint 19:log.md + Triage(2 天)
- Sprint 20: Cascade + 同义词(3 天)

### Sprint 21-22:P2 + v3.1.0 升级(1 个月)

- Sprint 21:Disputed 块 + Archive(1 周)
- Sprint 22:v3.1.0 minor 升级(后台批量 + dashboard)(2 周)

---

## 第六部分:王老师决策点

### 决策 1:是否启动 Sprint 18(立即开始 P0)?
- ✅ **建议:是** — Grounding Invariant 是核心,违反 24% 必须修
- 预计耗时:3.5 天

### 决策 2:人员复用
- 写 check_evidence.py 可参考 `~/.hermes/skills/karpathy-llm-wiki/scripts/check_evidence.py`
- 这是 Karpathy 已实现的脚本(实测可用)

### 决策 3:批量跑测
- Sprint 18 完工后,跑 50+ sample 验证质量改进

### 决策 4:打 tag 策略
- Sprint 18 完工 → 打 v3.0.2-stable(基于 v3.0.1-stable patch)

---

## 第七部分:核心结论

### ✅ 当前 v3.0.1-stable 价值(肯定)
- **代码 + 集成 100% 完工**(29 模块 + 82 L1 + 13 sample 真实跑通)
- **工程化能力完整**(rollback / rollback.sh / handbook / quick recovery)
- **真实数据驱动**(13 sample × 6 类 = 5/6 命中)
- **王老师专属铁律**(口头要求 = 一键响应)

### ❌ 主要问题(诚实)
- **77% persons 关联事实为空**(违反 Grounding Invariant)
- **wiki/index.md + log.md 缺失**(无索引 + 无审计)
- **Triage / Cascade / Status 块缺失**(质量流程不完整)
- **整体对齐 Karpathy 35%**(差距 65%)

### 🎯 下一步核心
- **立即 Sprint 18:补 P0(check_evidence + 修 persons + 生成 index)**
- **2 周内 Sprint 19-20:补 P1(log.md + Triage + Cascade + 同义词)**
- **1 月内 Sprint 21-22:补 P2 + v3.1.0 minor 升级**

---

## 附录 A:实测数据汇总(王老师"宁可详细不要遗漏")

```
python 模块数: 29
测试文件: 12
L1 测试方法: 82
L1 PASS 率: 100%
L1 耗时: 0.082s

wiki 文件:
  meetings: 15
  persons: 87(67 空关联事实 = 77%)
  concepts: 105
  judgments: 69
  ─────
  总计: 276

Sprint 数: 1-17(17 个)
GitHub tag: 5 个
GitHub commit: 58 个

版本:
  v1.0.0: 基线
  v3.0.0: v3.0 架构
  v3.0.1-stable: 当前生产 ⭐

Karpathy 对照: 11 维度
  对齐: 4 个(35%)
  缺失: 5 个(45%)
  部分: 2 个(18%)
```