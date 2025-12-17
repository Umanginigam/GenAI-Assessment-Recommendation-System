# import pandas as pd
# from backend.retriever import SHLRetriever, balance_results

# # ====== PATHS ======
# TEST_PATH = "data/test.csv"   # unlabeled test set
# OUTPUT_PATH = "submission/submission.csv"

# MAX_RESULTS = 10


# def load_test_queries(path):
#     if path.endswith(".csv"):
#         df = pd.read_csv(path)
#     else:
#         df = pd.read_excel(path)

#     return df.iloc[:, 0].dropna().tolist()


# def is_valid_individual_test(url):
#     url = url.lower()
#     forbidden_keywords = [
#         "solution",
#         "report",
#         "interview",
#         "remoteworkq",
#         "guide",
#         "on-demand"
#     ]
#     return not any(k in url for k in forbidden_keywords)

# def keyword_overlap_score(query, text):
#     q_tokens = set(query.lower().split())
#     t_tokens = set(text.lower().split())
#     return len(q_tokens & t_tokens)


# def main():
#     retriever = SHLRetriever()
#     queries = load_test_queries(TEST_PATH)

#     print("Loaded queries:", len(queries))

#     rows = []
#     for query in queries:
#         raw_results = retriever.retrieve(query, top_k=50)
#         balanced_results = balance_results(raw_results, max_results=50)
#         balanced_results = sorted(
#             balanced_results,
#             key=lambda x: keyword_overlap_score(query, x["assessment_name"]),
#             reverse=True
#         )
#         valid_results = []
#         for r in balanced_results:
#             if is_valid_individual_test(r["url"]):
#                 valid_results.append(r)
#                 if len(valid_results) == MAX_RESULTS:
#                    break

#     # safety: ensure at least 5
#     valid_results = valid_results[:MAX_RESULTS]

#     for r in valid_results:
#         rows.append({
#             "Query": query,
#             "Assessment_url": r["url"]
#         })

#     out_df = pd.DataFrame(rows)
#     out_df.to_csv(OUTPUT_PATH, index=False)

#     print("✅ Submission CSV generated:", OUTPUT_PATH)
#     print("Total rows:", len(out_df))


# if __name__ == "__main__":
#     main()
import pandas as pd
from backend.retriever import SHLRetriever, balance_results

TEST_PATH = "data/test.csv"
OUTPUT_PATH = "submission/submission.csv"

MIN_RESULTS = 5
MAX_RESULTS = 10


def main():
    df = pd.read_csv(TEST_PATH)
    queries = df.iloc[:, 0].dropna().tolist()

    print("Loaded queries:", len(queries))

    retriever = SHLRetriever()
    rows = []

    for query in queries:
        raw_results = retriever.retrieve(query, top_k=100)
        final_results = balance_results(raw_results, max_results=MAX_RESULTS)

        # 🔒 SAFETY: guarantee minimum 5
        if len(final_results) < MIN_RESULTS:
            final_results = raw_results[:MIN_RESULTS]

        final_results = final_results[:MAX_RESULTS]

        # ✅ IMPORTANT: this loop MUST be inside query loop
        for r in final_results:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Submission CSV generated:", OUTPUT_PATH)
    print("Total rows:", len(out_df))


if __name__ == "__main__":
    main()
