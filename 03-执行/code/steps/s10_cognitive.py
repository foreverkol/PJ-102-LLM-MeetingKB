"""
S10: 认知提炼（LLM）
- cognitive_refinement: 王老师的认知模式
- digital_human_material: 数字人素材
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s10_cognitive_refine(content: str, llm: LLMClient) -> dict:
    """LLM 认知提炼 + 数字人"""
    excerpt = content[:6000]

    prompt = f"""从会议中提炼王老师的认知模式 + 数字人素材，输出 JSON：

会议内容：{excerpt}

请输出：
{{
  "cognitive_refinement": [
    "认知1：王老师对 X 的理解是...",
    "认知2：王老师的决策风格是..."
  ],
  "digital_human_material": {{
    "speaking_style": "王老师的说话风格特点",
    "frequently_used_words": ["词1", "词2", "词3"],
    "thinking_framework": "王老师的思考框架"
  }}
}}

只输出 JSON。
"""
    result = llm.call(prompt, max_tokens=1500)
    return safe_json_parse(result, {
        "cognitive_refinement": [],
        "digital_human_material": {},
    })