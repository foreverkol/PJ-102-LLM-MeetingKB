# 🤖 PJ-102-LLM-MeetingKB · workbuddy v3.0 完整接入提示词

> **这份提示词给 workbuddy**(腾讯 Agent 工具)
> **复制整段粘贴到 workbuddy 即可**
> **workbuddy 会自动按 Sprint 1 + Sprint 2 + Sprint 3 顺序执行**
> **v1.0 → v3.0 主要差异:** MiniMax-M3 / 22 个模块 / 125 L1 测试 / SCHEMA v6.1+v7.0

---

## 📋 v3.0 完整提示词(粘贴用)

```
你是 workbuddy AI Agent。本任务：完整复制 PJ-102-LLM-MeetingKB v3.0.0。

## 项目背景(v3.0)

PJ-102-LLM-MeetingKB 是一个基于 LLM 真实调用(MiniMax-M3)的会议转写→知识库系统。

v3.0.0 release-ready,实测 125 个 L1 测试全 PASS(0.112s)。

- 仓库地址:https://github.com/foreverkol/PJ-102-LLM-MeetingKB
- v3.0.0 tag:73e325c
- 默认模型:MiniMax-M3(不是 MiniMax-Text-01,中国区 api.minimaxi.com)
- 22 个 Python 模块 / 32 个 L1 测试文件 / 125 个测试方法

## v3.0 新增能力(对比 v1.0)

### v6.1 4 补丁(必做)
1. **P-1 判断标注**:`[判断:发言人]` 标注会议判断句
2. **P-2 定量金融参数**:9 类金融参数(额度/利率/期限等)
3. **P-3 可转化资产 tag**:5 类 `#可转化资产/#BP素材` 等
4. **P-4 meeting_type 6 类**:client_visit / bank_communication / partner_coordination / ...

### v7.0 10 新规(必做)
1. ldamc 5 维自检(Lost/Different/Added/More/Connected)
2. contradictions 显式字段(`<!-- Status: Disputed -->`)
3. entity_id 统一编号(`person_{hash8}_{seq4}`)
4. canonical_name + aliases + 消歧
5. status_stage 5 阶段状态机(raw/compiled/reviewed/canonical/superseded)
6. topic_key judgment 主题聚合
7. evolution 演化链
8. scenario 新页面(11 字段)
9. external_ref 纯度规则
10. extraction_patch YAML 中间层

## 5 阶段执行顺序(Superpower)

### 阶段 1:代码获取 + 验证
```
1. git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
2. cd PJ-102-LLM-MeetingKB
3. git checkout v3.0.0
4. cat VERSION  # 应输出 3.0.0
5. pip install pyyaml  # citations.py 依赖
```

### 阶段 2:环境配置(王老师 MiniMax-M3 Key)
```bash
export MINIMAX_API_KEY="<your-real-key-from-~/.hermes/secrets.d/minimax_api_key.txt>"
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"
```

### 阶段 3:验证 L1 测试
```bash
cd 03-执行/code
python3 -m unittest discover tests/unit 2>&1 | tail -5
# 必须输出:Ran 125 tests in 0.X s  OK
```

### 阶段 4:测试 1 sample 真实 LLM 跑通(王老师限制 ≤10)
```bash
SAMPLE="/path/to/_原文.md"
python3 -c "
import sys; sys.path.insert(0, '.')
from llm_client import LLMClient
from steps import s2_scene_recognition, s3_standard_summary, s9_knowledge_classify
from steps.s10_cognitive import s10_cognitive_refine
from steps.s13_financial_params import s13_financial_params
llm = LLMClient(provider='auto')
content = open('$SAMPLE', encoding='utf-8').read()[:8000]
r2 = s2_scene_recognition(content[:4000], llm)
r3 = s3_standard_summary(content[:6000], llm)
r9 = s9_knowledge_classify(content[:8000], llm)
r10 = s10_cognitive_refine(content[:10000], llm)
r13 = s13_financial_params(content[:8000], llm)
print('meeting_type:', r2.get('scene_type'))
print('has [判断:]:', '[判断:' in r3.get('insight', ''))
print('quant_params:', len(r3.get('quantitative_params', [])))
print('convertible_tags:', len([t for t in r9.get('tags', []) if t.startswith('#可转化资产/')]))
print('ldamc_keys:', len(r10.get('ldamc', {}).keys()))
print('financial_params:', len(r13))
"
```

