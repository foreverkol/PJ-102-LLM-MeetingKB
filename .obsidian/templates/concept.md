---
type: concept
# ============================================
# @required 必填字段
# ============================================
name: "<% tp.file.title %>"
type: "concept"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
domain: ""
origin: ""
prerequisites: []
counter_examples: []
evolution: ""
source_ref: ""
source_meeting: ""
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: "concept_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:name / type / date / generator

## 📚 概念定义 (可选)

<% tp.file.cursor(1) %>

## 🔄 起源 (可选)

<% tp.file.cursor(2) %>

## ⚠️ 反例 (可选)

<% tp.file.cursor(3) %>

## 🔗 相关实体 (Dataview 自动)

\`\`\`dataview
LIST
FROM "concepts"
WHERE source_meeting = this.source_meeting AND file.name != this.file.name
SORT file.name ASC
\`\`\`