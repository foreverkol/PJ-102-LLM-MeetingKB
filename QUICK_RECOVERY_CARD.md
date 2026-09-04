# 🚨 王老师口头要求 → 一键操作卡(Quick Recovery Card)

> **使用场景**:王老师口头说任何要求 → Agent 立即找对应命令 → 60 秒内执行
> **生成时间**:2026-09-04
> **当前项目**:PJ-102-LLM-MeetingKB v3.0.1-stable

---

## 📍 项目根目录(所有命令的前缀)

```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
```

---

## 🎯 王老师口头要求速查表

### 版本回退类

| 王老师说 | Agent 立即执行 |
|---|---|
| **"回退到 v3.0.1-stable"** | `bash scripts/rollback.sh v3.0.1-stable` |
| **"回退到上一个稳定版"** | `bash scripts/rollback.sh v3.0.1-stable` |
| **"回退到 v3.0.0"** | `bash scripts/rollback.sh v3.0.0` |
| **"回退到 v1.0"** | `bash scripts/rollback.sh v1.1.0` |
| **"回退(保留未提交)"** | `bash scripts/rollback.sh v3.0.1-stable --keep` |

### 打包下载类

| 王老师说 | Agent 立即执行 |
|---|---|
| **"打包整个项目"** | `git archive --format=tar.gz --output=~/Desktop/PJ-102-$(cat VERSION).tar.gz $(cat VERSION)` |
| **"打包 v3.0.1-stable"** | `git archive --format=tar.gz --output=~/Desktop/v3.0.1-stable.tar.gz v3.0.1-stable` |
| **"下载项目"** | `git clone https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git` |
| **"下载 v3.0.1-stable 版"** | `git clone --branch=v3.0.1-stable https://github.com/foreverkol/PJ-102-LLM-MeetingKB.git` |

### 对比查看类

| 王老师说 | Agent 立即执行 |
|---|---|
| **"对比 v3.0.0 和 v3.0.1-stable"** | `git log v3.0.0..v3.0.1-stable --oneline` |
| **"看 v3.0.1-stable 有什么"** | `git ls-tree -r --name-only v3.0.1-stable` |
| **"列出所有 tag"** | `git tag -l -n1 "v*"` |
| **"看 v3.0.1-stable 的 STATE"** | `git show v3.0.1-stable:STATE.md` |
| **"查 VERSION"** | `cat VERSION` |

### 新版本发布类

| 王老师说 | Agent 立即执行 |
|---|---|
| **"打 v3.0.2-stable tag"** | 5 步法(更新 VERSION + commit + tag + push + release) |
| **"打 v3.1.0"** | 同上,VERSION = "3.1.0" |
| **"撤销这个 tag"** | `git tag -d v3.0.2-stable && git push origin :refs/tags/v3.0.2-stable` |

### 项目状态类

| 王老师说 | Agent 立即执行 |
|---|---|
| **"项目当前什么状态"** | `cat STATE.md` |
| **"运行 L1 测试"** | `python3 -m unittest discover 03-执行/tests/unit` |
| **"看最近 commit"** | `git log --oneline -10` |
| **"看谁改了文件"** | `git blame <file>` |

---

## ⚡ 一句话救命(最常用 5 个)

### 1. 项目被搞乱了,从头开始
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
bash scripts/rollback.sh v3.0.1-stable --keep
```

### 2. 打包给同事
```bash
cd "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
git archive --format=tar.gz --output=~/Desktop/PJ-102-v3.0.1-stable.tar.gz v3.0.1-stable
```

### 3. 看现在是什么版本
```bash
cat VERSION
git log --oneline -3
```

### 4. 测试不通过
```bash
python3 -m unittest discover 03-执行/tests/unit 2>&1 | grep -E "FAIL|ERROR"
```

### 5. 推送失败
```bash
# 看远程配置
git remote -v

# 改 SSH(王老师 134s 超时问题)
git remote set-url origin git@github.com:foreverkol/PJ-102-LLM-MeetingKB.git
git push origin main
```

---

## 🚨 紧急情况(王老师说"出事了")

### 工作树丢失
```bash
git reflog | head -10      # 找最近 commit
git reset --hard <hash>    # 恢复
```

### 误删 tag
```bash
# 找删除前的 commit
git fsck --unreachable | grep tag
```

### 远程仓库 502
```bash
# 等 5 分钟再 push,或换 HTTPS/SSH
```

---

## 📚 完整文档索引

- `GITHUB_OPERATIONS_HANDBOOK.md` — 完整操作手册(21 KB)
- `VERSION_MANAGEMENT.md` — 版本管理 + 5 种回退场景(8.5 KB)
- `STATE.md` — 项目当前状态
- `CHANGELOG.md` — 完整变更日志
- `04-复盘与决策/` — Sprint 报告目录
- `scripts/rollback.sh` — 一键回退脚本

---

**最后更新**:2026-09-04
**适用版本**:v3.0.1-stable 及后续所有 v3.x-stable