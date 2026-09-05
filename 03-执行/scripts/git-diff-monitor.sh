#!/usr/bin/env bash
#
# scripts/git-diff-monitor.sh
# 检查分支差异,过大时告警(王老师 9-05 OUT-OF-BAND)
#
# Cron:
#   0 9 * * 1 bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/03-执行/scripts/git-diff-monitor.sh >> /tmp/pj102-diff.log 2>&1
#
set -e

PJ102_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")"
cd "$PJ102_ROOT"

echo "🔍 PJ-102 分支差异检查 - $(date +%Y-%m-%d)"

WARN_THRESHOLD=10
BLOCK_THRESHOLD=30

for BR in $(git branch -l | sed 's/^\*\s*//' | grep -v "^main$" | grep -v "remotes/"); do
  if [ -z "$BR" ] || [ "$BR" = "remotes" ]; then
    continue
  fi
  COMMITS=$(git rev-list --count main..$BR 2>/dev/null || echo "0")
  FILES=$(git diff --name-only main..$BR 2>/dev/null | wc -l)

  if [ "$COMMITS" -gt "$BLOCK_THRESHOLD" ] || [ "$FILES" -gt 50 ]; then
    echo "❌ 分支 $BR 差异过大: $COMMITS commits / $FILES files (阈值: $BLOCK_THRESHOLD commits / 50 files)"
    echo "   ⚠️  必须合并或拆分子任务"
  elif [ "$COMMITS" -gt "$WARN_THRESHOLD" ] || [ "$FILES" -gt 20 ]; then
    echo "⚠️  分支 $BR 差异警告: $COMMITS commits / $FILES files (阈值: $WARN_THRESHOLD commits / 20 files)"
  else
    echo "✅ $BR: $COMMITS commits / $FILES files (正常)"
  fi
done
