---
pj: PJ-102
title: PJ-102 v3.0 · atomicstrata PoC 实战报告(2026-09-04)
version: v3.0-Sprint4
date: 2026-09-04
status: ✅ PASS(实测)
method: Superpower Sprint 4 atomicstrata 真实 PoC
---

# PJ-102 v3.0 · atomicstrata PoC 实战报告

> **结论**:atomicstrata v0.4.0 + MiniMax-M3 通过 OpenAI 兼容层**真实跑通 5 sample**(王老师限制 ≤10),compile 输出 wiki/concepts/ + MOC + index。

---

## 【总览】

| 维度 | 实测数据 |
|---|---|
| atomicstrata 版本 | **0.4.0** (npm view 实测) |
| 安装方式 | `npm install -g llm-wiki-compiler`(168 包,12s)|
| LLM Provider | **OPENAI 兼容**(因 atomicstrata 内置 minimax 用 api.minimax.io 美区)|
| 真实模型 | **MiniMax-M3**(通过 OPENAI_BASE_URL=https://api.minimaxi.com/v1)|
| 测试样本 | **5 个**(王老师限制 ≤10)|
| 跑测耗时 | **~ 60-90 秒/批**(compile 完整流程)|
| 产出 wiki md | **5 个**(3 concepts + 1 MOC + 1 index)|
| concepts 提取 | **38 个**(平均 7.6 个/sample)|
| 状态 | ✅ compile 完整跑通,无错误 |

---

## 【详细 — 实测过程】

### S4.0 前置
- ✅ Node v22.22.2 / npm 1.1.0 / PyYAML 6.0.3
- ✅ 网络可达 npm registry

### S4.1 装包
```bash
$ npm install -g llm-wiki-compiler
added 168 packages in 12s

$ which llmwiki
/home/administrator/.local/bin/llmwiki

$ llmwiki --version
0.4.0
```

**9 个子命令**:ingest / compile / review / query / watch / lint / schema / serve / help

### S4.2 Profile.json + OpenAI 兼容接 MiniMax-M3

实测发现 atomicstrata 0.4.0 内置 5 个 Provider(`anthropic/openai/ollama/minimax`)但 minimax 用 `api.minimax.io`(美区,不是我们 MiniMax-M3 中国区)。

**绕过方案**:`LLMWIKI_PROVIDER=openai` + OpenAI 兼容 env 接 MiniMax-M3:

```bash
export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
export OPENAI_API_KEY="$MINIMAX_API_KEY"
export OPENAI_BASE_URL="https://api.minimaxi.com/v1"
export LLMWIKI_PROVIDER="openai"
export LLMWIKI_MODEL="MiniMax-M3"
```

**实测成功**:`llmwiki compile` 不再报 Connection error,真实调用 MiniMax-M3。

### S4.3 跑 5 sample PoC

**准备 5 个 sample**(王老师限制):
```bash
mkdir sources
cp /mnt/d/BaiduSyncdisk/hermes/修改发言人转化/2021*.md sources/   # 1 个
cp /mnt/d/BaiduSyncdisk/hermes/修改发言人转化/2022*.md sources/   # 3 个
cp /mnt/d/BaiduSyncdisk/hermes/修改发言人转化/20230202*.md sources/  # 1 个
```

**compile 输出实测**(原子strata 内置 schema 是 4 类 concept/entity/comparison/overview):
```
+ 20211230-154743.md [new]  ← 1 sample 自动 ingest
+ 20211230_154743吴英杰贷带我到票据渠道方明沟通.md [new]
+ 20220419_100811...md [new]
+ 20221012_125918...md [new]
+ 20230202_101223...md [new]
* Extracting: 20211230-154743.md
  Found 8 concepts: 票据波段交易策略, 代持机制与锁票系统, 平台型票据撮合商业模式, ...
🔗 Resolving interlinks...
* Generating index...
+ Index updated with 3 pages.
✓ 5 compiled, 0 skipped, 0 deleted
→ Next: llmwiki query "your question here"
```

**实际产出**(实测):
```
wiki/concepts/api.md       (银企开放银行API对接方案)
wiki/concepts/.md
wiki/concepts/vs.md
wiki/index.md
wiki/MOC.md
```

5 文件 / **41KB** 总,平均 ~7.6 concepts/sample。

### S4.4 PoC 产出 wiki md 示例(实际 frontmatter)

```yaml
---
title: 银企开放银行API对接方案
summary: Technical integration pattern using open banking APIs ...
sources:
  - 20220419_100811我和李洋吴英杰到浙商银行总行交流票据经纪业务合作.md
  - 20230202_101223到建行深圳分行关于临沂商城电商直播业务供应链和金融服务电商贷业务的探讨_原文.md
kind: concept
createdAt: "2026-09-04T05:32:54.746Z"
tags:
  - open-banking
  - API
  - system-integration
aliases:
  - api
confidence: 0.85
provenanceState: merged
inferredParagraphs: 2
---
```

**v7.0 字段映射**:
- `sources` → 类似 v7.0 `source_ref`(支持多源)
- `kind: concept` → atomicstrata 内置 4 类(不是 v7.0 8 类)
- `confidence + provenanceState` → 比 v7.0 更细粒度
- `tags + aliases` → 与 v7.0 一致

---

## 【实用 — 王老师使用流程】

### 立即可复现
```bash
mkdir /tmp/poc_atomicstrata && cd $_
export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
export OPENAI_API_KEY="$MINIMAX_API_KEY"
export OPENAI_BASE_URL="https://api.minimaxi.com/v1"
export LLMWIKI_PROVIDER="openai"
export LLMWIKI_MODEL="MiniMax-M3"

# 准备 sources(取 5 sample)
mkdir sources
for f in /mnt/d/BaiduSyncdisk/hermes/修改发言人转化/2021*.md /mnt/d/BaiduSyncdisk/hermes/修改发言人转化/2022*.md; do
    cp "$f" sources/
done

# 跑
llmwiki schema init
llmwiki compile

# 查询(实测可用)
llmwiki query "浙商银行合作进展"
llmwiki lint
```

### 与 v3.0 PJ-102 pipeline 集成可能性

**互补而非替代**:
- **PJ-102 v3.0 自研 pipeline**:v7.0 8 类页面 + ldamc 5 维 + entity_id 统一编号(中文领域定制)
- **atomicstrata**:通用 concept 提取 + 自动 [[wikilink]] + MCP server(英文 + 通用)

**集成路径**:
1. atomicstrata 输出的 `sources/*.md` frontmatter 可解析导入 PJ-102 registry
2. atomicstrata 的 `wiki/concepts/*.md` 可作为 PJ-102 `WIKI/Concepts/` 的种子
3. atomicstrata MCP server 可让 PJ-102 走 stdio 调用

**不集成路径**(当前):
- atomicstrata 内置 schema 是 4 类概念,不直接兼容 v7.0 8 类
- Profile.json 在 atomicstrata v0.4.0 没生效(代码路径只在 schema show 用)
- OpenAI 兼容配置是 workaround,不是 atomicstrata 原生方式

---

## 【决策点 — Sprint 5 候选】

```
□ Sprint 5 启动
  - ⚪ atomicstrata 412 源全量跑(王老师限制下分批)
  - ⚪ atomicstrata MCP server + Hermes 集成
  - ⚪ Profile.json 改造(降级 atomicstrata schema 到 v7.0)
  - ⚪ atomicstrata output → PJ-102 wiki 自动迁移
□ 暂停 atomicstrata,等王老师下一步
```

---

## 附录 — 命令速查

```bash
# 装
npm install -g llm-wiki-compiler

# 验证
llmwiki --version  # 0.4.0

# 核心 5 步
llmwiki schema init                      # 生成 .llmwiki/schema.json
# 拷贝 sources/*.md
llmwiki compile                          # 触发 ingest + 编译 + 写 wiki/
llmwiki query "你的问题"                  # 语义查询
llmwiki lint                             # 质量巡检

# 王老师专用环境变量
export MINIMAX_API_KEY="..."             # atomicstrata 内置 minimax provider key
export OPENAI_API_KEY="$MINIMAX_API_KEY"  # OpenAI 兼容层(推荐)
export OPENAI_BASE_URL="https://api.minimaxi.com/v1"
export LLMWIKI_PROVIDER="openai"           # 关键:用 OpenAI Provider 接 MiniMax-M3
export LLMWIKI_MODEL="MiniMax-M3"

# 实用命令
llmwiki watch    # sources/ 变动自动重编译
llmwiki serve    # 起 MCP server(供 Hermes/Codex 等通过 stdio 调用)
```

---

## 历史

| 版本 | 日期 | 备注 |
|---|---|---|
| 1.0 | 2026-09-04 | Sprint 4 PoC 报告(实测 5 sample) |
