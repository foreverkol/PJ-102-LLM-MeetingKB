#!/bin/bash
# ============================================================
# PJ-902-09-Git学习与实践 · 一键回退脚本
# ============================================================
# 用法:
#   ./rollback.sh                  列出所有版本（供选择）
#   ./rollback.sh v1.0.0          回退到指定版本
#   ./rollback.sh v1.0.0 --force  强制回退（跳过确认）
# ============================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 项目根目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

FORCE=false
if [ "$2" = "--force" ]; then
    FORCE=true
fi

# 无参数：列出所有版本
if [ -z "$1" ]; then
    echo -e "${BLUE}📋 可用版本（按时间倒序）:${NC}"
    echo ""
    if [ -z "$(git tag -l)" ]; then
        echo -e "${YELLOW}  无任何版本${NC}"
        echo ""
        echo "用法: $0 <version>"
        echo "示例: $0 v1.0.0"
        exit 0
    fi

    git tag -l --sort=-creatordate | nl -ba | while read line; do
        echo -e "  ${GREEN}$line${NC}"
    done
    echo ""
    echo -e "${BLUE}回退方法:${NC}"
    echo "  $0 v1.0.0           # 回退到指定版本"
    exit 0
fi

VERSION=$1

# 验证版本存在
if ! git tag -l | grep -q "^$VERSION$"; then
    echo -e "${RED}❌ 错误: 版本 $VERSION 不存在${NC}"
    echo ""
    echo -e "${BLUE}可用版本:${NC}"
    git tag -l --sort=-creatordate | head -10
    exit 1
fi

# 显示回退信息
echo -e "${BLUE}🔄 一键回退${NC}"
echo ""
echo -e "  目标版本: ${GREEN}$VERSION${NC}"
echo -e "  当前 commit: ${YELLOW}$(git rev-parse --short HEAD)${NC}"
echo -e "  目标 commit: ${GREEN}$(git rev-parse --short $VERSION)${NC}"
echo ""

# 显示目标版本信息
echo -e "${BLUE}📋 目标版本信息:${NC}"
git log -1 --pretty=format:"  Commit: %h%n  Date: %ci%n  Message: %s%n" "$VERSION"
echo ""

# 确认
if [ "$FORCE" = false ]; then
    echo -e "${YELLOW}⚠️  确认回退到 $VERSION? [y/N]${NC}"
    read -r confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}🚀 开始回退...${NC}"

# 1. 保存当前状态
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD")
STASH_NAME="auto-stash-$(date +%Y%m%d_%H%M%S)"

if [ -n "$(git status --porcelain)" ]; then
    echo -e "  [1/4] ${BLUE}保存当前状态...${NC}"
    git stash push -u -m "$STASH_NAME" > /dev/null
    echo -e "        ${GREEN}✅ 已保存到 stash: $STASH_NAME${NC}"
else
    echo -e "  [1/4] ${YELLOW}工作区干净，无需保存${NC}"
fi

# 2. 切换版本
echo -e "  [2/4] ${BLUE}切换到 $VERSION...${NC}"
git checkout "$VERSION" > /dev/null 2>&1
echo -e "        ${GREEN}✅ 已切换到 $VERSION${NC}"

# 3. 恢复依赖
echo -e "  [3/4] ${BLUE}恢复依赖...${NC}"
if [ -f requirements.txt ]; then
    pip install -r requirements.txt --quiet 2>/dev/null || \
        echo -e "        ${YELLOW}⚠️  pip install 失败（可能无 requirements.txt 或网络问题）${NC}"
    echo -e "        ${GREEN}✅ 依赖已恢复${NC}"
else
    echo -e "        ${YELLOW}⚠️  无 requirements.txt，跳过${NC}"
fi

# 4. 验证（如果项目有测试）
echo -e "  [4/4] ${BLUE}验证回退...${NC}"
if [ -f tests/unit/smoke_test.py ]; then
    if python3 tests/unit/smoke_test.py > /tmp/rollback_test.log 2>&1; then
        echo -e "        ${GREEN}✅ 测试通过${NC}"
    else
        echo -e "        ${RED}❌ 测试失败（查看 /tmp/rollback_test.log）${NC}"
        echo ""
        echo "继续? [y/N]"
        read -r continue_confirm
        if [[ ! "$continue_confirm" =~ ^[Yy]$ ]]; then
            echo "回退完成但测试失败，请检查"
            exit 1
        fi
    fi
else
    echo -e "        ${YELLOW}⚠️  无测试脚本，跳过验证${NC}"
fi

echo ""
echo -e "${GREEN}✅ 回退成功: $VERSION${NC}"
echo ""
echo -e "${BLUE}📌 后续操作:${NC}"
echo "  • 查看代码:    ls"
echo "  • 查看 stash:  git stash list"
echo "  • 恢复 stash:  git stash pop"
echo "  • 回到 main:   git checkout main"
echo "  • 跑项目:      python3 pipeline.py --limit 10"