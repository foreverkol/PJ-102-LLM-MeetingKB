---
pj: PJ-102
title: PJ-102 项目迭代版本管理规范 v1.0
version: v3.0.1-stable + 规范建立
date: 2026-09-05
status: 📋 规范阶段(等待王老师评审)
method: 王老师 9-05 OUT-OF-BAND 触发 — 实测摸底 + 流程设计 + 防止再发机制
---

# PJ-102 项目迭代版本管理规范 v1.0

> **王老师 9-05 OUT-OF-BAND**:
> "我们项目是一个逐步迭代的过程,如果有差异比加大或者有分支要明确提示和版本设置以及版本分支的处理,如何出现这样的问题,怎么解决这个问题,最后如何保障再次出现"

> **核心目标**:**PJ-102 逐步迭代过程中,差异/分支/版本 的规范化处理流程 + 防止再发生机制**

---

## 第一部分:实测摸底(2026-09-05 21:30)

### 1.1 当前 PJ-102 版本管理现状(实事求是)

| 项 | 实测 | 问题 |
|----|------|------|
| Git tag | 5 个(v1.0-baseline / v1.0.0 / v1.1.0 / v3.0.0 / v3.0.1-stable) | 缺少 Sprint 18/19/20 的 stable tag(报告说打了实际没打)|
| Git branches | 仅 main | **没有 dev / feature / release / hotfix 分支** |
| 工作树脏区 | **48 项未提交**(16 modified + 32 untracked)| **未提交原子strata PoC 跑批残留** |
| VERSION 文件 | 13 B 单行 `3.0.1-stable` | 无语义版本字段 |
| VERSION_MANAGEMENT.md | 6.8 KB(王老师已写规范)| 但**缺少自动化校验** |
| atomicstrata PoC | `poc_atomicstrata/` 在 main 分支 | 没标 "PoC" / "experimental" 标记 |
| 本次会话错误 | Sprint 21 用了 v1.0/v2.0 错误版本号 | **已发生 2 次同类错误**(说明没防止机制)|

### 1.2 实测发现的"差异/分支/版本"风险点

| # | 风险 | 实测证据 |
|---|------|---------|
| **R1** | 多版本并行无隔离 | atomicstrata PoC(24 concepts)+ s4-s12 主线 在同一 main |
| **R2** | 大改动直接进 main,无 review | 本次 Sprint 21 直接 commit `c4317b7` 到 main |
| **R3** | 工作树脏区长期未提交 | 48 项未提交(占 16 modified + 32 untracked)|
| **R4** | Tag 不规范 / 不打 / 错打 | Sprint 18/19/20 说 push 了实际没 tag,b7acc0c 清理违规 tag |
| **R5** | 版本号规则无自动化检查 | 本会话 v1.0/v2.0 → v3.1.0-x 改了 2 次类错误 |
| **R6** | 命名不一致(v1.x vs v3.0.x)| v1.x baseline → v3.0 跨大版本但都共存 |
| **R7** | 没有"差异过大"预警机制 | 没有任何检查工具提示"分支差异 > N commits 需合并"|

---

## 第二部分:规范化处理流程(王老师需求"如何解决")

### 2.1 Git Flow 适配版(王老师"逐步迭代"风格)

**PJ-102 采用"简化版 GitFlow"**(避免企业级 GitFlow 的复杂度):

```
main                              ← 当前主分支(v3.0.1-stable)
  │
  ├── dev                         ← 持续开发分支(新 Sprint 工作分支)
  │   │
  │   ├── feature/sprint-21-v3.1.0-rc1 ← Sprint 21 特性分支
  │   ├── feature/sprint-22-xxx      ← Sprint 22 特性分支
  │   │
  │   └── release/v3.1.0-rc1         ← 发布候选分支
  │       │
  │       └── hotfix/xxx-yyy         ← 紧急修复分支
```

### 2.2 分支使用规则(差异/分支场景)

