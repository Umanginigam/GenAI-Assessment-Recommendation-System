import os
import chromadb
from sentence_transformers import SentenceTransformer

# ✅ Load model ONCE
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load Chroma client ONCE
_CLIENT = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

_COLLECTION = _CLIENT.get_collection(
    os.getenv("CHROMA_COLLECTION", "shl")
)


class SHLRetriever:
    def __init__(self):
        self.model = _MODEL
        self.collection = _COLLECTION

    def retrieve(self, query: str, top_k: int = 20):
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved = []
        for meta in results.get("metadatas", [[]])[0]:
            retrieved.append({
                "assessment_name": meta.get("assessment_name"),
                "description": meta.get("description"),
                "test_type": meta.get("test_type"),
                "url": meta.get("url"),
            })

        return retrieved
