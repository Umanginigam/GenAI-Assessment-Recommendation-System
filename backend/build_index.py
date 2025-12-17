import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

faiss.omp_set_num_threads(1)

DATA_PATH = "data/shl_catalog_clean.csv"
INDEX_PATH = "data/shl_faiss.index"
META_PATH = "data/shl_metadata.pkl"

def main():
    df = pd.read_csv(DATA_PATH)

    model = SentenceTransformer("all-mpnet-base-v2", device="cpu")

    print("🔹 Generating embeddings...")
    embeddings = model.encode(
        df["search_text"].tolist(),
        batch_size=16,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dim = embeddings.shape[1]

    print("🔹 Building FAISS index...")
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    metadata = df[["assessment_name", "url", "test_type"]].to_dict("records")
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("✅ FAISS index saved:", INDEX_PATH)
    print("✅ Metadata saved:", META_PATH)
    print("Total indexed assessments:", index.ntotal)

if __name__ == "__main__":
    main()
