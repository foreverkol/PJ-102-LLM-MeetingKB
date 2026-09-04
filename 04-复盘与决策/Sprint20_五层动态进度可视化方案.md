# PJ-102 · 工程计划动态执行体验优化方案

> **王老师 09-04 21:40 OUT-OF-BAND 诉求**:
> "工程计划动态执行过程中,清晰全过程+处理完了哪些+还有哪些步骤,类似好的体验展示,更好的体验反馈反馈,全项目固化模式推广"

---

## 【总览 — 5 层动态可视化体验】

| 层 | 模块 | 目的 | 实测状态 |
|---|---|---|:---:|
| L1 | **Todo 工具增强** | 当前会话步骤追踪 | ✅ 已用 |
| L2 | **EXECUTION_DASHBOARD.md** | 项目级实时进度看板 | 🆕 **待建** |
| L3 | **progress.sh CLI** | 5 秒生成进度报告 | 🆕 **待建** |
| L4 | **CHANGELOG.md 实时更新** | 时间线变更追踪 | ✅ 已有,需自动化 |
| L5 | **飞书汇报模板** | 跨平台汇报(王老师视角)| 🆕 **待建** |

---

## 【第一层 — Todo 工具增强(会话级)】

### 1.1 当前用法(实测)
```python
todo({todos: [...]})        # 一次创建
todo({todos: [...], merge: true})  # 增量更新
```

### 1.2 优化方案
- **添加结构化分组**:按 Sprint / W1-W4 分组
- **添加可视化 emoji**:⏳ 进行中 / ✅ 完成 / ❌ 取消 / ⏸️ 暂停
- **添加预估耗时**:每个 todo 可标注预期时间

### 1.3 实施成本
- 0 工作量(纯用法改进)
- 立即生效

---

## 【第二层 — EXECUTION_DASHBOARD.md(项目级)】

### 2.1 设计目标
**单一文件,实时反映**:
- 总计划步骤数(完成 / 总数)
- 当前阶段(Sprint N)
- 后续步骤清单
- 已完成 / 待办 时间线
- 各 Sprint 进度条

### 2.2 文件结构(实测设计)
```markdown
# PJ-102 · 执行看板

> 实时更新:每次 Sprint 完工自动刷新
> 当前版本:v3.0.3-stable
> 当前阶段:Sprint 20

## 总体进度

[████████████████████░░░░░] 78% (45/58 步骤)

## 当前阶段

### Sprint 20 — 进行中
⏳ [P2-1] Status: Disputed 块(预计 1 天)
⏳ [P2-2] Archive 归档页面(预计 1 天)
⏸️ [P2-3] Research multi-source(待启动)

## 已完成 Sprint

### Sprint 19 — ✅ 完成(2026-09-04 22:30)
- ✅ P1-1: wiki/log.md(151 行)
- ✅ P1-2: Triage 4 状态(173 行)
- ✅ P1-4: 同义词扩展(12 词典)

### Sprint 18 — ✅ 完成(2026-09-04 21:30)
- ✅ P0-1: check_evidence.py
- ✅ P0-2: Grounding Invariant 验证
- ✅ P0-3: wiki/index.md
- ✅ v3.0.2-stable tag

## 待办 Sprint

### Sprint 21 — 待启动
- P3-1: fact-check 自动验证
- P3-2: Knowledge Graph
- P3-3: Self-Improvement
```

### 2.3 自动生成脚本
**新增**:`03-执行/scripts/build_dashboard.py`

**数据源**:
1. `04-复盘与决策/Sprint*.md` 列表(已完成步骤)
2. `04-复盘与决策/Sprint19_*.md` 解析(本次进度)
3. `STATE.md` 当前阶段
4. `VERSION` 当前版本
5. `git log --oneline | wc -l` 总 commit 数

**输出**:`EXECUTION_DASHBOARD.md`(实时看板,自动生成)

---

## 【第三层 — progress.sh CLI(命令行)】

### 3.1 一键查看当前进度(王老师最常用)
```bash
bash 03-执行/scripts/progress.sh
```

### 3.2 输出示例
```
═══════════════════════════════════════════════════════
  PJ-102-LLM-MeetingKB · 执行进度(实时)
═══════════════════════════════════════════════════════

✅ v3.0.3-stable  当前生产版本
📊 当前阶段:Sprint 19 已完工
🎯 总体进度:78%(45/58 步骤)

📦 已完成 Sprint:
  ✅ Sprint  1-7  基础架构(7)
  ✅ Sprint  8   v3.0 真实跑通(1)
  ✅ Sprint  9   Wiki 真实化(1)
  ✅ Sprint 10   max_tokens 524288(1)
  ✅ Sprint 11   max_tokens 524288 + 5 sample(1)
  ✅ Sprint 12   5 sample 全部跑通(1)
  ✅ Sprint 13   10 sample(1)
  ✅ Sprint 14   13 sample(1)
  ✅ Sprint 15   v3.0.1-stable tag(1)
  ✅ Sprint 16   GitHub 操作手册(1)
  ✅ Sprint 17   版本登记表(1)
  ✅ Sprint 18   v3.0.2-stable tag + Grounding(1)
  ✅ Sprint 19   v3.0.3-stable tag + log.md + Triage(1)

⏳ 当前 Sprint 20 — P2 全套(进行中)
  ✅ P2-1  Status: Disputed 块
  ⏳ P2-2  Archive 归档页面
  ⏸️ P2-3  Research multi-source

📋 待办 Sprint:
  ⏸️ Sprint 21  P3(长期)
  ⏸️ Sprint 22  v3.1.0 minor(1 月)

📈 Karpathy 对齐率:
  v3.0.0:        35%
  v3.0.1-stable: 35%
  v3.0.2-stable: 53% (+18%)
  v3.0.3-stable: 75% (+22%) ⭐ 当前

📁 GitHub 状态:
  Commits: 64
  Tags: 7(v1.0-baseline / v1.0.0 / v1.1.0 / v3.0.0 / 
        v3.0.1-stable / v3.0.2-stable / v3.0.3-stable)
  L1 测试:82/82 PASS

═══════════════════════════════════════════════════════
  ✅ 项目就绪,可投产
═══════════════════════════════════════════════════════
```

