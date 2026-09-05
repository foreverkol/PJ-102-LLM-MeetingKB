# PJ-102 v3.0.1-stable + atomicstrata 配合方案 v1.0

## 核心原则
- s4-s12 主流程 **不动**(70 commits + v3.0.1-stable tag 不能推翻)
- atomicstrata 是 **辅助质量检查层**,**不写文件**到 s4-s12 输出目录
- 配合方式:atomicstrata 跑"质量检查 + 行号引用增强",通过 README/STATE 文档告诉王老师

## 阶段 A1(本周, 30-45 分钟)
**目标**:atomicstrata 跑同样 5 个新原始录音,跟 s4-s12 跑同样 5 个,对比 frontmatter 差异

执行:
1. s4-s12 流水线跑 5 个全新原始录音
   命令: cd 03-执行/code && python3 pipeline.py --batch
2. atomicstrata 跑同样 5 个(已跑过,产物在 03-执行/poc_atomicstrata/wiki/concepts/)
3. 对比报告:写 04-复盘与决策/A1_s4s12_vs_atomicstrata_对比报告.md

产出:
- 02-知识库/PJ-102-LLM-MeetingKB/meetings/ 多 5 个
- 04-复盘与决策/A1_对比报告.md(差异点 + 互补点)

## 阶段 A2(1 周)
**目标**:atomicstrata 跑全量 312 个原始录音,做"跨全库质量检查"

执行:
1. 复制所有 312 个原始录音到 03-执行/poc_atomicstrata/sources/
2. 跑 atomicstrata compile(后台,~3-5 小时)
3. 抽取矛盾报告(contradictions 字段)
4. 跟 s4-s12 的 dispute_detector.py 输出交叉对比
5. 写一份"矛盾清单 + 建议合并清单"

产出:
- 03-执行/poc_atomicstrata/wiki/concepts/ 300+ 个
- 04-复盘与决策/A2_矛盾检测报告.md
- 写回到 s4-s12 的 lint_wiki.py(增加 atomicstrata 矛盾源)

## 阶段 A3(2 周)
**目标**:atomicstrata 提供"行号引用增强层",不破坏 s4-s12 frontmatter

执行:
1. 写"atomicstrata → s4-s12 概念增强"脚本
   路径: 03-执行/code/atomicstrata_enhance_concepts.py
   逻辑: 读 atomicstrata concepts/*.md + s4-s12 concepts/*.md,
         匹配同源会议(文件名前缀相同),
         把 atomicstrata 的 sources[] + 行号引用(从 body 提取"Lines XX-YY"模式)
         追加到 s4-s12 concept 的 frontmatter,但**不覆盖** s4-s12 已有字段
2. 备份 s4-s12 105 个 concepts(02-知识库/concepts.bak/)
3. 跑增强脚本
4. 跑 lint_wiki.py 验证"覆盖率提升"

产出:
- 03-执行/code/atomicstrata_enhance_concepts.py(~ 200 行)
- 02-知识库/concepts/*.md frontmatter 多一个 `atomicstrata_refs:` 字段
- 04-复盘与决策/A3_行号引用增强报告.md

## 铁律(必须遵守)
1. s4-s12 文件 frontmatter 原字段不删,只追加
2. atomicstrata 写到 02-知识库/ 的内容必须 git commit 前有备份
3. 任何"覆盖"操作必须先 backup → diff → 确认
4. 王老师可随时"关掉 atomicstrata 增强":删除 03-执行/code/atomicstrata_enhance_concepts.py 即可

## 不做的事
- ❌ 不删 s4-s12 任何代码
- ❌ 不覆盖 s4-s12 已有 frontmatter 字段
- ❌ 不动 v3.0.1-stable tag
- ❌ 不替代 dispute_detector.py(只补充)
