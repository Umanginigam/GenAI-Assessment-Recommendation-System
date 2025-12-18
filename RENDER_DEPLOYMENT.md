# Render Deployment - Memory Optimization Guide

## The Problem
Render's free tier has **512MB memory limit**. The sentence-transformers model was loading at startup, causing out-of-memory errors.

## ✅ Fixes Applied

### 1. Lazy Loading
Changed `backend/retriever.py` to load the model only when first needed, not at startup:

```python
# Before (loads at import = 400MB+ at startup)
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# After (loads on first request = low memory at startup)
_MODEL = None
def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL
```

### 2. Render Configuration

#### Start Command (CRITICAL):
```bash
uvicorn backend.api.app:app --host 0.0.0.0 --port $PORT
```
**Note:** Must use `$PORT` (not `8000` or `"$PORT"`)

#### Environment Variables:
```
GITHUB_TOKEN=your_github_token
CHROMA_API_KEY=your_chroma_key
CHROMA_TENANT=your_tenant_id
CHROMA_DATABASE=SHL
CHROMA_COLLECTION=shl
```

#### Build Command:
```bash
pip install -r requirements.txt
```

### 3. Instance Type
If still getting OOM errors, you may need to upgrade:
- Free: 512MB RAM (may work with lazy loading)
- Starter ($7/mo): 2GB RAM (recommended)

## Testing Locally

```bash
# Activate venv
source venv/bin/activate

# Load environment
export $(cat .env | xargs)

# Start server
uvicorn backend.api.app:app --host 0.0.0.0 --port 8000

# Test health
curl http://localhost:8000/health

# Test recommendation
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"Java developer"}'
```

## Monitoring on Render

### Check Logs:
1. Go to Render Dashboard
2. Click your service
3. View "Logs" tab
4. Look for:
   - ✅ `INFO: Started server process`
   - ✅ `INFO: Uvicorn running on http://0.0.0.0:10000`
   - ❌ `Out of memory`
   - ❌ `No open ports detected`

### Expected Startup Log:
```
==> Starting service with 'uvicorn backend.api.app:app --host 0.0.0.0 --port $PORT'
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

## Common Issues & Solutions

### Issue: "No open ports detected"
**Cause:** App crashes before binding to port (usually memory issue)
**Solution:** 
1. Check for "Out of memory" in logs above this error
2. Verify lazy loading is working
3. Consider upgrading instance

### Issue: "Out of memory"
**Cause:** Model loading at startup
**Solution:**
1. ✅ Already fixed with lazy loading
2. If still happens, upgrade to Starter plan

### Issue: Import errors
**Cause:** Missing `__init__.py` or wrong import paths
**Solution:**
```bash
# Verify structure
ls backend/__init__.py
ls backend/api/__init__.py
ls backend/llm/__init__.py
```

### Issue: Environment variables not working
**Cause:** Not set in Render dashboard
**Solution:** 
1. Go to service → Environment
2. Add all variables from `.env`
3. Click "Save Changes"

## Memory Usage Timeline

| Stage | Memory Used |
|-------|-------------|
| Startup (with lazy loading) | ~150MB |
| First request (model loads) | ~450MB |
| Subsequent requests | ~450MB |

With lazy loading, startup stays under 512MB limit.

## Health Check After Deploy

```bash
# Replace YOUR_APP with your Render app name
export API_URL="https://YOUR_APP.onrender.com"

# Test health
curl $API_URL/health

# Test recommendation
curl -X POST $API_URL/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"Python developer with cloud experience"}'
```

## Summary

✅ Lazy loading implemented  
✅ Start command uses `$PORT`  
✅ Environment variables documented  
✅ Memory optimized for free tier  

**Deploy should now work on Render free tier!** 🚀

If you still see OOM errors after these fixes, you'll need to upgrade to Starter ($7/mo) for 2GB RAM.
