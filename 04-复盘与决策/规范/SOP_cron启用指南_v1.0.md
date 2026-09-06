---
pj: PJ-102
title: PJ-102 SOP 闸门 2/3 cron 启用指南 v1.0
version: v3.0.1-stable + Sprint 21 v3.1.0-rc1
date: 2026-09-05
status: ⏳ 待王老师手动执行(WSL cron sudo 权限限制)
---

# PJ-102 SOP 闸门 2/3 cron 启用指南 v1.0

> **王老师 9-05 OUT-OF-BAND 触发 SOP v1.0 后,Superpower 模式自主执行时发现**:
> **WSL 环境 cron 服务未启动,且无 sudo 权限启动**。

## ⚠️ 实测情况(2026-09-05 22:15)

```bash
$ service cron status
 * cron is not running

$ sudo service cron start
sudo: a terminal is required to read the password
exit=1
```

**根因**:WSL 默认 cron 不自动启动,需要 sudo 启动。

## 🔧 王老师手动启用(2 种方式)

### 方式 A:王老师手动启 cron(1 行命令)

```bash
sudo service cron start
```

然后执行下面"步骤 1" 添加 2 个 cron 任务。

### 方式 B:用 systemd 永久启用(WSL Ubuntu 22.04+)

```bash
sudo systemctl enable --now cron
```

## 📋 步骤 1:王老师手动添加 2 个 cron 任务

打开 crontab 编辑器:

```bash
crontab -e
```

粘贴以下 2 行(每行末尾换行):

```cron
# PJ-102 SOP 闸门 2/3 - 王老师 9-05 OUT-OF-BAND 触发
0 22 * * 0 bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/scripts/weekly-git-health.sh >> /tmp/pj102-git-health.log 2>&1
0 9 * * 1 bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/scripts/git-diff-monitor.sh >> /tmp/pj102-diff.log 2>&1
```

保存退出。

## 📊 验证

```bash
# 查看 cron 列表
crontab -l | grep -E "weekly-git-health|git-diff-monitor"

# 手动触发测试
bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/scripts/weekly-git-health.sh
```

预期输出:`PJ-102 Git 健康周报 - <日期>` + 工作树脏区数 + tag 列表。

## 🛡️ 闸门 1(pre-commit)已自动启用

`scripts/pre-commit-hooks/check-version-consistency.sh` 已安装到 `.git/hooks/pre-commit`,**每次 commit 自动运行**。

---

**生成者**: Hermes Agent (MiniMax-M3)
**生成时间**: 2026-09-05 22:15 CST
**关联**: SOP_版本管理规范_v1.0.md + Sprint21_v3.1.0-rc1_详细工程计划_v1.0.md
