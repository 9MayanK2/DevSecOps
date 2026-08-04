#!/usr/bin/env bash

kubectl rollout undo deployment/backend \
-n sentinelops

kubectl rollout undo deployment/frontend \
-n sentinelops