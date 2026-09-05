---
type: decision
# ============================================
# @required 必填字段
# ============================================
title: "<% tp.file.title %>"
date: "<% tp.date.now(\"YYYY-MM-DD\") %>"
type: "decision"
generator: "pj102-templater-v1.1"
# ============================================
# @optional 可选字段
# ============================================
problem: ""
alternatives: []
chosen: ""
reason: ""
outcome: ""
constraints: []
review_trigger: ""
value_grade: "B"
source_ref: ""
source_meeting: ""
canonical_name: "<% tp.file.title %>"
aliases: []
entity_id: "decision_<% tp.date.now(\"YYYYMMDD_HHmmss\") %>"
llm_provider: "minimax"
llm_model: "MiniMax-M3"
generated_at: "<% tp.date.now(\"YYYY-MM-DDTHH:mm:ss\") %>"
---

# <% tp.file.title %>

> **@required**:title / date / type / generator

## 🎯 问题 (可选)

<% tp.file.cursor(1) %>

## 🔄 备选方案 (可选)

<% tp.file.cursor(2) %>

## ✅ 已选方案 (可选)

<% tp.file.cursor(3) %>

## 📋 结果 (可选)

<% tp.file.cursor(4) %>