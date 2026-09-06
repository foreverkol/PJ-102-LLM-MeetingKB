# PJ-102 Sprint 22 详细推进方案 v1.0

> **模式**:v2.0(STATE.json 驱动 + 文档副作用)
> **真值源**:`STATE.json`(本方案随 STATE.json 更新而失效,以 STATE.json 为准)
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **王老师授权**:"按建议执行"

---

## 🎯 一句话目标

**Sprint 22 把 5 项决策点中的 3 项(DT-01 + CT-13B + 模式 v2.0 试用)从"等批"推进到"完成"**。

---

## 📊 当前状态(从 STATE.json 读取,实测 2026-09-06)

| 项 | 值 |
|---|---|
| 版本 | `3.1.0-stable` |
| 当前 Sprint | **Sprint 22**(M0-planning) |
| L1 测试 | **98 PASS / 3.45s** |
| Wiki 文件 | **351 个,BAD YAML 0** |
| 决策点待批 | **5 项**(DT-01 / AT-11 / CT-13B / BT-14 / ET-04) |
| P0 阻塞 | **DT-01 75 关系清单(等王老师批)** |
| 模式架构 | **v2.0(STATE.json 单一真值源,本 Sprint 试用)** |

---

## 🏗 推进架构:L1-L5 原子单元(替代 Sprint/M/T 三层嵌套)

### 原则

**每个 L = 最小可独立交付单元**,DoD 满足就 commit + 自动更新 STATE.json。

| L 级别 | 含义 | DoD 标准 | commit 频率 |
|---|---|---|---|
| **L1 文档** | 需求/设计/计划/复盘 | write_file + 实测 + commit | 每文档 1 commit |
| **L2 代码单文件** | 函数/类/模块 | 单测 PASS + commit | 每模块 1 commit |
| **L3 测试** | L1 单元测试套件 | `pytest -q` 100% PASS | 每测试文件 1 commit |
| **L4 集成** | 多模块协作 | 端到端 sample 跑通 + STATE.json 更新 | 每集成点 1 commit |
| **L5 发布** | tag / release | tag push + 文档全量同步 + STATE.json 冻结 | 每版本 1 commit |

### Sprint 22 任务分解(共 12 个 L 单元)

```
Sprint 22
├── [L4.1] DT-01 75 关系批量修复        [需 L1 文档:王老师批]
├── [L1.2] AT-11 浏览器 + API 选型      [等王老师确认]
├── [L4.3] CT-13B 阶段 A:解耦与抽象      [前置:无]
├── [L1.4] STATE.json v1 → v2 模式试用总结 [前置:L4.3]
├── [L3.5] state_to_md L1 测试           [前置:L1.4]
├── [L2.6] sync_state.py 反向同步脚本     [前置:L3.5]
├── [L3.7] sync_state L1 测试            [前置:L2.6]
├── [L1.8] Sprint 22 文档整理             [前置:L4.3]
├── [L4.9] Sprint 22 端到端验证           [前置:L1.8]
├── [L5.10] Sprint 22 tag (v3.1.1-rc1)   [前置:L4.9]
├── [L1.11] Sprint 22 复盘文档            [前置:L5.10]
└── [L1.12] Sprint 22 STATE.json 冻结    [前置:L1.11]
```

---

## 🚀 立即可执行的 3 步推进(本对话内)

### 步骤 1:**L4.1 DT-01 75 关系批量修复**

**前置**:王老师批 75 关系清单(STATE.json `pending_decisions[0].next_step`)

