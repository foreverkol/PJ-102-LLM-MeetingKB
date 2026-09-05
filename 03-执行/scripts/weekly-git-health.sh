#!/usr/bin/env bash
#
# scripts/weekly-git-health.sh
# 周日 22:00 跑,检查 PJ-102 git 健康度
#
# 王老师 9-05 OUT-OF-BAND 触发 - 防止工作树脏区 + 分支差异 + tag 异常再次发生
#
# Cron:
#   0 22 * * 0 bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/scripts/weekly-git-health.sh >> /tmp/pj102-git-health.log 2>&1
#
set -e

PJ102_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")"
cd "$PJ102_ROOT"

echo "========================================"
echo "PJ-102 Git 健康周报 - $(date +%Y-%m-%d)"
echo "========================================"

# 1. 工作树脏区
echo ""
echo "1️⃣ 工作树脏区:"
DIRTY=$(git status --short 2>/dev/null | wc -l)
MODIFIED=$(git status --short 2>/dev/null | grep -c "^ M" || echo "0")
UNTRACKED=$(git status --short 2>/dev/null | grep -c "^??" || echo "0")
echo "   总脏区: $DIRTY 项"
echo "   Modified: $MODIFIED 项"
echo "   Untracked: $UNTRACKED 项"

if [ "$DIRTY" -gt 15 ]; then
  echo "   ⚠️  脏区过大(> 15),需要王老师评审处理"
fi

# 2. 分支列表 + 差异
echo ""
echo "2️⃣ 分支 + 差异(相对 main):"
for BR in dev $(git branch -l | sed 's/^\*\s*//' | grep -v "^main$"); do
  if [ -n "$BR" ] && [ "$BR" != "main" ]; then
    DIFF=$(git rev-list --count main..$BR 2>/dev/null || echo "0")
    echo "   $BR: $DIFF commits ahead of main"
  fi
done

# 3. 最近 5 个 tag
echo ""
echo "3️⃣ 最近 5 个 tag:"
git for-each-ref --count=5 --format='%(refname:short) %(creatordate:short)' refs/tags 2>/dev/null

# 4. 当前 HEAD
echo ""
echo "4️⃣ 当前 HEAD:"
git log --oneline -1

# 5. 本周 commit 数
echo ""
echo "5️⃣ 本周 commit 数:"
WEEK_COMMITS=$(git log --since="7 days ago" --oneline 2>/dev/null | wc -l)
echo "   $WEEK_COMMITS commits"

# 6. 飞书告警阈值
if [ "$DIRTY" -gt 15 ] || [ "$WEEK_COMMITS" -eq 0 ]; then
  echo ""
  echo "⚠️  触发飞书告警:"
  echo "   - 脏区 $DIRTY 项(阈值 15)"
  echo "   - 本周 0 commits(阈值 > 0)"
  # 此处加飞书 webhook 调用
fi

echo ""
echo "========================================"
echo "健康周报生成完成"
