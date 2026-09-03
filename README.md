# PJ-102-LLM-MeetingKB

<div align="center">

![Build Status](https://img.shields.io/github/actions/workflow/status/foreverkol/PJ-102-LLM-MeetingKB/test.yml?branch=main&style=flat-square)
![Release](https://img.shields.io/github/v/release/foreverkol/PJ-102-LLM-MeetingKB?style=flat-square)
![License](https://img.shields.io/github/license/foreverkol/PJ-102-LLM-MeetingKB?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)
![Code style](https://img.shields.io/badge/code%20style-black-000000?style=flat-square)
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow?style=flat-square)

基于 LLM 真实调用（MiniMax M3）+ 12 步 pipeline 的会议转写→知识库全流程处理

</div>

---

## 🎯 一句话定位

**完全独立**的会议转写→知识库处理系统，使用 LLM 真实调用（默认 MiniMax M3）+ 12 步 pipeline。

## ✨ 核心特性

- ✅ **12 步全流程**：基础信息 → 场景识别 → FJV → 隐性知识 → 实体 → 决策 → 风险 → 知识归类 → 认知提炼 → 价值评级 → WIKI 落地
- ✅ **LLM 真实调用**：MiniMax M3（中国区 api.minimaxi.com）
- ✅ **5 类 WIKI 产出**：meeting / person / concept / judgment / comparison
- ✅ **完全独立**：零依赖其他项目
- ✅ **自动化发布**：release-please + Conventional Commits
- ✅ **生产级质量**：王老师认可 13/13 样本验证

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
cd PJ-102-LLM-MeetingKB

# 配置
cp config/.env.example .env
# 编辑 .env，填入 MINIMAX_API_KEY

# 跑批
cd 03-执行/code
python pipeline.py --limit 10
```

详细使用说明：[培训材料/使用手册_v1.0.md](./培训材料/使用手册_v1.0.md)

## 📋 项目状态

| 维度 | 状态 |
|---|---|
| 当前版本 | v1.0.0 |
| WIKI 产出 | 10+ 个 meetings |
| 烟雾测试 | 9/9 通过 |
| 自动化 | release-please + GitHub Actions |

## 🤖 workbuddy 接入

如需 workbuddy AI Agent 接入，请阅读：
- [WORKBUDDY_GUIDE.md](./WORKBUDDY_GUIDE.md) - 接入指南
- [WORKBUDDY_OPERATIONS.md](./WORKBUDDY_OPERATIONS.md) - 操作手册
- [WORKBUDDY_PROMPTS.md](./WORKBUDDY_PROMPTS.md) - 提示词

## 📚 文档

- [需求总纲](./01-需求/需求总纲_v1.0.md)
- [系统架构](./02-设计/系统架构_v1.0.md)
- [12 步 Pipeline 详细设计](./02-设计/12步Pipeline详细设计_v1.0.md)
- [使用手册](./培训材料/使用手册_v1.0.md)
- [FAQ](./培训材料/FAQ_v1.0.md)
- [CHANGELOG](./CHANGELOG.md)

## 🔒 安全

详见 [SECURITY.md](./SECURITY.md)。

## 🤝 贡献

提交 PR 前请阅读：
- [PR 模板](./.github/pull_request_template.md)
- [Issue 模板](./.github/ISSUE_TEMPLATE/)

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

---

**王老师认可质量**：meetings 质量非常不错（v1.0 13/13 验证）

**v1.0.0** · 2026-09-04 · 专业级自动化 GitHub 管理


<!-- test-release-please-marker: 测试 release-please 自动化 -->
