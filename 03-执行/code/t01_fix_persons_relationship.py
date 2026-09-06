#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
t01_fix_persons_relationship.py - T-01 persons relationship 字段自动修复

王老师 2026-09-06 OUT-OF-BAND '即启动 L4.1' → 实测启动。

v2 改进(2026-09-06):
  - 新增 --suggestions-file 参数,接受王老师已批改的 75 建议 JSON
  - apply 模式只填 JSON 中 suggested_relationship 非"未分类"的项
  - 安全机制:JSON 未填的 person 跳过(默认 dry-run 也不改)
  - 不擅自编造任何 relationship(王老师 9-04 抗幻觉铁律)

实测 (2026-09-06 10:43):
  - persons 总数: 99
  - 75 个 relationship 字段空
  - 12 个命中自动规则(CEO/团队/教授/专家等)
  - 63 个待王老师批改

用法:
    python3 t01_fix_persons_relationship.py --dry-run
    python3 t01_fix_persons_relationship.py --apply
        --suggestions-file path/to/王老师批改.json
    python3 t01_fix_persons_relationship.py --init-suggestions
        # 生成初始建议 JSON(75 个全部"未分类")
"""
import argparse
import json
import os
import sys
from pathlib import Path

WIKI_BASE = Path("/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/persons")
DEFAULT_SUGGESTIONS = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/04-复盘与决策/Sprint21_v3.1.0-rc1_子任务/T-01-75建议清单_待王老师审_v1.0.json")

# role → relationship 推断规则(扩展 v2)
ROLE_TO_RELATIONSHIP = {
    # 客户类
    "客户经理": "客户关系",
    "客户": "客户关系",
    "客户代表": "客户关系",
    "客户方": "客户关系",
    "客户总监": "客户关系",
    "客户老板": "客户关系",
    "签约方": "客户关系",
    # 银行类
    "行长": "银行联系人",
    "银行": "银行联系人",
    "客户经理(银行)": "银行联系人",
    "银行客户经理": "银行联系人",
    # 内部职能
    "律师": "法律顾问",
    "财务": "财务联系人",
    "评审人": "评审联系人",
    # 高管/团队
    "CEO": "客户关系",
    "创始人": "客户关系",
    "团队": "团队关系",
    "团队成员": "团队关系",
    "员工": "团队关系",
    "同事": "同事关系",
    # 学术
    "教授": "学术合作",
    "老师": "学术合作",
    # 专家/咨询
    "专家": "行业专家",
    "顾问": "顾问关系",
    # 投资
    "投资人": "投资关系",
    "投资": "投资关系",
    # 政府/媒体
    "政府": "政府关系",
    "媒体": "媒体关系",
    # 家庭/朋友
    "家庭": "家庭关系",
    "朋友": "朋友关系",
    # 同业
    "同行": "同业同行",
}


def parse_frontmatter(content: str) -> tuple:
    """解析 frontmatter, 返回 (fm_dict, body, raw_fm_text)"""
    if not content.startswith('---'):
        return {}, content, ""
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content, ""
    raw_fm = parts[1].strip()
    fm = {}
    for line in raw_fm.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2], raw_fm


def suggest_relationship(fm: dict, body: str, filename: str) -> str:
    """基于 role 字段建议 relationship"""
    role = fm.get('role', '').strip()
    # 1. 直接匹配
    if role in ROLE_TO_RELATIONSHIP:
        return ROLE_TO_RELATIONSHIP[role]
    # 2. 模糊匹配
    if '行长' in role or '银行' in role or '客户经理' in role:
        return '银行联系人'
    if '客户' in role or '老板' in role or '经理' in role:
        return '客户关系'
    if '律师' in role or '法务' in role:
        return '法律顾问'
    if '财务' in role or '会计' in role:
        return '财务联系人'
    if '评审' in role or '审批' in role:
        return '评审联系人'
    if 'CEO' in role or '创始人' in role or '控股' in role:
        return '客户关系'
    if '教授' in role or '老师' in role:
        return '学术合作'
    if '专家' in role or '博士' in role:
        return '行业专家'
    if '顾问' in role:
        return '顾问关系'
    if '投资人' in role or '投资' in role:
        return '投资关系'
    if '团队' in role or '成员' in role:
        return '团队关系'
    if '政府' in role or '国资' in role:
        return '政府关系'
    if '媒体' in role or '主持' in role:
        return '媒体关系'
    if '家长' in role or '家庭' in role or '子女' in role:
        return '家庭关系'
    if '朋友' in role:
        return '朋友关系'
    if '同事' in role or '同行' in role:
        return '同业同行'
    # 3. 兜底
    return '未分类(待人工确认)'


def init_suggestions_file(output_path: Path):
    """生成初始建议 JSON(75 个全部 '未分类(待人工确认)')"""
    suggestions = []
    for f in sorted(os.listdir(WIKI_BASE)):
        if not f.endswith('.md'):
            continue
        fp = WIKI_BASE / f
        content = fp.read_text(encoding='utf-8')
        fm, body, raw_fm = parse_frontmatter(content)
        rel = fm.get('relationship', '').strip()
        if rel and rel not in ['unknown', 'N/A', '[]', '{}', '未分类', '']:
            continue  # 已有有效 relationship,跳过
        suggested = suggest_relationship(fm, body, f)
        suggestions.append({
            'file': f,
            'name': fm.get('name', ''),
            'role': fm.get('role', ''),
            'current_relationship': rel,
            'suggested_relationship': suggested,
        })
    output_path.write_text(
        json.dumps(suggestions, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f"✅ 已生成初始建议:{output_path}")
    print(f"   总 {len(suggestions)} 个 person")
    sugg_count = sum(1 for s in suggestions if '未分类' not in s['suggested_relationship'])
    print(f"   可自动填:{sugg_count}")
    print(f"   需王老师批:{len(suggestions) - sugg_count}")


def load_suggestions(suggestions_file: Path) -> dict:
    """加载王老师已批改的建议,返回 {filename: suggested_relationship}"""
    if not suggestions_file.exists():
        print(f"❌ 建议文件不存在:{suggestions_file}")
        print(f"   先跑 --init-suggestions 生成初始建议")
        sys.exit(1)
    data = json.loads(suggestions_file.read_text(encoding='utf-8'))
    return {item['file']: item['suggested_relationship'] for item in data}


def main():
    parser = argparse.ArgumentParser(description="T-01 persons relationship 自动修复")
    parser.add_argument("--dry-run", action="store_true", default=True,
                       help="Dry run (默认)")
    parser.add_argument("--apply", action="store_true",
                       help="应用修改")
    parser.add_argument("--suggestions-file", type=str,
                       default=str(DEFAULT_SUGGESTIONS),
                       help=f"王老师批改的建议 JSON (默认:{DEFAULT_SUGGESTIONS.name})")
    parser.add_argument("--init-suggestions", action="store_true",
                       help="生成初始建议 JSON")
    parser.add_argument("--output", default="/tmp/pj102-t01-suggestions.json",
                       help="建议输出文件 (dry-run 默认)")
    args = parser.parse_args()

    if args.init_suggestions:
        init_suggestions_file(Path(args.suggestions_file))
        return 0

    apply_mode = args.apply
    suggestions_file = Path(args.suggestions_file)

    print("=" * 75)
    print("T-01 persons relationship 自动修复 (v2)")
    print("=" * 75)
    print(f"模式: {'APPLY' if apply_mode else 'DRY-RUN(只报告不修改)'}")
    print(f"建议文件: {suggestions_file}")
    print()

    if not WIKI_BASE.exists():
        print(f"❌ Wiki 目录不存在:{WIKI_BASE}")
        return 1

    # 加载王老师批改
    approved = load_suggestions(suggestions_file)
    print(f"王老师已批改:{len(approved)} 个 person")
    approved_count = sum(1 for r in approved.values() if '未分类' not in r)
    print(f"  已填 relationship:{approved_count}")
    print(f"  仍待批:{len(approved) - approved_count}")
    print()

    modified = 0
    skipped_already = 0
    skipped_manual = 0
    skipped_no_match = 0

    for f in sorted(os.listdir(WIKI_BASE)):
        if not f.endswith('.md'):
            continue
        fp = WIKI_BASE / f
        content = fp.read_text(encoding='utf-8')
        fm, body, raw_fm = parse_frontmatter(content)
        rel = fm.get('relationship', '').strip()

        # 已存在有效 relationship,跳过
        if rel and rel not in ['unknown', 'N/A', '[]', '{}', '未分类', '']:
            skipped_already += 1
            continue

        # 不在王老师批改清单,跳过(防漂移)
        if f not in approved:
            skipped_no_match += 1
            continue

        suggested = approved[f]

        # 王老师未填(仍"未分类"),跳过
        if '未分类' in suggested:
            skipped_manual += 1
            continue

        if apply_mode:
            # 安全机制:用新 frontmatter 重建
            new_lines = []
            for line in raw_fm.split('\n'):
                if line.strip().startswith('relationship:'):
                    continue
                new_lines.append(line)
            new_lines.append(f'relationship: "{suggested}"')
            new_fm = '\n'.join(new_lines)
            new_content = content.replace(raw_fm, new_fm, 1)
            fp.write_text(new_content, encoding='utf-8')
            modified += 1

    # 统计
    print(f"扫描文件: {sum(1 for f in os.listdir(WIKI_BASE) if f.endswith('.md'))}")
    print(f"已存在有效 relationship: {skipped_already}")
    print(f"不在王老师批改清单: {skipped_no_match}")
    print(f"王老师未填(仍'未分类'): {skipped_manual}")

    if apply_mode:
        print(f"\n✅ 已修改: {modified} 个文件")
        print(f"⏸️  仍待王老师批: {skipped_manual} 个")
    else:
        print(f"\n🔍 Dry-run 完成。")
        print(f"   预计 apply 会修改: {approved_count} 个文件")
        print(f"   如要应用: --apply")

    return 0


if __name__ == "__main__":
    sys.exit(main())