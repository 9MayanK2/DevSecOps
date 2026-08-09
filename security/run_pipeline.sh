#!/bin/bash
set -euo pipefail

##############################################################
# DevSecOps Master Pipeline Runner
##############################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

PYTHONPATH=. python3 security/core/orchestrator.py "$@"
