"""
S12: WIKI 写入（规则）
- 生成 5 类 WIKI Markdown
  1. meetings（已实现）
  2. persons（新增）
  3. concepts（新增）
  4. judgments（新增）
  5. comparisons（新增）
- 含完整 12 步结果
"""
from pathlib import Path
from typing import Dict, List


def s12_write_wiki(state: Dict, output_dir: Path) -> str:
    """生成 meeting Markdown 文件"""
    s1 = state["s1"]
    date = s1["date"]
    title = s1["title"]
    content_hash = state["content_hash"]

    md = f"""---
date: {date}
title: "{title}"
type: meeting
file_hash: {content_hash}
source: {state['sample']}
generated_at: 2026-09-04
generator: pj102-llm-meetingkb-v3.0
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
content_hash: {content_hash}
# === v6.1 P-4 meeting_type 6 类 ===
meeting_type: {state['s2'].get('scene_type', 'other')}
meeting_subtype: {state['s2'].get('scene_subtype', 'N/A')}
is_external_knowledge: {state['s2'].get('is_external_knowledge', False)}
# === v6.1 P-1 [判断:] 标注(已嵌入 body) ===
# === v7.0 ldamc 5 维自检(从 s10_cognitive 真实读取) ===
ldamc:
  lost: "{state.get('s10', {}).get('ldamc', {}).get('lost', '暂无')}"
  different: "{state.get('s10', {}).get('ldamc', {}).get('different', '暂无')}"
  added: "{state.get('s10', {}).get('ldamc', {}).get('added', '暂无')}"
  more: "{state.get('s10', {}).get('ldamc', {}).get('more', '暂无')}"
  connected: {state.get('s10', {}).get('ldamc', {}).get('connected', [])}
# === v7.0 §8.1 必填 ===
status_stage: compiled
value_grade: B
---

# {title}

## 📌 基础信息（S1）
- **日期**: {date}
- **录音时间**: {s1.get('recording_time', 'N/A')}
- **原文大小**: {s1['char_count']:,} 字符
- **估计时长**: {s1.get('duration_estimate', '')}

## 🎬 场景识别（S2）
- **场景类型**: {state['s2'].get('scene_type', 'N/A')}
- **视角**: {state['s2'].get('perspective', 'N/A')}
- **理由**: {state['s2'].get('scene_reason', 'N/A')}
- **置信度**: {state['s2'].get('confidence', 'N/A')}

## 📋 标准摘要（S3）

### 一句话总结
{state['s3'].get('one_sentence', 'N/A')}

### 背景
{state['s3'].get('background', 'N/A')}

### 问题
{state['s3'].get('problem', 'N/A')}

### 方法
{state['s3'].get('approach', 'N/A')}

### 结果
{state['s3'].get('outcome', 'N/A')}

### 王老师洞察
{state['s3'].get('insight', 'N/A')}

## 🔍 FJV 三分法（S4）

### 事实（Fact）
"""
    for f in state['s4'].get('facts', []):
        md += f"- {f}\n"
    if not state['s4'].get('facts'):
        md += "- （无）\n"

    md += "\n### 判断（Judgment · 王老师本人观点）\n"
    for j in state['s4'].get('judgments', []):
        md += f"- {j}\n"
    if not state['s4'].get('judgments'):
        md += "- （无）\n"

    md += "\n### 价值（Value）\n"
    for v in state['s4'].get('values', []):
        md += f"- {v}\n"
    if not state['s4'].get('values'):
        md += "- （无）\n"

    md += "\n## 🧠 隐性知识（S5 · 3 次子调用）\n\n### 体验性\n"
    for e in state['s5'].get('experiential', []):
        md += f"- {e}\n"
    if not state['s5'].get('experiential'):
        md += "- （无）\n"

    md += "\n### 判断性\n"
    for j in state['s5'].get('judgmental', []):
        md += f"- {j}\n"
    if not state['s5'].get('judgmental'):
        md += "- （无）\n"

    md += "\n### 关系性\n"
    for r in state['s5'].get('relational', []):
        md += f"- {r}\n"
    if not state['s5'].get('relational'):
        md += "- （无）\n"

    md += "\n## 🏷️ 5 类实体（S6）\n\n### 人物\n"
    for p in state['s6'].get('persons', []):
        if isinstance(p, dict):
            md += f"- **{p.get('name', '')}** - {p.get('role', '')} ({p.get('relationship', '')})\n"
        else:
            md += f"- {p}\n"
    if not state['s6'].get('persons'):
        md += "- （无）\n"

    md += "\n### 机构\n"
    for o in state['s6'].get('organizations', []):
        if isinstance(o, dict):
            md += f"- **{o.get('name', '')}** ({o.get('type', '')}) - {o.get('role', '')}\n"
        else:
            md += f"- {o}\n"
    if not state['s6'].get('organizations'):
        md += "- （无）\n"

    md += "\n### 概念\n"
    for c in state['s6'].get('concepts', []):
        if isinstance(c, dict):
            md += f"- **{c.get('name', '')}** - {c.get('definition', '')}\n"
        else:
            md += f"- {c}\n"
    if not state['s6'].get('concepts'):
        md += "- （无）\n"

    md += "\n### 产品\n"
    for p in state['s6'].get('products', []):
        if isinstance(p, dict):
            md += f"- **{p.get('name', '')}** ({p.get('type', '')}) - {p.get('description', '')}\n"
        else:
            md += f"- {p}\n"
    if not state['s6'].get('products'):
        md += "- （无）\n"

    md += "\n### 项目\n"
    for p in state['s6'].get('projects', []):
        if isinstance(p, dict):
            md += f"- **{p.get('name', '')}** ({p.get('status', '')}) - {p.get('description', '')}\n"
        else:
            md += f"- {p}\n"
    if not state['s6'].get('projects'):
        md += "- （无）\n"

    md += "\n## ✅ 决策和行动项（S7）\n\n### 关键决策\n"
    for d in state['s7'].get('decisions', []):
        if isinstance(d, dict):
            md += f"- **{d.get('decision', '')}** (决策人: {d.get('owner', 'N/A')})\n"
            if d.get('reason'):
                md += f"  - 理由: {d['reason']}\n"
            if d.get('deadline'):
                md += f"  - 期限: {d['deadline']}\n"
        else:
            md += f"- {d}\n"
    if not state['s7'].get('decisions'):
        md += "- （无）\n"

    md += "\n### 行动项\n"
    for a in state['s7'].get('action_items', []):
        if isinstance(a, dict):
            md += f"- **{a.get('action', '')}** (负责人: {a.get('owner', 'N/A')}, 期限: {a.get('deadline', 'N/A')})\n"
        else:
            md += f"- {a}\n"
    if not state['s7'].get('action_items'):
        md += "- （无）\n"

    md += "\n## ⚠️ 风险与盲区（S8）\n\n### 风险\n"
    for r in state['s8'].get('risks', []):
        if isinstance(r, dict):
            md += f"- **{r.get('risk', '')}** (影响: {r.get('impact', 'N/A')})\n"
        else:
            md += f"- {r}\n"
    if not state['s8'].get('risks'):
        md += "- （无）\n"

    md += "\n### 盲区\n"
    for b in state['s8'].get('blindspots', []):
        if isinstance(b, dict):
            md += f"- {b.get('blindspot', '')}\n"
        else:
            md += f"- {b}\n"
    if not state['s8'].get('blindspots'):
        md += "- （无）\n"

    md += "\n## 📚 知识归类（S9）\n"
    md += f"- **类型**: {state['s9'].get('knowledge_type', 'N/A')}\n"
    tags = state['s9'].get('tags', [])
    md += f"- **标签**: {', '.join(tags) if tags else '（无）'}\n"
    reuse = state['s9'].get('reuse_scenarios', [])
    md += f"- **复用场景**: {', '.join(reuse) if reuse else '（无）'}\n"

    md += "\n## 🧬 认知提炼（S10）\n\n### 认知模式\n"
    for c in state['s10'].get('cognitive_refinement', []):
        md += f"- {c}\n"
    if not state['s10'].get('cognitive_refinement'):
        md += "- （无）\n"

    dhm = state['s10'].get('digital_human_material', {})
    if isinstance(dhm, dict) and dhm:
        md += "\n### 数字人素材\n"
        md += f"- **说话风格**: {dhm.get('speaking_style', 'N/A')}\n"
        words = dhm.get('frequently_used_words', [])
        md += f"- **常用词**: {', '.join(words) if words else '（无）'}\n"
        md += f"- **思考框架**: {dhm.get('thinking_framework', 'N/A')}\n"

    md += "\n## ⭐ 价值评级（S11）\n"
    s11 = state['s11']
    md += f"- **相关度**: {s11.get('relevance', 0):.2f}\n"
    md += f"- **可行动性**: {s11.get('actionability', 0):.2f}\n"
    md += f"- **新颖性**: {s11.get('innovation', 0):.2f}\n"
    md += f"- **综合价值**: **{s11.get('value_score', 0):.2f}**\n"
    md += f"- **理由**: {s11.get('value_reason', 'N/A')}\n"

    md += "\n## 📑 元信息\n"
    md += f"- **LLM Provider**: {state['_meta']['llm_provider']}\n"
    md += f"- **LLM Model**: {state['_meta']['llm_model']}\n"
    md += f"- **生成时间**: 2026-09-03\n"
    md += f"- **项目**: PJ-102-LLM-MeetingKB\n"

    out_file = output_dir / "meetings" / f"meeting_{date}_{content_hash}.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(md, encoding='utf-8')
    return str(out_file)


