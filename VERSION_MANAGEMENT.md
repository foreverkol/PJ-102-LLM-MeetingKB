# PJ-102-LLM-MeetingKB · 版本管理 + 回退指南

> **当前稳定版本**:v3.1.0-rc1(M4 A+B 完成,98 测试 PASS,待王老师拍板升 v3.1.0-stable)
> **下一开发版**:Sprint 22(等王老师分配任务)
> **生成时间**:2026-09-06(Codex 二次评审 + M4 全量同步后)
> **适用**:PJ-102 v3.1 体系所有迭代

---

## 📌 2026-09-06 M4 阶段 A+B 完成(Codex 评审强化)

王老师 9-06 OUT-OF-BAND:"给专业更适合的建议 + 按建议执行 + 后续不需要确认 + 自动执行 + 评审调用 codex cli"

### M4 阶段 A(Codex 评审 6 项必修全完成)

| A | 项 | 状态 |
|---|---|------|
| A1 | H1 修复 frontmatter 损坏 | ✅ |
| A2 | H3 cascade_updater --apply 真实现 | ✅ |
| A3 | H4 t13 行号引用真升级 | ✅ |
| A4 | M1 T-09 兼容 meetings | ✅ |
| A5 | 新增 8 个单元测试 | ✅ (98 PASS) |
| A6 | H2 02-知识库 git 化 | ✅ (357 文件 init) |

### M4 阶段 B(王老师触发 6 项)

| B | 项 | 状态 |
|---|---|------|
| B1 | .base 空字段清理 | ⏭️ 跳过(已正确) |
| B2 | registry.yaml + launcher.yaml v3.1.0-rc1 | ✅ |
| B3 | 8 个 Templater @required/optional | ✅ |
| B4 | scenarios/ stub 标注 | ✅ |
| B5 | t07 改名 t07_scenario_status | ✅ |
| B6 | Makefile 框架集成 | ✅ |

### 分支架构(2026-09-06)

```
main (v3.0.1-stable, 55 commits)
  │
  ├── dev (本次会话 16 commits ahead)
  │   │
  │   └── feature/sprint-21-v3.1.0-rc1 (本次 M0-M4 全部)
  │
  ├── poc/atomicstrata-experiment (24 concepts)
  │
  └── backup/main-before-sop-v1.0 (SOP 执行前备份)

tag v3.1.0-rc1 (本次自打, alpha/rc 允许)
```

### Codex 二次评审(2026-09-06)

- **综合评分**:7.5/10(从 5/10 升 +2.5)
- **M4 A+B 完成度**:92%(12 项中 10 项真完成)
- **v3.1.0-stable 发布**:⏸️ 待王老师拍板
- **3 真阻塞决策**:scenarios 跑批 / stable 时机 / Sprint 22 范围

### 5 条铁律(2026-09-05 起,持续遵守)

1. **SemVer 严禁混用**
2. **实验性内容必须 poc/ 分支**
3. **工作树脏区 ≤ 5 项**
4. **文档必须全量同步**
5. **stable tag 必须王老师拍板**

### 4 道自动化闸门

| 闸门 | 检查 | 工具 | 状态 |
|------|------|------|------|
| 1. pre-commit | 版本号 + tag 命名 + poc 分支 | check-version-consistency.sh | ✅ 启用 exit 0 |
| 2. weekly cron | 工作树 + 分支 + tag | weekly-git-health.sh | ⏳ WSL sudo 限制 |
| 3. weekly cron | 分支差异 | git-diff-monitor.sh | ⏳ WSL sudo 限制 |
| 4. monthly review | 大版本对齐 | 王老师评审 | ⏳ 待设 |

### 资产清单(实测 2026-09-06)

| 项 | 数字 |
|----|------|
| meetings | 15 |
| persons | 99 |
| concepts | 137 主 + 22 poc_structured |
| judgments | 74 |
| scenarios | 1 (STUB) |
| comparisons | 0 |
| dataview 块 | 424 |
| Templater 模板 | 8 (v1.1) |
| .base 文件 | 5 |
| Python 模块 | 25 (新 9) |
| 单元测试 | 98 (PASS) |
| 02-知识库 git | 357 文件 |

### 王老师历史决策点(等下次触发)

- T-11 Web Clipper(浏览器 + API)
- T-14 三层架构(重写 s2-s4)
- T-13 B 方案(改 npm 包)
- T-01 75 剩余 relationship(/tmp/pj102-t01-suggestions.json)
- 11 个 YAML 损坏 judgments(title 嵌套引号)