**DoD**:
- [ ] 75 个 persons/*.md 的 `relationship` 字段全部填充(非空)
- [ ] `python3 03-执行/code/t01_fix_persons_relationship.py --apply` 退出 0
- [ ] `python3 -m pytest 03-执行/tests/unit/test_t01_fix_persons.py -q` 全 PASS
- [ ] `git commit -m "fix(t01): 批量应用 75 relationship"` 落地
- [ ] STATE.json 更新:`pending_decisions[0]` 移入 `completed_decisions` 数组

**预计耗时**:30 分钟(纯脚本执行)

### 步骤 2:**L4.3 CT-13B 阶段 A:解耦与抽象**

**前置**:无(已在 T-13B 启动分析 v1.0 明确范围)

**DoD**:
- [ ] `obsidian_export.py` 的所有硬编码 `/mnt/d/BaiduSyncdisk/...` → `argparse` 或 `PJ102_PROJECT_ROOT` 环境变量
- [ ] `obsidian_export.py` 加 `if __name__ == "__main__":` 入口
- [ ] `python3 -m obsidian_export --help` 打印完整用法
- [ ] `grep -rn "/mnt/d/BaiduSyncdisk" 03-执行/code/obsidian_export.py` 输出 0 条
- [ ] 现有 `test_obsidian_export.py` 全 PASS
- [ ] 新增 `test_obsidian_export_cli.py`(测试 CLI 入口)
- [ ] 跑 1 个 sample 真实端到端:CLAUDE.md 生成内容与硬编码版一致
- [ ] `git commit -m "refactor(t13b-a): obsidian_export 路径 argparse 化 + CLI 入口"`

**预计耗时**:3 天(实测可能更短,因为脚本规模小)

### 步骤 3:**L1.4 STATE.json v1 → v2 模式试用总结**

**前置**:Sprint 22 第 1 周结束(预计 7 天后)

**DoD**:
- [ ] 王老师跑了 DT-01 + CT-13B 后,验证 STATE.json 是否反映实际状态
- [ ] 写 `04-复盘与决策/Sprint22_STATE.json试用复盘_v1.0.md`(≤ 200 行)
- [ ] 评估 3 个关键问题:
  1. STATE.json 字段够不够?
  2. state_to_md.py 输出是否清晰?
  3. 是否需要 git hook?
- [ ] 决定是否进入 Sprint 23 模式 v2.0 全面推广

**预计耗时**:1 小时(文档)

---

## 📅 Sprint 22 时间表(4 周 = 20 工作日)

| 周 | 工作 | 产出 | 验收 |
|---|---|---|---|
| **W1**(本周) | 王老师批 75 → DT-01 闭环 | 75 个 person 文件更新 | L1 测试 98 PASS |
| **W1 末** | state_to_md.py 实测 | STATE.md 自动反映新状态 | `--check` 一致 |
| **W2** | CT-13B 阶段 A | obsidian_export.py CLI 化 | L3 测试 + 1 sample 端到端 |
| **W3** | CT-13B 阶段 B + C | npm 包 + 集成验证 | `npx pj102-...` 可调用 |
| **W4** | Sprint 22 收尾 | tag v3.1.1-rc1 + STATE.json 冻结 | v41 合规 + L3 全 PASS |
| **W4 末** | Sprint 22 复盘 + Sprint 23 启动 | 复盘文档 + STATE.json 进入 Sprint 23 | 模式 v2.0 决策 |

---

## 🎓 与 Superpower 元方法论对应

| 元方法论 | Sprint 22 对应 |
|---|---|
| 阶段 1:需求 | STATE.json `pending_decisions` + `do_now` |
| 阶段 2:设计 | STATE.json `mode_architecture` 字段 |
| 阶段 3:编码 | L2.6 sync_state.py + L4.3 obsidian_export CLI |
| 阶段 4:测试 | L3.5/3.7 state_to_md/sync_state L1 测试 |

---

## 🛡 协议遵守

- ✅ v41 不擅自打 stable tag → Sprint 22 末 v3.1.1-rc1 由王老师拍板升 stable
- ✅ v42 不虚假汇报 → STATE.json 所有数字脚本实测
- ✅ v44 不擅自分配任务 → DT-01/AT-11/CT-13B 启动条件均需王老师确认

---

## 🚦 等待王老师触发

| 触发项 | 当前状态 | 触发后 |
|---|---|---|
| **批 DT-01 75 关系清单** | JSON 文件就位 | L4.1 立即执行 |
| **确认 AT-11 浏览器 + API** | 待回复 | L1.2 启动 |
| **Sprint 22 模式 v2.0 试用反馈** | 本周跑完反馈 | 决定是否进 Sprint 23 |

---

## 📂 相关文件

- `STATE.json` — 单一真值源(本方案的依据)
- `STATE.md` — 自动生成的视图(STATE.json 改了跑 `state_to_md.py`)
- `scripts/state_to_md.py` — 自动生成器
- `04-复盘与决策/模式v2.0_STATE.json单一真值源.md` — 模式设计文档
- `04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-13B-atomicstrata-npm化启动分析_v1.0.md` — CT-13B 范围
- `04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-01-75建议清单_待王老师审_v1.0.json` — DT-01 待批

---

**生成**:Hermes Agent(MiniMax-M3)2026-09-06
**协议版本**:王老师 Superpower"按建议执行"协议 + 模式 v2.0
**下一里程碑**:王老师批 DT-01 → L4.1 执行 → STATE.json 自动更新