# ============================================================
# 4 类 WIKI 生成器（v1.1 补全）
# ============================================================

def s12_write_persons(state: Dict, output_dir: Path) -> List[str]:
    """从 S6 人物实体生成 persons WIKI"""
    written = []
    s1 = state["s1"]
    date = s1["date"]
    source = state["sample"]
    content_hash = state["content_hash"]

    for person in state.get('s6', {}).get('persons', []):
        if isinstance(person, dict):
            name = person.get('name', '').strip()
            if not name:
                continue
            # 用人物名生成稳定文件名
            safe_name = name.replace(' ', '_').replace('/', '_')
            md = f"""---
type: person
name: "{name}"
date: {date}
role: "{person.get('role', '')}"
relationship: "{person.get('relationship', '')}"
source_meeting: {source}
source_hash: {content_hash}
generated_at: 2026-09-04
generator: pj102-llm-meetingkb-v1.1
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
---

# {name}

## 👤 人物信息

- **姓名**: {name}
- **角色**: {person.get('role', 'N/A')}
- **与王老师关系**: {person.get('relationship', 'N/A')}

## 📅 出现会议

- **{s1.get('title', 'N/A')}** ({date})

## 🎯 在该会议中的活动

"""
            # 添加 S4 中与此人物相关的事实
            md += "### 关联事实\n"
            found = False
            for fact in state.get('s4', {}).get('facts', []):
                if name in fact or name[:2] in fact:
                    md += f"- {fact}\n"
                    found = True
            if not found:
                md += "- （无直接关联）\n"

            # 添加 S5 关系性
            md += "\n### 关联关系\n"
            found = False
            for rel in state.get('s5', {}).get('relational', []):
                if isinstance(rel, dict) and name in str(rel):
                    md += f"- {rel.get('relation', '')}: {rel.get('description', '')}\n"
                    found = True
            if not found:
                md += "- （无直接关联）\n"

            md += f"""
## 📊 价值评估

- **相关度**: {state.get('s11', {}).get('relevance', 0):.2f}
- **综合价值**: {state.get('s11', {}).get('value_score', 0):.2f}

## 📑 元信息

- **生成时间**: 2026-09-04
- **来源会议**: {source}
- **LLM**: {state['_meta']['llm_provider']} / {state['_meta']['llm_model']}
- **项目**: PJ-102-LLM-MeetingKB
"""

            out_file = output_dir / "persons" / f"person_{safe_name}_{content_hash[:8]}.md"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(md, encoding='utf-8')
            written.append(str(out_file))

    return written


def s12_write_concepts(state: Dict, output_dir: Path) -> List[str]:
    """从 S6 概念实体生成 concepts WIKI"""
    written = []
    s1 = state["s1"]
    date = s1["date"]
    source = state["sample"]
    content_hash = state["content_hash"]

    for concept in state.get('s6', {}).get('concepts', []):
        if isinstance(concept, dict):
            name = concept.get('name', '').strip()
            if not name:
                continue
            safe_name = name.replace(' ', '_').replace('/', '_')[:30]
            md = f"""---
type: concept
name: "{name}"
date: {date}
definition: "{concept.get('definition', '')}"
source_meeting: {source}
source_hash: {content_hash}
generated_at: 2026-09-04
generator: pj102-llm-meetingkb-v1.1
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
---

# {name}

## 📖 概念定义

{concept.get('definition', 'N/A')}

## 🔗 出现会议

- **{s1.get('title', 'N/A')}** ({date})

## 💡 相关讨论

"""
            # 添加 S3 中与此概念相关的内容
            s3 = state.get('s3', {})
            insight = s3.get('insight', '')
            if insight and (name in insight or name[:2] in insight):
                md += f"### 王老师洞察\n{insight}\n"

            md += f"""
## 📚 知识归类

- **类型**: {state.get('s9', {}).get('knowledge_type', 'N/A')}
- **标签**: {', '.join(state.get('s9', {}).get('tags', [])) or '（无）'}

## 📑 元信息

- **生成时间**: 2026-09-04
- **来源会议**: {source}
- **LLM**: {state['_meta']['llm_provider']} / {state['_meta']['llm_model']}
"""

            out_file = output_dir / "concepts" / f"concept_{safe_name}_{content_hash[:8]}.md"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(md, encoding='utf-8')
            written.append(str(out_file))

    return written


