---
pj: PJ-102
title: PJ-102 v3.0 · Sprint 15 报告 — v3.0.1-stable 锚定 + 版本管理基础设施
version: v3.0.1-stable
date: 2026-09-04
status: ✅ PASS(王老师 20:35 OUT-OF-BAND 触发)
method: Superpower Sprint 15 — 成熟稳定版本锚定 + 回退能力建设
---

# PJ-102 v3.0 · Sprint 15 报告

> **王老师 09-04 20:35 OUT-OF-BAND 语音诉求**:
> "将作为这个项目的一个新的发布的一个版本,后面会做相应迭代来方便出现问题会回退到这个大的版本上面"

---

## 【总览】

| 维度 | 数据 |
|---|---|
| 王老师触发 | "成熟稳定版本打 tag + 可回退" |
| Sprint 15 完成 | ✅ v3.0.1-stable tag + 回退能力建设 |
| 新增 commit | **1 个**(`ff7ca8e`)+ 1 个新 tag |
| 新增文件 | VERSION_MANAGEMENT.md(166 行)+ scripts/rollback.sh(94 行)|
| 关键能力 | **一键回退 / 版本对照 / 自动 stash** |

---

## 【详细 — Sprint 15 关键决策】

### 决策 1:把当前 13 sample 实测跑通版本作为 v3.0.1-stable

**理由**:
- v3.0.0 是理论架构(王老师 13:00 决策)
- v3.0.1-stable 是**实战锚点**(13 sample 真跑 + 6 类 5/6 命中)
- 不冲突:v3.0.0 保留为基线,v3.0.1-stable 是实战稳定版

### 决策 2:不打新主版本号(v3.1.0),用 stable 后缀

**理由**:
- v3.0 体系内稳定锚点,不需要 minor bump
- semantic versioning `v<major>.<minor>.<patch>-<suffix>` 严格遵循
- 王老师后续可基于 stable 迭代 patch(v3.0.2-stable 等)

### 决策 3:8 个非 PJ-102 文件 stash(不污染 PJ-102 commit)

**实测发现**:
- `03-执行/工具/output/争议焦点.md` / `证据链.md` / `财务vs通知对比.md` 等
- 这些是**法律案件调查类产物**(不是 PJ-102 项目内容)
- 误放 PJ-102 目录,**stash 保留但不 commit**

### 决策 4:VERSION_MANAGEMENT.md + scripts/rollback.sh 永久基础设施

- 166 行文档:版本号约定 + 4 种回退场景 + 5 步发布流程
- 94 行脚本:实战测试可用(列出 4 个 tag + 安全检查 + L1 验证)

---

## 【详细 — rollback.sh 实战测试结果】

```bash
$ bash scripts/rollback.sh

用法:
  bash scripts/rollback.sh <tag> [--keep]

可用 tag:
  v1.0-baseline (2026-09-04) - feat(s12): 补全 4 类 WIKI 生成器(v1.1)
  v1.0.0 (2026-09-03) - Release v1.0.0: PJ-102-LLM-MeetingKB 全项全量移植完成
  v1.1.0 (2026-09-04) - Release v1.1.0: 补全 4 类 WIKI 生成
  v3.0.0 (2026-09-04) - PJ-102 v3.0.0 release
```

✅ **列表功能正常** / ✅ **参数解析正常** / ✅ **tag 验证逻辑正常**

---

## 【王老师 4 种回退场景覆盖】

### 场景 1:开发中遇到 bug
```bash
git checkout v3.0.1-stable -- 03-执行/code/ 02-设计/
```

### 场景 2:对比 v3.0.0 → v3.0.1-stable
```bash
git log v3.0.0..v3.0.1-stable --oneline
git diff v3.0.0 v3.0.1-stable -- 03-执行/code/
```

### 场景 3:一键回退(rollback.sh)
```bash
bash scripts/rollback.sh v3.0.1-stable        # 硬回退
bash scripts/rollback.sh v3.0.1-stable --keep # 自动 stash
```

### 场景 4:历史版本对照
```bash
git tag -l "v*" | while read tag; do
    git show $tag:VERSION
done
```

---

## 【GitHub 状态】

```
PJ-102-LLM-MeetingKB:
- 55 个 commit(Sprint 1-15)
- 5 个 tag: v1.0-baseline / v1.0.0 / v1.1.0 / v3.0.0 / v3.0.1-stable
- L1 测试:82/82 PASS(0.078s)
- 全部 push 同步
```

本会话 S15 commit(1 个):
```
ff7ca8e S15 release: v3.0.1-stable 版本管理基础设施
```

新 tag:
```
v3.0.1-stable (push 成功,GitHub 已可见)
```

---

## 【决策点 — Sprint 16+ 候选】

```
□ Sprint 16 启动(打 v3.0.2-stable patch)
  - 比如修某个 bug / 优化某个 step
  - 增量 patch,不需要重跑 13 sample

□ Sprint 17 启动(v3.1.0 minor 升级)
  - 后台批量跑 50+ sample
  - 飞书 dashboard / cron 自动化

□ 暂停,等王老师后续迭代指令
```

---

## ⚠️ 已知问题 + 王老师决策点

1. **8 个非 PJ-102 文件暂存在 stash**:
 - `git stash list` 可看
 - 王老师决定:删除 / 移到正确项目 / 永久 stash
2. **.release-please-manifest.json 改 3.0.1-stable**:GitHub release 自动检测会识别这个变化
3. **后续每次 Sprint 完工**:王老师决策是否打新 stable tag(默认建议打)