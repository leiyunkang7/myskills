#!/bin/bash
#
# browser-use + MiniMax 一键配置脚本
#
# 用法:
#   ./setup.sh              # 完整安装
#   ./setup.sh --chrome-only  # 仅启动 Chrome
#   ./setup.sh --check       # 检查状态
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${HOME}/.local/share/pipx/venvs/browser-use"
CHROME_PORT=9222
CHROME_DATA_DIR=/tmp/chrome-test

usage() {
    cat <<EOF
用法: $0 [选项]

选项:
  --chrome-only  仅启动 Chrome (跳过安装)
  --check       仅检查状态
  --help        显示此帮助

示例:
  $0                    # 完整安装
  $0 --chrome-only      # 快速启动 Chrome
  $0 --check            # 检查配置状态
EOF
}

log() { echo "[$(date '+%H:%M:%S')] $*"; }
warn() { echo "[$(date '+%H:%M:%S')] ⚠️  $*" >&2; }
error() { echo "[$(date '+%H:%M:%S')] ❌  $*" >&2; }

check_chrome() {
    log "检查 Chrome..."
    if curl -s "http://127.0.0.1:${CHROME_PORT}/json/version" > /dev/null 2>&1; then
        log "✅ Chrome CDP 正常运行 (端口 ${CHROME_PORT})"
        return 0
    else
        warn "Chrome 未运行"
        return 1
    fi
}

start_chrome() {
    local chrome_path

    # 查找 Chrome
    chrome_path=$(find "${HOME}/.cache/ms-playwright" -name "chrome" -type f 2>/dev/null | grep -E "chromium-1217|chromium-1208" | head -1)

    if [ -z "$chrome_path" ]; then
        # 尝试其他位置
        chrome_path=$(find "${HOME}/.cache/ms-playwright" -name "chrome" -type f 2>/dev/null | head -1)
    fi

    if [ -z "$chrome_path" ] || [ ! -f "$chrome_path" ]; then
        error "未找到 Chrome 可执行文件"
        return 1
    fi

    log "启动 Chrome: $chrome_path"

    # 启动 Xvfb (如果需要)
    if [ -z "$DISPLAY" ]; then
        export DISPLAY=:99
    fi

    if ! pgrep -f "Xvfb ${DISPLAY}" > /dev/null 2>&1; then
        log "启动 Xvfb..."
        Xvfb "${DISPLAY}" -screen 0 1280x720x24 &
        sleep 2
    fi

    # 启动 Chrome
    log "启动 Chrome headless (CDP 端口 ${CHROME_PORT})..."
    nohup "$chrome_path" \
        --headless=new \
        --no-sandbox \
        --disable-setuid-sandbox \
        --disable-dev-shm-usage \
        --remote-debugging-port="${CHROME_PORT}" \
        --user-data-dir="${CHROME_DATA_DIR}" \
        > /tmp/chrome.log 2>&1 &

    sleep 3

    if check_chrome; then
        log "✅ Chrome 启动成功"
        return 0
    else
        error "Chrome 启动失败，查看日志: tail /tmp/chrome.log"
        return 1
    fi
}

install() {
    log "=== 安装 browser-use + MiniMax ==="

    # 1. 安装 browser-use
    if ! command -v browser-use &> /dev/null; then
        log "安装 browser-use..."
        pipx install browser-use
    else
        log "✅ browser-use 已安装"
    fi

    # 2. 安装 playwright
    log "安装 playwright..."
    if [ -d "$VENV_PATH" ]; then
        "$VENV_PATH/bin/python" -m pip install playwright --quiet 2>/dev/null || warn "playwright 安装跳过"
    fi

    # 3. 降级 websockets
    log "降级 websockets (解决 WebSocket 兼容性问题)..."
    if [ -d "$VENV_PATH" ]; then
        WS_VERSION=$("$VENV_PATH/bin/python" -c "import websockets; print(websockets.__version__)" 2>/dev/null || echo "unknown")
        log "  当前版本: $WS_VERSION"
        if [ "$WS_VERSION" != "13.1" ]; then
            "$VENV_PATH/bin/python" -m pip install "websockets<14" --quiet 2>/dev/null || warn "websockets 降级跳过"
        fi
    fi

    # 4. 启动 Chrome
    start_chrome

    log "=== 配置完成 ==="
    echo ""
    echo "下一步:"
    echo "  1. 运行测试: python ${SCRIPT_DIR}/minimax_llm_wrapper.py"
    echo "  2. 使用 wrapper:"
    echo "       from minimax_llm_wrapper import MiniMaxLLM"
    echo "       llm = MiniMaxLLM()"
    echo ""
}

# 主逻辑
case "${1:-}" in
    --chrome-only)
        start_chrome
        ;;
    --check)
        check_chrome
        ;;
    --help|-h)
        usage
        exit 0
        ;;
    *)
        install
        ;;
esac