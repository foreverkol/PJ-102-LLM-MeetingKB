# PJ-102-LLM-MeetingKB · STATE

> **状态**: ✅ v3.0.1-stable + Sprint 18/20 P0 完工
> **最后更新**: 2026-09-05 (由 Hermes 实测同步)
> **运行模式**: 独立项目 · Sprint 模式
> **基线对齐**: 与 v3.0.1-stable tag 一致(commit ff7ca8e)
> **HEAD 位置**: 3414518(Sprint 22 VERSION_MANAGEMENT.md 规范更新)

---

## 📊 当前状态(v3.0.1-stable)

| 维度 | 数据 | 来源 |
|---|---|---|
| 当前版本 | **v3.0.1-stable**(tag 已 push) | `git tag -l` 实测 |
| 当前 HEAD | `3414518` | `git log --oneline -1` |
| GitHub commits | **70** | `git rev-list --count HEAD` |
| Git tags | **5** 个 | `git tag -l --sort=-creatordate` |
| 已完成 Sprint | **8/12**(66%) | `04-复盘与决策/Sprint*.md` |
| 代码模块 | 22 个 Python 文件 | git 树统计 |
| WIKI md | 32 个(v1.0 baseline) | git 树统计 |
| L1 测试 | 125/125 PASS(0.112s) | Sprint 11 实测 |
| 10 Hard Gate | 10/10 PASS(L3 验收) | L3 验收报告 |
| LLM Provider | **MiniMax-M3** ⭐ 王老师 09-04 纠正 | llm_client.py |
| GitHub 同步 | ✅ origin/main = local/main | `git status` |

## 🏷️ 全部 tag(实测,2026-09-05)

```
v3.0.1-stable  ← 当前(2026-09-04 20:44 Sprint 15)
v3.0.0         (2026-09-04 13:00 Sprint 1 收尾)
v1.1.0         (2026-09-03 升级)
v1.0-baseline  (2026-09-03 起点)
v1.0.0         (2026-09-03 首次发布)
```

> ⚠️ v3.0.2-stable / v3.0.3-stable / v3.0.4-stable 三个 Sprint 节点 tag 在 2026-09-04 22:30 王老师规范更新后由 commit b7acc0c 清理(v41 教训:stable tag 必须是王老师确认"形成可发布大版本"才能打,不能每个 Sprint 都打)

---

## ✅ 已完成 Sprint(8/12 — 66%)

### Sprint 1 — v6.1 + v7.0 集成(W1-W4 26/26 TC)
- ✅ W1 v6.1 P-1/P-2/P-3/P-4 集成(7 TC):判断标注 / 金融参数 / 资产 tag / meeting_type
- ✅ W2 v7.0 + 9 个新模块(8 TC,44 L1):ldamc 5 维 / contradictions / entity_id / citations
- ✅ W3 Query + scenario(5 TC,25 L1):entity_nav / kb_retriever / s14_scenario / review_queue
- ✅ W4 自动化 + L3 + release(6 TC):GitHub CI / cron / SAMPLE_LIMIT=10 / v3.0.0 tag

### Sprint 3 — Sprint 3 总结报告(4375 B)
- 关联 2026-09-04 13:04,前置 atomicstrata 集成

### Sprint 6 — Hermes MCP 实际接入(4524 B)
- 关联 2026-09-04 14:48,配置层面接入完成

### Sprint 8 — v3.0 真实跑通(6282 B)
- 关联 2026-09-04 17:06,Wiki 产物 v3 落地

### Sprint 9 — v3.0 Wiki 质量真实化(5885 B)
- 关联 2026-09-04 17:29,meeting_type + ldamc 真实化

### Sprint 11 — max_tokens 524288 + 扩量(5061 B)
- 关联 2026-09-04 18:36,MiniMax-M3 官方上限

### Sprint 12 — 5 sample 全部跑通(3861 B)
- 关联 2026-09-04 19:06

### Sprint 13 — 10 sample 扩量(5045 B)
- 关联 2026-09-04 19:51,meeting_type 5/6 = 83.3%

### Sprint 14 — 13 sample 扩量(3302 B)
- 关联 2026-09-04 20:32,industry_exchange 命中 + personal_thinking 缺失

### Sprint 15 — v3.0.1-stable 锚定(4217 B)
- 关联 2026-09-04 20:44,tag ff7ca8e
- ✅ **当前稳定版本基线**

### Sprint 18 — Karpathy 对照 + P0 完工(13649 + 5271 B)
- 关联 2026-09-04 21:18 / 21:36
- 全项目复盘 + Karpathy LLM Wiki 对照 + index.md + Grounding Invariant

### Sprint 20 — 五层动态进度可视化(8571 B)
- 关联 2026-09-04 22:34
- build_dashboard.py + progress.sh + build_changelog 三个工具落地

---

## 🔵 进行中 / 待定(看板标记的 5 个)

