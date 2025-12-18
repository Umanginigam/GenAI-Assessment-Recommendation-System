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
        "http://127.0.0.1:5173",
       
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Request / Response Models ----------

class RecommendRequest(BaseModel):
    query: str

class Assessment(BaseModel):
    url: str
    name: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]

class RecommendResponse(BaseModel):
    recommended_assessments: List[Assessment]


# --------- Health ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# --------- Recommend ----------
@app.post("/recommend", response_model=RecommendResponse)
def recommend_assessments(req: RecommendRequest):
    results = recommend(req.query, max_results=10)

    if not results:
        raise HTTPException(
            status_code=200,
            detail="No recommendations found for the given query."
        )

    formatted = []
    for r in results[:10]:
        formatted.append({
            "url": r["url"],
            "name": r["assessment_name"],
            "adaptive_support": "Yes" if r.get("adaptive_irt", False) else "No",
            "description": r.get("description", ""),
            "duration": int(r.get("duration", 60)),
            "remote_support": "Yes" if r.get("remote_testing", False) else "No",
            "test_type": map_test_type(r.get("test_type"))
        })

    return {"recommended_assessments": formatted}

def map_test_type(t):
    mapping = {
        "K": "Knowledge & Skills",
        "P": "Personality & Behavior",
        "C": "Cognitive",
        "S": "Simulation"
    }
    if not t:
        return []
    return [mapping.get(t, t)]