### 阶段 5:跑批 + 落 WIKI(王老师限制 ≤10 sample)
```bash
# W4.3 脚本就位
SAMPLE_LIMIT=10 bash scripts/run_full_pipeline.sh
```

## v3.0 新增 CLI 命令

```bash
# v7.0 必填字段巡检
python3 03-执行/code/lint_wiki.py /path/to/WIKI/

# 实体导航(无需 LLM)
python3 03-执行/code/entity_nav.py --query "浙商银行上次聊什么" \
    --registry SYSTEM/registry/entity_registry.json \
    --persons-master SYSTEM/masters/persons_master.json

# 矛盾检测
python3 03-执行/code/dispute_detector.py \
    SYSTEM/masters/judgments_master.json \
    /path/to/WIKI/

# 增量调度
python3 03-执行/code/daily_incremental.py \
    --source /path/to/_原文.md \
    --state SYSTEM/state/processed_files.json

# scenario 提取
python3 -c "
import sys; sys.path.insert(0, '03-执行/code')
from steps.s14_scenario import s14_scenario
from llm_client import LLMClient
llm = LLMClient(provider='auto')
content = open('$SAMPLE', encoding='utf-8').read()[:10000]
scenarios = s14_scenario(content, llm)
print(f'识别 {len(scenarios)} 个 scenario')
for s in scenarios:
    print(f'  - {s[\"theme\"]}')
"

# 飞书告警
python3 03-执行/code/feishu_lint_alert.py --dry-run
```

## R5 防坑(写完即 ls + wc + head + git add + commit)

每次 write_file 后必须:
```bash
ls -la <path>           # 验证存在
wc -l <path>            # 验证行数
head -3 <path>          # 验证内容
git add <path>
git commit -m "..."
git log --oneline -1
```

任一失败立刻报告,不允许跨过。

## Superpower Plan-Execution-Phase 陷阱防控

王老师说"按建议执行"或"继续" = 全权授权。
**不要"是否继续 W2?"式询问**。
每步完成立即下一步。

## 已知坑(王老师 09-04 实测沉淀)

1. **MiniMax 模型**:`MiniMax-M3`,不是 `MiniMax-Text-01`
2. **base_url**:中国区 `api.minimaxi.com`(不是 `api.minimax.chat`)
3. **safe_json_parse** 已支持 list + markdown 围栏 + 尾随逗号
4. **entity_id**:`organization` 短前缀 = `org`,不要全词
5. **ldamc** 5 维解析用 `_parse_frontmatter` 支持 indent block
6. **王老师不跑全量**(默认 SAMPLE_LIMIT=10)
```

---

## 🆚 v3.0 vs v1.0 关键差异(给 workbuddy 看的对比)

| 维度 | v1.0 | v3.0 |
|---|---|---|
| 模型 | MiniMax-Text-01(旧) | **MiniMax-M3**(王老师 09-04 纠正) |
| 步骤 | 12 步 | **13 步**(新增 S13 金融参数 + S14 scenario) |
| 模块 | 16 个 | **22 个**(新增 11 个 v3.0 模块) |
| 测试 | 9 个 smoke | **125 个 L1 测试** |
| SCHEMA | v1.0 老 | **v6.1 + v7.0** |
| Wiki 类别 | 5 类 | **9 类**(含 scenario/external_ref) |
| 矛盾检测 | 无 | **Status: Disputed 自动加** |
| 增量调度 | 无 | **content_hash 跳过** |
| 飞书告警 | 无 | **3 段式消息** |

---

## 📋 workbuddy 操作要点

- **每写一份文件立即 git commit**(R5 防坑)
- **失败不静默**(Superpower 铁律)
- **每步完成飞书量化汇报**(数字 + 下一步)
- **总耗时约 2-3 小时**(实测经验)
- **王老师限制 ≤10 sample**,不要批量

---

## 📞 反馈与失败处理

workbuddy 跑测中遇真实阻塞(API 失败 / 路径不存在 / 模块找不到):
- 立即停止,不要硬扛
- 报告失败现象 + 已尝试步骤
- 不要编造"已修复"报告

参考 Skill:
- `~/.hermes/skills/write-file-lost-prevention/` — 五步实测法
- `~/.hermes/skills/v3-sprint-superpower-execution/` — Sprint 实战规范
