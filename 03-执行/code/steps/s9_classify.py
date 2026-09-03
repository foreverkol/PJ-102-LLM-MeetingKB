"""
S9: 知识归类（LLM）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s9_knowledge_classify(content: str, llm: LLMClient) -> dict:
    """LLM 知识归类"""
    excerpt = content[:4000]

    prompt = f"""将本会议归类，输出 JSON 格式：

会议内容（前 4000 字）：{excerpt}

请输出：
{{
  "knowledge_type": "业务/技术/管理/财务/法律/营销/产品/其他",
  "tags": ["标签1", "标签2", "标签3"],
  "reuse_scenarios": ["可复用于..."]
}}

只输出 JSON。
"""
    result = llm.call(prompt, max_tokens=500)
    return safe_json_parse(result, {
        "knowledge_type": "其他",
        "tags": [],
        "reuse_scenarios": [],
    })