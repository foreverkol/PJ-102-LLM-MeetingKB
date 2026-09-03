# PJ-102-LLM-MeetingKB

> **项目编号**: PJ-102
> **项目名称**: LLM MeetingKB (基于 LLM 的会议知识库)
> **创建日期**: 2026-09-03
> **当前版本**: v1.0
> **状态**: ✅ 已跑通（13/13 MiniMax M3 验证）

## 一句话定位

基于 LLM 真实调用（MiniMax M3）+ 12 步 pipeline + MiniMax M3 的会议转写→知识库全流程处理，**完全独立**的项目，不依赖 PJ-001 任何子项目。

## 核心特性

- ✅ 12 步全流程（基础信息 → 场景识别 → FJV → 隐性知识 → 实体 → 决策 → 风险 → 知识归类 → 认知提炼 → 价值评级 → WIKI 落地）
- ✅ LLM 真实调用（MiniMax M3 中国区）
- ✅ 5 类 WIKI 产出（meeting / person / concept / judgment / comparison）
- ✅ 完全独立（零依赖 PJ-001-07 / PJ-001-08 / PJ-001-111）
- ✅ 旧 WIKI 不移植（重新生成）

## 目录结构

```
PJ-102-LLM-MeetingKB/
├── 01-需求/           需求文档（5 项）
├── 02-设计/           设计文档（6 项）
├── 03-执行/           代码与测试
├── 04-复盘与决策/      状态与运维
├── system/           系统目录（源文件 / state / logs / out）
├── registry/         registry.db
├── cron/             调度脚本
├── tests/            测试（unit / e2e）
├── config/           配置文件
├── 培训材料/          使用手册
└── 培训材料/          FAQ
```

## WIKI 输出

```
/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/
├── meetings/     （meeting WIKI）
├── persons/       （person WIKI）
├── concepts/      （concept WIKI）
├── judgments/     （judgment WIKI）
└── comparisons/   （comparison WIKI）
```

## 快速开始

```bash
# 1. 设置环境变量
export MINIMAX_API_KEY="..."
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"

# 2. 跑批
cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code
python3 pipeline.py --limit 13 --write
```

## 王老师认可

> meetings 质量非常不错（v1.0 13/13 跑通）