| 状态 | Sprint | 报告 | 真实状态判断 |
|------|--------|------|--------------|
| 🔵 进行中 | Sprint 3 | Sprint3总结报告_v3.0.md | 报告已存在,看板状态判定偏严 |
| 🔵 进行中 | Sprint 14 | Sprint14_扩量+meeting_type报告.md | 报告已存在,看板状态判定偏严 |
| ⚠️ 警告 | Sprint 18 复盘 | Sprint18_全项目复盘_Karpathy对照_优化方案.md | 复盘已落地,优化方案待执行 |
| 🔵 进行中 | Sprint 20 | Sprint20_五层动态进度可视化方案.md | 工具已落地,看板自动生成可继续 |
| 🔵 进行中 | Sprint 22 | (无独立报告) | HEAD 3414518 — VERSION_MANAGEMENT.md 规范更新 |

> 📌 **看板"进行中"标记偏严**:脚本从报告前 500 字符判断 ✅ / ⚠️ / 🔵,但只要没看到 "✅ PASS" 字符串就标 🔵。Sprint 3/14/20 实际都已完成。

---

## ⚠️ 王老师硬限制(2026-09-04 13:00 明确)

- **不要跑全量 286 个录音文字**
- **只跑 ≤10 个测试样例**
- SAMPLE_LIMIT=10 默认配置已落实

---

## 🔒 永久防丢失机制(铁律零)

```
write_file → [1] ls -la 验证存在
          → [2] wc -l 验证行数
          → [3] head -3 验证内容
          → [4] git add <path>
          → [5] git commit -m "..." + git log --oneline -1 验证

任一失败立刻报告,不允许跨过。
```

2026-09-04 12:00 文档丢失事件教训固化。

---

## 📋 v6.1 4 补丁 + v7.0 10 新规(Sprint 1 落地)

### v6.1(4)
1. ✅ 判断标注 `[判断:发言人]`
2. ✅ 定量金融参数 9 类
3. ✅ 可转化资产 tag 5 类
4. ✅ meeting_type 6 类 + subtype 6 类

### v7.0(10)
1. ✅ ldamc 5 维自检
2. ✅ contradictions 字段
3. ✅ entity_id 统一编号
4. ✅ canonical_name + aliases
5. ✅ status_stage 5 阶段状态机
6. ✅ topic_key judgment 主题聚合
7. ✅ evolution 演化链
8. ✅ scenario 新页面类型
9. ✅ external_ref 纯度规则
10. ✅ extraction_patch YAML 中间层

---

## 📂 v3.0 Rev2 文档(4 份)

| 文档 | 行数 | 大小 | commit |
|---|---:|---:|---|
| 01-需求/需求总纲_v3.0-SCHEMA71集成.md | 412 | 21KB | 0adb139 |
| 02-设计/设计总纲_v3.0-SCHEMA71集成.md | 725 | 28KB | 9290435 |
| 03-执行/测试验证_v3.0-SCHEMA71集成.md | 841 | 35KB | b34ad46 |
| 03-执行/工程执行计划_v3.0-SCHEMA71集成.md | 304 | 10KB | 6d638e6 |

---

## 📈 最近 5 commit(实测)

```
3414518 docs: VERSION_MANAGEMENT.md 加王老师 22:30 规范更新
b7acc0c fix: 清理 Sprint 节点违规 tag + 修正版本规范
3d50c24 S20 release: v3.0.4-stable - 五层动态进度可视化体验升级
eedfc67 S20 feat: 五层动态进度可视化工具落地 — build_dashboard + progress.sh + build_changelog
cad5db6 S20 docs: 五层动态进度可视化方案 — 不改变执行内容,只增加观察/汇报层
```

> 注:`3d50c24` 是 Sprint 20 release commit,但其 tag `v3.0.4-stable` 已在 b7acc0c 清理。Sprint 20 实际工作落地,只是 tag 按 v41 规范回收。

---

## 🚧 工作树脏区(2026-09-05 实测)

```
git status 报告:
- 8 modified: 03-执行/工具/output/*.md (Sprint 11-14 跑批输出残留)
- 8 untracked: */03-执行/工具/ (空目录,9-04 23:54-55 创建)
```

> 📌 **未擅自处理**:王老师没说要清 git 脏区,按 v44 教训独立守护模式原则,只同步元数据不动工作树。需要清理请王老师指令。

---

## 待办 / 候选(王老师决策)

### Sprint 后续候选
- 🔵 **Sprint 21** — Karpathy 对照方案优化项落地(Sprint 18 复盘待执行项)
- 🔵 **Sprint 22** — 真实跑批数据补完 personal_thinking(Sprint 14 发现的真实数据缺失)
- 🔵 **运行 build_dashboard.py** — 看板自动生成已落地,可定期 cron 跑

### 元数据持续同步
- 🔵 看板自动生成 — 已可用 `python3 03-执行/scripts/build_dashboard.py`
- ⚪ STATE.md 本次同步(2026-09-05 12:54 由 Hermes 完成)

---

