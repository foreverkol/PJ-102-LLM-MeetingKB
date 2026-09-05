---
type: organization
# ============================================
# @required 必填字段
# ============================================
name: "<% tp.file.title %>"
canonical_name: "<% tp.file.title %>"
entity_id: "org_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
type: "organization"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
aliases: []
org_type: ""
industry: ""
cooperation_status: ""
relationship_depth: ""
business_model: ""
competitive_moat: ""
value_chain_position: ""
strategic_value: ""
interaction_history: ""
source_ref: ""
source_meeting: ""
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:name / canonical_name / entity_id / type / date / generator

## 🏢 机构信息

- **类型**: <% tp.system.suggester(["银行", "保理", "供应链", "科技", "助贷", "其他"]) %>

## 💼 业务模式 (可选)

<% tp.file.cursor(1) %>

## 🛡️ 竞争壁垒 (可选)

<% tp.file.cursor(2) %>

## 🤝 互动历史 (可选)

<% tp.file.cursor(3) %>