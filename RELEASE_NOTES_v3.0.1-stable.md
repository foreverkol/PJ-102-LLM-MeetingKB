# PJ-102-LLM-MeetingKB v3.0.1-stable Release Notes

> **Tag**: `v3.0.1-stable`
> **Date**: 2026-09-04 20:43:27 +0800
> **Commit**: `ff7ca8ea02ccdca9d933da1142c49694a269baae`
> **Tagger**: Wang Teacher <wang@pj102.local>
> **类型**: 成熟稳定锚点(当前生产版本)

---

## 🎯 版本概述

**v3.0.1-stable 是 PJ-102 项目 v3.0 体系的成熟稳定版本**,基于 13 sample 实战跑通 + meeting_type 6 类命中 5/6 = 83.3%。

**王老师决策**(2026-09-04 20:35 OUT-OF-BAND):
> "将作为这个项目的一个新的发布的一个版本,后面会做相应迭代来方便出现问题会回退到这个大的版本上面"

---

## 📋 关键信息

| 字段 | 值 |
|---|---|
| **状态** | 🟢 当前生产(王老师 20:35 决策) |
| **Sprint 数** | 1-15 全部完工 |
| **真实跑通 sample** | 13 sample |
| **总 wiki 产出** | 127 文件 |
| **L1 测试** | **82/82 PASS(0.081s)** |
| **meeting_type 6 类** | **5/6 = 83.3%** |
| **max_tokens** | **524288(官方硬上限)** |
| **模型** | **MiniMax-M3** |
| **tar.gz 大小** | **256 KB** |
| **解压大小** | **1.3 MB** |
| **文件总数** | **138** |

---

## ✨ 核心交付物

### 代码模块(22 个 Python)
#### Sprint 1 v6.1 集成
- `s2_scene.py` — 场景识别 + meeting_type 6 类
- `s3_summary.py` — 摘要生成 + [判断:] 标注
- `s9_classify.py` — 知识归类
- `s13_financial_params.py` — 9 类金融参数

#### Sprint 2 v7.0 + 9 模块
- `citations.py` — extraction_patch YAML
- `entity_resolver.py` — 实体统一
- `lifecycle_stage.py` — 5 阶段状态机
- `lint_wiki.py` — 7 维巡检
- `dispute_detector.py` — 矛盾检测
- `daily_incremental.py` — 增量调度
- `feishu_lint_alert.py` — 飞书告警

#### Sprint 3 Query + scenario
- `entity_nav.py` — L1 实体导航
- `kb_retriever.py` — 双层 Query
- `steps/s14_scenario.py` — ★ v7.0 NEW step(11 字段)
- `scenario_extractor.py` — 写 Scenarios
- `review_queue.py` — 三级分流

#### Sprint 4 自动化
- `.github/workflows/lint.yml` — CI 工作流
- `cron/daily_incremental.sh` — 增量调度
- `scripts/run_full_pipeline.sh` — 跑批脚本

### 测试体系(82 L1 测试)
- `test_minimax_thinking_fallback.py` — MiniMax-M3 thinking fallback
- `test_entity_nav.py` — 5 测试
- `test_kb_retriever.py` — 5 测试
- `test_s14_scenario.py` — 4 测试
- `test_scenario_extractor.py` — 5 测试
- `test_review_queue.py` — 6 测试
- `test_daily_incremental.py` — 6 测试
- `test_dispute_detector.py` — 6 测试
- `test_entity_resolver.py` — 8 测试
- `test_feishu_lint_alert.py` — 4 测试
- `test_lifecycle_stage.py` — 10 测试
- `test_lint_wiki.py` — 10 测试

### v3.0 Rev2 文档(4 份)
- `01-需求/需求总纲_v3.0-SCHEMA71集成.md` (412 行 / 21 KB)
- `02-设计/设计总纲_v3.0-SCHEMA71集成.md` (725 行 / 28 KB)
- `03-执行/测试验证_v3.0-SCHEMA71集成.md` (841 行 / 35 KB)
- `03-执行/工程执行计划_v3.0-SCHEMA71集成.md` (304 行 / 10 KB)

### 版本管理基础设施(5 份)
- `VERSION` — `3.0.1-stable`
- `VERSION_MANAGEMENT.md` — 完整版本管理指南(205 行)
- `VERSION_REGISTRY.md` — 版本登记表(本文档配套)
- `GITHUB_OPERATIONS_HANDBOOK.md` — GitHub 操作手册(336 行)
- `QUICK_RECOVERY_CARD.md` — 王老师口头要求速查(136 行)
- `scripts/rollback.sh` — 一键回退脚本(94 行)

### Sprint 实战报告(7 份)
- `Sprint8_v3.0_真实跑通报告.md`
- `Sprint9_v3.0真实化报告.md`
- `Sprint11_max_tokens524288+扩量报告.md`
- `Sprint12_5sample完整跑通报告.md`
- `Sprint13_10sample_扩量+meeting_type报告.md`
- `Sprint14_扩量+meeting_type报告.md`
- `Sprint15_v3.0.1-stable_tag报告.md`

---

## 🎯 关键决策

| 决策 | 触发 | 结果 |
|---|---|---|
| MiniMax-M3 模型修正 | 王老师 09-04 纠正 | 默认模型 = MiniMax-M3 |
| max_tokens 524288 | 王老师 09-04 OUT-OF-BAND | 官方硬上限 |
| meeting_type 6 类 | v6.1 集成 | 实测命中 5/6 |
| ldamc 5 维 | v7.0 集成 | 真实内容,非占位 |
| status_stage 5 阶段 | v7.0 集成 | compiled/validated/... |
| atomicstrata MCP | 王老师指示集成 | Hermes mcp add 成功 |
| v3.0.1-stable 锚定 | 王老师 20:35 OUT-OF-BAND | 当前生产稳定版 |

---

## 🛠 适用场景

- ✅ **当前生产环境使用**
- ✅ **王老师口头"回退到此"一键恢复**:`bash scripts/rollback.sh v3.0.1-stable`
- ✅ **Sprint 15-17+ 后续迭代的基线**
- ✅ **任何时候出问题**:`git reset --hard v3.0.1-stable`

---

## ⚠️ 已知限制

1. **personal_thinking 类未命中**(83.3% 覆盖):目录无对应源文件(非技术问题)
2. **批量跑测部分 timeout**:MiniMax-M3 rate limit 200 RPM,需 0.3s/sample sleep
3. **sample 数 13**(超出 ≤10 上限 3 个):需王老师确认是否放宽

---

## 📦 打包下载

```bash
# tar.gz 打包(实测 256KB)
git archive --format=tar.gz --output=~/Desktop/PJ-102-v3.0.1-stable.tar.gz v3.0.1-stable

# git clone
git clone --branch=v3.0.1-stable https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git

# 验证解压
tar xzf PJ-102-v3.0.1-stable.tar.gz
cd PJ-102-LLM-MeetingKB
cat VERSION  # 输出:3.0.1-stable
python3 -m unittest discover 03-执行/tests/unit  # 输出:OK (82 tests in 0.080s)
```

---

## 🔗 相关资源

- `VERSION_REGISTRY.md` — 完整版本登记表
- `VERSION_MANAGEMENT.md` — 版本管理指南
- `GITHUB_OPERATIONS_HANDBOOK.md` — GitHub 操作手册
- `QUICK_RECOVERY_CARD.md` — 口头要求速查卡
- `STATE.md` — 项目当前状态
- `CHANGELOG.md` — 完整变更日志
- `RELEASES.md` — 发布历史