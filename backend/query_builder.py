def build_expanded_query(intent: dict) -> str:
    parts = []

    if intent["technical_skills"]:
        parts.append(
            "Technical skills: " + ", ".join(intent["technical_skills"])
        )

    if intent["behavioral_skills"]:
        parts.append(
            "Behavioral skills: " + ", ".join(intent["behavioral_skills"])
        )

    if intent["role_keywords"]:
        parts.append(
            "Job role: " + ", ".join(intent["role_keywords"])
        )

    return ". ".join(parts)