### 3.3 实施成本
- 1 个新脚本(`progress.sh` / 50 行)
- 引用 `EXECUTION_DASHBOARD.md` 数据
- 1 次 Sprint 20 完工

---

## 【第四层 — CHANGELOG.md 实时更新】

### 4.1 当前现状
- `CHANGELOG.md` 存在但**手工维护**
- 每次 Sprint 完工,**人工追加**

### 4.2 自动化方案
**新增**:`03-执行/scripts/build_changelog.py`

**数据源**:`git log --oneline` 每个 commit 自动转 CHANGELOG 一行

**格式**:
```markdown
# PJ-102-LLM-MeetingKB · 变更日志

## [v3.0.3-stable] - 2026-09-04
- feat: wiki/log.md 自动生成(151 行)
- feat: Triage 4 状态判定模块
- feat: kb_retriever 同义词扩展(12 词典)

## [v3.0.2-stable] - 2026-09-04
- feat: check_evidence.py(Karpathy 复用)
- feat: wiki/index.md 全局索引
- release: v3.0.2-stable
...
```

### 4.3 实施成本
- 1 个新脚本(`build_changelog.py` / 50 行)
- 每次 commit 之后自动跑

---

## 【第五层 — 飞书汇报模板(王老师视角)】

### 5.1 当前汇报格式
- 每次 Sprint 完工都写"飞书终验"
- 格式固定:总览 / 详细 / GitHub / 决策点

### 5.2 模板固化
**新增**:`04-复盘与决策/templates/sprint_report_template.md`

**复用模板**:
- 王老师每次 Sprint 都看到相同的格式
- 飞书用户(王老师专属频道)能快速理解

---

## 【全项目固化模式推广】

### 6.1 不改变项目执行内容
- **保留所有现有 Sprint 流程**
- **新增的 5 层都是"观察"层 + "汇报"层**
- 项目代码 / 测试 / 设计 / 需求 = 完全不动

### 6.2 复用模式
**模式名**:`five-layer-progress-dashboard`

**适用项目**:
- ✅ PJ-102(本次实施)
- ✅ 任何 Superpower 模式项目
- ✅ 任何多 Sprint 复杂项目

**实施清单**(复制即可):
1. `03-执行/scripts/build_dashboard.py`(自动生成 EXECUTION_DASHBOARD.md)
2. `03-执行/scripts/progress.sh`(命令行实时查看)
3. `03-执行/scripts/build_changelog.py`(自动 CHANGELOG)
4. `04-复盘与决策/templates/sprint_report_template.md`(汇报模板)
5. `EXECUTION_DASHBOARD.md`(放在项目根,自动生成)

### 6.3 触发时机(可固化到 Superpower writing-skills)

每个 Sprint 完工后,Agent 自动:
```bash
# Sprint N 完工 5 步法
1. git add + commit
2. git push
3. bash scripts/build_dashboard.py   # 自动刷新
4. bash scripts/build_changelog.py   # 自动追加 CHANGELOG
5. bash scripts/progress.sh | tee /tmp/progress.log  # 王老师汇报
```

---

## 【实施计划】

### Sprint 20 立即落地(0.5 天)
- ✅ `build_dashboard.py`(80 行)
- ✅ `progress.sh`(50 行)
- ✅ `build_changelog.py`(60 行)
- ✅ `sprint_report_template.md`(40 行模板)

### Sprint 21 固化到 Superpower
- 把 5 层模式沉淀为 skill
- `~/.hermes/skills/five-layer-progress-dashboard/SKILL.md`

### Sprint 22 跨项目复用
- 把 5 个工具复制到 PJ-001 / PJ-005 / PJ-201 等

---

## 【决策点 — 王老师】

```
□ Sprint 20 立即启动(0.5 天落地 5 层)
  → 王老师每次 Sprint 完工后自动看到清晰进度
  → 全项目固化模式

□ 暂停,等王老师进一步指令
```

---

## 【关键洞察】

王老师,本次方案的关键洞察:
- **不改变执行内容**(代码 / 测试 / 设计 / Sprint 流程)
- **只增加"观察"层 + **汇报"层**(透明化)
- **复用于所有 Superpower 模式项目**(模式可推广)

这种"加层不改变"的设计,在 Hermes 已有 Skill 体系内**最安全**,因为:
- 不破坏现有 sprint 执行
- 不需要重新培训
- 王老师可见即可管

**等王老师一句话决定 Sprint 20 启动**。