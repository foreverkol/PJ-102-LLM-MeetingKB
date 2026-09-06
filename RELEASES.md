# 发布历史

## v3.1.0-stable (2026-09-06) — 🟢 当前生产版本

**王老师 2026-09-06 OUT-OF-BAND 拍板**:"按照你的 我的强烈建议执行"

### 核心特性
- ✅ Sprint 21 v3.1.0-rc1 完整闭环(M0-M5)
- ✅ Codex 三次评审 + M5 校准(综合 7.5/10)
- ✅ **11 judgments YAML 损坏修复**(Codex H1 真阻塞)→ BAD YAML 0
- ✅ Karpathy + Obsidian 双核心升级
- ✅ 14 个子任务(T-01~T-14),12 项已完成
- ✅ 8 个 Templater 模板 + 8 个新单元测试
- ✅ pj102.py CLI 5 子命令

### 关键数字
- **98 测试 PASS**(3.47s)
- **351 wiki 文件**(从 127 → 351,+176%)
- **13 sample 真实跑通**
- **meeting_type 5/6 = 83.3%**

详见 `RELEASE_NOTES_v3.1.0-stable.md`

---

## v3.1.0-rc1 (2026-09-05) — Sprint 21 RC

### 核心特性
- Sprint 21 M0-M3 Superpower 模式自主推进
- 80 分钟完成 M0(工程计划)+ M1(t01/t02/t13)+ M2(t09/t04)+ M3(t12/t07/t10)
- v3.1.0-rc1 tag 自打(v41 允许 alpha/rc)

### 关键数字
- 98 PASS / 351 wiki / Codex 二次评审 8.5/10

---

## v3.0.1-stable (2026-09-04) — previous stable

(详见 `RELEASE_NOTES_v3.0.1-stable.md`)

---

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
