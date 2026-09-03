# AGENT.md · PJ-102-LLM-MeetingKB

> 注意: 文件名是 AGENT.md（单数），不是 AGENTS.md（避免系统保护冲突）

## 项目身份

- **编号**: PJ-102
- **名称**: LLM MeetingKB
- **父项目**: null（独立项目）
- **创建日期**: 2026-09-03
- **当前版本**: v1.0
- **状态**: ✅ 跑通中（255 个全量）

## 一句话描述

基于 LLM 真实调用（MiniMax M3）+ 12 步 pipeline 的会议转写→知识库全流程处理，**完全独立**的项目。

## 核心结构

```
PJ-102-LLM-MeetingKB/
├── 01-需求/    需求文档（5 份）
├── 02-设计/    设计文档
├── 03-执行/code/    代码与测试
├── 04-复盘与决策/    状态与运维
├── system/                系统目录
├── registry/              registry.db
├── cron/                  调度脚本
├── tests/                 测试
├── config/                配置文件
├── 培训材料/              使用手册
└── 顶层入口
```

## 关键执行入口

| 任务 | 命令 |
|------|------|
| 跑全量 | `python3 pipeline.py` |
| 限制样本 | `python3 pipeline.py --limit 13` |
| 跳过 LLM | `python3 pipeline.py --no-llm` |
| 清空 WIKI | `python3 pipeline.py --clear` |

## 12 步 Pipeline

| 步骤 | 名称 | 文件 |
|---|---|---|
| S1 | 基础信息 | steps/s1_basic.py |
| S2 | 场景识别 | steps/s2_scene.py |
| S3 | 标准摘要 | steps/s3_summary.py |
| S4 | FJV 三分法 | steps/s4_fjv.py |
| S5 | 隐性知识 | steps/s5_implicit.py |
| S6 | 5 类实体 | steps/s6_entity.py |
| S7 | 决策+行动 | steps/s7_decision.py |
| S8 | 风险+盲区 | steps/s8_risk.py |
| S9 | 知识归类 | steps/s9_classify.py |
| S10 | 认知提炼 | steps/s10_cognitive.py |
| S11 | 价值评级 | steps/s11_value.py |
| S12 | WIKI 写入 | steps/s12_wiki.py |

## 关联项目（无）

- ❌ 不依赖任何 PJ-001 子项目

## 王老师评价

> meetings 质量非常不错