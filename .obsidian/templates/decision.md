---
type: decision
problem: ""
alternatives: []
chosen: ""
reason: ""
outcome: ""
constraints: []
review_trigger: ""
date: <% tp.date.now("YYYY-MM-DD") %>
value_grade: B
source_ref: ""
source_meeting: ""
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 🎯 问题

<% tp.file.cursor(1) %>

## 🔄 备选方案

<% tp.file.cursor(2) %>

## ✅ 已选方案

<% tp.file.cursor(3) %>

## 📋 结果

<% tp.file.cursor(4) %>