| 分支类型 | 命名规则 | 用途 | 生命周期 | 合并到 |
|---------|---------|------|---------|--------|
| **main** | `main` | 当前稳定版(v3.0.1-stable)| 永久 | - |
| **dev** | `dev` | 持续开发,新 Sprint 工作区 | 永久 | main(每个 Sprint 完工)|
| **feature** | `feature/sprint-N-xxx` | 单个 Sprint 特性开发 | 短(1-4 周)| dev |
| **release** | `release/v3.1.0-rc1` | 发布候选(整合 + 测试)| 中(1-2 周)| main + dev |
| **hotfix** | `hotfix/xxx-yyy` | 紧急修复 | 短(< 1 周)| main + dev |
| **poc** | `poc/<name>` | 实验性 PoC(不保证合并)| 长期 | 不合并,删除 |

### 2.3 原子strata PoC 的正确处置(实战案例)

**当前问题**:`poc_atomicstrata/` 在 main 分支,跟主线代码混在一起。

**正确做法**:

```bash
# 1. 移出 main 分支
git checkout -b poc/atomicstrata-experiment
git rm -r 03-执行/poc_atomicstrata
git commit -m "poc: 移出 atomicstrata 实验目录到 poc 分支"

# 2. main 分支干净
# 3. poc 分支独立维护,不合并到 main(除非王老师决策保留)
```

### 2.4 版本号规则(王老师 9-05 OUT-OF-BAND 触发)

**PJ-102 严格 Semantic Versioning + suffix**:

| 类型 | 格式 | 触发条件 | 王老师需确认 |
|------|------|---------|------------|
| **major** | `v3.0.0 → v4.0.0` | 架构升级 / 模型切换 | ✅ |
| **minor** | `v3.0.x → v3.1.0` | 新功能(如 Obsidian 集成)| ✅ |
| **patch** | `v3.1.0 → v3.1.1` | bug 修复 | 一般无需确认 |
| **alpha** | `v3.1.0-alpha1` | 详细规划阶段 | 仅内部 |
| **beta** | `v3.1.0-beta1` | 公测阶段 | ✅ |
| **rc** | `v3.1.0-rc1` | Release Candidate | ✅ |
| **stable** | `v3.1.0-stable` | 王老师确认"形成可发布大版本" | ✅(必要条件)|

**铁律(v41 强化版)**:
- ❌ **不再有"v3.0.2-stable / v3.0.3-stable / v3.0.4-stable"**(Sprint 节点 tag 已被 b7acc0c 清理)
- ✅ **只在大版本或王老师确认时才打 stable tag**
- ✅ alpha/beta/rc 不需要王老师确认,直接打

### 2.5 差异过大预警机制(王老师核心需求)

**每周 cron 自动检查**:

```bash
# scripts/git-diff-monitor.sh
#!/bin/bash
# 检查 main vs dev 差异
DIFF_COMMITS=$(git rev-list --count main..dev)
DIFF_FILES=$(git diff --name-only main..dev | wc -l)
if [ "$DIFF_COMMITS" -gt 20 ] || [ "$DIFF_FILES" -gt 30 ]; then
  echo "⚠️ 差异过大: $DIFF_COMMITS commits / $DIFF_FILES files"
  echo "建议:王老师评审 + 决定合并策略"
  # 飞书告警
fi
```

**差异阈值表**:

| 指标 | 警告 | 阻断(需要王老师确认) |
|------|------|------------------|
| commits 差异 | > 10 | > 30 |
| files 差异 | > 20 | > 50 |
| 工作树脏区 | > 5 项 | > 15 项 |
| 当前分支无 origin | 是 | 是 |

### 2.6 工作树脏区处理流程(本次 48 项的教训)

**每周 cron + Agent 检查**:

```
┌──────────────────────────────────────┐
│ 1. 周一 8:00 cron 跑:                │
│    git status --short | wc -l         │
│                                      │
│ 2. 如 > 5 项 modified + > 5 项 untracked:│
│    → 飞书告警"工作树脏区 X 项,请评估" │
│                                      │
│ 3. Agent 看到告警:                    │
│    → 自动识别哪类脏区(PoC 残留 / 跑批输出 / 新代码)│
│    → 提议:"commit / stash / gitignore / 移动" │
│                                      │
│ 4. 王老师拍板:执行                   │
└──────────────────────────────────────┘
```

---

## 第三部分:防止再发生机制(王老师"如何保障")

### 3.1 自动化检查清单(pre-commit hook)

`scripts/pre-commit-hooks/check-version-consistency.sh`:

