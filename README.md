# 🧠 GenAI-Assessment-Recommendation-System
An AI-powered assessment recommendation system that maps natural language hiring queries or job descriptions to the most relevant SHL Individual Test Solutions, using Retrieval-Augmented Generation (RAG), LLM-based intent extraction, and balanced recommendation logic.
This project was built as part of a GenAI take-home assessment, with an emphasis on problem-solving, context engineering, evaluation rigor, and explainability.
## 🚀 Key Features
🔍 Semantic Retrieval over 377+ SHL Individual Assessments
🧠 LLM-based Query Understanding (skills, behavior, role intent)
## ⚖️ Balanced Recommendations across:
Knowledge & Skills (K)
Personality & Behavior (P)
Simulations / Work Samples (S)
📊 Quantitative Evaluation using Mean Recall@10
🌐 FastAPI backend with strict API contract
💻 React + Tailwind frontend for easy testing
📈 Reproducible, modular, and interview-defensible design
## 🏗️ System Architecture
```bash
User Query / JD
      ↓
LLM-based Intent Extraction
      ↓
Expanded Semantic Query
      ↓
Embedding + Vector Search (FAISS)
      ↓
Top-K Candidate Retrieval
      ↓
Deterministic Balancing Logic (K / P / S)
      ↓
Final Recommendations (5–10)
```
## 📂 Project Structure
```bash SHL/
│
├── backend/
│   ├── api/              # FastAPI app (health, recommend)
│   ├── llm/              # LLM-based query understanding
│   ├── retriever/        # Embeddings + FAISS retrieval
│   ├── pipeline.py       # End-to-end recommendation pipeline
│
├── evaluation/
│   ├── evaluate_recall.py
│   ├── recall_at_k.py
│   ├── generate_test_predictions.py
│
├── data/
│   ├── shl_catalog_clean.csv
│   ├── Train.csv
│   ├── Test.csv
│
├── frontend/
│   └── shl-frontend/     # React + Tailwind UI
│
├── submission/
│   └── predictions.csv
│
├── flow.py               # Graphviz flowchart generation
└── README.md
```
## 📊 Data Pipeline
Crawling
SHL product catalog scraped using Playwright
Only Individual Test Solutions retained
Pre-packaged solutions explicitly excluded
Cleaning & Normalization
Text normalization
Test type mapping (K / P / S)
Construction of embedding-friendly search_text
Vector Indexing
Sentence-level embeddings
FAISS index for efficient semantic retrieval
## 🧠 Query Understanding (LLM)
The LLM is used only for structured intent extraction, not for recommendation generation.
### Extracted signals:
Technical skills (e.g., Java, Python, SQL)
Behavioral traits (e.g., collaboration, communication)
Role keywords
Seniority (when inferable)
## Example output:
```bash
{
  "technical_skills": ["Java"],
  "behavioral_skills": ["collaboration"],
  "role_keywords": ["developer"],
  "seniority": "unknown"
}
```
This structured intent guides retrieval and balancing.
## ⚖️ Balanced Recommendation Logic
Post-retrieval, a deterministic balancer ensures coverage across domains:
```bash
Test Type	Purpose
K	Technical knowledge & skills
P	Personality & behavioral traits
S	Simulation / reasoning ability
```
This avoids over-indexing on a single dimension and improves real-world relevance.
## 📈 Evaluation
Metric: Mean Recall@10
Dataset: Provided labeled train set
Challenge addressed: URL inconsistencies between labeled data and catalog
Solution: Canonical URL normalization before comparison
## Result
Mean Recall@10 ≈ 0.21
Clear improvement over baseline
Strong performance on skill-focused and behavioral queries
Evaluation scripts are fully reproducible.
## 🔌 API Endpoints (FastAPI)
Health Check
GET /health
Response:
```bash
{"status":"ok"}
```
Recommendation
POST /recommend
Request:
```bash
{ "query":"Java developer who works with business teams"}
```
Response:
```bash

  "recommended_assessments": [
    {
      "url": "https://www.shl.com/products/product-catalog/view/java-2-platform-enterprise-edition-1-4-fundamental/",
      "name": "Java 2 Platform Enterprise Edition 1.4 Fundamental",
      "adaptive_support": "No",
      "description": "Java 2 Platform Enterprise Edition 1.4 Fundamental: The Java 2 Platform Enterprise Edition (J2EE) 1.4 Fundamentals test measures knowledge of basic J2EE 1.4 Fundamentals. Designed for entry-level users, this…",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Knowledge & Skills"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/core-java-entry-level-new/",
      "name": "Core Java (Entry Level) (New)",
      "adaptive_support": "No",
      "description": "Core Java (Entry Level) (New): Multi-choice test that measures the knowledge of basic Java constructs, OOP concepts, file handling, exception handling, threads, generic class and inner class.",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Knowledge & Skills"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
      "name": "Core Java (Advanced Level) (New)",
      "adaptive_support": "No",
      "description": "Core Java (Advanced Level) (New): Multi-choice test that measures the knowledge of basic Java constructs, OOP concepts, files and exception handling, and advanced Java concepts like generics…",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Knowledge & Skills"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/java-web-services-new/",
      "name": "Java Web Services (New)",
      "adaptive_support": "No",
      "description": "Java Web Services (New): Multi-choice test that measures the knowledge of basic Java constructs, OOP concepts, file handling, exception handling, threads, generics and inner class.",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Knowledge & Skills"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "name": "Java 8 (New)",
      "adaptive_support": "No",
      "description": "Java 8 (New): Multi-choice test that measures the knowledge of Java class design, exceptions, generics, collections, concurrency, JDBC and Java I/O fundamentals.",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Knowledge & Skills"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/global-skills-development-report/",
      "name": "Global Skills Development Report",
      "adaptive_support": "No",
      "description": "Global Skills Development Report : This report is designed to be given to individuals who have completed the Global Skills Assessment (GSA). With coverage across the Great 8 Domains, this…",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Personality & Behavior"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/ai-skills/",
      "name": "AI Skills",
      "adaptive_support": "No",
      "description": "AI Skills : The AI Skills assessment measures the skills that help candidates successfully leverage AI in their work.",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Personality & Behavior"
      ]
    },
    {
      "url": "https://www.shl.com/products/product-catalog/view/verify-interactive-ability-report/",
      "name": "Verify Interactive Ability Report",
      "adaptive_support": "No",
      "description": "Verify Interactive Ability Report: Verify Interactive Ability Report",
      "duration": 60,
      "remote_support": "No",
      "test_type": [
        "Personality & Behavior"
      ]
    }]
```
CORS is explicitly enabled for frontend integration.
## 💻 Frontend
Built with React + Tailwind CSS
Simple, evaluator-friendly UI
Supports long JDs and natural language queries
Displays results in a tabular format
### ▶️ Running Locally
Backend
```bash
uvicorn backend.api.app:app --reload
```
Frontend
```bash
cd frontend/shl-frontend
npm install
npm run dev
```
## 🔮 Future Improvements
JD summarization before intent extraction
Learned re-ranking models
User feedback loop
Duration and geography-aware filtering
Multi-objective optimization (relevance vs diversity)
## 🧑‍🔬 Research & Engineering Focus
This project emphasizes:
Clear separation of modeling vs reasoning
Explainable GenAI usage
Evaluation-driven iteration
Avoidance of “vibe-coding”
It is designed to be defensible in technical interviews and extensible for further research.
## 📌 Author
Umangi Nigam
AI / Data Science | GenAI | RAG | LLMs