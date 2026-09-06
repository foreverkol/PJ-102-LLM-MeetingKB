# PJ-102 LLM MeetingKB · 项目状态

> **自动生成**:`python3 scripts/state_to_md.py`
> **生成时间**:2026-09-06 11:31:12 +0800
> **真值源**:`STATE.json`(不要手改本文件,改 STATE.json 后跑本脚本)

---

## 🎯 当前状态(一眼到底)

| 项 | 值 |
|---|---|
| **版本** | `3.1.0-stable` |
| **tag** | `v3.1.0-stable` |
| **分支** | `dev` |
| **ahead of main** | 25 commits |
| **当前 Sprint** | **Sprint 22** |
| **Sprint 状态** | M2-Sprint22推进中(where.py统一面板就绪) |
| **最后 commit** | `c634bd9` feat(t01): 99 人一键批改 CSV(王老师可直接 Excel 打开) |

---

## ✅ 上一 Sprint 战果(Sprint 21)

**完成日期**:2026-09-06  
**版本演进**:v3.1.0-rc1 → v3.1.0-stable

| 指标 | 数值 |
|---|---|
| L1 测试 | **98 passed in 3.45s** |
| Wiki 文件 | **351** |
| BAD YAML | **0** |
| Sprint 子任务 | 12/14 完成 + 5 待决策 |

---

## 🎯 待王老师决策点(优先级排序)

**当前生效 Sprint**:Sprint 22

| 优先级 | ID | 标题 | 阻塞 | ETA | 风险 |
|---|---|---|---|---|---|
| P1 | `AT-11` | AT-11 Web Clipper:浏览器 + API 来源 | 需王老师回复 2 项 | - | medium |
| P1 | `CT-13B` | CT-13B atomicstrata npm 化:阶段 C | 等王老师确认 npm link 验证是否启动 | - | medium |
| P2 | `BT-14` | BT-14 三层架构:评估中 | 架构级风险,Sprint 23 评估 | - | high |
| P3 | `DT-01` | 扫一眼 99 人 relationship,改错的(可选) | 无需操作,99/100 已全填 | - | low |
| P3 | `ET-04` | ET-04 organization entity:暂缓中 | 等 PJ-201 数据,自动暂停 | - | low |

---

## 🚀 Do Now(本 Sprint 立即行动)

1. 王老师只需决定 AT-11 是否启动(其他 4 项都不阻塞 Sprint 22 收尾)

---

## 🏗 模式架构 v2.0

- **单一真值源**:`STATE.json`
- **生成脚本**:`scripts/state_to_md.py`
- **核心原则**:STATE.json = 主体,STATE.md = 自动生成的 markdown 视图

**文档体系**(副作用而非主体):

- `STATE.md`:自动从 STATE.json 生成
- `STATE.json`:本文件 = 单一真值源
- `CHANGELOG.md`:自动从 git log 生成
- `VERSION_REGISTRY.md`:自动从 git tag + STATE.json 生成
- `RELEASE_NOTES_*.md`:模板 + STATE.json 填充

---

## 🛡 协议铁律遵守

- **v41_no_unauthorized_stable_tag**:OK
- **v42_no_false_reporting**:OK
- **v44_no_unauthorized_task_allocation**:OK
- **wang_superpower_protocol**:OK

---

## 📋 决策点详情(完整)

### AT-11:AT-11 Web Clipper:浏览器 + API 来源

- **优先级**:P1
- **阻塞**:需王老师回复 2 项
- **风险**:medium
- **下一步**:回复后 → 我开发 Web Clipper

### CT-13B:CT-13B atomicstrata npm 化:阶段 C 启动?

- **优先级**:P1
- **阻塞**:等王老师确认 npm link 验证是否启动
- **风险**:medium
- **下一步**:回复后 → 我推进

### BT-14:BT-14 三层架构:评估中

- **优先级**:P2
- **阻塞**:架构级风险,Sprint 23 评估
- **风险**:high
- **下一步**:Sprint 23 启动架构评估

### DT-01:扫一眼 99 人 relationship,改错的(可选)

- **优先级**:P3
- **阻塞**:无需操作,99/100 已全填
- **风险**:low
- **下一步**:跳过 → 我继续 Sprint 22 收尾

### ET-04:ET-04 organization entity:暂缓中

- **优先级**:P3
- **阻塞**:等 PJ-201 数据,自动暂停
- **风险**:low
- **下一步**:等 PJ-201 数据接入

---

_本文件由 `state_to_md.py` 从 `STATE.json` 自动生成于 2026-09-06 11:31:12 +0800_


DRIFT_MARKER_20260906
