# PJ-102-LLM-MeetingKB · 12步 Pipeline 详细设计 v1.0

## 1. 总体流程

```
输入: source_file (Path)
  ↓
读取 content
  ↓
12 步串行处理
  ↓
合并结果 → state: dict
  ↓
调用 writer.write_meeting(state) → 输出文件
  ↓
返回 state
```

## 2. 各步骤详细设计

### S1: 基础信息（规则，无需 LLM）

**输入**: filename + content

**处理逻辑**:
```python
def s1_basic_info(filename, content):
    # 1. 从文件名提取日期
    m = re.search(r'(202\d)(\d{2})(\d{2})', filename)
    date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    
    # 2. 从文件名提取标题
    title = re.sub(r'^202\d{5,6}_\d+', '', filename)
    title = re.sub(r'_原文\.md$', '', title).replace('_', ' ')
    
    # 3. 估计时长（按字符数）
    char_count = len(content)
    duration = max(1, char_count // 250)
    
    # 4. 提取录音时间
    time_match = re.search(r"录音交流开始时间[:：](\S+ \S+)", content)
    recording_time = time_match.group(1) if time_match else None
    
    return {
        "title": title,
        "date": date,
        "filename": filename,
        "char_count": char_count,
        "duration_estimate": f"约{duration}分钟",
        "recording_time": recording_time
    }
```

**输出示例**:
```json
{
  "title": "到西安与票圈郭小艳台州陈凌昌第一天的沟通",
  "date": "2026-08-02",
  "filename": "20260802_133331到西安与票圈郭小艳台州陈凌昌第一天的沟通_原文.md",
  "char_count": 100390,
  "duration_estimate": "约401分钟",
  "recording_time": "2026年08月02日 13:33"
}
```

### S2: 场景识别（LLM）

**输入**: content[:4000]

**Prompt**:
```
请分析以下会议转写，输出 JSON 格式的会议场景信息：

会议内容（前 4000 字）：
{excerpt}

请输出：
{
  "scene_type": "client_visit/team_meeting/phone_call/internal_discuss/online_meeting/other",
  "perspective": "sales_market/tech_research/management/finance/operation/other",
  "scene_reason": "简要说明为什么是这种场景",
  "confidence": "high/medium/low"
}

只输出 JSON，不要其他内容。
```

**输出示例**:
```json
{
  "scene_type": "client_visit",
  "perspective": "finance",
  "scene_reason": "围绕银行融资、政府民生工程",
  "confidence": "high"
}
```

### S3: 标准摘要（LLM）

**输入**: content[:6000]

**Prompt**: 6 字段标准摘要
- one_sentence（一句话）
- background（背景）
- problem（问题）
- approach（方法）
- outcome（结果）
- insight（王老师洞察）

**输出示例**: 6 字段完整

### S4: FJV 三分法（LLM）

**输入**: content[:8000]

**Prompt**: 5 facts + 5 judgments + 5 values

**输出示例**:
```json
{
  "facts": [
    "台州陈凌昌提到一个民生工程项目",
    ...
  ],
  "judgments": [
    "王老师认为当前中国大陆的股票市场在较长时间内会保持震荡",
    ...
  ],
  "values": [
    "通过与银行合作完成民生工程项目，可以获得稳定的收益",
    ...
  ]
}
```

### S5: 隐性知识（LLM × 3）

**输入**: content[:6000]

**3 次子调用**:
1. **体验性** (experiential): 亲身经历、案例、踩过的坑
2. **判断性** (judgmental): 思维模型、决策框架、判断标准
3. **关系性** (relational): 人脉网络、信任关系、合作模式

**输出示例**:
```json
{
  "experiential": [
    "王老师曾与一位朋友合作开展业务，但因对方挪用资金...",
    ...
  ],
  "judgmental": [
    "判断1: 王老师认为在处理复杂项目融资时...",
    ...
  ],
  "relational": [
    "人脉网络: 台州陈凌昌与工商银行温岭支行...",
    ...
  ]
}
```

### S6: 5 类实体（LLM）

**输入**: content[:8000]

**5 类**:
- persons: [{"name": ..., "role": ..., "relationship": ...}]
- organizations: [{"name": ..., "type": ..., "role": ...}]
- concepts: [{"name": ..., "definition": ..., "context": ...}]
- products: [{"name": ..., "type": ..., "description": ...}]
- projects: [{"name": ..., "status": ..., "description": ...}]

### S7: 决策+行动（LLM）

**输出**:
```json
{
  "decisions": [{"decision": ..., "owner": ..., "reason": ..., "deadline": ...}],
  "action_items": [{"action": ..., "owner": ..., "deadline": ..., "background": ...}]
}
```

### S8: 风险+盲区（LLM）

**输出**:
```json
{
  "risks": [{"risk": ..., "impact": "高/中/低", "mitigation": ...}],
  "blindspots": [{"blindspot": ..., "context": ...}],
  "uncertain": [...]
}
```

### S9: 知识归类（LLM）

**输出**:
```json
{
  "knowledge_type": "业务/技术/管理/财务/法律/营销/产品/其他",
  "tags": [...],
  "reuse_scenarios": [...]
}
```

### S10: 认知提炼（LLM）

**输出**:
```json
{
  "cognitive_refinement": [...],
  "digital_human_material": {
    "speaking_style": "...",
    "frequently_used_words": [...],
    "thinking_framework": "..."
  }
}
```

### S11: 价值评级（LLM）

**输出**:
```json
{
  "relevance": 0.85,
  "actionability": 0.7,
  "innovation": 0.6,
  "value_score": 0.73,
  "value_reason": "..."
}
```

### S12: WIKI 写入（规则）

**输入**: 完整 state (S1-S11)

**处理逻辑**:
```python
def write_meeting(state, output_dir):
    md = render_markdown(state)  # 模板渲染
    filename = f"meeting_{state['s1']['date']}_{content_hash}.md"
    path = output_dir / "meetings" / filename
    path.write_text(md, encoding='utf-8')
```

**Markdown 模板**:
- YAML frontmatter（date/title/type/file_hash/source/llm_provider/llm_model/content）
- 12 章节（每个 S 对应一节）

## 3. 串行处理流程

```python
def process_one(sample):
    content = read_file(sample)
    
    state = {}
    state['s1'] = s1_basic_info(sample['filename'], content)
    state['s2'] = s2_scene_recognition(content, llm)
    state['s3'] = s3_standard_summary(content, llm)
    state['s4'] = s4_fjv(content, llm)
    state['s5'] = s5_implicit_knowledge(content, llm)  # 3 次子调用
    state['s6'] = s6_entity_extraction(content, llm)
    state['s7'] = s7_action_decision(content, llm)
    state['s8'] = s8_risk_blindspot(content, llm)
    state['s9'] = s9_knowledge_classify(content, llm)
    state['s10'] = s10_cognitive_refine(content, llm)
    state['s11'] = s11_value_rating(content, llm)
    
    return state
```

## 4. 错误处理

每个步骤独立 try-except：
```python
try:
    result = llm_step(content, llm)
except Exception as e:
    log(f"Step X failed: {e}")
    result = default_value  # 不阻塞流程
```