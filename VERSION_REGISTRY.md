# PJ-102-LLM-MeetingKB · 版本登记表(Version Registry)

> **目的**:对 PJ-102 项目**所有关键版本**做完整登记 + 描述 + 对比
> **生成时间**:2026-09-04
> **维护人**:王老师 + Agent
> **核心版本**:v1.0.0(基线)+ **v3.0.1-stable(当前 ⭐)**

---

## 📋 一、版本总览

| 版本 | tag | 日期 | 状态 | 关键能力 |
|---|---|---|---|---|
| v1.0-baseline | `v1.0-baseline` | 2026-09-04 | 历史 | 补全 4 类 WIKI 生成器(persons/concepts/judgments/comparisons) |
| **v1.0.0** | `v1.0.0` | **2026-09-03** | **🟢 长期支持** | **PJ-102 全项全量移植完成** |
| v1.1.0 | `v1.1.0` | 2026-09-04 | 历史 | 补全 4 类 WIKI 生成 |
| v3.0.0 | `v3.0.0` | 2026-09-04 | 基线 | v3.0 架构发布 |
| **v3.0.1-stable** | `v3.0.1-stable` | **2026-09-04** | **🟢 当前生产** | **13 sample 实测跑通 + 5/6 类命中(83.3%)** |

---

## 🎯 二、两个关键版本详解

### 2.1 v1.0.0 — PJ-102 项目起点(基线)

#### 基本信息
```
Tag:           v1.0.0
Tagger:        Wang Teacher <wang@pj102.local>
Date:          2026-09-03 22:10:23 +0800
Commit:        7be5f636154e311758408e6c0f3315cd3ec93375
类型:          全项全量移植完成
用途:          项目起点基线,所有后续版本在此基础上迭代
```

#### 项目背景
- **起源**:从 PJ-902-09 完整移植(项目代号变更 pj902-09 → pj102)
- **范围**:整个项目代码 + 配置 + 文档完整迁移
- **意义**:这是 PJ-102 项目的**第一个稳定版本**,代表项目正式成立

#### 核心交付物
```
✅ scripts/version_manager.sh    # 版本管理 CLI
✅ scripts/rollback.sh          # 一键回退脚本
✅ scripts/verify_version.sh    # 验证脚本
✅ .github/workflows/test.yml   # GitHub 自动测试
✅ .github/workflows/release.yml # GitHub 自动发布
✅ VERSION                       # 版本号文件
✅ RELEASES.md                   # 发布历史
✅ CHANGELOG.md                  # 变更日志
```

#### 版本管理规范集成
```
- 分支策略:master → main(标准化)
- 包名规范:pj902-09 → pj102(项目代号)
- 自动发布:.github/workflows/release.yml
- 自动测试:.github/workflows/test.yml
- 一键回退:scripts/rollback.sh
```

#### 适用场景
- ✅ 回退到项目起点
- ✅ 测试 v1.0 阶段的所有功能
- ✅ 验证 PJ-902-09 → PJ-102 移植完整性

---

### 2.2 v3.0.1-stable — 当前生产稳定版本(王老师 09-04 20:35 决策)⭐

#### 基本信息
```
Tag:           v3.0.1-stable
Tagger:        Wang Teacher <wang@pj102.local>
Date:          2026-09-04 20:43:27 +0800
Commit:        ff7ca8ea02ccdca9d933da1142c49694a269baae
类型:          成熟稳定锚点
用途:          后续所有迭代的基线,出现问题可回退到此
```

#### 项目背景
- **驱动**:王老师 09-04 11:16 OUT-OF-BAND 指示"基于参考设计 SCHEMA_v6.1+v7.0 充分判断吸收"
- **触发**:王老师 09-04 20:35 OUT-OF-BAND"将作为成熟稳定版本打 tag,出现问题可回退"
- **范围**:13 sample 端到端跑通,meet_type 6 类命中 5/6,所有 L1 测试通过
- **意义**:这是 v3.0 体系的**实战稳定锚点**,代表 PJ-102 项目可用于生产

#### 核心交付物
```
✅ 22 个 Python 模块(原 16 + 6 v3.0 新增)
   - citations.py / entity_resolver.py / lifecycle_stage.py
   - lint_wiki.py / dispute_detector.py / daily_incremental.py
   - feishu_lint_alert.py / entity_nav.py / kb_retriever.py
   - scenario_extractor.py / review_queue.py / steps/s14_scenario.py

✅ max_tokens=524288(官方硬上限,MiniMax-M3)
✅ MiniMax-M3 真实调用 + thinking fallback
✅ atomicstrata MCP server 集成
✅ hermes mcp add atomicstrata 自动接入
✅ 13 sample 真实跑通
✅ 127 文件 wiki 产出
✅ 5/6 类 meeting_type 覆盖

✅ 测试基础设施
   - 82 个 L1 测试用例(0.081s 全 PASS)
   - 6 份 Sprint 报告(Sprint 8-14)
   - L3 验收 10 Hard Gate

✅ 版本管理基础设施
   - VERSION: 3.0.1-stable
   - VERSION_MANAGEMENT.md(205 行)
   - scripts/rollback.sh(94 行,支持 --keep)
   - GITHUB_OPERATIONS_HANDBOOK.md(336 行)
   - QUICK_RECOVERY_CARD.md(136 行)
```