## 🚧 Sprint 21 v3.1.0-rc1 状态(2026-09-05 21:00 实测)

> **王老师 9-05 OUT-OF-BAND**:"前面不是 V3.0 的版本吗"+"没有对项目 PJ-102 的继承"
> **修正**:3 个 Sprint 21 文档版本号从 v1.0/v2.0 → v3.1.0-minor/alpha1/rc1,真实继承 PJ-102 现有基础

### 3 个 Sprint 21 决策文档(已 commit `f7ff32c`)

| 文档 | 大小 | 状态 |
|------|------|------|
| `Sprint21_v3.1.0-minor路线图.md` | 8.5 KB | ✅ 粗略版 |
| `Sprint21_v3.1.0-alpha1详细方案.md` | 18.7 KB | ✅ 王老师语音第 1 次后 |
| `Sprint21_v3.1.0-rc1_Karpathy_Obsidian双核心升级方案.md` | 27.9 KB | ✅ 王老师语音第 2 次后(双核心定位) |

### v3.1.0-rc1 真实待做(14 个任务,精简)

基于已完工的 Sprint 18/19/20(check_evidence.py + index.md + log.md + Triage + 同义词 + 五层 dashboard),v3.1.0-rc1 真实待做只有 14 个任务(T-01~T-14),不是之前的 18 FR + 11 NFR。

**完整内容**:见 `04-复盘与决策/Sprint21_v3.1.0-rc1_Karpathy_Obsidian双核心升级方案.md` 第二部分修订(A/B/C/D/E 5 段)。

### 关键继承事实(实测,2026-09-05)

| 项 | 状态 |
|----|------|
| v3.0.1-stable tag | ✅ 55 commits,真实存在 |
| Sprint 18 P0 (cfd3954) | ✅ 代码已完成,tag v3.0.2-stable 未打(v41 教训)|
| Sprint 19 P1 (2d8b375) | ✅ 代码已完成,tag v3.0.3-stable 未打 |
| Sprint 20 (3d50c24) | ✅ 代码已完成,tag v3.0.4-stable 未打 |
| atomicstrata PoC | ✅ 24 concepts + 3 sources,commit `438716d` |

---

## 🚧 Sprint 21 v3.1.0-rc1 Superpower M0+M1 状态(2026-09-05 22:35 CST)

> **王老师 9-05 OUT-OF-BAND**:"按照你的建议智能化执行"
> **Superpower 模式**:授权后不询问直接执行,真阻塞才上报

### M0 详细工程计划 + 闸门(已落地)

| 产出 | 状态 | commit |
|------|------|--------|
| 详细工程计划 v1.0(16.5 KB, 8 部分) | ✅ | `20091f5` |
| 14 个 T-XX 子任务文件 | ✅ | `20091f5` |
| T-08 obsidian_export.py(200 行, 4 .base + CLAUDE.md) | ✅ | `20091f5` |
| 闸门 1 pre-commit hook(实测通过 exit 0) | ✅ | `d69ddb9` |
| SOP_cron 启用指南 v1.0(王老师手动) | ✅ | `b5cc000` |

### M1 P0 4 项(已落地)

| 任务 | 状态 | 实测产出 |
|------|------|---------|
| T-01 persons relationship | ✅ 部分 | 94 个空(94.9%) / 可自动分类 19 / 需人工 75 |
| T-02 Cascade Updates | ✅ 部分 | 13 sources / 派生 wiki > 280 |
| T-08 Obsidian Bases | ✅ 完成 | 4 .base + CLAUDE.md / 325 wiki 源 |
| T-13 行号引用 | ✅ 分析 | 主 wiki 0 / poc 24 中 22 / 279 处 |

### M1 commits(本次 4 个)

```
3a2051b feat(sprint21-m1): T-02 Cascade Updates + T-13 行号引用分析
b5cc000 feat(sprint21-m1-t01): T-01 persons relationship 修复脚本 + dry-run 实测
d69ddb9 sop: 闸门 1 pre-commit hook 落地并实测通过
20091f5 feat(sprint21-m0): 详细工程计划 v1.0 + 14 个子任务 + obsidian_export.py 落地
```

### 王老师拍板点(下一步)

1. **T-01 是否 apply**:🟢 A 仅 apply 19 个可自动分类 / 🟡 B 王老师审 94 个建议 / 🟣 C 不修改
2. **T-13 升级方案**:🟢 A 迁移 / 🟡 B 升级流水线 / 🟣 C 保留
3. **cron 启用**:王老师手动 `sudo service cron start` + 加 2 行(已在 SOP_cron启用指南_v1.0.md)
4. **M2 启动**:P1 5 项 T-03 + T-04 + T-05 + T-06 + T-09

### v44 教训:Superpower 模式自主推进

- ✅ 闸门 1 已启用并实测通过(exit 0)
- ✅ T-01/T-02/T-13 dry-run(不擅自 apply)
- ✅ T-08 完成(王老师立即可用)
- ❌ 不擅自 apply T-01 75 个需人工确认文件

---
