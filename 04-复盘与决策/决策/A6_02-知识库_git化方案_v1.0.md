---
pj: PJ-102
title: 02-知识库 git 化方案 v1.0
date: 2026-09-06
status: 待王老师拍板 A/B/C
related: M4 A6 (Codex 评审 A6 项)
---

# 02-知识库 git 化方案 v1.0

## 现状(实测 2026-09-06)

- `02-知识库/PJ-102-LLM-MeetingKB/` 下有 325 个 wiki .md + 6 个 .base + 1 个 CLAUDE.md
- `02-知识库/.git` 不存在(无 git 跟踪)
- 当前修改:T-01 apply 19 个损坏 + A1 修复 + A4 dataview 236 + 15 = 251 个 + cascade 33 个 = 等等,实际有 1+ 编辑不可追踪

## 方案 A:在 02-知识库/ 独立建 git 仓库(推荐)

**做法**:
```
cd /mnt/d/BaiduSyncdisk/hermes/02-知识库
git init
git add PJ-102-LLM-MeetingKB/
git commit -m "init: PJ-102 wiki 知识库 v3.1.0-rc1"
```

**优点**:
- 独立 git 仓库,王老师可单独 commit / rollback
- Codex 评审"git 化是架构决策,3 个选项"中最稳妥

**风险**:
- PJ-102 git 和 02-知识库 git 是两个 repo,**commit 不会同步**
- 王老师需要手动同步 commit

## 方案 B:把 02-知识库 移入 PJ-102 仓库

**做法**:
```
mv /mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/wiki
git -C /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB add wiki/
git commit
```

**优点**:
- 单 repo,自动同步

**风险**:
- **大改王老师现有规范**(王老师 CDE 三层架构:02-知识库 是 E 盘备份)
- 需要修改所有脚本路径

## 方案 C:用 git 子模块把 PJ-102-LLM-MeetingKB 子模块化

**做法**:
```
git -C /mnt/d/BaiduSyncdisk/hermes/02-知识库 init
git add PJ-102-LLM-MeetingKB/
git commit
git -C /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB submodule add /mnt/d/BaiduSyncdisk/hermes/02-知识库 wiki
```

**优点**:
- 单 git 但物理位置不变

**风险**:
- 子模块是高级 git 特性,易出错
- 王老师目前没用过

## 王老师建议

按 Codex 评审结论 + 王老师"项目创建零依赖"原则 + CDE 三层架构:

**🟢 A 独立 git**(推荐):风险最低,不动现有架构
**🟡 B 移入 PJ-102**:最干净但大改
**🟣 C 子模块**:高风险不推荐

## 王老师决策点

王老师请回复:
- 🟢 "A"(独立 git 化,我立即执行)
- 🟡 "B"(移入,需评估 SOP 兼容性)
- 🟣 "C"(子模块)
- 🔴 "暂缓,M4 不做 02-知识库 git 化"

## 我建议

🟢 A(独立 git 化)— 最稳妥,不破坏 CDE 架构

实施步骤(等王老师拍板):
1. cd /mnt/d/BaiduSyncdisk/hermes/02-知识库
2. git init + .gitignore(PJ-002 pipeline 不在 02-知识库)
3. git add PJ-102-LLM-MeetingKB/
4. git commit "init: wiki 知识库 v3.1.0-rc1"
5. 写 WIKI_README.md 说明 git 工作流

王老师请拍板。
