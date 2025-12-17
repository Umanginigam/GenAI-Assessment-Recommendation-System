from backend.pipeline import recommend

results = recommend(
    "Java developer who works with business stakeholders",
    max_results=10
)

for r in results:
    print(r["assessment_name"], r["test_type"])
