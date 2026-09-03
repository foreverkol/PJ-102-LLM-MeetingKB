#!/bin/bash
# ============================================================
# PJ-902-09-Git学习与实践 · 版本管理 CLI
# ============================================================
# 用法:
#   ./version_manager.sh list                          # 列出所有版本
#   ./version_manager.sh create v1.0.0 "Release note"   # 创建版本
#   ./version_manager.sh delete v1.0.0                  # 删除版本
#   ./version_manager.sh info                           # 显示当前版本信息
#   ./version_manager.sh update v1.0.1                  # 更新 VERSION 文件
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

# 帮助
show_help() {
    echo -e "${BLUE}PJ-902-09 版本管理 CLI${NC}"
    echo ""
    echo "用法: $0 <command> [args]"
    echo ""
    echo "命令:"
    echo "  list                    列出所有版本"
    echo "  create <version> [msg]  创建并推送新版本（tag）"
    echo "  delete <version>        删除指定版本（本地 + 远程）"
    echo "  info                    显示当前版本信息"
    echo "  update <version>        更新 VERSION 文件"
    echo "  help                    显示此帮助"
    echo ""
    echo "示例:"
    echo "  $0 list"
    echo "  $0 create v1.0.0 'Release v1.0.0: 全项全量移植完成'"
    echo "  $0 delete v0.9.0"
    echo "  $0 info"
    echo "  $0 update v1.0.1"
}

# 列出所有版本
cmd_list() {
    echo -e "${BLUE}📋 所有版本（按时间倒序）:${NC}"
    echo ""
    if git tag -l | head -1 > /dev/null 2>&1; then
        git tag -l --sort=-creatordate | nl -ba
    else
        echo -e "${YELLOW}  无任何版本${NC}"
    fi
    echo ""
    echo -e "${BLUE}📍 当前版本:${NC}"
    if [ -f VERSION ]; then
        cat VERSION
    else
        echo "  VERSION 文件不存在"
    fi
}

# 创建版本
cmd_create() {
    local VERSION=$1
    local MSG=${2:-"Release $VERSION"}

    if [ -z "$VERSION" ]; then
        echo -e "${RED}❌ 错误: 请提供版本号${NC}"
        echo "示例: $0 create v1.0.0"
        exit 1
    fi

    # 验证 SemVer
    if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
        echo -e "${RED}❌ 错误: 版本号不符合 SemVer 规范（v主.次.修订）${NC}"
        echo "示例: v1.0.0 / v1.0.0-rc.1"
        exit 1
    fi

    # 检查是否已存在
    if git tag -l | grep -q "^$VERSION$"; then
        echo -e "${RED}❌ 错误: 版本 $VERSION 已存在${NC}"
        exit 1
    fi

    # 更新 VERSION 文件
    echo "$VERSION" > VERSION

    echo -e "${BLUE}📦 创建版本 $VERSION${NC}"
    echo ""

    # 提交 VERSION 文件
    git add VERSION
    if ! git diff --cached --quiet; then
        git commit -m "chore: bump version to $VERSION"
    fi

    # 创建 tag
    git tag -a "$VERSION" -m "$MSG"
    echo -e "${GREEN}✅ 已创建本地 tag: $VERSION${NC}"

    # 推送
    echo ""
    echo -e "${BLUE}📤 推送到远程...${NC}"
    git push origin main || echo -e "${YELLOW}⚠️  推送 main 失败（可能需要 PR 流程）${NC}"
    git push origin "$VERSION"
    echo -e "${GREEN}✅ 已推送 tag: $VERSION${NC}"

    echo ""
    echo -e "${GREEN}✅ 版本 $VERSION 已创建并推送${NC}"
    echo -e "${YELLOW}📌 下一步: GitHub Actions 将自动测试并创建 Release${NC}"
    echo -e "${YELLOW}📌 查看: https://github.com/<user>/<repo>/releases/tag/$VERSION${NC}"
}

# 删除版本
cmd_delete() {
    local VERSION=$1

    if [ -z "$VERSION" ]; then
        echo -e "${RED}❌ 错误: 请提供版本号${NC}"
        echo "示例: $0 delete v0.9.0"
        exit 1
    fi

    echo -e "${YELLOW}⚠️  确认删除版本 $VERSION? [y/N]${NC}"
    read -r confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi

    # 删除本地
    git tag -d "$VERSION" 2>/dev/null && echo -e "${GREEN}✅ 已删除本地 tag${NC}" || echo -e "${YELLOW}⚠️  本地 tag 不存在${NC}"

    # 删除远程
    git push origin :refs/tags/"$VERSION" 2>/dev/null && echo -e "${GREEN}✅ 已删除远程 tag${NC}" || echo -e "${YELLOW}⚠️  远程 tag 删除失败（可能不存在）${NC}"

    # 删除 GitHub Release（需要 gh CLI）
    if command -v gh &> /dev/null; then
        gh release delete "$VERSION" --yes 2>/dev/null && echo -e "${GREEN}✅ 已删除 GitHub Release${NC}" || true
    fi
}

# 信息
cmd_info() {
    echo -e "${BLUE}📊 项目版本信息${NC}"
    echo ""

    # 当前 tag
    local CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "(无)")
    echo -e "  当前最近 tag: ${GREEN}$CURRENT_TAG${NC}"

    # 提交数
    local COMMIT_COUNT=$(git rev-list --count HEAD)
    echo -e "  总提交数: ${GREEN}$COMMIT_COUNT${NC}"

    # 最后提交
    echo ""
    echo -e "  最后提交:"
    git log -1 --pretty=format:"    %h - %s (%ci)" | head -1
    echo ""

    # VERSION 文件
    echo ""
    if [ -f VERSION ]; then
        echo -e "  VERSION 文件: ${GREEN}$(cat VERSION)${NC}"
    else
        echo -e "  VERSION 文件: ${YELLOW}不存在${NC}"
    fi

    # 远程仓库
    echo ""
    echo -e "  远程仓库:"
    git remote -v | head -2
}

# 更新 VERSION 文件
cmd_update() {
    local VERSION=$1

    if [ -z "$VERSION" ]; then
        echo -e "${RED}❌ 错误: 请提供版本号${NC}"
        exit 1
    fi

    echo "$VERSION" > VERSION
    git add VERSION
    git commit -m "chore: bump version to $VERSION"
    echo -e "${GREEN}✅ VERSION 文件已更新为 $VERSION${NC}"
}

# 主入口
case "${1:-help}" in
    list)
        cmd_list
        ;;
    create)
        cmd_create "$2" "$3"
        ;;
    delete|rm)
        cmd_delete "$2"
        ;;
    info|status)
        cmd_info
        ;;
    update|bump)
        cmd_update "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac