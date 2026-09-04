"""
v3.0 kb_retriever.py - 双层 Query 架构(借鉴 PJ-001 v6.0 §11)

L1 entity_nav.py: 实体导航(纯规则,毫秒级)
L2 semantic_synthesis: 语义综合(LLM 调用)

主入口 query_wiki(query):
  1. 调用 entity_nav.nav(query) → matches
  2. 若 L1 命中 → 返回 L1 结果
  3. 若 L1 fallback → 调 LLM 综合答案 + 引用
  4. 返回 {level: "L1"|"L2", content, citations: []}
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))
from entity_nav import EntityNav


class KBRetriever:
    """双层 Query 检索器"""

    def __init__(self,
                 registry_path: Path,
                 persons_master_path: Path,
                 llm_client=None,
                 wiki_root: Path = None):
        """
        Args:
            llm_client: LLMClient 实例(L2 兜底需要);None 时 L2 用占位
            wiki_root: WIKI/ 根目录(用于收集 L2 引用)
        """
        self.entity_nav = EntityNav(registry_path, persons_master_path)
        self.llm = llm_client
        self.wiki_root = Path(wiki_root) if wiki_root else None

    def query_wiki(self, query: str, max_l1: int = 5) -> Dict:
        """主入口:返回查询结果

        Returns:
            {
                "level": "L1" | "L2",
                "query": str,
                "matches": [L1 命中] | [],
                "synthesis": str | None,   # L2 综合答案
                "citations": [wiki paths],  # L2 引用
                "fallback_reason": str | None
            }
        """
        # L1
        l1_result = self.entity_nav.nav(query)
        if l1_result["matches"] and not l1_result["fallback_to_llm"]:
            matches = l1_result["matches"][:max_l1]
            return {
                "level": "L1",
                "query": query,
                "matches": matches,
                "synthesis": None,
                "citations": [],
                "fallback_reason": None,
            }

        # L2 fallback
        return self._query_l2(query, l1_result)

    def _query_l2(self, query: str, l1_result: dict) -> Dict:
        """L2 语义综合:用 LLM 综合答案"""
        if not self.llm:
            # 无 LLM,占位返回
            return self._query_l2_stub(query, l1_result)

        # 构造 prompt
        system_prompt = """你是王老师的个人知识库助手。基于已知的人物、机构、判断、决策信息,
用中文回答王老师的提问。回答中必须:
1. 引用具体的来源(meeting 日期 / person name / org name)
2. 简洁准确,不编造
3. 如有不确定,明确说明
"""
        user_prompt = self._build_l2_prompt(query, l1_result)
        try:
            synthesis = self.llm.call(user_prompt, system=system_prompt,
                                      max_tokens=8000)  # v3.0 S10: 升 8000
        except Exception as e:
            synthesis = f"[L2 错误: {e}]"

        citations = self._collect_citations(l1_result)

        return {
            "level": "L2",
            "query": query,
            "matches": l1_result.get("matches", []),
            "synthesis": synthesis,
            "citations": citations,
            "fallback_reason": "L1 无精确匹配 或 查询是综合类",
        }

    def _query_l2_stub(self, query: str, l1_result: dict) -> Dict:
        """无 LLM 时的占位返回(供 L1 测试用)"""
        matches = l1_result.get("matches", [])
        if matches:
            content = (
                f"[L2 Stub] 查询「{query}」命中 {len(matches)} 个实体:\n"
                + "\n".join(f"  - {m['canonical_name']} ({m['occurrences']} 次出现)"
                            for m in matches)
            )
        else:
            content = f"[L2 Stub] 查询「{query}」未找到匹配。检查 entity_nav L1 提取。"

        return {
            "level": "L2",
            "query": query,
            "matches": matches,
            "synthesis": content,
            "citations": [],
            "fallback_reason": "no LLM injected (stub mode)",
        }

    def _build_l2_prompt(self, query: str, l1_result: dict) -> str:
        matches = l1_result.get("matches", [])
        parts = [f"王老师的问题:{query}\n"]

        if matches:
            parts.append(f"\n已知相关实体(共 {len(matches)} 个):")
            for m in matches:
                parts.append(f"- {m['type']}: {m['canonical_name']} "
                             f"({m['occurrences']} 次出现)")

        parts.append("\n请基于已知信息回答王老师的问题。"
                     "如信息不足,明确说明。")
        return "\n".join(parts)

    def _collect_citations(self, l1_result: dict) -> List[str]:
        """从 L1 命中实体收集 wiki 路径作为引用"""
        if not self.wiki_root:
            return []
        paths = []
        for m in l1_result.get("matches", []):
            entity_type = m["type"]
            if entity_type == "organization":
                p = self.wiki_root / "Entities" / "Organizations" / f"{m['canonical_name']}.md"
            elif entity_type == "person":
                p = self.wiki_root / "Entities" / "Persons" / f"{m['canonical_name']}.md"
            else:
                continue
            if p.exists():
                paths.append(str(p.relative_to(self.wiki_root)))
        return paths


# ============ CLI ============

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--persons-master", required=True)
    parser.add_argument("--wiki-root")
    parser.add_argument("--stub", action="store_true",
                       help="L2 用 stub,不调 LLM")
    args = parser.parse_args()

    llm = None if args.stub else None   # TODO 真实接入
    retriever = KBRetriever(
        registry_path=Path(args.registry),
        persons_master_path=Path(args.persons_master),
        llm_client=llm,
        wiki_root=Path(args.wiki_root) if args.wiki_root else None,
    )
    result = retriever.query_wiki(args.query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