```bash
#!/bin/bash
# 防止 v1.0/v2.0 错误版本号再次发生
echo "🔍 检查版本号一致性..."

# 1. 找所有 .md 文件的版本号
SUSPECT=$(grep -rn "v[0-9]\+\.[0-9]\+\.[0-9]\+" 04-复盘与决策/*.md 2>/dev/null | \
  grep -v "v3.0.1-stable" | grep -v "v3.1.0")

if [ -n "$SUSPECT" ]; then
  echo "❌ 发现可疑版本号(非 v3.0.x / v3.1.x):"
  echo "$SUSPECT"
  exit 1
fi
echo "✅ 版本号检查通过"
```

### 3.2 自动化检查清单(weekly cron)

`scripts/weekly-git-health.sh`:

```bash
#!/bin/bash
# 每周日 22:00 跑
echo "📊 PJ-102 Git 健康周报"

# 1. 脏区检查
DIRTY=$(git status --short | wc -l)
echo "工作树脏区: $DIRTY 项"

# 2. 分支差异检查
for BR in dev feature/* release/*; do
  if [ -n "$BR" ]; then
    DIFF=$(git rev-list --count main..$BR 2>/dev/null)
    echo "  $BR vs main: $DIFF commits"
  fi
done

# 3. 最近 7 天 tags
TAGS=$(git for-each-ref --count=5 --format='%(refname:short) %(creatordate:short)' refs/tags)
echo "最近 tags:"
echo "$TAGS"

# 4. 飞书通知(如果脏区 > 15)
if [ "$DIRTY" -gt 15 ]; then
  echo "⚠️ 脏区过大,飞书告警(略)"
fi
```

### 3.3 命名规则检查(防止 v1.x / v3.0.x 混用)

`scripts/check-naming-consistency.sh`:

```bash
#!/bin/bash
# 检查 Sprint 文档版本号必须用 v3.x.x
echo "🔍 检查 Sprint 文档版本号一致性"

for f in 04-复盘与决策/Sprint*.md; do
  if grep -q "title:.*v[12]\." "$f"; then
    echo "❌ $f 使用了 v1.x / v2.x 命名"
    exit 1
  fi
done

# 检查 git tag 必须遵循 Semantic Versioning
INVALID_TAGS=$(git tag -l | grep -v "^v[0-9]\+\.[0-9]\+\.[0-9]\+\(\-\(alpha\|beta\|rc\|stable\)\)?$")
if [ -n "$INVALID_TAGS" ]; then
  echo "❌ 非法 tag 命名: $INVALID_TAGS"
  exit 1
fi

echo "✅ 命名规则一致"
```

### 3.4 文档化流程(王老师"逐步迭代"保障)

**`/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/04-复盘与决策/SOP_版本管理流程.md`**(新建):

| 步骤 | 触发 | 动作 | 工具 |
|------|------|------|------|
| **1. 新 Sprint 启动** | 王老师决策"开始 Sprint N" | `git checkout -b feature/sprint-N main` | git |
| **2. 开发** | 改代码 + 改文档 | 每个逻辑单元一个 commit | git |
| **3. Sprint 完工** | 王老师决策"Sprint N 完工" | `git checkout release/v3.x.y; git merge feature/sprint-N` | git |
| **4. 评审** | 王老师 review + 修改 | 反复 commit | git |
| **5. 打 tag** | 王老师确认"形成可发布大版本" | `git tag -a v3.x.y-stable -m "..."` | git |
| **6. 合并到 main** | Tag 完成后 | `git checkout main; git merge release/v3.x.y` | git |
| **7. dev 同步** | main 更新后 | `git checkout dev; git merge main` | git |
| **8. 检查工作树** | 每周 cron | 报警 + Agent 提议处理 | cron + Agent |

### 3.5 防止重复发生的"四道闸门"

| 闸门 | 检查内容 | 触发失败时 |
|------|---------|----------|
| **闸 1:pre-commit** | 1) 版本号一致性 2) 命名规则 | commit 阻断 |
| **闸 2:weekly cron** | 1) 工作树脏区 2) 分支差异 3) tag 完整性 | 飞书告警 |
| **闸 3:monthly review** | 1) 大版本对齐 2) 文档同步 3) 旧 Sprint 归档 | 王老师评审 |
| **闸 4:release branch** | 1) L1 测试 2) L3 验收 3) STATE.md / VERSION_MANAGEMENT.md 同步 | 自动检查 |

