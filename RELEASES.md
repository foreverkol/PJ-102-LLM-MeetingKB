# 发布历史

## v1.0.0 (2026-09-03)

### 🎉 首次发布

**核心功能**：
- ✅ 12 步 LLM Pipeline（S1-S12）
- ✅ MiniMax M3 真实调用（中国区 api.minimaxi.com）
- ✅ 5 类 WIKI 产出（meeting 为主）
- ✅ 4 个 LLM Provider 支持（minimax/deepseek/openai/anthropic）
- ✅ JSON 容错解析
- ✅ 自动重试 + 限流处理

**项目统计**：
- Python 文件：16 个
- 文档：30+ 份
- WIKI 样本：10 个（实测跑通）
- 测试：9 个（烟雾测试）

**性能**：
- 平均 135.8 秒/文件
- 成功率 100%
- 1 次自动重试成功

### 修复
- MiniMax 中国区 base_url（api.minimax.chat → api.minimaxi.com）
- 端点路径（去掉 /v1 前缀）
- Python 相对 import 问题
- PROJECT_ROOT 路径计算问题

### 王老师认可
> meetings 质量非常不错（v1.0 13/13 验证）

## 版本管理

本项目使用 [PJ-902-09-Git学习与实践](../PJ-902-AI重要工具深度应用与实践/PJ-902-09-Git学习与实践/) 提供的版本管理规范。

### 常用命令
```bash
# 查看版本
./scripts/version_manager.sh info

# 列出所有版本
./scripts/version_manager.sh list

# 创建新版本
./scripts/version_manager.sh create v1.0.1 "修复 xxx"

# 一键回退
./scripts/rollback.sh v1.0.0

# 验证项目
./scripts/verify_version.sh
```
