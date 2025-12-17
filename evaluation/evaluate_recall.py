import pandas as pd
from collections import defaultdict

from backend.pipeline import recommend
from evaluation.recall_at_k import recall_at_k

TRAIN_PATH = "data/Train.csv"

def main():
    df = pd.read_csv(TRAIN_PATH)

    # 🔧 FIX: normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    print("CSV columns after normalization:", df.columns.tolist())
    print(df.head(), "\n")

    # Build ground truth
    gt = defaultdict(list)
    for _, row in df.iterrows():
        gt[row["query"]].append(row["assessment_url"])

    recalls = []

    for query, true_urls in gt.items():
        results = recommend(query, max_results=10)
        predicted_urls = [r["url"] for r in results]

        r10 = recall_at_k(predicted_urls, true_urls, k=10)
        recalls.append(r10)

        print(f"Query: {query}")
        print(f"Recall@10: {r10:.2f}\n")

    mean_recall = sum(recalls) / len(recalls)
    print("================================")
    print(f"Mean Recall@10: {mean_recall:.3f}")
    print("================================")

if __name__ == "__main__":
    main()
