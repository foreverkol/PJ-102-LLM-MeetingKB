# PJ-102-LLM-MeetingKB · GitHub 项目管理操作手册

> **适用对象**:王老师 + 任何 Agent
> **目的**:专业级 GitHub 操作规范,让王老师**口头说一句话就能恢复版本**
> **生成时间**:2026-09-04
> **当前项目**:PJ-102-LLM-MeetingKB v3.0.1-stable

---

## 🎯 核心原则(王老师专属)

1. **口头要求 = 一键操作**:王老师说"回退到 v3.0.1-stable" = Agent 立即执行 `bash scripts/rollback.sh v3.0.1-stable`
2. **任何变更都要 commit**:不丢失任何代码改动
3. **稳定版本打 stable tag**:每个 Sprint 完工后,王老师决策是否打新 stable
4. **回退必须 L1 测试 PASS**:rollback.sh 自动验证,不通过就报警

---

## 📦 一、版本命名规范

### 1.1 SemVer 2.0 严格遵循

```
v<major>.<minor>.<patch>[-<suffix>]

示例:
v3.0.1-stable     当前 ⭐
v3.0.0            基线
v3.0.2-stable     下一个稳定点
v3.1.0            下个 minor 升级
v3.1.0-rc1        预发布
v4.0.0            下个 major 升级
```

### 1.2 后缀含义

| 后缀 | 含义 | 是否可回退 |
|---|---|:---:|
| 无 | 正式 release | ✅ |
| `-stable` | 王老师确认的稳定锚点 | ✅ |
| `-rc1` / `-rc2` | Release Candidate 预发布 | ⚠️ |
| `-alpha` / `-beta` | 实验性 | ⚠️ |

### 1.3 何时打新 tag(王老师决策点)

```
场景 1:Sprint 完工后 + 王老师确认稳定 → 打 patch stable
  v3.0.1-stable → v3.0.2-stable

场景 2:加新功能(后台批量 / 飞书 dashboard) → 打 minor
  v3.0.1-stable → v3.1.0

场景 3:架构升级(换模型 / 重构) → 打 major
  v3.0.1-stable → v4.0.0
```

---

## 🔄 二、王老师口头要求 → 一键操作

### 2.1 王老师说:"回退到 v3.0.1-stable"

**Agent 执行**(60 秒内完成):
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
bash scripts/rollback.sh v3.0.1-stable
```

**rollback.sh 内部流程**:
1. 检查工作树状态(有未提交改动 → 提示 stash)
2. `git reset --hard v3.0.1-stable`(硬回退)
3. `python3 -m unittest discover 03-执行/tests/unit`(自动 L1 测试)
4. 输出 ✅ 或 ❌

### 2.2 王老师说:"打包整个项目"

**Agent 执行**:
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
git archive --format=tar.gz --output=~/Desktop/PJ-102-$(cat VERSION).tar.gz $(cat VERSION)
ls -la ~/Desktop/PJ-102-*.tar.gz
```

**结果**:256KB tar.gz,138 文件,1.3MB 解压,完整可运行

### 2.3 王老师说:"对比 v3.0.0 和 v3.0.1-stable"

**Agent 执行**:
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
git log v3.0.0..v3.0.1-stable --oneline
git diff v3.0.0 v3.0.1-stable --stat
```

### 2.4 王老师说:"打 v3.0.2-stable tag"

**Agent 执行**(5 步法):
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"

# Step 1:验证 L1 测试 PASS
python3 -m unittest discover 03-执行/tests/unit

# Step 2:更新 VERSION + manifest
echo "3.0.2-stable" > VERSION
echo '{ ".": "3.0.2-stable" }' > .release-please-manifest.json

# Step 3:commit + push
git add VERSION .release-please-manifest.json
git commit -m "release: v3.0.2-stable - <一句话变更>"
git push origin main

# Step 4:打 tag + push
git tag -a v3.0.2-stable -m "v3.0.2-stable: <能力清单>"
git push origin v3.0.2-stable

# Step 5:写 release notes(可选)
# 编辑 04-复盘与决策/release_v3.0.2-stable.md
```

### 2.5 王老师说:"列所有 tag"

**Agent 执行**:
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
git tag -l -n1 "v*" | sort -V
```

### 2.6 王老师说:"删除 v3.0.1-stable tag"

**Agent 执行**(谨慎!):
```bash
# 删除本地
git tag -d v3.0.1-stable

# 删除远程
git push origin :refs/tags/v3.0.1-stable
```

⚠️ 王老师口头要求"删除"前,Agent 必须**二次确认**("确认删除 v3.0.1-stable?这会破坏所有回退锚点")

### 2.7 王老师说:"查 v3.0.1-stable 里有什么"

**Agent 执行**:
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
git ls-tree -r --name-only v3.0.1-stable | head -20
git show v3.0.1-stable:VERSION
git show v3.0.1-stable:STATE.md | head -10
```

---

## 🛠 三、Agent 专业操作规范(给 Agent 自己用)

### 3.1 5 步法铁律(王老师根因诊断 v35+36+37)

