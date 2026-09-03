# PJ-102-LLM-MeetingKB · LLM 调用架构 v1.0

## 1. 支持的 Provider

| 优先级 | Provider | Model | 适用 |
|---|---|---|---|
| 1 (默认) | MiniMax M3 | MiniMax-Text-01 | 王老师指定，中国区 |
| 2 | DeepSeek | deepseek-chat | 备用 |
| 3 | OpenAI | gpt-4o-mini | 备用 |
| 4 | Anthropic | claude-3-haiku | 备用 |
| 5 | Mock | - | 测试 |

## 2. MiniMax M3 调用详情

### 2.1 关键参数
- **base_url**: `https://api.minimaxi.com/v1`（**注意：不是 api.minimax.chat**）
- **端点**: `text/chatcompletion_v2`（**注意：不带 /v1 前缀**）
- **Authorization**: `Bearer $MINIMAX_API_KEY`
- **Content-Type**: `application/json`

### 2.2 调用示例
```python
import urllib.request
import json

url = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
payload = {
    "model": "MiniMax-Text-01",
    "messages": [
        {"role": "system", "content": "你是一个专业的中文会议纪要分析师。"},
        {"role": "user", "content": prompt}
    ],
    "max_tokens": 2000,
    "temperature": 0.3
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('MINIMAX_API_KEY')}"
    }
)

with urllib.request.urlopen(req, timeout=60) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
```

## 3. 环境变量

| 变量 | 必需 | 说明 |
|---|---|---|
| `MINIMAX_API_KEY` | 是（生产）| 从 `~/.hermes/.env` 读取 |
| `MINIMAX_CN_BASE_URL` | 推荐 | `https://api.minimaxi.com/v1` |
| `DEEPSEEK_API_KEY` | 否（备用）| DeepSeek 备用 |
| `OPENAI_API_KEY` | 否（备用）| OpenAI 备用 |
| `ANTHROPIC_API_KEY` | 否（备用）| Anthropic 备用 |

## 4. 调用参数

### 4.1 全局参数
| 参数 | 值 | 理由 |
|---|---|---|
| temperature | 0.3 | 保证一致性，避免发散 |
| timeout | 60 秒 | 单次调用超时 |
| max_retries | 3 | 重试次数 |
| retry_delay | exponential (1s, 2s, 4s) | 限流重试 |

### 4.2 各步骤 max_tokens

| 步骤 | max_tokens | 理由 |
|---|---|---|
| S1 | - | 规则处理 |
| S2 | 500 | 场景识别 |
| S3 | 1500 | 标准摘要 6 字段 |
| S4 | 2000 | FJV 各 5 条 |
| S5 | 800 × 3 | 三次子调用 |
| S6 | 2000 | 5 类实体 |
| S7 | 2000 | 决策+行动 |
| S8 | 1500 | 风险+盲区 |
| S9 | 500 | 知识归类 |
| S10 | 1500 | 认知提炼 |
| S11 | 500 | 价值评级 |
| S12 | - | 写入 |

## 5. Prompt 设计原则

1. **明确 JSON 输出格式**：在 prompt 中给出 JSON schema 示例
2. **强调 "只输出 JSON"**：避免 LLM 输出解释性文字
3. **控制输入长度**：截取前 N 字符，避免超出 context window
4. **角色设定**：system message 给 LLM 一个明确身份
5. **示例引导**：必要时给出 few-shot examples

## 6. JSON 容错解析

### 6.1 问题类型
- LLM 返回 markdown 包裹（```json ... ```）
- LLM 返回多余解释文字
- JSON 中有未转义引号
- 尾随逗号

### 6.2 容错流程
```python
def _safe_json_parse(content, default):
    # 1. 移除 markdown 包裹
    content = re.sub(r"^```(?:(?!)))\s?",", "", content)
    content = re.sub(r"\s?\`$", "", content)
    
    # 2. 提取 JSON 块
    m = re.search(r"\{[\s\S]*\}", content)
    if m:
        content = m.group(0)
    
    # 3. 尝试解析
    try:
        return json.loads(content)
    except:
        pass
    
    # 4. 修复尾随逗号
    try:
        content = re.sub(r",\s*}", "}", content)
        content = re.sub(r",\s*]", "]", content)
        return json.loads(content)
    except:
        return default
```

## 7. 限流处理

### 7.1 检测
- HTTP 429 → 限流
- HTTP 5xx → 服务异常

### 7.2 重试
```python
def call_with_retry(self, prompt, max_retries=3):
    for attempt in in:
        try:
            return self.call(prompt)
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
            else:
                raise
    return ""
```

## 8. 监控与日志

```python
import logging
logging.basicConfig(filename='system/logs/pipeline.log', level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"S1 done: {file}")
logger.warning(f"S4 failed: {file}, retrying...")
logger.error(f"S9 critical fail: {file}")
```