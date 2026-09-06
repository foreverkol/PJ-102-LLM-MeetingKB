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
| P0 | `DT-01` | 75 persons relationship 修复 | 等王老师批 63 个分组清单(已自动填 12,剩 63) | 5-7 天 | low |
| P1 | `AT-11` | Web Clipper 集成 | 浏览器(Chrome/Edge/Firefox)+ API 来源(Noteboo | 5-7 天 | medium |
| P1 | `CT-13B` | atomicstrata npm 化 | 范围已明确,等 Sprint 22 第二周启动 | 7-10 天 | medium |
| P2 | `BT-14` | 三层架构(raw/citations/wiki 重写) | 架构级风险,需 Sprint 23+ 评估 | 15-20 天 | high |
| P3 | `ET-04` | organization entity 暂缓 | 数据条件不具备(等 PJ-201 数据) | 3-5 天 | low |

---

## 🚀 Do Now(本 Sprint 立即行动)

1. 等王老师批 DT-01 63 个关系清单(已生成 CSV/Excel 一键批改表)
2. 等王老师试用 Sprint 22 模式 v2.0 反馈(决定是否进 Sprint 23 推广)
3. 等王老师确认 AT-11 浏览器 + API 来源
4. L4.3c npm link 跨项目验证(等 L4.3b 反馈)

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

### DT-01:75 persons relationship 修复

- **优先级**:P0
- **阻塞**:等王老师批 63 个分组清单(已自动填 12,剩 63)
- **关联文件**:`04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-01-75建议清单_待王老师审_v1.0.json`
- **待批数**:63
- **ETA(批后)**:5-7 天
- **风险**:low
- **下一步**:王老师批 63 清单 → --apply → 75 全填

### AT-11:Web Clipper 集成

- **优先级**:P1
- **阻塞**:浏览器(Chrome/Edge/Firefox)+ API 来源(NotebookLM/微信/自建)
- **ETA**:5-7 天
- **风险**:medium
- **下一步**:王老师确认浏览器 + API 来源

### CT-13B:atomicstrata npm 化

- **优先级**:P1
- **阻塞**:范围已明确,等 Sprint 22 第二周启动
- **关联文件**:`04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-13B-atomicstrata-npm化启动分析_v1.0.md`
- **ETA**:7-10 天
- **风险**:medium
- **下一步**:Sprint 22 M1 启动阶段 A(解耦与抽象 3 天)

### BT-14:三层架构(raw/citations/wiki 重写)

- **优先级**:P2
- **阻塞**:架构级风险,需 Sprint 23+ 评估
- **ETA**:15-20 天
- **风险**:high
- **下一步**:Sprint 23 启动架构评估,本 Sprint 暂缓

### ET-04:organization entity 暂缓

- **优先级**:P3
- **阻塞**:数据条件不具备(等 PJ-201 数据)
- **ETA**:3-5 天
- **风险**:low
- **下一步**:等 PJ-201 数据库接入后再启动

---

_本文件由 `state_to_md.py` 从 `STATE.json` 自动生成于 2026-09-06 11:31:12 +0800_
