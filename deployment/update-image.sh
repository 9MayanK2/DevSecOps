#!/usr/bin/env bash

set -e

IMAGE_TAG="$1"

ACCOUNT_ID="284064534086"

REGION="us-east-1"

NAMESPACE="sentinelops"

kubectl set image deployment/backend \
backend=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/sentinelops-backend:${IMAGE_TAG} \
-n ${NAMESPACE}

kubectl set image deployment/frontend \
frontend=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/sentinelops-frontend:${IMAGE_TAG} \
-n ${NAMESPACE}