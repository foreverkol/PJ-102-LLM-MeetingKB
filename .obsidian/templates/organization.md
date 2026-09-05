---
type: organization
name: "<% tp.file.title %>"
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: org_<% tp.date.now("YYYYMMDD_HHmmss") %>
org_type: <% tp.system.suggester(["银行", "保理", "供应链", "科技", "助贷", "其他"]) %>
industry: <% tp.system.suggester(["银行金融", "供应链金融", "产业互联网", "金融科技", "电商", "其他"]) %>
cooperation_status: <% tp.system.suggester(["活跃", "潜在", "历史", "已终止"]) %>
relationship_depth: 单点接触
business_model: ""
competitive_moat: ""
value_chain_position: ""
strategic_value: ""
interaction_history: ""
source_ref: ""
source_meeting: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 🏢 机构信息

- **类型**: <% tp.system.suggester(["银行", "保理", "供应链", "科技", "助贷", "其他"]) %>
- **行业**: <% tp.system.suggester(["银行金融", "供应链金融", "产业互联网", "金融科技", "电商", "其他"]) %>
- **合作状态**: <% tp.system.suggester(["活跃", "潜在", "历史", "已终止"]) %>

## 💼 业务模式

<% tp.file.cursor(1) %>

## 🛡️ 竞争壁垒

<% tp.file.cursor(2) %>

## 🤝 互动历史

<% tp.file.cursor(3) %>
