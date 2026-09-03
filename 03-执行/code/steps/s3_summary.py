"""
S3: 标准摘要（LLM，6 字段）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s3_standard_summary(content: str, llm: LLMClient) -> dict:
    """LLM 生成标准摘要（6 字段）"""
    excerpt = content[:6000]

    prompt = f"""请为以下会议转写生成结构化摘要，输出 JSON 格式：

会议内容（前 6000 字）：
{excerpt}

请输出：
{{
  "one_sentence": "一句话总结（不超过 100 字）",
  "background": "会议背景（150-200 字）",
  "problem": "讨论的核心问题（100-150 字）",
  "approach": "讨论的方法/方案（150-200 字）",
  "outcome": "会议结果/结论（100-200 字）",
  "insight": "王老师的关键洞察（100-200 字）"
}}

只输出 JSON，不要其他内容。
"""
    result = llm.call(prompt, max_tokens=1500)
    return safe_json_parse(result, {
        "one_sentence": "（LLM 失败）",
        "background": "",
        "problem": "",
        "approach": "",
        "outcome": "",
        "insight": "",
    })