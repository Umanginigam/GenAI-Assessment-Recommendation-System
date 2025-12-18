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
echo "🐍 Testing Python imports..."
python -c "
import sys
print('✓ Python path:', sys.path[0])
try:
    from backend.api.app import app
    print('✓ App imported successfully')
except Exception as e:
    print('❌ Import failed:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

echo ""
echo "🚀 Starting uvicorn..."
exec uvicorn backend.api.app:app --host 0.0.0.0 --port ${PORT:-10000}
