# 更新日志

## v1.0 (2026-09-03)

### 🎉 首次发布

**核心功能**：
- ✅ 12 步 LLM Pipeline（S1-S12）
- ✅ MiniMax M3 真实调用（中国区）
- ✅ 5 类 WIKI 产出（meeting 为主）
- ✅ 4 个 LLM Provider 支持（minimax/deepseek/openai/anthropic）
- ✅ JSON 容错解析
- ✅ 自动重试 + 限流处理

**文档**：
- ✅ 5 份需求文档
- ✅ 7 份设计文档
- ✅ 5 份复盘与决策文档
- ✅ 3 份培训材料
- ✅ 4 份顶层入口文档
- ✅ 3 份配置文件

**测试**：
- ✅ 9 个烟雾测试（全过）
- ✅ 10 个样本实测跑通（王老师认可质量）

**性能**：
- 平均 135.8 秒/文件
- 成功率 100%
- 1 次自动重试成功

### 🔧 修复

- MiniMax 中国区 base_url 修复（api.minimaxi.com）
- 端点路径修复（/text/chatcompletion_v2）
- Python 相对 import 修复
- PROJECT_ROOT 路径计算修复

### 📦 项目统计

- Python 文件：16 个
- 文档：30+ 份
- WIKI 样本：10 个
- 测试：9 个
- 总文件数：~70 个
