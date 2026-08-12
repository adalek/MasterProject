#!/usr/bin/env bash

set -e

PROJECT_ROOT="/home/s5803453/Desktop/MasterProject"

cd "$PROJECT_ROOT"

echo "Rebuilding Houdini RAG database..."
uv run python -m rag.ingest