#!/bin/bash
set -euo pipefail

##############################################################
# OWASP ZAP DAST Security Scanner
##############################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

source "$PROJECT_ROOT/security/config/tools.conf" 2>/dev/null || true

ZAP_IMAGE="${ZAP_IMAGE:-ghcr.io/zaproxy/zaproxy:stable}"
OUTPUT_DIR="$PROJECT_ROOT/compliance/reports/zap"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RAW_REPORT="$OUTPUT_DIR/zap_${TIMESTAMP}.json"

mkdir -p "$OUTPUT_DIR"

echo "=================================================="
echo "             OWASP ZAP DAST SECURITY SCAN"
echo "=================================================="
echo "[INFO] Checking Docker..."

if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed or not in PATH."
    exit 1
fi

echo "[INFO] Checking OWASP ZAP image..."
if ! docker image inspect "$ZAP_IMAGE" &> /dev/null; then
    echo "[INFO] Pulling OWASP ZAP image ($ZAP_IMAGE)..."
    docker pull "$ZAP_IMAGE"
fi

# Detect Docker Compose network name
DOCKER_NET=""
if docker network inspect devsecops_devsecops-network &>/dev/null; then
    DOCKER_NET="devsecops_devsecops-network"
elif docker network inspect sentinelops-network &>/dev/null; then
    DOCKER_NET="sentinelops-network"
fi

if [ -n "$DOCKER_NET" ]; then
    TARGET_URL="${ZAP_TARGET_URL:-http://sentinelops-frontend:8080}"
    NET_FLAG="--network=$DOCKER_NET"
    echo "[INFO] Detected container network: $DOCKER_NET"
else
    TARGET_URL="${ZAP_TARGET_URL:-http://localhost:3000}"
    NET_FLAG="--network=host"
    echo "[INFO] Container network not detected. Using host network..."
fi

echo "[INFO] Target URL: $TARGET_URL"

echo "[INFO] Running OWASP ZAP DAST Baseline Scan..."

# Run ZAP scan. ZAP returns code 1 if warnings found, 2 if errors found, 0 if pass.
ZAP_EXIT=0
docker run --rm \
    $NET_FLAG \
    -v "$OUTPUT_DIR:/zap/wrk:rw" \
    "$ZAP_IMAGE" \
    zap-baseline.py \
    -t "$TARGET_URL" \
    -J "zap_${TIMESTAMP}.json" || ZAP_EXIT=$?

if [ ! -f "$RAW_REPORT" ]; then
    echo "[ERROR] OWASP ZAP scan failed to generate report file ($RAW_REPORT)."
    exit 1
fi

echo "[SUCCESS] OWASP ZAP DAST Scan Execution Completed."
echo "Report Generated: $RAW_REPORT"
echo "=================================================="
