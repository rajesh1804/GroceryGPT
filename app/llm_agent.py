import requests
import os
from llm_utils import get_available_model

API_KEY = os.getenv("OPENROUTER_API_KEY")

def rerank_results(query, candidates):
    model_id = get_available_model()

    if not API_KEY:
        return "❌ OpenRouter API key not set. Please check your .env file."

    prompt = f"""You are a product ranking AI. User searched for: '{query}'. Rank these products:
{[c['name'] for c in candidates]}. After the re-ranked list, provide a brief explanation for the ranking."""

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = res.json()

        if "choices" not in data:
            print("🔍 Unexpected response from OpenRouter:", data)
            return "⚠️ Failed to rerank results — check API key, quota, or request format."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ LLM reranking failed:", e)
        return f"⚠️ Reranking failed: {e}"
