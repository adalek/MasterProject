#!/usr/bin/env bash

set -e

PROJECT_ROOT="/home/s5803453/Desktop/MasterProject"

cd "$PROJECT_ROOT"

echo "Starting Houdini RAG server..."
echo "Project: $PROJECT_ROOT"
echo "URL: http://127.0.0.1:8000"

exec uv run uvicorn src.rag_server:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload