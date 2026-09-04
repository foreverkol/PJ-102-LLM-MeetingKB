#!/usr/bin/env bash
#
# scripts/run_full_pipeline.sh - PJ-102 v3.0 全量跑批脚本
#
# 王老师 09-04 13:00 明确:不要全量跑全量录音文字,只跑 10 个测试样例
# 因此本脚本默认 SAMPLE_LIMIT=10,可在环境变量调整
#
# 设计:
#   - 默认 sample_limit=10(王老师指令)
#   - workers=1(LLM 限流)
#   - timeout=900s 单文件
#   - 失败 fail-fast 不静默
#   - 全程日志落 SYSTEM/logs/full_run_$(date).log
#
set -euo pipefail

# ============ 参数 ============
PJ102_ROOT="/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB"
CODE_DIR="$PJ102_ROOT/03-执行/code"
SOURCE_DIR="/mnt/d/BaiduSyncdisk/hermes/修改发言人转化"
WIKI_DIR="/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB"
LOGS_DIR="$PJ102_ROOT/03-执行/SYSTEM/logs"
STATE_DIR="$PJ102_ROOT/03-执行/SYSTEM/state"

mkdir -p "$LOGS_DIR" "$STATE_DIR"

# 王老师限制:≤10 sample
SAMPLE_LIMIT="${SAMPLE_LIMIT:-10}"

# 跑测开关:WRITE=1 写入 WIKI,=0 dry-run
WRITE="${WRITE:-0}"

# 失败容忍:FAIL_FAST=1 失败立即退出,=0 继续(默认 1)
FAIL_FAST="${FAIL_FAST:-1}"

LOG_FILE="$LOGS_DIR/full_run_$(date +%Y-%m-%d_%H%M).log"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
log() { echo "[$(TS)] $*" | tee -a "$LOG_FILE"; }
die() { log "❌ FATAL: $*"; exit 1; }

log "=========================================="
log "PJ-102 v3.0 全量跑批启动(SAMPLE_LIMIT=$SAMPLE_LIMIT)"
log "=========================================="

# ============ Preflight ============
log "[1/3] Preflight"

command -v python3 >/dev/null 2>&1 || die "python3 未安装"
[[ -d "$SOURCE_DIR" ]] || die "源目录不存在: $SOURCE_DIR"
[[ -d "$CODE_DIR" ]] || die "代码目录不存在: $CODE_DIR"

if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
    if [[ -f ~/.hermes/secrets.d/minimax_api_key.txt ]]; then
        export MINIMAX_API_KEY=$(cat ~/.hermes/secrets.d/minimax_api_key.txt)
        log "✓ MiniMax API Key 从 secrets.d 加载"
    else
        die "MiniMax API Key 未设置"
    fi
fi
export MINIMAX_CN_BASE_URL="${MINIMAX_CN_BASE_URL:-https://api.minimaxi.com/v1}"

# ============ 全量计数 ============
md_count=$(find "$SOURCE_DIR" -maxdepth 1 -name "*.md" | wc -l)
log "源目录总文件数: $md_count"
log "本次跑批数(SAMPLE_LIMIT): $SAMPLE_LIMIT"
log "剩余文件将留待后续: $((md_count - SAMPLE_LIMIT))"

# ============ Run pipeline.py ============
log "[2/3] 运行 pipeline.py --limit $SAMPLE_LIMIT"

cd "$CODE_DIR"

limit_flag="--limit $SAMPLE_LIMIT"
write_flag=""
if [[ "$WRITE" == "1" ]]; then
    write_flag="--write"
    log "  ⚠️ WRITE=1,本次会写入 WIKI/$WIKI_DIR"
else
    log "  → WRITE=0 dry-run 模式(只验证可执行,不写 WIKI)"
fi

if python3 pipeline.py $limit_flag $write_flag 2>&1 | tee -a "$LOG_FILE" | tail -30; then
    log "✓ pipeline.py 跑批完成"
else
    if [[ "$FAIL_FAST" == "1" ]]; then
        die "pipeline.py 失败(FAIL_FAST=1)"
    else
        log "⚠️ pipeline.py 失败但 FAIL_FAST=0,继续"
    fi
fi

# ============ Lint 巡检 ============
log "[3/3] lint_wiki.py 健康巡检(8 维度)"

python3 lint_wiki.py "$WIKI_DIR/WIKI/" 2>&1 \
    | tee "$LOGS_DIR/last_lint.json" \
    | head -30

# ============ 飞书告警(可选) ============
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
log "PJ-102 v3.0 全量跑批完成"
log "=========================================="
exit 0
