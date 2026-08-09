#!/bin/bash

set -euo pipefail

##############################################################
# Load Framework
##############################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECURITY_DIR="$(dirname "$SCRIPT_DIR")"

source "$SECURITY_DIR/scripts/config.sh"
source "$SECURITY_DIR/scripts/logger.sh"
source "$SECURITY_DIR/scripts/docker.sh"
source "$SECURITY_DIR/scripts/utils.sh"

TARGET="${1:-all}"

##############################################################
# Banner
##############################################################

echo
echo "=================================================="
echo "               TRIVY SECURITY SCAN ($TARGET)"
echo "=================================================="
echo

##############################################################
# Validate Docker
##############################################################

log_info "Checking Docker..."
check_docker

##############################################################
# Check Trivy Image
##############################################################

log_info "Checking Trivy image..."
pull_image_if_missing "$TRIVY_IMAGE"

create_report_directory "$TRIVY_REPORT_DIR"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

##############################################################
# Backend Scan
##############################################################

if [ "$TARGET" == "backend" ] || [ "$TARGET" == "all" ]; then
    log_info "Checking Backend Docker image..."
    if ! docker image inspect "$BACKEND_IMAGE" >/dev/null 2>&1; then
        log_error "Backend image not found."
        exit 1
    fi

    BACKEND_JSON_HOST="$TRIVY_REPORT_DIR/backend_${TIMESTAMP}.json"
    BACKEND_JSON_CONTAINER="/workspace/compliance/reports/trivy/backend_${TIMESTAMP}.json"

    log_info "Scanning Backend Image..."
    BACKEND_SCAN_STATUS=0
    if ! docker run --rm \
      --net=host \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$HOME/.cache/trivy:/root/.cache/trivy" \
      -v "$PWD":/workspace \
      "$TRIVY_IMAGE" \
      image \
      --format json \
      -o "$BACKEND_JSON_CONTAINER" \
      "$BACKEND_IMAGE"; then
        log_warning "Backend scan with DB update failed. Retrying with --skip-db-update..."
        if ! docker run --rm \
          --net=host \
          -v /var/run/docker.sock:/var/run/docker.sock \
          -v "$HOME/.cache/trivy:/root/.cache/trivy" \
          -v "$PWD":/workspace \
          "$TRIVY_IMAGE" \
          image \
          --skip-db-update \
          --format json \
          -o "$BACKEND_JSON_CONTAINER" \
          "$BACKEND_IMAGE"; then
            log_error "Backend Trivy scan failed completely."
            BACKEND_SCAN_STATUS=1
        fi
    fi

    if [ $BACKEND_SCAN_STATUS -eq 0 ]; then
        log_success "Backend scan completed: $BACKEND_JSON_HOST"
    else
        log_error "Backend scan ended with errors."
        exit 1
    fi
fi

##############################################################
# Frontend Scan
##############################################################

if [ "$TARGET" == "frontend" ] || [ "$TARGET" == "all" ]; then
    log_info "Checking Frontend Docker image..."
    if ! docker image inspect "$FRONTEND_IMAGE" >/dev/null 2>&1; then
        log_error "Frontend image not found."
        exit 1
    fi

    FRONTEND_JSON_HOST="$TRIVY_REPORT_DIR/frontend_${TIMESTAMP}.json"
    FRONTEND_JSON_CONTAINER="/workspace/compliance/reports/trivy/frontend_${TIMESTAMP}.json"

    log_info "Scanning Frontend Image..."
    FRONTEND_SCAN_STATUS=0
    if ! docker run --rm \
      --net=host \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$HOME/.cache/trivy:/root/.cache/trivy" \
      -v "$PWD":/workspace \
      "$TRIVY_IMAGE" \
      image \
      --format json \
      -o "$FRONTEND_JSON_CONTAINER" \
      "$FRONTEND_IMAGE"; then
        log_warning "Frontend scan with DB update failed. Retrying with --skip-db-update..."
        if ! docker run --rm \
          --net=host \
          -v /var/run/docker.sock:/var/run/docker.sock \
          -v "$HOME/.cache/trivy:/root/.cache/trivy" \
          -v "$PWD":/workspace \
          "$TRIVY_IMAGE" \
          image \
          --skip-db-update \
          --format json \
          -o "$FRONTEND_JSON_CONTAINER" \
          "$FRONTEND_IMAGE"; then
            log_error "Frontend Trivy scan failed completely."
            FRONTEND_SCAN_STATUS=1
        fi
    fi

    if [ $FRONTEND_SCAN_STATUS -eq 0 ]; then
        log_success "Frontend scan completed: $FRONTEND_JSON_HOST"
    else
        log_error "Frontend scan ended with errors."
        exit 1
    fi
fi

echo
echo "=================================================="
echo "           TRIVY SCAN COMPLETED ($TARGET)"
echo "=================================================="
