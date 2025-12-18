import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com"
)

MODEL_NAME = "gpt-4o-mini"   # or gpt-3.5-turbo

def extract_intent(query: str) -> dict:
    prompt = f"""
You are an assistant helping recommend hiring assessments.

Extract structured intent from the input.

Return ONLY valid JSON with:
- technical_skills: list of strings
- behavioral_skills: list of strings
- role_keywords: list of strings
- seniority: one of [entry, mid, senior, unknown]

Rules:
- Do not hallucinate skills
- Be concise
- If not mentioned, return empty lists

Input:
{query}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You extract structured hiring intent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        # Safe fallback (VERY IMPORTANT)
        return {
            "technical_skills": [],
            "behavioral_skills": [],
            "role_keywords": [],
            "seniority": "unknown"
        }
