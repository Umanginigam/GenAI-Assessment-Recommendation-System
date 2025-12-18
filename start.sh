#!/bin/bash
set -e

echo "=================================================="
echo "🔧 Starting SHL API with debug output..."
echo "=================================================="

echo "📦 Python version:"
python --version

echo ""
echo "📍 Current directory:"
pwd

echo ""
echo "📂 Directory contents:"
ls -la

echo ""
echo "🔍 Checking environment variables:"
echo "CHROMA_API_KEY: ${CHROMA_API_KEY:+set}"
echo "CHROMA_TENANT: ${CHROMA_TENANT:+set}"
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:+set}"
echo "PORT: ${PORT:-NOT SET}"

echo ""
echo "🐍 Testing Python imports step by step..."

python -c "
import sys
import traceback

print('Step 1: Testing FastAPI...')
try:
    from fastapi import FastAPI
    print('✓ FastAPI imported')
except Exception as e:
    print('❌ FastAPI failed:', e)
    traceback.print_exc()
    sys.exit(1)

print('Step 2: Testing backend.retriever...')
try:
    from backend.retriever import SHLRetriever
    print('✓ Retriever imported')
except Exception as e:
    print('❌ Retriever failed:', e)
    traceback.print_exc()
    sys.exit(1)

print('Step 3: Testing backend.llm...')
try:
    from backend.llm.query_understanding import extract_intent
    print('✓ LLM imported')
except Exception as e:
    print('❌ LLM failed:', e)
    traceback.print_exc()
    sys.exit(1)

print('Step 4: Testing backend.pipeline...')
try:
    from backend.pipeline import recommend
    print('✓ Pipeline imported')
except Exception as e:
    print('❌ Pipeline failed:', e)
    traceback.print_exc()
    sys.exit(1)

print('Step 5: Testing backend.api.app...')
try:
    from backend.api.app import app
    print('✓ App imported successfully')
except Exception as e:
    print('❌ App import failed:', e)
    traceback.print_exc()
    sys.exit(1)

print('✅ All imports successful!')
" || exit 1

echo ""
echo "🚀 Starting uvicorn on port ${PORT:-10000}..."
exec uvicorn backend.api.app:app --host 0.0.0.0 --port ${PORT:-10000}
