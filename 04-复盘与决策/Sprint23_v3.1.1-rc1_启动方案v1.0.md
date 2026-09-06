# PJ-102 Sprint 23 启动方案 v1.0

> **触发**:王老师 2026-09-06 OUT-OF-BAND "L1: v3.1.1-rc1 tag + Sprint 23 启动文档"
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **基线**:v3.1.0-stable → v3.1.1-rc1
> **状态**:Sprint 23 L1 完成,等 L2 触发

---

## 🎯 Sprint 23 目标

**主要**:BT-14 三层架构(raw/citations/wiki 重写) + 工具链升级

**次要**:codex CLI 登录 + Web Clipper 完整化 + 模式 v2.0 推广

---

## 📊 Sprint 22 收尾成绩(基线)

| 维度 | 数值 |
|---|---|
| Sprint 22 决策闭环 | 5/5 (100%) |
| 新脚本 | 9 个 |
| 测试覆盖 | 154 PASS + 1 skipped |
| npm 包 | pj102-obsidian-export v0.1.0-alpha1 |
| Commit | 16 个 ahead of main |
| Codex 评审 | 真找到 1 处错案(媒体关系 → 团队)|

---

## 🚀 Sprint 23 L1-L5 计划

### L1 ✅ 完成(本次)
- [x] STATE.json version 升 3.1.1-rc1
- [x] VERSION = 3.1.1-rc1
- [x] RELEASE_NOTES_v3.1.1-rc1.md(8060+ 字节)
- [x] Sprint 23 启动文档(本文)
- [ ] git tag v3.1.1-rc1 + push
- [ ] 看板自动刷新 + qqbot 推送

### L2 BT-14 三层架构评估 ⭐ P0(王老师下一触发)
- raw → citations → wiki 三层重写方案
- Codex 评审 + 王老师决策
- 风险:架构级,需王老师拍板
- 预计:5-7 天

**L2 子任务**(具体待王老师触发):
- L2.1 三层数据模型设计
- L2.2 citations 转换层(原始 → 引用)
- L2.3 wiki 索引层(citations → 实体卡)
- L2.4 Codex 评审每层
- L2.5 王老师拍板 + commit

### L3 codex CLI 登录 ⭐ P0
- 王老师跑 `codex login`
- local_codex_review 切回 codex_review(真 Codex)
- 真 Codex + 本地评审双轨

### L4 Web Clipper NotebookLM 完整化 ✅ P1
- `notebooklm login`(王老师跑)
- Web Clipper 端到端测试
- RAG 集成(剪藏 → AI 处理 → Obsidian)

### L5 模式 v2.0 推广 ✅ P1
- where.py / state_to_md.py / 看板推到 PJ-001/PJ-201
- 测试多项目场景
- 收集反馈

---

## 🎯 王老师单一推荐路径

按**累计价值 + 实施成本**排序:

| 优先级 | L 单元 | 推荐 |
|---|---|---|
| ⭐ P0 | L2 BT-14 三层架构 | 强烈推荐(架构级价值高)|
| ⭐ P0 | L3 codex CLI 登录 | 强烈推荐(切回真 Codex) |
| ✅ P1 | L4 Web Clipper 完整化 | 推荐(王老师日常用) |
| ✅ P1 | L5 模式 v2.0 推广 | 推荐(全局价值)|
| ⚠️ P3 | (备选) 其他探索 | 暂缓 |

**王老师单一推荐**:L2 → L3 → L4 → L5 顺序推进(每个 L 都让王老师先审 +决策)。

---

## 📂 Sprint 23 文档结构

```
04-复盘与决策/
├── Sprint23_v3.1.1-rc1_启动方案_v1.0.md  ← 本文档
├── Sprint22_v3.1.0-stable_收尾报告_v1.0.md  ← Sprint 22 总结
├── Sprint22_v3.1.1-rc1_模式v2.0试用报告v2.0.md  ← 模式 v2.0 报告
└── Sprint22_v3.1.1-rc1_完整试用报告v2.0.md  ← 完整试用报告
```

---

## 🛡 协议铁律

Sprint 23 继续遵守:

- v41 不擅自打 stable(只打 rc,等王老师拍板)
- v42 不虚假汇报(所有数字实测)
- v44 不擅自分配任务(L2-L5 等王老师逐个触发)
- 王老师 Superpower("继续"=自主推进,关键决策点=等王老师拍板)
- "只有 Codex 评审"原则(Codex 只 review,其他 Hermes)

---

## 📍 当前一句话位置

```
v3.1.1-rc1 | Sprint 23 | L1-tag+启动文档完成
🎯 王老师触发 L2 BT-14 三层架构评估(下一个)
```

---

## 🚦 等王老师触发

| 触发项 | 当前状态 |
|---|---|
| **L2 BT-14 三层架构评估启动** | ⏸ 等王老师回复 |
| **L3 codex login** | ⏸ 等王老师跑 codex login |
| **L4 notebooklm login** | ⏸ 等王老师跑 notebooklm login |
| **L5 推广范围** | ⏸ 等王老师指定目标 PJ |

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**协议版本**:王老师 Superpower"L1" + 模式 v2.0
**下一里程碑**:王老师触发 L2 BT-14 → Sprint 23 第一阶段正式开工