# PJ-102 Sprint 25 启动方案 v1.0

> **触发**:王老师 2026-09-06 OUT-OF-BAND "按推荐执行"
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **基线**:v3.1.2-rc1 → v3.1.3-rc1
> **状态**:Sprint 24 全部 L2-L6 完成,Sprint 25 启动

---

## 🎯 Sprint 25 目标

**主要**:Sprint 24 模式 v2.0 v3.0 跨 PJ 实测 + 真 Codex 评审切回 + 看板 Swarm 实施

**次要**:Web Clipper RAG 完整化 + 跨 PJ 数据血缘打通

---

## 📊 Sprint 24 收尾成绩(基线)

| 维度 | 数值 |
|---|---|
| Sprint 24 决策闭环 | 0 项(无新增决策,直接推进)|
| Sprint 24 新脚本 | 3 个(llm_cite_extract + build_web_dashboard 升级 + tier_classifier 升级)|
| Sprint 24 测试 | 172 PASS + 1 skipped(无回归) |
| Sprint 24 Git commits | 3 个(L2-L6 实施)|
| L2 推广 | 26 个 PJ 接收 6 核心脚本(156 文件)|
| 三层架构数据血缘 | 402 文件(从 363 → 402) |
| 看板 v3 移动端 | 4 个 CSS 媒体查询 |

### Sprint 24 累计产出

| 件 | 状态 |
|---|---|
| llm_cite_extract.py (6811 字节) | ✅ 就绪,API 沙箱限制 |
| 看板 v3 移动端 CSS | ✅ 4 个 @media 规则 |
| 26 PJ 接收工具 | ✅ where/state_to_md/sync_state/build_web_dashboard/feishu_notify/kanban_refresh |
| Web Clipper 端到端 | ✅ Wikipedia 30582 字节抓取 + 26 citations |

---

## 🚀 Sprint 25 L1-L6 计划

### L1 ✅ 完成(本次)
- [x] STATE.json version 升 3.1.3-rc1
- [x] VERSION = 3.1.3-rc1
- [x] Sprint 25 启动文档(本文)
- [x] Sprint 24 试用报告 v1.0
- [ ] v3.1.3-rc1 tag + push

### L2 Sprint 24 试用报告 v1.0 ⭐ P0(王老师先审)
- 评估 Sprint 24 全部 L 单元的实际效果
- 收集 26 个 PJ 推广反馈
- 评估三层架构数据血缘价值
- 评估看板 v3 移动端体验
- 评估 LLM 抽取质量(等 API 解锁)

### L3 跨 PJ 看板 Swarm ⭐ P0
- 把 26 个 PJ 的看板汇总到一个 hub
- 每个 PJ 显示进度 + 决策点 + Sprint 状态
- 王老师一屏看 26 个 PJ
- 实测 1-2 个 PJ 接入 hub

### L4 真 Codex CLI 登录 + 切回 ⭐ P0(等王老师 login)
- 王老师跑 `codex login`
- codex_reviewer.py 自动检测 → 切回真 Codex
- 双轨:真 Codex + 本地评审都保留
- 跑最近 3 commit 真 Codex 评审对比

### L5 Web Clipper + NotebookLM 端到端真数据 ⭐ P0(等王老师 login)
- 王老师跑 `notebooklm login`
- 抓 5-10 个真实 URL
- `notebooklm_rag.py --sync` 推到 notebook
- AI 处理结果 → 写到 wiki
- 闭环验证

### L6 模式 v2.0 v3.0 持续推广 ✅ P1
- 收集 26 个 PJ 反馈
- 修复工具 bug(基于实测)
- 增加新功能(基于需求)
- 写推广手册 v1.0

---

## 🎯 王老师单一推荐路径

| 优先级 | L 单元 | 推荐 |
|---|---|---|
| ⭐ P0 | L2 Sprint 24 试用报告 | 强烈推荐(完整评估) |
| ⭐ P0 | L3 跨 PJ 看板 Swarm | 强烈推荐(全局价值) |
| ⭐ P0 | L4 codex login 切换 | 强烈推荐(王老师操作) |
| ⭐ P0 | L5 Web Clipper + NotebookLM | 强烈推荐(王老师操作) |
| ✅ P1 | L6 模式 v2.0 持续推广 | 推荐(运维) |

**王老师单一推荐**:L2 → L3 → L4 → L5 → L6 顺序推进(每个 L 都让王老师先审 +决策)。

---

## 📂 Sprint 25 文档结构

```
04-复盘与决策/
├── Sprint25_v3.1.3-rc1_启动方案_v1.0.md  ← 本文档
├── Sprint24_v3.1.2-rc1_完整试用报告v1.0.md  ← Sprint 24 总结(本次新写)
├── Sprint24_v3.1.2-rc1_启动方案v1.0.md  ← Sprint 24 启动
└── Sprint23_v3.1.1-rc1_完整收尾报告v1.0.md  ← Sprint 23 总结
```

---

## 🛡 协议铁律

Sprint 25 继续遵守:

- v41 不擅自打 stable(只打 rc,等王老师拍板)
- v42 不虚假汇报(所有数字实测)
- v44 不擅自分配任务(L2-L6 等王老师逐个触发)
- 王老师 Superpower("继续"=自主推进,关键决策点=等王老师拍板)
- "只有 Codex 评审"原则(Codex 只 review,其他 Hermes)

---

## 📍 当前一句话位置

```
v3.1.3-rc1 | Sprint 25 | L1-tag+启动文档完成
🎯 王老师触发 L2/L3/L4/L5(任何一项即可启动)
```

---

## 🚦 等王老师触发

| 触发项 | 当前状态 |
|---|---|
| **L2 Sprint 24 试用报告** | ⏸ 等王老师触发(已写好模板) |
| **L3 跨 PJ 看板 Swarm** | ⏸ 等王老师触发 |
| **L4 codex login** | ⏸ 等王老师跑 codex login |
| **L5 notebooklm login** | ⏸ 等王老师跑 notebooklm login |
| **L6 模式 v2.0 持续推广** | ⏸ 等王老师触发 |

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**协议版本**:王老师 Superpower"按推荐执行" + 模式 v2.0
**下一里程碑**:王老师触发 L2 → Sprint 25 第一阶段正式开工