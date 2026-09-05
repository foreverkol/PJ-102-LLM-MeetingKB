---
type: external_ref
title: "<% tp.file.title %>"
source_url: ""
authors: ""
publication_date: <% tp.date.now("YYYY-MM-DD") %>
key_claims: []
can_update_internal: false
source_ref: ""
date: <% tp.date.now("YYYY-MM-DD") %>
generator: pj102-templater-v1.0
llm_provider: minimax
llm_model: MiniMax-M3
generated_at: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

## 🔗 链接

<% tp.file.cursor(1) %>

## 👤 作者

<% tp.file.cursor(2) %>

## 📌 关键观点

<% tp.file.cursor(3) %>

## 🔄 可同步内部

<% tp.system.suggester(["是", "否"]) %>
