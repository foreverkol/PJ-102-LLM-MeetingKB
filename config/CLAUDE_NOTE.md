# CLAUDE_NOTE.md · PJ-102-LLM-MeetingKB

> 注意: 文件名是 CLAUDE_NOTE.md（避免系统保护冲突）

## 项目概览

PJ-102-LLM-MeetingKB 是基于 MiniMax M3 + 12 步 pipeline 的会议转写→知识库全流程处理独立项目。

## 关键特性

1. **完全独立** - 不依赖 PJ-001 任何子项目
2. **12 步 pipeline** - 每步独立 LLM 调用
3. **LLM 真实调用** - MiniMax M3（中国区）
4. **5 类 WIKI** - meeting / person / concept / judgment / comparison

## 关键命令

```bash
# 跑批
cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/code
python3 pipeline.py

# 测试
python3 pipeline.py --limit 13

# 跳过 LLM
python3 pipeline.py --no-llm
```

## 环境变量

```bash
export MINIMAX_API_KEY="..."  # 从 ~/.hermes/.env 读取
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"
```

## 注意事项

1. **不要修改其他项目** - PJ-102 是独立项目
2. **不要读取 PJ-001 WIKI** - 重新生成
3. **不要修改源文件** - `修改发言人转化/` 只读
4. **API key 从 ~/.hermes/.env 读取** - 不要硬编码

## 王老师认可

> meetings 质量非常不错（v1.0 13/13 验证）