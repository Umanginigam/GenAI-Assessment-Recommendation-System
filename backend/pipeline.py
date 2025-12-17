from llm.query_understanding import extract_intent
from backend.query_builder import build_expanded_query
from backend.retriever import SHLRetriever
from backend.balancer import balance_results

retriever = SHLRetriever()

def recommend(query, max_results=10):
    intent = extract_intent(query)
    expanded_query = build_expanded_query(intent)

    retrieved = retriever.retrieve(expanded_query, top_k=30)

    final = balance_results(
        results=retrieved,
        intent=intent,
        max_results=max_results
    )

    return final