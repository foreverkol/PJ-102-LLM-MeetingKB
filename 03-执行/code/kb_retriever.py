"""
v3.0 kb_retriever.py - 双层 Query 架构(借鉴 PJ-001 v6.0 §11)

L1 entity_nav.py: 实体导航(纯规则,毫秒级)
L2 semantic_synthesis: 语义综合(LLM 调用)

主入口 query_wiki(query):
  1. expand_query(query) - Sprint 19 P1-4 同义词扩展
  2. 调用 entity_nav.nav(query) → matches
  3. 若 L1 命中 → 返回 L1 结果
  4. 若 L1 fallback → 调 LLM 综合答案 + 引用
  5. 返回 {level: "L1"|"L2", content, citations: [], expanded_queries: []}
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))
from entity_nav import EntityNav


class KBRetriever:
    """双层 Query 检索器"""

    # Sprint 19 P1-4: 同义词扩展词典(Karpathy Query 推荐)
    SYNONYMS = {
        "供应链金融": ["产融结合", "贸易融资", "票据融资", "供应链"],
        "票交所": ["票交所", "交易所", "ECDS", "票交所系统"],
        "票据经纪": ["票据经纪业务", "票据经纪公司", "票据中介"],
        "浙商银行": ["浙商", "浙商总行", "浙商银行总行"],
        "深度数科": ["深度", "深公司", "深度数科CEO"],
        "票据业务": ["票据", "电票", "纸票", "银票", "商票"],
        "风控": ["风控", "风险控制", "风险经营", "风控产品"],
        "数据": ["数据", "数字化", "数据要素", "数据资产"],
        "可信": ["可信", "可信数据", "可信数据交互"],
        "供应链": ["供应链", "产业互联网", "产业链"],
        "数据表达": ["数据表达", "金融表达", "两个表达"],
        "为恩科技": ["为恩", "为恩科技"],
    }

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

    def expand_query(self, query: str) -> List[str]:
        """同义词扩展:返回原 query + 扩展 query 列表"""
        expanded = [query]
        for canonical, synonyms in self.SYNONYMS.items():
            if canonical in query:
                for syn in synonyms:
                    if syn != canonical:
                        new_query = query.replace(canonical, syn)
                        if new_query not in expanded:
                            expanded.append(new_query)
        return expanded

    def query_wiki(self, query: str, max_l1: int = 5) -> Dict:
        """主入口:返回查询结果

        Returns:
            {
                "level": "L1" | "L2",
                "query": str,
                "matches": [L1 命中] | [],
                "synthesis": str | None,
                "citations": [wiki paths],
                "fallback_reason": str | None
                "expanded_queries": [str]
            }
        """
        # Sprint 19 P1-4: 同义词扩展
        expanded = self.expand_query(query)

        # L1 — 优先用原 query,如果失败用扩展 query
        l1_result = self.entity_nav.nav(query)
        if not l1_result["matches"] or l1_result["fallback_to_llm"]:
            for eq in expanded[1:]:  # 跳过原 query
                eq_result = self.entity_nav.nav(eq)
                if eq_result["matches"] and not eq_result["fallback_to_llm"]:
                    l1_result = eq_result
                    break

        if l1_result["matches"] and not l1_result["fallback_to_llm"]:
            matches = l1_result["matches"][:max_l1]
            return {
                "level": "L1",
                "query": query,
                "matches": matches,
                "synthesis": None,
                "citations": [],
                "fallback_reason": None,
                "expanded_queries": expanded,
            }

        # L2 fallback
        return self._query_l2(query, l1_result, expanded)

    def _query_l2(self, query: str, l1_result: dict, expanded: List[str] = None) -> Dict:
        """L2 语义综合:用 LLM 综合答案"""
        if expanded is None:
            expanded = [query]
        if not self.llm:
            return self._query_l2_stub(query, l1_result)

        system_prompt = """你是王老师的个人知识库助手。基于已知的人物、机构、判断、决策信息,
用中文回答王老师的提问。回答中必须:
1. 引用具体的来源(meeting 日期 / person name / org name)
2. 简洁准确,不编造
3. 如有不确定,明确说明
"""
        user_prompt = self._build_l2_prompt(query, l1_result)
        try:
            synthesis = self.llm.call(user_prompt, system=system_prompt,
                                      max_tokens=524288)
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
            "expanded_queries": expanded,
        }

    def _query_l2_stub(self, query: str, l1_result: dict) -> Dict:
        """L2 stub — 无 LLM 时的占位"""
        return {
            "level": "L2",
            "query": query,
            "matches": l1_result.get("matches", []),
            "synthesis": f"[L2 stub] 基于 L1 命中,{len(l1_result.get('matches', []))} 个匹配;无 LLM 调用。",
            "citations": self._collect_citations(l1_result),
            "fallback_reason": "L1 无精确匹配 + 无 LLM",
        }

    def _build_l2_prompt(self, query: str, l1_result: dict) -> str:
        """构造 L2 prompt — 综合 L1 命中 + 文档"""
        lines = [f"用户问题:{query}", "", "已知信息:"]
        for m in l1_result.get("matches", [])[:5]:
            lines.append(f"- {m.get('canonical_name', m.get('name', '?'))}: {m.get('path', '?')}")
        lines.append("")
        lines.append("请基于以上信息回答用户问题。")
        return "\n".join(lines)

    def _collect_citations(self, l1_result: dict) -> List[str]:
        """从 L1 命中收集 wiki 路径"""
        paths = []
        for m in l1_result.get("matches", []):
            if "path" in m and self.wiki_root:
                p = Path(m["path"])
                if not p.is_absolute():
                    p = self.wiki_root / p
                if p.exists():
                    paths.append(str(p.relative_to(self.wiki_root)))
            elif "canonical_name" in m and self.wiki_root:
                p = self.wiki_root / "Entities" / "Persons" / f"{m['canonical_name']}.md"
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

    llm = None if args.stub else None
    retriever = KBRetriever(
        registry_path=Path(args.registry),
        persons_master_path=Path(args.persons_master),
        llm_client=llm,
        wiki_root=Path(args.wiki_root) if args.wiki_root else None,
    )
    result = retriever.query_wiki(args.query)
    print(json.dumps(result, ensure_ascii=False, indent=2))