# 🤖 PJ-102-LLM-MeetingKB · workbuddy 完整接入提示词

> **这份提示词给 workbuddy**（腾讯 Agent 工具）
> **复制整段粘贴到 workbuddy 即可**
> **workbuddy 会自动按 5 阶段执行**

---

## 📋 完整提示词（一次性复制）

```
你是 workbuddy AI Agent。本任务：完整复制 PJ-102-LLM-MeetingKB 项目。

## 项目背景

PJ-102-LLM-MeetingKB 是一个完整的会议转写→知识库系统，使用 12 步 LLM Pipeline + MiniMax M3。
项目地址：https://github.com/foreverkol/PJ-102-LLM-MeetingKB
当前版本：v1.0.0
状态：已验证质量（10 个样本成功）

## 你的目标

1. 完整克隆项目到本地 Windows 环境
2. 阅读并理解所有核心文档
3. 配置环境变量（API key）
4. 跑通烟雾测试
5. 复制源文件并跑批
6. 在你的环境中具备运行该 pipeline 的能力

## 任务流程（5 阶段）

### 阶段 1：克隆项目（预计 5 分钟）

请执行：
1. 在你的工作目录创建 PJ-Projects 文件夹
2. 打开 PowerShell 或 CMD，cd 到该目录
3. 执行：git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
   （如果 git 不可用，下载 https://github.com/foreverkol/PJ-102-LLM-MeetingKB/releases/download/v1.0.0/pj102-v1.0.0.tar.gz 并解压）
4. cd PJ-102-LLM-MeetingKB
5. 列出所有文件，统计数量

完成后报告：
- 项目完整路径
- 文件总数
- README.md 的核心内容

### 阶段 2：阅读核心文档（预计 15 分钟）

按顺序阅读以下 5 个文档，每个文档阅读后用 1 段话告诉我你的理解：

1. README.md（5 分钟）
2. WORKBUDDY_GUIDE.md（专门给你的接入指南）
3. 培训材料/使用手册_v1.0.md
4. 02-设计/系统架构_v1.0.md
5. 03-执行/code/pipeline.py

完成 5 个文档阅读后，总结：
- 这个项目做什么？
- 12 步 Pipeline 如何工作？
- 5 类 WIKI 是什么？

### 阶段 3：配置环境（预计 10 分钟）

执行：
1. 复制配置文件：
   copy config\.env.example .env

2. 编辑 .env，填入：
   MINIMAX_API_KEY=<API key，需要询问用户获取>
   MINIMAX_CN_BASE_URL=https://api.minimaxi.com/v1

3. 验证环境：
   python --version  # 应 3.11+
   pip list  # 检查依赖

4. 跑烟雾测试（关键！）：
   python tests/unit/smoke_test.py

完成后报告：
- Python 版本
- 烟雾测试结果（必须 9/9 通过）
- 任何失败详情

### 阶段 4：复制源文件 + 跑批（预计 30 分钟）

执行：
1. 创建源文件目录（如不存在）：
   mkdir system\data\raw

2. 询问用户：你的会议录音原文文件在哪里？
   （用户应将 .md 格式的会议录音文件复制到 system\data\raw\）

3. 生成索引：
   python -c "import json, hashlib, re; from pathlib import Path; SRC = Path('system/data/raw'); samples = []; 
[exec for f in sorted(SRC.glob('*.md')): content = f.read_text(encoding='utf-8'); h = hashlib.sha256(content.encode()).hexdigest()[:12]; m = re.search(r'(202[0-9])([0-9]{2})([0-9]{2})', f.name); date = f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else 'unknown'; samples.append({'filename': f.name, 'content_hash': h, 'date': date, 'size_bytes': len(content)}); 
Path('system/data/index.json').write_text(json.dumps({'version': 'v1.0', 'sample_count': len(samples), 'samples': samples}, ensure_ascii=False, indent=2), encoding='utf-8'); print(f'Indexed {len(samples)} samples')"

4. 跑 5 个样本（验证流程）：
   cd 03-执行\code
   python pipeline.py --limit 5

5. 查看 WIKI 输出位置：../../02-知识库/PJ-102-LLM-MeetingKB/meetings/

完成后报告：
- 索引生成的样本数
- 跑批成功率
- WIKI 平均大小
- 任何错误

### 阶段 5：全量跑批（预计 9 小时后台，可选）

询问用户是否需要跑全量。如果需要：
1. 后台执行：
   cd 03-执行\code
   start /b python pipeline.py > pj102_full.log 2>&1

2. 监控进度：
   type pj102_full.log

3. 完成后报告：成功/失败数、总耗时、总 WIKI 数

## ⚠️ 关键修复（必须记住）

1. **MiniMax base_url 必须是 `api.minimaxi.com`**，不是 `api.minimax.chat`
2. **端点路径 `/text/chatcompletion_v2`**，不带 `/v1` 前缀
3. **Python 相对 import 用绝对路径**（不能 `from .. import`）
4. **PROJECT_ROOT 是 3 层**（不是 4 层）
5. **JSON 容错解析**：LLM 返回可能含 markdown 包裹，已实现自动处理

## 🛠️ 故障处理

如果出错：
1. 查看 system/logs/ 下的日志
2. 查阅 04-复盘与决策/故障处理手册_v1.0.md
3. 查阅 培训材料/FAQ_v1.0.md
4. 检查环境变量是否正确设置

## ✅ 验证清单

完成后必须确认：
- [ ] 项目已克隆
- [ ] 5 个核心文档已读并理解
- [ ] .env 已配置（API key > 100 字符）
- [ ] 烟雾测试 9/9 通过
- [ ] 源文件已复制 + 索引生成
- [ ] 5 个样本跑通
- [ ] WIKI 输出到正确位置

## 🎯 最终目标

完成后你（workbuddy）应该具备：
1. 100% 理解 PJ-102 项目的能力
2. 在你环境运行该 pipeline 的能力
3. 处理用户提供的会议录音的能力
4. 改进和扩展项目的能力

## 📞 完成后请总结

最终请总结：
1. 你成功理解了多少？
2. 你能在你的环境跑通 pipeline 吗？
3. 你能处理用户的会议录音吗？
4. 你能改进这个项目吗？如果能，给出具体建议。

---

请开始阶段 1。
```

