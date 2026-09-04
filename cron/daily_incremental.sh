#!/usr/bin/env bash
#
# cron/daily_incremental.sh - PJ-102 v3.0 定时增量调度
#
# 安装(王老师 cron):
#   0 9,18 * * * cd /mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB && bash cron/daily_incremental.sh >> logs/daily.log 2>&1
#
# 设计:
#   - 不破坏原则:源文件只读 + 输出只写 SYSTEM + 飞书可选
#   - 三步式:preflight → run → notify
#   - 失败 fail-fast 不静默(Superpower 铁律:fail-silent 是反模式)
#
set -euo pipefail

# ============ 常量 ============
PJ102_ROOT="/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
CODE_DIR="$PJ102_ROOT/03-执行/code"
SOURCE_DIR="/mnt/d/BaiduSyncdisk/hermes/修改发言人转化"
STATE_FILE="$PJ102_ROOT/03-执行/SYSTEM/state/processed_files.json"
LOGS_DIR="$PJ102_ROOT/03-执行/SYSTEM/logs"

mkdir -p "$LOGS_DIR" "$(dirname "$STATE_FILE")"

LOG_FILE="$LOGS_DIR/daily_$(date +%Y-%m-%d).log"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

log() { echo "[$TIMESTAMP] $*" | tee -a "$LOG_FILE"; }
die() { log "❌ FATAL: $*"; exit 1; }

log "=========================================="
log "PJ-102 v3.0 daily_incremental 启动"
log "=========================================="

# ============ Step 1: Preflight ============
log "[1/3] Preflight 检查"

# 1.1: Python 环境
command -v python3 >/dev/null 2>&1 || die "python3 未安装"

# 1.2: MiniMax API Key
if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
    if [[ -f ~/.hermes/secrets.d/minimax_api_key.txt ]]; then
        export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
        log "✓ MiniMax API Key 从 secrets.d 加载"
    else
        die "MiniMax API Key 未设置(env 变量 + secrets.d 都无)"
    fi
else
    log "✓ MiniMax API Key 已设置(env)"
fi

# 1.3: MiniMax base URL
export MINIMAX_CN_BASE_URL="${MINIMAX_CN_BASE_URL:-https://api.minimaxi.com/v1}"

# 1.4: 源目录
[[ -d "$SOURCE_DIR" ]] || die "源目录不存在: $SOURCE_DIR"

# 1.5: 代码目录
[[ -d "$CODE_DIR" ]] || die "代码目录不存在: $CODE_DIR"

# 1.6: 计数器
md_count=$(find "$SOURCE_DIR" -maxdepth 1 -name "*.md" | wc -l)
log "✓ 源目录含 $md_count 个 _原文.md"

# ============ Step 2: Run daily_incremental ============
log "[2/3] 运行 daily_incremental.py"

# 切换到 code dir
cd "$CODE_DIR"

# 跑增量(dry-run 先看)
log "  → dry-run 检测新文件"
python3 daily_incremental.py \
    --source "$SOURCE_DIR" \
    --state "$STATE_FILE" \
    --dry-run \
    2>&1 | tee -a "$LOG_FILE" | head -50

# 真实跑(无 dry_run flag)
log "  → 真实跑 pipeline"
python3 daily_incremental.py \
    --source "$SOURCE_DIR" \
    --state "$STATE_FILE" \
    2>&1 | tee -a "$LOG_FILE" | head -50

# ============ Step 3: Lint 巡检 ============
log "[3/3] lint_wiki.py 健康巡检"

python3 lint_wiki.py "$PJ102_ROOT/02-知识库/PJ-102-LLM-MeetingKB/WIKI/" 2>&1 \
    | tee -a "$LOG_FILE" | head -30

# ============ Step 4: 飞书告警(可选) ============
if [[ -n "${FEISHU_WEBHOOK_URL:-}" ]] || [[ -f ~/.hermes/secrets.d/feishu_webhook.txt ]]; then
    log "[可选] 飞书告警"
    if [[ -z "${FEISHU_WEBHOOK_URL:-}" ]] && [[ -f ~/.hermes/secrets.d/feishu_webhook.txt ]]; then
        export FEISHU_WEBHOOK_URL=$(cat ~/.hermes/secrets.d/feishu_webhook.txt)
    fi
    python3 feishu_lint_alert.py --report "$LOGS_DIR/last_lint.json" 2>&1 | tail -10
else
    log "[可选] 飞书 webhook 未配置,跳过告警"
fi

log "=========================================="
log "PJ-102 v3.0 daily_incremental 完成"
log "=========================================="
exit 0
