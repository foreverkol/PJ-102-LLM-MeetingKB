#!/usr/bin/env bash
#
# scripts/run_atomicstrata_mcp.sh - 启动 atomicstrata MCP server(供 Hermes/Codex 通过 stdio 调用)
#
# 安装依赖:
#   npm install -g llm-wiki-compiler  (v0.4.0+)
#
# 王老师 MiniMax-M3 配置:
#   atomicstrata 内置 minimax provider 用 api.minimax.io(美区,不兼容 MiniMax-M3 中国区)
#   绕过方案:走 OpenAI 兼容层 LLMWIKI_PROVIDER=openai + OPENAI_BASE_URL=https://api.minimaxi.com/v1
#
# 王老师运行:
#   bash scripts/run_atomicstrata_mcp.sh
#
# Hermes 集成 (config.yaml mcp_servers):
#   - name: atomicstrata
#     command: bash /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB/scripts/run_atomicstrata_mcp.sh
#     args: []
#
set -euo pipefail

PJ102_ROOT="/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
LLMWIKI_ROOT="${LLMWIKI_ROOT:-/tmp/poc_atomicstrata}"

# ============ Preflight ========= ===
command -v llmwiki >/dev/null 2>&1 || {
    echo "❌ llmwiki 未装"
    echo "   安装: npm install -g llm-wiki-compiler"
    exit 1
}

# ============ MiniMax-M3 OpenAI 兼容配置 =========
if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
    if [[ -f ~/.hermes/secrets.d/minimax_api_key.txt ]]; then
        export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
    else
        echo "❌ MINIMAX_API_KEY 未设置(env 或 ~/.hermes/secrets.d/minimax_api_key.txt)"
        exit 1
    fi
fi

export OPENAI_API_KEY="$MINIMAX_API_KEY"
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://api.minimaxi.com/v1}"
export LLMWIKI_PROVIDER="openai"
export LLMWIKI_MODEL="MiniMax-M3"

# ============ 准备 llmwiki root(若不存在自动建) =========
if [[ ! -d "$LLMWIKI_ROOT/sources" ]]; then
    mkdir -p "$LLMWIKI_ROOT/sources"
fi

if [[ ! -f "$LLMWIKI_ROOT/.llmwiki/schema.json" ]]; then
    echo "ℹ️ 初始化 llmwiki schema: $LLMWIKI_ROOT"
    (cd "$LLMWIKI_ROOT" && llmwiki schema init >/dev/null 2>&1)
fi

# ============ 启 MCP server(stdio) =========
# atomicstrata 的 stdio 协议遵循 JSON-RPC 2.0 + MCP 2024-11-05
# Hermes 通过 mcp_servers.command 自动 spawn 并接管 stdin/stdout
exec llmwiki serve --root "$LLMWIKI_ROOT"