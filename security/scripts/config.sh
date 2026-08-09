#!/bin/bash

##################################################
# Project Configuration
##################################################

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Load .env variables if present
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

##################################################
# Report Directories
##################################################

REPORT_ROOT="$PROJECT_ROOT/compliance/reports"

HADOLINT_REPORT_DIR="$REPORT_ROOT/hadolint"
TRIVY_REPORT_DIR="$REPORT_ROOT/trivy"
SEMGREP_REPORT_DIR="$REPORT_ROOT/semgrep"
GITLEAKS_REPORT_DIR="$REPORT_ROOT/gitleaks"
ZAP_REPORT_DIR="$REPORT_ROOT/zap"

##################################################
# Tool Images
##################################################

HADOLINT_IMAGE="hadolint/hadolint:latest"

TRIVY_IMAGE="aquasec/trivy:latest"

GITLEAKS_IMAGE="zricethezav/gitleaks:latest"


##################################################
# Dockerfiles
##################################################

BACKEND_DOCKERFILE="$PROJECT_ROOT/app/server/Dockerfile"

FRONTEND_DOCKERFILE="$PROJECT_ROOT/app/client/Dockerfile"

##################################################
# Backend Image
##################################################

BACKEND_IMAGE="sentinelops-backend:latest"

##################################################
# Frontend Image
##################################################

FRONTEND_IMAGE="sentinelops-frontend:latest"
