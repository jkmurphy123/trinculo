#!/usr/bin/env bash
set -euo pipefail
export $(grep -v '^#' .env | xargs -d '\n' -I {} echo {})
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