def s12_write_judgments(state: Dict, output_dir: Path) -> List[str]:
    """从 S4 判断生成论 judgments WIKI"""
    written = []
    s1 = state["s1"]
    date = s1["date"]
    source = state["sample"]
    content_hash = state["content_hash"]

    judgments = state.get('s4', {}).get('judgments', [])
    for i, j in enumerate(judgments, 1):
        if not j or not isinstance(j, str):
            continue
        # 取前 30 字作为标题
        title = j[:30].replace('/', '_').replace(':', '_')
        md = f"""---
type: judgment
title: "{j[:60]}"
date: {date}
author: "王老师本人观点"
source_meeting: {source}
source_hash: {content_hash}
generated_at: 2026-09-04
generator: pj102-llm-meetingkb-v1.1
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
---

# 判断 #{i}：{j[:50]}

## 💭 判断内容

{j}

## 🔗 来源会议

- **{s1.get('title', 'N/A')}** ({date})

## 📋 上下文

"""
        # 添加 S3 背景
        md += f"### 背景\n{state.get('s3', {}).get('background', 'N/A')}\n"

        # 添加相关事实
        md += "\n### 相关事实\n"
        facts = state.get('s4', {}).get('facts', [])
        for f in facts[:3]:
            md += f"- {f}\n"

        # 添加价值评估
        md += f"""
## ⭐ 价值评估

- **综合价值**: {state.get('s11', {}).get('value_score', 0):.2f}
- **可行动性**: {state.get('s11', {}).get('actionability', 0):.2f}

## 📑 元信息

- **生成时间**: 2026-09-04
- **来源会议**: {source}
- **LLM**: {state['_meta']['llm_provider']} / {state['_meta']['llm_model']}
"""

        out_file = output_dir / "judgments" / f"judgment_{date}_{content_hash[:8]}_{i}.md"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(md, encoding='utf-8')
        written.append(str(out_file))

    return written


def s12_write_comparisons(state: Dict, output_dir: Path) -> List[str]:
    """从 S6/S4 中识别比较关系，生成 comparisons WIKI"""
    written = []
    s1 = state["s1"]
    date = s1["date"]
    source = state["sample"]
    content_hash = state["content_hash"]

    # 从 S4 facts 中识别比较关系（包含"vs"、"对比"、"vs" 等关键词）
    facts = state.get('s4', {}).get('facts', [])
    comparisons_found = []
    for fact in facts:
        if isinstance(fact, str):
            if any(kw in fact for kw in [' vs ', '对比', '比较', '不同', '差异', '优劣势']):
                comparisons_found.append(fact)

    # 从 S5 关系中识别
    s5_rel = state.get('s5', {}).get('relational', [])
    for rel in s5_rel:
        if isinstance(rel, dict):
            desc = rel.get('description', '')
            if any(kw in desc for kw in ['对比', '比较', '差异', ' vs ']):
                comparisons_found.append(f"{rel.get('relation', '')}: {desc}")

    if not comparisons_found:
        return written

    # 合并为一个 comparisons 文件
    md = f"""---
type: comparison
date: {date}
source_meeting: {source}
source_hash: {content_hash}
comparison_count: {len(comparisons_found)}
generated_at: 2026-09-04
generator: pj102-llm-meetingkb-v1.1
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
---

# 比较关系 - {s1.get('title', 'N/A')}

## 📅 来源会议

- **{s1.get('title', 'N/A')}** ({date})

## 🔄 比较内容

"""
    for i, comp in enumerate(comparisons_found, 1):
        md += f"### 比较 #{i}\n{comp}\n\n\n"

    md += f"""
## 📑 元信息

- **比较数**: {len(comparisons_found)}
- **生成时间**: 2026-09-04
- **来源会议**: {source}
- **LLM**: {state['_meta']['llm_provider']} / {state['_meta']['llm_model']}
"""

    out_file = output_dir / "comparisons" / f"comparison_{date}_{content_hash[:8]}.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(md, encoding='utf-8')
    written.append(str(out_file))

    return written


def s12_write_all_5_types(state: Dict, output_dir: Path) -> Dict[str, List[str]]:
    """一次生成全部 5 类 WIKI，返回各类型产出列表"""
    result = {
        "meetings": [s12_write_wiki(state, output_dir)],
        "persons": s12_write_persons(state, output_dir),
        "concepts": s12_write_concepts(state, output_dir),
        "judgments": s12_write_judgments(state, output_dir),
        "comparisons": s12_write_comparisons(state, output_dir),
    }
    return result