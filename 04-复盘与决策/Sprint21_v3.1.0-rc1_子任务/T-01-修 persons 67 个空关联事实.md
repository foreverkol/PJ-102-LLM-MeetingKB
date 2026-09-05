---
task_id: T-01
title: 修 persons 67 个空关联事实
priority: P0
status: ✅ 部分落地(Superpower M0)
parent_sprint: Sprint 21 v3.1.0-rc1
created: 2026-09-05 22:20 CST
updated: 2026-09-05 22:20 CST
---

# T-01: 修 persons 67 个空关联事实

## 📋 实测摸底(2026-09-05 22:20 CST)

实测 99 个 persons,**94 个 relationship 字段空(94.9%)**:
- relationship 字段空: 94
- source_meeting 字段空: 0(OK)
- name / role / type / date: 0% 空

## ✅ 已完成

1. **t01_fix_persons_relationship.py**(200 行)落地
2. **Dry-run 实测**:
   - 可自动分类:19 个(role 字段已知)
   - 需人工确认:75 个(role 未知,需王老师拍板)
3. 建议输出:`/tmp/pj102-t01-suggestions.json`(94 个建议)

## ⏳ 待王老师决策

王老师 9-05 OUT-OF-BAND Superpower 授权后,我自主完成:
- ✅ 脚本 + dry-run 实测
- ❌ 不擅自 apply(75 个需人工确认)

王老师选项:
- 🟢 A 王老师审 94 个建议清单,标记要 apply 的,Agent 跑 --apply
- 🟡 B Agent 跑 --apply 只 apply 19 个"可自动分类"(安全子集)
- 🟣 C 暂不修改,Sprint M1 D5 一起处理
