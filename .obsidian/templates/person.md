---
type: person
name: "<% tp.file.title %>"
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: person_<% tp.date.now("YYYYMMDD_HHmmss") %>
org: ""
job_title: ""
relation_to_wang: <% tp.system.suggester(["客户", "合作伙伴", "银行", "同事", "友人", "其他"]) %>
trust_level: B
capabilities: []
thinking_framework: ""
values_beliefs: ""
decision_style: ""
emotional_tone: ""
value_chain_position: ""
business_relations: []
source_ref: ""
source_meeting: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 👤 人物信息

- **姓名**: <% tp.file.title %>
- **职位**: <% tp.file.cursor(1) %>
- **与王老师关系**: <% tp.system.suggester(["客户", "合作伙伴", "银行", "同事", "友人", "其他"]) %>

## 💭 思维框架

<% tp.file.cursor(2) %>

## 💎 价值观

<% tp.file.cursor(3) %>

## 🤝 业务关系

<% tp.file.cursor(4) %>

## 🔗 相关实体 (Dataview 自动)

\`\`\`dataview
LIST
FROM "persons"
WHERE source_meeting = this.source_meeting AND file.name != this.file.name
SORT file.name ASC
\`\`\`

\`\`\`dataview
LIST
FROM "meetings,concepts,judgments"
WHERE contains(related_persons, this.name) OR contains(related_persons, "<% tp.file.title %>")
LIMIT 10
\`\`\`
