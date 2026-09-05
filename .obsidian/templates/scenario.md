---
type: scenario
theme: "<% tp.file.title %>"
customer: ""
pain_point: ""
offering: ""
value_capture: ""
channel: ""
key_resources: []
key_constraints: []
hidden_assumptions: []
trigger_signals: []
failure_modes: []
source_ref: ""
source_meeting: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 🎯 客户与痛点

- **目标客户**: <% tp.file.cursor(1) %>
- **核心痛点**: <% tp.file.cursor(2) %>

## 💡 提供的价值

<% tp.file.cursor(3) %>

## 💰 价值捕获

<% tp.file.cursor(4) %>

## 📡 渠道

<% tp.file.cursor(5) %>