#### 技术指标
```
代码量:
- Python 模块:22 个
- 测试文件:12 个 / 82 个方法
- L1 测试:82/82 PASS(0.081s)

数据规模:
- 13 sample 端到端跑通
- 15 meetings / 25 judgments / 38 persons / 49 concepts
- 总计 127 文件 wiki 产出

质量指标:
- meeting_type 6 类覆盖:5/6 = 83.3%
- v6.1+v7.0 字段:100% 真实命中
- MiniMax-M3 rate limit:200 RPM(超时自动 fallback)

打包大小:
- tar.gz:256 KB
- 解压后:1.3 MB
- 文件总数:138
```

#### 适用场景
- ✅ **当前生产环境使用**
- ✅ 王老师口头"回退到此"一键恢复
- ✅ Sprint 15-17 后续迭代的基线
- ✅ 任何时候出问题 git reset --hard v3.0.1-stable

---

## 🔄 三、两个版本对比(王老师关注点)

| 维度 | v1.0.0 | v3.0.1-stable | 增长 |
|---|---|---|---|
| **日期** | 2026-09-03 | 2026-09-04 | 1 天 |
| **Python 模块** | ~16 个 | 22 个 | +38% |
| **L1 测试** | 基础 | 82 个 | 完整测试体系 |
| **真实跑通** | 0 | 13 sample | 数据驱动验证 |
| **wiki 产出** | 0 | 127 文件 | 实战产出 |
| **meeting_type** | 未分类 | 5/6 类 | v6.1+v7.0 集成 |
| **MiniMax-M3** | ❌ | ✅ | 王老师纠正生效 |
| **max_tokens** | 默认 | 524288(官方上限)| 性能优化 |
| **MCP 集成** | ❌ | atomicstrata | 工具扩展 |
| **版本管理** | 基础 | rollback.sh + 5 文档 | 专业级 |
| **回退能力** | 手动 | 一键脚本 | 自动化 |

**结论**:v3.0.1-stable 是 v1.0.0 的**全面升级**,从基线到生产,代码量 +38%、测试覆盖完整、数据驱动验证、专业级版本管理。

---

## 📜 四、版本演进时间线

```
2026-09-03 22:10:23  v1.0.0  ← 项目起点(全项全量移植)
         ↓
2026-09-04 11:16     王老师指示 v6.1+v7.0 集成
         ↓
2026-09-04 13:00     v3.0.0  ← v3.0 架构发布
         ↓
Sprint 1-15 开发过程(v3.0.0 → v3.0.1-stable 中间过程)
         ↓
2026-09-04 20:35     王老师"成熟稳定版本"诉求
         ↓
2026-09-04 20:43     v3.0.1-stable  ← 当前生产稳定
```

---

## 🛠 五、版本操作命令速查

### 5.1 查看版本信息
```bash
# 当前版本
cat VERSION

# 所有 tag
git tag -l -n1 "v*"

# v1.0.0 详情
git show v1.0.0

# v3.0.1-stable 详情
git show v3.0.1-stable
```

### 5.2 回退到指定版本
```bash
# 回退到 v1.0.0
bash scripts/rollback.sh v1.0.0

# 回退到 v3.0.1-stable
bash scripts/rollback.sh v3.0.1-stable
```

### 5.3 打包下载
```bash
# 打包 v1.0.0
git archive --format=tar.gz --output=~/Desktop/PJ-102-v1.0.0.tar.gz v1.0.0

# 打包 v3.0.1-stable
git archive --format=tar.gz --output=~/Desktop/PJ-102-v3.0.1-stable.tar.gz v3.0.1-stable
```

### 5.4 对比版本
```bash
git log v1.0.0..v3.0.1-stable --oneline
git diff v1.0.0 v3.0.1-stable --stat
```

---

## 📞 六、版本相关文档索引

| 文档 | 位置 | 用途 |
|---|---|---|
| `VERSION` | 根目录 | 当前版本号 |
| `.release-please-manifest.json` | 根目录 | 自动发布配置 |
| `VERSION_MANAGEMENT.md` | 根目录 | 版本管理完整指南 |
| `GITHUB_OPERATIONS_HANDBOOK.md` | 根目录 | GitHub 操作手册 |
| `QUICK_RECOVERY_CARD.md` | 根目录 | 王老师口头要求速查 |
| `VERSION_REGISTRY.md` | 根目录 | **本文档**版本登记 |
| `STATE.md` | 根目录 | 项目当前状态 |
| `CHANGELOG.md` | 根目录 | 完整变更日志 |
| `RELEASES.md` | 根目录 | 发布历史 |
| `scripts/rollback.sh` | scripts/ | 一键回退脚本 |

---

## ⚠️ 七、王老师决策点

### 决策 1:是否把 v1.0.0 标记为长期支持(LTS)?
- ✅ 建议:是(作为项目起点,长期保留)
- 当前:LTS ✅

### 决策 2:v3.0.1-stable 是否作为生产版本?
- ✅ 建议:是(13 sample 实战验证)
- 当前:生产 ✅

### 决策 3:后续是否打 v3.0.2-stable patch?
- 王老师决策点:每次 Sprint 完工后是否打新 patch
- 默认建议:每个 Sprint 完工打

### 决策 4:何时升级到 v3.1.0?
- 触发:加新功能(后台批量 / 飞书 dashboard)
- 决策:王老师根据业务需求决定