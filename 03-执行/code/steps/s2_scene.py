"""
S2: 场景识别（LLM）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s2_scene_recognition(content: str, llm: LLMClient) -> dict:
    """LLM 识别会议场景"""
    excerpt = content[:4000]

    prompt = f"""请分析以下会议转写，输出 JSON 格式的会议场景信息：

会议内容（前 4000 字）：
{excerpt}

请输出：
{{
  "scene_type": "client_visit/team_meeting/phone_call/internal_discuss/online_meeting/other",
  "perspective": "sales_market/tech_research/management/finance/operation/other",
  "scene_reason": "简要说明为什么是这种场景",
  "confidence": "high/medium/low"
}}

只输出 JSON，不要其他内容。
"""
    result = llm.call(prompt, max_tokens=500)
    return safe_json_parse(result, {
        "scene_type": "unknown",
        "perspective": "other",
        "scene_reason": "LLM 未返回",
        "confidence": "low",
    })