#!/usr/bin/env bash

set -e

kubectl rollout status deployment/backend \
-n sentinelops

kubectl rollout status deployment/frontend \
-n sentinelops