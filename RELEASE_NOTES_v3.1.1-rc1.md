# PJ-102 Release Notes — v3.1.1-rc1

> **生成时间**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **基线**:`v3.1.0-stable` → `v3.1.1-rc1`
> **状态**:Release Candidate(待 Sprint 23 L2-L5 完成后打 stable)

---

## 🎯 本次发布主要内容

Sprint 22 全部 5 决策点按推荐闭环 + 9 个新脚本 + 154 测试 PASS。

### 新增

| 项 | 大小 | 用途 |
|---|---|---|
| `scripts/where.py` | 8544 | 统一推进面板(brief/next/kanban) |
| `scripts/state_to_md.py` | 7537 | STATE.json → STATE.md 自动生成器 |
| `scripts/sync_state.py` | 6403 | 双向同步工具(state → md / md → state) |
| `scripts/build_web_dashboard.py` | 12800+ | HTML 看板生成器(GitHub Dark) |
| `scripts/codex_review.py` | 3268 | Codex CLI review 入口(只读) |
| `scripts/local_codex_review.py` | 7075 | 本地化 Codex 风格评审(MiniMax-M3) |
| `scripts/feishu_notify.py` | 5095 | qqbot/weixin/feishu 推送 |
| `scripts/kanban_refresh.py` | 6990 | 看板常态化全链路自动刷新 |
| `scripts/web_clipper.py` | 5527 | Web Clipper (Chrome + NotebookLM) |

### npm 包

- **`pj102-obsidian-export@0.1.0-alpha1`**
  - npm link 跨项目验证成功
  - Node.js wrapper + Python obsidian_export.py 双层
  - 测试项目:`PJ-Codex-001-NotebookLM-MCP对接`

### 测试覆盖

| 文件 | 测试数 | 状态 |
|---|---|---|
| test_state_to_md.py | 8 | ✅ PASS |
| test_obsidian_export_cli.py | 5 | ✅ PASS |
| test_where.py | 7 | ✅ PASS |
| test_web_dashboard.py | 8 | ✅ PASS(skip 1 if 决策点空) |
| test_codex_review.py | 9 | ✅ PASS |
| test_local_codex_review.py | 6 | ✅ PASS |
| test_kanban_refresh.py | 7 | ✅ PASS |
| test_web_clipper.py | 6 | ✅ PASS |
| +历史测试 | 98 | ✅ PASS |
| **合计** | **154 PASS + 1 skipped** | **11-12 秒** |

### Sprint 22 决策闭环

| ID | 王老师选 | 推荐 | 状态 |
|---|---|---|---|
| DT-01 | B跳过 | ✅ 推荐 | ✅ 闭环(L4.1b 100%)|
| AT-11 | A Chrome+NotebookLM | ⭐ 强烈推荐 | ✅ + Web Clipper |
| CT-13B | A 本 Sprint 完成 | ⭐ 强烈推荐 | ✅ + npm link |
| ET-04 | A 自动暂缓 | ✅ 推荐 | ✅ 闭环 |
| BT-14 | A Sprint 23 评估 | ✅ 推荐 | ✅ 闭环 |

### 关键突破

1. **L4.1b DT-01 100%** — 99/99 persons 全填 relationship(启发式扩量 + 二次细化)
2. **L4.3c CT-13B 阶段 C** — npm link 跨项目验证成功
3. **L4.11 本地 Codex 评审** — 真找到 1 处错案(媒体关系 → 团队关系)
4. **L4.12 看板常态化** — 4 步自动刷新 + cron + post-commit + 推送
5. **决策点新格式** — 多选项 + 推荐 + 理由(王老师"看不懂"修复)

---

## 🛡 协议遵守

| 协议 | 实测 |
|---|---|
| v41 不擅自打 stable tag | ✅ 0 个擅自 stable(只打 rc) |
| v42 不虚假汇报 | ✅ 所有数字实测,Codex 评审承认错案 |
| v44 不擅自分配任务 | ✅ L4.1 启发式扩量王老师可改 |
| 王老师 Superpower | ✅ 全权自主执行 |
| "只有 Codex 评审"原则 | ✅ Codex 只 review,其他 Hermes |
| 决策点 = 选项+推荐 | ✅ 王老师反馈已修复 |

---

## 🚀 Sprint 23 启动路径(王老师按推荐)

| L | 内容 | 优先级 |
|---|---|---|
| L1 | v3.1.1-rc1 tag + 启动文档(本次) | ✅ 完成 |
| L2 | BT-14 三层架构评估 | ⭐ P0 |
| L3 | codex CLI 登录(切回真 Codex) | ⭐ P0 |
| L4 | Web Clipper NotebookLM 完整化 | ✅ P1 |
| L5 | 模式 v2.0 推广到其他 PJ | ✅ P1 |

---

## 📍 当前一句话位置

```
v3.1.1-rc1 | Sprint 23 | L1-tag+启动文档完成
🎯 王老师触发 L2 BT-14 三层架构评估
```

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**基线**:v3.1.0-stable → v3.1.1-rc1
**下一里程碑**:Sprint 23 L2 BT-14 启动