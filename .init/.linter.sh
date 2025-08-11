#!/bin/bash
cd /home/kavia/workspace/code-generation/user-plan-based-api-management-95986-95995/plan_based_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

