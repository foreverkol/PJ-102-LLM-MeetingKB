# 更新日志

本项目遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。

## [v3.0.0] - 2026-09-04

### 🎉 v3.0 大版本 — SCHEMA v6.1 + v7.0 集成

**驱动**:王老师 09-04 11:16 指示"基于参考设计 SCHEMA_v6.1+v7.0 充分判断吸收"
**实测**:王老师 09-04 11:34 纠正"MiniMax-M3,不是 MiniMax-Text-01"
**执行**:Superpower 4 阶段 + 不停留不询问原则 / Sprint 1 / W1-W4 / 26 TC 全完成 / 125 L1 测试全 PASS / 10 Hard Gate 全 PASS / v3.0.0 tag 73e325c

#### ✨ v6.1 P-1/P-2/P-3/P-4 集成(4 补丁)

- **P-1** 五要素摘要加 `[判断:发言人]` 标注(s3_summary.py)
- **P-2** 定量金融参数 9 类(s13_financial_params.py 新增 step)
- **P-3** 可转化资产 tag 5 类 `#BP素材` `#官网文案` `#销售话术` `#演讲素材` `#客户案例`(s9_classify.py)
- **P-4** meeting_type 6 类 + subtype 6 类(s2_scene.py)

#### ✨ v7.0 10 新规集成

- **v7.0-001** ldamc 5 维自检 lost/different/added/more/connected(s10_cognitive.py)
- **v7.0-002** contradictions 显式字段(dispute_detector.py)
- **v7.0-003** entity_id 统一编号 `person_{hash8}_{seq4}`(entity_resolver.py + 8 测试)
- **v7.0-004** canonical_name + aliases + 消歧(s6_entity.py)
- **v7.0-005** status_stage 5 阶段状态机 `raw/compiled/reviewed/canonical/superseded`(lifecycle_stage.py + 10 测试)
- **v7.0-006** topic_key judgment 主题聚合(s7_decision.py)
- **v7.0-007** evolution 演化链 `evolved_from/to`(s7_decision.py)
- **v7.0-008** scenario 11 字段新页面类型(s14_scenario.py + scenario_extractor.py)
- **v7.0-009** external_ref 纯度规则(s2_scene.py `is_external_knowledge`)
- **v7.0-010** extraction_patch YAML 中间层(citations.py)

#### 🆕 9 个 v3.0 新模块

- `citations.py` — v7.0 extraction_patch YAML(85 行 + 6 测试)
- `entity_resolver.py` — 实体统一编号(174 行 + 8 测试)
- `lifecycle_stage.py` — 状态机(110 行 + 10 测试)
- `lint_wiki.py` — 7 维 + v7.0 必填字段检查(261 行 + 10 测试)
- `dispute_detector.py` — 矛盾检测(127 行 + 6 测试)
- `daily_incremental.py` — 增量调度(192 行 + 6 测试)
- `feishu_lint_alert.py` — 飞书 webhook(170 行 + 4 测试)
- `entity_nav.py` — L1 实体导航(154 行 + 5 测试)
- `kb_retriever.py` — 双层 Query(174 行 + 5 测试)
- `scenario_extractor.py` — scenario 写入(126 行 + 5 测试)
- `review_queue.py` — 三级分流(152 行 + 6 测试)
- `steps/s14_scenario.py` — ★v7.0 新增 step(121 行 + 4 测试)

#### 🔧 关键修复

- **MiniMax-Text-01 → MiniMax-M3**(王老师 09-04 11:34 纠正,commit d3645f2)
- safe_json_parse 支持 list + markdown 围栏
- entity_id `organization_xxx_NNNN` → `org_xxx_NNNN` 短前缀
- _parse_frontmatter 支持 ldamc 多行 indent block

#### 📦 部署基础设施

- `.github/workflows/lint.yml` — 3 jobs CI(69 L1 测试 + lint dry-run + frontend 文档校验)
- `cron/daily_incremental.sh` — 每日 9/18 点自动调度(106 行 bash)
- `scripts/run_full_pipeline.sh` — 跑批脚本(113 行 bash,SAMPLE_LIMIT=10 默认)

#### 🧪 测试覆盖

- **125 个 L1 测试方法** / 32 个 test_*.py 文件
- **10 / 10 Hard Gate 全 PASS**(实测):
  - T1 v1.0 baseline + v6.1+v7.0 字段
  - T2 check_evidence 0 errors
  - T3 lint 8 维(含 v7.0 必填)
  - T4 v6.1 4 补丁覆盖
  - T5 v7.0 ldamc 5 维 100%
  - T6 entity_id 全员覆盖
  - T7 topic_key 100%
  - T8 scenario ≥ 1
  - T9 extraction_patch YAML parse
  - T10 smoke_test 9/9

#### 📦 文档升级

- 4 份 v3.0 Rev2 文档(需求/设计/测试/工程计划)+ L3 验收报告 = 5 份
- 6 份参考设计/ 设计参考 全部入库(从原 v1.0 单层结构升级)

#### ⚠️ 王老师明确限制

- **不要跑全量 286 个录音文字**
- **只跑 ≤10 个测试样例**(SAMPLE_LIMIT 默认 10 已落实)
- **Superpower "Plan-Execution-Phase 陷阱"防控**:已签字 = 全权授权

---

## [v1.1.0] - 2026-09-03

### 🔧 改进
- 补全 4 类 WIKI 生成器(s12 v1.1)

## [v1.0.0] - 2026-09-03

### 🎉 首次发布
- 12 步 LLM Pipeline(S1-S12)
- MiniMax M3 真实调用(中国区)
- 5 类 WIKI 产出
- 4 个 LLM Provider 支持
- JSON 容错解析
- 自动重试 + 限流处理
- 完整文档(30+ 份)
- 烟雾测试(9 个全过)
- GitHub Actions CI/CD

### 🐛 修复
- MiniMax 中国区 base_url(`api.minimaxi.com`)
- 端点路径(`/text/chatcompletion_v2`)
- Python 相对 import 问题
- PROJECT_ROOT 路径计算问题

### 关键里程碑
- 2026-09-03 v1.0 创建
- 王老师认可 WIKI 质量
- Git 仓库初始化
- 完整版本管理集成