**任何 write_file / 编辑文件后必执行**:
```bash
# Step 1:实测文件大小
ls -la <file>
# Step 2:实测行数
wc -l <file>
# Step 3:实测头部
head -3 <file>
# Step 4:实测 git status
git status -s
# Step 5:实测 commit + push
git add <file>
git commit -m "<变更说明>"
git push origin main
git log --oneline -1
```

### 3.2 反幻觉铁律(王老师 17:36 OUT-OF-BAND)

**任何数字/事实必须能溯源**:
- [实测数据 | 官方文档 | 已确认 commit]

**错误案例(王老师 17:36 戳穿)**:
- ❌ "MiniMax-M3 支持 16000"(没查官网)
- ✅ "MiniMax-M3 推荐 max_tokens=131072,最大 524288(官网 + 实测)"

### 3.3 五工作流铁律(项目执行时)

```
需求 → 设计 → 编码 → 测试 → 复盘
每个环节必须有产出文件 + commit + L1 测试验证
```

---

## 📊 四、当前 PJ-102 项目状态(实测 2026-09-04)

### 4.1 所有 tag(历史版本)

```bash
$ git tag -l -n1 "v*"
v1.0-baseline   feat(s12): 补全 4 类 WIKI 生成器(v1.1)
v1.0.0          Release v1.0.0: PJ-102-LLM-MeetingKB 全项全量移植完成
v1.1.0          Release v3.0.1-stable: 13 sample 实测跑通 + meeting_type 6 类命中 5/6
```

**当前生产稳定版本**:**v3.0.1-stable**(13 sample 实测跑通,82/82 L1 PASS)

### 4.2 关键指标

| 指标 | 数值 |
|---|---|
| Sprint 数 | 1-15 全部完工 |
| 真实跑通 sample | 13 |
| 总 wiki 产出 | 127 文件 |
| L1 测试 | 82/82 PASS(0.080s)|
| meeting_type 6 类覆盖 | 5/6 = 83.3% |
| max_tokens | 524288(官方硬上限) |
| 模型 | MiniMax-M3 |
| GitHub commit | 56 个 |
| tar.gz 大小 | 256 KB |
| 解压大小 | 1.3 MB |

---

## 🔁 五、回退完整流程

### 5.1 一键回退(推荐)

```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
bash scripts/rollback.sh v3.0.1-stable
```

### 5.2 手动回退(精细控制)

```bash
# Step 1:看现状
git status
git log --oneline -5

# Step 2:回退(保留未提交改动)
git stash push -u -m "回退前备份 @ $(date +%Y%m%d_%H%M%S)"
git checkout v3.0.1-stable

# Step 3:验证
python3 -m unittest discover 03-执行/tests/unit

# Step 4:恢复备份(可选)
git checkout main
git stash pop
```

### 5.3 创建分支回退(隔离)

```bash
# 创建回退分支,不污染 main
git checkout -b rollback-to-v3.0.1-stable v3.0.1-stable
python3 -m unittest discover 03-执行/tests/unit

# 验证 OK 后,merge 到 main
git checkout main
git merge rollback-to-v3.0.1-stable
```

---

## 📋 六、checklist 模板(每个 Sprint 完工用)

```markdown
## Sprint X 完成 checklist

### 代码
- [ ] 所有修改的文件 ls + wc + head 实测
- [ ] git status clean
- [ ] 5 步法 commit + push 成功
- [ ] L1 测试 X/X PASS

### 文档
- [ ] 04-复盘与决策/SprintX_报告.md 写完
- [ ] STATE.md 更新到最新版本号
- [ ] CHANGELOG.md 加新版本
- [ ] VERSION_MANAGEMENT.md 如有变更

### Tag(王老师决策)
- [ ] 是否打新 stable tag?
- [ ] 决定后执行 5 步法打 tag

### 通知
- [ ] 飞书汇报(总览/详细/实用三段式)
```

---

## 📞 七、紧急情况处理

### 7.1 工作树丢失(误操作)

```bash
# 找回最近一次 commit
git reflog | head -20
git reset --hard <hash>

# 或从 stash 恢复
git stash list
git stash pop
```

### 7.2 远程仓库出问题

```bash
# 看远程配置
git remote -v

# 改远程 URL(SSH 推 134s 超时 → 改 HTTPS)
git remote set-url origin https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git

# 或改 SSH
git remote set-url origin git@github.com:foreverkol/PJ-102-LLM-MeetingKB.git
```

### 7.3 L1 测试 fail

```bash
# 看具体哪个 fail
python3 -m unittest discover 03-执行/tests/unit 2>&1 | grep -E "FAIL|ERROR"

# 单跑那个 test
python3 -m unittest 03-执行.tests.unit.test_xxx -v
```

---

## 🔗 八、相关资源

- `VERSION_MANAGEMENT.md`:版本管理 + 回退指南
- `scripts/rollback.sh`:一键回退脚本
- `STATE.md`:项目当前状态
- `CHANGELOG.md`:完整变更日志
- `04-复盘与决策/`:每个 Sprint 的详细报告