from collections import defaultdict

from evaluation.utils import normalize_url

def recall_at_k(predicted_urls, true_urls, k=10):
    pred_ids = {normalize_url(u) for u in predicted_urls[:k]}
    true_ids = {normalize_url(u) for u in true_urls}

    hits = pred_ids & true_ids
    return len(hits) / len(true_ids) if true_ids else 0.0
