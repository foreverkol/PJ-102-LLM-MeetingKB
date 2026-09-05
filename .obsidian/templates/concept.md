---
type: concept
name: "<% tp.file.title %>"
domain: <% tp.system.suggester(["供应链金融", "票据业务", "保理业务", "助贷", "数据风控", "其他"]) %>
origin: ""
prerequisites: []
counter_examples: []
evolution: ""
source_ref: ""
source_meeting: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 📚 概念定义

<% tp.file.cursor(1) %>

## 🔄 起源

<% tp.file.cursor(2) %>

## ⚠️ 反例

<% tp.file.cursor(3) %>

## 🔗 相关实体 (Dataview 自动)

\`\`\`dataview
LIST
FROM "concepts"
WHERE source_meeting = this.source_meeting AND file.name != this.file.name
SORT file.name ASC
\`\`\`
