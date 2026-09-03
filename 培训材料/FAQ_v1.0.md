# PJ-102-LLM-MeetingKB · FAQ v1.0

## 1. 基础问题

### Q1: 什么是 PJ-102-LLM-MeetingKB？

**A**: PJ-102-LLM-MeetingKB 是一个**完全独立**的会议转写→知识库处理项目。它使用 LLM 真实调用（默认 MiniMax M3）+ 12 步 pipeline，将会议录音原文转换为高质量的 Markdown 知识库。

### Q2: 为什么要新建独立项目（PJ-102）而不是用 PJ-001-07？

**A**: 王老师要求"完全独立，零依赖"。PJ-102 的特点：
- ✅ 不与 PJ-001 任何子项目共享代码
- ✅ 旧 WIKI 不移植（重新生成）
- ✅ 独立的 WIKI 输出目录
- ✅ 独立的 registry

### Q3: 跟 PJ-001-08 八月样本有什么区别？

**A**: PJ-001-08 是验证版本（13 个 8 月份样本），PJ-102 是生产版本（255 个全量）：
| 维度 | PJ-001-08 | PJ-102 |
|---|---|---|
| 项目位置 | PJ-001-08 八月样本 | PJ-102-LLM-MeetingKB |
| WIKI 数量 | 13 | 10（已验证）/ 255（目标）|
| 代码 | 单文件 pipeline_v3.py | 16 个拆分模块 |
| 文档 | 1 份需求 | 12 份完整 |
| 定位 | 验证 | 生产 |

## 2. 运行问题

### Q4: 跑批报"找不到 index"？

**A**: 路径错误。检查：
```bash
ls /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/system/data/index.json
```

如果不存在，需重新复制源文件。

### Q5: API key 无效？

**A**: 检查：
```bash
echo "MINIMAX_API_KEY 长度: ${#MINIMAX_API_KEY}"
```

如果 < 100 字符，需要从 `~/.hermes/.env` 重新读取：
```bash
source /home/administrator/.hermes/.env
export MINIMAX_API_KEY=$(grep ^MINIMAX_API_KEY= /home/administrator/.hermes/.env | cut -d= -f2)
```

### Q6: 跑批超时（HTTP 404）？

**A**: base_url 错误。确保：
```bash
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"
```

⚠️ 是 `api.minimaxi.com`，不是 `api.minimax.chat`！

### Q7: 跑批很慢怎么办？

**A**: 当前每个文件 135.8 秒（含 11 次 LLM 调用）。这是正常的。

**优化方法**：
- 减少 prompt 长度
- 并发处理（v2.0）
- 缓存机制（v1.1）

### Q8: LLM 调用 429 限流？

**A**: 代码已自动处理（exponential backoff）。如果频繁触发：
- 联系 Hermes 管理员申请更高配额
- 或切换到备用 provider

### Q9: JSON 解析失败？

**A**: 代码已通过 `safe_json_parse()` 容错处理：
- 移除 ```json 包裹
- 修复尾随逗号
- 提取 JSON 块
- 失败返回默认值（不阻塞）

## 3. 输出问题

### Q10: WIKI 输出在哪里？

**A**: 
```
/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/
├── meetings/
├── persons/
├── concepts/
├── judgments/
└── comparisons/
```

### Q11: 生成的 WIKI 包含哪些内容？

**A**: 12 章节：
1. 📌 基础信息（S1）
2. 🎬 场景识别（S2）
3. 📋 标准摘要（S3）
4. 🔍 FJV 三分法（S4）
5. 🧠 隐性知识（S5）
6. 🏷️ 5 类实体（S6）
7. ✅ 决策和行动项（S7）
8. ⚠️ 风险与盲区（S8）
9. 📚 知识归类（S9）
10. 🧬 认知提炼（S10）
11. ⭐ 价值评级（S11）
12. 📑 元信息

### Q12: 如何查看单个 WIKI？

**A**: 
```bash
cat /mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/meetings/meeting_2026-08-02_c1fca66c828c.md
```

或在 Obsidian 中打开 Vault：`/mnt/d/BaiduSyncdisk/hermes/02-知识库/`

### Q13: 5 类 WIKI 中只有 meeting？

**A**: 当前 v1.0 只生成 meeting。person / concept / judgment / comparison 待实现。

## 4. 配置问题

### Q14: 如何切换 LLM Provider？

**A**: 
```bash
# 切到 DeepSeek
export DEEPSEEK_API_KEY="..."
export MINIMAX_API_KEY=""
python3 pipeline.py --provider deepseek

