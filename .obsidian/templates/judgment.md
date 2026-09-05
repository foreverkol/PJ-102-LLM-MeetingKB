---
type: judgment
# ============================================
# @required 必填字段
# ============================================
topic_key: "<% tp.file.title %>"
judgment_id: "j_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
type: "judgment"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
statement: ""
judgment_type: ""
evidence_strength: "B"
evidence_chain: []
evolved_from: ""
evolved_to: ""
contradictions: []
counter_arguments: []
confidence_level: "B"
confidence_rationale: ""
source_ref: ""
source_meeting: ""
canonical_name: "<% tp.file.title %>"
aliases: []
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:topic_key / judgment_id / type / date / generator

## 💡 判断陈述 (可选)

<% tp.file.cursor(1) %>

## 🔍 证据链 (可选)

<% tp.file.cursor(2) %>

## ⚖️ 反方观点 (可选)

<% tp.file.cursor(3) %>

## 📊 置信度 (可选)

<% tp.file.cursor(4) %>