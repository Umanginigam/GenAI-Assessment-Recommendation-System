#!/bin/bash
set -e

echo "=================================================="
echo "🔧 Starting SHL API with debug output..."
echo "=================================================="
echo ""
echo "🔍 Checking environment variables:"
echo "CHROMA_API_KEY: ${CHROMA_API_KEY:+set}"
echo "CHROMA_TENANT: ${CHROMA_TENANT:+set}"
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:+set}"
echo "PORT: ${PORT:-NOT SET}"
echo "🚀 Starting SHL API on port ${PORT:-10000}..."
# Skip all tests - start server directly
exec uvicorn backend.api.app:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1
