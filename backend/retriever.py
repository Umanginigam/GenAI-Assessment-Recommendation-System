import os
import chromadb
from sentence_transformers import SentenceTransformer


class SHLRetriever:
    def __init__(self):
        # ---- Embedding model (same as before) ----
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # ---- Chroma Cloud client ----
        self.client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )

        # ---- Collection ----
        self.collection = self.client.get_collection(
            os.getenv("CHROMA_COLLECTION", "shl")
        )

    def retrieve(self, query: str, top_k: int = 20):
        # ---- Encode query ----
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        # ---- Query Chroma ----
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # ---- Format results (match your old output) ----
        retrieved = []
        metadatas = results.get("metadatas", [[]])[0]

        for meta in metadatas:
            retrieved.append({
                "assessment_name": meta.get("assessment_name"),
                "description": meta.get("description"),
                "test_type": meta.get("test_type"),
                "url": meta.get("url"),
            })

        return retrieved
