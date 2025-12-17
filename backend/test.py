# from pathlib import Path
# import sys
# # Ensure local project folders are on sys.path so the 'retrieval' package can be imported
# _root = Path(__file__).resolve().parent
# sys.path.append(str(_root))
# sys.path.append(str(_root.parent))

# from backend.retriever import SHLRetriever

# retriever = SHLRetriever()

# query = "Java developer who works with business stakeholders"
# results = retriever.retrieve(query, top_k=10)

# for r in results:
#     print(r["assessment_name"], r["test_type"], r["score"])

from backend.pipeline import recommend

results = recommend(
    "Java developer who works with business stakeholders",
    max_results=10
)

for r in results:
    print(r["assessment_name"], r["test_type"])
