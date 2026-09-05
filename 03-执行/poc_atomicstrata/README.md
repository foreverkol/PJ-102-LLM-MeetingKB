# PJ-102 · atomicstrata PoC 工作目录

> **状态**: ✅ v1.0 实测完成 (2026-09-05)
> **基础**: 全新原始录音转写 5 个 (来自 `D:\BaiduSyncdisk\hermes\修改发言人转化\`)
> **profile**: `pj102-finance-meeting v1.0.0` (本目录 `.llmwiki/profile.json`)

---

## 🎯 用途

这是 **PJ-102-LLM-MeetingKB** 项目探索 atomicstrata 工程的实测工作目录,不是项目本体。

**目标**:
- 验证 atomicstrata 是否能解决 PJ-102 Karpathy 5 原则违反 (P2 引用溯源 / P3 增量更新 / P4 矛盾标注)
- 沉淀 6 entities profile 模板 (meetings / persons / organizations / topics / judgments / comparisons)
- 跑通 1 篇 → 5 篇小样本 → 待扩量到全量

---

## 📂 目录结构

```
poc_atomicstrata/
├── README.md                (本文件)
├── log.md                   (compile 运行日志)
├── .llmwiki/                (atomicstrata 配置 + 状态)
│   ├── profile.json         (8.3 KB - pj102-finance-meeting v1.0.0)
│   ├── state.json           (compile 状态)
│   ├── pending-embeddings.json
│   └── journal/             (compile 过程日志)
├── sources/                 (5 个原始录音转写输入)
│   ├── pj102_20220902_...历城控股票据供应链...md     (51 KB)
│   ├── pj102_20230202_...建行深圳临沂商城...md        (123 KB)
│   ├── pj102_20240115_...工商行杭州助贷...md            (92 KB)
│   ├── pj102_20250102_...助贷王洪丽资产包...md         (8 KB, 小样本)
│   └── pj102_20260105_...萧山畅聚科技丁献忠...md     (169 KB)
└── wiki/                    (编译产物)
    ├── MOC.md               (主题分组索引)
    ├── index.md             (全量索引)
    └── concepts/            (24 个概念页)
        ├── 商票供应链业务模式.md
        ├── 新一代票据系统与可拆分功能.md
        ├── 差额纳税与保理公司注册选址.md
        ├── 供应链金融平台的三种部署模式.md
        ├── 临沂商票试点与15条指导意见.md
        ├── 总包方保理风控闭环模式.md
        ├── 电票期限缩短与新规影响.md
        ├── 临沂商城直播电商生态.md
        ├── 贷款中介转贷垫资业务.md
        ├── 供应链金融与产业图谱.md
        ├── 深度数科票据数据平台.md
        ├── 数据驱动的银行助贷模式.md
        ├── 手机租赁延伸小额贷款业务.md
        ├── 受托支付与风控流程.md
        ├── 银行渠道返佣与合作模式.md
        ├── 科技型企业大额信用贷款.md
        ├── 资产包购买与处置模式.md
        ├── 分布式诉讼与回款率指标.md
        ├── 不良资产交易结构设计.md
        ├── 电催调解诉讼业务分工.md
        ├── 助贷与小额贷款业务.md
        ├── 资金撮合与优先级资金供给.md
        ├── 司法管辖与互联网法院开户.md
        └── 不良资产市场供需与价格.md
```

---

## 📊 实测结果 (2026-09-05)

| 维度 | 实测 |
|------|------|
| **5 个原始录音跑批** | ✅ 5/5 成功 |
| **耗时** | 262 秒 (4.4 分钟, ~41s/篇) |
| **概念页产出** | 24 个 (平均 ~12 KB) |
| **profile 验证** | ✅ "Profile 'pj102-finance-meeting' is valid" |
| **Query 准确率** | 3/3 = 100% |
| **行号精确引用** | ✅ `^[pj102_20220902_...:101-103]` 格式 |
| **矛盾检测** | 0 (本次 5 篇无矛盾) |

---

## 🔧 运行方法

### 重新跑 compile

```bash
cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/poc_atomicstrata

# 设置环境变量
export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
export OPENAI_API_KEY="$MINIMAX_API_KEY"
export OPENAI_BASE_URL=https://api.minimaxi.com/v1
export LLMWIKI_PROVIDER=openai
export LLMWIKI_MODEL=MiniMax-M3
export LLMWIKI_OUTPUT_LANG=zh-CN

# 跑
llmwiki compile --verbose
```

### Query 跨文档问答

```bash
llmwiki query "临沂商城普惠助贷试点怎么做的?" --lang zh-CN
llmwiki query "深度数科票据数据平台核心方法论?" --lang zh-CN
llmwiki query "5 个录音里都提到的供应链金融核心是什么?" --lang zh-CN
```

---

## 🚦 与 PJ-102 项目关系

- **不是** PJ-102 项目的官方产出(不是 v3.0.1-stable 的产物)
- **是** 探索 atomicstrata 工程能力的 PoC,为 Sprint 21 决策提供实测依据
- **下一阶段**:如决定采用 atomicstrata,需新建 `PJ-102-LLM-MeetingKB-atomicstrata-v1.0/` 独立项目
  (按王老师 2026-09-03 决策:**基于成功模式创建新项目时,新项目与原项目零依赖**)

---

## 📜 关键决策记录

| 时间 | 决策 | 原因 |
|------|------|------|
| 2026-09-05 | 放在 `03-执行/poc_atomicstrata/` 而非 `/tmp/` | 王老师规范要求(项目产物在项目目录) |
| 2026-09-05 | 6 entities profile (含 comparisons) | PJ-102 WIKI 5 类齐全,comparisons 补齐 |
| 2026-09-05 | 跨年 4 选 5 样本 (2022/2023/2024/2025/2026) | 王老师"实验验证再升级"决策偏好 |

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 15:21 CST
**协议版本**: hermes-anti-hallucination v42