---

## 🚀 王老师使用方法

### 选项 A：一次性复制完整提示词（推荐）

1. 复制上面"完整提示词"整段（在 ``` 之间）
2. 粘贴到 workbuddy
3. 按回车执行
4. workbuddy 会自动按 5 阶段执行

### 选项 B：分阶段执行

如果 workbuddy 不够智能，可以分阶段：

**阶段 1 提示词**：
```
请执行：克隆 PJ-102-LLM-MeetingKB 项目
git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
完成后报告项目路径和文件数量。
```

**阶段 2 提示词**：
```
请阅读 PJ-102-LLM-MeetingKB 项目的 5 个核心文档：
README.md / WORKBUDDY_GUIDE.md / 培训材料/使用手册_v1.0.md / 02-设计/系统架构_v1.0.md / 03-执行/code/pipeline.py
每个文档阅读后用 1 段话总结。
```

**阶段 3 提示词**：
```
请配置 PJ-102-LLM-MeetingKB 环境：
1. copy config\.env.example .env
2. 编辑 .env 填入 MINIMAX_API_KEY
3. python tests/unit/smoke_test.py
完成后报告测试结果。
```

**阶段 4 提示词**：
```
请复制源文件并跑批：
1. mkdir system\data\raw
2. 让用户提供源文件到 system\data\raw\
3. python pipeline.py --limit 5
完成后报告跑批结果。
```

---

## 💡 提示词技巧

### 让 workbuddy 更高效
- 提供具体路径和命令
- 明确每个阶段的预期输出
- 关键修复要醒目（用 ⚠️ 标记）

### 如果 workbuddy 卡住
- 给一个简化的版本
- 一次只执行一个命令
- 让 workbuddy 自己 debug

### 如果 workbuddy 报错
- 让它贴出完整错误信息
- 让它自己诊断原因
- 查阅 WORKBUDDY_GUIDE.md 中的故障处理

---

## 📋 完整文件清单

王老师您也可以把以下文件一起发给 workbuddy：

```
PJ-102-LLM-MeetingKB/
├── README.md（项目入口）
├── WORKBUDDY_GUIDE.md（专门给 AI Agent 的指南）
├── WORKBUDDY_OPERATIONS.md（人工操作手册）
├── WORKBUDDY_PROMPTS.md（本文件，给 workbuddy 的提示词）
├── 培训材料/使用手册_v1.0.md
├── 02-设计/系统架构_v1.0.md
├── 03-执行/code/（16 个 Python）
├── tests/unit/smoke_test.py
└── .env.example
```

workbuddy 收到这些文件后，按提示词执行即可。

---

## 🎯 王老师下一步

### 选项 A：直接使用本提示词
- 复制"完整提示词"
- 给 workbuddy 执行

### 选项 B：让我针对 workbuddy 优化
- 如果您告诉我 workbuddy 的具体能力
- 我可以调整提示词

### 选项 C：先小范围测试
- 用一个简单任务测试 workbuddy
- 确认它能理解命令
- 再给完整任务

我推荐**选项 A**——提示词已写好，王老师您直接复制粘贴即可。
