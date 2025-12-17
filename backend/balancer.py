def balance_results(results, intent, max_results=10):
    """
    results: list of retrieved items (already ranked)
    intent: output from LLM
    """

    k_tests = [r for r in results if r["test_type"] == "K"]
    p_tests = [r for r in results if r["test_type"] == "P"]
    s_tests = [r for r in results if r["test_type"] == "S"]

    has_behavioral = len(intent.get("behavioral_skills", [])) > 0

    final = []

    # Always prioritize technical skills
    final.extend(k_tests[:5])

    if has_behavioral:
        final.extend(p_tests[:3])

    # Add simulations if available
    final.extend(s_tests[:2])

    # Fallback: fill from remaining
    if len(final) < max_results:
        remaining = [
            r for r in results if r not in final
        ]
        final.extend(remaining[: max_results - len(final)])

    return final[:max_results]
