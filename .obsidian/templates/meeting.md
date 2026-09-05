---
type: meeting
# ============================================
# @required 必填字段
# ============================================
title: "<% tp.file.title %>"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
type: "meeting"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
duration_min: 0
participants: []
key_topics: []
meeting_type: ""
meeting_subtype: ""
chapters: []
action_items: []
ldamc: ""
source_ref: ""
source_meeting: ""
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: "meeting_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
value_grade: "B"
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:title / date / type / generator

## 📅 会议信息

- **日期**: <% tp.date.now("YYYY-MM-DD") %>
- **时长**: <% tp.file.cursor(1) %> 分钟

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
WHERE source_meeting = this.source_meeting AND file.name != this.file.name
SORT file.name ASC
\`\`\`