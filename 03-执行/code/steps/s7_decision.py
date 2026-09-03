"""
S7: 行动项+决策（LLM）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s7_action_decision(content: str, llm: LLMClient) -> dict:
    """LLM 提取决策和行动项"""
    excerpt = content[:6000]

    prompt = f"""从会议中提取决策和行动项，输出 JSON 格式：

会议内容（前 6000 字）：
{excerpt}

请输出：
{{
  "decisions": [
    {{"decision": "决策内容", "owner": "决策人", "reason": "理由", "deadline": "期限"}}
  ],
  "action_items": [
    {{"action": "行动内容", "owner": "负责人", "deadline": "期限", "background": "背景"}}
  ]
}}

每类最多 5 条，只输出 JSON。
"""
    result = llm.call(prompt, max_tokens=2000)
    return safe_json_parse(result, {
        "decisions": [], "action_items": [],
    })