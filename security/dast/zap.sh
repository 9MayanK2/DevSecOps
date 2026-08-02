#!/bin/bash
set -euo pipefail

##############################################################
# OWASP ZAP DAST Security Scanner
##############################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$PROJECT_ROOT/security/config/tools.conf" 2>/dev/null || true

ZAP_IMAGE="${ZAP_IMAGE:-ghcr.io/zaproxy/zaproxy:stable}"
TARGET_URL="${ZAP_TARGET_URL:-http://localhost:5000}"
OUTPUT_DIR="$PROJECT_ROOT/compliance/reports/zap"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RAW_REPORT="$OUTPUT_DIR/zap_${TIMESTAMP}.json"

mkdir -p "$OUTPUT_DIR"

echo "=================================================="
echo "             OWASP ZAP DAST SECURITY SCAN"
echo "=================================================="
echo "[INFO] Target URL: $TARGET_URL"
echo "[INFO] Checking Docker..."

if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed or not in PATH."
    exit 1
fi

echo "[INFO] Checking OWASP ZAP image..."
if ! docker image inspect "$ZAP_IMAGE" &> /dev/null; then
    echo "[INFO] Pulling OWASP ZAP image ($ZAP_IMAGE)..."
    docker pull "$ZAP_IMAGE" || true
fi

echo "[INFO] Running OWASP ZAP DAST Baseline Scan..."

docker run --rm \
    --network host \
    --user "$(id -u):$(id -g)" \
    -v "$OUTPUT_DIR:/zap/wrk" \
    "$ZAP_IMAGE" \
    zap-baseline.py \
    -t "$TARGET_URL" \
    -J "zap_${TIMESTAMP}.json" \
    -I

if [ ! -f "$RAW_REPORT" ]; then
    echo "[ERROR] ZAP report was not generated."
    exit 1
fi

echo "[SUCCESS] OWASP ZAP DAST Scan Completed."
echo "Report Generated: $RAW_REPORT"
echo "=================================================="
