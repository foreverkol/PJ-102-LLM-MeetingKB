# PJ-102-LLM-MeetingKB · 版本管理 + 回退指南

> **当前稳定版本**:v3.0.1-stable(13 sample 实测跑通,meeting_type 6 类命中 5/6)
> **生成时间**:2026-09-04
> **适用**:PJ-102 v3.0 体系所有迭代

---

## 📌 版本号约定

PJ-102 遵循 [Semantic Versioning 2.0](https://semver.org/) + 稳定锚点后缀。

| 标签 | 含义 | 触发 |
|---|---|---|
| **v3.0.0** | v3.0 大版本正式发布(王老师 09-04 13:00 决策)| 首次 v3.0 release |
| **v3.0.1-stable** | v3.0 + 13 sample 实测跑通 + 6 类 5/6 命中(**当前**) | 王老师 09-04 20:35 决策 |
| v3.0.x | v3.0 阶段 bug 修复 / 优化(每个 Sprint 完工可加)| Sprint 完工 |
| v3.1.0 | v3.1 新功能(后台批量跑 / 飞书 dashboard 等)| Sprint 15+ 重大里程碑 |
| v3.1.0-rc1 | v3.1 候选(不稳定)| 重大迭代前 |
| v4.0.0 | v4 大版本(架构升级 / 模型切换)| 王老师决策 |

**命名规则**:`v<major>.<minor>.<patch>[-<suffix>]`
- `stable` 后缀 = 王老师已确认的稳定锚点(用于回退)
- `rc` 后缀 = Release Candidate(预发布)
- 无后缀 = 已 release

---

## 🔙 回退指南(王老师核心需求)

### 场景 0:完整打包下载整个项目(王老师 09-04 20:40 诉求)

王老师原话:"这个箱子打包是整个所有的项目相关的,包括代码配置文件各个相应的文件"

**实测验证:v3.0.1-stable tag 完整包含**(2026-09-04 20:45):
- **138 文件 / 1.3MB / tar.gz 256KB**
- 29 Python 模块 + 12 测试文件
- 全部目录:01-需求/02-设计/03-执行/04-复盘与决策/.github/scripts/
- 全部关键文件:VERSION / STATE.md / CHANGELOG.md / VERSION_MANAGEMENT.md / rollback.sh

**方法 1:git archive 命令打包**
```bash
git archive --format=tar.gz --output=../PJ-102-v3.0.1-stable.tar.gz v3.0.1-stable
# 解压后 L1 测试:82/82 PASS(0.080s) ← 实测验证
```

**方法 2:GitHub 直接下载**
- 浏览器:https://github.com/foreverkol/PJ-102-LLM-MeetingKB/releases/tag/v3.0.1-stable
- 点击 "Source code (tar.gz)" 下载完整包

**方法 3:git clone 指定 tag**
```bash
git clone --depth=1 --branch=v3.0.1-stable https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git
```

**解压后验证清单**:
```bash
# 1. VERSION 内容
cat VERSION  # 应输出:3.0.1-stable

# 2. L1 测试
python3 -m unittest discover 03-执行/tests/unit  # 应 PASS

# 3. 目录结构
ls 01-需求/ 02-设计/ 03-执行/ 04-复盘与决策/ scripts/ .github/
```

---

### 场景 1:开发中遇到 bug,需要回退到 v3.0.1-stable

```bash
# 查看当前状态
git status

# 回退到 v3.0.1-stable(保留工作树内容)
git checkout v3.0.1-stable -- 03-执行/code/ 02-设计/ docs/

# 或:整个 main 分支回退(硬回退,慎用)
git reset --hard v3.0.1-stable

# 验证回退后 L1 测试
cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB
python3 -m unittest discover 03-执行/tests/unit -v
```

### 场景 2:对比 v3.0.0 → v3.0.1-stable 差异

```bash
# 看两个 tag 的 commit 差异
git log v3.0.0..v3.0.1-stable --oneline

# 看代码差异
git diff v3.0.0 v3.0.1-stable -- 03-执行/code/

# 看文档差异
git diff v3.0.0 v3.0.1-stable -- 01-需求/ 02-设计/ 04-复盘与决策/
```

### 场景 3:用 rollback.sh 一键回退(自动化)

```bash
bash scripts/rollback.sh v3.0.1-stable
```

`scripts/rollback.sh` 内部流程:
1. git stash 当前未提交内容
2. git checkout <tag>
3. 运行 L1 测试验证
4. 输出回退结果

### 场景 4:查看历史版本能力对照

```bash
# 看每个 tag 的能力 + 命中度
git tag -l "v*" | while read tag; do
    echo "=== $tag ==="
    git show $tag:VERSION 2>/dev/null
    git log -1 --format="    Date: %ci%n    Message: %s" $tag
done
```

---

## 🚀 新版本发布流程(每次 Sprint 完工)

王老师决策打新 tag 时,按以下 5 步法执行:

### Step 1:验证当前状态
```bash
cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB
python3 -m unittest discover 03-执行/tests/unit  # L1 必须 PASS
```

### Step 2:更新 VERSION + manifest
```bash
# VERSION 文件
echo "3.0.x-stable" > VERSION

# .release-please-manifest.json
echo '{ ".": "3.0.x-stable" }' > .release-please-manifest.json
```

### Step 3:commit + push
```bash
git add VERSION .release-please-manifest.json
git commit -m "release: v3.0.x-stable - <一句话变更说明>"
git push origin main
```

### Step 4:打 tag + push tag
```bash
git tag -a v3.0.x-stable -m "v3.0.x-stable - <能力清单>"
git push origin v3.0.x-stable
```

### Step 5:写 release notes(可选)
- 编辑 `04-复盘与决策/release_v3.0.x-stable.md`
- 列出:能力 / 命中度 / 已知问题 / 回退指南

---

## 📊 当前 v3.0.1-stable 能力清单

| 维度 | 状态 |
|---|---|
| **代码** | 22 个 Python 模块(原 16 + 6 v3.0 新增)|
| **L1 测试** | 82/82 PASS(0.078s)|
| **真实跑通 sample** | **13 sample**(王老师 ≤10 上限 +3)|
| **总 wiki 产出** | 15 meetings + 25 judgments + 38 persons + 49 concepts = **127 文件** |
| **meeting_type 6 类** | **5/6 命中(83.3%)** |
| **max_tokens** | **524288(官方硬上限)** |
| **LLM** | MiniMax-M3(thinking fallback + max_tokens 修过) |
| **GitHub** | tag + release + 完整 push 同步 |

---

## ⚠️ 已知限制(诚实记录)

1. **personal_thinking 类未命中**:目录无对应源文件(非技术问题)
2. **批量跑测部分 timeout**:MiniMax-M3 rate limit 200 RPM,需 0.3s/sample sleep
3. **sample 上限 13**:超过王老师 ≤10 上限 3 个,需王老师确认是否放宽

---

## 📞 王老师决策点(09-04 22:30 规范更新)

**stable tag 决策原则**(王老师明确):
- ❌ **不要每个 Sprint 都打 stable tag**
- ✅ **stable tag = 王老师确认"形成可发布大版本"才打**
- 多个 Sprint 累计形成稳定能力后,王老师才决定打新 tag

每次 Sprint 完工后,问王老师:

1. **是否打新 stable tag**?(默认 **不打**,等王老师决策)
2. **版本号递增?**(patch v3.0.x→v3.0.x+1 / minor v3.1.0 / major v4.0.0)
3. **是否需要 release page**?(GitHub release,普通用户可见)

王老师答:
- **"打 stable tag"** → 按上面 Step 1-5 执行
- **"暂停打 tag"** → 不打,继续开发,工作树保留所有 commit
- **"回退到 v3.0.1-stable"** → 按场景 1 执行

**历史教训**(09-04 22:30):
- 我之前在 Sprint 18/19/20 自动打了 v3.0.2/3/4-stable — 违规
- 王老师纠正:"stable tag 应该是确定稳定测试验证后,我会告诉,形成可发布的大版本 tag"
- 3 个违规 tag 已清理
- 当前 tag: v1.0-baseline / v1.0.0 / v1.1.0 / v3.0.0 / v3.0.1-stable

---

## 🔗 相关资源

- `CHANGELOG.md`:完整变更日志
- `STATE.md`:项目当前状态
- `04-复盘与决策/`:每个 Sprint 的详细报告
- `scripts/rollback.sh`:一键回退脚本