#!/bin/bash
# ============================================================
# PJ-902-09-Git学习与实践 · 版本验证脚本
# ============================================================
# 用法:
#   ./verify_version.sh
# ============================================================

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 版本验证${NC}"
echo ""

ERRORS=0
WARNINGS=0

# 1. 检查 git 仓库
echo -e "[1/10] 检查 git 仓库..."
if [ -d .git ]; then
    echo -e "      ${GREEN}✅ 是 git 仓库${NC}"
else
    echo -e "      ${RED}❌ 不是 git 仓库${NC}"
    ERRORS=$((ERRORS+1))
fi

# 2. 检查 VERSION 文件
echo -e "[2/10] 检查 VERSION 文件..."
if [ -f VERSION ]; then
    VERSION=$(cat VERSION)
    if [[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
        echo -e "      ${GREEN}✅ VERSION = $VERSION (SemVer 合规)${NC}"
    else
        echo -e "      ${YELLOW}⚠️  VERSION = $VERSION (不符合 SemVer)${NC}"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo -e "      ${RED}❌ VERSION 文件不存在${NC}"
    ERRORS=$((ERRORS+1))
fi

# 3. 检查 .gitignore
echo -e "[3/10] 检查 .gitignore..."
if [ -f .gitignore ]; then
    HAS_ENV=$(grep -c "^\.env$" .gitignore || echo 0)
    HAS_PYCACHE=$(grep -c "__pycache__" .gitignore || echo 0)
    if [ "$HAS_ENV" -gt 0 ] && [ "$HAS_PYCACHE" -gt 0 ]; then
        echo -e "      ${GREEN}✅ .gitignore 完整（含 .env 和 __pycache__）${NC}"
    else
        echo -e "      ${YELLOW}⚠️  .gitignore 不完整（建议添加 .env 和 __pycache__）${NC}"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo -e "      ${RED}❌ .gitignore 不存在${NC}"
    ERRORS=$((ERRORS+1))
fi

# 4. 检查 scripts/
echo -e "[4/10] 检查 scripts/..."
if [ -d scripts ]; then
    for script in version_manager.sh rollback.sh; do
        if [ -f "scripts/$script" ]; then
            if [ -x "scripts/$script" ]; then
                echo -e "      ${GREEN}✅ scripts/$script 可执行${NC}"
            else
                echo -e "      ${YELLOW}⚠️  scripts/$script 不可执行（chmod +x）${NC}"
                WARNINGS=$((WARNINGS+1))
            fi
        else
            echo -e "      ${YELLOW}⚠️  scripts/$script 不存在${NC}"
            WARNINGS=$((WARNINGS+1))
        fi
    done
else
    echo -e "      ${RED}❌ scripts/ 不存在${NC}"
    ERRORS=$((ERRORS+1))
fi

# 5. 检查 .github/workflows/
echo -e "[5/10] 检查 .github/workflows/..."
if [ -d .github/workflows ]; then
    HAS_TEST=$(ls .github/workflows/test.yml 2>/dev/null || echo "")
    HAS_RELEASE=$(ls .github/workflows/release.yml 2>/dev/null || echo "")
    if [ -n "$HAS_TEST" ] && [ -n "$HAS_RELEASE" ]; then
        echo -e "      ${GREEN}✅ test.yml + release.yml 都在${NC}"
    else
        echo -e "      ${YELLOW}⚠️  workflows 不完整（缺 test.yml 或 release.yml）${NC}"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo -e "      ${RED}❌ .github/workflows/ 不存在${NC}"
    ERRORS=$((ERRORS+1))
fi

# 6. 检查 README.md
echo -e "[6/10] 检查 README.md..."
if [ -f README.md ]; then
    SIZE=$(stat -c%s README.md)
    if [ "$SIZE" -gt 1000 ]; then
        echo -e "      ${GREEN}✅ README.md 存在（$SIZE 字节）${NC}"
    else
        echo -e "      ${YELLOW}⚠️  README.md 太短（$SIZE 字节）${NC}"
        WARNINGS=$((WARNINGS+1))
    fi
else
    echo -e "      ${RED}❌ README.md 不存在${NC}"
    ERRORS=$((ERRORS+1))
fi

# 7. 检查 tags
echo -e "[7/10] 检查 git tags..."
TAG_COUNT=$(git tag -l | wc -l)
echo -e "      ${BLUE}当前有 $TAG_COUNT 个 tag${NC}"
if [ "$TAG_COUNT" -gt 0 ]; then
    git tag -l --sort=-creatordate | head -3 | while read tag; do
        echo -e "        - $tag"
    done
fi

# 8. 检查远程仓库
echo -e "[8/10] 检查远程仓库..."
if git remote -v | grep -q origin; then
    ORIGIN=$(git remote get-url origin)
    echo -e "      ${GREEN}✅ origin: $ORIGIN${NC}"
else
    echo -e "      ${YELLOW}⚠️  无 origin 远程仓库${NC}"
    WARNINGS=$((WARNINGS+1))
fi

# 9. 检查工作区状态
echo -e "[9/10] 检查工作区状态..."
if [ -z "$(git status --porcelain)" ]; then
    echo -e "      ${GREEN}✅ 工作区干净${NC}"
else
    echo -e "      ${YELLOW}⚠️  有未提交的更改${NC}"
    git status --short | head -5
    WARNINGS=$((WARNINGS+1))
fi

# 10. 检查测试
echo -e "[10/10] 检查测试..."
if [ -d tests ]; then
    TEST_COUNT=$(find tests -name "*.py" 2>/dev/null | wc -l)
    echo -e "      ${GREEN}✅ 有 $TEST_COUNT 个测试文件${NC}"
else
    echo -e "      ${YELLOW}⚠️  无 tests/ 目录${NC}"
    WARNINGS=$((WARNINGS+1))
fi

# 总结
echo ""
echo -e "${BLUE}=========================================${NC}"
if [ "$ERRORS" -eq 0 ]; then
    if [ "$WARNINGS" -eq 0 ]; then
        echo -e "${GREEN}✅ 所有检查通过（0 错误，0 警告）${NC}"
    else
        echo -e "${YELLOW}⚠️  通过（有 $WARNINGS 个警告）${NC}"
    fi
    exit 0
else
    echo -e "${RED}❌ 有 $ERRORS 个错误，$WARNINGS 个警告${NC}"
    exit 1
fi