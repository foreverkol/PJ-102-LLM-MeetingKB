# PJ-102-LLM-MeetingKB · 版本登记表

> **生成时间**:2026-09-06
> **当前稳定版本**:**v3.1.0-stable**(王老师拍板)
> **历史稳定版本**:v3.0.1-stable, v1.0.0
> **协议版本**:v41(不擅自打 stable tag) + v42(实测说话) + v44(不擅自分配任务)

---

## 📊 版本总表

| 版本 | 类型 | tag commit | date | 状态 | 王老师拍板 |
|---|---|---|---|---|---|
| **v1.0.0** | 全项全量移植 | (备份未显式 commit) | 2026-09-03 | archived | ✅ |
| **v1.1.0** | 4 类 wiki 补全 | (备份未显式 commit) | 2026-09-03 | archived | ✅ |
| **v3.0.0** | v3.0 主版本 | `364b719` | 2026-09-04 | archived | ✅ |
| **v3.0.1-stable** | 成熟稳定锚点 | `ff7ca8e` | 2026-09-04 | previous | ✅ |
| **v3.0.2-stable** | Karpathy 对齐 | `cfd3954` | 2026-09-04 | archived | ✅ |
| **v3.0.3-stable** | Karpathy P1 全套 | `2d8b375` | 2026-09-05 | archived | ✅ |
| **v3.1.0-rc1** | Sprint 21 RC | `db7011d` | 2026-09-05 | previous-rc | ✅(auto, v41 允许) |
| **v3.1.0-stable** | **Sprint 21 完整闭环** | **(本版本)** | **2026-09-06** | **🟢 current** | ✅ |

---

## 🔄 版本对比表

| 维度 | v3.0.1-stable | v3.1.0-rc1 | **v3.1.0-stable** |
|---|---|---|---|
| Sprint 数 | 1-15 | 1-21 (M0-M3) | **1-21 (M0-M5)** |
| 测试 | 82 PASS | 98 PASS | **98 PASS** |
| Wiki 文件 | 127 | 351 | **351** |
| BAD YAML | 0 | 11(Codex H1) | **0(本版本修复)** |
| meeting_type | 5/6 = 83.3% | 5/6 = 83.3% | **5/6 = 83.3%** |
| Codex 评审 | - | 1 次(8.5/10) | **3 次 + M5 校准(7.5/10)** |
| Karpathy 对齐 | - | Karpathy 路线 | **Karpathy + Obsidian 双核心** |
| 5 项决策点 | - | 待启动 | **状态卡片化,等 Sprint 22** |
| 王老师决策依赖 | - | v3.1.0-stable 拍板 | **✅ 已拍板** |

---

## 📅 时间线

```
2026-09-03 → v1.0.0 release(全项全量移植)
2026-09-03 → v1.1.0 release(4 类 wiki 补全)
2026-09-04 → v3.0.0 release(主版本)
2026-09-04 → v3.0.1-stable(王老师拍板,生产稳定)
2026-09-04 → v3.0.2-stable(Karpathy 对齐)
2026-09-05 → v3.0.3-stable(Karpathy P1 全套)
2026-09-05 → Sprint 21 启动(王老师 OUT-OF-BAND)
2026-09-05 → v3.1.0-rc1(M0-M3 + Superpower)
2026-09-06 → Codex 三次评审 + M5 校准(7.5/10)
2026-09-06 → E 选项执行:11 YAML 修复 + 拍板邀请
2026-09-06 → v3.1.0-stable 拍板(本版本)✅
```

---

## 🛠 版本管理命令速查

```bash
# 查看所有 tag
git tag -l -n1

# 当前版本
cat VERSION  # 3.1.0-stable

# 一键回退到 v3.1.0-stable
bash scripts/rollback.sh v3.1.0-stable

# 一键回退到 v3.0.1-stable
bash scripts/rollback.sh v3.0.1-stable

# 打包当前版本
git archive --format=tar.gz \
  --output=~/Desktop/PJ-102-v3.1.0-stable.tar.gz \
  v3.1.0-stable

# 验证
python3 -m pytest 03-执行/tests/unit/ -q
# 期望输出:98 passed in 3.47s
```

---

## 📋 决策点状态(本版本不包含)

| 决策项 | 版本依赖 | 启动方式 |
|---|---|---|
| T-01 75 relationship | v3.1.0-stable | 等王老师批 75 建议清单 |
| T-11 Web Clipper | v3.1.0-stable | 等王老师确认浏览器 + API |
| T-13B atomicstrata npm 化 | v3.1.0-stable | Sprint 22 启动 |
| T-14 三层架构 | v3.1.0-stable | Sprint 23+ 评估 |
| T-04 organization | v3.1.0-stable | 等 PJ-201 数据 |

---

## 🔗 相关文档

- `VERSION_MANAGEMENT.md` — 版本管理详细指南
- `STATE.md` — 项目当前状态
- `CHANGELOG.md` — 完整变更日志
- `RELEASES.md` — 发布历史
- `RELEASE_NOTES_v3.0.1-stable.md` — 上一个 stable 版本发布说明
- `RELEASE_NOTES_v3.1.0-stable.md` — **本版本发布说明**
- `04-复盘与决策/E选项_执行报告_v1.0.md` — 拍板依据