---
type: meeting
title: "<% tp.file.title %>"
date: <% tp.date.now("YYYY-MM-DD") %>
duration_min:
participants: []
key_topics: []
meeting_type: <% tp.system.suggester(["银行沟通", "客户拜访", "内部讨论", "外部会议", "其他"]) %>
meeting_subtype:
chapters: []
action_items: []
ldamc: ""
source_ref: "<% tp.date.now("YYYYMMDD_HHmmss") %>_xxx_原文.md"
source_meeting: "<% tp.date.now("YYYYMMDD_HHmmss") %>_xxx_原文.md"
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: meeting_<% tp.date.now("YYYYMMDD_HHmmss") %>
generator: pj102-templater-v1.0
value_grade: B
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 📅 会议信息

- **日期**: <% tp.date.now("YYYY-MM-DD") %>
- **时长**: <% tp.file.cursor(1) %> 分钟
- **类型**: <% tp.system.suggester(["银行沟通", "客户拜访", "内部讨论", "外部会议", "其他"]) %>

## 👥 参与人

<% tp.file.cursor(2) %>

## 📋 关键议题

<% tp.file.cursor(3) %>

## 🎯 行动项

<% tp.file.cursor(4) %>

## 🔗 相关实体 (Dataview 自动)

\`\`\`dataview
LIST
FROM "meetings"
WHERE source_meeting = "<% tp.date.now("YYYYMMDD_HHmmss") %>_xxx_原文.md" AND file.name != this.file.name
SORT file.name ASC
\`\`\`
