---
pj: PJ-102
title: PJ-102 v3.0 · Obsidian 集成配置 + 9 块 Dataview
version: v3.0-Sprint3
date: 2026-09-04
status: ready-to-deploy
---

# PJ-102 v3.0 · Obsidian 集成 · 9 块 Dataview

> **目的**:把 v3.0 WIKI 接入 Obsidian 双击即可观测全貌。
> **王老师约束**:不跑全量(≤10 sample),**纯文档 + 配置**零 LLM 消耗。

---

## 安装步骤(王老师本机)

```bash
# 1. 复制 .obsidian/ 配置到 WIKI 根目录
cp -r 02-设计/obsidian-config/.obsidian /mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/WIKI/

# 2. 复制 9 块 Dataview 视图文件
cp 02-设计/obsidian-config/WIKI/.dataview-views.md /mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB/WIKI/

# 3. Obsidian → 打开 vault:指向 02-知识库/PJ-102-LLM-MeetingKB/WIKI/
#    自动识别 .obsidian/ 配置 + Dataview 插件
```

## 9 块 Dataview 视图(全览)

```dataview
TABLE type, date, value_grade, source_ref
FROM "WIKI"
WHERE type
SORT date DESC, type ASC
LIMIT 200
```

```dataview
TABLE type, title, updated
FROM "WIKI"
WHERE date(today) - date(updated) <= 7
SORT updated DESC
```

```dataview
LIST
FROM "WIKI/Knowledge/Judgments"
WHERE value_grade = "S"
SORT updated DESC
```

```dataview
TABLE length(rows) as "出场数"
FROM "WIKI/Meetings"
FLATTEN persons_mentioned as person
GROUP BY person
SORT length(rows) DESC
LIMIT 20
```

```dataview
LIST
FROM "WIKI"
WHERE contains(text, "Status: Disputed")
SORT updated DESC
```

```dataview
TASK
FROM "WIKI"
WHERE !completed AND due
SORT due ASC
```

```dataview
TABLE length(rows) as "数量"
FROM "WIKI"
WHERE type
GROUP BY type
SORT length(rows) DESC
```

```dataview
TABLE length(rows) as "出现数"
FROM "WIKI/Concepts"
GROUP BY link(concept_name)
LIMIT 20
```

```dataview
TABLE s11.value_score as "评分", type, date
FROM "WIKI/Meetings"
WHERE s11
SORT s11.value_score DESC
LIMIT 20
```

## v7.0 字段全部自动识别

每页 md frontmatter 含:
- type (meeting/person/organization/concept/judgment/decision/comparison/scenario)
- date / updated / created
- source_ref(v7.0 §8.1 必填)
- status_stage(5 阶段状态机)
- entity_id(实体统一编号)
- value_grade(S/A/B/C)
- sensitivity(public/internal/sensitive/highly-sensitive)
- tags(含 #可转化资产/ 前缀)
- ldamc 5 维(lost/different/added/more/connected)
- contradictions(v7.0 §v7.0-002)
- topic_key(v7.0 §v7.0-006)

Dataview DQL 全部可查。

## 王老师双击预期效果

打开 vault 后:
- **左侧 sidebar**:文件树 + 标签页
- **中间主区**:Graph View(节点 = md,边 = [[wikilink]])
- **Dataview tab**:9 块视图(总览 / 最近更新 / S级判断 / 人物频次 / 矛盾清单 / 待跟进 / 类型分布 / 概念共现 / 评分)
- **可视化**:无 LLM 调用,毫秒级响应

## 与 v3.0 Sprint 1 集成一致性

- v3.0 ldamc 5 维 → Dataview 自动展示每页自检完整性
- v3.0 contradictions → Dataview 视图 5 一键列矛盾清单
- v3.0 entity_id → Dataview 实体链接可点
- v3.0 status_stage → Dataview 可按阶段过滤
- v7.0 §8.1 必填字段 → lint_wiki.py 自动校验(超出 Dataview 范围)

## 不在 Sprint 3 范围(留待 Sprint 4+)

- ⚪ atomicstrata Profile.json(S3.2 计划)
- ⚪ 312 源实际跑批(W4.3 脚本就位,等王老师指令)
- ⚪ Obsidian Sync 多端同步(需要王老师 Obsidian 账号)

## 故障排查

| 现象 | 修复 |
|---|---|
| Dataview 插件未生效 | Obsidian → Settings → Community Plugins → 启用 Dataview |
| [[wikilink]] 不跳转 | frontmatter 缺 source_ref → 跑 `python3 lint_wiki.py` 校验 |
| Graph View 空 | 没建立 [[wikilink]] 双向链接,需先跑 pipeline.py 生成 |
| 中文路径乱码 | Obsidian → Settings → Files → Use UTF-8 Encoding |
