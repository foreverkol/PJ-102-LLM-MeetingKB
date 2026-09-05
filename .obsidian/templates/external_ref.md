---
type: external_ref
# ============================================
# @required 必填字段
# ============================================
title: "<% tp.file.title %>"
type: "external_ref"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
source_url: ""
authors: ""
publication_date: ""
key_claims: []
can_update_internal: false
source_ref: ""
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: "ref_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:title / type / date / generator

## 🔗 链接 (可选)

<% tp.file.cursor(1) %>

## 👤 作者 (可选)

<% tp.file.cursor(2) %>

## 📌 关键观点 (可选)

<% tp.file.cursor(3) %>