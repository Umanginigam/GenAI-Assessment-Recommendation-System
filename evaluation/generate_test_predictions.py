import pandas as pd
from backend.pipeline import recommend

TEST_PATH = "data/Test.csv"
OUTPUT_PATH = "submission/predictions.csv"

def main():
    df = pd.read_csv(TEST_PATH)

    # Normalize column name
    df.columns = [c.strip().lower() for c in df.columns]

    rows = []

    for query in df["query"]:
        results = recommend(query, max_results=10)

        for r in results:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Test predictions saved to:", OUTPUT_PATH)
    print("Total rows:", len(out_df))

if __name__ == "__main__":
    main()
