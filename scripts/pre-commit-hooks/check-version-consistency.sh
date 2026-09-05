#!/usr/bin/env bash
#
# pre-commit-hooks/check-version-consistency.sh
# 防止 Sprint 文档用错版本号(v1.x / v2.x / 3.x.x 混用)
#
# 王老师 9-05 OUT-OF-BAND:"前面不是 V3.0 的版本吗"
# v41 教训:stable tag 必须是王老师确认"形成可发布大版本"才能打
#
# 安装:
#   ln -s ../../scripts/pre-commit-hooks/check-version-consistency.sh .git/hooks/pre-commit
#
set -e

PJ102_ROOT="$(git rev-parse --show-toplevel)"
cd "$PJ102_ROOT"

echo "🔍 检查 Sprint 文档版本号一致性..."

# 1. 04-复盘与决策/Sprint*.md 必须遵循 v3.x.x 命名
SUSPECT=$(find 04-复盘与决策 -name "Sprint*.md" -type f -exec grep -l "title:.*v[12]\." {} \; 2>/dev/null || true)

if [ -n "$SUSPECT" ]; then
  echo "❌ 以下文件使用了 v1.x / v2.x 命名(必须改为 v3.x.x):"
  echo "$SUSPECT"
  echo ""
  echo "修正方法:"
  echo "  - PJ-102 当前大版本:v3.0.1-stable"
  echo "  - 下一稳定版:v3.1.0(王老师确认后)"
  echo "  - 开发中:v3.1.0-alpha1 / v3.1.0-rc1"
  exit 1
fi

# 2. git tag 必须遵循 SemVer
echo "🔍 检查 git tag 命名..."
INVALID_TAGS=$(git tag -l | grep -v "^v[0-9]\+\.[0-9]\+\.[0-9]\+\(-\(alpha[0-9]*\|beta[0-9]*\|rc[0-9]*\|stable\)\)\?$" || true)
if [ -n "$INVALID_TAGS" ]; then
  echo "❌ 非法 tag 命名(v41 教训:必须遵循 SemVer):"
  echo "$INVALID_TAGS"
  exit 1
fi

# 3. 严禁提交 atomicstrata poc 到 main(必须用 poc/ 分支)
echo "🔍 检查 atomicstrata PoC 分支..."
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ] && [ -d "03-执行/poc_atomicstrata" ]; then
  echo "⚠️  atomicstrata PoC 在 main 分支(应移到 poc/atomicstrata-experiment)"
  echo "修复方法:"
  echo "  git checkout -b poc/atomicstrata-experiment"
  echo "  git rm -r 03-执行/poc_atomicstrata"
  echo "  git commit -m 'poc: 移出 atomicstrata 实验目录'"
  exit 1
fi

echo "✅ 版本号一致性检查通过"
exit 0
