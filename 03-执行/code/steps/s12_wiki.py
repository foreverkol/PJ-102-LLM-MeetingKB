"""
S12: WIKI 写入（规则）
- 生成 meeting Markdown
- 含完整 12 步结果
"""
from pathlib import Path
from typing import Dict


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
generated_at: 2026-09-03
generator: pj102-llm-meetingkb-v1.0
llm_provider: {state['_meta']['llm_provider']}
llm_model: {state['_meta']['llm_model']}
content_hash: {content_hash}
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