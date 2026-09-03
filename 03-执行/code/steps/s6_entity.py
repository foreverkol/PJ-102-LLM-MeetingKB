"""
S6: 5 类实体提取（LLM）
- persons: 人物
- organizations: 机构
- concepts: 概念
- products: 产品
- projects: 项目
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_client import LLMClient, safe_json_parse


def s6_entity_extraction(content: str, llm: LLMClient) -> dict:
    """LLM 提取 5 类实体"""
    excerpt = content[:8000]

    prompt = f"""从会议中提取 5 类实体，输出 JSON 格式：

会议内容（前 8000 字）：
{excerpt}

请输出：
{{
  "persons": [
    {{"name": "姓名", "role": "角色/职位", "relationship": "与王老师的关系"}}
  ],
  "organizations": [
    {{"name": "机构名", "type": "银行/政府/企业/机构", "role": "在本会议中的角色"}}
  ],
  "concepts": [
    {{"name": "概念名", "definition": "简短定义", "context": "在本会议中的语境"}}
  ],
  "products": [
    {{"name": "产品名", "type": "金融产品/科技产品", "description": "描述"}}
  ],
  "projects": [
    {{"name": "项目名", "status": "进行中/计划/已落地", "description": "描述"}}
  ]
}}

每类最多 5 条，只输出 JSON。
"""
    result = llm.call(prompt, max_tokens=2000)
    return safe_json_parse(result, {
        "persons": [], "organizations": [], "concepts": [], "products": [], "projects": [],
    })