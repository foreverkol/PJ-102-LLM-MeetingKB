# PJ-102 Sprint 24 启动方案 v1.0

> **触发**:王老师 2026-09-06 OUT-OF-BAND "A+B 全部执行"
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **基线**:v3.1.1-rc1 → v3.1.2-rc1
> **状态**:Sprint 23 全部 L1-L5 完成,Sprint 24 L1 启动

---

## 🎯 Sprint 24 目标

**主要**:模式 v2.0 全面推广 + L5 跨项目实测 + Codex CLI 登录切换

**次要**:Web Clipper 完整化 + 看板 v3 升级

---

## 📊 Sprint 23 收尾成绩(基线)

| 维度 | 数值 |
|---|---|
| Sprint 22-23 决策闭环 | 9 项(100%)|
| Sprint 23 新脚本 | 6 个 |
| Sprint 23 测试 | 172 PASS + 1 skipped |
| Sprint 23 Git commits | 5 个 |
| 三层架构数据血缘 | raw:12 / citations:123 / wiki:255 |
| L5 推广 | 6 脚本 → PJ-001(试水)|
| Web Clipper 实测 | 3 个真实 URL(2026-09-06)|

---

## 🚀 Sprint 24 L1-L6 计划

### L1 ✅ 完成(本次)
- [x] STATE.json version 升 3.1.2-rc1
- [x] VERSION = 3.1.2-rc1
- [x] Sprint 24 启动文档(本文)
- [x] v3.1.2-rc1 tag + push
- [ ] git push 异常修复

### L2 模式 v2.0 v3.0 多 PJ 同步 ⭐ P0
- 把 6 个核心脚本(Sprint 23 已用)推广到所有 30 个 PJ
- **不**自动推广(PJ 需独立决定)
- 提供 `promote_v2_to_pj.py --all --dry-run` 预览
- 王老师逐个确认

### L3 Codex CLI 登录 + 切换回真 Codex ⭐ P0
- 王老师跑 `codex login`
- `codex_reviewer.py` 自动检测 → 切回真 Codex
- 双轨:真 Codex + local Codex 都保留
- 验证:跑 commit 评审 → 应调真 Codex

### L4 Web Clipper + NotebookLM 端到端真实数据 ⭐ P0
- 王老师跑 `notebooklm login`
- 抓 5-10 个真实 URL(GitHub/Python docs/Anthropic 等)
- `notebooklm_rag.py --sync` 推到 notebook
- AI 处理结果 → 写到 wiki
- 闭环验证

### L5 看板 v3 升级(移动端友好)✅ P1
- HTML 看板增加响应式设计
- 看板 Swarm:多 PJ 同时展示
- qqbot/weixin 推送内容加看板截图

### L6 BT-14 三层架构深化 ✅ P1
- 真实 LLM 抽取(raw → citations 走 LLM 不用规则)
- 评估 LLM 抽取质量(Codex 评审 + 王老师审)
- 写"L2.7 LLM 抽取 v1.0" 工具

---

## 🎯 王老师单一推荐路径

| 优先级 | L 单元 | 推荐 |
|---|---|---|
| ⭐ P0 | L2 模式 v2.0 v3.0 多 PJ 同步 | 强烈推荐(全局价值)|
| ⭐ P0 | L3 codex login 切换 | 强烈推荐(质量门禁)|
| ⭐ P0 | L4 Web Clipper 端到端 | 强烈推荐(王老师用) |
| ✅ P1 | L5 看板 v3 移动端 | 推荐(用户体验) |
| ✅ P1 | L6 BT-14 LLM 抽取 | 推荐(架构深化) |
| ⚠️ P3 | (备选) 其他探索 | 暂缓 |

**王老师单一推荐**:L2 → L3 → L4 → L5 → L6 顺序推进(每个 L 都让王老师先审 +决策)。

---

## 📂 Sprint 24 文档结构

```
04-复盘与决策/
├── Sprint24_v3.1.2-rc1_启动方案_v1.0.md  ← 本文档
├── Sprint23_v3.1.1-rc1_完整收尾报告v1.0.md  ← Sprint 23 总结
├── Sprint23_v3.1.1-rc1_BT-14三层架构设计v1.0.md  ← BT-14 设计
└── Sprint23_v3.1.1-rc1_启动方案v1.0.md  ← Sprint 23 启动
```

---

## 🛡 协议铁律

Sprint 24 继续遵守:

- v41 不擅自打 stable(只打 rc,等王老师拍板)
- v42 不虚假汇报(所有数字实测)
- v44 不擅自分配任务(L2-L6 等王老师逐个触发)
- 王老师 Superpower("继续"=自主推进,关键决策点=等王老师拍板)
- "只有 Codex 评审"原则(Codex 只 review,其他 Hermes)

---

## 📍 当前一句话位置

```
v3.1.2-rc1 | Sprint 24 | L1-tag+启动文档完成
🎯 王老师触发 L2/L3/L4(任何一项即可启动)
```

---

## 🚦 等王老师触发

| 触发项 | 当前状态 |
|---|---|
| **L2 模式 v2.0 v3.0 推广** | ⏸ 等王老师选目标 PJ |
| **L3 codex login** | ⏸ 等王老师跑 codex login |
| **L4 notebooklm login** | ⏸ 等王老师跑 notebooklm login |
| **L5 看板 v3 移动端** | ⏸ 等王老师触发 |
| **L6 BT-14 LLM 抽取** | ⏸ 等王老师触发 |

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**协议版本**:王老师 Superpower"A+B 全部执行" + 模式 v2.0
**下一里程碑**:王老师触发 L2/L3/L4 → Sprint 24 第一阶段正式开工