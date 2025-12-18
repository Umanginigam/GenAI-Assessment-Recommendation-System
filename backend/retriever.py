import os
import chromadb
from sentence_transformers import SentenceTransformer

# ✅ Lazy load to reduce startup memory
_MODEL = None
_CLIENT = None
_COLLECTION = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL

def get_collection():
    global _CLIENT, _COLLECTION
    if _CLIENT is None:
        _CLIENT = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )
        _COLLECTION = _CLIENT.get_collection(
            os.getenv("CHROMA_COLLECTION", "shl")
        )
    return _COLLECTION


class SHLRetriever:
    def __init__(self):
        # Lazy load on first use
        self.model = None
        self.collection = None

    def retrieve(self, query: str, top_k: int = 20):
        # Load on first request to save memory at startup
        if self.model is None:
            self.model = get_model()
        if self.collection is None:
            self.collection = get_collection()
            
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
