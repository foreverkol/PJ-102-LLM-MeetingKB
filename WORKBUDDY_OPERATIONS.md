# PJ-102-LLM-MeetingKB · workbuddy 接入操作手册

> **本手册给王老师您**（人工操作）
> **目标**: 在 Windows 本地部署 workbuddy，让它复制 PJ-102 全部能力

---

## 📋 前置准备清单

王老师在开始前准备：

### 1. workbuddy 安装（Windows 本地）

- ✅ 已安装腾讯 workbuddy 客户端
- ✅ 知道 workbuddy 的工作目录
- ✅ workbuddy 已配置 Python 环境（如未配置，可让 workbuddy 自行下载）

### 2. 项目可访问性

- ✅ GitHub 账号 foreverkol 可访问
- ✅ PJ-102 仓库地址：`https://github.com/foreverkol/PJ-102-LLM-MeetingKB`
- ✅ 可下载 Release 包：`https://github.com/foreverkol/PJ-102-LLM-MeetingKB/releases/tag/v1.0.0`

### 3. LLM API Key

- ✅ 已获取 MiniMax M3 API key（key 长度 > 100）
- ✅ 或 DeepSeek / OpenAI / Anthropic 的 API key

---

## 🚀 5 阶段操作流程

### 阶段 1：让 workbuddy 克隆项目（5 分钟）

打开 workbuddy，输入下方"阶段 1 提示词"。

### 阶段 2：让 workbuddy 阅读核心文档（15 分钟）

输入下方"阶段 2 提示词"。

### 阶段 3：让 workbuddy 配置环境（10 分钟）

输入下方"阶段 3 提示词"。

### 阶段 4：让 workbuddy 复制源文件 + 跑批（30 分钟）

输入下方"阶段 4 提示词"。

### 阶段 5：让 workbuddy 运行全量（9 小时后台，可选）

输入下方"阶段 5 提示词"。

---

## 🔧 关键修复（必须告诉 workbuddy）

1. **MiniMax base_url 必须是 `api.minimaxi.com`**（不是 `api.minimax.chat`）
2. **端点路径 `/text/chatcompletion_v2`**（不带 /v1 前缀）
3. **Python 相对 import 用绝对路径**

## 🎯 王老师决策

### 选项 A：直接给 workbuddy 提示词（推荐）
- 复制下方"完整提示词"
- 粘贴到 workbuddy
- 让它自动执行

### 选项 B：分阶段给提示词
- 一次只给一个阶段
- 验证后再给下一个

### 选项 C：让 workbuddy 完全自主
- 一次性给完整提示词
- 让它自己决定如何执行

我推荐**选项 A**——结构化提示词最适合 workbuddy 类工具。

---

## 📋 详细提示词见：`WORKBUDDY_PROMPTS.md`

本文件包含完整操作手册，配套的提示词文件在 `WORKBUDDY_PROMPTS.md`。
