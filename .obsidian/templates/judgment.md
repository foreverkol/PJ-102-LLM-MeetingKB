---
type: judgment
topic_key: "<% tp.file.title %>"
judgment_id: j_<% tp.date.now("YYYYMMDD_HHmmss") %>
statement: ""
judgment_type: <% tp.system.suggester(["战略判断", "战术判断", "风险判断", "机会判断", "其他"]) %>
evidence_strength: B
evidence_chain: []
evolved_from: ""
evolved_to: ""
contradictions: []
counter_arguments: []
confidence_level: B
confidence_rationale: ""
source_ref: ""
source_meeting: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 💡 判断陈述

<% tp.file.cursor(1) %>

## 🔍 证据链

<% tp.file.cursor(2) %>

## ⚖️ 反方观点

<% tp.file.cursor(3) %>

## 📊 置信度

<% tp.file.cursor(4) %>
