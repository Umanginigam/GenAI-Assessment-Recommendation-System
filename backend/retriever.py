import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/shl_faiss.index"
META_PATH = "data/shl_metadata.pkl"

class SHLRetriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def retrieve(self, query, top_k=20):
        q_emb = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(q_emb, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            item = self.metadata[idx]
            item["score"] = float(score)
            results.append(item)

        return results