# 切到 OpenAI
export OPENAI_API_KEY="..."
export MINIMAX_API_KEY=""
python3 pipeline.py --provider openai
```

### Q15: 如何修改 prompt？

**A**: 编辑 `03-执行/code/steps/s?_*.py` 文件，修改 prompt 字符串。例如修改 S4：
```python
# 编辑 03-执行/code/steps/s4_fjv.py
prompt = f"""...新的 prompt..."""
```

### Q16: 项目目录在哪里？

**A**: 
```
/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/
```

## 5. 性能问题

### Q17: 单文件处理时间？

**A**: 实测 **135.8 秒**（10 个样本平均）。

**拆分**：
- S1（规则）：< 1 秒
- S2-S11（11 次 LLM）：约 130 秒
- S12（写入）：< 1 秒

### Q18: 全量 255 个需要多久？

**A**: 约 **9.6 小时**（后端自动跑）。

### Q19: 如何加速？

**A**: 短期（v1.1）：
- prompt 压缩
- 缓存机制

中期（v2.0）：
- 并发处理
- 批量调用

### Q20: 如何看性能？

**A**: 看跑批日志：
```
📊 10 成功 / 0 失败
⏱️  总耗时: 1358.2s, 平均: 135.8s/文件
```

或看详细报告：
```
04-复盘与决策/性能基准报告_v1.0.md
```

## 6. 数据问题

### Q21: 源文件是哪个目录？

**A**: 
```
/mnt/d/BaiduSyncdisk/hermes/修改发言人转化/
```

⚠️ 本项目**只读**，不会修改。

### Q22: 复制源文件的目的？

**A**: 
- ✅ 独立副本（即使源目录变化也不影响）
- ✅ 加速访问（避免反复读网络盘）
- ✅ 不修改源目录

### Q23: WIKI 内容会重复吗？

**A**: 不会。文件命名 `meeting_{date}_{content_hash}.md`：
- date: YYYY-MM-DD
- content_hash: sha256 前 12 位
- 同文件不会重复生成

### Q24: 如何重新生成某个 WIKI？

**A**: 
```bash
# 1. 删除原文件
rm /mnt/d/.../PJ-102-LLM-MeetingKB/meetings/meeting_*.md

# 2. 重跑（自动重新生成）
python3 pipeline.py --sample "原文件名.md"
```

## 7. 故障问题

### Q25: 跑批中断怎么办？

**A**: 再次运行即可：
```bash
python3 pipeline.py  # 自动跳过已存在的 WIKI
```

### Q26: 全部失败怎么办？

**A**: 检查：
1. API key
2. 网络
3. base_url
4. 查看故障处理手册：`04-复盘与决策/故障处理手册_v1.0.md`

### Q27: 单文件失败影响整体吗？

**A**: 不影响。每个文件独立处理，失败记录到日志，继续下一个。

## 8. 集成问题

### Q28: 如何集成到 Obsidian？

**A**: 
1. 打开 Obsidian
2. 打开 Vault：`/mnt/d/BaiduSyncdisk/hermes/02-知识库/`
3. 浏览 `PJ-102-LLM-MeetingKB/meetings/`

### Q29: 如何自动化跑批？

**A**: 用 cron（待实现）：
```bash
# 每周日凌晨 2 点
0 2 * * 0 cd /mnt/d/.../PJ-102/03-执行/code && python3 pipeline.py
```

### Q30: 如何备份？

**A**: 
```bash
tar -czf /tmp/pj102_$(date +%Y%m%d).tar.gz \
  /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/
```

## 9. 王老师认可

> meetings 质量非常不错（v1.0 验证跑通）

## 10. 反馈

- 文档：`04-复盘与决策/` + `培训材料/`
- 故障：`故障处理手册_v1.0.md`
- 反馈：提供日志 + 错误信息给 Agent