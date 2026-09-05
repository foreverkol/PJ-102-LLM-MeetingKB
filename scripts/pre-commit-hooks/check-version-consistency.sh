#!/usr/bin/env bash
#
# pre-commit-hooks/check-version-consistency.sh
# v41 教训:历史 tag 不动 + Sprint 21+ 必须 v3.x.x
#
set -e

PJ102_ROOT="$(git rev-parse --show-toplevel)"
cd "$PJ102_ROOT"

echo "🔍 检查 Sprint 21+ 文档版本号一致性..."

# 1. Sprint 21+ 文件名必须含 v3.x.x
BAD_NAMES=""
for f in $(find 04-复盘与决策 -name "Sprint2[1-9]*.md" 2>/dev/null); do
  if ! echo "$(basename $f)" | grep -q "v3\.[0-9]\.[0-9]"; then
    BAD_NAMES="$BAD_NAMES $f"
  fi
done

if [ -n "$BAD_NAMES" ]; then
  echo "❌ Sprint 21+ 文件名必须含 v3.x.x:"
  echo "$BAD_NAMES"
  exit 1
fi

# 2. Sprint 21+ frontmatter
BAD_FM=""
for f in $(find 04-复盘与决策 -name "Sprint2[1-9]*.md" 2>/dev/null); do
  if head -10 "$f" | grep -qE "^version:.*v[12]\.[0-9]+"; then
    BAD_FM="$BAD_FM $f"
  fi
done

if [ -n "$BAD_FM" ]; then
  echo "❌ Sprint 21+ frontmatter 不能 v1.x/v2.x:"
  echo "$BAD_FM"
  exit 1
fi

# 3. git tag 白名单
# 接受:backup/* + vN.x.x + vN.x.x-suffix + vN.x-suffix (历史 v1.0-baseline 等)
INVALID_TAGS=""
for t in $(git tag -l); do
  if echo "$t" | grep -q "^backup/"; then
    continue
  fi
  # 接受 vN.x.x, vN.x.x-suffix, vN.x-suffix (兼容历史)
  if ! echo "$t" | grep -qE "^v[0-9]+(\.[0-9]+){1,2}(-[a-zA-Z0-9]+)?$"; then
    INVALID_TAGS="$INVALID_TAGS $t"
  fi
done

if [ -n "$INVALID_TAGS" ]; then
  echo "❌ 非法 tag 命名:"
  echo "$INVALID_TAGS"
  exit 1
fi

# 4. atomicstrata poc 在 main?
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ] && [ -d "03-执行/poc_atomicstrata" ]; then
  echo "⚠️  atomicstrata PoC 在 main 分支"
  exit 1
fi

echo "✅ 版本号一致性检查通过"
exit 0
