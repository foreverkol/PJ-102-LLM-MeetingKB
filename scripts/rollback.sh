#!/usr/bin/env bash
#
# scripts/rollback.sh - PJ-102 一键回退到指定 tag
#
# 王老师 09-04 20:35 需求:支持任意版本回退
#
# 用法:
#   bash scripts/rollback.sh v3.0.1-stable      # 回退到指定 tag
#   bash scripts/rollback.sh                     # 列出所有可用 tag
#   bash scripts/rollback.sh v3.0.1-stable --keep  # 回退但保留工作树未提交内容
#
set -e

# ===== 1. 颜色定义 =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ===== 2. 参数解析 =====
TARGET_TAG="${1:-}"
KEEP_FLAG="${2:-}"

# ===== 3. 无 tag 参数:列出所有可用 =====
if [ -z "$TARGET_TAG" ]; then
    echo -e "${YELLOW}用法:${NC}"
    echo "  bash scripts/rollback.sh <tag> [--keep]"
    echo ""
    echo -e "${YELLOW}可用 tag:${NC}"
    git tag -l "v*" | while read tag; do
        date=$(git log -1 --format="%ci" "$tag" 2>/dev/null | cut -d' ' -f1)
        msg=$(git tag -l -n1 "$tag" | sed 's/^[^ ]* *//')
        echo -e "  ${GREEN}$tag${NC} ($date) - $msg"
    done
    exit 0
fi

# ===== 4. 验证 tag 存在 =====
if ! git rev-parse --verify "$TARGET_TAG" >/dev/null 2>&1; then
    echo -e "${RED}❌ Tag 不存在: $TARGET_TAG${NC}"
    echo -e "${YELLOW}可用 tag:${NC}"
    git tag -l "v*"
    exit 1
fi

# ===== 5. 安全检查:工作树状态 =====
if [ -n "$(git status --porcelain)" ]; then
    if [ "$KEEP_FLAG" = "--keep" ]; then
        echo -e "${YELLOW}⚠️  工作树有未提交改动,先 stash...${NC}"
        git stash push -u -m "rollback.sh 自动备份 @ $(date +%Y%m%d_%H%M%S)"
    else
        echo -e "${RED}❌ 工作树有未提交改动,请先 commit 或 stash${NC}"
        echo "  或使用 --keep 选项自动备份:"
        echo "  bash scripts/rollback.sh $TARGET_TAG --keep"
        exit 1
    fi
fi

# ===== 6. 执行回退 =====
echo -e "${YELLOW}🔄 准备回退到 $TARGET_TAG...${NC}"

# 获取 tag 信息
TAG_DATE=$(git log -1 --format="%ci" "$TARGET_TAG")
TAG_MSG=$(git tag -l -n1 "$TARGET_TAG" | sed 's/^[^ ]* *//')
echo "  Tag:      $TARGET_TAG"
echo "  Date:     $TAG_DATE"
echo "  Message:  $TAG_MSG"
echo ""

# 6.1 git reset --hard(默认)
if [ "$KEEP_FLAG" != "--keep-current" ]; then
    echo -e "${YELLOW}执行: git reset --hard $TARGET_TAG${NC}"
    git reset --hard "$TARGET_TAG"
fi

# 6.2 验证 L1 测试
echo ""
echo -e "${YELLOW}🧪 验证 L1 测试...${NC}"
if python3 -m unittest discover 03-执行/tests/unit 2>&1 | tail -3 | grep -q "OK"; then
    echo -e "${GREEN}✅ L1 测试 PASS${NC}"
else
    echo -e "${RED}❌ L1 测试 FAIL,可能回退后代码损坏${NC}"
    echo "  回退操作已完成,但测试失败,请人工检查"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ 回退成功!${NC}"
echo "  当前 HEAD: $(git log -1 --format='%h %s')"
echo "  当前 VERSION: $(cat VERSION)"
echo ""
echo "后续可选操作:"
echo "  git log --oneline -10              # 查看历史"
echo "  git diff HEAD~5                    # 查看最近 5 个 commit 差异"
echo "  bash scripts/rollback.sh           # 查看其他 tag"