---

## 第四部分:具体修复动作(2026-09-05 21:00 实施清单)

### 4.1 立即修复(本次会话)

| # | 动作 | 目的 |
|---|------|------|
| **F1** | 48 项工作树脏区审计 | 区分 PoC 残留 / 跑批输出 / 新代码 |
| **F2** | `poc_atomicstrata/` 移到 `poc/atomicstrata-experiment` 分支 | 隔离实验性内容 |
| **F3** | 创建 dev 分支 | 持续开发 |
| **F4** | 写 VERSION_MANAGEMENT.md v2.0 补充自动化检查章节 | 完整规范 |
| **F5** | 写 SOP_版本管理流程.md(王老师流程)| 落地流程文档 |
| **F6** | 写 scripts/pre-commit-hooks/check-version-consistency.sh | 自动化 |
| **F7** | 写 scripts/weekly-git-health.sh | 周报 cron |
| **F8** | 在 STATE.md 末尾新增"版本管理规范"章节 | 同步规范 |

### 4.2 后续(待王老师拍板)

| # | 动作 | 触发 |
|---|------|------|
| **F9** | 设置 weekly cron 周日 22:00 跑 git-health | 王老师决策 |
| **F10** | 创建 release/v3.1.0-rc1 分支(在 dev 上)| Sprint 21 完工时 |
| **F11** | 王老师评审 v3.1.0-rc1 → 打 stable tag | 王老师确认后 |

---

## 第五部分:王老师拍板点(3 个决策)

### 决策 1:本次会话脏区怎么处理?

| 选项 | 动作 |
|------|------|
| 🟢 **A 全部 commit + clean**(F1-F8 全部执行)| 一次性整理 |
| 🟡 B 仅 commit 重要的,其余移到 `.gitignore` | 保守 |
| 🟣 C 不动,等下次 Sprint 一起处理 | 最保守 |

### 决策 2:atomicstrata PoC 处理?

| 选项 | 动作 |
|------|------|
| 🟢 **A 移到 `poc/atomicstrata-experiment` 分支**(F2)| 隔离 |
| 🟡 B 保留在 main,但加 `.poc_marker` 文件 | 标记 |
| 🟣 C 删除(王老师不需要)| 干净 |

### 决策 3:分支策略用哪种?

| 选项 | 模式 |
|------|------|
| 🟢 **A 简化版 GitFlow**(main + dev + feature/release/hotfix)| 推荐 |
| 🟡 B 仅 main + feature 分支 | 极简 |
| 🟣 C Trunk-based development(只 main + 短期 feature)| 最简 |

---

## 第六部分:防止再发生的"军规"

王老师 9-05 OUT-OF-BAND 触发,本规范确立以下**铁律**(王老师拍板后写入 PJ-000 基本法):

### 铁律 1:**版本号必须遵循 Semantic Versioning**

- 严禁 v1.x / v2.x / v3.0.x 混用
- 严禁"Sprint N 完工打 stable tag"(除非形成可发布大版本)

### 铁律 2:**实验性内容必须用 poc 分支**

- atomicstrata 等实验性内容不允许在 main
- 必须 `poc/<name>` 分支或 `.poc` 文件标记

### 铁律 3:**工作树脏区不能 > 5 项**

- 每周 cron 检查
- > 5 项飞书告警
- > 15 项 Agent 强制评审处理

### 铁律 4:**文档必须全量同步**

- 任何版本/分支改动 → STATE.md / VERSION_MANAGEMENT.md / README.md 同步
- 任何 Sprint 启动 → 04-复盘与决策/ 写 Sprint 计划
- 任何 Sprint 完工 → 04-复盘与决策/ 写 Sprint 报告 + git tag

### 铁律 5:**王老师拍板后才能打 stable tag**

- alpha / beta / rc 可以自打
- stable 必须王老师口头确认

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 21:30 CST
**协议版本**: hermes-anti-hallucination v42 + v44 教训(诚实告知)
**关联文档**: PJ-102 STATE.md / VERSION_MANAGEMENT.md / Sprint18 全项目复盘 Karpathy 对照优化方案.md
**王老师拍板**:决策 1/2/3 → 我立即执行 F1-F8
