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

| 优先级 | ID | 标题 | 状态 | 推荐选项 |
|---|---|---|---|---|
| P1 | `AT-11` | AT-11 Web Clipper | ⏸ 等王老师回复 | A. ⭐ 强烈推荐 |
| P1 | `CT-13B` | CT-13B 阶段 C npm link | 🔄 阶段 A+B 完成 | A. ⭐ 强烈推荐 |
| P2 | `BT-14` | BT-14 三层架构 | ⏸ Sprint 23 评估 | A. ✅ 推荐 |
| P3 | `DT-01` | DT-01 99 人 relationship | ✅ 已 100% (99/99) | B. ✅ 推荐 |
| P3 | `ET-04` | ET-04 organization entity | ⏸ 自动暂缓 | A. ✅ 推荐 |

---

## 🚀 Do Now(本 Sprint 立即行动)

1. 王老师只需回复 AT-11 和 CT-13B(我推荐 A+A,推荐理由见决策点卡片)

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

### AT-11:AT-11 Web Clipper

- **优先级**:P1
- **状态**:⏸ 等王老师回复
- **推荐**:`A` A. Chrome + NotebookLM API — Chrome 用户最多(王老师常用),NotebookLM 王老师已有账号;5-7 天完成,与 Sprint 22 收尾并行
- **风险**:medium
- **下一步**:-

### CT-13B:CT-13B 阶段 C npm link

- **优先级**:P1
- **状态**:🔄 阶段 A+B 完成
- **推荐**:`A` A. 做(本 Sprint 完成) — npm 包结构 + Node.js wrapper 已就绪,只差跨项目验证;1-2 天工作量,闭合 L4.3c
- **风险**:medium
- **下一步**:-

### BT-14:BT-14 三层架构

- **优先级**:P2
- **状态**:⏸ Sprint 23 评估
- **推荐**:`A` A. 等 Sprint 23 评估(自动) — 架构级风险不应在 Sprint 22 推进,需专项评估
- **风险**:high
- **下一步**:-

### DT-01:DT-01 99 人 relationship

- **优先级**:P3
- **状态**:✅ 已 100% (99/99)
- **推荐**:`A` A. 扫一眼 CSV,改错的(可选) — Codex 评审已修正1 个错案,启发式扩量到 99 人,王老师扫一遍耗 30+ 分钟发现不了新问题
- **风险**:low
- **下一步**:-

### ET-04:ET-04 organization entity

- **优先级**:P3
- **状态**:⏸ 自动暂缓
- **推荐**:`A` A. 等 PJ-201 数据接入(自动) — 无需王老师操作,数据条件不成熟时不应推进
- **风险**:low
- **下一步**:-

---

_本文件由 `state_to_md.py` 从 `STATE.json` 自动生成于 2026-09-06 11:31:12 +0800_
