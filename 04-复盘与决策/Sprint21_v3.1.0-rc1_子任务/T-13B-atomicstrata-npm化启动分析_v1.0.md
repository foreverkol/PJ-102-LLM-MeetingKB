# T-13B: atomicstrata npm 化 — 启动分析与范围说明 v1.0

> **触发**:王老师 2026-09-06 OUT-OF-BAND "按建议执行"
> **优先级**:Sprint 22 第一周启动
> **生成**:2026-09-06 by Hermes Agent(MiniMax-M3)
> **状态**:⚪ 启动分析完成,等 Sprint 22 启动

---

## 🎯 T-13B 真实含义澄清

### 命名来源

王老师消息原文:**"CT-13B atomicstrata npm 化"** — Codex 二次评审 §C + §D + §E + M5 校准报告 D 节提及的扩展任务。

**易混淆点**:
- **T-13**(已存在) = "Sources[] 行号级引用"(PJ-102 项目内 PoC 24 concepts 升级为 frontmatter 结构化)
- **T-13B**(本次) = **"把 atomicstrata 集成层封装为可发布/可独立调用的 npm 命令"** — 与 T-13 平行的扩展任务

### 实际要做的事

**不是**:把 atomicstrata 官方仓库改造成 npm 包(那是 atomicstrata 项目维护者的事)

**是**:PJ-102 项目当前的 `obsidian_export.py`(读 atomicstrata-profile.json → 生成 CLAUDE.md / .base 文件 / Dataview 模板)封装为:
- ✅ **可独立 npm install 调用**:`npx pj102-atomicstrata-export <profile.json> <output_dir>`
- ✅ **跨项目复用**:任何有 atomicstrata profile 的项目都可调用
- ✅ **解耦**:PJ-102 项目不直接 import obsidian_export.py,改调 npm 包

---

## 📊 当前状态实测(2026-09-06)

### atomicstrata 集成层在 PJ-102 项目内的存在形式

```
02-设计/atomicstrata-profile.json     (8 entities × 166 行 profile)
03-执行/code/obsidian_export.py       (327 行,主集成代码)
03-执行/code/t04_organization_entity.py (引用 profile)
03-执行/code/t13_sources_line_citations.py (PoC 24 concepts 用 prose)
poc/atomicstrata-experiment 分支      (24 concepts + 3 sources)
```

### obsidian_export.py 当前功能(实测 grep)

```python
# 读 atomicstrata-profile.json → 生成 CLAUDE.md / .base / Dataview 模板
SCHEMA_PATH = Path("/mnt/d/.../PJ-102-LLM-MeetingKB/02-设计/atomicstrata-profile.json")
# 硬编码 /mnt/d 路径 → 跨项目无法复用
# 仅生成 markdown 字符串 → 不支持独立命令行调用
# 与 pipeline 紧耦合 → 不易独立测试
```

**3 个限制**:
1. **硬编码绝对路径**(`/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/...`)
2. **仅作为 Python 模块**(无 CLI 入口)
3. **无 package.json / npm 配置**(PJ-102 项目本身不是 npm 项目)

---

## 🚀 Sprint 22 T-13B 实施方案

### 阶段 A:解耦与抽象(3 天)

1. **路径抽象**:obsidian_export.py 的所有硬编码路径 → `argparse` 或环境变量 `PJ102_PROJECT_ROOT`
2. **CLI 入口**:加 `__main__.py` + `python3 -m obsidian_export --profile <path> --out <dir>`
3. **单测覆盖**:`test_obsidian_export.py` 覆盖 CLI 调用 + 输出格式

### 阶段 B:npm 封装(2 天)

1. **新建 npm 包**:`pj102-atomicstrata-export/`
   ```
   package.json
   bin/pj102-atomicstrata-export.js  (Node.js wrapper)
   src/index.py                       (Python 核心逻辑)
   README.md
   ```
2. **Node.js wrapper**:用 `child_process.execSync` 调 Python(避免重写)
3. **发布测试**:`npm link` 本地测试 + `npm pack` 验证打包

### 阶段 C:集成验证(2 天)

1. **PJ-102 项目切换**:`obsidian_export.py` → 调 `npx pj102-atomicstrata-export`
2. **跑全量 L1 测试**:98 PASS 不变
3. **跑 1 sample 真实端到端**:验证 npm 路径下 CLAUDE.md 生成正确

### 阶段 D:文档 + 教程(1 天)

1. README.md(安装 / 用法 / 配置)
2. CHANGELOG.md(0.1.0 初版)
3. 一键验证脚本

---

## 📋 验收标准

| 项 | 验收 |
|---|---|
| **硬编码路径清零** | `grep -rn "/mnt/d/BaiduSyncdisk" 03-执行/code/` 输出 0 条 |
| **CLI 可独立调用** | `python3 -m obsidian_export --help` 打印用法 |
| **npm 包可用** | `npx pj102-atomicstrata-export --profile test.json --out out/` 生成正确文件 |
| **L1 测试不回归** | 98 PASS / 3.62s |
| **端到端真跑通** | PJ-102 跑 1 sample,CLAUDE.md 真实生成 |
| **跨项目复用** | 在测试目录建一个最小 profile,生成结果一致 |

---

## ⚠️ 风险与缓解

| 风险 | 等级 | 缓解 |
|---|---|---|
| Node.js + Python 双语言依赖 | 🟡 中 | 用 `child_process.execSync`,不引入新概念 |
| npm 包发布到公网 | 🟢 低 | 仅本地 `npm link`,不发布 |
| 现有 obsidian_export.py 重构有回归风险 | 🟡 中 | 阶段 A + 阶段 C 分步验证,L1 测试守门 |
| 王老师工作流不熟 npm | 🟢 低 | 提供 `make install-pj102-export` 一键命令 |

---

## 🛠 v44 不擅自处理原则确认

| 项 | 是否等王老师拍板 |
|---|---|
| 是否启动 Sprint 22 T-13B | ✅ **等王老师确认** |
| 是否发布到 npm 公网 | ✅ **明确否**(仅本地 `npm link`) |
| 是否重写 obsidian_export.py 现有逻辑 | ✅ **明确否**(只重构路径 + 加 CLI) |
| 跨项目复用范围 | ✅ **等王老师确认**(Sprint 22 启动时) |

---

## 🚦 当前决策状态

**王老师拍板选项**(Sprint 22 启动时):

```
🟢 A 立即启动(预计 8 天,本任务)
🟡 B Sprint 22 第二周启动(让 T-01 75 先跑)
🟣 C 暂缓到 Sprint 23+(让其他决策项先动)
```

**Hermes 建议**:**选项 B** — 让 T-01 75 跑(王老师批 1 小时)优先,T-13B 在 Sprint 22 第二周启动。

---

## 📂 相关文件

- `03-执行/code/obsidian_export.py`(327 行,当前实现)
- `02-设计/atomicstrata-profile.json`(166 行,profile 定义)
- `03-执行/tests/unit/test_obsidian_export.py`(已存在测试)
- `04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-13-Sources[] 行号级引用.md`(T-13 原始任务文档)

---

## 🔗 相关决策

- T-13B 与 T-13 互不冲突:T-13 改 frontmatter,T-13B 改工具链
- T-13B 与 E 选项相互独立:本任务不阻塞 v3.1.0-stable(已拍板)
- T-13B 与 v44:严格遵守,所有 npm 化决策均需王老师拍板

---

**报告人**:Hermes Agent(MiniMax-M3)
**协议版本**:v44(不擅自分配任务) + 王老师 Superpower"按建议执行"协议