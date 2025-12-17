from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.pipeline import recommend

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0"
)

# ✅ CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Request / Response Models ----------

class RecommendRequest(BaseModel):
    query: str

class Assessment(BaseModel):
    assessment_name: str
    url: str

class RecommendResponse(BaseModel):
    recommendations: List[Assessment]

# ---------- Endpoints ----------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend", response_model=RecommendResponse)
def recommend_endpoint(req: RecommendRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = recommend(req.query, max_results=10)

    response = [
        {
            "assessment_name": r["assessment_name"],
            "url": r["url"]
        }
        for r in results
    ]

    return {"recommendations": response}
